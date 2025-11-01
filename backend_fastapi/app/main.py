from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.config import settings
from app.core.rate_limit import limiter
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Modern K9 Operations Management System API with JWT authentication",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": True}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "error": True
        }
    )


# Root endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/api/docs",
        "api": {
            "v1": {
                "auth": f"{settings.API_V1_PREFIX}/auth",
                "users": f"{settings.API_V1_PREFIX}/users",
                "dogs": f"{settings.API_V1_PREFIX}/dogs",
                "employees": f"{settings.API_V1_PREFIX}/employees",
                "projects": f"{settings.API_V1_PREFIX}/projects",
            }
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from app.db.session import engine
    from app.core.redis_client import redis_client
    
    # Check database
    from sqlalchemy import text
    db_status = "connected"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check Redis
    redis_status = "connected" if redis_client.is_connected() else "disconnected"
    
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "redis": redis_status,
    }


# Register API routers
logger.info("Registering API routers...")

# Authentication endpoints
from app.api.v1.auth import router as auth_router
app.include_router(
    auth_router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)
logger.info("✓ Authentication routes registered")

# Dog management endpoints
from app.api.v1.dogs import router as dogs_router
app.include_router(
    dogs_router,
    prefix=f"{settings.API_V1_PREFIX}/dogs",
    tags=["Dogs"]
)
logger.info("✓ Dog management routes registered")

# Employee management endpoints
from app.api.v1.employees import router as employees_router
app.include_router(
    employees_router,
    prefix=f"{settings.API_V1_PREFIX}/employees",
    tags=["Employees"]
)
logger.info("✓ Employee management routes registered")

# Project management endpoints
from app.api.v1.projects import router as projects_router
app.include_router(
    projects_router,
    prefix=f"{settings.API_V1_PREFIX}/projects",
    tags=["Projects"]
)
logger.info("✓ Project management routes registered")

# Handler Daily System endpoints
from app.api.v1.handler_daily import router as handler_daily_router
app.include_router(
    handler_daily_router,
    prefix=f"{settings.API_V1_PREFIX}/handler-daily",
    tags=["Handler Daily System"]
)
logger.info("✓ Handler Daily System routes registered")

# TODO: Report routers disabled temporarily due to Pydantic circular dependency issues
# These need to be refactored to avoid circular imports and recursion errors
# For now, the Flask app can still serve these reports via its existing blueprints

# # Attendance Reports endpoints
# from app.api.v1.attendance_reports import router as attendance_reports_router
# app.include_router(
#     attendance_reports_router,
#     prefix=f"{settings.API_V1_PREFIX}/reports/attendance",
#     tags=["Attendance Reports"]
# )
# logger.info("✓ Attendance Reports routes registered")

# # Training Reports endpoints
# from app.api.v1.training_reports import router as training_reports_router
# app.include_router(
#     training_reports_router,
#     prefix=f"{settings.API_V1_PREFIX}/reports/training",
#     tags=["Training Reports"]
# )
# logger.info("✓ Training Reports routes registered")

# # Breeding Reports endpoints (feeding, checkup, veterinary, caretaker)
# from app.api.v1.breeding_reports import router as breeding_reports_router
# app.include_router(
#     breeding_reports_router,
#     prefix=f"{settings.API_V1_PREFIX}/reports/breeding",
#     tags=["Breeding Reports"]
# )
# logger.info("✓ Breeding Reports routes registered")

# Training CRUD endpoints
from app.api.v1.training import router as training_router
app.include_router(
    training_router,
    prefix=f"{settings.API_V1_PREFIX}/training",
    tags=["Training Sessions"]
)
logger.info("✓ Training CRUD routes registered")

# Veterinary CRUD endpoints
from app.api.v1.veterinary import router as veterinary_router
app.include_router(
    veterinary_router,
    prefix=f"{settings.API_V1_PREFIX}/veterinary",
    tags=["Veterinary Visits"]
)
logger.info("✓ Veterinary CRUD routes registered")

logger.info(f"✓ K9 Operations FastAPI server initialized")
logger.info(f"✓ Environment: {settings.ENVIRONMENT}")
logger.info(f"✓ API Documentation: /api/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
