import { apiClient } from '../api/apiClient';
import { FeedingReportData, ReportFilters, PDFExportResponse } from '../../types/breeding';

export const feedingService = {
  async getDailyReport(filters: Omit<ReportFilters, 'range_type'>): Promise<FeedingReportData> {
    const response = await apiClient.get<FeedingReportData>('/breeding/feeding/daily', {
      params: filters
    });
    return response.data;
  },

  async getWeeklyReport(filters: Omit<ReportFilters, 'range_type'>): Promise<FeedingReportData> {
    const response = await apiClient.get<FeedingReportData>('/breeding/feeding/weekly', {
      params: filters
    });
    return response.data;
  },

  async getUnifiedReport(filters: ReportFilters): Promise<FeedingReportData> {
    const response = await apiClient.get<FeedingReportData>('/breeding/feeding/unified', {
      params: filters
    });
    return response.data;
  },

  async exportDailyPDF(filters: Omit<ReportFilters, 'range_type' | 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/breeding/feeding/daily/export-pdf', null, {
      params: filters
    });
    return response.data;
  },

  async exportWeeklyPDF(filters: Omit<ReportFilters, 'range_type' | 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/breeding/feeding/weekly/export-pdf', null, {
      params: filters
    });
    return response.data;
  },

  async exportUnifiedPDF(filters: Omit<ReportFilters, 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/breeding/feeding/unified/export-pdf', null, {
      params: filters
    });
    return response.data;
  }
};
