import { apiClient } from '../api/apiClient';
import type { TrainingReportData, TrainingFilters, PDFExportResponse } from '../../types/training';

export const trainingService = {
  async getUnifiedReport(filters: TrainingFilters): Promise<TrainingReportData> {
    const response = await apiClient.get<TrainingReportData>('/training/reports/unified', {
      params: filters
    });
    return response.data;
  },

  async exportUnifiedPDF(filters: Omit<TrainingFilters, 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/training/reports/unified/export-pdf', null, {
      params: filters
    });
    return response.data;
  }
};
