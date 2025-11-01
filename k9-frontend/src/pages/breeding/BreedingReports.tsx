import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { feedingService } from '@/services/breeding/feedingService';
import { checkupService } from '@/services/breeding/checkupService';
import { veterinaryService } from '@/services/breeding/veterinaryService';
import { caretakerService } from '@/services/breeding/caretakerService';
import type { RangeType, ReportFilters } from '@/types/breeding';

type ReportType = 'feeding' | 'checkup' | 'veterinary' | 'caretaker';

export default function BreedingReports() {
  const [activeReport, setActiveReport] = useState<ReportType>('feeding');
  const [filters, setFilters] = useState<ReportFilters>({
    range_type: 'daily',
    date: new Date().toISOString().split('T')[0],
    page: 1,
    per_page: 50
  });

  const { data: feedingData, isLoading: loadingFeeding } = useQuery({
    queryKey: ['feedingReport', filters],
    queryFn: () => feedingService.getUnifiedReport(filters),
    enabled: activeReport === 'feeding'
  });

  const { data: checkupData, isLoading: loadingCheckup } = useQuery({
    queryKey: ['checkupReport', filters],
    queryFn: () => checkupService.getUnifiedReport(filters),
    enabled: activeReport === 'checkup'
  });

  const { data: veterinaryData, isLoading: loadingVeterinary } = useQuery({
    queryKey: ['veterinaryReport', filters],
    queryFn: () => veterinaryService.getUnifiedReport(filters),
    enabled: activeReport === 'veterinary'
  });

  const { data: caretakerData, isLoading: loadingCaretaker } = useQuery({
    queryKey: ['caretakerReport', filters],
    queryFn: () => caretakerService.getUnifiedReport(filters),
    enabled: activeReport === 'caretaker'
  });

  const handleRangeTypeChange = (rangeType: RangeType) => {
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
      let result;
      if (activeReport === 'feeding') {
        result = await feedingService.exportUnifiedPDF(filters);
      } else if (activeReport === 'checkup') {
        result = await checkupService.exportUnifiedPDF(filters);
      } else if (activeReport === 'veterinary') {
        result = await veterinaryService.exportUnifiedPDF(filters);
      } else {
        result = await caretakerService.exportUnifiedPDF(filters);
      }
      alert(`تم تصدير التقرير بنجاح: ${result.path}`);
    } catch (error) {
      console.error('Error exporting PDF:', error);
      alert('حدث خطأ أثناء تصدير التقرير');
    }
  };

  const isLoading = loadingFeeding || loadingCheckup || loadingVeterinary || loadingCaretaker;

  return (
    <div className="container-fluid py-4" dir="rtl">
      <div className="row mb-4">
        <div className="col">
          <h2 className="mb-0">
            <i className="fas fa-clipboard-list ms-2"></i>
            تقارير الإنتاج والرعاية
          </h2>
          <p className="text-muted mb-0">تقارير شاملة للتغذية والفحوصات والرعاية البيطرية واليومية</p>
        </div>
        <div className="col-auto">
          <button className="btn btn-primary" onClick={handleExportPDF}>
            <i className="fas fa-file-pdf ms-2"></i>
            تصدير PDF
          </button>
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-12">
          <ul className="nav nav-tabs">
            <li className="nav-item">
              <button
                className={`nav-link ${activeReport === 'feeding' ? 'active' : ''}`}
                onClick={() => setActiveReport('feeding')}
              >
                <i className="fas fa-utensils ms-2"></i>
                تقارير التغذية
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeReport === 'checkup' ? 'active' : ''}`}
                onClick={() => setActiveReport('checkup')}
              >
                <i className="fas fa-heartbeat ms-2"></i>
                تقارير الفحوصات
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeReport === 'veterinary' ? 'active' : ''}`}
                onClick={() => setActiveReport('veterinary')}
              >
                <i className="fas fa-stethoscope ms-2"></i>
                التقارير البيطرية
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeReport === 'caretaker' ? 'active' : ''}`}
                onClick={() => setActiveReport('caretaker')}
              >
                <i className="fas fa-user-nurse ms-2"></i>
                تقارير الرعاية اليومية
              </button>
            </li>
          </ul>
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
                onChange={(e) => handleRangeTypeChange(e.target.value as RangeType)}
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
          </div>
        </div>
      </div>

      {activeReport === 'feeding' && feedingData && (
        <div className="row g-4 mb-4">
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الكلاب</h6>
                <h3 className="mb-0">{feedingData.kpis.total_dogs}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الوجبات</h6>
                <h3 className="mb-0">{feedingData.kpis.total_meals}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الطعام (كجم)</h6>
                <h3 className="mb-0">{feedingData.kpis.total_food_kg.toFixed(2)}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">متوسط الطعام لكل كلب</h6>
                <h3 className="mb-0">{feedingData.kpis.avg_food_per_dog.toFixed(2)}</h3>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeReport === 'checkup' && checkupData && (
        <div className="row g-4 mb-4">
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الكلاب</h6>
                <h3 className="mb-0">{checkupData.kpis.total_dogs}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الفحوصات</h6>
                <h3 className="mb-0">{checkupData.kpis.total_checkups}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">متوسط الوزن (كجم)</h6>
                <h3 className="mb-0">{checkupData.kpis.avg_weight.toFixed(2)}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">متوسط الحرارة (°C)</h6>
                <h3 className="mb-0">{checkupData.kpis.avg_temperature.toFixed(1)}</h3>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeReport === 'veterinary' && veterinaryData && (
        <div className="row g-4 mb-4">
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الزيارات</h6>
                <h3 className="mb-0">{veterinaryData.kpis.total_visits}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الكلاب</h6>
                <h3 className="mb-0">{veterinaryData.kpis.total_dogs}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي التكلفة</h6>
                <h3 className="mb-0">{veterinaryData.kpis.total_cost.toFixed(2)}</h3>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeReport === 'caretaker' && caretakerData && (
        <div className="row g-4 mb-4">
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي الكلاب</h6>
                <h3 className="mb-0">{caretakerData.kpis.total_dogs}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">إجمالي السجلات</h6>
                <h3 className="mb-0">{caretakerData.kpis.total_logs}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">متوسط التمرين (دقيقة)</h6>
                <h3 className="mb-0">{caretakerData.kpis.avg_exercise_minutes.toFixed(0)}</h3>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card border-0 shadow-sm h-100">
              <div className="card-body">
                <h6 className="text-muted mb-1">كلاب بها حوادث</h6>
                <h3 className="mb-0 text-warning">{caretakerData.kpis.dogs_with_incidents}</h3>
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
          ) : (
            <div className="table-responsive">
              {activeReport === 'feeding' && feedingData && (
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>اسم الكلب</th>
                      <th>الكود</th>
                      <th>المشروع</th>
                      <th>عدد الوجبات</th>
                      <th>إجمالي الطعام (كجم)</th>
                      <th>الحالة البدنية</th>
                    </tr>
                  </thead>
                  <tbody>
                    {feedingData.rows.map((row, index) => (
                      <tr key={index}>
                        <td>{row.dog_name}</td>
                        <td>{row.dog_code}</td>
                        <td>{row.project_name || '-'}</td>
                        <td>{row.meal_count}</td>
                        <td>{row.total_food_kg.toFixed(2)}</td>
                        <td>{row.avg_body_condition || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}

              {activeReport === 'checkup' && checkupData && (
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>اسم الكلب</th>
                      <th>الكود</th>
                      <th>المشروع</th>
                      <th>عدد الفحوصات</th>
                      <th>متوسط الوزن</th>
                      <th>متوسط الحرارة</th>
                      <th>الحالة البدنية</th>
                    </tr>
                  </thead>
                  <tbody>
                    {checkupData.rows.map((row, index) => (
                      <tr key={index}>
                        <td>{row.dog_name}</td>
                        <td>{row.dog_code}</td>
                        <td>{row.project_name || '-'}</td>
                        <td>{row.checkup_count}</td>
                        <td>{row.avg_weight?.toFixed(2) || '-'}</td>
                        <td>{row.avg_temperature?.toFixed(1) || '-'}</td>
                        <td>{row.body_condition || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}

              {activeReport === 'veterinary' && veterinaryData && (
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>اسم الكلب</th>
                      <th>الكود</th>
                      <th>الطبيب البيطري</th>
                      <th>تاريخ الزيارة</th>
                      <th>نوع الزيارة</th>
                      <th>الأولوية</th>
                      <th>التشخيص</th>
                      <th>التكلفة</th>
                    </tr>
                  </thead>
                  <tbody>
                    {veterinaryData.rows.map((row, index) => (
                      <tr key={index}>
                        <td>{row.dog_name}</td>
                        <td>{row.dog_code}</td>
                        <td>{row.vet_name || '-'}</td>
                        <td>{row.visit_date}</td>
                        <td>{row.visit_type}</td>
                        <td>
                          <span className={`badge ${
                            row.priority === 'CRITICAL' ? 'bg-danger' :
                            row.priority === 'HIGH' ? 'bg-warning' :
                            'bg-info'
                          }`}>
                            {row.priority || '-'}
                          </span>
                        </td>
                        <td>{row.diagnosis || '-'}</td>
                        <td>{row.cost?.toFixed(2) || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}

              {activeReport === 'caretaker' && caretakerData && (
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>اسم الكلب</th>
                      <th>الكود</th>
                      <th>المشروع</th>
                      <th>عدد السجلات</th>
                      <th>متوسط التمرين (دقيقة)</th>
                      <th>حوادث</th>
                      <th>الراعي</th>
                    </tr>
                  </thead>
                  <tbody>
                    {caretakerData.rows.map((row, index) => (
                      <tr key={index}>
                        <td>{row.dog_name}</td>
                        <td>{row.dog_code}</td>
                        <td>{row.project_name || '-'}</td>
                        <td>{row.log_count}</td>
                        <td>{row.avg_exercise_minutes?.toFixed(0) || '-'}</td>
                        <td>
                          {row.has_incidents ? (
                            <span className="badge bg-warning">نعم</span>
                          ) : (
                            <span className="badge bg-success">لا</span>
                          )}
                        </td>
                        <td>{row.caretaker_name || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
