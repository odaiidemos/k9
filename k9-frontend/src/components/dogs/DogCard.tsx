import { Link } from 'react-router-dom';
import type { Dog } from '@/types/dog';

interface DogCardProps {
  dog: Dog;
  onEdit: (dog: Dog) => void;
  onDelete: (dog: Dog) => void;
}

const DogCard = ({ dog, onEdit, onDelete }: DogCardProps) => {
  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return 'bg-success';
      case 'TRAINING':
        return 'bg-primary';
      case 'RETIRED':
        return 'bg-secondary';
      case 'INJURED':
        return 'bg-warning';
      case 'DECEASED':
        return 'bg-dark';
      default:
        return 'bg-secondary';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return 'نشط';
      case 'TRAINING':
        return 'تحت التدريب';
      case 'RETIRED':
        return 'متقاعد';
      case 'INJURED':
        return 'مصاب';
      case 'DECEASED':
        return 'متوفى';
      default:
        return status;
    }
  };

  const getGenderIcon = (gender: string) => {
    return gender === 'MALE' ? 'fa-mars' : 'fa-venus';
  };

  const getGenderLabel = (gender: string) => {
    return gender === 'MALE' ? 'ذكر' : 'أنثى';
  };

  const calculateAge = (birthDate: string) => {
    const birth = new Date(birthDate);
    const today = new Date();
    const ageInMonths = (today.getFullYear() - birth.getFullYear()) * 12 + (today.getMonth() - birth.getMonth());
    const years = Math.floor(ageInMonths / 12);
    const months = ageInMonths % 12;
    return years > 0 ? `${years} سنة ${months > 0 ? `و ${months} شهر` : ''}` : `${months} شهر`;
  };

  return (
    <div className="card h-100 shadow-sm">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start mb-3">
          <div>
            <h5 className="card-title mb-1">
              <i className="fas fa-dog ms-2 text-primary"></i>
              {dog.name}
            </h5>
            <span className="badge bg-light text-dark">{dog.code}</span>
          </div>
          <span className={`badge ${getStatusBadgeClass(dog.current_status)}`}>
            {getStatusLabel(dog.current_status)}
          </span>
        </div>

        <div className="mb-3">
          <p className="mb-1">
            <i className="fas fa-paw ms-2 text-muted"></i>
            <strong>السلالة:</strong> {dog.breed}
          </p>
          {dog.family_line && (
            <p className="mb-1">
              <i className="fas fa-dna ms-2 text-muted"></i>
              <strong>السلسلة العائلية:</strong> {dog.family_line}
            </p>
          )}
          <p className="mb-1">
            <i className={`fas ${getGenderIcon(dog.gender)} ms-2 text-muted`}></i>
            <strong>الجنس:</strong> {getGenderLabel(dog.gender)}
          </p>
          <p className="mb-1">
            <i className="fas fa-birthday-cake ms-2 text-muted"></i>
            <strong>العمر:</strong> {calculateAge(dog.birth_date)}
          </p>
          {dog.specialization && (
            <p className="mb-1">
              <i className="fas fa-medal ms-2 text-muted"></i>
              <strong>التخصص:</strong> {dog.specialization}
            </p>
          )}
        </div>

        <div className="btn-group w-100" role="group">
          <Link to={`/dogs/${dog.id}`} className="btn btn-sm btn-outline-primary">
            <i className="fas fa-eye ms-2"></i>
            عرض
          </Link>
          <button
            type="button"
            className="btn btn-sm btn-outline-secondary"
            onClick={() => onEdit(dog)}
          >
            <i className="fas fa-edit ms-2"></i>
            تعديل
          </button>
          <button
            type="button"
            className="btn btn-sm btn-outline-danger"
            onClick={() => onDelete(dog)}
          >
            <i className="fas fa-trash ms-2"></i>
            حذف
          </button>
        </div>
      </div>
    </div>
  );
};

export default DogCard;
