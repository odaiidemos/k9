"""
Training Pydantic schemas for the K9 Operations Management System
"""
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from .enums import TrainingCategory, SocializationType, BallWorkType
from .common import BaseSchema, UUIDMixin, TimestampMixin


class TrainingSessionBase(BaseSchema):
    """Base TrainingSession schema"""
    dog_id: UUID
    trainer_id: UUID
    project_id: Optional[UUID] = None
    category: TrainingCategory
    subject: str = Field(..., min_length=1, max_length=200)
    session_date: datetime
    duration: int = Field(..., gt=0)
    success_rating: int = Field(..., ge=0, le=10)
    location: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    weather_conditions: Optional[str] = Field(None, max_length=100)
    equipment_used: List[str] = Field(default_factory=list)


class TrainingSessionCreate(TrainingSessionBase):
    """Schema for creating a training session"""
    pass


class TrainingSessionUpdate(BaseSchema):
    """Schema for updating a training session"""
    dog_id: Optional[UUID] = None
    trainer_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    category: Optional[TrainingCategory] = None
    subject: Optional[str] = Field(None, min_length=1, max_length=200)
    session_date: Optional[datetime] = None
    duration: Optional[int] = Field(None, gt=0)
    success_rating: Optional[int] = Field(None, ge=0, le=10)
    location: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    weather_conditions: Optional[str] = Field(None, max_length=100)
    equipment_used: Optional[List[str]] = None


class TrainingSessionInDB(TrainingSessionBase, UUIDMixin):
    """Schema representing TrainingSession in database"""
    created_at: datetime


class TrainingSessionResponse(TrainingSessionBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class BreedingTrainingActivityBase(BaseSchema):
    """Base BreedingTrainingActivity schema"""
    project_id: Optional[UUID] = None
    dog_id: UUID
    trainer_id: UUID
    session_date: datetime
    category: TrainingCategory
    subtype_socialization: Optional[SocializationType] = None
    subtype_ball: Optional[BallWorkType] = None
    subject: str
    duration: int = Field(..., gt=0)
    duration_days: Optional[int] = Field(None, gt=0)
    success_rating: int = Field(..., ge=1, le=5)
    location: Optional[str] = Field(None, max_length=100)
    weather_conditions: Optional[str] = Field(None, max_length=100)
    equipment_used: List[dict] = Field(default_factory=list)
    notes: Optional[str] = None


class BreedingTrainingActivityCreate(BreedingTrainingActivityBase):
    """Schema for creating a breeding training activity"""
    pass


class BreedingTrainingActivityUpdate(BaseSchema):
    """Schema for updating a breeding training activity"""
    project_id: Optional[UUID] = None
    dog_id: Optional[UUID] = None
    trainer_id: Optional[UUID] = None
    session_date: Optional[datetime] = None
    category: Optional[TrainingCategory] = None
    subtype_socialization: Optional[SocializationType] = None
    subtype_ball: Optional[BallWorkType] = None
    subject: Optional[str] = None
    duration: Optional[int] = Field(None, gt=0)
    duration_days: Optional[int] = Field(None, gt=0)
    success_rating: Optional[int] = Field(None, ge=1, le=5)
    location: Optional[str] = Field(None, max_length=100)
    weather_conditions: Optional[str] = Field(None, max_length=100)
    equipment_used: Optional[List[dict]] = None
    notes: Optional[str] = None


class BreedingTrainingActivityInDB(BreedingTrainingActivityBase, UUIDMixin, TimestampMixin):
    """Schema representing BreedingTrainingActivity in database"""
    created_by_user_id: Optional[UUID] = None


class BreedingTrainingActivityResponse(BreedingTrainingActivityBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    updated_at: Optional[datetime] = None


class PuppyTrainingBase(BaseSchema):
    """Base PuppyTraining schema"""
    puppy_id: UUID
    trainer_id: UUID
    training_name: str = Field(..., min_length=1, max_length=200)
    training_type: TrainingCategory
    session_date: datetime
    duration: int = Field(..., gt=0)
    puppy_age_weeks: Optional[int] = Field(None, ge=0)
    developmental_stage: Optional[str] = Field(None, max_length=50)
    success_rating: int = Field(..., ge=0, le=10)
    skills_learned: List[str] = Field(default_factory=list)
    behavior_observations: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    weather_conditions: Optional[str] = Field(None, max_length=100)
    equipment_used: List[str] = Field(default_factory=list)
    previous_skills: List[str] = Field(default_factory=list)
    new_skills_acquired: List[str] = Field(default_factory=list)
    areas_for_improvement: Optional[str] = None
    notes: Optional[str] = None


class PuppyTrainingCreate(PuppyTrainingBase):
    """Schema for creating a puppy training session"""
    pass


class PuppyTrainingUpdate(BaseSchema):
    """Schema for updating a puppy training session"""
    training_name: Optional[str] = Field(None, min_length=1, max_length=200)
    training_type: Optional[TrainingCategory] = None
    session_date: Optional[datetime] = None
    duration: Optional[int] = Field(None, gt=0)
    puppy_age_weeks: Optional[int] = Field(None, ge=0)
    developmental_stage: Optional[str] = Field(None, max_length=50)
    success_rating: Optional[int] = Field(None, ge=0, le=10)
    skills_learned: Optional[List[str]] = None
    behavior_observations: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    weather_conditions: Optional[str] = Field(None, max_length=100)
    equipment_used: Optional[List[str]] = None
    previous_skills: Optional[List[str]] = None
    new_skills_acquired: Optional[List[str]] = None
    areas_for_improvement: Optional[str] = None
    notes: Optional[str] = None


class PuppyTrainingInDB(PuppyTrainingBase, UUIDMixin):
    """Schema representing PuppyTraining in database"""
    created_at: datetime


class PuppyTrainingResponse(PuppyTrainingBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
