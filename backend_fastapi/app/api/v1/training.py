"""
Training Session CRUD endpoints for K9 Operations Management System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.models import User, TrainingSession, UserRole, AuditAction, Dog, Employee
from app.schemas.training import TrainingSessionCreate, TrainingSessionUpdate, TrainingSessionResponse
from app.schemas.common import PaginatedResponse
from app.schemas.enums import TrainingCategory
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[TrainingSessionResponse])
async def list_training_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    dog_id: Optional[UUID] = None,
    trainer_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    category: Optional[TrainingCategory] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    min_rating: Optional[int] = Query(None, ge=0, le=10),
):
    """
    List all training sessions accessible to the current user with filtering and pagination
    
    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return
    - **dog_id**: Filter by specific dog
    - **trainer_id**: Filter by specific trainer
    - **project_id**: Filter by specific project (ignored for PROJECT_MANAGER)
    - **category**: Filter by training category
    - **date_from**: Filter sessions from this date
    - **date_to**: Filter sessions until this date
    - **min_rating**: Filter sessions with minimum success rating
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can list
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بعرض جلسات التدريب"
        )
    
    # Base query with user permissions
    query = db.query(TrainingSession)
    
    # Apply RBAC: PROJECT_MANAGER sees only their project's sessions - server-side enforcement
    if current_user.role == UserRole.PROJECT_MANAGER:
        query = query.filter(TrainingSession.project_id == current_user.project_id)
        # Ignore project_id parameter - managers can only see their own project
    elif project_id:
        # GENERAL_ADMIN can filter by specific project
        query = query.filter(TrainingSession.project_id == project_id)
    
    # Apply additional filters
    if dog_id:
        query = query.filter(TrainingSession.dog_id == dog_id)
    if trainer_id:
        query = query.filter(TrainingSession.trainer_id == trainer_id)
    if category:
        query = query.filter(TrainingSession.category == category)
    if date_from:
        query = query.filter(TrainingSession.session_date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(TrainingSession.session_date <= datetime.combine(date_to, datetime.max.time()))
    if min_rating is not None:
        query = query.filter(TrainingSession.success_rating >= min_rating)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    sessions = query.order_by(TrainingSession.session_date.desc()).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=[TrainingSessionResponse.from_orm(session) for session in sessions],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/stats/summary")
async def get_training_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    project_id: Optional[UUID] = None,
    dog_id: Optional[UUID] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
):
    """
    Get summary statistics about training sessions
    
    Returns counts by category, average ratings, and total training hours
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can access statistics
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بعرض إحصائيات التدريب"
        )
    
    # Base query with user permissions
    query = db.query(TrainingSession)
    
    # PROJECT_MANAGER: Always enforce their project scope
    if current_user.role == UserRole.PROJECT_MANAGER:
        query = query.filter(TrainingSession.project_id == current_user.project_id)
        # Ignore project_id filter if provided - they can only see their own
    elif project_id:
        # GENERAL_ADMIN can filter by specific project
        query = query.filter(TrainingSession.project_id == project_id)
    if dog_id:
        query = query.filter(TrainingSession.dog_id == dog_id)
    if date_from:
        query = query.filter(TrainingSession.session_date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(TrainingSession.session_date <= datetime.combine(date_to, datetime.max.time()))
    
    sessions = query.all()
    
    # Calculate statistics
    total = len(sessions)
    total_hours = sum(s.duration for s in sessions) / 60  # Convert minutes to hours
    avg_rating = sum(s.success_rating for s in sessions) / total if total > 0 else 0
    
    by_category = {}
    for session in sessions:
        category_key = session.category.value if session.category else "UNKNOWN"
        by_category[category_key] = by_category.get(category_key, 0) + 1
    
    return {
        "total_sessions": total,
        "total_hours": round(total_hours, 2),
        "average_success_rating": round(avg_rating, 2),
        "by_category": by_category,
        "top_categories": sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:5]
    }


@router.get("/{session_id}", response_model=TrainingSessionResponse)
async def get_training_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific training session
    
    - **session_id**: UUID of the training session
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can access
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى بيانات جلسات التدريب"
        )
    
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="جلسة التدريب غير موجودة"
        )
    
    # Check permissions
    if current_user.role == UserRole.PROJECT_MANAGER:
        if session.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="غير مصرح لك بالوصول إلى بيانات هذه الجلسة التدريبية"
            )
    
    return TrainingSessionResponse.from_orm(session)


@router.post("/", response_model=TrainingSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_training_session(
    session_data: TrainingSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new training session record
    
    - **session_data**: Training session creation data
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can create
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بإنشاء جلسات تدريب"
        )
    
    # Verify dog exists
    dog = db.query(Dog).filter(Dog.id == session_data.dog_id).first()
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الكلب غير موجود في النظام"
        )
    
    # Verify trainer exists
    trainer = db.query(Employee).filter(Employee.id == session_data.trainer_id).first()
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المدرب غير موجود في النظام"
        )
    
    # PROJECT_MANAGER can only create sessions for their project - enforce explicitly
    if current_user.role == UserRole.PROJECT_MANAGER:
        if not current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="المدير لا يملك مشروع محدد"
            )
        session_data.project_id = current_user.project_id
    
    # Create training session
    training_session = TrainingSession(**session_data.dict())
    db.add(training_session)
    db.commit()
    db.refresh(training_session)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.CREATE,
        target_type="TrainingSession",
        target_id=str(training_session.id),
        details={
            "dog_id": str(session_data.dog_id),
            "trainer_id": str(session_data.trainer_id),
            "category": session_data.category.value,
            "subject": session_data.subject,
            "session_date": session_data.session_date.isoformat(),
            "success_rating": session_data.success_rating
        }
    )
    
    return TrainingSessionResponse.from_orm(training_session)


@router.put("/{session_id}", response_model=TrainingSessionResponse)
async def update_training_session(
    session_id: UUID,
    session_data: TrainingSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing training session record
    
    - **session_id**: UUID of the training session to update
    - **session_data**: Updated training session data (only provided fields will be updated)
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can update
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بتعديل جلسات التدريب"
        )
    
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="جلسة التدريب غير موجودة"
        )
    
    # Check permissions
    if current_user.role == UserRole.PROJECT_MANAGER:
        if session.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="غير مصرح لك بتعديل بيانات هذه الجلسة التدريبية"
            )
    
    # Verify dog if being updated
    if session_data.dog_id:
        dog = db.query(Dog).filter(Dog.id == session_data.dog_id).first()
        if not dog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="الكلب غير موجود في النظام"
            )
    
    # Verify trainer if being updated
    if session_data.trainer_id:
        trainer = db.query(Employee).filter(Employee.id == session_data.trainer_id).first()
        if not trainer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="المدرب غير موجود في النظام"
            )
    
    # Update only provided fields
    update_data = session_data.dict(exclude_unset=True)
    
    # PROJECT_MANAGER cannot change project_id - remove it completely
    if current_user.role == UserRole.PROJECT_MANAGER:
        update_data.pop('project_id', None)
    
    for field, value in update_data.items():
        setattr(session, field, value)
    
    db.commit()
    db.refresh(session)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        target_type="TrainingSession",
        target_id=str(session.id),
        details={"updated_fields": list(update_data.keys())}
    )
    
    return TrainingSessionResponse.from_orm(session)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_training_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a training session record (GENERAL_ADMIN only)
    
    - **session_id**: UUID of the training session to delete
    """
    if current_user.role != UserRole.GENERAL_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="يجب أن تكون مسؤول عام لحذف جلسات التدريب"
        )
    
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="جلسة التدريب غير موجودة"
        )
    
    # Log audit before deletion
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.DELETE,
        target_type="TrainingSession",
        target_id=str(session.id),
        details={
            "subject": session.subject,
            "dog_id": str(session.dog_id),
            "trainer_id": str(session.trainer_id),
            "category": session.category.value,
            "session_date": session.session_date.isoformat()
        }
    )
    
    db.delete(session)
    db.commit()
    
    return None
