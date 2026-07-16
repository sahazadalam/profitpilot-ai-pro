"""
API v1 initialization module.
Registers all endpoint routers for version 1 of the API.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    health, auth, products, sales, dashboard, analytics, 
    prediction, recommendation, intelligence, chat
)

# Create main v1 router
router = APIRouter(prefix="/api/v1")

# Include endpoint routers
router.include_router(health.router)
router.include_router(auth.router)
router.include_router(products.router)
router.include_router(sales.router)
router.include_router(dashboard.router)
router.include_router(analytics.router)
router.include_router(prediction.router)
router.include_router(recommendation.router)
router.include_router(intelligence.router)
router.include_router(chat.router)  # Add chat router

__all__ = ["router"]