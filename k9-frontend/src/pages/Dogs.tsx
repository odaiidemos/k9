import { useState } from 'react';
import { useDogs, useDeleteDog, useDogStatistics } from '@services/dog/dogService';
import DogCard from '@/components/dogs/DogCard';
import type { Dog, DogFilters, DogStatus, DogGender } from '@/types/dog';

const Dogs = () => {
  const [filters, setFilters] = useState<DogFilters>({
    skip: 0,
    limit: 12,
  });

  const { data: dogsData, isLoading, error } = useDogs(filters);
  const { data: stats } = useDogStatistics();
  const deleteMutation = useDeleteDog();

  const handleEdit = (dog: Dog) => {
    // TODO: Open edit modal
    console.log('Edit dog:', dog);
  };

  const handleDelete = async (dog: Dog) => {
    if (window.confirm(`هل أنت متأكد من حذف الكلب "${dog.name}"؟`)) {
      try {
        await deleteMutation.mutateAsync(dog.id);
      } catch (error) {
        console.error('Failed to delete dog:', error);
      }
    }
  };

  const handleFilterChange = (newFilters: Partial<DogFilters>) => {
    setFilters((prev) => ({ ...prev, ...newFilters, skip: 0 }));
  };

  const handlePageChange = (newSkip: number) => {
    setFilters((prev) => ({ ...prev, skip: newSkip }));
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

  const totalPages = Math.ceil((dogsData?.total || 0) / (filters.limit || 12));
  const currentPage = Math.floor((filters.skip || 0) / (filters.limit || 12)) + 1;

  return (
    <div className="container-fluid py-4">
      {/* Page Header */}
      <div className="row mb-4">
        <div className="col-12">
          <h1 className="display-5">
            <i className="fas fa-dog ms-3 text-primary"></i>
            إدارة الكلاب
          </h1>
          <p className="text-muted">إدارة شاملة لجميع الكلاب البوليسية في النظام</p>
        </div>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="row mb-4">
          <div className="col-md-3">
            <div className="card bg-primary text-white">
              <div className="card-body">
                <h3 className="mb-0">{stats.total}</h3>
                <small>إجمالي الكلاب</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-success text-white">
              <div className="card-body">
                <h3 className="mb-0">{stats.by_status.ACTIVE || 0}</h3>
                <small>نشط</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-info text-white">
              <div className="card-body">
                <h3 className="mb-0">{stats.by_status.TRAINING || 0}</h3>
                <small>تحت التدريب</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-secondary text-white">
              <div className="card-body">
                <h3 className="mb-0">{stats.by_status.RETIRED || 0}</h3>
                <small>متقاعد</small>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Search and Filters */}
      <div className="row mb-4">
        <div className="col-md-4">
          <input
            type="text"
            className="form-control"
            placeholder="بحث بالاسم أو الكود أو رقم الشريحة..."
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
                status: (e.target.value as DogStatus) || undefined,
              })
            }
          >
            <option value="">كل الحالات</option>
            <option value="ACTIVE">نشط</option>
            <option value="TRAINING">تحت التدريب</option>
            <option value="RETIRED">متقاعد</option>
            <option value="INJURED">مصاب</option>
            <option value="DECEASED">متوفى</option>
          </select>
        </div>
        <div className="col-md-2">
          <select
            className="form-select"
            onChange={(e) =>
              handleFilterChange({
                gender: (e.target.value as DogGender) || undefined,
              })
            }
          >
            <option value="">كل الأنواع</option>
            <option value="MALE">ذكر</option>
            <option value="FEMALE">أنثى</option>
          </select>
        </div>
        <div className="col-md-2">
          <input
            type="text"
            className="form-control"
            placeholder="فلترة حسب السلالة..."
            onChange={(e) =>
              handleFilterChange({ breed: e.target.value || undefined })
            }
          />
        </div>
        <div className="col-md-2">
          <button className="btn btn-primary w-100">
            <i className="fas fa-plus ms-2"></i>
            إضافة كلب جديد
          </button>
        </div>
      </div>

      {/* Dogs Grid */}
      <div className="row g-4 mb-4">
        {dogsData?.items.map((dog) => (
          <div key={dog.id} className="col-md-6 col-lg-4">
            <DogCard dog={dog} onEdit={handleEdit} onDelete={handleDelete} />
          </div>
        ))}
      </div>

      {/* Pagination */}
      {dogsData && dogsData.total > (filters.limit || 12) && (
        <div className="row">
          <div className="col-12">
            <nav>
              <ul className="pagination justify-content-center">
                <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                  <button
                    className="page-link"
                    onClick={() =>
                      handlePageChange(((currentPage - 2) * (filters.limit || 12)))
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

      {/* Empty State */}
      {dogsData?.items.length === 0 && (
        <div className="row">
          <div className="col-12">
            <div className="card text-center py-5">
              <div className="card-body">
                <i className="fas fa-dog fa-4x text-muted mb-3"></i>
                <h5>لا توجد كلاب</h5>
                <p className="text-muted">
                  {filters.search || filters.status || filters.gender || filters.breed
                    ? 'لم يتم العثور على نتائج مطابقة للفلاتر المحددة'
                    : 'ابدأ بإضافة كلب جديد إلى النظام'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dogs;
