"""
Dashboard schemas for response validation.
Defines Pydantic models for dashboard endpoints.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class DashboardSummaryResponse(BaseModel):
    """
    Response schema for dashboard summary.
    """
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: dict = Field(..., description="Dashboard summary data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Dashboard summary retrieved successfully",
                "data": {
                    "total_products": 150,
                    "total_sales": 1250,
                    "today_sales": 25,
                    "revenue": 150000.0,
                    "profit": 45000.0,
                    "inventory_value": 500000.0,
                    "out_of_stock": 5,
                    "low_stock": 15
                }
            }
        }
    }


class TopProductResponse(BaseModel):
    """
    Response schema for top products.
    """
    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    total_quantity_sold: int = Field(..., description="Total quantity sold")
    total_revenue: float = Field(..., description="Total revenue from this product")
    total_profit: float = Field(..., description="Total profit from this product")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": "507f1f77bcf86cd799439011",
                "product_name": "MacBook Pro 2024",
                "category": "Electronics",
                "total_quantity_sold": 50,
                "total_revenue": 124950.0,
                "total_profit": 24950.0
            }
        }
    }


class RevenueChartResponse(BaseModel):
    """
    Response schema for revenue chart data.
    """
    labels: List[str] = Field(..., description="Date labels")
    revenue: List[float] = Field(..., description="Revenue values")
    profit: List[float] = Field(..., description="Profit values")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "labels": ["2026-07-16", "2026-07-15", "2026-07-14"],
                "revenue": [5000.0, 4500.0, 6000.0],
                "profit": [1500.0, 1200.0, 1800.0]
            }
        }
    }


class ProfitSummaryResponse(BaseModel):
    """
    Response schema for profit summary.
    """
    daily: dict = Field(..., description="Daily profit")
    weekly: dict = Field(..., description="Weekly profit")
    monthly: dict = Field(..., description="Monthly profit")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "daily": {"profit": 1500.0, "revenue": 5000.0},
                "weekly": {"profit": 10500.0, "revenue": 35000.0},
                "monthly": {"profit": 45000.0, "revenue": 150000.0}
            }
        }
    }