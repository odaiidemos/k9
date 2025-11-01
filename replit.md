# K9 Operations Management System

## Overview
This project is a comprehensive, web-based, and mobile-first K9 operations management system designed for military and police canine units, featuring Arabic RTL compatibility. Its core purpose is to manage the entire lifecycle of K9s, including employee supervision, project management, training, veterinary care, breeding, and operational missions. The system aims to streamline operations, enhance efficiency, and provide robust tracking and reporting for critical canine unit functions, supporting optimized K9 deployment and resource utilization.

## User Preferences
Preferred communication style: Simple, everyday language.

## Migration to Modern Stack (In Progress - October 2025)

### Migration Overview
The system is being migrated from Flask to FastAPI (backend) and React+TypeScript (frontend) while maintaining all functionality and Arabic RTL support.

### Migration Status
**Phase 1: Core Backend Infrastructure (✅ COMPLETED - October 28, 2025)**

**Completed:**
- ✅ FastAPI project structure created (`backend_fastapi/`)
- ✅ Configuration system with environment variables
- ✅ JWT authentication and security module (access + refresh tokens)
- ✅ Redis client for caching
- ✅ Database session management (sync and async)
- ✅ Authentication services and endpoints (tested and working)
- ✅ Audit logging service (with SECURITY_EVENT tracking)
- ✅ RBAC dependencies for role-based access control
- ✅ Pydantic schemas for all entities (comprehensive schema library)
- ✅ **Shared SQLAlchemy Layer**: Created framework-agnostic `k9_shared/db.py` module
- ✅ **Refactored 27+ files**: All models now import from shared db instance
- ✅ **Dual Framework Operation**: Flask (port 5000) and FastAPI (port 8000) running concurrently
- ✅ **Database Integration**: Both frameworks successfully querying shared PostgreSQL database
- ✅ **Authentication Working**: JWT login endpoint tested with successful token generation

**Architecture Achievement:**
Successfully implemented shared SQLAlchemy layer that:
1. ✅ Eliminates import conflicts between Flask and FastAPI
2. ✅ Maintains single source of truth for all database models
3. ✅ Enables both frameworks to run concurrently without conflicts
4. ✅ Prevents schema drift during migration
5. ✅ Allows gradual feature migration without downtime

**Technical Details:**
- **Shared Module**: `k9_shared/db.py` provides framework-agnostic SQLAlchemy instance
- **Files Refactored**: Updated `app.py` + 3 model files + 23 service/route files
- **Bug Fixes**: Corrected attribute names (`account_locked_until`, `created_at`) in FastAPI services
- **Database Setup**: Ran all Flask migrations successfully, created 40+ tables
- **Test User**: Admin account created and tested (username: admin)

**Phase 2: React Frontend & Authentication (✅ COMPLETED - October 29, 2025)**

**Completed:**
- ✅ React + TypeScript + Vite frontend setup (`k9-frontend/`)
- ✅ Bootstrap 5 RTL integration with Arabic font support (Noto Sans Arabic)
- ✅ Redux Toolkit for global state management
- ✅ React Query for server state management and API caching
- ✅ Axios API client with JWT token handling and automatic refresh
- ✅ Authentication components (Login, Password Reset) with full RTL support
- ✅ Protected routes and authorization logic
- ✅ MFA (Multi-Factor Authentication) flow with improved UX
- ✅ **Critical Security Fixes**:
  - Migrated from localStorage to sessionStorage (reduces XSS exposure)
  - Fixed refresh interceptor to properly update Redux state
  - Implemented real password reset API integration with Flask backend
  - Added TODO for migrating to httpOnly cookies in production
- ✅ Comprehensive error handling and loading states
- ✅ Vite dev server configured on port 3000 (proxy to FastAPI on 8000)

**Technical Details:**
- **Frontend Stack**: React 19 + TypeScript 5.9 + Vite 7.1
- **State Management**: Redux Toolkit with typed hooks
- **API Layer**: React Query + Axios with automatic token refresh
- **Styling**: Bootstrap 5.3 RTL + Custom SCSS + Font Awesome 7.1
- **Security**: SessionStorage for tokens (interim solution until httpOnly cookies), CSRF protection, input validation
- **Authentication Flow**: JWT-based with MFA support, locked credentials during MFA step, cancel/retry logic

**Phase 3: Handler Daily System Backend (✅ COMPLETED - October 30, 2025)**

**Completed:**
- ✅ Comprehensive Pydantic schemas for Handler Daily System (schedules, reports, notifications)
- ✅ Daily schedule management API endpoints (create, list, get, update, lock)
- ✅ Schedule item management (handler assignments)
- ✅ Handler report CRUD operations with full workflow support
- ✅ Report submission and approval/rejection endpoints
- ✅ Notification management (list, mark read, mark all read, unread count)
- ✅ **Comprehensive Security Implementation** (verified through multiple architect reviews):
  - ✅ **Schedule Management (5 endpoints)**: Project-scoped for PROJECT_MANAGER, assignment-scoped for HANDLER
  - ✅ **Schedule Items (2 endpoints)**: Project-scoped with locked schedule enforcement
  - ✅ **Handler Reports (6 endpoints)**: Full project isolation for all operations
  - ✅ **Notifications (4 endpoints)**: User-scoped with project-scoped creation
  - ✅ **Cross-Project Protection**: PROJECT_MANAGERs cannot access other projects' data
  - ✅ **Handler Self-Access**: HANDLERs can only view/edit their own assignments
  - ✅ **Schedule Locking**: Locked schedules are immutable for all roles
  - ✅ **Draft-Only Updates**: Report modifications restricted to draft status only
  - ✅ **Project-Scoped Notifications**: Notifications only sent to relevant project managers
  - ✅ **Audit Logging**: All critical operations logged for compliance
- ✅ Pagination and filtering support for all list endpoints
- ✅ Flask parity achieved: All security constraints match legacy implementation

**Technical Details:**
- **API Routes**: `/api/v1/handler-daily/*` with 17 fully-secured endpoints
- **Models Integrated**: DailySchedule, DailyScheduleItem, HandlerReport, HandlerReportHealth, HandlerReportTraining, HandlerReportCare, HandlerReportBehavior, HandlerReportIncident, HandlerReportAttachment, Notification
- **Permission Model**: Three-tier RBAC with strict project-level isolation
  - HANDLER: Own assignments/schedules/reports only
  - PROJECT_MANAGER: Assigned project only (all operations)
  - GENERAL_ADMIN: Full system access
- **Workflow**: Draft → Submitted → Approved/Rejected with project-scoped notifications
- **Security Validation**: Multiple architect reviews confirmed no RBAC vulnerabilities

**Phase 4: Core CRUD React Pages (✅ COMPLETED - October 30, 2025)**

**Completed:**
- ✅ Dogs CRUD page with full create/edit modal integration
- ✅ Employees CRUD page with full create/edit modal integration
- ✅ Projects CRUD page with full create/edit modal integration
- ✅ **Critical Bug Fixes**:
  - Fixed EmployeeFormModal to preserve `is_active` status (was incorrectly reactivating inactive employees)
  - Added error handling and user feedback to all CRUD modals
  - Proper state management for checkbox fields
- ✅ **Architect Approved**: All CRUD modals validated for data integrity and error handling
- ✅ Both Flask (5000) and FastAPI (8000) backends running concurrently
- ✅ React Query hooks for data fetching with automatic cache invalidation
- ✅ Bootstrap 5 RTL modal components with Arabic labels

**Technical Details:**
- **Components**: DogFormModal, EmployeeFormModal, ProjectFormModal with full validation
- **API Integration**: useCreateDog/useUpdateDog hooks and similar for Employees/Projects
- **Error Handling**: Try/catch with user-friendly Arabic error messages
- **State Management**: Proper form state with is_active preservation for employees

**Phase 5: Handler Daily System React Pages (✅ COMPLETED - November 1, 2025)**

**Completed:**
- ✅ TypeScript types for Handler Daily System (schedules, reports, notifications, all enums)
- ✅ API services for schedules (create, list, get, update, lock, schedule items)
- ✅ API services for reports (create, list, get, update, submit, approve, reject)
- ✅ API services for notifications (list, mark read, mark all read, unread count)
- ✅ Handler Dashboard page with stats, today's schedule, recent reports, and notifications
- ✅ Supervisor Dashboard page with pending reports review and schedule management
- ✅ Routes added to AppRouter for /handler/dashboard and /supervisor/dashboard
- ✅ Full Arabic RTL support maintained

**Technical Details:**
- **Handler Dashboard Features**: Stats cards (total, approved, pending, this month), today's schedule display, recent reports table, real-time notifications panel
- **Supervisor Dashboard Features**: Report review stats (total, pending, approved, rejected), pending reports table with approve/reject actions, recent schedules list
- **API Integration**: React Query for data fetching and caching, Axios interceptors for JWT auth
- **UI Components**: Bootstrap 5 RTL cards, tables, badges with Font Awesome icons

**Phase 6: Breeding Management React Pages (✅ COMPLETED - November 1, 2025)**

**Completed:**
- ✅ TypeScript types for breeding management (feeding, checkup, veterinary, caretaker logs)
- ✅ All enums: BodyConditionScale, PrepMethod, VeterinaryVisitType, VeterinaryPriority
- ✅ API services:
  - `feedingService` - Daily/weekly/unified reports with PDF export
  - `checkupService` - Daily/weekly/unified reports with PDF export
  - `veterinaryService` - Unified veterinary reports with PDF export
  - `caretakerService` - Unified daily care reports with PDF export
- ✅ Breeding Reports Dashboard (`/breeding/reports`)
  - Tabbed interface for 4 report types (feeding, checkup, veterinary, caretaker)
  - Smart date range selector (daily, weekly, monthly, custom)
  - Dynamic KPI cards showing aggregated statistics
  - Detailed data tables with pagination
  - PDF export functionality for all report types
- ✅ Full Arabic RTL support with Bootstrap 5 UI

**Technical Details:**
- **Report Types**: 4 comprehensive breeding/care reports with unified API
- **Date Ranges**: Flexible range selector supporting daily, weekly, monthly, and custom periods
- **KPIs**: Dynamic statistics cards (total dogs, meals, weight, temperature, costs, incidents)
- **Data Visualization**: Detailed tables showing per-dog metrics and aggregations
- **Export**: One-click PDF export for all report types via FastAPI backend

**Phase 7: Training Reports React Pages (✅ COMPLETED - November 1, 2025)**

**Completed:**
- ✅ TypeScript types for training management
- ✅ All enums: TrainingSessionType, TrainingStatus, PerformanceRating
- ✅ API service: `trainingService` - Unified training reports with PDF export
- ✅ Training Reports Dashboard (`/training/reports`)
  - Smart date range selector (daily, weekly, monthly, custom)
  - Session type filter (obedience, detection, tracking, protection, agility, etc.)
  - KPI cards: total sessions, total dogs, total hours, average duration
  - Detailed table with performance ratings and session status
  - PDF export functionality
- ✅ Full Arabic RTL support with Bootstrap 5 UI

**Technical Details:**
- **Session Types**: 7 training types (Obedience, Detection, Tracking, Protection, Agility, Socialization, Other)
- **Performance Rating**: 5-level rating system (Excellent, Good, Average, Below Average, Poor) with color-coded badges
- **KPIs**: Session count, dog count, total training hours, average session duration
- **Filters**: Date range, project, trainer, dog, and session type filters

**Next Phase: Attendance Tracking React Pages and System Integration**

**Migration Architecture:**
- Flask (port 5000) - Legacy backend, being phased out
- FastAPI (port 8000) - New backend for API endpoints
- React (port 3000) - Modern SPA frontend
- Shared PostgreSQL database
- Shared SQLAlchemy models
- React frontend communicates with FastAPI via API proxy

## System Architecture

### UI/UX Decisions
- **UI Framework**: Bootstrap 5 RTL for comprehensive UI components with right-to-left language support.
- **Styling**: Custom CSS optimized for RTL layouts and comprehensive dark mode support with toggle.
- **Fonts**: Google Fonts, specifically Noto Sans Arabic, for appropriate Arabic text rendering.
- **Responsiveness**: Mobile-first design approach ensuring full responsiveness across all device types.

### Technical Implementations
- **Backend Framework**: Flask (Python) utilizing a modular Blueprint structure.
- **Database**: PostgreSQL, integrated via SQLAlchemy ORM.
- **Authentication**: Flask-Login implements session-based authentication and role-based access control with `GENERAL_ADMIN`, `PROJECT_MANAGER`, and `HANDLER` tiers.
- **Database Migrations**: Flask-Migrate, powered by Alembic, for schema versioning and management.
- **File Handling**: Local file system storage for uploads.
- **Security**: Incorporates CSRF protection, configurable session timeouts, input validation, and audit logging.
- **Database Backup & Restore**: Comprehensive backup/restore functionality using pg_dump/psql, automated scheduling via APScheduler, configurable retention, and an admin dashboard for management.

### Feature Specifications
- **Core Management**: Tracks K9 lifecycle, employee information, training records, veterinary care, and breeding production.
- **Project Operations**: Manages project lifecycle, resource allocation, incident logging, and performance evaluations.
- **Attendance System**: Comprehensive tracking with shift management, scheduling, project-specific recording, dual group tracking, leave management, and Arabic RTL PDF export. Includes an advanced Unified Matrix Attendance System with filtering, pagination, and multi-format export.
- **Ultra-Granular Permission System**: Provides `GENERAL_ADMIN` users with control over `PROJECT_MANAGER` access at a subsection level, featuring 79 distinct permission combinations, audit logging, and an intuitive admin dashboard.
- **Excel Export System**: Comprehensive XLSX export functionality for attendance reports and permissions data with Arabic RTL support, auto-formatted columns, and styled headers.
- **Modern Reporting Hub**: Centralized dashboard with dynamic statistics, categorized report organization (Attendance, Training, Breeding, Veterinary, Production, General), and integrated chart visualization.
- **Data Visualization Framework**: Chart.js integration with custom RTL-aware utilities for interactive charts across all reporting modules.
- **Handler Daily System**: Comprehensive daily operations management for K9 handlers featuring:
  - Daily schedule creation and management with auto-locking
  - Handler report submission with health checks, training logs, care tracking, behavior observations, and incident reporting
  - Configurable grace period for late report submissions (HANDLER_REPORT_GRACE_MINUTES)
  - Real-time notification system for schedule changes, report approvals/rejections
  - User management with bulk import from Excel/CSV
  - Automated cron jobs for schedule locking (23:59 daily) and notification cleanup (weekly)
  - **Enhanced Notification System**:
    - Direct links from notifications to specific reports/schedules
    - Pending reports counter in admin navigation menu
    - Separate notification pages for handlers (`/handler/notifications`) and admins (`/admin/notifications`)
    - Automatic notifications sent to project managers and admins when handlers submit reports
    - Real-time unread counters in navigation for all user roles

### System Design Choices
- **Client/Server Separation**: Clear distinction between frontend and backend.
- **Data Integrity**: Uses Enum-based status management.
- **Secure Identification**: UUID fields for object identification.
- **Flexible Data Storage**: JSON fields for metadata and audit logs.
- **Performance**: Optimized with database connection pooling and file size limits.
- **Scalability**: Modular architecture and role-based data isolation.

### Employee vs User/Handler Architecture
The system uses **two distinct but complementary concepts** for managing handlers:

**1. Employee Table (General Workforce Management)**
- **Purpose**: Manages ALL employees across the organization (handlers, vets, trainers, project managers, etc.)
- **Used by**: Attendance system, Project assignments, Training records, Veterinary records, Breeding/Production
- **Fields**: `employee_id` (badge number), `name`, `role` (HANDLER, VET, TRAINER, etc.)
- **Access**: Via `/employees` routes and Employee management pages
- **Shift Assignment**: Employees must be assigned to shifts via `/attendance/assignments` to appear in attendance dropdowns

**2. User Table with HANDLER Role (Authentication & Daily Operations)**
- **Purpose**: User accounts for handlers who need system access for daily reporting
- **Used by**: Handler Daily System (schedules, reports, notifications), Authentication/login
- **Fields**: `username`, `password_hash`, `full_name`, `role=HANDLER`
- **Access**: Via `/admin/users` and User management pages
- **Schedule Assignment**: Users are assigned to daily schedules via `/supervisor/schedules/create`

**Key Workflow:**
1. **For Attendance**: Create Employee record → Assign to shift via `/attendance/assignments` → Record attendance
2. **For Handler Daily Reports**: Create User account → Assign to daily schedule → Handler submits reports
3. **Optional**: Link Employee and User records via `user_account_id` field for integrated functionality

**Important Notes:**
- Attendance dropdowns only show employees **assigned to shifts** (not all employees)
- Daily schedule creation uses User accounts with HANDLER role
- These systems can work independently or be linked through the optional `user_account_id` field

## External Dependencies

### Python Packages
- **Flask Ecosystem**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate.
- **Security**: Werkzeug.
- **Database**: psycopg2-binary.
- **PDF Generation**: ReportLab.
- **Excel Export**: openpyxl.
- **Scheduling**: APScheduler.
- **Google API**: google-api-python-client (for future Google Drive integration).

### Frontend Dependencies
- **UI Framework**: Bootstrap 5 RTL.
- **Icon Library**: Font Awesome 6.
- **Fonts**: Google Fonts (Noto Sans Arabic).
- **Charting**: Chart.js.

### Database Requirements
- **Primary Database**: PostgreSQL (automatically configured for production and Replit environments).
- **UUID Compatibility**: Native UUID support for PostgreSQL, automatic string fallback for SQLite.
- **Connection Pooling**: Configured for production PostgreSQL.
- **Migration Support**: Flask-Migrate with Alembic.