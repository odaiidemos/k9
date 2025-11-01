import { apiClient } from '../api/apiClient';
import { VeterinaryReportData, ReportFilters, PDFExportResponse } from '../../types/breeding';

export const veterinaryService = {
  async getUnifiedReport(filters: ReportFilters): Promise<VeterinaryReportData> {
    const response = await apiClient.get<VeterinaryReportData>('/breeding/veterinary/unified', {
      params: filters
    });
    return response.data;
  },

  async exportUnifiedPDF(filters: Omit<ReportFilters, 'page' | 'per_page'>): Promise<PDFExportResponse> {
    const response = await apiClient.post<PDFExportResponse>('/breeding/veterinary/unified/export-pdf', null, {
      params: filters
    });
    return response.data;
  }
};
