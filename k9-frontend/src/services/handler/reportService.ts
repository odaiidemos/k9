import { apiClient } from '../api/apiClient';
import type {
  HandlerReport,
  HandlerReportCreateRequest,
  HandlerReportUpdateRequest
} from '../../types/handler';

export const reportService = {
  async createReport(data: HandlerReportCreateRequest): Promise<HandlerReport> {
    const response = await apiClient.post<HandlerReport>('/handler-daily/reports', data);
    return response.data;
  },

  async getReports(params?: {
    handler_user_id?: string;
    dog_id?: string;
    project_id?: string;
    status?: string;
    date_from?: string;
    date_to?: string;
    skip?: number;
    limit?: number;
  }): Promise<HandlerReport[]> {
    const response = await apiClient.get<HandlerReport[]>('/handler-daily/reports', { params });
    return response.data;
  },

  async getReport(reportId: string): Promise<HandlerReport> {
    const response = await apiClient.get<HandlerReport>(`/handler-daily/reports/${reportId}`);
    return response.data;
  },

  async updateReport(reportId: string, data: HandlerReportUpdateRequest): Promise<HandlerReport> {
    const response = await apiClient.put<HandlerReport>(`/handler-daily/reports/${reportId}`, data);
    return response.data;
  },

  async submitReport(reportId: string): Promise<HandlerReport> {
    const response = await apiClient.post<HandlerReport>(`/handler-daily/reports/${reportId}/submit`);
    return response.data;
  },

  async approveReport(reportId: string, reviewNotes?: string): Promise<HandlerReport> {
    const response = await apiClient.post<HandlerReport>(`/handler-daily/reports/${reportId}/approve`, {
      review_notes: reviewNotes
    });
    return response.data;
  },

  async rejectReport(reportId: string, reviewNotes: string): Promise<HandlerReport> {
    const response = await apiClient.post<HandlerReport>(`/handler-daily/reports/${reportId}/reject`, {
      review_notes: reviewNotes
    });
    return response.data;
  }
};
