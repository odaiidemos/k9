"""
Caching utilities for FastAPI application
"""
from app.core.redis_client import redis_client
from typing import Optional, Any, Callable
from functools import wraps
import json
import hashlib
import logging

logger = logging.getLogger(__name__)


def generate_cache_key(prefix: str, **kwargs) -> str:
    """
    Generate a consistent cache key from prefix and kwargs
    
    Args:
        prefix: Cache key prefix (e.g., "attendance_daily", "training_report")
        **kwargs: Parameters to include in the key
    
    Returns:
        Generated cache key string
    """
    # Sort kwargs for consistent key generation
    sorted_params = sorted(kwargs.items())
    param_str = json.dumps(sorted_params, sort_keys=True, default=str)
    param_hash = hashlib.md5(param_str.encode()).hexdigest()[:12]
    return f"{prefix}:{param_hash}"


def cache_response(prefix: str, expire: int = 300):
    """
    Decorator to cache FastAPI endpoint responses
    
    Args:
        prefix: Cache key prefix
        expire: Expiration time in seconds (default: 5 minutes)
    
    Usage:
        @cache_response("attendance_daily", expire=600)
        async def get_attendance_report(project_id: str, date: str):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function arguments
            cache_key = generate_cache_key(prefix, **kwargs)
            
            # Try to get cached response
            try:
                cached = redis_client.get_json(cache_key)
                if cached:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return cached
            except Exception as e:
                logger.warning(f"Cache get failed: {e}")
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache the result
            try:
                redis_client.set_json(cache_key, result, expire=expire)
                logger.debug(f"Cached response for key: {cache_key}")
            except Exception as e:
                logger.warning(f"Cache set failed: {e}")
            
            return result
        
        return wrapper
    return decorator


def invalidate_cache_pattern(pattern: str):
    """
    Invalidate all cache keys matching a pattern
    
    Args:
        pattern: Redis key pattern (e.g., "attendance_*", "training_report:*")
    """
    try:
        # Get Redis client
        client = redis_client._get_client()
        
        # Find all keys matching pattern
        keys = list(client.scan_iter(match=pattern))
        
        if keys:
            client.delete(*keys)
            logger.info(f"Invalidated {len(keys)} cache keys matching pattern: {pattern}")
    except Exception as e:
        logger.error(f"Cache invalidation failed for pattern {pattern}: {e}")


def invalidate_cache_key(key: str):
    """
    Invalidate a specific cache key
    
    Args:
        key: Cache key to invalidate
    """
    try:
        redis_client.delete(key)
        logger.debug(f"Invalidated cache key: {key}")
    except Exception as e:
        logger.error(f"Cache invalidation failed for key {key}: {e}")


class CacheManager:
    """
    Manager for cache invalidation on CRUD operations
    """
    
    @staticmethod
    def invalidate_attendance_reports(project_id: Optional[str] = None):
        """Invalidate attendance report caches"""
        if project_id:
            invalidate_cache_pattern(f"attendance_daily:*{project_id}*")
            invalidate_cache_pattern(f"pm_daily:*{project_id}*")
        else:
            invalidate_cache_pattern("attendance_daily:*")
            invalidate_cache_pattern("pm_daily:*")
    
    @staticmethod
    def invalidate_training_reports(project_id: Optional[str] = None):
        """Invalidate training report caches"""
        if project_id:
            invalidate_cache_pattern(f"training_daily:*{project_id}*")
        else:
            invalidate_cache_pattern("training_daily:*")
    
    @staticmethod
    def invalidate_feeding_reports(project_id: Optional[str] = None):
        """Invalidate feeding report caches"""
        if project_id:
            invalidate_cache_pattern(f"feeding_*:*{project_id}*")
        else:
            invalidate_cache_pattern("feeding_*:*")
    
    @staticmethod
    def invalidate_checkup_reports(project_id: Optional[str] = None):
        """Invalidate checkup report caches"""
        if project_id:
            invalidate_cache_pattern(f"checkup_*:*{project_id}*")
        else:
            invalidate_cache_pattern("checkup_*:*")
    
    @staticmethod
    def invalidate_veterinary_reports(project_id: Optional[str] = None):
        """Invalidate veterinary report caches"""
        if project_id:
            invalidate_cache_pattern(f"veterinary_*:*{project_id}*")
        else:
            invalidate_cache_pattern("veterinary_*:*")
    
    @staticmethod
    def invalidate_caretaker_reports(project_id: Optional[str] = None):
        """Invalidate caretaker report caches"""
        if project_id:
            invalidate_cache_pattern(f"caretaker_*:*{project_id}*")
        else:
            invalidate_cache_pattern("caretaker_*:*")
    
    @staticmethod
    def invalidate_all_reports():
        """Invalidate all report caches"""
        invalidate_cache_pattern("*_daily:*")
        invalidate_cache_pattern("*_report:*")
        invalidate_cache_pattern("feeding_*:*")
        invalidate_cache_pattern("checkup_*:*")
        invalidate_cache_pattern("veterinary_*:*")
        invalidate_cache_pattern("caretaker_*:*")
