export const ProjectStatus = {
  PLANNED: 'PLANNED',
  ACTIVE: 'ACTIVE',
  COMPLETED: 'COMPLETED',
  ON_HOLD: 'ON_HOLD',
  CANCELLED: 'CANCELLED',
} as const;

export type ProjectStatus = typeof ProjectStatus[keyof typeof ProjectStatus];

export interface Project {
  id: string;
  name: string;
  code: string;
  main_task?: string;
  description?: string;
  status: ProjectStatus;
  start_date: string;
  end_date?: string;
  expected_completion_date?: string;
  location?: string;
  mission_type?: string;
  priority: string;
  duration_days?: number;
  created_at: string;
  updated_at?: string;
  manager_id?: string;
  project_manager_id?: string;
  success_rating?: number;
}

export interface ProjectCreate {
  name: string;
  code: string;
  main_task?: string;
  description?: string;
  status?: ProjectStatus;
  start_date: string;
  end_date?: string;
  expected_completion_date?: string;
  location?: string;
  mission_type?: string;
  priority?: string;
  manager_id?: string;
  project_manager_id?: string;
  success_rating?: number;
  final_report?: string;
  lessons_learned?: string;
}

export interface ProjectUpdate {
  name?: string;
  code?: string;
  main_task?: string;
  description?: string;
  status?: ProjectStatus;
  start_date?: string;
  end_date?: string;
  expected_completion_date?: string;
  location?: string;
  mission_type?: string;
  priority?: string;
  manager_id?: string;
  project_manager_id?: string;
  success_rating?: number;
  final_report?: string;
  lessons_learned?: string;
}

export interface ProjectFilters {
  skip?: number;
  limit?: number;
  status?: ProjectStatus;
  priority?: string;
  search?: string;
}

export interface ProjectStats {
  total: number;
  by_status: Record<string, number>;
  by_priority: Record<string, number>;
  average_success_rating: number;
  completed_projects: number;
}
