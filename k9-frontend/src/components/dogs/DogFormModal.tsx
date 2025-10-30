import { useState, useEffect, FormEvent } from 'react';
import { Dog, DogCreate, DogUpdate, DogStatus, DogGender } from '@/types/dog';

interface DogFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: DogCreate | DogUpdate) => Promise<void>;
  dog?: Dog;
  isSubmitting: boolean;
}

const DogFormModal = ({ isOpen, onClose, onSubmit, dog, isSubmitting }: DogFormModalProps) => {
  const [formData, setFormData] = useState<DogCreate>({
    name: '',
    code: '',
    breed: '',
    gender: 'MALE' as DogGender,
    birth_date: new Date().toISOString().split('T')[0],
    current_status: 'ACTIVE' as DogStatus,
  });
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (dog) {
      setFormData({
        name: dog.name,
        code: dog.code,
        breed: dog.breed,
        family_line: dog.family_line,
        gender: dog.gender,
        birth_date: dog.birth_date,
        microchip_id: dog.microchip_id,
        current_status: dog.current_status,
        location: dog.location,
        specialization: dog.specialization,
        color: dog.color,
        weight: dog.weight,
        height: dog.height,
      });
    } else {
      setFormData({
        name: '',
        code: '',
        breed: '',
        gender: 'MALE' as DogGender,
        birth_date: new Date().toISOString().split('T')[0],
        current_status: 'ACTIVE' as DogStatus,
      });
    }
    setError('');
  }, [dog, isOpen]);

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
      [name]: name === 'weight' || name === 'height' ? (value ? parseFloat(value) : undefined) : value || undefined
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }} onClick={onClose}>
      <div className="modal-dialog modal-lg modal-dialog-scrollable" onClick={(e) => e.stopPropagation()}>
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              <i className={`fas ${dog ? 'fa-edit' : 'fa-plus'} ms-2`}></i>
              {dog ? 'تعديل بيانات الكلب' : 'إضافة كلب جديد'}
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
                  <label className="form-label">السلالة <span className="text-danger">*</span></label>
                  <input
                    type="text"
                    className="form-control"
                    name="breed"
                    value={formData.breed}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">السلسلة العائلية</label>
                  <input
                    type="text"
                    className="form-control"
                    name="family_line"
                    value={formData.family_line || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">الجنس <span className="text-danger">*</span></label>
                  <select
                    className="form-select"
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    required
                  >
                    <option value="MALE">ذكر</option>
                    <option value="FEMALE">أنثى</option>
                  </select>
                </div>
                <div className="col-md-6">
                  <label className="form-label">تاريخ الميلاد <span className="text-danger">*</span></label>
                  <input
                    type="date"
                    className="form-control"
                    name="birth_date"
                    value={formData.birth_date}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">رقم الشريحة الإلكترونية</label>
                  <input
                    type="text"
                    className="form-control"
                    name="microchip_id"
                    value={formData.microchip_id || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">الحالة <span className="text-danger">*</span></label>
                  <select
                    className="form-select"
                    name="current_status"
                    value={formData.current_status}
                    onChange={handleChange}
                    required
                  >
                    <option value="ACTIVE">نشط</option>
                    <option value="TRAINING">تحت التدريب</option>
                    <option value="RETIRED">متقاعد</option>
                    <option value="INJURED">مصاب</option>
                    <option value="DECEASED">متوفى</option>
                  </select>
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
                  <label className="form-label">التخصص</label>
                  <input
                    type="text"
                    className="form-control"
                    name="specialization"
                    value={formData.specialization || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-4">
                  <label className="form-label">اللون</label>
                  <input
                    type="text"
                    className="form-control"
                    name="color"
                    value={formData.color || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-4">
                  <label className="form-label">الوزن (كجم)</label>
                  <input
                    type="number"
                    step="0.1"
                    className="form-control"
                    name="weight"
                    value={formData.weight || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-4">
                  <label className="form-label">الطول (سم)</label>
                  <input
                    type="number"
                    step="0.1"
                    className="form-control"
                    name="height"
                    value={formData.height || ''}
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

export default DogFormModal;
