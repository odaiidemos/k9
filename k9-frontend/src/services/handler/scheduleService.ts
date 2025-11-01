import { apiClient } from '../api/apiClient';
import {
  DailySchedule,
  DailyScheduleItem,
  DailyScheduleCreateRequest,
  DailyScheduleItemCreateRequest
} from '../../types/handler';

export const scheduleService = {
  async createSchedule(data: DailyScheduleCreateRequest): Promise<DailySchedule> {
    const response = await apiClient.post<DailySchedule>('/handler-daily/schedules', data);
    return response.data;
  },

  async getSchedules(params?: {
    date_from?: string;
    date_to?: string;
    project_id?: string;
    skip?: number;
    limit?: number;
  }): Promise<DailySchedule[]> {
    const response = await apiClient.get<DailySchedule[]>('/handler-daily/schedules', { params });
    return response.data;
  },

  async getSchedule(scheduleId: string): Promise<DailySchedule> {
    const response = await apiClient.get<DailySchedule>(`/handler-daily/schedules/${scheduleId}`);
    return response.data;
  },

  async updateSchedule(scheduleId: string, data: { notes?: string; status?: string }): Promise<DailySchedule> {
    const response = await apiClient.put<DailySchedule>(`/handler-daily/schedules/${scheduleId}`, data);
    return response.data;
  },

  async lockSchedule(scheduleId: string): Promise<DailySchedule> {
    const response = await apiClient.post<DailySchedule>(`/handler-daily/schedules/${scheduleId}/lock`);
    return response.data;
  },

  async createScheduleItem(data: DailyScheduleItemCreateRequest): Promise<DailyScheduleItem> {
    const response = await apiClient.post<DailyScheduleItem>('/handler-daily/schedule-items', data);
    return response.data;
  },

  async updateScheduleItem(itemId: string, data: {
    status?: string;
    replacement_handler_id?: string;
    absence_reason?: string;
    replacement_notes?: string;
  }): Promise<DailyScheduleItem> {
    const response = await apiClient.put<DailyScheduleItem>(`/handler-daily/schedule-items/${itemId}`, data);
    return response.data;
  }
};
