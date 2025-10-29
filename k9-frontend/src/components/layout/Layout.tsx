import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

const Layout: React.FC = () => {
  return (
    <div className="d-flex flex-column min-vh-100">
      <Navbar />
      <main className="flex-grow-1 bg-light">
        <Outlet />
      </main>
      <footer className="bg-dark text-white py-3 text-center">
        <div className="container">
          <p className="mb-0">
            &copy; 2025 نظام إدارة عمليات الكلاب. جميع الحقوق محفوظة.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
