"""
Training Reports API endpoints
Migrated from Flask k9/api/trainer_daily_api.py
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from uuid import UUID

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.core.rate_limit import limiter, RateLimits, pdf_export_rate_limit
from app.models import User

# Import Flask services (reuse business logic)
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from k9.services.trainer_daily_services import get_trainer_daily, export_trainer_daily_pdf
from k9.models.models import AuditAction
from k9.utils.utils import log_audit

router = APIRouter()


# ============================================================================
# Pydantic Schemas
# ============================================================================

class TrainerDailyRequest(BaseModel):
    """Request schema for trainer daily report"""
    date: date = Field(..., description="Report date in YYYY-MM-DD format")
    project_id: Optional[UUID] = Field(None, description="Optional filter by project UUID")
    trainer_id: Optional[UUID] = Field(None, description="Optional filter by trainer UUID")
    dog_id: Optional[UUID] = Field(None, description="Optional filter by dog UUID")
    category: Optional[str] = Field(None, description="Optional filter by training category")


class PDFExportResponse(BaseModel):
    """Response schema for PDF export endpoints"""
    path: str = Field(..., description="Path to generated PDF file")
    success: bool = True


# ============================================================================
# Trainer Daily Report Endpoints
# ============================================================================

@router.post(
    "/trainer-daily/run",
    summary="Run Trainer Daily Report",
    description="Generate trainer daily report data in JSON format with optional filters"
)
@limiter.limit(RateLimits.STANDARD)
async def run_trainer_daily(
    request: Request,
    data: TrainerDailyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate trainer daily report
    
    - **date**: Report date (YYYY-MM-DD) - required
    - **project_id**: Optional filter by project UUID
    - **trainer_id**: Optional filter by trainer UUID
    - **dog_id**: Optional filter by dog UUID
    - **category**: Optional filter by training category
    
    Returns detailed training activity report data
    
    Note: PROJECT_MANAGER role requires project_id parameter
    """
    try:
        # Validate PROJECT_MANAGER has project_id
        if current_user.role.value == "PROJECT_MANAGER" and not data.project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project ID is required for PROJECT_MANAGER"
            )
        
        # Get report data
        result = get_trainer_daily(
            project_id=str(data.project_id) if data.project_id else None,
            date_filter=data.date,
            trainer_id=str(data.trainer_id) if data.trainer_id else None,
            dog_id=str(data.dog_id) if data.dog_id else None,
            category=data.category,
            user=current_user
        )
        
        # Log audit trail
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='TrainingReport',
            target_id=str(data.project_id) if data.project_id else None,
            description=f"Generated trainer daily report for date {data.date}",
            old_values={},
            new_values={"report_type": "trainer_daily", "date": str(data.date)}
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/trainer-daily/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Trainer Daily Report as PDF",
    description="Generate and export trainer daily report as PDF file"
)
@limiter.limit(pdf_export_rate_limit)
async def export_pdf_trainer_daily(
    request: Request,
    data: TrainerDailyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export trainer daily report as PDF
    
    - **date**: Report date (YYYY-MM-DD) - required
    - **project_id**: Optional filter by project UUID
    - **trainer_id**: Optional filter by trainer UUID
    - **dog_id**: Optional filter by dog UUID
    - **category**: Optional filter by training category
    
    Returns path to generated PDF file
    """
    try:
        # Validate PROJECT_MANAGER has project_id
        if current_user.role.value == "PROJECT_MANAGER" and not data.project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project ID is required for PROJECT_MANAGER"
            )
        
        # Get report data first
        report_data = get_trainer_daily(
            project_id=str(data.project_id) if data.project_id else None,
            date_filter=data.date,
            trainer_id=str(data.trainer_id) if data.trainer_id else None,
            dog_id=str(data.dog_id) if data.dog_id else None,
            category=data.category,
            user=current_user
        )
        
        # Generate PDF
        pdf_path = export_trainer_daily_pdf(report_data)
        
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
            target_type='TrainingReport',
            target_id=str(data.project_id) if data.project_id else None,
            description=f"Exported trainer daily PDF for date {data.date}",
            old_values={},
            new_values={"report_type": "trainer_daily_pdf", "date": str(data.date), "file_path": pdf_path}
        )
        
        return PDFExportResponse(path=pdf_path)
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
