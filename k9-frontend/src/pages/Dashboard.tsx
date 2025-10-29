import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div className="container-fluid py-4">
      <div className="row">
        <div className="col-12">
          <h1 className="mb-4">
            <i className="fas fa-home me-2"></i>
            لوحة التحكم
          </h1>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-md-3">
          <div className="card text-bg-primary">
            <div className="card-body">
              <h5 className="card-title">
                <i className="fas fa-dog me-2"></i>
                الكلاب
              </h5>
              <p className="card-text display-6">--</p>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card text-bg-success">
            <div className="card-body">
              <h5 className="card-title">
                <i className="fas fa-users me-2"></i>
                الموظفين
              </h5>
              <p className="card-text display-6">--</p>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card text-bg-info">
            <div className="card-body">
              <h5 className="card-title">
                <i className="fas fa-project-diagram me-2"></i>
                المشاريع
              </h5>
              <p className="card-text display-6">--</p>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card text-bg-warning">
            <div className="card-body">
              <h5 className="card-title">
                <i className="fas fa-tasks me-2"></i>
                المهام
              </h5>
              <p className="card-text display-6">--</p>
            </div>
          </div>
        </div>
      </div>

      <div className="row mt-4">
        <div className="col-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">مرحباً بك في نظام إدارة عمليات الكلاب</h5>
              <p className="card-text">
                يمكنك الآن إدارة جميع عمليات الكلاب والموظفين والمشاريع من خلال هذا النظام.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
