"""
Breeding Pydantic schemas for the K9 Operations Management System
Includes all breeding, production, and care-related schemas
"""
from pydantic import Field
from typing import Optional, List
from datetime import datetime, date, time
from uuid import UUID

from .enums import (
    MaturityStatus, HeatStatus, MatingResult, PregnancyStatus, DeliveryStatus,
    DogGender, ProductionCycleType, ProductionResult,
    PrepMethod, BodyConditionScale, PartStatus, Severity,
    GroomingYesNo, GroomingCleanlinessScore, Route, Unit, Reaction,
    StoolColor, StoolConsistency, StoolContent, UrineColor, VomitColor, ExcretionPlace
)
from .common import BaseSchema, UUIDMixin, TimestampMixin


class DogMaturityBase(BaseSchema):
    """Base DogMaturity schema"""
    dog_id: UUID
    maturity_date: Optional[date] = None
    maturity_status: MaturityStatus = MaturityStatus.JUVENILE
    weight_at_maturity: Optional[float] = Field(None, gt=0)
    height_at_maturity: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None


class DogMaturityCreate(DogMaturityBase):
    """Schema for creating a dog maturity record"""
    pass


class DogMaturityUpdate(BaseSchema):
    """Schema for updating a dog maturity record"""
    maturity_date: Optional[date] = None
    maturity_status: Optional[MaturityStatus] = None
    weight_at_maturity: Optional[float] = Field(None, gt=0)
    height_at_maturity: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None


class DogMaturityInDB(DogMaturityBase, UUIDMixin, TimestampMixin):
    """Schema representing DogMaturity in database"""
    pass


class DogMaturityResponse(DogMaturityBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class HeatCycleBase(BaseSchema):
    """Base HeatCycle schema"""
    dog_id: UUID
    cycle_number: int = Field(..., gt=0)
    start_date: date
    end_date: Optional[date] = None
    duration_days: Optional[int] = Field(None, ge=0)
    status: HeatStatus = HeatStatus.IN_HEAT
    behavioral_changes: Optional[str] = None
    physical_signs: Optional[str] = None
    appetite_changes: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class HeatCycleCreate(HeatCycleBase):
    """Schema for creating a heat cycle"""
    pass


class HeatCycleUpdate(BaseSchema):
    """Schema for updating a heat cycle"""
    cycle_number: Optional[int] = Field(None, gt=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_days: Optional[int] = Field(None, ge=0)
    status: Optional[HeatStatus] = None
    behavioral_changes: Optional[str] = None
    physical_signs: Optional[str] = None
    appetite_changes: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class HeatCycleInDB(HeatCycleBase, UUIDMixin, TimestampMixin):
    """Schema representing HeatCycle in database"""
    pass


class HeatCycleResponse(HeatCycleBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class MatingRecordBase(BaseSchema):
    """Base MatingRecord schema"""
    female_id: UUID
    male_id: UUID
    heat_cycle_id: Optional[UUID] = None
    mating_date: date
    mating_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=100)
    supervised_by: Optional[UUID] = None
    success_rate: Optional[int] = Field(None, ge=0, le=10)
    duration_minutes: Optional[int] = Field(None, ge=0)
    behavior_observed: Optional[str] = None
    complications: Optional[str] = None
    notes: Optional[str] = None


class MatingRecordCreate(MatingRecordBase):
    """Schema for creating a mating record"""
    pass


class MatingRecordUpdate(BaseSchema):
    """Schema for updating a mating record"""
    heat_cycle_id: Optional[UUID] = None
    mating_date: Optional[date] = None
    mating_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=100)
    supervised_by: Optional[UUID] = None
    success_rate: Optional[int] = Field(None, ge=0, le=10)
    duration_minutes: Optional[int] = Field(None, ge=0)
    behavior_observed: Optional[str] = None
    complications: Optional[str] = None
    notes: Optional[str] = None


class MatingRecordInDB(MatingRecordBase, UUIDMixin):
    """Schema representing MatingRecord in database"""
    created_at: datetime


class MatingRecordResponse(MatingRecordBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class PregnancyRecordBase(BaseSchema):
    """Base PregnancyRecord schema"""
    mating_record_id: UUID
    dog_id: UUID
    confirmed_date: Optional[date] = None
    expected_delivery_date: Optional[date] = None
    status: PregnancyStatus = PregnancyStatus.NOT_PREGNANT
    week_1_checkup: dict = Field(default_factory=dict)
    week_2_checkup: dict = Field(default_factory=dict)
    week_3_checkup: dict = Field(default_factory=dict)
    week_4_checkup: dict = Field(default_factory=dict)
    week_5_checkup: dict = Field(default_factory=dict)
    week_6_checkup: dict = Field(default_factory=dict)
    week_7_checkup: dict = Field(default_factory=dict)
    week_8_checkup: dict = Field(default_factory=dict)
    ultrasound_results: List[dict] = Field(default_factory=list)
    special_diet: Optional[str] = None
    exercise_restrictions: Optional[str] = None
    medications: List[dict] = Field(default_factory=list)
    notes: Optional[str] = None


class PregnancyRecordCreate(PregnancyRecordBase):
    """Schema for creating a pregnancy record"""
    pass


class PregnancyRecordUpdate(BaseSchema):
    """Schema for updating a pregnancy record"""
    confirmed_date: Optional[date] = None
    expected_delivery_date: Optional[date] = None
    status: Optional[PregnancyStatus] = None
    week_1_checkup: Optional[dict] = None
    week_2_checkup: Optional[dict] = None
    week_3_checkup: Optional[dict] = None
    week_4_checkup: Optional[dict] = None
    week_5_checkup: Optional[dict] = None
    week_6_checkup: Optional[dict] = None
    week_7_checkup: Optional[dict] = None
    week_8_checkup: Optional[dict] = None
    ultrasound_results: Optional[List[dict]] = None
    special_diet: Optional[str] = None
    exercise_restrictions: Optional[str] = None
    medications: Optional[List[dict]] = None
    notes: Optional[str] = None


class PregnancyRecordInDB(PregnancyRecordBase, UUIDMixin, TimestampMixin):
    """Schema representing PregnancyRecord in database"""
    pass


class PregnancyRecordResponse(PregnancyRecordBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class DeliveryRecordBase(BaseSchema):
    """Base DeliveryRecord schema"""
    pregnancy_record_id: UUID
    delivery_date: date
    delivery_start_time: Optional[time] = None
    delivery_end_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=100)
    vet_present: Optional[UUID] = None
    handler_present: Optional[UUID] = None
    assistance_required: bool = False
    assistance_type: Optional[str] = None
    total_puppies: int = Field(default=0, ge=0)
    live_births: int = Field(default=0, ge=0)
    stillbirths: int = Field(default=0, ge=0)
    delivery_complications: Optional[str] = None
    mother_condition: Optional[str] = None
    notes: Optional[str] = None


class DeliveryRecordCreate(DeliveryRecordBase):
    """Schema for creating a delivery record"""
    pass


class DeliveryRecordUpdate(BaseSchema):
    """Schema for updating a delivery record"""
    delivery_date: Optional[date] = None
    delivery_start_time: Optional[time] = None
    delivery_end_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=100)
    vet_present: Optional[UUID] = None
    handler_present: Optional[UUID] = None
    assistance_required: Optional[bool] = None
    assistance_type: Optional[str] = None
    total_puppies: Optional[int] = Field(None, ge=0)
    live_births: Optional[int] = Field(None, ge=0)
    stillbirths: Optional[int] = Field(None, ge=0)
    delivery_complications: Optional[str] = None
    mother_condition: Optional[str] = None
    notes: Optional[str] = None


class DeliveryRecordInDB(DeliveryRecordBase, UUIDMixin):
    """Schema representing DeliveryRecord in database"""
    created_at: datetime


class DeliveryRecordResponse(DeliveryRecordBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class PuppyRecordBase(BaseSchema):
    """Base PuppyRecord schema"""
    delivery_record_id: UUID
    puppy_number: int = Field(..., gt=0)
    name: Optional[str] = Field(None, max_length=100)
    temporary_id: Optional[str] = Field(None, max_length=20)
    gender: DogGender
    birth_weight: Optional[float] = Field(None, gt=0)
    birth_time: Optional[time] = None
    birth_order: Optional[int] = Field(None, gt=0)
    alive_at_birth: bool = True
    current_status: str = Field(default="صحي ونشط", max_length=50)
    color: Optional[str] = Field(None, max_length=50)
    markings: Optional[str] = None
    birth_defects: Optional[str] = None
    week_1_weight: Optional[float] = Field(None, gt=0)
    week_2_weight: Optional[float] = Field(None, gt=0)
    week_3_weight: Optional[float] = Field(None, gt=0)
    week_4_weight: Optional[float] = Field(None, gt=0)
    week_5_weight: Optional[float] = Field(None, gt=0)
    week_6_weight: Optional[float] = Field(None, gt=0)
    week_7_weight: Optional[float] = Field(None, gt=0)
    week_8_weight: Optional[float] = Field(None, gt=0)
    weaning_date: Optional[date] = None
    placement_date: Optional[date] = None
    placement_location: Optional[str] = Field(None, max_length=100)
    adult_dog_id: Optional[UUID] = None
    notes: Optional[str] = None


class PuppyRecordCreate(PuppyRecordBase):
    """Schema for creating a puppy record"""
    pass


class PuppyRecordUpdate(BaseSchema):
    """Schema for updating a puppy record"""
    name: Optional[str] = Field(None, max_length=100)
    temporary_id: Optional[str] = Field(None, max_length=20)
    birth_weight: Optional[float] = Field(None, gt=0)
    current_status: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=50)
    markings: Optional[str] = None
    birth_defects: Optional[str] = None
    week_1_weight: Optional[float] = Field(None, gt=0)
    week_2_weight: Optional[float] = Field(None, gt=0)
    week_3_weight: Optional[float] = Field(None, gt=0)
    week_4_weight: Optional[float] = Field(None, gt=0)
    week_5_weight: Optional[float] = Field(None, gt=0)
    week_6_weight: Optional[float] = Field(None, gt=0)
    week_7_weight: Optional[float] = Field(None, gt=0)
    week_8_weight: Optional[float] = Field(None, gt=0)
    weaning_date: Optional[date] = None
    placement_date: Optional[date] = None
    placement_location: Optional[str] = Field(None, max_length=100)
    adult_dog_id: Optional[UUID] = None
    notes: Optional[str] = None


class PuppyRecordInDB(PuppyRecordBase, UUIDMixin, TimestampMixin):
    """Schema representing PuppyRecord in database"""
    pass


class PuppyRecordResponse(PuppyRecordBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class ProductionCycleBase(BaseSchema):
    """Base ProductionCycle schema"""
    female_id: UUID
    male_id: UUID
    cycle_type: ProductionCycleType
    heat_start_date: Optional[date] = None
    mating_date: date
    expected_delivery_date: Optional[date] = None
    actual_delivery_date: Optional[date] = None
    result: ProductionResult = ProductionResult.UNKNOWN
    number_of_puppies: int = Field(default=0, ge=0)
    puppies_survived: int = Field(default=0, ge=0)
    puppies_info: List[dict] = Field(default_factory=list)
    prenatal_care: Optional[str] = None
    delivery_notes: Optional[str] = None
    complications: Optional[str] = None


class ProductionCycleCreate(ProductionCycleBase):
    """Schema for creating a production cycle"""
    pass


class ProductionCycleUpdate(BaseSchema):
    """Schema for updating a production cycle"""
    cycle_type: Optional[ProductionCycleType] = None
    heat_start_date: Optional[date] = None
    mating_date: Optional[date] = None
    expected_delivery_date: Optional[date] = None
    actual_delivery_date: Optional[date] = None
    result: Optional[ProductionResult] = None
    number_of_puppies: Optional[int] = Field(None, ge=0)
    puppies_survived: Optional[int] = Field(None, ge=0)
    puppies_info: Optional[List[dict]] = None
    prenatal_care: Optional[str] = None
    delivery_notes: Optional[str] = None
    complications: Optional[str] = None


class ProductionCycleInDB(ProductionCycleBase, UUIDMixin, TimestampMixin):
    """Schema representing ProductionCycle in database"""
    pass


class ProductionCycleResponse(ProductionCycleBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class FeedingLogBase(BaseSchema):
    """Base FeedingLog schema"""
    project_id: Optional[UUID] = None
    date: date
    time: time
    dog_id: UUID
    recorder_employee_id: Optional[UUID] = None
    meal_type_fresh: bool = False
    meal_type_dry: bool = False
    meal_name: Optional[str] = Field(None, max_length=120)
    prep_method: Optional[PrepMethod] = None
    grams: Optional[int] = Field(None, ge=0)
    water_ml: Optional[int] = Field(None, ge=0)
    supplements: List[dict] = Field(default_factory=list)
    body_condition: Optional[BodyConditionScale] = None
    notes: Optional[str] = None


class FeedingLogCreate(FeedingLogBase):
    """Schema for creating a feeding log"""
    pass


class FeedingLogUpdate(BaseSchema):
    """Schema for updating a feeding log"""
    date: Optional[date] = None
    time: Optional[time] = None
    meal_type_fresh: Optional[bool] = None
    meal_type_dry: Optional[bool] = None
    meal_name: Optional[str] = Field(None, max_length=120)
    prep_method: Optional[PrepMethod] = None
    grams: Optional[int] = Field(None, ge=0)
    water_ml: Optional[int] = Field(None, ge=0)
    supplements: Optional[List[dict]] = None
    body_condition: Optional[BodyConditionScale] = None
    notes: Optional[str] = None


class FeedingLogInDB(FeedingLogBase, UUIDMixin, TimestampMixin):
    """Schema representing FeedingLog in database"""
    created_by_user_id: Optional[UUID] = None


class FeedingLogResponse(FeedingLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class DailyCheckupLogBase(BaseSchema):
    """Base DailyCheckupLog schema"""
    project_id: Optional[UUID] = None
    date: date
    time: time
    dog_id: UUID
    examiner_employee_id: Optional[UUID] = None
    eyes: Optional[str] = Field(None, max_length=50)
    ears: Optional[str] = Field(None, max_length=50)
    nose: Optional[str] = Field(None, max_length=50)
    front_legs: Optional[str] = Field(None, max_length=50)
    hind_legs: Optional[str] = Field(None, max_length=50)
    coat: Optional[str] = Field(None, max_length=50)
    tail: Optional[str] = Field(None, max_length=50)
    severity: Optional[str] = Field(None, max_length=50)
    symptoms: Optional[str] = None
    initial_diagnosis: Optional[str] = None
    suggested_treatment: Optional[str] = None
    notes: Optional[str] = None


class DailyCheckupLogCreate(DailyCheckupLogBase):
    """Schema for creating a daily checkup log"""
    pass


class DailyCheckupLogUpdate(BaseSchema):
    """Schema for updating a daily checkup log"""
    date: Optional[date] = None
    time: Optional[time] = None
    eyes: Optional[str] = Field(None, max_length=50)
    ears: Optional[str] = Field(None, max_length=50)
    nose: Optional[str] = Field(None, max_length=50)
    front_legs: Optional[str] = Field(None, max_length=50)
    hind_legs: Optional[str] = Field(None, max_length=50)
    coat: Optional[str] = Field(None, max_length=50)
    tail: Optional[str] = Field(None, max_length=50)
    severity: Optional[str] = Field(None, max_length=50)
    symptoms: Optional[str] = None
    initial_diagnosis: Optional[str] = None
    suggested_treatment: Optional[str] = None
    notes: Optional[str] = None


class DailyCheckupLogInDB(DailyCheckupLogBase, UUIDMixin, TimestampMixin):
    """Schema representing DailyCheckupLog in database"""
    created_by_user_id: Optional[UUID] = None


class DailyCheckupLogResponse(DailyCheckupLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class ExcretionLogBase(BaseSchema):
    """Base ExcretionLog schema"""
    project_id: Optional[UUID] = None
    date: date
    time: time
    dog_id: UUID
    recorder_employee_id: Optional[UUID] = None
    stool_color: Optional[str] = Field(None, max_length=50)
    stool_consistency: Optional[str] = Field(None, max_length=50)
    stool_content: Optional[str] = Field(None, max_length=50)
    constipation: bool = False
    stool_place: Optional[str] = Field(None, max_length=50)
    stool_notes: Optional[str] = None
    urine_color: Optional[str] = Field(None, max_length=50)
    urine_notes: Optional[str] = None
    vomit_color: Optional[str] = Field(None, max_length=50)
    vomit_count: Optional[int] = Field(None, ge=0)
    vomit_notes: Optional[str] = None


class ExcretionLogCreate(ExcretionLogBase):
    """Schema for creating an excretion log"""
    pass


class ExcretionLogUpdate(BaseSchema):
    """Schema for updating an excretion log"""
    date: Optional[date] = None
    time: Optional[time] = None
    stool_color: Optional[str] = Field(None, max_length=50)
    stool_consistency: Optional[str] = Field(None, max_length=50)
    stool_content: Optional[str] = Field(None, max_length=50)
    constipation: Optional[bool] = None
    stool_place: Optional[str] = Field(None, max_length=50)
    stool_notes: Optional[str] = None
    urine_color: Optional[str] = Field(None, max_length=50)
    urine_notes: Optional[str] = None
    vomit_color: Optional[str] = Field(None, max_length=50)
    vomit_count: Optional[int] = Field(None, ge=0)
    vomit_notes: Optional[str] = None


class ExcretionLogInDB(ExcretionLogBase, UUIDMixin, TimestampMixin):
    """Schema representing ExcretionLog in database"""
    created_by_user_id: Optional[UUID] = None


class ExcretionLogResponse(ExcretionLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class GroomingLogBase(BaseSchema):
    """Base GroomingLog schema"""
    project_id: Optional[UUID] = None
    date: date
    time: time
    dog_id: UUID
    recorder_employee_id: Optional[UUID] = None
    washed_bathed: Optional[GroomingYesNo] = None
    shampoo_type: Optional[str] = Field(None, max_length=120)
    brushing: Optional[GroomingYesNo] = None
    nail_trimming: Optional[GroomingYesNo] = None
    teeth_brushing: Optional[GroomingYesNo] = None
    ear_cleaning: Optional[GroomingYesNo] = None
    eye_cleaning: Optional[GroomingYesNo] = None
    cleanliness_score: Optional[GroomingCleanlinessScore] = None
    notes: Optional[str] = None


class GroomingLogCreate(GroomingLogBase):
    """Schema for creating a grooming log"""
    pass


class GroomingLogUpdate(BaseSchema):
    """Schema for updating a grooming log"""
    date: Optional[date] = None
    time: Optional[time] = None
    washed_bathed: Optional[GroomingYesNo] = None
    shampoo_type: Optional[str] = Field(None, max_length=120)
    brushing: Optional[GroomingYesNo] = None
    nail_trimming: Optional[GroomingYesNo] = None
    teeth_brushing: Optional[GroomingYesNo] = None
    ear_cleaning: Optional[GroomingYesNo] = None
    eye_cleaning: Optional[GroomingYesNo] = None
    cleanliness_score: Optional[GroomingCleanlinessScore] = None
    notes: Optional[str] = None


class GroomingLogInDB(GroomingLogBase, UUIDMixin, TimestampMixin):
    """Schema representing GroomingLog in database"""
    created_by_user_id: Optional[UUID] = None


class GroomingLogResponse(GroomingLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class DewormingLogBase(BaseSchema):
    """Base DewormingLog schema"""
    project_id: Optional[UUID] = None
    date: date
    time: time
    dog_id: UUID
    specialist_employee_id: Optional[UUID] = None
    dog_weight_kg: Optional[float] = Field(None, gt=0)
    product_name: Optional[str] = Field(None, max_length=120)
    active_ingredient: Optional[str] = Field(None, max_length=120)
    standard_dose_mg_per_kg: Optional[float] = Field(None, gt=0)
    calculated_dose_mg: Optional[float] = Field(None, gt=0)
    administered_amount: Optional[float] = Field(None, gt=0)
    amount_unit: Optional[str] = Field(None, max_length=20)
    administration_route: Optional[str] = Field(None, max_length=20)
    batch_number: Optional[str] = Field(None, max_length=60)
    expiry_date: Optional[date] = None
    adverse_reaction: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    next_due_date: Optional[date] = None


class DewormingLogCreate(DewormingLogBase):
    """Schema for creating a deworming log"""
    pass


class DewormingLogUpdate(BaseSchema):
    """Schema for updating a deworming log"""
    date: Optional[date] = None
    time: Optional[time] = None
    dog_weight_kg: Optional[float] = Field(None, gt=0)
    product_name: Optional[str] = Field(None, max_length=120)
    active_ingredient: Optional[str] = Field(None, max_length=120)
    standard_dose_mg_per_kg: Optional[float] = Field(None, gt=0)
    calculated_dose_mg: Optional[float] = Field(None, gt=0)
    administered_amount: Optional[float] = Field(None, gt=0)
    amount_unit: Optional[str] = Field(None, max_length=20)
    administration_route: Optional[str] = Field(None, max_length=20)
    batch_number: Optional[str] = Field(None, max_length=60)
    expiry_date: Optional[date] = None
    adverse_reaction: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    next_due_date: Optional[date] = None


class DewormingLogInDB(DewormingLogBase, UUIDMixin, TimestampMixin):
    """Schema representing DewormingLog in database"""
    created_by_user_id: Optional[UUID] = None


class DewormingLogResponse(DewormingLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class CleaningLogBase(BaseSchema):
    """Base CleaningLog schema"""
    project_id: UUID
    date: date
    time: time
    dog_id: UUID
    recorder_employee_id: Optional[UUID] = None
    area_type: Optional[str] = Field(None, max_length=50)
    cage_house_number: Optional[str] = Field(None, max_length=60)
    alternate_place: Optional[str] = Field(None, max_length=120)
    cleaned_house: Optional[str] = Field(None, max_length=10)
    washed_house: Optional[str] = Field(None, max_length=10)
    disinfected_house: Optional[str] = Field(None, max_length=10)
    group_disinfection: Optional[str] = Field(None, max_length=10)
    group_description: Optional[str] = Field(None, max_length=120)
    materials_used: List[dict] = Field(default_factory=list)
    notes: Optional[str] = None


class CleaningLogCreate(CleaningLogBase):
    """Schema for creating a cleaning log"""
    pass


class CleaningLogUpdate(BaseSchema):
    """Schema for updating a cleaning log"""
    date: Optional[date] = None
    time: Optional[time] = None
    area_type: Optional[str] = Field(None, max_length=50)
    cage_house_number: Optional[str] = Field(None, max_length=60)
    alternate_place: Optional[str] = Field(None, max_length=120)
    cleaned_house: Optional[str] = Field(None, max_length=10)
    washed_house: Optional[str] = Field(None, max_length=10)
    disinfected_house: Optional[str] = Field(None, max_length=10)
    group_disinfection: Optional[str] = Field(None, max_length=10)
    group_description: Optional[str] = Field(None, max_length=120)
    materials_used: Optional[List[dict]] = None
    notes: Optional[str] = None


class CleaningLogInDB(CleaningLogBase, UUIDMixin, TimestampMixin):
    """Schema representing CleaningLog in database"""
    created_by_user_id: Optional[UUID] = None


class CleaningLogResponse(CleaningLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime


class CaretakerDailyLogBase(BaseSchema):
    """Base CaretakerDailyLog schema"""
    date: date
    project_id: Optional[UUID] = None
    dog_id: UUID
    caretaker_employee_id: Optional[UUID] = None
    kennel_code: Optional[str] = Field(None, max_length=50)
    house_clean: bool = False
    house_vacuum: bool = False
    house_tap_clean: bool = False
    house_drain_clean: bool = False
    dog_clean: bool = False
    dog_washed: bool = False
    dog_brushed: bool = False
    bowls_bucket_clean: bool = False
    notes: Optional[str] = None


class CaretakerDailyLogCreate(CaretakerDailyLogBase):
    """Schema for creating a caretaker daily log"""
    pass


class CaretakerDailyLogUpdate(BaseSchema):
    """Schema for updating a caretaker daily log"""
    kennel_code: Optional[str] = Field(None, max_length=50)
    house_clean: Optional[bool] = None
    house_vacuum: Optional[bool] = None
    house_tap_clean: Optional[bool] = None
    house_drain_clean: Optional[bool] = None
    dog_clean: Optional[bool] = None
    dog_washed: Optional[bool] = None
    dog_brushed: Optional[bool] = None
    bowls_bucket_clean: Optional[bool] = None
    notes: Optional[str] = None


class CaretakerDailyLogInDB(CaretakerDailyLogBase, UUIDMixin, TimestampMixin):
    """Schema representing CaretakerDailyLog in database"""
    created_by_user_id: Optional[UUID] = None


class CaretakerDailyLogResponse(CaretakerDailyLogBase, UUIDMixin):
    """Schema for API responses"""
    created_at: datetime
