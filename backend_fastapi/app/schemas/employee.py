"""
Employee Pydantic schemas for the K9 Operations Management System
"""
from pydantic import EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

from .enums import EmployeeRole
from .common import BaseSchema, UUIDMixin, TimestampMixin


class EmployeeBase(BaseSchema):
    """Base Employee schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100)
    employee_id: str = Field(..., min_length=1, max_length=20)
    role: EmployeeRole
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    hire_date: date


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee"""
    certifications: List[dict] = Field(default_factory=list)
    assigned_to_user_id: Optional[UUID] = None
    user_account_id: Optional[UUID] = None


class EmployeeUpdate(BaseSchema):
    """Schema for updating an employee - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    employee_id: Optional[str] = Field(None, min_length=1, max_length=20)
    role: Optional[EmployeeRole] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    hire_date: Optional[date] = None
    is_active: Optional[bool] = None
    certifications: Optional[List[dict]] = None
    assigned_to_user_id: Optional[UUID] = None
    user_account_id: Optional[UUID] = None


class EmployeeInDB(EmployeeBase, UUIDMixin, TimestampMixin):
    """Schema representing Employee in database"""
    is_active: bool
    certifications: List[dict]
    assigned_to_user_id: Optional[UUID] = None
    user_account_id: Optional[UUID] = None


class EmployeeResponse(EmployeeBase, UUIDMixin):
    """Schema for API responses"""
    is_active: bool
    certifications: List[dict]
    created_at: datetime
    updated_at: Optional[datetime] = None
    assigned_to_user_id: Optional[UUID] = None
    user_account_id: Optional[UUID] = None
