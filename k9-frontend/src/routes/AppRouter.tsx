import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import Dashboard from '../pages/Dashboard';
import Dogs from '../pages/Dogs';
import Employees from '../pages/Employees';
import Projects from '../pages/Projects';
import Login from '../pages/Login';

const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="dogs" element={<Dogs />} />
          <Route path="employees" element={<Employees />} />
          <Route path="projects" element={<Projects />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
