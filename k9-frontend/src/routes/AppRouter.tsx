import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import Dashboard from '../pages/Dashboard';
import Dogs from '../pages/Dogs';
import Employees from '../pages/Employees';
import Projects from '../pages/Projects';
import Login from '../pages/Login';
import PasswordReset from '../pages/PasswordReset';
import HandlerDashboard from '../pages/handler/HandlerDashboard';
import SupervisorDashboard from '../pages/supervisor/SupervisorDashboard';
import BreedingReports from '../pages/breeding/BreedingReports';

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/password-reset" element={<PasswordReset />} />
        
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="dogs" element={<Dogs />} />
          <Route path="employees" element={<Employees />} />
          <Route path="projects" element={<Projects />} />
          <Route path="handler/dashboard" element={<HandlerDashboard />} />
          <Route path="supervisor/dashboard" element={<SupervisorDashboard />} />
          <Route path="breeding/reports" element={<BreedingReports />} />
        </Route>
        
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
