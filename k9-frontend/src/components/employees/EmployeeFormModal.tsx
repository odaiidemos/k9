import { useState, useEffect, FormEvent } from 'react';
import type { Employee, EmployeeCreate, EmployeeUpdate, EmployeeRole } from '@/types/employee';

interface EmployeeFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: EmployeeCreate | EmployeeUpdate) => Promise<void>;
  employee?: Employee;
  isSubmitting: boolean;
}

const EmployeeFormModal = ({ isOpen, onClose, onSubmit, employee, isSubmitting }: EmployeeFormModalProps) => {
  const [formData, setFormData] = useState<EmployeeCreate & { is_active?: boolean }>({
    name: '',
    employee_id: '',
    role: 'سائس' as EmployeeRole,
    hire_date: new Date().toISOString().split('T')[0],
    is_active: true,
  });
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (employee) {
      setFormData({
        name: employee.name,
        employee_id: employee.employee_id,
        role: employee.role,
        phone: employee.phone,
        email: employee.email,
        hire_date: employee.hire_date,
        is_active: employee.is_active,
      });
    } else {
      setFormData({
        name: '',
        employee_id: '',
        role: 'سائس' as EmployeeRole,
        hire_date: new Date().toISOString().split('T')[0],
        is_active: true,
      });
    }
    setError('');
  }, [employee, isOpen]);

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({
        ...prev,
        [name]: checked
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value || undefined
      }));
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }} onClick={onClose}>
      <div className="modal-dialog modal-lg modal-dialog-scrollable" onClick={(e) => e.stopPropagation()}>
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              <i className={`fas ${employee ? 'fa-edit' : 'fa-plus'} ms-2`}></i>
              {employee ? 'تعديل بيانات الموظف' : 'إضافة موظف جديد'}
            </h5>
            <button type="button" className="btn-close" onClick={onClose} disabled={isSubmitting}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label">الاسم <span className="text-danger">*</span></label>
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
                  <label className="form-label">رقم الموظف <span className="text-danger">*</span></label>
                  <input
                    type="text"
                    className="form-control"
                    name="employee_id"
                    value={formData.employee_id}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">الدور <span className="text-danger">*</span></label>
                  <select
                    className="form-select"
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                    required
                  >
                    <option value="سائس">سائس</option>
                    <option value="مدرب">مدرب</option>
                    <option value="مربي">مربي</option>
                    <option value="طبيب">طبيب</option>
                    <option value="مسؤول مشروع">مسؤول مشروع</option>
                  </select>
                </div>
                <div className="col-md-6">
                  <label className="form-label">تاريخ التوظيف <span className="text-danger">*</span></label>
                  <input
                    type="date"
                    className="form-control"
                    name="hire_date"
                    value={formData.hire_date}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">الهاتف</label>
                  <input
                    type="tel"
                    className="form-control"
                    name="phone"
                    value={formData.phone || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">البريد الإلكتروني</label>
                  <input
                    type="email"
                    className="form-control"
                    name="email"
                    value={formData.email || ''}
                    onChange={handleChange}
                  />
                </div>
                {employee && (
                  <div className="col-12">
                    <div className="form-check">
                      <input
                        className="form-check-input"
                        type="checkbox"
                        name="is_active"
                        id="is_active"
                        checked={formData.is_active || false}
                        onChange={handleChange}
                      />
                      <label className="form-check-label" htmlFor="is_active">
                        نشط
                      </label>
                    </div>
                  </div>
                )}
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

export default EmployeeFormModal;
