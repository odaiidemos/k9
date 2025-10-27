from typing import Generator, AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from backend_fastapi.config import settings
from backend_fastapi.database import get_async_db, get_sync_db

# Import existing User model from Flask app
from k9.models.models import User

# Security
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_sync_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    
    Args:
        current_user: Current user from get_current_user dependency
        
    Returns:
        User: Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def require_role(*roles):
    """
    Dependency to require specific user roles.
    
    Args:
        *roles: Variable number of UserRole enum values
        
    Returns:
        Callable dependency function
        
    Example:
        @app.get("/admin")
        async def admin_endpoint(user: User = Depends(require_role(UserRole.GENERAL_ADMIN))):
            ...
    """
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for async database session.
    Alias for get_async_db for convenience.
    """
    async for session in get_async_db():
        yield session


def get_sync_db_session() -> Generator[Session, None, None]:
    """
    Dependency for sync database session.
    Alias for get_sync_db for convenience.
    """
    yield from get_sync_db()
