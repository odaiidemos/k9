"""
K9 Operations Management System Pydantic Schemas
Exports all schemas for the FastAPI backend
"""

# Common and base schemas
from .common import BaseSchema, TimestampMixin, UUIDMixin

# Enums
from .enums import (
    UserRole, EmployeeRole, DogStatus, DogGender,
    TrainingCategory, SocializationType, BallWorkType,
    VisitType, ProductionCycleType, ProductionResult,
    MaturityStatus, HeatStatus, MatingResult, PregnancyStatus, DeliveryStatus,
    ProjectStatus, ElementType, PerformanceRating, TargetType,
    AuditAction, EntityType, AttendanceStatus, AbsenceReason,
    PartStatus, Severity, GroomingYesNo, GroomingCleanlinessScore,
    Route, Unit, Reaction, PrepMethod, BodyConditionScale,
    StoolColor, StoolConsistency, StoolContent, UrineColor, VomitColor, ExcretionPlace,
    PermissionType, BackupFrequency,
    ScheduleStatus, ScheduleItemStatus, ReportStatus,
    HealthCheckStatus, TrainingType, BehaviorType, IncidentType,
    StoolShape, NotificationType, TaskStatus, TaskPriority
)

# User schemas
from .user import (
    UserBase, UserCreate, UserUpdate, UserInDB, UserResponse,
    UserLogin, UserPasswordChange, UserMFASetup, UserMFAVerify
)

# Employee schemas
from .employee import (
    EmployeeBase, EmployeeCreate, EmployeeUpdate, EmployeeInDB, EmployeeResponse
)

# Dog schemas
from .dog import (
    DogBase, DogCreate, DogUpdate, DogInDB, DogResponse
)

# Project schemas
from .project import (
    ProjectBase, ProjectCreate, ProjectUpdate, ProjectInDB, ProjectResponse,
    ProjectAssignmentBase, ProjectAssignmentCreate, ProjectAssignmentUpdate,
    ProjectAssignmentInDB, ProjectAssignmentResponse,
    IncidentBase, IncidentCreate, IncidentUpdate, IncidentInDB, IncidentResponse,
    SuspicionBase, SuspicionCreate, SuspicionUpdate, SuspicionInDB, SuspicionResponse,
    PerformanceEvaluationBase, PerformanceEvaluationCreate, PerformanceEvaluationUpdate,
    PerformanceEvaluationInDB, PerformanceEvaluationResponse
)

# Training schemas
from .training import (
    TrainingSessionBase, TrainingSessionCreate, TrainingSessionUpdate,
    TrainingSessionInDB, TrainingSessionResponse,
    BreedingTrainingActivityBase, BreedingTrainingActivityCreate,
    BreedingTrainingActivityUpdate, BreedingTrainingActivityInDB,
    BreedingTrainingActivityResponse,
    PuppyTrainingBase, PuppyTrainingCreate, PuppyTrainingUpdate,
    PuppyTrainingInDB, PuppyTrainingResponse
)

# Veterinary schemas
from .veterinary import (
    VeterinaryVisitBase, VeterinaryVisitCreate, VeterinaryVisitUpdate,
    VeterinaryVisitInDB, VeterinaryVisitResponse
)

# Breeding schemas
from .breeding import (
    DogMaturityBase, DogMaturityCreate, DogMaturityUpdate, DogMaturityInDB, DogMaturityResponse,
    HeatCycleBase, HeatCycleCreate, HeatCycleUpdate, HeatCycleInDB, HeatCycleResponse,
    MatingRecordBase, MatingRecordCreate, MatingRecordUpdate, MatingRecordInDB, MatingRecordResponse,
    PregnancyRecordBase, PregnancyRecordCreate, PregnancyRecordUpdate, PregnancyRecordInDB, PregnancyRecordResponse,
    DeliveryRecordBase, DeliveryRecordCreate, DeliveryRecordUpdate, DeliveryRecordInDB, DeliveryRecordResponse,
    PuppyRecordBase, PuppyRecordCreate, PuppyRecordUpdate, PuppyRecordInDB, PuppyRecordResponse,
    ProductionCycleBase, ProductionCycleCreate, ProductionCycleUpdate, ProductionCycleInDB, ProductionCycleResponse,
    FeedingLogBase, FeedingLogCreate, FeedingLogUpdate, FeedingLogInDB, FeedingLogResponse,
    DailyCheckupLogBase, DailyCheckupLogCreate, DailyCheckupLogUpdate, DailyCheckupLogInDB, DailyCheckupLogResponse,
    ExcretionLogBase, ExcretionLogCreate, ExcretionLogUpdate, ExcretionLogInDB, ExcretionLogResponse,
    GroomingLogBase, GroomingLogCreate, GroomingLogUpdate, GroomingLogInDB, GroomingLogResponse,
    DewormingLogBase, DewormingLogCreate, DewormingLogUpdate, DewormingLogInDB, DewormingLogResponse,
    CleaningLogBase, CleaningLogCreate, CleaningLogUpdate, CleaningLogInDB, CleaningLogResponse,
    CaretakerDailyLogBase, CaretakerDailyLogCreate, CaretakerDailyLogUpdate, CaretakerDailyLogInDB, CaretakerDailyLogResponse
)

# Attendance schemas
from .attendance import (
    AttendanceRecordBase, AttendanceRecordCreate, AttendanceRecordUpdate,
    AttendanceRecordInDB, AttendanceRecordResponse,
    ProjectShiftBase, ProjectShiftCreate, ProjectShiftUpdate,
    ProjectShiftInDB, ProjectShiftResponse,
    ProjectShiftAssignmentBase, ProjectShiftAssignmentCreate, ProjectShiftAssignmentUpdate,
    ProjectShiftAssignmentInDB, ProjectShiftAssignmentResponse,
    ProjectAttendanceBase, ProjectAttendanceCreate, ProjectAttendanceUpdate,
    ProjectAttendanceInDB, ProjectAttendanceResponse,
    ShiftBase, ShiftCreate, ShiftUpdate, ShiftInDB, ShiftResponse,
    ShiftAssignmentBase, ShiftAssignmentCreate, ShiftAssignmentUpdate,
    ShiftAssignmentInDB, ShiftAssignmentResponse,
    AttendanceBase, AttendanceCreate, AttendanceUpdate, AttendanceInDB, AttendanceResponse,
    AttendanceDayBase, AttendanceDayCreate, AttendanceDayUpdate, AttendanceDayInDB, AttendanceDayResponse
)

# Handler Daily System schemas
from .handler import (
    DailyScheduleBase, DailyScheduleCreate, DailyScheduleUpdate,
    DailyScheduleInDB, DailyScheduleResponse,
    DailyScheduleItemBase, DailyScheduleItemCreate, DailyScheduleItemUpdate,
    DailyScheduleItemInDB, DailyScheduleItemResponse,
    HandlerReportBase, HandlerReportCreate, HandlerReportUpdate,
    HandlerReportInDB, HandlerReportResponse,
    HandlerReportHealthBase, HandlerReportHealthCreate, HandlerReportHealthUpdate,
    HandlerReportHealthInDB, HandlerReportHealthResponse,
    HandlerReportTrainingBase, HandlerReportTrainingCreate, HandlerReportTrainingUpdate,
    HandlerReportTrainingInDB, HandlerReportTrainingResponse,
    HandlerReportCareBase, HandlerReportCareCreate, HandlerReportCareUpdate,
    HandlerReportCareInDB, HandlerReportCareResponse,
    HandlerReportBehaviorBase, HandlerReportBehaviorCreate, HandlerReportBehaviorUpdate,
    HandlerReportBehaviorInDB, HandlerReportBehaviorResponse,
    HandlerReportIncidentBase, HandlerReportIncidentCreate, HandlerReportIncidentUpdate,
    HandlerReportIncidentInDB, HandlerReportIncidentResponse,
    HandlerReportAttachmentBase, HandlerReportAttachmentCreate,
    HandlerReportAttachmentInDB, HandlerReportAttachmentResponse,
    NotificationBase, NotificationCreate, NotificationUpdate,
    NotificationInDB, NotificationResponse,
    TaskBase, TaskCreate, TaskUpdate, TaskInDB, TaskResponse
)

# Audit and Permission schemas
from .audit import (
    AuditLogBase, AuditLogCreate, AuditLogInDB, AuditLogResponse,
    SubPermissionBase, SubPermissionCreate, SubPermissionUpdate,
    SubPermissionInDB, SubPermissionResponse,
    PermissionAuditLogBase, PermissionAuditLogCreate,
    PermissionAuditLogInDB, PermissionAuditLogResponse,
    ProjectManagerPermissionBase, ProjectManagerPermissionCreate, ProjectManagerPermissionUpdate,
    ProjectManagerPermissionInDB, ProjectManagerPermissionResponse,
    BackupSettingsBase, BackupSettingsCreate, BackupSettingsUpdate,
    BackupSettingsInDB, BackupSettingsResponse
)

__all__ = [
    # Common
    "BaseSchema", "TimestampMixin", "UUIDMixin",
    
    # Enums
    "UserRole", "EmployeeRole", "DogStatus", "DogGender",
    "TrainingCategory", "SocializationType", "BallWorkType",
    "VisitType", "ProductionCycleType", "ProductionResult",
    "MaturityStatus", "HeatStatus", "MatingResult", "PregnancyStatus", "DeliveryStatus",
    "ProjectStatus", "ElementType", "PerformanceRating", "TargetType",
    "AuditAction", "EntityType", "AttendanceStatus", "AbsenceReason",
    "PartStatus", "Severity", "GroomingYesNo", "GroomingCleanlinessScore",
    "Route", "Unit", "Reaction", "PrepMethod", "BodyConditionScale",
    "StoolColor", "StoolConsistency", "StoolContent", "UrineColor", "VomitColor", "ExcretionPlace",
    "PermissionType", "BackupFrequency",
    "ScheduleStatus", "ScheduleItemStatus", "ReportStatus",
    "HealthCheckStatus", "TrainingType", "BehaviorType", "IncidentType",
    "StoolShape", "NotificationType", "TaskStatus", "TaskPriority",
    
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserInDB", "UserResponse",
    "UserLogin", "UserPasswordChange", "UserMFASetup", "UserMFAVerify",
    
    # Employee
    "EmployeeBase", "EmployeeCreate", "EmployeeUpdate", "EmployeeInDB", "EmployeeResponse",
    
    # Dog
    "DogBase", "DogCreate", "DogUpdate", "DogInDB", "DogResponse",
    
    # Project
    "ProjectBase", "ProjectCreate", "ProjectUpdate", "ProjectInDB", "ProjectResponse",
    "ProjectAssignmentBase", "ProjectAssignmentCreate", "ProjectAssignmentUpdate",
    "ProjectAssignmentInDB", "ProjectAssignmentResponse",
    "IncidentBase", "IncidentCreate", "IncidentUpdate", "IncidentInDB", "IncidentResponse",
    "SuspicionBase", "SuspicionCreate", "SuspicionUpdate", "SuspicionInDB", "SuspicionResponse",
    "PerformanceEvaluationBase", "PerformanceEvaluationCreate", "PerformanceEvaluationUpdate",
    "PerformanceEvaluationInDB", "PerformanceEvaluationResponse",
    
    # Training
    "TrainingSessionBase", "TrainingSessionCreate", "TrainingSessionUpdate",
    "TrainingSessionInDB", "TrainingSessionResponse",
    "BreedingTrainingActivityBase", "BreedingTrainingActivityCreate",
    "BreedingTrainingActivityUpdate", "BreedingTrainingActivityInDB",
    "BreedingTrainingActivityResponse",
    "PuppyTrainingBase", "PuppyTrainingCreate", "PuppyTrainingUpdate",
    "PuppyTrainingInDB", "PuppyTrainingResponse",
    
    # Veterinary
    "VeterinaryVisitBase", "VeterinaryVisitCreate", "VeterinaryVisitUpdate",
    "VeterinaryVisitInDB", "VeterinaryVisitResponse",
    
    # Breeding
    "DogMaturityBase", "DogMaturityCreate", "DogMaturityUpdate", "DogMaturityInDB", "DogMaturityResponse",
    "HeatCycleBase", "HeatCycleCreate", "HeatCycleUpdate", "HeatCycleInDB", "HeatCycleResponse",
    "MatingRecordBase", "MatingRecordCreate", "MatingRecordUpdate", "MatingRecordInDB", "MatingRecordResponse",
    "PregnancyRecordBase", "PregnancyRecordCreate", "PregnancyRecordUpdate", "PregnancyRecordInDB", "PregnancyRecordResponse",
    "DeliveryRecordBase", "DeliveryRecordCreate", "DeliveryRecordUpdate", "DeliveryRecordInDB", "DeliveryRecordResponse",
    "PuppyRecordBase", "PuppyRecordCreate", "PuppyRecordUpdate", "PuppyRecordInDB", "PuppyRecordResponse",
    "ProductionCycleBase", "ProductionCycleCreate", "ProductionCycleUpdate", "ProductionCycleInDB", "ProductionCycleResponse",
    "FeedingLogBase", "FeedingLogCreate", "FeedingLogUpdate", "FeedingLogInDB", "FeedingLogResponse",
    "DailyCheckupLogBase", "DailyCheckupLogCreate", "DailyCheckupLogUpdate", "DailyCheckupLogInDB", "DailyCheckupLogResponse",
    "ExcretionLogBase", "ExcretionLogCreate", "ExcretionLogUpdate", "ExcretionLogInDB", "ExcretionLogResponse",
    "GroomingLogBase", "GroomingLogCreate", "GroomingLogUpdate", "GroomingLogInDB", "GroomingLogResponse",
    "DewormingLogBase", "DewormingLogCreate", "DewormingLogUpdate", "DewormingLogInDB", "DewormingLogResponse",
    "CleaningLogBase", "CleaningLogCreate", "CleaningLogUpdate", "CleaningLogInDB", "CleaningLogResponse",
    "CaretakerDailyLogBase", "CaretakerDailyLogCreate", "CaretakerDailyLogUpdate", "CaretakerDailyLogInDB", "CaretakerDailyLogResponse",
    
    # Attendance
    "AttendanceRecordBase", "AttendanceRecordCreate", "AttendanceRecordUpdate",
    "AttendanceRecordInDB", "AttendanceRecordResponse",
    "ProjectShiftBase", "ProjectShiftCreate", "ProjectShiftUpdate",
    "ProjectShiftInDB", "ProjectShiftResponse",
    "ProjectShiftAssignmentBase", "ProjectShiftAssignmentCreate", "ProjectShiftAssignmentUpdate",
    "ProjectShiftAssignmentInDB", "ProjectShiftAssignmentResponse",
    "ProjectAttendanceBase", "ProjectAttendanceCreate", "ProjectAttendanceUpdate",
    "ProjectAttendanceInDB", "ProjectAttendanceResponse",
    "ShiftBase", "ShiftCreate", "ShiftUpdate", "ShiftInDB", "ShiftResponse",
    "ShiftAssignmentBase", "ShiftAssignmentCreate", "ShiftAssignmentUpdate",
    "ShiftAssignmentInDB", "ShiftAssignmentResponse",
    "AttendanceBase", "AttendanceCreate", "AttendanceUpdate", "AttendanceInDB", "AttendanceResponse",
    "AttendanceDayBase", "AttendanceDayCreate", "AttendanceDayUpdate", "AttendanceDayInDB", "AttendanceDayResponse",
    
    # Handler Daily
    "DailyScheduleBase", "DailyScheduleCreate", "DailyScheduleUpdate",
    "DailyScheduleInDB", "DailyScheduleResponse",
    "DailyScheduleItemBase", "DailyScheduleItemCreate", "DailyScheduleItemUpdate",
    "DailyScheduleItemInDB", "DailyScheduleItemResponse",
    "HandlerReportBase", "HandlerReportCreate", "HandlerReportUpdate",
    "HandlerReportInDB", "HandlerReportResponse",
    "HandlerReportHealthBase", "HandlerReportHealthCreate", "HandlerReportHealthUpdate",
    "HandlerReportHealthInDB", "HandlerReportHealthResponse",
    "HandlerReportTrainingBase", "HandlerReportTrainingCreate", "HandlerReportTrainingUpdate",
    "HandlerReportTrainingInDB", "HandlerReportTrainingResponse",
    "HandlerReportCareBase", "HandlerReportCareCreate", "HandlerReportCareUpdate",
    "HandlerReportCareInDB", "HandlerReportCareResponse",
    "HandlerReportBehaviorBase", "HandlerReportBehaviorCreate", "HandlerReportBehaviorUpdate",
    "HandlerReportBehaviorInDB", "HandlerReportBehaviorResponse",
    "HandlerReportIncidentBase", "HandlerReportIncidentCreate", "HandlerReportIncidentUpdate",
    "HandlerReportIncidentInDB", "HandlerReportIncidentResponse",
    "HandlerReportAttachmentBase", "HandlerReportAttachmentCreate",
    "HandlerReportAttachmentInDB", "HandlerReportAttachmentResponse",
    "NotificationBase", "NotificationCreate", "NotificationUpdate",
    "NotificationInDB", "NotificationResponse",
    "TaskBase", "TaskCreate", "TaskUpdate", "TaskInDB", "TaskResponse",
    
    # Audit
    "AuditLogBase", "AuditLogCreate", "AuditLogInDB", "AuditLogResponse",
    "SubPermissionBase", "SubPermissionCreate", "SubPermissionUpdate",
    "SubPermissionInDB", "SubPermissionResponse",
    "PermissionAuditLogBase", "PermissionAuditLogCreate",
    "PermissionAuditLogInDB", "PermissionAuditLogResponse",
    "ProjectManagerPermissionBase", "ProjectManagerPermissionCreate", "ProjectManagerPermissionUpdate",
    "ProjectManagerPermissionInDB", "ProjectManagerPermissionResponse",
    "BackupSettingsBase", "BackupSettingsCreate", "BackupSettingsUpdate",
    "BackupSettingsInDB", "BackupSettingsResponse",
]
