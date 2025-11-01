# K9 Operations Management System

## Overview
This project is a comprehensive, web-based, and mobile-first K9 operations management system designed for military and police canine units, featuring Arabic RTL compatibility. Its core purpose is to manage the entire lifecycle of K9s, including employee supervision, project management, training, veterinary care, breeding, and operational missions. The system aims to streamline operations, enhance efficiency, and provide robust tracking and reporting for critical canine unit functions, supporting optimized K9 deployment and resource utilization.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### UI/UX Decisions
- **UI Framework**: Bootstrap 5 RTL for comprehensive UI components with right-to-left language support.
- **Styling**: Custom CSS optimized for RTL layouts and comprehensive dark mode support with toggle.
- **Fonts**: Google Fonts, specifically Noto Sans Arabic, for appropriate Arabic text rendering.
- **Responsiveness**: Mobile-first design approach ensuring full responsiveness across all device types.

### Technical Implementations
- **Backend Framework**: FastAPI (Python) for new development, migrating from Flask. **Status: Core CRUD APIs running on port 8000** ✓
- **Frontend Framework**: React + TypeScript + Vite. **Status: Running on port 5000** ✓
- **Database**: PostgreSQL, integrated via SQLAlchemy ORM (shared layer for Flask/FastAPI). **Status: Provisioned and migrated** ✓
- **Authentication**: JWT authentication with Redis for caching, RBAC for role-based access control.
- **State Management (Frontend)**: Redux Toolkit for global state, React Query for server state.
- **API Client**: Axios with JWT token handling and automatic refresh.
- **Database Migrations**: Flask-Migrate (Alembic) for schema versioning.
- **File Handling**: Local file system storage for uploads.
- **Security**: CSRF protection, configurable session timeouts, input validation, audit logging, and migration to sessionStorage for tokens (with future httpOnly cookies).
- **Database Backup & Restore**: Comprehensive backup/restore functionality using pg_dump/psql, automated scheduling via APScheduler.

### Migration Status (Updated: Nov 1, 2025)
**✓ Backend Migration - Core Features Complete:**
- FastAPI server running on port 8000
- Working Routers: Authentication (JWT), Dogs, Employees, Projects, Handler Daily System, Training, Veterinary
- Health endpoint: http://localhost:8000/health
- API Documentation: http://localhost:8000/api/docs

**⚠️ Pending Work:**
- Report routers (Attendance, Training, Breeding) require refactoring due to Pydantic circular dependencies
- Frontend-to-backend integration testing
- Redis configuration for caching
- Full end-to-end testing of CRUD operations

**Admin Credentials:**
- Username: admin
- Password: admin123

### Feature Specifications
- **Core Management**: Tracks K9 lifecycle, employee information, training records, veterinary care, and breeding production.
- **Project Operations**: Manages project lifecycle, resource allocation, incident logging, and performance evaluations.
- **Attendance System**: Comprehensive tracking with shift management, scheduling, project-specific recording, dual group tracking, leave management, and Arabic RTL PDF export. Includes an advanced Unified Matrix Attendance System.
- **Ultra-Granular Permission System**: Provides `GENERAL_ADMIN` users with control over `PROJECT_MANAGER` access at a subsection level with 79 distinct permission combinations.
- **Excel Export System**: Comprehensive XLSX export functionality for attendance reports and permissions data with Arabic RTL support.
- **Modern Reporting Hub**: Centralized dashboard with dynamic statistics, categorized report organization (Attendance, Training, Breeding, Veterinary, Production, General), and integrated Chart.js visualization.
- **Handler Daily System**: Comprehensive daily operations management for K9 handlers featuring daily schedule creation, handler report submission (health, training, care, behavior, incident), configurable grace periods, real-time notification system with direct links, and user management with bulk import. Includes Handler and Supervisor dashboards.
- **Breeding Management**: Includes comprehensive breeding and care reports (feeding, checkup, veterinary, caretaker logs) with tabbed interface, dynamic KPIs, and PDF export.
- **Training Reports**: Features training reports dashboard with date range selector, session type filter, KPIs (total sessions, dogs, hours), and PDF export.

### System Design Choices
- **Client/Server Separation**: Clear distinction between frontend and backend with API proxy.
- **Data Integrity**: Uses Enum-based status management and UUIDs for object identification.
- **Flexible Data Storage**: JSON fields for metadata and audit logs.
- **Performance**: Optimized with database connection pooling and file size limits.
- **Scalability**: Modular architecture and role-based data isolation.
- **Employee vs User/Handler Architecture**: Distinct `Employee` table for general workforce management and `User` table with `HANDLER` role for system access and daily operations, with optional linking.

## External Dependencies

### Python Packages
- **FastAPI Ecosystem**: FastAPI, Uvicorn.
- **Flask Ecosystem (Legacy)**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate.
- **Database**: psycopg2-binary, SQLAlchemy.
- **Security**: Werkzeug, PyJWT.
- **Caching**: Redis.
- **PDF Generation**: ReportLab.
- **Excel Export**: openpyxl.
- **Scheduling**: APScheduler.
- **Google API**: google-api-python-client (for future Google Drive integration).

### Frontend Dependencies
- **UI Framework**: Bootstrap 5 RTL.
- **Icon Library**: Font Awesome 6.
- **Fonts**: Google Fonts (Noto Sans Arabic).
- **Charting**: Chart.js.
- **React Ecosystem**: React, TypeScript, Vite, Redux Toolkit, React Query, Axios.

### Database Requirements
- **Primary Database**: PostgreSQL.
- **Redis**: For caching and session management.