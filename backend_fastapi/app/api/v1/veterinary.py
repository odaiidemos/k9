"""
Veterinary Visit CRUD endpoints for K9 Operations Management System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.models import User, VeterinaryVisit, UserRole, AuditAction, Dog, Employee
from app.schemas.veterinary import VeterinaryVisitCreate, VeterinaryVisitUpdate, VeterinaryVisitResponse
from app.schemas.common import PaginatedResponse
from app.schemas.enums import VisitType
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[VeterinaryVisitResponse])
async def list_veterinary_visits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    dog_id: Optional[UUID] = None,
    vet_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    visit_type: Optional[VisitType] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
):
    """
    List all veterinary visits accessible to the current user with filtering and pagination
    
    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return
    - **dog_id**: Filter by specific dog
    - **vet_id**: Filter by specific veterinarian
    - **project_id**: Filter by specific project (ignored for PROJECT_MANAGER)
    - **visit_type**: Filter by visit type (ROUTINE, EMERGENCY, VACCINATION)
    - **date_from**: Filter visits from this date
    - **date_to**: Filter visits until this date
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can list
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بعرض الزيارات البيطرية"
        )
    
    # Base query with user permissions
    query = db.query(VeterinaryVisit)
    
    # Apply RBAC: PROJECT_MANAGER sees only their project's visits - server-side enforcement
    if current_user.role == UserRole.PROJECT_MANAGER:
        query = query.filter(VeterinaryVisit.project_id == current_user.project_id)
        # Ignore project_id parameter - managers can only see their own project
    elif project_id:
        # GENERAL_ADMIN can filter by specific project
        query = query.filter(VeterinaryVisit.project_id == project_id)
    
    # Apply additional filters
    if dog_id:
        query = query.filter(VeterinaryVisit.dog_id == dog_id)
    if vet_id:
        query = query.filter(VeterinaryVisit.vet_id == vet_id)
    if visit_type:
        query = query.filter(VeterinaryVisit.visit_type == visit_type)
    if date_from:
        query = query.filter(VeterinaryVisit.visit_date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(VeterinaryVisit.visit_date <= datetime.combine(date_to, datetime.max.time()))
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    visits = query.order_by(VeterinaryVisit.visit_date.desc()).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=[VeterinaryVisitResponse.from_orm(visit) for visit in visits],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/stats/summary")
async def get_veterinary_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    project_id: Optional[UUID] = None,
    dog_id: Optional[UUID] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
):
    """
    Get summary statistics about veterinary visits
    
    Returns counts by visit type, average costs, and total visits
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can access statistics
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بعرض إحصائيات الزيارات البيطرية"
        )
    
    # Base query with user permissions
    query = db.query(VeterinaryVisit)
    
    # PROJECT_MANAGER: Always enforce their project scope
    if current_user.role == UserRole.PROJECT_MANAGER:
        query = query.filter(VeterinaryVisit.project_id == current_user.project_id)
        # Ignore project_id filter if provided - they can only see their own
    elif project_id:
        # GENERAL_ADMIN can filter by specific project
        query = query.filter(VeterinaryVisit.project_id == project_id)
    if dog_id:
        query = query.filter(VeterinaryVisit.dog_id == dog_id)
    if date_from:
        query = query.filter(VeterinaryVisit.visit_date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(VeterinaryVisit.visit_date <= datetime.combine(date_to, datetime.max.time()))
    
    visits = query.all()
    
    # Calculate statistics
    total = len(visits)
    total_cost = sum(v.cost for v in visits if v.cost)
    avg_cost = total_cost / len([v for v in visits if v.cost]) if any(v.cost for v in visits) else 0
    
    by_visit_type = {}
    for visit in visits:
        visit_type_key = visit.visit_type.value if visit.visit_type else "UNKNOWN"
        by_visit_type[visit_type_key] = by_visit_type.get(visit_type_key, 0) + 1
    
    # Count vaccinations
    vaccinations_count = sum(len(v.vaccinations_given) for v in visits if v.vaccinations_given)
    
    return {
        "total_visits": total,
        "total_cost": round(total_cost, 2),
        "average_cost": round(avg_cost, 2),
        "total_vaccinations": vaccinations_count,
        "by_visit_type": by_visit_type,
        "emergency_visits": by_visit_type.get("EMERGENCY", 0),
        "routine_visits": by_visit_type.get("ROUTINE", 0)
    }


@router.get("/{visit_id}", response_model=VeterinaryVisitResponse)
async def get_veterinary_visit(
    visit_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific veterinary visit
    
    - **visit_id**: UUID of the veterinary visit
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can access
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى بيانات الزيارات البيطرية"
        )
    
    visit = db.query(VeterinaryVisit).filter(VeterinaryVisit.id == visit_id).first()
    
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الزيارة البيطرية غير موجودة"
        )
    
    # Check permissions
    if current_user.role == UserRole.PROJECT_MANAGER:
        if visit.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="غير مصرح لك بالوصول إلى بيانات هذه الزيارة البيطرية"
            )
    
    return VeterinaryVisitResponse.from_orm(visit)


@router.post("/", response_model=VeterinaryVisitResponse, status_code=status.HTTP_201_CREATED)
async def create_veterinary_visit(
    visit_data: VeterinaryVisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new veterinary visit record
    
    - **visit_data**: Veterinary visit creation data including dog, vet, visit type, and medical details
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can create
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بإنشاء زيارات بيطرية"
        )
    
    # Verify dog exists
    dog = db.query(Dog).filter(Dog.id == visit_data.dog_id).first()
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الكلب غير موجود في النظام"
        )
    
    # Verify vet exists
    vet = db.query(Employee).filter(Employee.id == visit_data.vet_id).first()
    if not vet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الطبيب البيطري غير موجود في النظام"
        )
    
    # PROJECT_MANAGER can only create visits for their project - enforce explicitly
    if current_user.role == UserRole.PROJECT_MANAGER:
        if not current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="المدير لا يملك مشروع محدد"
            )
        visit_data.project_id = current_user.project_id
    
    # Create veterinary visit
    visit = VeterinaryVisit(**visit_data.dict())
    db.add(visit)
    db.commit()
    db.refresh(visit)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.CREATE,
        target_type="VeterinaryVisit",
        target_id=str(visit.id),
        details={
            "dog_id": str(visit_data.dog_id),
            "vet_id": str(visit_data.vet_id),
            "visit_type": visit_data.visit_type.value,
            "visit_date": visit_data.visit_date.isoformat(),
            "diagnosis": visit_data.diagnosis
        }
    )
    
    return VeterinaryVisitResponse.from_orm(visit)


@router.put("/{visit_id}", response_model=VeterinaryVisitResponse)
async def update_veterinary_visit(
    visit_id: UUID,
    visit_data: VeterinaryVisitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing veterinary visit record
    
    - **visit_id**: UUID of the veterinary visit to update
    - **visit_data**: Updated veterinary visit data (only provided fields will be updated)
    """
    # Only GENERAL_ADMIN and PROJECT_MANAGER can update
    if current_user.role not in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بتعديل الزيارات البيطرية"
        )
    
    visit = db.query(VeterinaryVisit).filter(VeterinaryVisit.id == visit_id).first()
    
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الزيارة البيطرية غير موجودة"
        )
    
    # Check permissions
    if current_user.role == UserRole.PROJECT_MANAGER:
        if visit.project_id != current_user.project_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="غير مصرح لك بتعديل بيانات هذه الزيارة البيطرية"
            )
    
    # Verify dog if being updated
    if visit_data.dog_id:
        dog = db.query(Dog).filter(Dog.id == visit_data.dog_id).first()
        if not dog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="الكلب غير موجود في النظام"
            )
    
    # Verify vet if being updated
    if visit_data.vet_id:
        vet = db.query(Employee).filter(Employee.id == visit_data.vet_id).first()
        if not vet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="الطبيب البيطري غير موجود في النظام"
            )
    
    # Update only provided fields
    update_data = visit_data.dict(exclude_unset=True)
    
    # PROJECT_MANAGER cannot change project_id - remove it completely
    if current_user.role == UserRole.PROJECT_MANAGER:
        update_data.pop('project_id', None)
    
    for field, value in update_data.items():
        setattr(visit, field, value)
    
    db.commit()
    db.refresh(visit)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        target_type="VeterinaryVisit",
        target_id=str(visit.id),
        details={"updated_fields": list(update_data.keys())}
    )
    
    return VeterinaryVisitResponse.from_orm(visit)


@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_veterinary_visit(
    visit_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a veterinary visit record (GENERAL_ADMIN only)
    
    - **visit_id**: UUID of the veterinary visit to delete
    """
    if current_user.role != UserRole.GENERAL_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="يجب أن تكون مسؤول عام لحذف الزيارات البيطرية"
        )
    
    visit = db.query(VeterinaryVisit).filter(VeterinaryVisit.id == visit_id).first()
    
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الزيارة البيطرية غير موجودة"
        )
    
    # Log audit before deletion
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.DELETE,
        target_type="VeterinaryVisit",
        target_id=str(visit.id),
        details={
            "visit_type": visit.visit_type.value,
            "dog_id": str(visit.dog_id),
            "vet_id": str(visit.vet_id),
            "visit_date": visit.visit_date.isoformat(),
            "diagnosis": visit.diagnosis
        }
    )
    
    db.delete(visit)
    db.commit()
    
    return None
