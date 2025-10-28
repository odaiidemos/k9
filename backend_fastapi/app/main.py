from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
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
    db_status = "connected"
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")  # type: ignore
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

# Additional routers will be added here as they are implemented
# from app.api.v1.users import router as users_router
# app.include_router(users_router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Users"])

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
