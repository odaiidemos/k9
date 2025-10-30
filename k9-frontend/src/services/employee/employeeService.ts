import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@services/api/apiClient';
import type {
  Employee,
  EmployeeCreate,
  EmployeeUpdate,
  EmployeeFilters,
  EmployeeStats,
} from '@/types/employee';
import type { PaginatedResponse } from '@/types';

const EMPLOYEES_KEY = 'employees';

export const employeeService = {
  async getEmployees(filters?: EmployeeFilters): Promise<PaginatedResponse<Employee>> {
    const params = new URLSearchParams();
    if (filters?.skip !== undefined) params.append('skip', filters.skip.toString());
    if (filters?.limit) params.append('limit', filters.limit.toString());
    if (filters?.role) params.append('role', filters.role);
    if (filters?.is_active !== undefined) params.append('is_active', filters.is_active.toString());
    if (filters?.search) params.append('search', filters.search);

    const response = await apiClient.get<PaginatedResponse<Employee>>(
      `/employees?${params.toString()}`
    );
    return response.data;
  },

  async getEmployee(id: string): Promise<Employee> {
    const response = await apiClient.get<Employee>(`/employees/${id}`);
    return response.data;
  },

  async createEmployee(data: EmployeeCreate): Promise<Employee> {
    const response = await apiClient.post<Employee>('/employees', data);
    return response.data;
  },

  async updateEmployee(id: string, data: EmployeeUpdate): Promise<Employee> {
    const response = await apiClient.put<Employee>(`/employees/${id}`, data);
    return response.data;
  },

  async deleteEmployee(id: string): Promise<void> {
    await apiClient.delete(`/employees/${id}`);
  },

  async getEmployeeStats(): Promise<EmployeeStats> {
    const response = await apiClient.get<EmployeeStats>('/employees/stats/summary');
    return response.data;
  },
};

export const useEmployees = (filters?: EmployeeFilters) => {
  return useQuery({
    queryKey: [EMPLOYEES_KEY, filters],
    queryFn: () => employeeService.getEmployees(filters),
  });
};

export const useEmployee = (id: string) => {
  return useQuery({
    queryKey: [EMPLOYEES_KEY, id],
    queryFn: () => employeeService.getEmployee(id),
    enabled: !!id,
  });
};

export const useCreateEmployee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: employeeService.createEmployee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [EMPLOYEES_KEY] });
    },
  });
};

export const useUpdateEmployee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: EmployeeUpdate }) =>
      employeeService.updateEmployee(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [EMPLOYEES_KEY] });
    },
  });
};

export const useDeleteEmployee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: employeeService.deleteEmployee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [EMPLOYEES_KEY] });
    },
  });
};

export const useEmployeeStatistics = () => {
  return useQuery({
    queryKey: [EMPLOYEES_KEY, 'stats'],
    queryFn: employeeService.getEmployeeStats,
  });
};
