export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

export interface BaseFilters {
  skip?: number;
  limit?: number;
  search?: string;
}
