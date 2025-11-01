export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
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

export * from './dog';
export * from './employee';
export * from './project';
export * from './handler';
export * from './breeding';
export * from './training';
export * from './common';
