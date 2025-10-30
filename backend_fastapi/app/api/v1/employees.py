"""
Employee CRUD endpoints for K9 Operations Management System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.models import User, Employee, UserRole, AuditAction, EmployeeRole
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.schemas.common import PaginatedResponse
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[EmployeeResponse])
async def list_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    role: Optional[EmployeeRole] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
):
    """
    List all employees accessible to the current user with filtering and pagination
    
    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return
    - **role**: Filter by employee role
    - **is_active**: Filter by active status
    - **search**: Search in name, employee_id, email, or phone
    """
    # Base query with user permissions
    query = db.query(Employee)
    if current_user.role != UserRole.GENERAL_ADMIN:
        query = query.filter(Employee.assigned_to_user_id == current_user.id)
    
    # Apply filters
    if role:
        query = query.filter(Employee.role == role)
    if is_active is not None:
        query = query.filter(Employee.is_active == is_active)
    if search:
        query = query.filter(
            or_(
                Employee.name.ilike(f"%{search}%"),
                Employee.employee_id.ilike(f"%{search}%"),
                Employee.email.ilike(f"%{search}%"),
                Employee.phone.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    employees = query.order_by(Employee.name).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=[EmployeeResponse.from_orm(emp) for emp in employees],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific employee
    
    - **employee_id**: UUID of the employee
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الموظف غير موجود"
        )
    
    # Check permissions
    if current_user.role != UserRole.GENERAL_ADMIN and employee.assigned_to_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى بيانات هذا الموظف"
        )
    
    return EmployeeResponse.from_orm(employee)


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new employee record
    
    - **employee_data**: Employee creation data including name, employee_id, role, etc.
    """
    # Check if employee_id already exists
    existing_employee = db.query(Employee).filter(Employee.employee_id == employee_data.employee_id).first()
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رقم الموظف موجود بالفعل في النظام"
        )
    
    # Check if email already exists (if provided)
    if employee_data.email:
        existing_email = db.query(Employee).filter(Employee.email == employee_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="البريد الإلكتروني موجود بالفعل في النظام"
            )
    
    # Assign employee to PROJECT_MANAGER or use provided assignment for GENERAL_ADMIN
    if current_user.role == UserRole.PROJECT_MANAGER:
        employee_data.assigned_to_user_id = current_user.id
    
    # Create employee instance
    employee = Employee(**employee_data.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.CREATE,
        target_type="Employee",
        target_id=str(employee.id),
        details={
            "name": employee.name,
            "employee_id": employee.employee_id,
            "role": employee.role.value
        }
    )
    
    return EmployeeResponse.from_orm(employee)


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: UUID,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing employee record
    
    - **employee_id**: UUID of the employee to update
    - **employee_data**: Updated employee data (only provided fields will be updated)
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الموظف غير موجود"
        )
    
    # Check permissions
    if current_user.role != UserRole.GENERAL_ADMIN and employee.assigned_to_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بتعديل بيانات هذا الموظف"
        )
    
    # Check for unique employee_id if being updated
    if employee_data.employee_id and employee_data.employee_id != employee.employee_id:
        existing_employee = db.query(Employee).filter(Employee.employee_id == employee_data.employee_id).first()
        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رقم الموظف موجود بالفعل في النظام"
            )
    
    # Check for unique email if being updated
    if employee_data.email and employee_data.email != employee.email:
        existing_email = db.query(Employee).filter(Employee.email == employee_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="البريد الإلكتروني موجود بالفعل في النظام"
            )
    
    # Update only provided fields
    update_data = employee_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    db.commit()
    db.refresh(employee)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        target_type="Employee",
        target_id=str(employee.id),
        details={"updated_fields": list(update_data.keys())}
    )
    
    return EmployeeResponse.from_orm(employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an employee record (GENERAL_ADMIN only)
    
    - **employee_id**: UUID of the employee to delete
    """
    if current_user.role != UserRole.GENERAL_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="يجب أن تكون مسؤول عام لحذف سجلات الموظفين"
        )
    
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="الموظف غير موجود"
        )
    
    # Log audit before deletion
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.DELETE,
        target_type="Employee",
        target_id=str(employee.id),
        details={
            "name": employee.name,
            "employee_id": employee.employee_id,
            "role": employee.role.value
        }
    )
    
    db.delete(employee)
    db.commit()
    
    return None


@router.get("/stats/summary")
async def get_employee_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get summary statistics about employees
    
    Returns counts by role and active status
    """
    # Base query with user permissions
    query = db.query(Employee)
    if current_user.role != UserRole.GENERAL_ADMIN:
        query = query.filter(Employee.assigned_to_user_id == current_user.id)
    
    employees = query.all()
    
    # Calculate statistics
    total = len(employees)
    active_count = sum(1 for emp in employees if emp.is_active)
    inactive_count = total - active_count
    
    by_role = {}
    for emp in employees:
        role_key = emp.role.value if emp.role else "UNKNOWN"
        by_role[role_key] = by_role.get(role_key, 0) + 1
    
    return {
        "total": total,
        "active": active_count,
        "inactive": inactive_count,
        "by_role": by_role
    }
