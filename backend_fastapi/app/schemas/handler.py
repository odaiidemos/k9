"""
Handler Daily System Pydantic schemas for the K9 Operations Management System
Includes DailySchedule, HandlerReport, Notification, and Task schemas
"""
from pydantic import Field
from typing import Optional
from datetime import datetime, date, time
from uuid import UUID

from .enums import (
    ScheduleStatus, ScheduleItemStatus, ReportStatus,
    HealthCheckStatus, TrainingType, BehaviorType, IncidentType,
    StoolColor, StoolShape, NotificationType, TaskStatus, TaskPriority
)
from .common import BaseSchema, UUIDMixin, TimestampMixin


class DailyScheduleBase(BaseSchema):
    """Base DailySchedule schema"""
    date: date
    project_id: Optional[UUID] = None
    status: ScheduleStatus = ScheduleStatus.OPEN
    notes: Optional[str] = None


class DailyScheduleCreate(DailyScheduleBase):
    """Schema for creating a daily schedule"""
    created_by_user_id: UUID


class DailyScheduleUpdate(BaseSchema):
    """Schema for updating a daily schedule"""
    status: Optional[ScheduleStatus] = None
    notes: Optional[str] = None


class DailyScheduleInDB(DailyScheduleBase, UUIDMixin, TimestampMixin):
    """Schema representing DailySchedule in database"""
    created_by_user_id: UUID


class DailyScheduleResponse(DailyScheduleBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    created_by_user_id: UUID


class DailyScheduleItemBase(BaseSchema):
    """Base DailyScheduleItem schema"""
    daily_schedule_id: UUID
    handler_user_id: UUID
    dog_id: Optional[UUID] = None
    shift_id: Optional[UUID] = None
    status: ScheduleItemStatus = ScheduleItemStatus.PLANNED
    replacement_handler_id: Optional[UUID] = None
    absence_reason: Optional[str] = Field(None, max_length=500)
    replacement_notes: Optional[str] = None


class DailyScheduleItemCreate(DailyScheduleItemBase):
    """Schema for creating a daily schedule item"""
    pass


class DailyScheduleItemUpdate(BaseSchema):
    """Schema for updating a daily schedule item"""
    status: Optional[ScheduleItemStatus] = None
    replacement_handler_id: Optional[UUID] = None
    absence_reason: Optional[str] = Field(None, max_length=500)
    replacement_notes: Optional[str] = None


class DailyScheduleItemInDB(DailyScheduleItemBase, UUIDMixin, TimestampMixin):
    """Schema representing DailyScheduleItem in database"""
    pass


class DailyScheduleItemResponse(DailyScheduleItemBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class HandlerReportBase(BaseSchema):
    """Base HandlerReport schema"""
    date: date
    schedule_item_id: Optional[UUID] = None
    handler_user_id: UUID
    dog_id: UUID
    project_id: Optional[UUID] = None
    location: Optional[str] = Field(None, max_length=200)
    status: ReportStatus = ReportStatus.DRAFT


class HandlerReportCreate(HandlerReportBase):
    """Schema for creating a handler report"""
    pass


class HandlerReportUpdate(BaseSchema):
    """Schema for updating a handler report"""
    location: Optional[str] = Field(None, max_length=200)
    status: Optional[ReportStatus] = None
    review_notes: Optional[str] = None


class HandlerReportInDB(HandlerReportBase, UUIDMixin, TimestampMixin):
    """Schema representing HandlerReport in database"""
    submitted_at: Optional[datetime] = None
    reviewed_by_user_id: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None


class HandlerReportResponse(HandlerReportBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    submitted_at: Optional[datetime] = None
    reviewed_by_user_id: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None


class HandlerReportHealthBase(BaseSchema):
    """Base HandlerReportHealth schema"""
    report_id: UUID
    eyes_status: Optional[HealthCheckStatus] = None
    eyes_notes: Optional[str] = Field(None, max_length=500)
    nose_status: Optional[HealthCheckStatus] = None
    nose_notes: Optional[str] = Field(None, max_length=500)
    ears_status: Optional[HealthCheckStatus] = None
    ears_notes: Optional[str] = Field(None, max_length=500)
    mouth_status: Optional[HealthCheckStatus] = None
    mouth_notes: Optional[str] = Field(None, max_length=500)
    teeth_status: Optional[HealthCheckStatus] = None
    teeth_notes: Optional[str] = Field(None, max_length=500)
    gums_status: Optional[HealthCheckStatus] = None
    gums_notes: Optional[str] = Field(None, max_length=500)
    front_limbs_status: Optional[HealthCheckStatus] = None
    front_limbs_notes: Optional[str] = Field(None, max_length=500)
    back_limbs_status: Optional[HealthCheckStatus] = None
    back_limbs_notes: Optional[str] = Field(None, max_length=500)
    hair_status: Optional[HealthCheckStatus] = None
    hair_notes: Optional[str] = Field(None, max_length=500)
    tail_status: Optional[HealthCheckStatus] = None
    tail_notes: Optional[str] = Field(None, max_length=500)
    rear_status: Optional[HealthCheckStatus] = None
    rear_notes: Optional[str] = Field(None, max_length=500)


class HandlerReportHealthCreate(HandlerReportHealthBase):
    """Schema for creating handler report health section"""
    pass


class HandlerReportHealthUpdate(HandlerReportHealthBase):
    """Schema for updating handler report health section"""
    pass


class HandlerReportHealthInDB(HandlerReportHealthBase, UUIDMixin):
    """Schema representing HandlerReportHealth in database"""
    pass


class HandlerReportHealthResponse(HandlerReportHealthBase, UUIDMixin):
    """Schema for API responses"""
    pass


class HandlerReportTrainingBase(BaseSchema):
    """Base HandlerReportTraining schema"""
    report_id: UUID
    training_type: TrainingType
    description: Optional[str] = None
    time_from: Optional[time] = None
    time_to: Optional[time] = None
    notes: Optional[str] = None


class HandlerReportTrainingCreate(HandlerReportTrainingBase):
    """Schema for creating handler report training session"""
    pass


class HandlerReportTrainingUpdate(BaseSchema):
    """Schema for updating handler report training session"""
    training_type: Optional[TrainingType] = None
    description: Optional[str] = None
    time_from: Optional[time] = None
    time_to: Optional[time] = None
    notes: Optional[str] = None


class HandlerReportTrainingInDB(HandlerReportTrainingBase, UUIDMixin):
    """Schema representing HandlerReportTraining in database"""
    pass


class HandlerReportTrainingResponse(HandlerReportTrainingBase, UUIDMixin):
    """Schema for API responses"""
    pass


class HandlerReportCareBase(BaseSchema):
    """Base HandlerReportCare schema"""
    report_id: UUID
    food_amount: Optional[str] = Field(None, max_length=100)
    food_type: Optional[str] = Field(None, max_length=200)
    supplements: Optional[str] = Field(None, max_length=200)
    water_amount: Optional[str] = Field(None, max_length=100)
    grooming_done: bool = False
    washing_done: bool = False
    excretion_location: Optional[str] = Field(None, max_length=200)
    stool_color: Optional[StoolColor] = None
    stool_shape: Optional[StoolShape] = None


class HandlerReportCareCreate(HandlerReportCareBase):
    """Schema for creating handler report care section"""
    pass


class HandlerReportCareUpdate(HandlerReportCareBase):
    """Schema for updating handler report care section"""
    pass


class HandlerReportCareInDB(HandlerReportCareBase, UUIDMixin):
    """Schema representing HandlerReportCare in database"""
    pass


class HandlerReportCareResponse(HandlerReportCareBase, UUIDMixin):
    """Schema for API responses"""
    pass


class HandlerReportBehaviorBase(BaseSchema):
    """Base HandlerReportBehavior schema"""
    report_id: UUID
    good_behavior_notes: Optional[str] = None
    bad_behavior_notes: Optional[str] = None


class HandlerReportBehaviorCreate(HandlerReportBehaviorBase):
    """Schema for creating handler report behavior section"""
    pass


class HandlerReportBehaviorUpdate(HandlerReportBehaviorBase):
    """Schema for updating handler report behavior section"""
    pass


class HandlerReportBehaviorInDB(HandlerReportBehaviorBase, UUIDMixin):
    """Schema representing HandlerReportBehavior in database"""
    pass


class HandlerReportBehaviorResponse(HandlerReportBehaviorBase, UUIDMixin):
    """Schema for API responses"""
    pass


class HandlerReportIncidentBase(BaseSchema):
    """Base HandlerReportIncident schema"""
    report_id: UUID
    incident_type: IncidentType
    description: str
    incident_datetime: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=200)


class HandlerReportIncidentCreate(HandlerReportIncidentBase):
    """Schema for creating handler report incident"""
    pass


class HandlerReportIncidentUpdate(BaseSchema):
    """Schema for updating handler report incident"""
    incident_type: Optional[IncidentType] = None
    description: Optional[str] = None
    incident_datetime: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=200)


class HandlerReportIncidentInDB(HandlerReportIncidentBase, UUIDMixin):
    """Schema representing HandlerReportIncident in database"""
    pass


class HandlerReportIncidentResponse(HandlerReportIncidentBase, UUIDMixin):
    """Schema for API responses"""
    pass


class HandlerReportAttachmentBase(BaseSchema):
    """Base HandlerReportAttachment schema"""
    incident_id: UUID
    filename: str = Field(..., max_length=255)
    original_filename: str = Field(..., max_length=255)
    file_path: str = Field(..., max_length=500)
    file_type: str = Field(..., max_length=50)
    file_size: int
    sha256_hash: str = Field(..., max_length=64)


class HandlerReportAttachmentCreate(HandlerReportAttachmentBase):
    """Schema for creating handler report attachment"""
    pass


class HandlerReportAttachmentInDB(HandlerReportAttachmentBase, UUIDMixin):
    """Schema representing HandlerReportAttachment in database"""
    uploaded_at: datetime


class HandlerReportAttachmentResponse(HandlerReportAttachmentBase, UUIDMixin):
    """Schema for API responses"""
    uploaded_at: datetime


class NotificationBase(BaseSchema):
    """Base Notification schema"""
    user_id: UUID
    type: NotificationType
    title: str = Field(..., max_length=200)
    message: str
    related_id: Optional[str] = Field(None, max_length=36)
    related_type: Optional[str] = Field(None, max_length=50)
    read: bool = False


class NotificationCreate(NotificationBase):
    """Schema for creating a notification"""
    pass


class NotificationUpdate(BaseSchema):
    """Schema for updating a notification"""
    read: Optional[bool] = None


class NotificationInDB(NotificationBase, UUIDMixin):
    """Schema representing Notification in database"""
    read_at: Optional[datetime] = None
    created_at: datetime


class NotificationResponse(NotificationBase, UUIDMixin):
    """Schema for API responses"""
    read_at: Optional[datetime] = None
    created_at: datetime


class TaskBase(BaseSchema):
    """Base Task schema"""
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_to_user_id: UUID
    project_id: Optional[UUID] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    created_by_user_id: UUID


class TaskUpdate(BaseSchema):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None


class TaskInDB(TaskBase, UUIDMixin, TimestampMixin):
    """Schema representing Task in database"""
    created_by_user_id: UUID
    completed_at: Optional[datetime] = None


class TaskResponse(TaskBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    created_by_user_id: UUID
    completed_at: Optional[datetime] = None
