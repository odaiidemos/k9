"""
Pydantic-compatible enums for the K9 Operations Management System
All enums from the SQLAlchemy models converted to Python enums
"""
from enum import Enum


class UserRole(str, Enum):
    GENERAL_ADMIN = "GENERAL_ADMIN"
    PROJECT_MANAGER = "PROJECT_MANAGER"
    HANDLER = "HANDLER"


class EmployeeRole(str, Enum):
    HANDLER = "سائس"
    TRAINER = "مدرب"
    BREEDER = "مربي"
    VET = "طبيب"
    PROJECT_MANAGER = "مسؤول مشروع"


class DogStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    DECEASED = "DECEASED"
    TRAINING = "TRAINING"


class DogGender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class TrainingCategory(str, Enum):
    OBEDIENCE = "طاعة"
    DETECTION = "كشف"
    AGILITY = "رشاقة"
    ATTACK = "هجوم"
    FITNESS = "لياقة"
    SOCIALIZATION = "تطبيع"
    BALL_WORK = "تدريب الكرة"
    OTHER = "أخرى"


class SocializationType(str, Enum):
    HUMAN_INTERACTION = "تفاعل مع البشر"
    ANIMAL_INTERACTION = "تفاعل مع الحيوانات"
    VEHICLE_EXPOSURE = "التعرض للمركبات"
    SOUND_DESENSITIZATION = "إزالة الحساسية للأصوات"
    ENVIRONMENT_EXPLORATION = "استكشاف البيئة"
    CROWD_INTERACTION = "تفاعل مع الحشود"


class BallWorkType(str, Enum):
    FETCH_TRAINING = "تدريب الإحضار"
    CATCH_TRAINING = "تدريب المسك"
    AGILITY_BALL = "كرة الرشاقة"
    COORDINATION_BALL = "كرة التناسق"
    REWARD_BALL = "كرة المكافأة"


class VisitType(str, Enum):
    ROUTINE = "ROUTINE"
    EMERGENCY = "EMERGENCY"
    VACCINATION = "VACCINATION"


class ProductionCycleType(str, Enum):
    NATURAL = "NATURAL"
    ARTIFICIAL = "ARTIFICIAL"


class ProductionResult(str, Enum):
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class MaturityStatus(str, Enum):
    JUVENILE = "يافع"
    MATURE = "بالغ"
    RETIRED = "متقاعد"


class HeatStatus(str, Enum):
    NOT_IN_HEAT = "لا توجد دورة"
    IN_HEAT = "في الدورة"
    POST_HEAT = "بعد الدورة"
    COMPLETED = "مكتملة"
    PRE_HEAT = "ما قبل الحرارة"


class MatingResult(str, Enum):
    SUCCESSFUL = "نجح"
    FAILED = "فشل"
    UNKNOWN = "غير معروف"


class DeliveryStatus(str, Enum):
    EXPECTED = "متوقع"
    IN_PROGRESS = "جاري"
    COMPLETED = "مكتمل"
    COMPLICATIONS = "مضاعفات"


class PregnancyStatus(str, Enum):
    NOT_PREGNANT = "غير حامل"
    PREGNANT = "حامل"
    DELIVERED = "ولدت"


class ProjectStatus(str, Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ElementType(str, Enum):
    WEAPON = "WEAPON"
    DRUG = "DRUG"
    EXPLOSIVE = "EXPLOSIVE"
    OTHER = "OTHER"


class PerformanceRating(str, Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    WEAK = "WEAK"


class TargetType(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    DOG = "DOG"


class AuditAction(str, Enum):
    CREATE = "CREATE"
    EDIT = "EDIT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    SECURITY_EVENT = "SECURITY_EVENT"


class EntityType(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    DOG = "DOG"


class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
    SICK = "SICK"
    LEAVE = "LEAVE"
    REMOTE = "REMOTE"
    OVERTIME = "OVERTIME"


class AbsenceReason(str, Enum):
    ANNUAL = "إجازة سنوية"
    SICK = "مريض"
    EMERGENCY = "حالة طارئة"
    TRAINING = "تدريب"
    MISSION = "مهمة"
    NO_REASON = "بلا سبب"
    OTHER = "أخرى"


class PartStatus(str, Enum):
    NORMAL = "سليم"
    REDNESS = "احمرار"
    INFLAMMATION = "التهاب"
    DISCHARGE = "إفرازات"
    SWELLING = "تورم"
    WOUND = "جرح"
    PAIN = "ألم"
    OTHER = "أخرى"


class Severity(str, Enum):
    MILD = "خفيف"
    MODERATE = "متوسط"
    SEVERE = "شديد"


class GroomingYesNo(str, Enum):
    YES = "YES"
    NO = "NO"


class GroomingCleanlinessScore(str, Enum):
    SCORE_1 = "1"
    SCORE_2 = "2"
    SCORE_3 = "3"
    SCORE_4 = "4"
    SCORE_5 = "5"


class Route(str, Enum):
    ORAL = "فموي"
    TOPICAL = "موضعي"
    INJECTION = "حقن"


class Unit(str, Enum):
    ML = "مل"
    MG = "ملغم"
    TABLET = "قرص"


class Reaction(str, Enum):
    NONE = "لا يوجد"
    VOMITING = "قيء"
    DIARRHEA = "إسهال"
    LETHARGY = "خمول"
    SKIN_ALLERGY = "تحسس جلدي"
    OTHER = "أخرى"


class PrepMethod(str, Enum):
    BOILED = "غليان"
    STEAMED = "تبخير"
    SOAKED = "نقع"
    OTHER = "أخرى"


class BodyConditionScale(str, Enum):
    VERY_THIN = "نحيف جدًا (1)"
    THIN = "نحيف (2)"
    BELOW_IDEAL = "أقل من المثالي (3)"
    NEAR_IDEAL = "قريب من المثالي (4)"
    IDEAL = "مثالي (5)"
    ABOVE_IDEAL = "فوق المثالي (6)"
    FULL = "ممتلئ (7)"
    OBESE = "سمين (8)"
    VERY_OBESE = "سمين جدًا (9)"


class StoolColor(str, Enum):
    شفاف_او_فاتح = "شفاف/فاتح"
    اصفر = "أصفر"
    بني = "بني"
    داكن = "داكن"
    اخضر = "أخضر"
    وردي_دموي = "وردي/دموي"
    اخرى = "أخرى"
    BROWN = "بني"
    YELLOW = "أصفر"
    GREEN = "أخضر"
    BLACK = "أسود"
    RED = "أحمر"
    WHITE = "أبيض"


class StoolConsistency(str, Enum):
    سائل = "سائل"
    لين = "لين"
    طبيعي_مشكّل = "طبيعي مُشكّل"
    صلب = "صلب"
    شديد_الصلابة = "شديد الصلابة"


class StoolContent(str, Enum):
    طبيعي = "طبيعي"
    مخاط = "مخاط"
    دم = "دم"
    طفيليات_او_ديدان = "طفيليات/ديدان"
    بقايا_طعام = "بقايا طعام"
    جسم_غريب = "جسم غريب"
    عشب = "عشب"
    اخرى = "أخرى"


class UrineColor(str, Enum):
    شفاف = "شفاف"
    اصفر_فاتح = "أصفر فاتح"
    اصفر = "أصفر"
    اصفر_غامق = "أصفر غامق"
    بني_مصفر = "بني مصفر"
    وردي_دموي = "وردي/دموي"


class VomitColor(str, Enum):
    شفاف = "شفاف"
    اصفر = "أصفر"
    بني = "بني"
    اخضر = "أخضر"
    وردي_دموي = "وردي/دموي"
    رغوي = "رغوي"
    اخرى = "أخرى"


class ExcretionPlace(str, Enum):
    داخل_البيت = "داخل البيت"
    خارج_البيت = "خارج البيت"
    القفص = "القفص"
    المكان_المخصص = "المكان المخصص"
    اخرى = "أخرى"


class PermissionType(str, Enum):
    VIEW = "VIEW"
    CREATE = "CREATE"
    EDIT = "EDIT"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    ASSIGN = "ASSIGN"
    APPROVE = "APPROVE"


class BackupFrequency(str, Enum):
    DISABLED = "DISABLED"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


class ScheduleStatus(str, Enum):
    OPEN = "OPEN"
    LOCKED = "LOCKED"


class ScheduleItemStatus(str, Enum):
    PLANNED = "PLANNED"
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    REPLACED = "REPLACED"


class ReportStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class HealthCheckStatus(str, Enum):
    NORMAL = "سليم"
    ABNORMAL = "غير طبيعي"
    NEEDS_ATTENTION = "يحتاج متابعة"


class TrainingType(str, Enum):
    FITNESS = "لياقة"
    AGILITY = "خفة الحركة"
    OBEDIENCE = "طاعة"
    BALL = "كرة"
    EXPLOSIVES = "متفجرات"
    OTHER = "أخرى"


class BehaviorType(str, Enum):
    GOOD = "جيد"
    BAD = "سيئ"


class IncidentType(str, Enum):
    SUSPICION = "اشتباه"
    DETECTION = "كشف"


class StoolShape(str, Enum):
    NORMAL = "طبيعي"
    HARD = "صلب"
    SOFT = "لين"
    LIQUID = "سائل"


class NotificationType(str, Enum):
    SCHEDULE_CREATED = "SCHEDULE_CREATED"
    EMPLOYEE_REPLACED = "EMPLOYEE_REPLACED"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    REPORT_SUBMITTED = "REPORT_SUBMITTED"
    REPORT_APPROVED = "REPORT_APPROVED"
    REPORT_REJECTED = "REPORT_REJECTED"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TaskPriority(str, Enum):
    LOW = "منخفضة"
    MEDIUM = "متوسطة"
    HIGH = "عالية"
    URGENT = "عاجلة"
