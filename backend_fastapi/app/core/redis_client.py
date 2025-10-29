import redis
from backend_fastapi.app.core.config import settings
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self._client = None
    
    def _get_client(self):
        """Get or create Redis client connection (lazy initialization)"""
        if self._client is None:
            try:
                self._client = redis.from_url(settings.REDIS_URL, decode_responses=True)
                self._client.ping()
                logger.info("Redis connection established successfully")
            except Exception as e:
                logger.error(f"Failed to connect to Redis at {settings.REDIS_URL}: {e}")
                raise ConnectionError(f"Could not connect to Redis: {e}")
        return self._client
    
    def get(self, key: str) -> Optional[str]:
        """Get value from Redis"""
        return self._get_client().get(key)
    
    def set(self, key: str, value: str, expire: Optional[int] = None):
        """Set value in Redis with optional expiration (seconds)"""
        client = self._get_client()
        if expire:
            client.setex(key, expire, value)
        else:
            client.set(key, value)
    
    def delete(self, key: str):
        """Delete key from Redis"""
        self._get_client().delete(key)
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        return bool(self._get_client().exists(key))
    
    def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value from Redis"""
        value = self.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set_json(self, key: str, value: dict, expire: Optional[int] = None):
        """Set JSON value in Redis"""
        self.set(key, json.dumps(value), expire)
    
    def incr(self, key: str) -> int:
        """Increment counter"""
        return self._get_client().incr(key)
    
    def expire(self, key: str, seconds: int):
        """Set expiration on key"""
        self._get_client().expire(key, seconds)
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        try:
            if self._client is None:
                return False
            self._client.ping()
            return True
        except Exception:
            return False


# Global Redis client instance
redis_client = RedisClient()
