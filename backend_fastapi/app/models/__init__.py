"""
SQLAlchemy models for K9 Operations Management System

This module provides access to models from the existing Flask application.
We import them lazily to avoid circular dependencies and initialization issues.

Note: We reuse the existing SQLAlchemy models from the k9 package to ensure
both Flask and FastAPI work with the same database schema.
"""
import sys
import os

# Add project root to Python path to import k9 package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import enums directly (they don't depend on db instance)
from k9.models.models import (
    UserRole,
    EmployeeRole,
    DogStatus,
    DogGender,
    AuditAction,
    ProjectStatus,
    AttendanceStatus,
)

from k9.models.models_handler_daily import (
    ReportStatus,
    NotificationType,
)


def get_user_model():
    """Lazy import User model to avoid circular dependencies"""
    from k9.models.models import User
    return User


def get_audit_log_model():
    """Lazy import AuditLog model"""
    from k9.models.models import AuditLog
    return AuditLog


def get_employee_model():
    """Lazy import Employee model"""
    from k9.models.models import Employee
    return Employee


def get_dog_model():
    """Lazy import Dog model"""
    from k9.models.models import Dog
    return Dog


def get_project_model():
    """Lazy import Project model"""
    from k9.models.models import Project
    return Project


# For convenience, expose models via properties
# These will be imported only when accessed
class _Models:
    @property
    def User(self):
        return get_user_model()
    
    @property
    def AuditLog(self):
        return get_audit_log_model()
    
    @property
    def Employee(self):
        return get_employee_model()
    
    @property
    def Dog(self):
        return get_dog_model()
    
    @property
    def Project(self):
        return get_project_model()


models = _Models()

# Direct imports for commonly used models (use in services)
User = get_user_model()
AuditLog = get_audit_log_model()

__all__ = [
    # Enums
    "UserRole",
    "EmployeeRole", 
    "DogStatus",
    "DogGender",
    "AuditAction",
    "ProjectStatus",
    "AttendanceStatus",
    "ReportStatus",
    "NotificationType",
    
    # Models
    "User",
    "AuditLog",
    "models",
    
    # Lazy loaders
    "get_user_model",
    "get_audit_log_model",
    "get_employee_model",
    "get_dog_model",
    "get_project_model",
]
