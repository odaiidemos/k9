from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from backend_fastapi.config import settings

# Import existing SQLAlchemy models from Flask app
from app import db, Base

# Sync engine (for compatibility with existing Flask models)
sync_engine = create_engine(
    settings.database_url_sync,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG
)

# Async engine for FastAPI
# Note: asyncpg doesn't support connect_args like psycopg2, so we simplify the configuration
try:
    async_engine = create_async_engine(
        settings.database_url_async,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG,
        future=True
    )
except Exception as e:
    # Fallback: If async engine fails, log error and use None
    # This allows the app to start even if async DB isn't available
    import logging
    logging.error(f"Failed to create async engine: {e}")
    async_engine = None

# Session factories
if async_engine is not None:
    AsyncSessionLocal = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
else:
    AsyncSessionLocal = None

SyncSessionLocal = sessionmaker(
    sync_engine,
    class_=Session,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.
    Use this for async endpoints.
    """
    if AsyncSessionLocal is None:
        raise RuntimeError("Async database engine not initialized")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Generator[Session, None, None]:
    """
    Dependency for getting sync database session.
    Use this for compatibility with existing Flask SQLAlchemy models.
    """
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


async def init_db():
    """
    Initialize database tables.
    Note: In production, use Alembic migrations instead.
    """
    if async_engine is not None:
        async with async_engine.begin() as conn:
            # Don't create tables - use existing Flask migrations
            # await conn.run_sync(Base.metadata.create_all)
            pass


async def close_db():
    """Close database connections"""
    if async_engine is not None:
        await async_engine.dispose()
