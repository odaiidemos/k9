import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@services/api/apiClient';
import type { Dog, DogCreate, DogUpdate, DogFilters, PaginatedDogs, DogStatistics } from '@/types/dog';

const DOG_QUERY_KEY = 'dogs';

// Fetch paginated list of dogs
export const useDogs = (filters?: DogFilters) => {
  return useQuery({
    queryKey: [DOG_QUERY_KEY, 'list', filters],
    queryFn: async (): Promise<PaginatedDogs> => {
      const response = await apiClient.get('/dogs/', { params: filters });
      return response.data;
    },
  });
};

// Fetch single dog by ID
export const useDog = (dogId: string | undefined) => {
  return useQuery({
    queryKey: [DOG_QUERY_KEY, dogId],
    queryFn: async (): Promise<Dog> => {
      const response = await apiClient.get(`/dogs/${dogId}`);
      return response.data;
    },
    enabled: !!dogId,
  });
};

// Fetch dog statistics
export const useDogStatistics = () => {
  return useQuery({
    queryKey: [DOG_QUERY_KEY, 'stats'],
    queryFn: async (): Promise<DogStatistics> => {
      const response = await apiClient.get('/dogs/stats/summary');
      return response.data;
    },
  });
};

// Create new dog
export const useCreateDog = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: DogCreate): Promise<Dog> => {
      const response = await apiClient.post('/dogs/', data);
      return response.data;
    },
    onSuccess: () => {
      // Invalidate and refetch dog list
      queryClient.invalidateQueries({ queryKey: [DOG_QUERY_KEY, 'list'] });
      queryClient.invalidateQueries({ queryKey: [DOG_QUERY_KEY, 'stats'] });
    },
  });
};

// Update existing dog
export const useUpdateDog = (dogId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: DogUpdate): Promise<Dog> => {
      const response = await apiClient.put(`/dogs/${dogId}`, data);
      return response.data;
    },
    onSuccess: () => {
      // Invalidate and refetch dog list and specific dog
      queryClient.invalidateQueries({ queryKey: [DOG_QUERY_KEY, 'list'] });
      queryClient.invalidateQueries({ queryKey: [DOG_QUERY_KEY, dogId] });
      queryClient.invalidateQueries({ queryKey: [DOG_QUERY_KEY, 'stats'] });
    },
  });
};

// Delete dog
export const useDeleteDog = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (dogId: string): Promise<void> => {
      await apiClient.delete(`/dogs/${dogId}`);
    },
    onSuccess: () => {
      // Invalidate and refetch dog list
      queryClient.invalidateQueries({ queryKey: [DOG_QUERY_KEY, 'list'] });
      queryClient.invalidateQueries({ queryKey: [DOG_QUERY_KEY, 'stats'] });
    },
  });
};
