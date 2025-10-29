import React from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          <i className="fas fa-paw me-2"></i>
          نظام إدارة عمليات الكلاب
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                <i className="fas fa-home me-1"></i>
                الرئيسية
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/dogs">
                <i className="fas fa-dog me-1"></i>
                الكلاب
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/employees">
                <i className="fas fa-users me-1"></i>
                الموظفين
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/projects">
                <i className="fas fa-project-diagram me-1"></i>
                المشاريع
              </Link>
            </li>
          </ul>
          <ul className="navbar-nav">
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                href="#"
                id="userDropdown"
                role="button"
                data-bs-toggle="dropdown"
              >
                <i className="fas fa-user me-1"></i>
                المستخدم
              </a>
              <ul className="dropdown-menu dropdown-menu-end">
                <li>
                  <Link className="dropdown-item" to="/profile">
                    <i className="fas fa-user-circle me-2"></i>
                    الملف الشخصي
                  </Link>
                </li>
                <li><hr className="dropdown-divider" /></li>
                <li>
                  <Link className="dropdown-item" to="/login">
                    <i className="fas fa-sign-out-alt me-2"></i>
                    تسجيل الخروج
                  </Link>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
