import { apiClient } from '../api/apiClient';
import type { CheckupReportData, ReportFilters, PDFExportResponse } from '../../types/breeding';

export const checkupService = {
  async getDailyReport(filters: Omit<ReportFilters, 'range_type'>): Promise<CheckupReportData> {
    const response = await apiClient.get<CheckupReportData>('/breeding/checkup/daily', {
      params: filters
    });
    return response.data;
  },

  async getWeeklyReport(filters: Omit<ReportFilters, 'range_type'>): Promise<CheckupReportData> {
    const response = await apiClient.get<CheckupReportData>('/breeding/checkup/weekly', {
      params: filters
    });
    return response.data;
  },

  async getUnifiedReport(filters: ReportFilters): Promise<CheckupReportData> {
    const response = await apiClient.get<CheckupReportData>('/breeding/checkup/unified', {
      params: filters
    });
    return response.data;
  },

  async exportDailyPDF(filters: Omit<ReportFilters, 'range_type' | 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/breeding/checkup/daily/export-pdf', null, {
      params: filters
    });
    return response.data;
  },

  async exportWeeklyPDF(filters: Omit<ReportFilters, 'range_type' | 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/breeding/checkup/weekly/export-pdf', null, {
      params: filters
    });
    return response.data;
  },

  async exportUnifiedPDF(filters: Omit<ReportFilters, 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/breeding/checkup/unified/export-pdf', null, {
      params: filters
    });
    return response.data;
  }
};
