"""
Audit and Permission Pydantic schemas for the K9 Operations Management System
"""
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from .enums import AuditAction, PermissionType
from .common import BaseSchema, UUIDMixin, TimestampMixin


class AuditLogBase(BaseSchema):
    """Base AuditLog schema"""
    user_id: UUID
    action: AuditAction
    target_type: Optional[str] = Field(None, max_length=50)
    target_id: Optional[UUID] = None
    target_name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    old_values: dict = Field(default_factory=dict)
    new_values: dict = Field(default_factory=dict)
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    session_id: Optional[str] = Field(None, max_length=255)
    extra_data: dict = Field(default_factory=dict)


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log"""
    pass


class AuditLogInDB(AuditLogBase, UUIDMixin):
    """Schema representing AuditLog in database"""
    created_at: datetime


class AuditLogResponse(AuditLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class SubPermissionBase(BaseSchema):
    """Base SubPermission schema"""
    user_id: UUID
    section: str = Field(..., max_length=50)
    subsection: str = Field(..., max_length=100)
    permission_type: PermissionType
    project_id: Optional[UUID] = None
    is_granted: bool = False


class SubPermissionCreate(SubPermissionBase):
    """Schema for creating a sub-permission"""
    pass


class SubPermissionUpdate(BaseSchema):
    """Schema for updating a sub-permission"""
    is_granted: Optional[bool] = None


class SubPermissionInDB(SubPermissionBase, UUIDMixin, TimestampMixin):
    """Schema representing SubPermission in database"""
    pass


class SubPermissionResponse(SubPermissionBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class PermissionAuditLogBase(BaseSchema):
    """Base PermissionAuditLog schema"""
    changed_by_user_id: UUID
    target_user_id: UUID
    section: str = Field(..., max_length=50)
    subsection: str = Field(..., max_length=100)
    permission_type: PermissionType
    project_id: Optional[UUID] = None
    old_value: bool
    new_value: bool
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None


class PermissionAuditLogCreate(PermissionAuditLogBase):
    """Schema for creating a permission audit log"""
    pass


class PermissionAuditLogInDB(PermissionAuditLogBase, UUIDMixin):
    """Schema representing PermissionAuditLog in database"""
    created_at: datetime


class PermissionAuditLogResponse(PermissionAuditLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class ProjectManagerPermissionBase(BaseSchema):
    """Base ProjectManagerPermission schema (legacy)"""
    user_id: UUID
    project_id: UUID
    can_manage_assignments: bool = True
    can_manage_shifts: bool = True
    can_manage_attendance: bool = True
    can_manage_training: bool = True
    can_manage_incidents: bool = True
    can_manage_performance: bool = True
    can_view_veterinary: bool = True
    can_view_breeding: bool = True


class ProjectManagerPermissionCreate(ProjectManagerPermissionBase):
    """Schema for creating a project manager permission"""
    pass


class ProjectManagerPermissionUpdate(BaseSchema):
    """Schema for updating a project manager permission"""
    can_manage_assignments: Optional[bool] = None
    can_manage_shifts: Optional[bool] = None
    can_manage_attendance: Optional[bool] = None
    can_manage_training: Optional[bool] = None
    can_manage_incidents: Optional[bool] = None
    can_manage_performance: Optional[bool] = None
    can_view_veterinary: Optional[bool] = None
    can_view_breeding: Optional[bool] = None


class ProjectManagerPermissionInDB(ProjectManagerPermissionBase, UUIDMixin, TimestampMixin):
    """Schema representing ProjectManagerPermission in database"""
    pass


class ProjectManagerPermissionResponse(ProjectManagerPermissionBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class BackupSettingsBase(BaseSchema):
    """Base BackupSettings schema"""
    auto_backup_enabled: bool = False
    backup_frequency: str = "DISABLED"
    backup_hour: int = Field(default=2, ge=0, le=23)
    retention_days: int = Field(default=30, gt=0)
    google_drive_enabled: bool = False
    google_drive_folder_id: Optional[str] = Field(None, max_length=255)
    google_drive_credentials: Optional[str] = None


class BackupSettingsCreate(BackupSettingsBase):
    """Schema for creating backup settings"""
    updated_by_user_id: UUID


class BackupSettingsUpdate(BaseSchema):
    """Schema for updating backup settings"""
    auto_backup_enabled: Optional[bool] = None
    backup_frequency: Optional[str] = None
    backup_hour: Optional[int] = Field(None, ge=0, le=23)
    retention_days: Optional[int] = Field(None, gt=0)
    google_drive_enabled: Optional[bool] = None
    google_drive_folder_id: Optional[str] = Field(None, max_length=255)
    google_drive_credentials: Optional[str] = None
    updated_by_user_id: Optional[UUID] = None


class BackupSettingsInDB(BackupSettingsBase):
    """Schema representing BackupSettings in database"""
    id: int
    last_backup_at: Optional[datetime] = None
    last_backup_status: Optional[str] = Field(None, max_length=50)
    last_backup_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    updated_by_user_id: Optional[UUID] = None


class BackupSettingsResponse(BackupSettingsBase):
    """Schema for API responses"""
    id: int
    last_backup_at: Optional[datetime] = None
    last_backup_status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
