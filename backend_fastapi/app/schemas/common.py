"""
Common schemas and base classes for the K9 Operations Management System
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class TimestampMixin(BaseModel):
    """Mixin for created_at and updated_at timestamps"""
    created_at: datetime
    updated_at: Optional[datetime] = None


class UUIDMixin(BaseModel):
    """Mixin for UUID primary key"""
    id: UUID
