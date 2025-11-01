import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { trainingService } from '@/services/training/trainingService';
import type { TrainingFilters } from '@/types/training';

export default function TrainingReports() {
  const [filters, setFilters] = useState<TrainingFilters>({
    range_type: 'daily',
    date: new Date().toISOString().split('T')[0],
    page: 1,
    per_page: 50
  });

  const { data: reportData, isLoading } = useQuery({
    queryKey: ['trainingReport', filters],
    queryFn: () => trainingService.getUnifiedReport(filters)
  });

  const handleRangeTypeChange = (rangeType: TrainingFilters['range_type']) => {
    setFilters({
      ...filters,
      range_type: rangeType,
      date: rangeType === 'daily' ? new Date().toISOString().split('T')[0] : undefined,
      week_start: undefined,
      year_month: undefined,
      date_from: undefined,
      date_to: undefined
    });
  };

  const handleExportPDF = async () => {
    try {
      const result = await trainingService.exportUnifiedPDF(filters);
      alert(`تم تصدير التقرير بنجاح: ${result.path}`);
    } catch (error) {
      console.error('Error exporting PDF:', error);
      alert('حدث خطأ أثناء تصدير التقرير');
    }
  };

  const getPerformanceBadgeClass = (rating?: string) => {
    switch (rating) {
      case 'EXCELLENT':
        return 'bg-success';
      case 'GOOD':
        return 'bg-primary';
      case 'AVERAGE':
        return 'bg-info';
      case 'BELOW_AVERAGE':
        return 'bg-warning';
      case 'POOR':
        return 'bg-danger';
      default:
        return 'bg-secondary';
    }
  };

  const getPerformanceText = (rating?: string) => {
    switch (rating) {
      case 'EXCELLENT':
        return 'ممتاز';
      case 'GOOD':
        return 'جيد';
      case 'AVERAGE':
        return 'متوسط';
      case 'BELOW_AVERAGE':
        return 'أقل من المتوسط';
      case 'POOR':
        return 'ضعيف';
      default:
        return '-';
    }
  };

  const getSessionTypeText = (type: string) => {
    const typeMap: Record<string, string> = {
      OBEDIENCE: 'الطاعة',
      DETECTION: 'الكشف',
      TRACKING: 'التعقب',
      PROTECTION: 'الحماية',
      AGILITY: 'الرشاقة',
      SOCIALIZATION: 'التنشئة الاجتماعية',
      OTHER: 'أخرى'
    };
    return typeMap[type] || type;
  };

  const getStatusText = (status: string) => {
    const statusMap: Record<string, string> = {
      SCHEDULED: 'مجدول',
      IN_PROGRESS: 'قيد التنفيذ',
      COMPLETED: 'مكتمل',
      CANCELLED: 'ملغي'
    };
    return statusMap[status] || status;
  };

  return (
    <div className="container-fluid py-4" dir="rtl">
      <div className="row mb-4">
        <div className="col">
          <h2 className="mb-0">
            <i className="fas fa-graduation-cap ms-2"></i>
            تقارير التدريب
          </h2>
          <p className="text-muted mb-0">تقارير شاملة لجلسات التدريب والأداء</p>
        </div>
        <div className="col-auto">
          <button className="btn btn-primary" onClick={handleExportPDF}>
            <i className="fas fa-file-pdf ms-2"></i>
            تصدير PDF
          </button>
        </div>
      </div>

      <div className="card border-0 shadow-sm mb-4">
        <div className="card-body">
          <div className="row g-3">
            <div className="col-md-3">
              <label className="form-label">نوع الفترة</label>
              <select
                className="form-select"
                value={filters.range_type}
                onChange={(e) => handleRangeTypeChange(e.target.value as TrainingFilters['range_type'])}
              >
                <option value="daily">يومي</option>
                <option value="weekly">أسبوعي</option>
                <option value="monthly">شهري</option>
                <option value="custom">مخصص</option>
              </select>
            </div>

            {filters.range_type === 'daily' && (
              <div className="col-md-3">
                <label className="form-label">التاريخ</label>
                <input
                  type="date"
                  className="form-control"
                  value={filters.date || ''}
                  onChange={(e) => setFilters({ ...filters, date: e.target.value })}
                />
              </div>
            )}

            {filters.range_type === 'weekly' && (
              <div className="col-md-3">
                <label className="form-label">بداية الأسبوع</label>
                <input
                  type="date"
                  className="form-control"
                  value={filters.week_start || ''}
                  onChange={(e) => setFilters({ ...filters, week_start: e.target.value })}
                />
              </div>
            )}

            {filters.range_type === 'monthly' && (
              <div className="col-md-3">
                <label className="form-label">الشهر</label>
                <input
                  type="month"
                  className="form-control"
                  value={filters.year_month || ''}
                  onChange={(e) => setFilters({ ...filters, year_month: e.target.value })}
                />
              </div>
            )}

            {filters.range_type === 'custom' && (
              <>
                <div className="col-md-3">
                  <label className="form-label">من تاريخ</label>
                  <input
                    type="date"
                    className="form-control"
                    value={filters.date_from || ''}
                    onChange={(e) => setFilters({ ...filters, date_from: e.target.value })}
                  />
                </div>
                <div className="col-md-3">
                  <label className="form-label">إلى تاريخ</label>
                  <input
                    type="date"
                    className="form-control"
                    value={filters.date_to || ''}
                    onChange={(e) => setFilters({ ...filters, date_to: e.target.value })}
                  />
                </div>
              </>
            )}

            <div className="col-md-3">
              <label className="form-label">المشروع (اختياري)</label>
              <input
                type="text"
                className="form-control"
                placeholder="معرف المشروع"
                value={filters.project_id || ''}
                onChange={(e) => setFilters({ ...filters, project_id: e.target.value })}
              />
            </div>

            <div className="col-md-3">
              <label className="form-label">نوع الجلسة (اختياري)</label>
              <select
                className="form-select"
                value={filters.session_type || ''}
                onChange={(e) => setFilters({ ...filters, session_type: e.target.value })}
              >
                <option value="">الكل</option>
                <option value="OBEDIENCE">الطاعة</option>
                <option value="DETECTION">الكشف</option>
                <option value="TRACKING">التعقب</option>
                <option value="PROTECTION">الحماية</option>
                <option value="AGILITY">الرشاقة</option>
                <option value="SOCIALIZATION">التنشئة الاجتماعية</option>
                <option value="OTHER">أخرى</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {reportData && (
        <div className="row g-4 mb-4">
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الجلسات</h6>
                <h3 className="mb-0">{reportData.kpis.total_sessions}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الكلاب</h6>
                <h3 className="mb-0">{reportData.kpis.total_dogs}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الساعات</h6>
                <h3 className="mb-0">{reportData.kpis.total_hours.toFixed(1)}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">متوسط المدة (دقيقة)</h6>
                <h3 className="mb-0">{reportData.kpis.avg_duration_minutes.toFixed(0)}</h3>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="card border-0 shadow-sm">
        <div className="card-header bg-white">
          <h5 className="mb-0">
            <i className="fas fa-table ms-2"></i>
            تفاصيل التقرير
          </h5>
        </div>
        <div className="card-body">
          {isLoading ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">جاري التحميل...</span>
              </div>
            </div>
          ) : reportData ? (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>اسم الكلب</th>
                    <th>الكود</th>
                    <th>المدرب</th>
                    <th>التاريخ</th>
                    <th>نوع الجلسة</th>
                    <th>المدة (دقيقة)</th>
                    <th>تقييم الأداء</th>
                    <th>الحالة</th>
                  </tr>
                </thead>
                <tbody>
                  {reportData.rows.map((row, index) => (
                    <tr key={index}>
                      <td>{row.dog_name}</td>
                      <td>{row.dog_code}</td>
                      <td>{row.trainer_name || '-'}</td>
                      <td>{row.session_date}</td>
                      <td>{getSessionTypeText(row.session_type)}</td>
                      <td>{row.duration_minutes || '-'}</td>
                      <td>
                        <span className={`badge ${getPerformanceBadgeClass(row.performance_rating)}`}>
                          {getPerformanceText(row.performance_rating)}
                        </span>
                      </td>
                      <td>{getStatusText(row.status)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="alert alert-info mb-0">
              <i className="fas fa-info-circle ms-2"></i>
              لا توجد بيانات لعرضها
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
