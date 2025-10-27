import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "K9 Operations FastAPI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql://localhost/k9_operations")
    
    # JWT Settings
    SECRET_KEY: str = os.environ.get("SESSION_SECRET", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:5000", "http://localhost:8000", "http://127.0.0.1:5000", "http://127.0.0.1:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Redis Settings
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Celery Settings
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Security
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_DURATION_MINUTES: int = 30
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER: str = "uploads"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 25
    MAX_PAGE_SIZE: int = 100
    
    @property
    def database_url_async(self) -> str:
        """Convert sync database URL to async version for SQLAlchemy async engine"""
        url = self.DATABASE_URL
        
        # Remove sslmode parameter if present (asyncpg doesn't support it)
        if "?" in url and "sslmode=" in url:
            base_url, params = url.split("?", 1)
            # Filter out sslmode parameter
            params_list = [p for p in params.split("&") if not p.startswith("sslmode=")]
            if params_list:
                url = f"{base_url}?{'&'.join(params_list)}"
            else:
                url = base_url
        
        # Convert to asyncpg driver
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url
    
    @property
    def database_url_sync(self) -> str:
        """Ensure sync database URL has correct prefix"""
        if self.DATABASE_URL.startswith("postgres://"):
            return self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
        return self.DATABASE_URL


settings = Settings()
