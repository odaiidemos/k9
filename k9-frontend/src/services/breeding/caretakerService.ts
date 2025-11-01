import { apiClient } from '../api/apiClient';
import type { CaretakerReportData, ReportFilters, PDFExportResponse } from '../../types/breeding';

export const caretakerService = {
  async getUnifiedReport(filters: ReportFilters): Promise<CaretakerReportData> {
    const response = await apiClient.get<CaretakerReportData>('/breeding/caretaker/unified', {
      params: filters
    });
    return response.data;
  },

  async exportUnifiedPDF(filters: Omit<ReportFilters, 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/breeding/caretaker/unified/export-pdf', null, {
      params: filters
    });
    return response.data;
  }
};
