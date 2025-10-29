"""
Dog CRUD endpoints for K9 Operations Management System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.models import User, Dog, UserRole, AuditAction
from app.schemas.dog import DogCreate, DogUpdate, DogResponse
from app.schemas.common import PaginatedResponse
from app.schemas.enums import DogStatus, DogGender
from app.services.audit_service import AuditService

router = APIRouter()


def get_user_accessible_dogs(db: Session, user: User) -> List[Dog]:
    """Get dogs accessible to the current user based on their role"""
    if user.role == UserRole.GENERAL_ADMIN:
        return db.query(Dog).all()
    else:
        return db.query(Dog).filter(Dog.assigned_to_user_id == user.id).all()


@router.get("/", response_model=PaginatedResponse[DogResponse])
async def list_dogs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[DogStatus] = None,
    gender: Optional[DogGender] = None,
    breed: Optional[str] = None,
    search: Optional[str] = None,
):
    """
    List all dogs accessible to the current user with filtering and pagination
    
    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return
    - **status**: Filter by dog status
    - **gender**: Filter by dog gender
    - **breed**: Filter by breed
    - **search**: Search in name, code, or microchip_id
    """
    # Base query with user permissions
    query = db.query(Dog)
    if current_user.role != UserRole.GENERAL_ADMIN:
        query = query.filter(Dog.assigned_to_user_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(Dog.current_status == status)
    if gender:
        query = query.filter(Dog.gender == gender)
    if breed:
        query = query.filter(Dog.breed.ilike(f"%{breed}%"))
    if search:
        query = query.filter(
            or_(
                Dog.name.ilike(f"%{search}%"),
                Dog.code.ilike(f"%{search}%"),
                Dog.microchip_id.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    dogs = query.order_by(Dog.name).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=[DogResponse.from_orm(dog) for dog in dogs],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{dog_id}", response_model=DogResponse)
async def get_dog(
    dog_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific dog
    
    - **dog_id**: UUID of the dog
    """
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الكلب غير موجود"
        )
    
    # Check permissions
    if current_user.role != UserRole.GENERAL_ADMIN and dog.assigned_to_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى بيانات هذا الكلب"
        )
    
    return DogResponse.from_orm(dog)


@router.post("/", response_model=DogResponse, status_code=status.HTTP_201_CREATED)
async def create_dog(
    dog_data: DogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new dog record
    
    - **dog_data**: Dog creation data including name, breed, gender, etc.
    """
    # Check if code already exists
    existing_dog = db.query(Dog).filter(Dog.code == dog_data.code).first()
    if existing_dog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز الكلب موجود بالفعل في النظام"
        )
    
    # Check if microchip_id already exists (if provided)
    if dog_data.microchip_id:
        existing_microchip = db.query(Dog).filter(Dog.microchip_id == dog_data.microchip_id).first()
        if existing_microchip:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رقم الشريحة الإلكترونية موجود بالفعل في النظام"
            )
    
    # Assign dog to PROJECT_MANAGER or use provided assignment for GENERAL_ADMIN
    if current_user.role == UserRole.PROJECT_MANAGER:
        dog_data.assigned_to_user_id = current_user.id
    
    # Create dog instance
    dog = Dog(**dog_data.dict())
    db.add(dog)
    db.commit()
    db.refresh(dog)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.CREATE,
        target_type="Dog",
        target_id=str(dog.id),
        details={
            "name": dog.name,
            "code": dog.code,
            "breed": dog.breed
        }
    )
    
    return DogResponse.from_orm(dog)


@router.put("/{dog_id}", response_model=DogResponse)
async def update_dog(
    dog_id: UUID,
    dog_data: DogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing dog record
    
    - **dog_id**: UUID of the dog to update
    - **dog_data**: Updated dog data (only provided fields will be updated)
    """
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الكلب غير موجود"
        )
    
    # Check permissions
    if current_user.role != UserRole.GENERAL_ADMIN and dog.assigned_to_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بتعديل بيانات هذا الكلب"
        )
    
    # Check for unique code if being updated
    if dog_data.code and dog_data.code != dog.code:
        existing_dog = db.query(Dog).filter(Dog.code == dog_data.code).first()
        if existing_dog:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز الكلب موجود بالفعل في النظام"
            )
    
    # Check for unique microchip_id if being updated
    if dog_data.microchip_id and dog_data.microchip_id != dog.microchip_id:
        existing_microchip = db.query(Dog).filter(Dog.microchip_id == dog_data.microchip_id).first()
        if existing_microchip:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رقم الشريحة الإلكترونية موجود بالفعل في النظام"
            )
    
    # Update only provided fields
    update_data = dog_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dog, field, value)
    
    db.commit()
    db.refresh(dog)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        target_type="Dog",
        target_id=str(dog.id),
        details={"updated_fields": list(update_data.keys())}
    )
    
    return DogResponse.from_orm(dog)


@router.delete("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dog(
    dog_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a dog record (GENERAL_ADMIN only)
    
    - **dog_id**: UUID of the dog to delete
    """
    if current_user.role != UserRole.GENERAL_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="يجب أن تكون مسؤول عام لحذف سجلات الكلاب"
        )
    
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الكلب غير موجود"
        )
    
    # Log audit before deletion
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.DELETE,
        target_type="Dog",
        target_id=str(dog.id),
        details={
            "name": dog.name,
            "code": dog.code,
            "breed": dog.breed
        }
    )
    
    db.delete(dog)
    db.commit()
    
    return None


class DogStatistics(BaseModel):
    """Dog statistics response schema"""
    total: int
    by_status: dict[str, int]
    by_gender: dict[str, int]
    by_breed: dict[str, int]
    top_breeds: List[tuple[str, int]]
    
    model_config = ConfigDict(from_attributes=True)


@router.get("/stats/summary", response_model=DogStatistics)
async def get_dog_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get summary statistics about dogs
    
    Returns counts by status, gender, and breed
    """
    # Base query with user permissions
    query = db.query(Dog)
    if current_user.role != UserRole.GENERAL_ADMIN:
        query = query.filter(Dog.assigned_to_user_id == current_user.id)
    
    dogs = query.all()
    
    # Calculate statistics
    total = len(dogs)
    by_status = {}
    by_gender = {}
    by_breed = {}
    
    for dog in dogs:
        # Count by status
        status_key = dog.current_status.value if dog.current_status else "UNKNOWN"
        by_status[status_key] = by_status.get(status_key, 0) + 1
        
        # Count by gender
        gender_key = dog.gender.value if dog.gender else "UNKNOWN"
        by_gender[gender_key] = by_gender.get(gender_key, 0) + 1
        
        # Count by breed
        breed_key = dog.breed or "UNKNOWN"
        by_breed[breed_key] = by_breed.get(breed_key, 0) + 1
    
    return DogStatistics(
        total=total,
        by_status=by_status,
        by_gender=by_gender,
        by_breed=by_breed,
        top_breeds=sorted(by_breed.items(), key=lambda x: x[1], reverse=True)[:5]
    )
