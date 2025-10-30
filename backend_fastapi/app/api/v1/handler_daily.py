"""
Handler Daily System endpoints for K9 Operations Management System
Includes daily schedules, handler reports, and notifications
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime, timedelta

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.models import (
    User, UserRole, Dog, Project,
    DailySchedule, DailyScheduleItem, HandlerReport,
    HandlerReportHealth, HandlerReportTraining, HandlerReportCare,
    HandlerReportBehavior, HandlerReportIncident,
    HandlerReportAttachment, Notification
)
from app.schemas.handler import (
    DailyScheduleCreate, DailyScheduleUpdate, DailyScheduleResponse,
    DailyScheduleItemCreate, DailyScheduleItemUpdate, DailyScheduleItemResponse,
    HandlerReportCreate, HandlerReportUpdate, HandlerReportResponse,
    HandlerReportHealthCreate, HandlerReportHealthUpdate, HandlerReportHealthResponse,
    HandlerReportTrainingCreate, HandlerReportTrainingUpdate, HandlerReportTrainingResponse,
    HandlerReportCareCreate, HandlerReportCareUpdate, HandlerReportCareResponse,
    HandlerReportBehaviorCreate, HandlerReportBehaviorUpdate, HandlerReportBehaviorResponse,
    HandlerReportIncidentCreate, HandlerReportIncidentUpdate, HandlerReportIncidentResponse,
    NotificationCreate, NotificationUpdate, NotificationResponse
)
from app.schemas.common import PaginatedResponse, MessageResponse
from app.schemas.enums import (
    ScheduleStatus, ReportStatus, NotificationType, ScheduleItemStatus
)
from app.services.audit_service import AuditService
from app.models import AuditAction

router = APIRouter()


# ============================================================================
# Daily Schedule Endpoints
# ============================================================================

@router.post("/schedules", response_model=DailyScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_daily_schedule(
    schedule_data: DailyScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new daily schedule (supervisors only)
    """
    # Only project managers and general admins can create schedules
    if current_user.role not in [UserRole.PROJECT_MANAGER, UserRole.GENERAL_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only supervisors can create daily schedules"
        )
    
    # Project managers can only create schedules for their assigned project
    if current_user.role == UserRole.PROJECT_MANAGER:
        if schedule_data.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only create schedules for their assigned project"
            )
    
    # Check if schedule already exists for this date and project
    existing = db.query(DailySchedule).filter(
        DailySchedule.date == schedule_data.date,
        DailySchedule.project_id == schedule_data.project_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Schedule already exists for {schedule_data.date}"
        )
    
    # Create schedule
    schedule = DailySchedule(
        date=schedule_data.date,
        project_id=schedule_data.project_id,
        status=schedule_data.status,
        notes=schedule_data.notes,
        created_by_user_id=current_user.id
    )
    
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    
    # Audit log
    AuditService.log(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.CREATE,
        resource_type="DailySchedule",
        resource_id=str(schedule.id),
        details={"date": str(schedule.date), "project_id": str(schedule.project_id)}
    )
    
    return schedule


@router.get("/schedules", response_model=PaginatedResponse[DailyScheduleResponse])
async def list_daily_schedules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    project_id: Optional[UUID] = None,
    status: Optional[ScheduleStatus] = None,
):
    """
    List daily schedules with filtering and pagination
    """
    query = db.query(DailySchedule)
    
    # Role-based filtering
    if current_user.role == UserRole.HANDLER:
        # Handlers can only see schedules where they have assignments
        query = query.join(DailyScheduleItem).filter(
            DailyScheduleItem.handler_user_id == current_user.id
        ).distinct()
    elif current_user.role == UserRole.PROJECT_MANAGER and current_user.project_id:
        # Project managers only see their project's schedules
        query = query.filter(DailySchedule.project_id == current_user.project_id)
    # GENERAL_ADMIN can see all schedules
    
    # Filter by date range
    if date_from:
        query = query.filter(DailySchedule.date >= date_from)
    if date_to:
        query = query.filter(DailySchedule.date <= date_to)
    
    # Filter by project (with permission check)
    if project_id:
        if current_user.role == UserRole.PROJECT_MANAGER and project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only view schedules for their assigned project"
            )
        query = query.filter(DailySchedule.project_id == project_id)
    
    # Filter by status
    if status:
        query = query.filter(DailySchedule.status == status)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    schedules = query.order_by(desc(DailySchedule.date)).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=schedules,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/schedules/{schedule_id}", response_model=DailyScheduleResponse)
async def get_daily_schedule(
    schedule_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a specific daily schedule by ID
    """
    schedule = db.query(DailySchedule).filter(DailySchedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    # Check permissions based on role
    if current_user.role == UserRole.HANDLER:
        # Handlers can only view schedules where they have assignments
        has_assignment = db.query(DailyScheduleItem).filter(
            DailyScheduleItem.daily_schedule_id == schedule_id,
            DailyScheduleItem.handler_user_id == current_user.id
        ).first()
        
        if not has_assignment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this schedule"
            )
    elif current_user.role == UserRole.PROJECT_MANAGER:
        if current_user.project_id != schedule.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this schedule"
            )
    # GENERAL_ADMIN can view all schedules
    
    return schedule


@router.patch("/schedules/{schedule_id}", response_model=DailyScheduleResponse)
async def update_daily_schedule(
    schedule_id: UUID,
    update_data: DailyScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a daily schedule
    """
    schedule = db.query(DailySchedule).filter(DailySchedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    # Only supervisors can update
    if current_user.role not in [UserRole.PROJECT_MANAGER, UserRole.GENERAL_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only supervisors can update schedules"
        )
    
    # Project managers can only update schedules for their assigned project
    if current_user.role == UserRole.PROJECT_MANAGER:
        if schedule.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only update schedules for their assigned project"
            )
    
    # Cannot modify locked schedules
    if schedule.status == ScheduleStatus.LOCKED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify locked schedule"
        )
    
    # Update fields
    if update_data.status is not None:
        schedule.status = update_data.status
    if update_data.notes is not None:
        schedule.notes = update_data.notes
    
    db.commit()
    db.refresh(schedule)
    
    # Audit log
    AuditService.log(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        resource_type="DailySchedule",
        resource_id=str(schedule.id),
        details={"status": schedule.status.value if schedule.status else None}
    )
    
    return schedule


@router.post("/schedules/{schedule_id}/lock", response_model=DailyScheduleResponse)
async def lock_daily_schedule(
    schedule_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Lock a daily schedule (prevent further modifications)
    """
    schedule = db.query(DailySchedule).filter(DailySchedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    # Only supervisors can lock
    if current_user.role not in [UserRole.PROJECT_MANAGER, UserRole.GENERAL_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only supervisors can lock schedules"
        )
    
    # Project managers can only lock schedules for their assigned project
    if current_user.role == UserRole.PROJECT_MANAGER:
        if schedule.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only lock schedules for their assigned project"
            )
    
    # Check if already locked
    if schedule.status == ScheduleStatus.LOCKED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Schedule is already locked"
        )
    
    schedule.status = ScheduleStatus.LOCKED
    db.commit()
    db.refresh(schedule)
    
    # Audit log
    AuditService.log(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        resource_type="DailySchedule",
        resource_id=str(schedule.id),
        details={"action": "locked"}
    )
    
    return schedule


# ============================================================================
# Schedule Item Endpoints
# ============================================================================

@router.post("/schedule-items", response_model=DailyScheduleItemResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule_item(
    item_data: DailyScheduleItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a schedule item (handler assignment)
    """
    # Only supervisors can create schedule items
    if current_user.role not in [UserRole.PROJECT_MANAGER, UserRole.GENERAL_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only supervisors can create schedule items"
        )
    
    # Verify schedule exists and is not locked
    schedule = db.query(DailySchedule).filter(DailySchedule.id == item_data.daily_schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    
    # Project managers can only create items for their assigned project's schedules
    if current_user.role == UserRole.PROJECT_MANAGER:
        if schedule.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only create schedule items for their assigned project"
            )
    
    if schedule.status == ScheduleStatus.LOCKED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot modify locked schedule")
    
    # Create schedule item
    item = DailyScheduleItem(
        daily_schedule_id=item_data.daily_schedule_id,
        handler_user_id=item_data.handler_user_id,
        dog_id=item_data.dog_id,
        shift_id=item_data.shift_id,
        status=item_data.status,
        replacement_handler_id=item_data.replacement_handler_id,
        absence_reason=item_data.absence_reason,
        replacement_notes=item_data.replacement_notes
    )
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    # Create notification for handler
    notification = Notification(
        user_id=item_data.handler_user_id,
        type=NotificationType.SCHEDULE_CREATED,
        title="جدول يومي جديد",
        message=f"تم تعيينك لجدول يوم {schedule.date}",
        related_id=str(schedule.id),
        related_type="DailySchedule"
    )
    db.add(notification)
    db.commit()
    
    return item


@router.get("/schedule-items", response_model=PaginatedResponse[DailyScheduleItemResponse])
async def list_schedule_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    schedule_id: Optional[UUID] = None,
    handler_id: Optional[UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    """
    List schedule items with filtering
    """
    query = db.query(DailyScheduleItem)
    
    # Role-based filtering - apply project/assignment scoping first
    if current_user.role == UserRole.HANDLER:
        # Handlers only see their own assignments
        query = query.filter(DailyScheduleItem.handler_user_id == current_user.id)
    elif current_user.role == UserRole.PROJECT_MANAGER and current_user.project_id:
        # Project managers only see items from their project's schedules
        query = query.join(DailySchedule).filter(
            DailySchedule.project_id == current_user.project_id
        )
    # GENERAL_ADMIN can see all items
    
    # Additional filters
    if schedule_id:
        # Verify user has permission to view this schedule
        schedule = db.query(DailySchedule).filter(DailySchedule.id == schedule_id).first()
        if schedule:
            if current_user.role == UserRole.PROJECT_MANAGER and schedule.project_id != current_user.project_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Project managers can only view items for their assigned project"
                )
            elif current_user.role == UserRole.HANDLER:
                # Verify handler has assignment in this schedule
                has_assignment = db.query(DailyScheduleItem).filter(
                    DailyScheduleItem.daily_schedule_id == schedule_id,
                    DailyScheduleItem.handler_user_id == current_user.id
                ).first()
                if not has_assignment:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to view items for this schedule"
                    )
        query = query.filter(DailyScheduleItem.daily_schedule_id == schedule_id)
    
    if handler_id:
        # Only allow if user has permission to view this handler's data
        if current_user.role == UserRole.HANDLER and handler_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Handlers can only view their own assignments"
            )
        query = query.filter(DailyScheduleItem.handler_user_id == handler_id)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/handler/today-schedule", response_model=Optional[DailyScheduleItemResponse])
async def get_handler_today_schedule(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get today's schedule assignment for the current handler
    """
    if current_user.role != UserRole.HANDLER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is for handlers only"
        )
    
    today = date.today()
    
    # Find today's schedule
    schedule = db.query(DailySchedule).filter(DailySchedule.date == today).first()
    if not schedule:
        return None
    
    # Find handler's assignment
    item = db.query(DailyScheduleItem).filter(
        DailyScheduleItem.daily_schedule_id == schedule.id,
        DailyScheduleItem.handler_user_id == current_user.id
    ).first()
    
    return item


# ============================================================================
# Handler Report Endpoints
# ============================================================================

@router.post("/reports", response_model=HandlerReportResponse, status_code=status.HTTP_201_CREATED)
async def create_handler_report(
    report_data: HandlerReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new handler daily report
    """
    # Handlers can only create reports for themselves
    if current_user.role == UserRole.HANDLER and report_data.handler_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create reports for yourself"
        )
    
    # Project managers can only create reports for their assigned project
    if current_user.role == UserRole.PROJECT_MANAGER:
        if report_data.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only create reports for their assigned project"
            )
    
    # Check if report already exists for this date and handler
    existing = db.query(HandlerReport).filter(
        HandlerReport.date == report_data.date,
        HandlerReport.handler_user_id == report_data.handler_user_id,
        HandlerReport.dog_id == report_data.dog_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report already exists for this date and dog"
        )
    
    # Create report
    report = HandlerReport(
        date=report_data.date,
        schedule_item_id=report_data.schedule_item_id,
        handler_user_id=report_data.handler_user_id,
        dog_id=report_data.dog_id,
        project_id=report_data.project_id,
        location=report_data.location,
        status=ReportStatus.DRAFT
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return report


@router.get("/reports", response_model=PaginatedResponse[HandlerReportResponse])
async def list_handler_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    handler_id: Optional[UUID] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    status: Optional[ReportStatus] = None,
):
    """
    List handler reports with filtering and pagination
    """
    query = db.query(HandlerReport)
    
    # Permission-based filtering
    if current_user.role == UserRole.HANDLER:
        query = query.filter(HandlerReport.handler_user_id == current_user.id)
    elif current_user.role == UserRole.PROJECT_MANAGER and current_user.project_id:
        # Project managers only see reports from their assigned project
        query = query.filter(HandlerReport.project_id == current_user.project_id)
    # GENERAL_ADMIN can see all reports
    
    # Additional filters
    if handler_id:
        query = query.filter(HandlerReport.handler_user_id == handler_id)
    
    # Date filters
    if date_from:
        query = query.filter(HandlerReport.date >= date_from)
    if date_to:
        query = query.filter(HandlerReport.date <= date_to)
    
    # Status filter
    if status:
        query = query.filter(HandlerReport.status == status)
    
    total = query.count()
    reports = query.order_by(desc(HandlerReport.date)).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=reports,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/reports/{report_id}", response_model=HandlerReportResponse)
async def get_handler_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a specific handler report
    """
    report = db.query(HandlerReport).filter(HandlerReport.id == report_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Permission check based on role
    if current_user.role == UserRole.HANDLER:
        if report.handler_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this report"
            )
    elif current_user.role == UserRole.PROJECT_MANAGER:
        if report.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this report"
            )
    # GENERAL_ADMIN can view all reports
    
    return report


@router.patch("/reports/{report_id}", response_model=HandlerReportResponse)
async def update_handler_report(
    report_id: UUID,
    update_data: HandlerReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a handler report (draft only)
    """
    report = db.query(HandlerReport).filter(HandlerReport.id == report_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Role-based authorization
    if current_user.role == UserRole.HANDLER:
        # Handlers can only update their own reports
        if report.handler_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this report"
            )
        # Handlers can only update draft reports
        if report.status != ReportStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only update draft reports"
            )
    elif current_user.role == UserRole.PROJECT_MANAGER:
        # Project managers can only update reports from their assigned project
        if report.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only update reports for their assigned project"
            )
        # Supervisors also cannot modify submitted/approved reports
        if report.status != ReportStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only update draft reports"
            )
    # GENERAL_ADMIN has full access but still respects draft-only rule
    elif current_user.role == UserRole.GENERAL_ADMIN:
        if report.status != ReportStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only update draft reports"
            )
    
    # Update fields
    if update_data.location is not None:
        report.location = update_data.location
    
    db.commit()
    db.refresh(report)
    
    return report


@router.post("/reports/{report_id}/submit", response_model=HandlerReportResponse)
async def submit_handler_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Submit a report for review
    """
    report = db.query(HandlerReport).filter(HandlerReport.id == report_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Only handler can submit their own reports
    if report.handler_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to submit this report"
        )
    
    if report.status != ReportStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report already submitted"
        )
    
    # Update status
    report.status = ReportStatus.SUBMITTED
    report.submitted_at = datetime.utcnow()
    db.commit()
    db.refresh(report)
    
    # Create notification for supervisors (project-scoped)
    # Get supervisors for this specific project only
    if report.project_id:
        supervisors = db.query(User).filter(
            or_(
                # Project managers for this specific project
                and_(User.role == UserRole.PROJECT_MANAGER, User.project_id == report.project_id),
                # General admins
                User.role == UserRole.GENERAL_ADMIN
            ),
            User.is_active == True
        ).all()
    else:
        # If no project, notify only general admins
        supervisors = db.query(User).filter(
            User.role == UserRole.GENERAL_ADMIN,
            User.is_active == True
        ).all()
    
    for supervisor in supervisors:
        notification = Notification(
            user_id=supervisor.id,
            type=NotificationType.REPORT_SUBMITTED,
            title="تقرير جديد للمراجعة",
            message=f"قام {current_user.full_name} بإرسال تقرير يوم {report.date}",
            related_id=str(report.id),
            related_type="HandlerReport"
        )
        db.add(notification)
    
    db.commit()
    
    # Audit log
    AuditService.log(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        resource_type="HandlerReport",
        resource_id=str(report.id),
        details={"action": "submitted"}
    )
    
    return report


@router.post("/reports/{report_id}/approve", response_model=HandlerReportResponse)
async def approve_handler_report(
    report_id: UUID,
    review_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Approve a handler report (supervisors only)
    """
    if current_user.role not in [UserRole.PROJECT_MANAGER, UserRole.GENERAL_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only supervisors can approve reports"
        )
    
    report = db.query(HandlerReport).filter(HandlerReport.id == report_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Project managers can only approve reports from their assigned project
    if current_user.role == UserRole.PROJECT_MANAGER:
        if report.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only approve reports for their assigned project"
            )
    
    if report.status != ReportStatus.SUBMITTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only approve submitted reports"
        )
    
    # Update status
    report.status = ReportStatus.APPROVED
    report.reviewed_by_user_id = current_user.id
    report.reviewed_at = datetime.utcnow()
    report.review_notes = review_notes
    db.commit()
    db.refresh(report)
    
    # Notify handler
    notification = Notification(
        user_id=report.handler_user_id,
        type=NotificationType.REPORT_APPROVED,
        title="تم اعتماد التقرير",
        message=f"تم اعتماد تقريرك ليوم {report.date}",
        related_id=str(report.id),
        related_type="HandlerReport"
    )
    db.add(notification)
    db.commit()
    
    # Audit log
    AuditService.log(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        resource_type="HandlerReport",
        resource_id=str(report.id),
        details={"action": "approved", "reviewer_id": str(current_user.id)}
    )
    
    return report


@router.post("/reports/{report_id}/reject", response_model=HandlerReportResponse)
async def reject_handler_report(
    report_id: UUID,
    review_notes: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reject a handler report (supervisors only)
    """
    if current_user.role not in [UserRole.PROJECT_MANAGER, UserRole.GENERAL_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only supervisors can reject reports"
        )
    
    report = db.query(HandlerReport).filter(HandlerReport.id == report_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Project managers can only reject reports from their assigned project
    if current_user.role == UserRole.PROJECT_MANAGER:
        if report.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project managers can only reject reports for their assigned project"
            )
    
    if report.status != ReportStatus.SUBMITTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only reject submitted reports"
        )
    
    # Update status
    report.status = ReportStatus.REJECTED
    report.reviewed_by_user_id = current_user.id
    report.reviewed_at = datetime.utcnow()
    report.review_notes = review_notes
    db.commit()
    db.refresh(report)
    
    # Notify handler
    notification = Notification(
        user_id=report.handler_user_id,
        type=NotificationType.REPORT_REJECTED,
        title="تم رفض التقرير",
        message=f"تم رفض تقريرك ليوم {report.date}. السبب: {review_notes}",
        related_id=str(report.id),
        related_type="HandlerReport"
    )
    db.add(notification)
    db.commit()
    
    # Audit log
    AuditService.log(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        resource_type="HandlerReport",
        resource_id=str(report.id),
        details={"action": "rejected", "reviewer_id": str(current_user.id)}
    )
    
    return report


# ============================================================================
# Notification Endpoints
# ============================================================================

@router.get("/notifications", response_model=PaginatedResponse[NotificationResponse])
async def list_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    unread_only: bool = False,
):
    """
    List notifications for the current user
    """
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.read.is_(False))
    
    total = query.count()
    notifications = query.order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=notifications,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/notifications/unread-count")
async def get_unread_notifications_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get count of unread notifications
    """
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.read == False
    ).count()
    
    return {"count": count}


@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Mark a notification as read
    """
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this notification"
        )
    
    notification.read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    db.refresh(notification)
    
    return notification


@router.post("/notifications/mark-all-read", response_model=MessageResponse)
async def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Mark all notifications as read for the current user
    """
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.read == False
    ).update({"read": True, "read_at": datetime.utcnow()})
    
    db.commit()
    
    return MessageResponse(
        message=f"Marked {count} notifications as read",
        success=True
    )
