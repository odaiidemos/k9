"""
Breeding Reports API endpoints
Migrated from Flask APIs:
- k9/api/breeding_feeding_reports_api.py (feeding logs CRUD, daily/weekly/unified reports, PDF exports)
- k9/api/breeding_checkup_reports_api.py (checkup logs CRUD, daily/weekly/unified reports, PDF exports)
- k9/api/veterinary_reports_api.py (unified veterinary reports, PDF exports)
- k9/api/caretaker_daily_report_api.py (unified caretaker reports, PDF exports)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date as date_type
from uuid import UUID

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.core.rate_limit import limiter, RateLimits, pdf_export_rate_limit
from app.models import User
from app.schemas.common import MessageResponse

import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from k9.models.models import AuditAction
from k9.utils.utils import log_audit

router = APIRouter()


# ============================================================================
# Pydantic Schemas
# ============================================================================

class PDFExportResponse(BaseModel):
    """Response schema for PDF export endpoints"""
    path: str = Field(..., description="Path to generated PDF file")
    success: bool = True


# ============================================================================
# Helper function to call Flask blueprints from FastAPI
# ============================================================================

def call_flask_endpoint(blueprint_name: str, function_name: str, query_params: dict, current_user: User) -> Any:
    """
    Helper function to call Flask blueprint endpoints from FastAPI
    
    Args:
        blueprint_name: Name of the Flask blueprint module
        function_name: Name of the function in the blueprint
        query_params: Query parameters as dict
        current_user: Current authenticated user
        
    Returns:
        Response from Flask endpoint
    """
    from flask import Flask
    from flask_login import AnonymousUserMixin
    
    app = Flask(__name__)
    
    # Build query string
    query_string = '&'.join([f'{k}={v}' for k, v in query_params.items() if v is not None])
    
    # Import the blueprint
    if blueprint_name == 'feeding':
        from k9.api.breeding_feeding_reports_api import bp as flask_bp
    elif blueprint_name == 'checkup':
        from k9.api.breeding_checkup_reports_api import bp as flask_bp
    elif blueprint_name == 'veterinary':
        from k9.api.veterinary_reports_api import bp as flask_bp
    elif blueprint_name == 'caretaker':
        from k9.api.caretaker_daily_report_api import bp as flask_bp
    else:
        raise ValueError(f"Unknown blueprint: {blueprint_name}")
    
    # Call the Flask endpoint in test context
    with app.test_request_context(f'/?{query_string}'):
        from flask import g
        g.user = current_user
        
        # Get the function from the blueprint
        response = flask_bp.view_functions[function_name]()
        
        # Handle tuple responses (data, status_code)
        if isinstance(response, tuple) and len(response) >= 2:
            result_data = response[0]
            status_code_val = int(response[1]) if len(response) > 1 else 200
            
            if status_code_val != 200:
                error_msg = result_data.get('error', 'Error') if isinstance(result_data, dict) else 'Error'
                raise HTTPException(status_code=status_code_val, detail=error_msg)
            return result_data
        
        return response


# ============================================================================
# FEEDING REPORTS ENDPOINTS
# ============================================================================

@router.get(
    "/feeding/daily",
    summary="Get Daily Feeding Report",
    description="Generate daily feeding report data with KPIs and detailed rows",
    tags=["Feeding Reports"]
)
@limiter.limit(RateLimits.STANDARD)
async def get_feeding_daily(
    request: Request,
    date: date_type = Query(..., description="Report date"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get daily feeding report data
    
    - **date**: Report date (YYYY-MM-DD) - required
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    - **page**: Page number for pagination
    - **per_page**: Results per page (max 100)
    
    Returns detailed feeding logs with KPIs
    """
    try:
        return call_flask_endpoint(
            'feeding',
            'feeding_daily_data',
            {
                'date': str(date),
                'project_id': project_id or '',
                'dog_id': dog_id or '',
                'page': page,
                'per_page': per_page
            },
            current_user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/feeding/weekly",
    summary="Get Weekly Feeding Report",
    description="Generate weekly feeding report data with aggregated KPIs",
    tags=["Feeding Reports"]
)
@limiter.limit(RateLimits.STANDARD)
async def get_feeding_weekly(
    request: Request,
    date: date_type = Query(..., description="Date within target week"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get weekly feeding report data
    
    - **date**: Date within the target week (YYYY-MM-DD) - required
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    - **page**: Page number for pagination
    - **per_page**: Results per page (max 100)
    
    Returns aggregated feeding data for the week
    """
    try:
        return call_flask_endpoint(
            'feeding',
            'feeding_weekly_data',
            {
                'date': str(date),
                'project_id': project_id or '',
                'dog_id': dog_id or '',
                'page': page,
                'per_page': per_page
            },
            current_user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/feeding/unified",
    summary="Get Unified Feeding Report",
    description="Generate unified feeding report with flexible range selector (daily/weekly/monthly/custom)",
    tags=["Feeding Reports"]
)
@limiter.limit(RateLimits.STANDARD)
async def get_feeding_unified(
    request: Request,
    range_type: str = Query(..., description="Range type: daily, weekly, monthly, custom"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    date: Optional[date_type] = Query(None, description="For daily range type"),
    week_start: Optional[date_type] = Query(None, description="For weekly range type"),
    year_month: Optional[str] = Query(None, description="For monthly range type (YYYY-MM)"),
    date_from: Optional[date_type] = Query(None, description="For custom range type"),
    date_to: Optional[date_type] = Query(None, description="For custom range type"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get unified feeding report with range selector
    
    - **range_type**: daily, weekly, monthly, or custom
    - **date**: For daily range type
    - **week_start**: For weekly range type
    - **year_month**: For monthly range type (YYYY-MM)
    - **date_from / date_to**: For custom range type
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns feeding data with smart aggregation based on date range
    """
    try:
        params = {
            'range_type': range_type,
            'project_id': project_id or '',
            'dog_id': dog_id or '',
            'page': page,
            'per_page': per_page
        }
        if date:
            params['date'] = str(date)
        if week_start:
            params['week_start'] = str(week_start)
        if year_month:
            params['year_month'] = year_month
        if date_from:
            params['date_from'] = str(date_from)
        if date_to:
            params['date_to'] = str(date_to)
        
        return call_flask_endpoint('feeding', 'feeding_unified_data', params, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/feeding/daily/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Daily Feeding Report as PDF",
    description="Generate and export daily feeding report as PDF file",
    tags=["Feeding Reports"]
)
@limiter.limit(pdf_export_rate_limit)
async def export_feeding_daily_pdf(
    request: Request,
    date: date_type = Query(..., description="Report date"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export daily feeding report as PDF
    
    - **date**: Report date (YYYY-MM-DD)
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns path to generated PDF file
    """
    try:
        result = call_flask_endpoint(
            'feeding',
            'export_daily_pdf',
            {
                'date': str(date),
                'project_id': project_id or '',
                'dog_id': dog_id or ''
            },
            current_user
        )
        
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='FeedingReport',
            target_id=project_id,
            description=f"Exported feeding daily PDF for date {date}",
            old_values={},
            new_values={"report_type": "feeding_daily_pdf", "date": str(date)}
        )
        
        if isinstance(result, dict) and 'path' in result:
            return PDFExportResponse(path=result['path'])
        raise HTTPException(status_code=500, detail="PDF export failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/feeding/weekly/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Weekly Feeding Report as PDF",
    description="Generate and export weekly feeding report as PDF file",
    tags=["Feeding Reports"]
)
@limiter.limit(pdf_export_rate_limit)
async def export_feeding_weekly_pdf(
    request: Request,
    date: date_type = Query(..., description="Date within target week"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export weekly feeding report as PDF
    
    - **date**: Date within target week (YYYY-MM-DD)
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns path to generated PDF file
    """
    try:
        result = call_flask_endpoint(
            'feeding',
            'export_weekly_pdf',
            {
                'date': str(date),
                'project_id': project_id or '',
                'dog_id': dog_id or ''
            },
            current_user
        )
        
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='FeedingReport',
            target_id=project_id,
            description=f"Exported feeding weekly PDF for date {date}",
            old_values={},
            new_values={"report_type": "feeding_weekly_pdf", "date": str(date)}
        )
        
        if isinstance(result, dict) and 'path' in result:
            return PDFExportResponse(path=result['path'])
        raise HTTPException(status_code=500, detail="PDF export failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/feeding/unified/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Unified Feeding Report as PDF",
    description="Generate and export unified feeding report as PDF file",
    tags=["Feeding Reports"]
)
@limiter.limit(pdf_export_rate_limit)
async def export_feeding_unified_pdf(
    request: Request,
    range_type: str = Query(..., description="Range type: daily, weekly, monthly, custom"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    date: Optional[date_type] = Query(None, description="For daily range type"),
    week_start: Optional[date_type] = Query(None, description="For weekly range type"),
    year_month: Optional[str] = Query(None, description="For monthly range type (YYYY-MM)"),
    date_from: Optional[date_type] = Query(None, description="For custom range type"),
    date_to: Optional[date_type] = Query(None, description="For custom range type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export unified feeding report as PDF
    
    - **range_type**: daily, weekly, monthly, or custom
    - **date**: For daily range type
    - **week_start**: For weekly range type
    - **year_month**: For monthly range type (YYYY-MM)
    - **date_from / date_to**: For custom range type
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns path to generated PDF file
    """
    try:
        params = {
            'range_type': range_type,
            'project_id': project_id or '',
            'dog_id': dog_id or ''
        }
        if date:
            params['date'] = str(date)
        if week_start:
            params['week_start'] = str(week_start)
        if year_month:
            params['year_month'] = year_month
        if date_from:
            params['date_from'] = str(date_from)
        if date_to:
            params['date_to'] = str(date_to)
        
        result = call_flask_endpoint('feeding', 'feeding_unified_export_pdf', params, current_user)
        
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='FeedingReport',
            target_id=project_id,
            description=f"Exported feeding unified PDF for range {range_type}",
            old_values={},
            new_values={"report_type": "feeding_unified_pdf", "range_type": range_type}
        )
        
        if isinstance(result, dict) and 'path' in result:
            return PDFExportResponse(path=result['path'])
        raise HTTPException(status_code=500, detail="PDF export failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# CHECKUP REPORTS ENDPOINTS
# ============================================================================

@router.get(
    "/checkup/daily",
    summary="Get Daily Checkup Report",
    description="Generate daily checkup report data with KPIs and detailed rows",
    tags=["Checkup Reports"]
)
@limiter.limit(RateLimits.STANDARD)
async def get_checkup_daily(
    request: Request,
    date: date_type = Query(..., description="Report date"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get daily checkup report data
    
    - **date**: Report date (YYYY-MM-DD) - required
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    - **page**: Page number for pagination
    - **per_page**: Results per page (max 100)
    
    Returns detailed checkup logs with KPIs
    """
    try:
        return call_flask_endpoint(
            'checkup',
            'checkup_daily_data',
            {
                'date': str(date),
                'project_id': project_id or '',
                'dog_id': dog_id or '',
                'page': page,
                'per_page': per_page
            },
            current_user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/checkup/weekly",
    summary="Get Weekly Checkup Report",
    description="Generate weekly checkup report data with aggregated KPIs",
    tags=["Checkup Reports"]
)
@limiter.limit(RateLimits.STANDARD)
async def get_checkup_weekly(
    request: Request,
    date: date_type = Query(..., description="Date within target week"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get weekly checkup report data
    
    - **date**: Date within the target week (YYYY-MM-DD) - required
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    - **page**: Page number for pagination
    - **per_page**: Results per page (max 100)
    
    Returns aggregated checkup data for the week
    """
    try:
        return call_flask_endpoint(
            'checkup',
            'checkup_weekly_data',
            {
                'date': str(date),
                'project_id': project_id or '',
                'dog_id': dog_id or '',
                'page': page,
                'per_page': per_page
            },
            current_user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/checkup/unified",
    summary="Get Unified Checkup Report",
    description="Generate unified checkup report with flexible range selector (daily/weekly/monthly/custom)",
    tags=["Checkup Reports"]
)
@limiter.limit(RateLimits.STANDARD)
async def get_checkup_unified(
    request: Request,
    range_type: str = Query(..., description="Range type: daily, weekly, monthly, custom"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    date: Optional[date_type] = Query(None, description="For daily range type"),
    week_start: Optional[date_type] = Query(None, description="For weekly range type"),
    year_month: Optional[str] = Query(None, description="For monthly range type (YYYY-MM)"),
    date_from: Optional[date_type] = Query(None, description="For custom range type"),
    date_to: Optional[date_type] = Query(None, description="For custom range type"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get unified checkup report with range selector
    
    - **range_type**: daily, weekly, monthly, or custom
    - **date**: For daily range type
    - **week_start**: For weekly range type
    - **year_month**: For monthly range type (YYYY-MM)
    - **date_from / date_to**: For custom range type
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns checkup data with smart aggregation based on date range
    """
    try:
        params = {
            'range_type': range_type,
            'project_id': project_id or '',
            'dog_id': dog_id or '',
            'page': page,
            'per_page': per_page
        }
        if date:
            params['date'] = str(date)
        if week_start:
            params['week_start'] = str(week_start)
        if year_month:
            params['year_month'] = year_month
        if date_from:
            params['date_from'] = str(date_from)
        if date_to:
            params['date_to'] = str(date_to)
        
        return call_flask_endpoint('checkup', 'checkup_unified_data', params, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/checkup/daily/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Daily Checkup Report as PDF",
    description="Generate and export daily checkup report as PDF file",
    tags=["Checkup Reports"]
)
@limiter.limit(pdf_export_rate_limit)
async def export_checkup_daily_pdf(
    request: Request,
    date: date_type = Query(..., description="Report date"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export daily checkup report as PDF
    
    - **date**: Report date (YYYY-MM-DD)
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns path to generated PDF file
    """
    try:
        result = call_flask_endpoint(
            'checkup',
            'export_checkup_daily_pdf',
            {
                'date': str(date),
                'project_id': project_id or '',
                'dog_id': dog_id or ''
            },
            current_user
        )
        
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='CheckupReport',
            target_id=project_id,
            description=f"Exported checkup daily PDF for date {date}",
            old_values={},
            new_values={"report_type": "checkup_daily_pdf", "date": str(date)}
        )
        
        if isinstance(result, dict) and 'path' in result:
            return PDFExportResponse(path=result['path'])
        raise HTTPException(status_code=500, detail="PDF export failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/checkup/weekly/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Weekly Checkup Report as PDF",
    description="Generate and export weekly checkup report as PDF file",
    tags=["Checkup Reports"]
)
@limiter.limit(pdf_export_rate_limit)
async def export_checkup_weekly_pdf(
    request: Request,
    date: date_type = Query(..., description="Date within target week"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export weekly checkup report as PDF
    
    - **date**: Date within target week (YYYY-MM-DD)
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns path to generated PDF file
    """
    try:
        result = call_flask_endpoint(
            'checkup',
            'export_checkup_weekly_pdf',
            {
                'date': str(date),
                'project_id': project_id or '',
                'dog_id': dog_id or ''
            },
            current_user
        )
        
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='CheckupReport',
            target_id=project_id,
            description=f"Exported checkup weekly PDF for date {date}",
            old_values={},
            new_values={"report_type": "checkup_weekly_pdf", "date": str(date)}
        )
        
        if isinstance(result, dict) and 'path' in result:
            return PDFExportResponse(path=result['path'])
        raise HTTPException(status_code=500, detail="PDF export failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/checkup/unified/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Unified Checkup Report as PDF",
    description="Generate and export unified checkup report as PDF file",
    tags=["Checkup Reports"]
)
@limiter.limit(pdf_export_rate_limit)
async def export_checkup_unified_pdf(
    request: Request,
    range_type: str = Query(..., description="Range type: daily, weekly, monthly, custom"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    date: Optional[date_type] = Query(None, description="For daily range type"),
    week_start: Optional[date_type] = Query(None, description="For weekly range type"),
    year_month: Optional[str] = Query(None, description="For monthly range type (YYYY-MM)"),
    date_from: Optional[date_type] = Query(None, description="For custom range type"),
    date_to: Optional[date_type] = Query(None, description="For custom range type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export unified checkup report as PDF
    
    - **range_type**: daily, weekly, monthly, or custom
    - **date**: For daily range type
    - **week_start**: For weekly range type
    - **year_month**: For monthly range type (YYYY-MM)
    - **date_from / date_to**: For custom range type
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns path to generated PDF file
    """
    try:
        params = {
            'range_type': range_type,
            'project_id': project_id or '',
            'dog_id': dog_id or ''
        }
        if date:
            params['date'] = str(date)
        if week_start:
            params['week_start'] = str(week_start)
        if year_month:
            params['year_month'] = year_month
        if date_from:
            params['date_from'] = str(date_from)
        if date_to:
            params['date_to'] = str(date_to)
        
        result = call_flask_endpoint('checkup', 'checkup_unified_export_pdf', params, current_user)
        
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='CheckupReport',
            target_id=project_id,
            description=f"Exported checkup unified PDF for range {range_type}",
            old_values={},
            new_values={"report_type": "checkup_unified_pdf", "range_type": range_type}
        )
        
        if isinstance(result, dict) and 'path' in result:
            return PDFExportResponse(path=result['path'])
        raise HTTPException(status_code=500, detail="PDF export failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# VETERINARY REPORTS ENDPOINTS
# ============================================================================

@router.get(
    "/veterinary/unified",
    summary="Get Unified Veterinary Report",
    description="Generate unified veterinary report with flexible range selector (daily/weekly/monthly/custom)",
    tags=["Veterinary Reports"]
)
@limiter.limit(RateLimits.STANDARD)
async def get_veterinary_unified(
    request: Request,
    range_type: str = Query("daily", description="Range type: daily, weekly, monthly, custom"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    show_kpis: bool = Query(True, description="Include KPI calculations"),
    date: Optional[date_type] = Query(None, description="For daily range type"),
    week_start: Optional[date_type] = Query(None, description="For weekly range type"),
    year_month: Optional[str] = Query(None, description="For monthly range type (YYYY-MM)"),
    date_from: Optional[date_type] = Query(None, description="For custom range type"),
    date_to: Optional[date_type] = Query(None, description="For custom range type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get unified veterinary report with range selector
    
    - **range_type**: daily, weekly, monthly, or custom
    - **date**: For daily range type
    - **week_start**: For weekly range type
    - **year_month**: For monthly range type (YYYY-MM)
    - **date_from / date_to**: For custom range type
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    - **show_kpis**: Include KPI calculations
    
    Returns veterinary visit data with smart aggregation based on date range
    """
    try:
        params = {
            'range_type': range_type,
            'project_id': project_id or '',
            'dog_id': dog_id or '',
            'show_kpis': '1' if show_kpis else '0'
        }
        if date:
            params['date'] = str(date)
        if week_start:
            params['week_start'] = str(week_start)
        if year_month:
            params['year_month'] = year_month
        if date_from:
            params['date_from'] = str(date_from)
        if date_to:
            params['date_to'] = str(date_to)
        
        return call_flask_endpoint('veterinary', 'veterinary_data', params, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/veterinary/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Veterinary Report as PDF",
    description="Generate and export veterinary report as PDF file",
    tags=["Veterinary Reports"]
)
@limiter.limit(pdf_export_rate_limit)
async def export_veterinary_pdf(
    request: Request,
    range_type: str = Query("daily", description="Range type: daily, weekly, monthly, custom"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    date: Optional[date_type] = Query(None, description="For daily range type"),
    week_start: Optional[date_type] = Query(None, description="For weekly range type"),
    year_month: Optional[str] = Query(None, description="For monthly range type (YYYY-MM)"),
    date_from: Optional[date_type] = Query(None, description="For custom range type"),
    date_to: Optional[date_type] = Query(None, description="For custom range type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export veterinary report as PDF
    
    - **range_type**: daily, weekly, monthly, or custom
    - **date**: For daily range type
    - **week_start**: For weekly range type
    - **year_month**: For monthly range type (YYYY-MM)
    - **date_from / date_to**: For custom range type
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns path to generated PDF file
    """
    try:
        params = {
            'range_type': range_type,
            'project_id': project_id or '',
            'dog_id': dog_id or ''
        }
        if date:
            params['date'] = str(date)
        if week_start:
            params['week_start'] = str(week_start)
        if year_month:
            params['year_month'] = year_month
        if date_from:
            params['date_from'] = str(date_from)
        if date_to:
            params['date_to'] = str(date_to)
        
        result = call_flask_endpoint('veterinary', 'export_pdf', params, current_user)
        
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='VeterinaryReport',
            target_id=project_id,
            description=f"Exported veterinary PDF for range {range_type}",
            old_values={},
            new_values={"report_type": "veterinary_pdf", "range_type": range_type}
        )
        
        if isinstance(result, dict) and 'path' in result:
            return PDFExportResponse(path=result['path'])
        raise HTTPException(status_code=500, detail="PDF export failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# CARETAKER REPORTS ENDPOINTS
# ============================================================================

@router.get(
    "/caretaker/unified",
    summary="Get Unified Caretaker Daily Report",
    description="Generate unified caretaker daily report with flexible range selector (daily/weekly/monthly/custom)",
    tags=["Caretaker Reports"]
)
@limiter.limit(RateLimits.STANDARD)
async def get_caretaker_unified(
    request: Request,
    range_type: str = Query("daily", description="Range type: daily, weekly, monthly, custom"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    date: Optional[date_type] = Query(None, description="For daily range type"),
    week_start: Optional[date_type] = Query(None, description="For weekly range type"),
    year_month: Optional[str] = Query(None, description="For monthly range type (YYYY-MM)"),
    date_from: Optional[date_type] = Query(None, description="For custom range type"),
    date_to: Optional[date_type] = Query(None, description="For custom range type"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get unified caretaker daily report with range selector
    
    - **range_type**: daily, weekly, monthly, or custom
    - **date**: For daily range type
    - **week_start**: For weekly range type
    - **year_month**: For monthly range type (YYYY-MM)
    - **date_from / date_to**: For custom range type
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns caretaker daily log data with smart aggregation based on date range
    """
    try:
        params = {
            'range_type': range_type,
            'project_id': project_id or '',
            'dog_id': dog_id or '',
            'page': page,
            'per_page': per_page
        }
        if date:
            params['date'] = str(date)
        if week_start:
            params['week_start'] = str(week_start)
        if year_month:
            params['year_month'] = year_month
        if date_from:
            params['date_from'] = str(date_from)
        if date_to:
            params['date_to'] = str(date_to)
        
        return call_flask_endpoint('caretaker', 'caretaker_daily_unified_data', params, current_user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/caretaker/export-pdf",
    response_model=PDFExportResponse,
    summary="Export Caretaker Daily Report as PDF",
    description="Generate and export caretaker daily report as PDF file",
    tags=["Caretaker Reports"]
)
@limiter.limit(pdf_export_rate_limit)
async def export_caretaker_pdf(
    request: Request,
    range_type: str = Query("daily", description="Range type: daily, weekly, monthly, custom"),
    project_id: Optional[str] = Query(None, description="Optional filter by project UUID"),
    dog_id: Optional[str] = Query(None, description="Optional filter by dog UUID"),
    date: Optional[date_type] = Query(None, description="For daily range type"),
    week_start: Optional[date_type] = Query(None, description="For weekly range type"),
    year_month: Optional[str] = Query(None, description="For monthly range type (YYYY-MM)"),
    date_from: Optional[date_type] = Query(None, description="For custom range type"),
    date_to: Optional[date_type] = Query(None, description="For custom range type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export caretaker daily report as PDF
    
    - **range_type**: daily, weekly, monthly, or custom
    - **date**: For daily range type
    - **week_start**: For weekly range type
    - **year_month**: For monthly range type (YYYY-MM)
    - **date_from / date_to**: For custom range type
    - **project_id**: Optional filter by project UUID
    - **dog_id**: Optional filter by dog UUID
    
    Returns path to generated PDF file
    """
    try:
        params = {
            'range_type': range_type,
            'project_id': project_id or '',
            'dog_id': dog_id or ''
        }
        if date:
            params['date'] = str(date)
        if week_start:
            params['week_start'] = str(week_start)
        if year_month:
            params['year_month'] = year_month
        if date_from:
            params['date_from'] = str(date_from)
        if date_to:
            params['date_to'] = str(date_to)
        
        result = call_flask_endpoint('caretaker', 'caretaker_daily_unified_export_pdf', params, current_user)
        
        log_audit(
            user_id=current_user.id,
            action=AuditAction.EXPORT,
            target_type='CaretakerReport',
            target_id=project_id,
            description=f"Exported caretaker daily PDF for range {range_type}",
            old_values={},
            new_values={"report_type": "caretaker_daily_pdf", "range_type": range_type}
        )
        
        if isinstance(result, dict) and 'path' in result:
            return PDFExportResponse(path=result['path'])
        raise HTTPException(status_code=500, detail="PDF export failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
