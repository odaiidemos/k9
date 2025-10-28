"""
Shared SQLAlchemy database instance for K9 Operations Management System

This module provides a framework-agnostic SQLAlchemy instance that can be
used by both Flask and FastAPI applications, ensuring a single source of
truth for database models and preventing import conflicts.

Usage in Flask:
    from k9_shared.db import db
    db.init_app(app)

Usage in FastAPI:
    from k9_shared.db import Base, engine
    # Use Base and engine for session management
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass


# Create shared SQLAlchemy instance
db = SQLAlchemy(model_class=Base)

# Export commonly used attributes
__all__ = ['db', 'Base']
