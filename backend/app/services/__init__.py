"""
Services module initialization.
Exports all service classes for business logic.
"""
from app.services.auth_service import auth_service
from app.services.product_service import product_service
from app.services.sales_service import sales_service
from app.services.dashboard_service import dashboard_service
from app.services.analytics_service import analytics_service

__all__ = [
    "auth_service",
    "product_service",
    "sales_service",
    "dashboard_service",
    "analytics_service"
]