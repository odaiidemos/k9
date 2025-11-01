import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { scheduleService } from '@/services/handler/scheduleService';
import { reportService } from '@/services/handler/reportService';
import { notificationService } from '@/services/handler/notificationService';
import { useAppSelector } from '@/store/hooks';
import { DailySchedule, HandlerReport, Notification, ReportStatus } from '@/types/handler';

export default function HandlerDashboard() {
  const user = useAppSelector((state) => state.auth.user);
  const [todayDate] = useState(new Date().toISOString().split('T')[0]);

  const { data: todaySchedule, isLoading: loadingSchedule } = useQuery<DailySchedule | null>({
    queryKey: ['todaySchedule', user?.id, todayDate],
    queryFn: async () => {
      const schedules = await scheduleService.getSchedules({
        date_from: todayDate,
        date_to: todayDate
      });
      return schedules.length > 0 ? schedules[0] : null;
    },
    enabled: !!user
  });

  const { data: recentReports = [], isLoading: loadingReports } = useQuery<HandlerReport[]>({
    queryKey: ['recentReports', user?.id],
    queryFn: () => reportService.getReports({ handler_user_id: user?.id, limit: 5 }),
    enabled: !!user
  });

  const { data: notifications = [], isLoading: loadingNotifications } = useQuery<Notification[]>({
    queryKey: ['notifications', user?.id],
    queryFn: () => notificationService.getNotifications(true),
    enabled: !!user
  });

  const { data: stats } = useQuery({
    queryKey: ['reportStats', user?.id],
    queryFn: async () => {
      const allReports = await reportService.getReports({ handler_user_id: user?.id });
      const thisMonth = new Date();
      thisMonth.setDate(1);
      const thisMonthStr = thisMonth.toISOString().split('T')[0];

      return {
        total: allReports.length,
        approved: allReports.filter(r => r.status === ReportStatus.APPROVED).length,
        pending: allReports.filter(r => r.status === ReportStatus.SUBMITTED).length,
        thisMonth: allReports.filter(r => r.date >= thisMonthStr).length
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

  return (
    <div className="container-fluid py-4" dir="rtl">
      <div className="row mb-4">
        <div className="col">
          <h2 className="mb-0">
            <i className="fas fa-user-shield ms-2"></i>
            لوحة تحكم السائس
          </h2>
          <p className="text-muted mb-0">{new Date().toLocaleDateString('ar-SA')}</p>
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
                  <h6 className="text-muted mb-1">التقارير المعتمدة</h6>
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
                  <h6 className="text-muted mb-1">تقارير الشهر الحالي</h6>
                  <h3 className="mb-0">{stats?.thisMonth || 0}</h3>
                </div>
                <div className="text-info">
                  <i className="fas fa-calendar-alt fa-2x"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-lg-8">
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-header bg-white">
              <h5 className="mb-0">
                <i className="fas fa-calendar-day ms-2"></i>
                جدول اليوم
              </h5>
            </div>
            <div className="card-body">
              {loadingSchedule ? (
                <div className="text-center py-4">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">جاري التحميل...</span>
                  </div>
                </div>
              ) : todaySchedule ? (
                <div>
                  <p><strong>التاريخ:</strong> {todaySchedule.date}</p>
                  <p><strong>الحالة:</strong> {todaySchedule.status === 'LOCKED' ? 'مقفل' : 'مفتوح'}</p>
                  {todaySchedule.notes && <p><strong>ملاحظات:</strong> {todaySchedule.notes}</p>}
                </div>
              ) : (
                <div className="alert alert-info mb-0">
                  <i className="fas fa-info-circle ms-2"></i>
                  لا يوجد جدول محدد لهذا اليوم
                </div>
              )}
            </div>
          </div>

          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white">
              <h5 className="mb-0">
                <i className="fas fa-file-alt ms-2"></i>
                التقارير الأخيرة
              </h5>
            </div>
            <div className="card-body">
              {loadingReports ? (
                <div className="text-center py-4">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">جاري التحميل...</span>
                  </div>
                </div>
              ) : recentReports.length > 0 ? (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>التاريخ</th>
                        <th>الموقع</th>
                        <th>الحالة</th>
                        <th>الإجراءات</th>
                      </tr>
                    </thead>
                    <tbody>
                      {recentReports.map((report) => (
                        <tr key={report.id}>
                          <td>{report.date}</td>
                          <td>{report.location || '-'}</td>
                          <td>
                            <span className={`badge ${getStatusBadgeClass(report.status)}`}>
                              {getStatusText(report.status)}
                            </span>
                          </td>
                          <td>
                            <button className="btn btn-sm btn-outline-primary">
                              <i className="fas fa-eye ms-1"></i>
                              عرض
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="alert alert-info mb-0">
                  <i className="fas fa-info-circle ms-2"></i>
                  لا توجد تقارير بعد
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="col-lg-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white">
              <h5 className="mb-0">
                <i className="fas fa-bell ms-2"></i>
                الإشعارات
                {notifications.length > 0 && (
                  <span className="badge bg-danger me-2">{notifications.length}</span>
                )}
              </h5>
            </div>
            <div className="card-body">
              {loadingNotifications ? (
                <div className="text-center py-4">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">جاري التحميل...</span>
                  </div>
                </div>
              ) : notifications.length > 0 ? (
                <div className="list-group list-group-flush">
                  {notifications.map((notification) => (
                    <div key={notification.id} className="list-group-item px-0">
                      <div className="d-flex w-100 justify-content-between">
                        <h6 className="mb-1">{notification.title}</h6>
                        <small className="text-muted">
                          {new Date(notification.created_at).toLocaleDateString('ar-SA')}
                        </small>
                      </div>
                      <p className="mb-1 small">{notification.message}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="alert alert-info mb-0">
                  <i className="fas fa-info-circle ms-2"></i>
                  لا توجد إشعارات جديدة
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
