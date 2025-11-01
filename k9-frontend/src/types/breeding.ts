export enum BodyConditionScale {
  VERY_THIN = 'VERY_THIN',
  THIN = 'THIN',
  IDEAL = 'IDEAL',
  OVERWEIGHT = 'OVERWEIGHT',
  OBESE = 'OBESE'
}

export enum PrepMethod {
  RAW = 'RAW',
  COOKED = 'COOKED',
  DRY_KIBBLE = 'DRY_KIBBLE',
  WET_CANNED = 'WET_CANNED',
  MIXED = 'MIXED'
}

export enum VeterinaryVisitType {
  ROUTINE = 'ROUTINE',
  EMERGENCY = 'EMERGENCY',
  FOLLOWUP = 'FOLLOWUP',
  VACCINATION = 'VACCINATION',
  SURGERY = 'SURGERY',
  DENTAL = 'DENTAL'
}

export enum VeterinaryPriority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL'
}

export interface FeedingLog {
  id: string;
  dog_id: string;
  project_id?: string;
  date: string;
  meal_type?: string;
  food_type?: string;
  amount_kg?: number;
  prep_method?: PrepMethod;
  supplements?: string;
  body_condition?: BodyConditionScale;
  notes?: string;
  created_by_user_id: string;
  created_at: string;
}

export interface CheckupLog {
  id: string;
  dog_id: string;
  project_id?: string;
  checkup_date: string;
  weight_kg?: number;
  body_condition?: BodyConditionScale;
  temperature_c?: number;
  heart_rate?: number;
  respiratory_rate?: number;
  notes?: string;
  vet_id?: string;
  created_by_user_id: string;
  created_at: string;
}

export interface VeterinaryVisit {
  id: string;
  dog_id: string;
  vet_id?: string;
  project_id?: string;
  visit_date: string;
  visit_type: VeterinaryVisitType;
  priority?: VeterinaryPriority;
  complaint?: string;
  diagnosis?: string;
  treatment?: string;
  medications?: string;
  follow_up_date?: string;
  notes?: string;
  cost?: number;
  created_by_user_id: string;
  created_at: string;
}

export interface CaretakerDailyLog {
  id: string;
  dog_id: string;
  project_id?: string;
  date: string;
  morning_health_check?: string;
  evening_health_check?: string;
  feeding_notes?: string;
  exercise_duration_minutes?: number;
  exercise_notes?: string;
  grooming_notes?: string;
  behavioral_notes?: string;
  incidents?: string;
  caretaker_user_id: string;
  created_at: string;
}

export interface FeedingReportData {
  kpis: {
    total_dogs: number;
    total_meals: number;
    total_food_kg: number;
    avg_food_per_dog: number;
    body_condition_distribution: Record<string, number>;
  };
  rows: Array<{
    dog_name: string;
    dog_code: string;
    project_name?: string;
    meal_count: number;
    total_food_kg: number;
    avg_body_condition?: string;
    notes?: string;
  }>;
  pagination: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
}

export interface CheckupReportData {
  kpis: {
    total_dogs: number;
    total_checkups: number;
    avg_weight: number;
    avg_temperature: number;
    body_condition_distribution: Record<string, number>;
  };
  rows: Array<{
    dog_name: string;
    dog_code: string;
    project_name?: string;
    checkup_count: number;
    avg_weight?: number;
    avg_temperature?: number;
    body_condition?: string;
  }>;
  pagination: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
}

export interface VeterinaryReportData {
  kpis: {
    total_visits: number;
    total_dogs: number;
    visit_type_distribution: Record<string, number>;
    priority_distribution: Record<string, number>;
    total_cost: number;
  };
  rows: Array<{
    dog_name: string;
    dog_code: string;
    vet_name?: string;
    visit_date: string;
    visit_type: string;
    priority?: string;
    diagnosis?: string;
    cost?: number;
  }>;
  pagination: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
}

export interface CaretakerReportData {
  kpis: {
    total_dogs: number;
    total_logs: number;
    avg_exercise_minutes: number;
    dogs_with_incidents: number;
  };
  rows: Array<{
    dog_name: string;
    dog_code: string;
    project_name?: string;
    log_count: number;
    avg_exercise_minutes?: number;
    has_incidents: boolean;
    caretaker_name?: string;
  }>;
  pagination: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
}

export type RangeType = 'daily' | 'weekly' | 'monthly' | 'custom';

export interface ReportFilters {
  range_type: RangeType;
  date?: string;
  week_start?: string;
  year_month?: string;
  date_from?: string;
  date_to?: string;
  project_id?: string;
  dog_id?: string;
  page?: number;
  per_page?: number;
}

export interface PDFExportResponse {
  path: string;
  success: boolean;
}
