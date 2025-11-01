"""
Attendance Reports API endpoints
Migrated from Flask k9/api/attendance_reporting_api.py and k9/api/pm_daily_api.py
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.core.rate_limit import limiter, RateLimits, pdf_export_rate_limit
from app.models import User
from app.schemas.common import MessageResponse

# Import Flask services (we'll reuse business logic)
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from k9.services.attendance_reporting_services import (
    get_daily_sheet, 
    validate_project_date_access,
    get_user_accessible_projects
)
from k9.services.pm_daily_services import get_pm_daily
from k9.models.models import AuditAction
from k9.utils.utils import log_audit

router = APIRouter()


# ============================================================================
# Pydantic Schemas
# ============================================================================

class DailySheetRequest(BaseModel):
    """Request schema for daily attendance sheet"""
    project_id: UUID = Field(..., description="Project UUID")
    date: date = Field(..., description="Report date in YYYY-MM-DD format")


class PMDailyRequest(BaseModel):
    """Request schema for PM daily report"""
    project_id: UUID = Field(..., description="Project UUID")
    date: date = Field(..., description="Report date in YYYY-MM-DD format")


class ProjectInfo(BaseModel):
    """Project information schema"""
    id: str
    name: str
    code: str


class ProjectsResponse(BaseModel):
    """Response schema for accessible projects list"""
    projects: List[ProjectInfo]


class PDFExportResponse(BaseModel):
    """Response schema for PDF export endpoints"""
    path: str = Field(..., description="Path to generated PDF file")
    success: bool = True


# ============================================================================
# Daily Sheet Endpoints
# ============================================================================

@router.post(
    "/daily-sheet/run",
    summary="Run Daily Attendance Sheet Report",
    description="Generate daily attendance sheet report data in JSON format"
)
@limiter.limit(RateLimits.STANDARD)
async def run_daily_sheet(
    request: Request,
    data: DailySheetRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate daily attendance sheet report
    
    - **project_id**: Project UUID
    - **date**: Report date (YYYY-MM-DD)
    
    Returns detailed attendance data with employee check-ins/outs
    """
    try:
        # Validate user access to project and date
        if not validate_project_date_access(str(data.project_id), data.date, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied for this project"
            )
        
        # Get daily sheet data
        result = get_daily_sheet(str(data.project_id), data.date, current_user)
        
        # Log audit trail
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='AttendanceReport',
            target_id=str(data.project_id),
            description=f"Generated daily attendance sheet for project {data.project_id} on {data.date}",
            old_values={},
            new_values={"report_type": "daily_sheet", "date": str(data.date)}
        )
        
        return result
        
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/daily-sheet/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Daily Sheet as PDF",
    description="Generate and export daily attendance sheet as PDF file"
)
@limiter.limit(pdf_export_rate_limit)
async def export_pdf_daily_sheet(
    request: Request,
    data: DailySheetRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export daily attendance sheet as PDF
    
    - **project_id**: Project UUID
    - **date**: Report date (YYYY-MM-DD)
    
    Returns path to generated PDF file
    """
    try:
        # Validate user access to project and date
        if not validate_project_date_access(str(data.project_id), data.date, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied for this project"
            )
        
        # Get daily sheet data first
        sheet_data = get_daily_sheet(str(data.project_id), data.date, current_user)
        
        # Export to PDF
        pdf_path = export_daily_attendance_pdf(sheet_data)
        
        # Verify file was created
        if not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate PDF file"
            )
        
        # Log audit trail
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='AttendanceReport',
            target_id=str(data.project_id),
            description=f"Exported daily attendance sheet PDF for project {data.project_id} on {data.date}",
            old_values={},
            new_values={"report_type": "daily_sheet_pdf", "date": str(data.date), "file_path": pdf_path}
        )
        
        return PDFExportResponse(path=pdf_path)
        
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# PM Daily Report Endpoints
# ============================================================================

@router.post(
    "/pm-daily/run",
    summary="Run PM Daily Report",
    description="Generate Project Manager daily report data in JSON format"
)
@limiter.limit(RateLimits.STANDARD)
async def run_pm_daily(
    request: Request,
    data: PMDailyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate PM daily report
    
    - **project_id**: Project UUID
    - **date**: Report date (YYYY-MM-DD)
    
    Returns detailed project management daily report data
    """
    try:
        # Get report data (service handles access control)
        result = get_pm_daily(str(data.project_id), str(data.date), current_user)
        
        # Log audit trail
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='PMDailyReport',
            target_id=str(data.project_id),
            description=f"Generated PM daily report for project {data.project_id} on {data.date}",
            old_values={},
            new_values={"report_type": "pm_daily", "date": str(data.date)}
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# ============================================================================
# Helper Endpoints
# ============================================================================

@router.get(
    "/projects",
    response_model=ProjectsResponse,
    summary="Get Accessible Projects",
    description="Get list of projects accessible to current user for attendance reporting"
)
@limiter.limit(RateLimits.LIST)
async def get_accessible_projects(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get list of projects accessible to the current user
    
    Returns list of projects with id, name, and code
    """
    try:
        projects = get_user_accessible_projects(current_user)
        return ProjectsResponse(projects=projects)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch accessible projects"
        )
