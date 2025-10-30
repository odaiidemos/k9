import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@services/api/apiClient';
import type {
  Project,
  ProjectCreate,
  ProjectUpdate,
  ProjectFilters,
  ProjectStats,
} from '@/types/project';
import type { PaginatedResponse } from '@/types';

const PROJECTS_KEY = 'projects';

export const projectService = {
  async getProjects(filters?: ProjectFilters): Promise<PaginatedResponse<Project>> {
    const params = new URLSearchParams();
    if (filters?.skip !== undefined) params.append('skip', filters.skip.toString());
    if (filters?.limit) params.append('limit', filters.limit.toString());
    if (filters?.status) params.append('status', filters.status);
    if (filters?.priority) params.append('priority', filters.priority);
    if (filters?.search) params.append('search', filters.search);

    const response = await apiClient.get<PaginatedResponse<Project>>(
      `/projects?${params.toString()}`
    );
    return response.data;
  },

  async getProject(id: string): Promise<Project> {
    const response = await apiClient.get<Project>(`/projects/${id}`);
    return response.data;
  },

  async createProject(data: ProjectCreate): Promise<Project> {
    const response = await apiClient.post<Project>('/projects', data);
    return response.data;
  },

  async updateProject(id: string, data: ProjectUpdate): Promise<Project> {
    const response = await apiClient.put<Project>(`/projects/${id}`, data);
    return response.data;
  },

  async deleteProject(id: string): Promise<void> {
    await apiClient.delete(`/projects/${id}`);
  },

  async getProjectStats(): Promise<ProjectStats> {
    const response = await apiClient.get<ProjectStats>('/projects/stats/summary');
    return response.data;
  },
};

export const useProjects = (filters?: ProjectFilters) => {
  return useQuery({
    queryKey: [PROJECTS_KEY, filters],
    queryFn: () => projectService.getProjects(filters),
  });
};

export const useProject = (id: string) => {
  return useQuery({
    queryKey: [PROJECTS_KEY, id],
    queryFn: () => projectService.getProject(id),
    enabled: !!id,
  });
};

export const useCreateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: projectService.createProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [PROJECTS_KEY] });
    },
  });
};

export const useUpdateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ProjectUpdate }) =>
      projectService.updateProject(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [PROJECTS_KEY] });
    },
  });
};

export const useDeleteProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: projectService.deleteProject,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [PROJECTS_KEY] });
    },
  });
};

export const useProjectStatistics = () => {
  return useQuery({
    queryKey: [PROJECTS_KEY, 'stats'],
    queryFn: projectService.getProjectStats,
  });
};
