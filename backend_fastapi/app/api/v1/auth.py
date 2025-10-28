"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from app.db.session import get_db
from app.services.auth_service import AuthenticationService
from app.core.dependencies import get_current_user, get_current_active_user
from app.models import User
from app.schemas.user import UserResponse

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6)
    mfa_token: Optional[str] = Field(None, description="MFA token if MFA is enabled")


class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
    mfa_required: bool = False


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Refresh token response schema"""
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens
    
    - **username**: User's username
    - **password**: User's password
    - **mfa_token**: Optional MFA token if MFA is enabled for the user
    """
    # Get client IP
    client_ip = request.client.host if request.client else None
    
    # Authenticate user
    success, user, message, tokens = AuthenticationService.authenticate_user(
        db=db,
        username=login_data.username,
        password=login_data.password,
        mfa_token=login_data.mfa_token,
        ip_address=client_ip
    )
    
    # Check if MFA is required
    if not success and message == "MFA_REQUIRED" and user:
        return LoginResponse(
            access_token="",
            refresh_token="",
            user=UserResponse.from_orm(user),
            mfa_required=True
        )
    
    if not success or not tokens or not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return LoginResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        user=UserResponse.from_orm(user),
        mfa_required=False
    )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Get a new access token using refresh token
    
    - **refresh_token**: Valid refresh token
    """
    success, new_access_token, message = AuthenticationService.refresh_access_token(
        db=db,
        refresh_token=refresh_data.refresh_token
    )
    
    if not success or not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return RefreshTokenResponse(
        access_token=new_access_token,
        token_type="bearer"
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Logout current user
    
    Note: With JWT tokens, logout is handled client-side by removing tokens.
    This endpoint is provided for audit logging purposes.
    """
    from app.services.audit_service import AuditService
    from app.models import AuditAction
    
    AuditService.log_audit(
        db=db,
        user_id=str(current_user.id),
        action=AuditAction.LOGOUT,
        target_type="User",
        target_id=str(current_user.id),
        details={"username": current_user.username}
    )
    
    return MessageResponse(
        message="تم تسجيل الخروج بنجاح",
        success=True
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current authenticated user information
    """
    return UserResponse.from_orm(current_user)


@router.get("/health")
async def health_check():
    """
    Health check endpoint for authentication service
    """
    return {
        "status": "healthy",
        "service": "authentication",
        "message": "Authentication service is running"
    }
