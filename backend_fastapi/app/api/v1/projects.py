"""
Project CRUD endpoints for K9 Operations Management System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.core.dependencies import get_current_active_user
from app.models import User, Project, UserRole, AuditAction, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.common import PaginatedResponse
from app.services.audit_service import AuditService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ProjectResponse])
async def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[ProjectStatus] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
):
    """
    List all projects accessible to the current user with filtering and pagination
    
    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return
    - **status**: Filter by project status
    - **priority**: Filter by priority level
    - **search**: Search in name, code, or description
    """
    # Base query with user permissions
    query = db.query(Project)
    if current_user.role != UserRole.GENERAL_ADMIN:
        query = query.filter(Project.manager_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(Project.status == status)
    if priority:
        query = query.filter(Project.priority.ilike(f"%{priority}%"))
    if search:
        query = query.filter(
            or_(
                Project.name.ilike(f"%{search}%"),
                Project.code.ilike(f"%{search}%"),
                Project.description.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    projects = query.order_by(Project.start_date.desc()).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=[ProjectResponse.from_orm(project) for project in projects],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific project
    
    - **project_id**: UUID of the project
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المشروع غير موجود"
        )
    
    # Check permissions
    if current_user.role != UserRole.GENERAL_ADMIN and project.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بالوصول إلى بيانات هذا المشروع"
        )
    
    return ProjectResponse.from_orm(project)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new project record
    
    - **project_data**: Project creation data including name, code, dates, etc.
    """
    # Check if code already exists
    existing_project = db.query(Project).filter(Project.code == project_data.code).first()
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز المشروع موجود بالفعل في النظام"
        )
    
    # Set manager_id to current user if PROJECT_MANAGER
    if current_user.role == UserRole.PROJECT_MANAGER:
        project_data.manager_id = current_user.id
    
    # Create project instance
    project = Project(**project_data.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.CREATE,
        target_type="Project",
        target_id=str(project.id),
        details={
            "name": project.name,
            "code": project.code,
            "status": project.status.value
        }
    )
    
    return ProjectResponse.from_orm(project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing project record
    
    - **project_id**: UUID of the project to update
    - **project_data**: Updated project data (only provided fields will be updated)
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المشروع غير موجود"
        )
    
    # Check permissions
    if current_user.role != UserRole.GENERAL_ADMIN and project.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لك بتعديل بيانات هذا المشروع"
        )
    
    # Check for unique code if being updated
    if project_data.code and project_data.code != project.code:
        existing_project = db.query(Project).filter(Project.code == project_data.code).first()
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز المشروع موجود بالفعل في النظام"
            )
    
    # Update only provided fields
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    # Calculate duration if dates are set
    if project.start_date and project.end_date:
        project.duration_days = (project.end_date - project.start_date).days
    
    db.commit()
    db.refresh(project)
    
    # Log audit
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.UPDATE,
        target_type="Project",
        target_id=str(project.id),
        details={"updated_fields": list(update_data.keys())}
    )
    
    return ProjectResponse.from_orm(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a project record (GENERAL_ADMIN only)
    
    - **project_id**: UUID of the project to delete
    """
    if current_user.role != UserRole.GENERAL_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="يجب أن تكون مسؤول عام لحذف المشاريع"
        )
    
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المشروع غير موجود"
        )
    
    # Log audit before deletion
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.DELETE,
        target_type="Project",
        target_id=str(project.id),
        details={
            "name": project.name,
            "code": project.code,
            "status": project.status.value
        }
    )
    
    db.delete(project)
    db.commit()
    
    return None


@router.get("/stats/summary")
async def get_project_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get summary statistics about projects
    
    Returns counts by status and priority
    """
    # Base query with user permissions
    query = db.query(Project)
    if current_user.role != UserRole.GENERAL_ADMIN:
        query = query.filter(Project.manager_id == current_user.id)
    
    projects = query.all()
    
    # Calculate statistics
    total = len(projects)
    by_status = {}
    by_priority = {}
    
    for project in projects:
        # Count by status
        status_key = project.status.value if project.status else "UNKNOWN"
        by_status[status_key] = by_status.get(status_key, 0) + 1
        
        # Count by priority
        priority_key = project.priority or "UNKNOWN"
        by_priority[priority_key] = by_priority.get(priority_key, 0) + 1
    
    # Calculate average success rating
    rated_projects = [p for p in projects if p.success_rating is not None]
    avg_rating = sum(p.success_rating for p in rated_projects) / len(rated_projects) if rated_projects else 0
    
    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "average_success_rating": round(avg_rating, 2),
        "completed_projects": by_status.get("COMPLETED", 0)
    }
