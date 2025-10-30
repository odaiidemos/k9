import type { Employee } from '@/types/employee';

interface EmployeeCardProps {
  employee: Employee;
  onEdit: (employee: Employee) => void;
  onDelete: (employee: Employee) => void;
}

const EmployeeCard = ({ employee, onEdit, onDelete }: EmployeeCardProps) => {
  return (
    <div className="card h-100">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start mb-3">
          <h5 className="card-title mb-0">{employee.name}</h5>
          <span
            className={`badge ${
              employee.is_active ? 'bg-success' : 'bg-secondary'
            }`}
          >
            {employee.is_active ? 'نشط' : 'غير نشط'}
          </span>
        </div>

        <div className="mb-3">
          <p className="mb-2">
            <i className="fas fa-id-card ms-2 text-muted"></i>
            <strong>رقم الموظف:</strong> {employee.employee_id}
          </p>
          <p className="mb-2">
            <i className="fas fa-briefcase ms-2 text-muted"></i>
            <strong>الوظيفة:</strong> {employee.role}
          </p>
          {employee.phone && (
            <p className="mb-2">
              <i className="fas fa-phone ms-2 text-muted"></i>
              <strong>الهاتف:</strong> {employee.phone}
            </p>
          )}
          {employee.email && (
            <p className="mb-2">
              <i className="fas fa-envelope ms-2 text-muted"></i>
              <strong>البريد:</strong> {employee.email}
            </p>
          )}
          <p className="mb-2">
            <i className="fas fa-calendar ms-2 text-muted"></i>
            <strong>تاريخ التعيين:</strong>{' '}
            {new Date(employee.hire_date).toLocaleDateString('ar-EG')}
          </p>
        </div>

        {employee.certifications && employee.certifications.length > 0 && (
          <div className="mb-3">
            <p className="mb-1">
              <i className="fas fa-certificate ms-2 text-muted"></i>
              <strong>الشهادات:</strong>
            </p>
            <div className="ms-4">
              {employee.certifications.map((cert, index) => (
                <span key={index} className="badge bg-info ms-1">
                  {cert.name || `شهادة ${index + 1}`}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="d-flex gap-2 mt-3">
          <button
            className="btn btn-sm btn-outline-primary flex-fill"
            onClick={() => onEdit(employee)}
          >
            <i className="fas fa-edit ms-1"></i>
            تعديل
          </button>
          <button
            className="btn btn-sm btn-outline-danger flex-fill"
            onClick={() => onDelete(employee)}
          >
            <i className="fas fa-trash ms-1"></i>
            حذف
          </button>
        </div>
      </div>
    </div>
  );
};

export default EmployeeCard;
