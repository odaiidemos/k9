"""
Authentication service for handling login, MFA, and security
"""
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from app.models import User, AuditAction
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_mfa_token,
    get_password_hash,
)
from app.core.redis_client import redis_client
from app.services.audit_service import AuditService


class AccountLockoutService:
    """Handle account lockout logic"""
    
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 30
    
    @staticmethod
    def is_account_locked(user: User) -> bool:
        """Check if account is currently locked"""
        if not user.locked_until:
            return False
        return datetime.utcnow() < user.locked_until
    
    @staticmethod
    def get_lockout_time_remaining(user: User) -> int:
        """Get remaining lockout time in minutes"""
        if not user.locked_until:
            return 0
        delta = user.locked_until - datetime.utcnow()
        return max(0, int(delta.total_seconds() / 60))
    
    @staticmethod
    def increment_failed_attempts(user: User, db: Session) -> None:
        """Increment failed login attempts and lock if threshold reached"""
        user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
        
        if user.failed_login_attempts >= AccountLockoutService.MAX_FAILED_ATTEMPTS:
            from datetime import timedelta
            user.locked_until = datetime.utcnow() + timedelta(
                minutes=AccountLockoutService.LOCKOUT_DURATION_MINUTES
            )
        
        db.commit()
    
    @staticmethod
    def reset_failed_attempts(user: User, db: Session) -> None:
        """Reset failed attempts counter"""
        user.failed_login_attempts = 0
        user.locked_until = None
        db.commit()


class AuthenticationService:
    """Handle authentication logic"""
    
    @staticmethod
    def authenticate_user(
        db: Session,
        username: str,
        password: str,
        mfa_token: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Tuple[bool, Optional[User], str, Optional[Dict[str, str]]]:
        """
        Authenticate user with username, password, and optional MFA
        
        Returns:
            (success, user, message, tokens)
        """
        # Find user
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False, None, "اسم المستخدم أو كلمة المرور غير صحيحة", None
        
        # Check if account is locked
        if AccountLockoutService.is_account_locked(user):
            remaining = AccountLockoutService.get_lockout_time_remaining(user)
            AuditService.log_security_event(
                db, user.id, "LOCKED_ACCOUNT_ACCESS_ATTEMPT",
                {"username": username, "ip": ip_address}
            )
            return False, None, f"الحساب مؤقت لمدة {remaining} دقيقة بسبب محاولات دخول فاشلة متكررة", None
        
        # Verify password
        if not user.is_active or not check_password_hash(user.password_hash, password):
            AccountLockoutService.increment_failed_attempts(user, db)
            AuditService.log_security_event(
                db, user.id, "FAILED_LOGIN_ATTEMPT",
                {"username": username, "ip": ip_address, "attempts": user.failed_login_attempts}
            )
            return False, None, "اسم المستخدم أو كلمة المرور غير صحيحة", None
        
        # Check MFA if enabled
        if user.mfa_enabled:
            if not mfa_token:
                return False, user, "MFA_REQUIRED", None
            
            # Verify MFA token
            mfa_valid = False
            if mfa_token.startswith("backup-"):
                # Backup code verification
                backup_code = mfa_token[7:]
                from app.core.security import verify_backup_code
                mfa_valid, new_codes = verify_backup_code(user.backup_codes or [], backup_code)
                if mfa_valid:
                    user.backup_codes = new_codes
                    db.commit()
                    AuditService.log_security_event(
                        db, user.id, "BACKUP_CODE_USED", {"username": username}
                    )
            else:
                # TOTP verification
                if user.mfa_secret:
                    mfa_valid = verify_mfa_token(user.mfa_secret, mfa_token)
            
            if not mfa_valid:
                AccountLockoutService.increment_failed_attempts(user, db)
                AuditService.log_security_event(
                    db, user.id, "FAILED_MFA_ATTEMPT",
                    {"username": username, "ip": ip_address}
                )
                return False, None, "رمز المصادقة الثنائية غير صحيح", None
        
        # Successful login
        AccountLockoutService.reset_failed_attempts(user, db)
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Generate tokens
        access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        # Log successful login
        AuditService.log_audit(
            db, user.id, AuditAction.LOGIN, "User", str(user.id),
            {"username": username}
        )
        AuditService.log_security_event(
            db, user.id, "SUCCESSFUL_LOGIN",
            {"username": username, "ip": ip_address, "mfa_used": user.mfa_enabled}
        )
        
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        
        return True, user, "تم تسجيل الدخول بنجاح", tokens
    
    @staticmethod
    def refresh_access_token(
        db: Session,
        refresh_token: str
    ) -> Tuple[bool, Optional[str], str]:
        """
        Generate new access token from refresh token
        
        Returns:
            (success, new_access_token, message)
        """
        from app.core.security import decode_token
        
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return False, None, "Invalid refresh token"
        
        user_id = payload.get("sub")
        if not user_id:
            return False, None, "Invalid token payload"
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            return False, None, "User not found or inactive"
        
        # Generate new access token
        new_access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.value}
        )
        
        return True, new_access_token, "Token refreshed successfully"


def verify_backup_code(backup_codes: list, code: str) -> Tuple[bool, list]:
    """Verify backup code and remove it from the list"""
    if code in backup_codes:
        new_codes = [c for c in backup_codes if c != code]
        return True, new_codes
    return False, backup_codes
