export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
}

export interface Dog {
  id: string;
  name: string;
  code: string;
  breed: string;
  date_of_birth: string;
  gender: string;
  status: string;
}

export interface Employee {
  id: string;
  name: string;
  code: string;
  position: string;
  department: string;
  hire_date: string;
}

export interface Project {
  id: string;
  name: string;
  code: string;
  description: string;
  start_date: string;
  end_date?: string;
  status: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface ApiError {
  detail: string;
  error: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

export * from './handler';
export * from './breeding';
