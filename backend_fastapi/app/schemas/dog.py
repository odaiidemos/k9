"""
Dog Pydantic schemas for the K9 Operations Management System
"""
from pydantic import Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

from .enums import DogStatus, DogGender
from .common import BaseSchema, UUIDMixin, TimestampMixin


class DogBase(BaseSchema):
    """Base Dog schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=20)
    breed: str = Field(..., min_length=1, max_length=100)
    family_line: Optional[str] = Field(None, max_length=100)
    gender: DogGender
    birth_date: date
    microchip_id: Optional[str] = Field(None, max_length=50)
    current_status: DogStatus = DogStatus.ACTIVE
    location: Optional[str] = Field(None, max_length=100)
    specialization: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    weight: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)


class DogCreate(DogBase):
    """Schema for creating a new dog"""
    birth_certificate: Optional[str] = Field(None, max_length=255)
    photo: Optional[str] = Field(None, max_length=255)
    medical_records: List[str] = Field(default_factory=list)
    assigned_to_user_id: Optional[UUID] = None
    father_id: Optional[UUID] = None
    mother_id: Optional[UUID] = None


class DogUpdate(BaseSchema):
    """Schema for updating a dog - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    breed: Optional[str] = Field(None, min_length=1, max_length=100)
    family_line: Optional[str] = Field(None, max_length=100)
    gender: Optional[DogGender] = None
    birth_date: Optional[date] = None
    microchip_id: Optional[str] = Field(None, max_length=50)
    current_status: Optional[DogStatus] = None
    location: Optional[str] = Field(None, max_length=100)
    specialization: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    weight: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)
    birth_certificate: Optional[str] = Field(None, max_length=255)
    photo: Optional[str] = Field(None, max_length=255)
    medical_records: Optional[List[str]] = None
    assigned_to_user_id: Optional[UUID] = None
    father_id: Optional[UUID] = None
    mother_id: Optional[UUID] = None


class DogInDB(DogBase, UUIDMixin, TimestampMixin):
    """Schema representing Dog in database"""
    birth_certificate: Optional[str] = None
    photo: Optional[str] = None
    medical_records: List[str]
    assigned_to_user_id: Optional[UUID] = None
    father_id: Optional[UUID] = None
    mother_id: Optional[UUID] = None


class DogResponse(DogBase, UUIDMixin):
    """Schema for API responses"""
    birth_certificate: Optional[str] = None
    photo: Optional[str] = None
    medical_records: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None
    assigned_to_user_id: Optional[UUID] = None
    father_id: Optional[UUID] = None
    mother_id: Optional[UUID] = None
