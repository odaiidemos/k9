export enum ScheduleStatus {
  OPEN = 'OPEN',
  LOCKED = 'LOCKED'
}

export enum ScheduleItemStatus {
  PLANNED = 'PLANNED',
  PRESENT = 'PRESENT',
  ABSENT = 'ABSENT',
  REPLACED = 'REPLACED'
}

export enum ReportStatus {
  DRAFT = 'DRAFT',
  SUBMITTED = 'SUBMITTED',
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED'
}

export enum HealthCheckStatus {
  NORMAL = 'NORMAL',
  ABNORMAL = 'ABNORMAL',
  REQUIRES_ATTENTION = 'REQUIRES_ATTENTION'
}

export enum TrainingType {
  OBEDIENCE = 'OBEDIENCE',
  DETECTION = 'DETECTION',
  TRACKING = 'TRACKING',
  PROTECTION = 'PROTECTION',
  AGILITY = 'AGILITY',
  OTHER = 'OTHER'
}

export enum StoolColor {
  BROWN = 'BROWN',
  GREEN = 'GREEN',
  YELLOW = 'YELLOW',
  BLACK = 'BLACK',
  RED = 'RED',
  WHITE = 'WHITE'
}

export enum StoolShape {
  NORMAL = 'NORMAL',
  SOFT = 'SOFT',
  HARD = 'HARD',
  LIQUID = 'LIQUID'
}

export enum IncidentType {
  INJURY = 'INJURY',
  ILLNESS = 'ILLNESS',
  BEHAVIORAL = 'BEHAVIORAL',
  EQUIPMENT_DAMAGE = 'EQUIPMENT_DAMAGE',
  ESCAPE_ATTEMPT = 'ESCAPE_ATTEMPT',
  AGGRESSION = 'AGGRESSION',
  OTHER = 'OTHER'
}

export enum NotificationType {
  SCHEDULE_CREATED = 'SCHEDULE_CREATED',
  SCHEDULE_UPDATED = 'SCHEDULE_UPDATED',
  SCHEDULE_LOCKED = 'SCHEDULE_LOCKED',
  REPORT_SUBMITTED = 'REPORT_SUBMITTED',
  REPORT_APPROVED = 'REPORT_APPROVED',
  REPORT_REJECTED = 'REPORT_REJECTED',
  TASK_ASSIGNED = 'TASK_ASSIGNED',
  GENERAL = 'GENERAL'
}

export interface DailySchedule {
  id: string;
  date: string;
  project_id?: string;
  status: ScheduleStatus;
  notes?: string;
  created_by_user_id: string;
  created_at: string;
}

export interface DailyScheduleItem {
  id: string;
  daily_schedule_id: string;
  handler_user_id: string;
  dog_id?: string;
  shift_id?: string;
  status: ScheduleItemStatus;
  replacement_handler_id?: string;
  absence_reason?: string;
  replacement_notes?: string;
  created_at: string;
}

export interface HandlerReport {
  id: string;
  date: string;
  schedule_item_id?: string;
  handler_user_id: string;
  dog_id: string;
  project_id?: string;
  location?: string;
  status: ReportStatus;
  created_at: string;
  submitted_at?: string;
  reviewed_by_user_id?: string;
  reviewed_at?: string;
}

export interface HandlerReportHealth {
  id: string;
  report_id: string;
  eyes_status?: HealthCheckStatus;
  eyes_notes?: string;
  nose_status?: HealthCheckStatus;
  nose_notes?: string;
  ears_status?: HealthCheckStatus;
  ears_notes?: string;
  mouth_status?: HealthCheckStatus;
  mouth_notes?: string;
  teeth_status?: HealthCheckStatus;
  teeth_notes?: string;
  gums_status?: HealthCheckStatus;
  gums_notes?: string;
  front_limbs_status?: HealthCheckStatus;
  front_limbs_notes?: string;
  back_limbs_status?: HealthCheckStatus;
  back_limbs_notes?: string;
  hair_status?: HealthCheckStatus;
  hair_notes?: string;
  tail_status?: HealthCheckStatus;
  tail_notes?: string;
  rear_status?: HealthCheckStatus;
  rear_notes?: string;
}

export interface HandlerReportTraining {
  id: string;
  report_id: string;
  training_type: TrainingType;
  description?: string;
  time_from?: string;
  time_to?: string;
  notes?: string;
}

export interface HandlerReportCare {
  id: string;
  report_id: string;
  food_amount?: string;
  food_type?: string;
  supplements?: string;
  water_amount?: string;
  grooming_done: boolean;
  washing_done: boolean;
  excretion_location?: string;
  stool_color?: StoolColor;
  stool_shape?: StoolShape;
}

export interface HandlerReportBehavior {
  id: string;
  report_id: string;
  good_behavior_notes?: string;
  bad_behavior_notes?: string;
}

export interface HandlerReportIncident {
  id: string;
  report_id: string;
  incident_type: IncidentType;
  description: string;
  incident_datetime?: string;
  location?: string;
}

export interface Notification {
  id: string;
  user_id: string;
  type: NotificationType;
  title: string;
  message: string;
  related_id?: string;
  related_type?: string;
  read: boolean;
  read_at?: string;
  created_at: string;
}

export interface DailyScheduleCreateRequest {
  date: string;
  project_id?: string;
  notes?: string;
  created_by_user_id: string;
}

export interface DailyScheduleItemCreateRequest {
  daily_schedule_id: string;
  handler_user_id: string;
  dog_id?: string;
  shift_id?: string;
}

export interface HandlerReportCreateRequest {
  date: string;
  schedule_item_id?: string;
  handler_user_id: string;
  dog_id: string;
  project_id?: string;
  location?: string;
}

export interface HandlerReportUpdateRequest {
  location?: string;
  status?: ReportStatus;
  review_notes?: string;
}
