"""
Project Pydantic schemas for the K9 Operations Management System
"""
from pydantic import Field
from typing import Optional, List
from datetime import date, datetime, time
from uuid import UUID

from .enums import (
    ProjectStatus, ElementType, PerformanceRating, TargetType
)
from .common import BaseSchema, UUIDMixin, TimestampMixin


class ProjectBase(BaseSchema):
    """Base Project schema with common fields"""
    name: str = Field(..., min_length=1, max_length=200)
    code: str = Field(..., min_length=1, max_length=20)
    main_task: Optional[str] = None
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNED
    start_date: date
    end_date: Optional[date] = None
    expected_completion_date: Optional[date] = None
    location: Optional[str] = Field(None, max_length=200)
    mission_type: Optional[str] = Field(None, max_length=100)
    priority: str = Field(default="MEDIUM", max_length=20)


class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    manager_id: Optional[UUID] = None
    project_manager_id: Optional[UUID] = None
    success_rating: Optional[int] = Field(None, ge=0, le=10)
    final_report: Optional[str] = None
    lessons_learned: Optional[str] = None


class ProjectUpdate(BaseSchema):
    """Schema for updating a project - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    main_task: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    expected_completion_date: Optional[date] = None
    location: Optional[str] = Field(None, max_length=200)
    mission_type: Optional[str] = Field(None, max_length=100)
    priority: Optional[str] = Field(None, max_length=20)
    manager_id: Optional[UUID] = None
    project_manager_id: Optional[UUID] = None
    success_rating: Optional[int] = Field(None, ge=0, le=10)
    final_report: Optional[str] = None
    lessons_learned: Optional[str] = None


class ProjectInDB(ProjectBase, UUIDMixin, TimestampMixin):
    """Schema representing Project in database"""
    duration_days: Optional[int] = None
    manager_id: Optional[UUID] = None
    project_manager_id: Optional[UUID] = None
    success_rating: Optional[int] = None
    final_report: Optional[str] = None
    lessons_learned: Optional[str] = None


class ProjectResponse(ProjectBase, UUIDMixin):
    """Schema for API responses"""
    duration_days: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    manager_id: Optional[UUID] = None
    project_manager_id: Optional[UUID] = None
    success_rating: Optional[int] = None


class ProjectAssignmentBase(BaseSchema):
    """Base ProjectAssignment schema"""
    project_id: UUID
    dog_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    is_active: bool = True
    assigned_from: datetime
    assigned_to: Optional[datetime] = None
    notes: Optional[str] = None


class ProjectAssignmentCreate(ProjectAssignmentBase):
    """Schema for creating a project assignment"""
    pass


class ProjectAssignmentUpdate(BaseSchema):
    """Schema for updating a project assignment"""
    is_active: Optional[bool] = None
    assigned_to: Optional[datetime] = None
    notes: Optional[str] = None


class ProjectAssignmentInDB(ProjectAssignmentBase, UUIDMixin, TimestampMixin):
    """Schema representing ProjectAssignment in database"""
    assigned_date: date
    unassigned_date: Optional[date] = None


class ProjectAssignmentResponse(ProjectAssignmentBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class IncidentBase(BaseSchema):
    """Base Incident schema"""
    project_id: UUID
    name: str = Field(..., min_length=1, max_length=200)
    incident_date: date
    incident_time: time
    incident_type: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    severity: str = Field(default="MEDIUM", max_length=20)


class IncidentCreate(IncidentBase):
    """Schema for creating an incident"""
    reported_by: Optional[UUID] = None
    people_involved: List[UUID] = Field(default_factory=list)
    dogs_involved: List[UUID] = Field(default_factory=list)
    attachments: List[str] = Field(default_factory=list)
    witness_statements: Optional[str] = None
    resolved: bool = False
    resolution_notes: Optional[str] = None
    resolution_date: Optional[date] = None


class IncidentUpdate(BaseSchema):
    """Schema for updating an incident"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    incident_date: Optional[date] = None
    incident_time: Optional[time] = None
    incident_type: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    severity: Optional[str] = Field(None, max_length=20)
    reported_by: Optional[UUID] = None
    people_involved: Optional[List[UUID]] = None
    dogs_involved: Optional[List[UUID]] = None
    attachments: Optional[List[str]] = None
    witness_statements: Optional[str] = None
    resolved: Optional[bool] = None
    resolution_notes: Optional[str] = None
    resolution_date: Optional[date] = None


class IncidentInDB(IncidentBase, UUIDMixin, TimestampMixin):
    """Schema representing Incident in database"""
    reported_by: Optional[UUID] = None
    people_involved: List[UUID]
    dogs_involved: List[UUID]
    attachments: List[str]
    witness_statements: Optional[str] = None
    resolved: bool
    resolution_notes: Optional[str] = None
    resolution_date: Optional[date] = None


class IncidentResponse(IncidentBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    reported_by: Optional[UUID] = None
    resolved: bool


class SuspicionBase(BaseSchema):
    """Base Suspicion schema"""
    project_id: UUID
    element_type: ElementType
    suspicion_type: Optional[str] = Field(None, max_length=100)
    risk_level: str = Field(default="MEDIUM", max_length=20)
    subtype: Optional[str] = Field(None, max_length=100)
    discovery_date: date
    discovery_time: time
    location: str = Field(..., min_length=1, max_length=200)


class SuspicionCreate(SuspicionBase):
    """Schema for creating a suspicion"""
    detected_by_dog: Optional[UUID] = None
    handler: Optional[UUID] = None
    detection_method: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    quantity_estimate: Optional[str] = Field(None, max_length=100)
    attachments: List[str] = Field(default_factory=list)
    authorities_notified: bool = False
    evidence_collected: bool = False
    follow_up_required: bool = True
    follow_up_notes: Optional[str] = None


class SuspicionUpdate(BaseSchema):
    """Schema for updating a suspicion"""
    element_type: Optional[ElementType] = None
    suspicion_type: Optional[str] = Field(None, max_length=100)
    risk_level: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    authorities_notified: Optional[bool] = None
    evidence_collected: Optional[bool] = None
    follow_up_required: Optional[bool] = None
    follow_up_notes: Optional[str] = None


class SuspicionInDB(SuspicionBase, UUIDMixin, TimestampMixin):
    """Schema representing Suspicion in database"""
    detected_by_dog: Optional[UUID] = None
    handler: Optional[UUID] = None
    detection_method: Optional[str] = None
    description: Optional[str] = None
    quantity_estimate: Optional[str] = None
    attachments: List[str]
    authorities_notified: bool
    evidence_collected: bool
    follow_up_required: bool
    follow_up_notes: Optional[str] = None


class SuspicionResponse(SuspicionBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    detected_by_dog: Optional[UUID] = None
    handler: Optional[UUID] = None


class PerformanceEvaluationBase(BaseSchema):
    """Base PerformanceEvaluation schema"""
    project_id: UUID
    evaluator_id: UUID
    target_type: TargetType
    target_employee_id: Optional[UUID] = None
    target_dog_id: Optional[UUID] = None
    evaluation_date: date
    rating: PerformanceRating


class PerformanceEvaluationCreate(PerformanceEvaluationBase):
    """Schema for creating a performance evaluation"""
    uniform_ok: bool = True
    id_card_ok: bool = True
    appearance_ok: bool = True
    cleanliness_ok: bool = True
    punctuality: Optional[int] = Field(None, ge=1, le=10)
    job_knowledge: Optional[int] = Field(None, ge=1, le=10)
    teamwork: Optional[int] = Field(None, ge=1, le=10)
    communication: Optional[int] = Field(None, ge=1, le=10)
    obedience_level: Optional[int] = Field(None, ge=1, le=10)
    detection_accuracy: Optional[int] = Field(None, ge=1, le=10)
    physical_condition: Optional[int] = Field(None, ge=1, le=10)
    handler_relationship: Optional[int] = Field(None, ge=1, le=10)
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    comments: Optional[str] = None
    recommendations: Optional[str] = None


class PerformanceEvaluationUpdate(BaseSchema):
    """Schema for updating a performance evaluation"""
    rating: Optional[PerformanceRating] = None
    uniform_ok: Optional[bool] = None
    id_card_ok: Optional[bool] = None
    appearance_ok: Optional[bool] = None
    cleanliness_ok: Optional[bool] = None
    punctuality: Optional[int] = Field(None, ge=1, le=10)
    job_knowledge: Optional[int] = Field(None, ge=1, le=10)
    teamwork: Optional[int] = Field(None, ge=1, le=10)
    communication: Optional[int] = Field(None, ge=1, le=10)
    obedience_level: Optional[int] = Field(None, ge=1, le=10)
    detection_accuracy: Optional[int] = Field(None, ge=1, le=10)
    physical_condition: Optional[int] = Field(None, ge=1, le=10)
    handler_relationship: Optional[int] = Field(None, ge=1, le=10)
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    comments: Optional[str] = None
    recommendations: Optional[str] = None


class PerformanceEvaluationInDB(PerformanceEvaluationBase, UUIDMixin, TimestampMixin):
    """Schema representing PerformanceEvaluation in database"""
    uniform_ok: bool
    id_card_ok: bool
    appearance_ok: bool
    cleanliness_ok: bool
    punctuality: Optional[int] = None
    job_knowledge: Optional[int] = None
    teamwork: Optional[int] = None
    communication: Optional[int] = None
    obedience_level: Optional[int] = None
    detection_accuracy: Optional[int] = None
    physical_condition: Optional[int] = None
    handler_relationship: Optional[int] = None
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    comments: Optional[str] = None
    recommendations: Optional[str] = None


class PerformanceEvaluationResponse(PerformanceEvaluationBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    uniform_ok: bool
    id_card_ok: bool
    appearance_ok: bool
    cleanliness_ok: bool
