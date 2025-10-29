import React from 'react';

const Employees: React.FC = () => {
  return (
    <div className="container-fluid py-4">
      <div className="row mb-4">
        <div className="col-12">
          <h1>
            <i className="fas fa-users me-2"></i>
            إدارة الموظفين
          </h1>
        </div>
      </div>

      <div className="row mb-3">
        <div className="col-12">
          <button className="btn btn-primary">
            <i className="fas fa-plus me-2"></i>
            إضافة موظف جديد
          </button>
        </div>
      </div>

      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">قائمة الموظفين</h5>
              <p className="text-muted">سيتم عرض قائمة الموظفين هنا</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Employees;
