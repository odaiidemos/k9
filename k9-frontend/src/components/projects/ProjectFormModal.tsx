import { useState, useEffect, FormEvent } from 'react';
import type { Project, ProjectCreate, ProjectUpdate, ProjectStatus } from '@/types/project';

interface ProjectFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: ProjectCreate | ProjectUpdate) => Promise<void>;
  project?: Project;
  isSubmitting: boolean;
}

const ProjectFormModal = ({ isOpen, onClose, onSubmit, project, isSubmitting }: ProjectFormModalProps) => {
  const [formData, setFormData] = useState<ProjectCreate>({
    name: '',
    code: '',
    status: 'PLANNED' as ProjectStatus,
    start_date: new Date().toISOString().split('T')[0],
    priority: 'MEDIUM',
  });
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (project) {
      setFormData({
        name: project.name,
        code: project.code,
        main_task: project.main_task,
        description: project.description,
        status: project.status,
        start_date: project.start_date,
        end_date: project.end_date,
        expected_completion_date: project.expected_completion_date,
        location: project.location,
        mission_type: project.mission_type,
        priority: project.priority,
      });
    } else {
      setFormData({
        name: '',
        code: '',
        status: 'PLANNED' as ProjectStatus,
        start_date: new Date().toISOString().split('T')[0],
        priority: 'MEDIUM',
      });
    }
    setError('');
  }, [project, isOpen]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    
    try {
      await onSubmit(formData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'حدث خطأ أثناء حفظ البيانات');
      throw err;
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value || undefined
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }} onClick={onClose}>
      <div className="modal-dialog modal-lg modal-dialog-scrollable" onClick={(e) => e.stopPropagation()}>
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              <i className={`fas ${project ? 'fa-edit' : 'fa-plus'} ms-2`}></i>
              {project ? 'تعديل بيانات المشروع' : 'إضافة مشروع جديد'}
            </h5>
            <button type="button" className="btn-close" onClick={onClose} disabled={isSubmitting}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label">اسم المشروع <span className="text-danger">*</span></label>
                  <input
                    type="text"
                    className="form-control"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">الكود <span className="text-danger">*</span></label>
                  <input
                    type="text"
                    className="form-control"
                    name="code"
                    value={formData.code}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">الحالة <span className="text-danger">*</span></label>
                  <select
                    className="form-select"
                    name="status"
                    value={formData.status}
                    onChange={handleChange}
                    required
                  >
                    <option value="PLANNED">مخطط</option>
                    <option value="ACTIVE">نشط</option>
                    <option value="COMPLETED">مكتمل</option>
                    <option value="ON_HOLD">معلق</option>
                    <option value="CANCELLED">ملغي</option>
                  </select>
                </div>
                <div className="col-md-6">
                  <label className="form-label">الأولوية</label>
                  <select
                    className="form-select"
                    name="priority"
                    value={formData.priority}
                    onChange={handleChange}
                  >
                    <option value="HIGH">عالية</option>
                    <option value="MEDIUM">متوسطة</option>
                    <option value="LOW">منخفضة</option>
                  </select>
                </div>
                <div className="col-md-6">
                  <label className="form-label">تاريخ البدء <span className="text-danger">*</span></label>
                  <input
                    type="date"
                    className="form-control"
                    name="start_date"
                    value={formData.start_date}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">تاريخ الانتهاء</label>
                  <input
                    type="date"
                    className="form-control"
                    name="end_date"
                    value={formData.end_date || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">تاريخ الإنجاز المتوقع</label>
                  <input
                    type="date"
                    className="form-control"
                    name="expected_completion_date"
                    value={formData.expected_completion_date || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">الموقع</label>
                  <input
                    type="text"
                    className="form-control"
                    name="location"
                    value={formData.location || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">نوع المهمة</label>
                  <input
                    type="text"
                    className="form-control"
                    name="mission_type"
                    value={formData.mission_type || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">المهمة الرئيسية</label>
                  <input
                    type="text"
                    className="form-control"
                    name="main_task"
                    value={formData.main_task || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-12">
                  <label className="form-label">الوصف</label>
                  <textarea
                    className="form-control"
                    name="description"
                    rows={4}
                    value={formData.description || ''}
                    onChange={handleChange}
                  />
                </div>
                {error && (
                  <div className="col-12">
                    <div className="alert alert-danger mb-0">
                      <i className="fas fa-exclamation-circle ms-2"></i>
                      {error}
                    </div>
                  </div>
                )}
              </div>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={onClose}
                disabled={isSubmitting}
              >
                إلغاء
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <span className="spinner-border spinner-border-sm ms-2" role="status" aria-hidden="true"></span>
                    جاري الحفظ...
                  </>
                ) : (
                  <>
                    <i className="fas fa-save ms-2"></i>
                    حفظ
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProjectFormModal;
