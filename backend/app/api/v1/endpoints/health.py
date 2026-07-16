"""
Health check endpoints for ProfitPilot AI Pro.
Provides API status and service health monitoring.
"""
from fastapi import APIRouter, Depends, status
from datetime import datetime
import logging
from app.database.mongodb import MongoDB, get_database
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create router with prefix and tags
router = APIRouter(tags=["health"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Root endpoint",
    description="Welcome to ProfitPilot AI Pro API"
)
async def root():
    """
    Root endpoint returning welcome message and API information.
    
    Returns:
        dict: Welcome message with API details
    """
    return {
        "success": True,
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Check the health status of all services"
)
async def health_check(db: MongoDB = Depends(get_database)):
    """
    Comprehensive health check endpoint.
    Verifies database connectivity and overall system health.
    
    Args:
        db: MongoDB connection instance (injected)
        
    Returns:
        dict: Health status with service details
    """
    # Check database health
    db_status = "healthy"
    db_details = {}
    
    try:
        if db.db is not None:
            # Additional check: ping database
            await db.client.admin.command('ping')
            db_details = {
                "connected": True,
                "database": settings.MONGODB_DB_NAME
            }
        else:
            db_status = "unhealthy"
            db_details = {
                "connected": False,
                "error": "Database not connected"
            }
    except Exception as e:
        db_status = "unhealthy"
        db_details = {
            "connected": False,
            "error": str(e)
        }
        logger.error(f"Database health check failed: {str(e)}")
    
    # Determine overall system status
    overall_status = "healthy" if db_status == "healthy" else "unhealthy"
    
    return {
        "success": True,
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": {
                "status": "healthy",
                "version": settings.APP_VERSION,
                "environment": settings.ENVIRONMENT
            },
            "database": {
                "status": db_status,
                "details": db_details
            }
        }
    }


@router.get(
    "/ping",
    status_code=status.HTTP_200_OK,
    summary="Simple ping endpoint",
    description="Simple ping for basic connectivity check"
)
async def ping():
    """
    Simple ping endpoint for quick connectivity testing.
    
    Returns:
        dict: Pong response with timestamp
    """
    return {
        "success": True,
        "message": "pong",
        "timestamp": datetime.utcnow().isoformat()
    }