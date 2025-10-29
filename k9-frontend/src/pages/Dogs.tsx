import React from 'react';

const Dogs: React.FC = () => {
  return (
    <div className="container-fluid py-4">
      <div className="row mb-4">
        <div className="col-12">
          <h1>
            <i className="fas fa-dog me-2"></i>
            إدارة الكلاب
          </h1>
        </div>
      </div>

      <div className="row mb-3">
        <div className="col-12">
          <button className="btn btn-primary">
            <i className="fas fa-plus me-2"></i>
            إضافة كلب جديد
          </button>
        </div>
      </div>

      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">قائمة الكلاب</h5>
              <p className="text-muted">سيتم عرض قائمة الكلاب هنا</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dogs;
