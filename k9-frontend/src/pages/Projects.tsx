import { useState } from 'react';
import {
  useProjects,
  useDeleteProject,
  useProjectStatistics,
} from '@services/project/projectService';
import ProjectCard from '@/components/projects/ProjectCard';
import type { Project, ProjectFilters, ProjectStatus } from '@/types/project';

const Projects = () => {
  const [filters, setFilters] = useState<ProjectFilters>({
    skip: 0,
    limit: 12,
  });

  const { data: projectsData, isLoading, error } = useProjects(filters);
  const { data: stats } = useProjectStatistics();
  const deleteMutation = useDeleteProject();

  const handleEdit = (project: Project) => {
    console.log('Edit project:', project);
  };

  const handleDelete = async (project: Project) => {
    if (window.confirm(`هل أنت متأكد من حذف المشروع "${project.name}"؟`)) {
      try {
        await deleteMutation.mutateAsync(project.id);
      } catch (error) {
        console.error('Failed to delete project:', error);
      }
    }
  };

  const handleFilterChange = (newFilters: Partial<ProjectFilters>) => {
    setFilters((prev: ProjectFilters) => ({ ...prev, ...newFilters, skip: 0 }));
  };

  const handlePageChange = (newSkip: number) => {
    setFilters((prev: ProjectFilters) => ({ ...prev, skip: newSkip }));
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

  const totalPages = Math.ceil((projectsData?.total || 0) / (filters.limit || 12));
  const currentPage = Math.floor((filters.skip || 0) / (filters.limit || 12)) + 1;

  return (
    <div className="container-fluid py-4">
      <div className="row mb-4">
        <div className="col-12">
          <h1 className="display-5">
            <i className="fas fa-project-diagram ms-3 text-primary"></i>
            إدارة المشاريع
          </h1>
          <p className="text-muted">إدارة شاملة لجميع مشاريع الوحدة</p>
        </div>
      </div>

      {stats && (
        <div className="row mb-4">
          <div className="col-md-3">
            <div className="card bg-primary text-white">
              <div className="card-body">
                <h3 className="mb-0">{stats.total}</h3>
                <small>إجمالي المشاريع</small>
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
                <h3 className="mb-0">{stats.completed_projects}</h3>
                <small>مكتمل</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-warning text-dark">
              <div className="card-body">
                <h3 className="mb-0">{stats.average_success_rating.toFixed(1)}</h3>
                <small>متوسط التقييم</small>
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
            placeholder="بحث بالاسم أو الكود أو الوصف..."
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
                status: (e.target.value as ProjectStatus) || undefined,
              })
            }
          >
            <option value="">كل الحالات</option>
            <option value="PLANNED">مخطط</option>
            <option value="ACTIVE">نشط</option>
            <option value="COMPLETED">مكتمل</option>
            <option value="ON_HOLD">معلق</option>
            <option value="CANCELLED">ملغي</option>
          </select>
        </div>
        <div className="col-md-2">
          <select
            className="form-select"
            onChange={(e) =>
              handleFilterChange({ priority: e.target.value || undefined })
            }
          >
            <option value="">كل الأولويات</option>
            <option value="HIGH">عالية</option>
            <option value="MEDIUM">متوسطة</option>
            <option value="LOW">منخفضة</option>
          </select>
        </div>
        <div className="col-md-4">
          <button className="btn btn-primary w-100">
            <i className="fas fa-plus ms-2"></i>
            إضافة مشروع جديد
          </button>
        </div>
      </div>

      <div className="row g-4 mb-4">
        {projectsData?.items.map((project: Project) => (
          <div key={project.id} className="col-md-6 col-lg-4">
            <ProjectCard
              project={project}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          </div>
        ))}
      </div>

      {projectsData && projectsData.total > (filters.limit || 12) && (
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

      {projectsData?.items.length === 0 && (
        <div className="row">
          <div className="col-12">
            <div className="card text-center py-5">
              <div className="card-body">
                <i className="fas fa-project-diagram fa-4x text-muted mb-3"></i>
                <h5>لا توجد مشاريع</h5>
                <p className="text-muted">
                  {filters.search || filters.status || filters.priority
                    ? 'لم يتم العثور على نتائج مطابقة للفلاتر المحددة'
                    : 'ابدأ بإضافة مشروع جديد إلى النظام'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Projects;
