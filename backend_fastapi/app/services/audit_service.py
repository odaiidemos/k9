"""
Audit logging service
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import json

from app.models import AuditLog, AuditAction


class AuditService:
    """Handle audit logging operations"""
    
    @staticmethod
    def log_audit(
        db: Session,
        user_id: str,
        action: AuditAction,
        target_type: str,
        target_id: str,
        details: Optional[Dict[str, Any]] = None,
        target_name: Optional[str] = None
    ) -> AuditLog:
        """
        Log an audit event
        
        Args:
            db: Database session
            user_id: ID of user performing the action
            action: Type of action (CREATE, UPDATE, DELETE, etc.)
            target_type: Type of target (User, Dog, Employee, etc.)
            target_id: ID of the target
            details: Additional details as dictionary
            target_name: Optional name of the target
        
        Returns:
            Created AuditLog instance
        """
        log = AuditLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            target_name=target_name,
            description=json.dumps(details) if details else None,
            timestamp=datetime.utcnow()
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def log_security_event(
        db: Session,
        user_id: str,
        event_type: str,
        details: Dict[str, Any]
    ) -> AuditLog:
        """
        Log a security event
        
        Args:
            db: Database session
            user_id: ID of user involved
            event_type: Type of security event
            details: Event details
        
        Returns:
            Created AuditLog instance
        """
        details_copy = details.copy()
        details_copy['event_type'] = event_type
        
        return AuditService.log_audit(
            db=db,
            user_id=user_id,
            action=AuditAction.SECURITY_EVENT,
            target_type='SecurityEvent',
            target_id=user_id,
            details=details_copy
        )
    
    @staticmethod
    def log_export(
        db: Session,
        user_id: str,
        export_type: str,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """
        Log a data export event
        
        Args:
            db: Database session
            user_id: ID of user performing export
            export_type: Type of export (PDF, Excel, etc.)
            details: Export details
        
        Returns:
            Created AuditLog instance
        """
        export_details = details.copy() if details else {}
        export_details['export_type'] = export_type
        
        return AuditService.log_audit(
            db=db,
            user_id=user_id,
            action=AuditAction.EXPORT,
            target_type='Export',
            target_id=user_id,
            details=export_details
        )
    
    @staticmethod
    def get_user_activity(
        db: Session,
        user_id: str,
        limit: int = 50
    ) -> list[AuditLog]:
        """
        Get recent activity for a user
        
        Args:
            db: Database session
            user_id: ID of user
            limit: Maximum number of records to return
        
        Returns:
            List of AuditLog instances
        """
        return (
            db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_target_history(
        db: Session,
        target_type: str,
        target_id: str,
        limit: int = 50
    ) -> list[AuditLog]:
        """
        Get history for a specific target
        
        Args:
            db: Database session
            target_type: Type of target
            target_id: ID of target
            limit: Maximum number of records to return
        
        Returns:
            List of AuditLog instances
        """
        return (
            db.query(AuditLog)
            .filter(
                AuditLog.target_type == target_type,
                AuditLog.target_id == target_id
            )
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .all()
        )
