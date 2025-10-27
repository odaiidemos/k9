"""
User Pydantic schemas for the K9 Operations Management System
"""
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from .enums import UserRole
from .common import BaseSchema, UUIDMixin, TimestampMixin


class UserBase(BaseSchema):
    """Base User schema with common fields"""
    username: str = Field(..., min_length=3, max_length=80)
    email: EmailStr
    role: UserRole
    full_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    allowed_sections: List[str] = Field(default_factory=list)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=128)
    project_id: Optional[UUID] = None
    dog_id: Optional[UUID] = None


class UserUpdate(BaseSchema):
    """Schema for updating a user - all fields optional"""
    username: Optional[str] = Field(None, min_length=3, max_length=80)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    allowed_sections: Optional[List[str]] = None
    active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    project_id: Optional[UUID] = None
    dog_id: Optional[UUID] = None
    mfa_enabled: Optional[bool] = None


class UserInDB(UserBase, UUIDMixin, TimestampMixin):
    """Schema representing User in database"""
    password_hash: str
    active: bool
    last_login: Optional[datetime] = None
    
    # Security fields
    failed_login_attempts: int
    account_locked_until: Optional[datetime] = None
    password_changed_at: datetime
    
    # MFA fields
    mfa_enabled: bool
    mfa_secret: Optional[str] = None
    backup_codes: List[str] = Field(default_factory=list)
    
    # Handler-specific fields
    project_id: Optional[UUID] = None
    dog_id: Optional[UUID] = None


class UserResponse(UserBase, UUIDMixin):
    """Schema for API responses - excludes sensitive data"""
    active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    mfa_enabled: bool
    project_id: Optional[UUID] = None
    dog_id: Optional[UUID] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class UserPasswordChange(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class UserMFASetup(BaseModel):
    """Schema for MFA setup"""
    mfa_secret: str
    verification_code: str


class UserMFAVerify(BaseModel):
    """Schema for MFA verification"""
    code: str
