export enum TrainingSessionType {
  OBEDIENCE = 'OBEDIENCE',
  DETECTION = 'DETECTION',
  TRACKING = 'TRACKING',
  PROTECTION = 'PROTECTION',
  AGILITY = 'AGILITY',
  SOCIALIZATION = 'SOCIALIZATION',
  OTHER = 'OTHER'
}

export enum TrainingStatus {
  SCHEDULED = 'SCHEDULED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED'
}

export enum PerformanceRating {
  EXCELLENT = 'EXCELLENT',
  GOOD = 'GOOD',
  AVERAGE = 'AVERAGE',
  BELOW_AVERAGE = 'BELOW_AVERAGE',
  POOR = 'POOR'
}

export interface TrainingSession {
  id: string;
  dog_id: string;
  trainer_user_id: string;
  project_id?: string;
  session_date: string;
  session_type: TrainingSessionType;
  duration_minutes?: number;
  location?: string;
  objectives?: string;
  activities?: string;
  performance_rating?: PerformanceRating;
  notes?: string;
  status: TrainingStatus;
  created_by_user_id: string;
  created_at: string;
}

export interface TrainingReportData {
  kpis: {
    total_sessions: number;
    total_dogs: number;
    total_hours: number;
    avg_duration_minutes: number;
    session_type_distribution: Record<string, number>;
    performance_distribution: Record<string, number>;
  };
  rows: Array<{
    dog_name: string;
    dog_code: string;
    trainer_name?: string;
    session_date: string;
    session_type: string;
    duration_minutes?: number;
    performance_rating?: string;
    status: string;
  }>;
  pagination: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
}

export interface TrainingFilters {
  range_type: 'daily' | 'weekly' | 'monthly' | 'custom';
  date?: string;
  week_start?: string;
  year_month?: string;
  date_from?: string;
  date_to?: string;
  project_id?: string;
  dog_id?: string;
  trainer_id?: string;
  session_type?: string;
  page?: number;
  per_page?: number;
}

export interface PDFExportResponse {
  path: string;
  success: boolean;
}
