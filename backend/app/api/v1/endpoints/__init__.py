"""
API v1 endpoints initialization module.
Exports all endpoint modules for version 1 of the API.
"""
from app.api.v1.endpoints import (
    health, auth, products, sales, dashboard, analytics, 
    prediction, recommendation, intelligence, chat
)

# Export all endpoint modules
__all__ = [
    "health", "auth", "products", "sales", "dashboard", 
    "analytics", "prediction", "recommendation", "intelligence", "chat"
]