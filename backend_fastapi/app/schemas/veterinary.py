"""
Veterinary Pydantic schemas for the K9 Operations Management System
"""
from pydantic import Field
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

from .enums import VisitType
from .common import BaseSchema, UUIDMixin


class VeterinaryVisitBase(BaseSchema):
    """Base VeterinaryVisit schema"""
    dog_id: UUID
    vet_id: UUID
    project_id: Optional[UUID] = None
    visit_type: VisitType
    visit_date: datetime
    weight: Optional[float] = Field(None, gt=0)
    temperature: Optional[float] = Field(None, gt=0)
    heart_rate: Optional[int] = Field(None, gt=0)
    blood_pressure: Optional[str] = Field(None, max_length=20)
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medications: List[dict] = Field(default_factory=list)
    stool_color: Optional[str] = Field(None, max_length=50)
    stool_consistency: Optional[str] = Field(None, max_length=50)
    urine_color: Optional[str] = Field(None, max_length=50)
    vaccinations_given: List[dict] = Field(default_factory=list)
    next_visit_date: Optional[date] = None
    notes: Optional[str] = None
    cost: Optional[float] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=120)
    weather: Optional[str] = Field(None, max_length=80)
    vital_signs: dict = Field(default_factory=dict)


class VeterinaryVisitCreate(VeterinaryVisitBase):
    """Schema for creating a veterinary visit"""
    pass


class VeterinaryVisitUpdate(BaseSchema):
    """Schema for updating a veterinary visit"""
    dog_id: Optional[UUID] = None
    vet_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    visit_type: Optional[VisitType] = None
    visit_date: Optional[datetime] = None
    weight: Optional[float] = Field(None, gt=0)
    temperature: Optional[float] = Field(None, gt=0)
    heart_rate: Optional[int] = Field(None, gt=0)
    blood_pressure: Optional[str] = Field(None, max_length=20)
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medications: Optional[List[dict]] = None
    stool_color: Optional[str] = Field(None, max_length=50)
    stool_consistency: Optional[str] = Field(None, max_length=50)
    urine_color: Optional[str] = Field(None, max_length=50)
    vaccinations_given: Optional[List[dict]] = None
    next_visit_date: Optional[date] = None
    notes: Optional[str] = None
    cost: Optional[float] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=120)
    weather: Optional[str] = Field(None, max_length=80)
    vital_signs: Optional[dict] = None


class VeterinaryVisitInDB(VeterinaryVisitBase, UUIDMixin):
    """Schema representing VeterinaryVisit in database"""
    created_at: datetime


class VeterinaryVisitResponse(VeterinaryVisitBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
