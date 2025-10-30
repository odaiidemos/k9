import type { Project } from '@/types/project';

interface ProjectCardProps {
  project: Project;
  onEdit: (project: Project) => void;
  onDelete: (project: Project) => void;
}

const statusColors: Record<string, string> = {
  PLANNED: 'bg-secondary',
  ACTIVE: 'bg-success',
  COMPLETED: 'bg-primary',
  ON_HOLD: 'bg-warning',
  CANCELLED: 'bg-danger',
};

const statusLabels: Record<string, string> = {
  PLANNED: 'مخطط',
  ACTIVE: 'نشط',
  COMPLETED: 'مكتمل',
  ON_HOLD: 'معلق',
  CANCELLED: 'ملغي',
};

const priorityColors: Record<string, string> = {
  HIGH: 'text-danger',
  MEDIUM: 'text-warning',
  LOW: 'text-success',
};

const Project Card = ({ project, onEdit, onDelete }: ProjectCardProps) => {
  return (
    <div className="card h-100">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start mb-3">
          <h5 className="card-title mb-0">{project.name}</h5>
          <span className={`badge ${statusColors[project.status]}`}>
            {statusLabels[project.status]}
          </span>
        </div>

        <div className="mb-3">
          <p className="mb-2">
            <i className="fas fa-barcode ms-2 text-muted"></i>
            <strong>الكود:</strong> {project.code}
          </p>
          {project.main_task && (
            <p className="mb-2">
              <i className="fas fa-tasks ms-2 text-muted"></i>
              <strong>المهمة:</strong> {project.main_task}
            </p>
          )}
          <p className="mb-2">
            <i className="fas fa-calendar-alt ms-2 text-muted"></i>
            <strong>تاريخ البدء:</strong>{' '}
            {new Date(project.start_date).toLocaleDateString('ar-EG')}
          </p>
          {project.end_date && (
            <p className="mb-2">
              <i className="fas fa-calendar-check ms-2 text-muted"></i>
              <strong>تاريخ الانتهاء:</strong>{' '}
              {new Date(project.end_date).toLocaleDateString('ar-EG')}
            </p>
          )}
          {project.location && (
            <p className="mb-2">
              <i className="fas fa-map-marker-alt ms-2 text-muted"></i>
              <strong>الموقع:</strong> {project.location}
            </p>
          )}
          <p className="mb-2">
            <i
              className={`fas fa-exclamation-circle ms-2 ${
                priorityColors[project.priority] || 'text-muted'
              }`}
            ></i>
            <strong>الأولوية:</strong> {project.priority}
          </p>
          {project.duration_days !== undefined && (
            <p className="mb-2">
              <i className="fas fa-clock ms-2 text-muted"></i>
              <strong>المدة:</strong> {project.duration_days} يوم
            </p>
          )}
        </div>

        {project.description && (
          <p className="text-muted small mb-3">{project.description}</p>
        )}

        <div className="d-flex gap-2 mt-3">
          <button
            className="btn btn-sm btn-outline-primary flex-fill"
            onClick={() => onEdit(project)}
          >
            <i className="fas fa-edit ms-1"></i>
            تعديل
          </button>
          <button
            className="btn btn-sm btn-outline-danger flex-fill"
            onClick={() => onDelete(project)}
          >
            <i className="fas fa-trash ms-1"></i>
            حذف
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;
