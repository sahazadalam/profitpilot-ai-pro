"""
CORS middleware configuration for ProfitPilot AI Pro.
Handles Cross-Origin Resource Sharing settings.
"""
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


def setup_cors(app):
    """
    Configure CORS middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    # Use settings.CORS_ORIGINS directly (it's already a List[str])
    origins = settings.CORS_ORIGINS
    
    logger.info(f"Configuring CORS with origins: {origins}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
        expose_headers=["Content-Length", "X-Total-Count"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )