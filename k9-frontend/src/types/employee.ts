export const EmployeeRole = {
  HANDLER: 'سائس',
  TRAINER: 'مدرب',
  BREEDER: 'مربي',
  VET: 'طبيب',
  PROJECT_MANAGER: 'مسؤول مشروع',
} as const;

export type EmployeeRole = typeof EmployeeRole[keyof typeof EmployeeRole];

export interface Employee {
  id: string;
  name: string;
  employee_id: string;
  role: EmployeeRole;
  phone?: string;
  email?: string;
  hire_date: string;
  is_active: boolean;
  certifications: Record<string, any>[];
  created_at: string;
  updated_at?: string;
  assigned_to_user_id?: string;
  user_account_id?: string;
}

export interface EmployeeCreate {
  name: string;
  employee_id: string;
  role: EmployeeRole;
  phone?: string;
  email?: string;
  hire_date: string;
  certifications?: Record<string, any>[];
  assigned_to_user_id?: string;
  user_account_id?: string;
}

export interface EmployeeUpdate {
  name?: string;
  employee_id?: string;
  role?: EmployeeRole;
  phone?: string;
  email?: string;
  hire_date?: string;
  is_active?: boolean;
  certifications?: Record<string, any>[];
  assigned_to_user_id?: string;
  user_account_id?: string;
}

export interface EmployeeFilters {
  skip?: number;
  limit?: number;
  role?: EmployeeRole;
  is_active?: boolean;
  search?: string;
}

export interface EmployeeStats {
  total: number;
  active: number;
  inactive: number;
  by_role: Record<string, number>;
}
