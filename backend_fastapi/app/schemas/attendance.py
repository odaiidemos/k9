"""
Attendance Pydantic schemas for the K9 Operations Management System
Includes both project-specific and standalone attendance systems
"""
from pydantic import Field
from typing import Optional
from datetime import datetime, date, time
from uuid import UUID

from .enums import AttendanceStatus, AbsenceReason, EntityType
from .common import BaseSchema, UUIDMixin, TimestampMixin


class AttendanceRecordBase(BaseSchema):
    """Base AttendanceRecord schema (project-specific attendance)"""
    project_assignment_id: UUID
    date: date
    status: AttendanceStatus
    notes: Optional[str] = None
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None


class AttendanceRecordCreate(AttendanceRecordBase):
    """Schema for creating an attendance record"""
    recorded_by: UUID
    absence_reason: Optional[AbsenceReason] = None


class AttendanceRecordUpdate(BaseSchema):
    """Schema for updating an attendance record"""
    status: Optional[AttendanceStatus] = None
    notes: Optional[str] = None
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    absence_reason: Optional[AbsenceReason] = None


class AttendanceRecordInDB(AttendanceRecordBase, UUIDMixin, TimestampMixin):
    """Schema representing AttendanceRecord in database"""
    recorded_by: UUID
    absence_reason: Optional[AbsenceReason] = None


class AttendanceRecordResponse(AttendanceRecordBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    recorded_by: UUID
    absence_reason: Optional[AbsenceReason] = None


class ProjectShiftBase(BaseSchema):
    """Base ProjectShift schema"""
    project_id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    start_time: time
    end_time: time
    is_active: bool = True


class ProjectShiftCreate(ProjectShiftBase):
    """Schema for creating a project shift"""
    pass


class ProjectShiftUpdate(BaseSchema):
    """Schema for updating a project shift"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_active: Optional[bool] = None


class ProjectShiftInDB(ProjectShiftBase, UUIDMixin, TimestampMixin):
    """Schema representing ProjectShift in database"""
    pass


class ProjectShiftResponse(ProjectShiftBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class ProjectShiftAssignmentBase(BaseSchema):
    """Base ProjectShiftAssignment schema"""
    project_shift_id: UUID
    entity_type: EntityType
    entity_id: UUID
    is_active: bool = True
    assigned_date: date
    notes: Optional[str] = None


class ProjectShiftAssignmentCreate(ProjectShiftAssignmentBase):
    """Schema for creating a project shift assignment"""
    pass


class ProjectShiftAssignmentUpdate(BaseSchema):
    """Schema for updating a project shift assignment"""
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class ProjectShiftAssignmentInDB(ProjectShiftAssignmentBase, UUIDMixin, TimestampMixin):
    """Schema representing ProjectShiftAssignment in database"""
    pass


class ProjectShiftAssignmentResponse(ProjectShiftAssignmentBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class ProjectAttendanceBase(BaseSchema):
    """Base ProjectAttendance schema"""
    project_shift_id: UUID
    date: date
    entity_type: EntityType
    entity_id: UUID
    status: AttendanceStatus
    absence_reason: Optional[AbsenceReason] = None
    late_reason: Optional[str] = None
    notes: Optional[str] = None
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None


class ProjectAttendanceCreate(ProjectAttendanceBase):
    """Schema for creating a project attendance record"""
    recorded_by_user_id: UUID


class ProjectAttendanceUpdate(BaseSchema):
    """Schema for updating a project attendance record"""
    status: Optional[AttendanceStatus] = None
    absence_reason: Optional[AbsenceReason] = None
    late_reason: Optional[str] = None
    notes: Optional[str] = None
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None


class ProjectAttendanceInDB(ProjectAttendanceBase, UUIDMixin, TimestampMixin):
    """Schema representing ProjectAttendance in database"""
    recorded_by_user_id: UUID


class ProjectAttendanceResponse(ProjectAttendanceBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    recorded_by_user_id: UUID


class ShiftBase(BaseSchema):
    """Base Shift schema (standalone, not project-specific)"""
    name: str = Field(..., min_length=1, max_length=100)
    start_time: time
    end_time: time
    is_active: bool = True


class ShiftCreate(ShiftBase):
    """Schema for creating a standalone shift"""
    pass


class ShiftUpdate(BaseSchema):
    """Schema for updating a standalone shift"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_active: Optional[bool] = None


class ShiftInDB(ShiftBase, UUIDMixin, TimestampMixin):
    """Schema representing Shift in database"""
    pass


class ShiftResponse(ShiftBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class ShiftAssignmentBase(BaseSchema):
    """Base ShiftAssignment schema (standalone)"""
    shift_id: UUID
    entity_type: EntityType
    entity_id: UUID
    is_active: bool = True
    assigned_date: date
    notes: Optional[str] = None


class ShiftAssignmentCreate(ShiftAssignmentBase):
    """Schema for creating a standalone shift assignment"""
    pass


class ShiftAssignmentUpdate(BaseSchema):
    """Schema for updating a standalone shift assignment"""
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class ShiftAssignmentInDB(ShiftAssignmentBase, UUIDMixin, TimestampMixin):
    """Schema representing ShiftAssignment in database"""
    pass


class ShiftAssignmentResponse(ShiftAssignmentBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class AttendanceBase(BaseSchema):
    """Base Attendance schema (standalone, not project-specific)"""
    shift_id: UUID
    date: date
    entity_type: EntityType
    entity_id: UUID
    status: AttendanceStatus
    absence_reason: Optional[AbsenceReason] = None
    late_reason: Optional[str] = None
    notes: Optional[str] = None
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None


class AttendanceCreate(AttendanceBase):
    """Schema for creating a standalone attendance record"""
    recorded_by_user_id: UUID


class AttendanceUpdate(BaseSchema):
    """Schema for updating a standalone attendance record"""
    status: Optional[AttendanceStatus] = None
    absence_reason: Optional[AbsenceReason] = None
    late_reason: Optional[str] = None
    notes: Optional[str] = None
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None


class AttendanceInDB(AttendanceBase, UUIDMixin, TimestampMixin):
    """Schema representing Attendance in database"""
    recorded_by_user_id: UUID


class AttendanceResponse(AttendanceBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
    recorded_by_user_id: UUID


class AttendanceDayBase(BaseSchema):
    """Base AttendanceDay schema (unified global attendance)"""
    employee_id: UUID
    date: date
    status: AttendanceStatus
    note: Optional[str] = None
    source: str = Field(default="global", max_length=16)
    project_id: Optional[UUID] = None
    locked: bool = False


class AttendanceDayCreate(AttendanceDayBase):
    """Schema for creating an attendance day record"""
    pass


class AttendanceDayUpdate(BaseSchema):
    """Schema for updating an attendance day record"""
    status: Optional[AttendanceStatus] = None
    note: Optional[str] = None
    locked: Optional[bool] = None


class AttendanceDayInDB(AttendanceDayBase, UUIDMixin, TimestampMixin):
    """Schema representing AttendanceDay in database"""
    pass


class AttendanceDayResponse(AttendanceDayBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
