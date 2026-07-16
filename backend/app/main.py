"""
Main application module for ProfitPilot AI Pro.
Initializes FastAPI application, configures middleware, and handles lifecycle events.
"""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    generic_exception_handler
)
from app.database.mongodb import mongodb, get_database
from app.middleware.cors import setup_cors
from app.api.v1 import router as v1_router
from app.api.v1.endpoints import health

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info(f"Starting up {settings.APP_NAME}...")
    try:
        # Connect to MongoDB
        await mongodb.connect()
        logger.info("MongoDB connection established successfully")
    except Exception as e:
        logger.error(f"Failed to establish MongoDB connection: {str(e)}")
        # Continue startup even if database connection fails (for graceful degradation)
        # The health check will report the issue
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}...")
    try:
        # Disconnect from MongoDB
        await mongodb.disconnect()
        logger.info("MongoDB connection closed successfully")
    except Exception as e:
        logger.error(f"Error during MongoDB disconnection: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Autonomous Business Intelligence & Decision Platform",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Setup CORS
setup_cors(app)
logger.info("CORS configured successfully")

# Add exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation errors.
    
    Args:
        request: FastAPI request object
        exc: Validation exception
        
    Returns:
        JSONResponse: Structured error response
    """
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "message": "Validation error",
                "code": "VALIDATION_ERROR",
                "status_code": 422,
                "details": exc.errors()
            }
        }
    )


# Include API routers
app.include_router(v1_router)

# Include root endpoints (non-versioned)
app.include_router(health.router)


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )