import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { scheduleService } from '@/services/handler/scheduleService';
import { reportService } from '@/services/handler/reportService';
import { useAppSelector } from '@/store/hooks';
import { DailySchedule, HandlerReport, ReportStatus } from '@/types/handler';

export default function SupervisorDashboard() {
  const user = useAppSelector((state) => state.auth.user);
  const [filter, setFilter] = useState({
    status: '',
    dateFrom: '',
    dateTo: ''
  });

  const { data: schedules = [], isLoading: loadingSchedules } = useQuery<DailySchedule[]>({
    queryKey: ['schedules', filter],
    queryFn: () => scheduleService.getSchedules({
      date_from: filter.dateFrom || undefined,
      date_to: filter.dateTo || undefined,
      limit: 10
    }),
    enabled: !!user
  });

  const { data: reports = [], isLoading: loadingReports } = useQuery<HandlerReport[]>({
    queryKey: ['pendingReports', user?.id],
    queryFn: () => reportService.getReports({ 
      status: ReportStatus.SUBMITTED,
      limit: 10 
    }),
    enabled: !!user
  });

  const { data: stats } = useQuery({
    queryKey: ['supervisorStats', user?.id],
    queryFn: async () => {
      const allReports = await reportService.getReports({});
      
      return {
        total: allReports.length,
        pending: allReports.filter(r => r.status === ReportStatus.SUBMITTED).length,
        approved: allReports.filter(r => r.status === ReportStatus.APPROVED).length,
        rejected: allReports.filter(r => r.status === ReportStatus.REJECTED).length
      };
    },
    enabled: !!user
  });

  const getStatusBadgeClass = (status: ReportStatus) => {
    switch (status) {
      case ReportStatus.DRAFT:
        return 'bg-secondary';
      case ReportStatus.SUBMITTED:
        return 'bg-warning';
      case ReportStatus.APPROVED:
        return 'bg-success';
      case ReportStatus.REJECTED:
        return 'bg-danger';
      default:
        return 'bg-secondary';
    }
  };

  const getStatusText = (status: ReportStatus) => {
    switch (status) {
      case ReportStatus.DRAFT:
        return 'مسودة';
      case ReportStatus.SUBMITTED:
        return 'قيد المراجعة';
      case ReportStatus.APPROVED:
        return 'معتمد';
      case ReportStatus.REJECTED:
        return 'مرفوض';
      default:
        return status;
    }
  };

  const handleApprove = async (reportId: string) => {
    try {
      await reportService.approveReport(reportId);
      alert('تم اعتماد التقرير بنجاح');
    } catch (error) {
      console.error('Error approving report:', error);
      alert('حدث خطأ أثناء اعتماد التقرير');
    }
  };

  const handleReject = async (reportId: string) => {
    const notes = prompt('أدخل سبب الرفض:');
    if (!notes) return;

    try {
      await reportService.rejectReport(reportId, notes);
      alert('تم رفض التقرير');
    } catch (error) {
      console.error('Error rejecting report:', error);
      alert('حدث خطأ أثناء رفض التقرير');
    }
  };

  return (
    <div className="container-fluid py-4" dir="rtl">
      <div className="row mb-4">
        <div className="col">
          <h2 className="mb-0">
            <i className="fas fa-user-tie ms-2"></i>
            لوحة تحكم المشرف
          </h2>
          <p className="text-muted mb-0">إدارة الجداول اليومية ومراجعة تقارير السائسين</p>
        </div>
        <div className="col-auto">
          <button className="btn btn-primary">
            <i className="fas fa-plus ms-2"></i>
            إنشاء جدول جديد
          </button>
        </div>
      </div>

      <div className="row g-3 mb-4">
        <div className="col-md-3">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="flex-grow-1">
                  <h6 className="text-muted mb-1">إجمالي التقارير</h6>
                  <h3 className="mb-0">{stats?.total || 0}</h3>
                </div>
                <div className="text-primary">
                  <i className="fas fa-file-alt fa-2x"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="flex-grow-1">
                  <h6 className="text-muted mb-1">قيد المراجعة</h6>
                  <h3 className="mb-0 text-warning">{stats?.pending || 0}</h3>
                </div>
                <div className="text-warning">
                  <i className="fas fa-clock fa-2x"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="flex-grow-1">
                  <h6 className="text-muted mb-1">معتمدة</h6>
                  <h3 className="mb-0 text-success">{stats?.approved || 0}</h3>
                </div>
                <div className="text-success">
                  <i className="fas fa-check-circle fa-2x"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex align-items-center">
                <div className="flex-grow-1">
                  <h6 className="text-muted mb-1">مرفوضة</h6>
                  <h3 className="mb-0 text-danger">{stats?.rejected || 0}</h3>
                </div>
                <div className="text-danger">
                  <i className="fas fa-times-circle fa-2x"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row g-4 mb-4">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white">
              <h5 className="mb-0">
                <i className="fas fa-hourglass-half ms-2"></i>
                التقارير قيد المراجعة
                {reports.length > 0 && (
                  <span className="badge bg-warning me-2">{reports.length}</span>
                )}
              </h5>
            </div>
            <div className="card-body">
              {loadingReports ? (
                <div className="text-center py-4">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">جاري التحميل...</span>
                  </div>
                </div>
              ) : reports.length > 0 ? (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>التاريخ</th>
                        <th>السائس</th>
                        <th>الكلب</th>
                        <th>الموقع</th>
                        <th>الحالة</th>
                        <th>الإجراءات</th>
                      </tr>
                    </thead>
                    <tbody>
                      {reports.map((report) => (
                        <tr key={report.id}>
                          <td>{report.date}</td>
                          <td>{report.handler_user_id}</td>
                          <td>{report.dog_id}</td>
                          <td>{report.location || '-'}</td>
                          <td>
                            <span className={`badge ${getStatusBadgeClass(report.status)}`}>
                              {getStatusText(report.status)}
                            </span>
                          </td>
                          <td>
                            <div className="btn-group btn-group-sm">
                              <button className="btn btn-outline-primary">
                                <i className="fas fa-eye ms-1"></i>
                                عرض
                              </button>
                              <button 
                                className="btn btn-outline-success"
                                onClick={() => handleApprove(report.id)}
                              >
                                <i className="fas fa-check ms-1"></i>
                                اعتماد
                              </button>
                              <button 
                                className="btn btn-outline-danger"
                                onClick={() => handleReject(report.id)}
                              >
                                <i className="fas fa-times ms-1"></i>
                                رفض
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="alert alert-info mb-0">
                  <i className="fas fa-info-circle ms-2"></i>
                  لا توجد تقارير قيد المراجعة
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white">
              <h5 className="mb-0">
                <i className="fas fa-calendar-alt ms-2"></i>
                الجداول اليومية الأخيرة
              </h5>
            </div>
            <div className="card-body">
              {loadingSchedules ? (
                <div className="text-center py-4">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">جاري التحميل...</span>
                  </div>
                </div>
              ) : schedules.length > 0 ? (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>التاريخ</th>
                        <th>المشروع</th>
                        <th>الحالة</th>
                        <th>الملاحظات</th>
                        <th>الإجراءات</th>
                      </tr>
                    </thead>
                    <tbody>
                      {schedules.map((schedule) => (
                        <tr key={schedule.id}>
                          <td>{schedule.date}</td>
                          <td>{schedule.project_id || '-'}</td>
                          <td>
                            <span className={`badge ${schedule.status === 'LOCKED' ? 'bg-secondary' : 'bg-primary'}`}>
                              {schedule.status === 'LOCKED' ? 'مقفل' : 'مفتوح'}
                            </span>
                          </td>
                          <td>{schedule.notes || '-'}</td>
                          <td>
                            <div className="btn-group btn-group-sm">
                              <button className="btn btn-outline-primary">
                                <i className="fas fa-eye ms-1"></i>
                                عرض
                              </button>
                              {schedule.status !== 'LOCKED' && (
                                <button className="btn btn-outline-secondary">
                                  <i className="fas fa-edit ms-1"></i>
                                  تعديل
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="alert alert-info mb-0">
                  <i className="fas fa-info-circle ms-2"></i>
                  لا توجد جداول بعد
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
