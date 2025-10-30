"""
Rate limiting middleware using SlowAPI and Redis
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from app.core.redis_client import redis_client
from app.models import User, UserRole
import logging

logger = logging.getLogger(__name__)


def get_user_identifier(request: Request) -> str:
    """
    Get identifier for rate limiting based on user authentication
    
    - Authenticated users: use user ID
    - Unauthenticated users: use IP address
    """
    # Check if user is authenticated (from JWT token)
    if hasattr(request.state, "user") and request.state.user:
        user: User = request.state.user
        return f"user:{user.id}"
    
    # Fallback to IP address
    return get_remote_address(request)


def get_user_limit(request: Request) -> str:
    """
    Get rate limit string based on user role
    
    - General Admin / Project Manager: 240/minute
    - Regular users: 120/minute
    - Unauthenticated: 60/minute
    """
    if hasattr(request.state, "user") and request.state.user:
        user: User = request.state.user
        if user.role in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
            return "240/minute"
        return "120/minute"
    
    # Unauthenticated users get lower limit
    return "60/minute"


# Initialize limiter with Redis storage
limiter = Limiter(
    key_func=get_user_identifier,
    storage_uri=redis_client._get_client() if redis_client.is_connected() else None,
    default_limits=["120/minute"],  # Default limit
    headers_enabled=True  # Send rate limit info in response headers
)


# Rate limit presets for different endpoint types
class RateLimits:
    """Predefined rate limits for different endpoint types"""
    
    # General API endpoints
    STANDARD = "120/minute"
    ADMIN = "240/minute"
    
    # PDF export endpoints (more resource intensive)
    PDF_EXPORT = "20/minute"
    PDF_EXPORT_ADMIN = "40/minute"
    
    # CRUD operations
    CREATE = "60/minute"
    UPDATE = "100/minute"
    DELETE = "30/minute"
    
    # List/Read operations
    LIST = "180/minute"
    READ = "200/minute"


def dynamic_rate_limit(request: Request) -> str:
    """
    Dynamic rate limit based on user role and endpoint type
    Used with @limiter.limit(dynamic_rate_limit)
    """
    return get_user_limit(request)


def pdf_export_rate_limit(request: Request) -> str:
    """
    Rate limit for PDF export endpoints
    """
    if hasattr(request.state, "user") and request.state.user:
        user: User = request.state.user
        if user.role in [UserRole.GENERAL_ADMIN, UserRole.PROJECT_MANAGER]:
            return RateLimits.PDF_EXPORT_ADMIN
    
    return RateLimits.PDF_EXPORT
