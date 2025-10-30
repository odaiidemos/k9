import { useState } from 'react';
import {
  useEmployees,
  useDeleteEmployee,
  useEmployeeStatistics,
} from '@services/employee/employeeService';
import EmployeeCard from '@/components/employees/EmployeeCard';
import type { Employee, EmployeeFilters, EmployeeRole } from '@/types/employee';

const Employees = () => {
  const [filters, setFilters] = useState<EmployeeFilters>({
    skip: 0,
    limit: 12,
  });

  const { data: employeesData, isLoading, error } = useEmployees(filters);
  const { data: stats } = useEmployeeStatistics();
  const deleteMutation = useDeleteEmployee();

  const handleEdit = (employee: Employee) => {
    console.log('Edit employee:', employee);
  };

  const handleDelete = async (employee: Employee) => {
    if (window.confirm(`هل أنت متأكد من حذف الموظف "${employee.name}"؟`)) {
      try {
        await deleteMutation.mutateAsync(employee.id);
      } catch (error) {
        console.error('Failed to delete employee:', error);
      }
    }
  };

  const handleFilterChange = (newFilters: Partial<EmployeeFilters>) => {
    setFilters((prev: EmployeeFilters) => ({ ...prev, ...newFilters, skip: 0 }));
  };

  const handlePageChange = (newSkip: number) => {
    setFilters((prev: EmployeeFilters) => ({ ...prev, skip: newSkip }));
  };

  if (isLoading) {
    return (
      <div className="container-fluid py-4">
        <div className="text-center py-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">جاري التحميل...</span>
          </div>
          <p className="mt-3">جاري تحميل البيانات...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container-fluid py-4">
        <div className="alert alert-danger">
          <i className="fas fa-exclamation-circle ms-2"></i>
          حدث خطأ أثناء تحميل البيانات
        </div>
      </div>
    );
  }

  const totalPages = Math.ceil((employeesData?.total || 0) / (filters.limit || 12));
  const currentPage = Math.floor((filters.skip || 0) / (filters.limit || 12)) + 1;

  return (
    <div className="container-fluid py-4">
      <div className="row mb-4">
        <div className="col-12">
          <h1 className="display-5">
            <i className="fas fa-users ms-3 text-primary"></i>
            إدارة الموظفين
          </h1>
          <p className="text-muted">إدارة شاملة لجميع موظفي الوحدة</p>
        </div>
      </div>

      {stats && (
        <div className="row mb-4">
          <div className="col-md-3">
            <div className="card bg-primary text-white">
              <div className="card-body">
                <h3 className="mb-0">{stats.total}</h3>
                <small>إجمالي الموظفين</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-success text-white">
              <div className="card-body">
                <h3 className="mb-0">{stats.active}</h3>
                <small>نشط</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-secondary text-white">
              <div className="card-body">
                <h3 className="mb-0">{stats.inactive}</h3>
                <small>غير نشط</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-info text-white">
              <div className="card-body">
                <h3 className="mb-0">{Object.keys(stats.by_role).length}</h3>
                <small>أنواع الوظائف</small>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="row mb-4">
        <div className="col-md-4">
          <input
            type="text"
            className="form-control"
            placeholder="بحث بالاسم أو رقم الموظف أو البريد..."
            onChange={(e) =>
              handleFilterChange({ search: e.target.value || undefined })
            }
          />
        </div>
        <div className="col-md-2">
          <select
            className="form-select"
            onChange={(e) =>
              handleFilterChange({
                role: (e.target.value as EmployeeRole) || undefined,
              })
            }
          >
            <option value="">كل الوظائف</option>
            <option value="سائس">سائس</option>
            <option value="مدرب">مدرب</option>
            <option value="مربي">مربي</option>
            <option value="طبيب">طبيب</option>
            <option value="مسؤول مشروع">مسؤول مشروع</option>
          </select>
        </div>
        <div className="col-md-2">
          <select
            className="form-select"
            onChange={(e) =>
              handleFilterChange({
                is_active:
                  e.target.value === '' ? undefined : e.target.value === 'true',
              })
            }
          >
            <option value="">كل الحالات</option>
            <option value="true">نشط</option>
            <option value="false">غير نشط</option>
          </select>
        </div>
        <div className="col-md-4">
          <button className="btn btn-primary w-100">
            <i className="fas fa-plus ms-2"></i>
            إضافة موظف جديد
          </button>
        </div>
      </div>

      <div className="row g-4 mb-4">
        {employeesData?.items.map((employee: Employee) => (
          <div key={employee.id} className="col-md-6 col-lg-4">
            <EmployeeCard
              employee={employee}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          </div>
        ))}
      </div>

      {employeesData && employeesData.total > (filters.limit || 12) && (
        <div className="row">
          <div className="col-12">
            <nav>
              <ul className="pagination justify-content-center">
                <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                  <button
                    className="page-link"
                    onClick={() =>
                      handlePageChange((currentPage - 2) * (filters.limit || 12))
                    }
                    disabled={currentPage === 1}
                  >
                    السابق
                  </button>
                </li>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <li
                    key={page}
                    className={`page-item ${page === currentPage ? 'active' : ''}`}
                  >
                    <button
                      className="page-link"
                      onClick={() => handlePageChange((page - 1) * (filters.limit || 12))}
                    >
                      {page}
                    </button>
                  </li>
                ))}
                <li
                  className={`page-item ${
                    currentPage === totalPages ? 'disabled' : ''
                  }`}
                >
                  <button
                    className="page-link"
                    onClick={() => handlePageChange(currentPage * (filters.limit || 12))}
                    disabled={currentPage === totalPages}
                  >
                    التالي
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      )}

      {employeesData?.items.length === 0 && (
        <div className="row">
          <div className="col-12">
            <div className="card text-center py-5">
              <div className="card-body">
                <i className="fas fa-users fa-4x text-muted mb-3"></i>
                <h5>لا يوجد موظفون</h5>
                <p className="text-muted">
                  {filters.search || filters.role || filters.is_active !== undefined
                    ? 'لم يتم العثور على نتائج مطابقة للفلاتر المحددة'
                    : 'ابدأ بإضافة موظف جديد إلى النظام'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Employees;
