"""
Database session management for FastAPI

This module provides database session management that's compatible with the
existing Flask application. We reuse the same database and models.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

# Get database URL from environment (same as Flask app)
database_url = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/k9_db")

# Ensure postgresql:// prefix for compatibility
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Create engine with connection pooling
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    echo=os.environ.get("ENVIRONMENT", "development") == "development"
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session in FastAPI endpoints
    
    Usage:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
