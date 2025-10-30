"""
SQLAlchemy models for K9 Operations Management System

This module provides access to models from the shared k9_shared.db instance.
All models now use the framework-agnostic shared SQLAlchemy instance.
"""
import sys
import os

# Add project root to Python path to import k9 package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import shared db instance
from k9_shared.db import db

# Import enums
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
    ScheduleStatus,
    ScheduleItemStatus,
    HealthCheckStatus,
    TrainingType,
    BehaviorType,
    IncidentType,
    StoolColor,
    StoolShape,
    TaskStatus,
    TaskPriority,
)

# Import models directly now that they use shared db
from k9.models.models import (
    User,
    Employee,
    Dog,
    Project,
    AuditLog,
    TrainingSession,
    VeterinaryVisit,
)

from k9.models.models_handler_daily import (
    DailySchedule,
    DailyScheduleItem,
    HandlerReport,
    HandlerReportHealth,
    HandlerReportTraining,
    HandlerReportCare,
    HandlerReportBehavior,
    HandlerReportIncident,
    HandlerReportAttachment,
    Notification,
)

__all__ = [
    # Shared db
    "db",
    
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
    "ScheduleStatus",
    "ScheduleItemStatus",
    "HealthCheckStatus",
    "TrainingType",
    "BehaviorType",
    "IncidentType",
    "StoolColor",
    "StoolShape",
    "TaskStatus",
    "TaskPriority",
    
    # Models
    "User",
    "Employee",
    "Dog",
    "Project",
    "AuditLog",
    "TrainingSession",
    "VeterinaryVisit",
    "DailySchedule",
    "DailyScheduleItem",
    "HandlerReport",
    "HandlerReportHealth",
    "HandlerReportTraining",
    "HandlerReportCare",
    "HandlerReportBehavior",
    "HandlerReportIncident",
    "HandlerReportAttachment",
    "Notification",
]
