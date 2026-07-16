"""
Analytics schemas for request/response validation.
Defines Pydantic models for analytics endpoints.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class RevenueAnalyticsResponse(BaseModel):
    """Response schema for revenue analytics."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Revenue analytics data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Revenue analytics retrieved successfully",
                "data": {
                    "today": 5000.0,
                    "weekly": 35000.0,
                    "monthly": 150000.0,
                    "yearly": 1800000.0,
                    "total": 1800000.0
                }
            }
        }
    }


class ProfitAnalyticsResponse(BaseModel):
    """Response schema for profit analytics."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Profit analytics data")


class GrowthAnalyticsResponse(BaseModel):
    """Response schema for growth analytics."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Growth analytics data")


class BusinessHealthResponse(BaseModel):
    """Response schema for business health."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Business health data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Business health calculated successfully",
                "data": {
                    "score": 85,
                    "status": "Excellent",
                    "details": {
                        "revenue_growth": 15.5,
                        "profit_margin": 25.0,
                        "inventory_health": 90,
                        "sales_trend": "upward",
                        "low_stock_ratio": 0.05
                    },
                    "explanation": "Revenue is growing at 15.5% with healthy profit margins..."
                }
            }
        }
    }


class TopProductsResponse(BaseModel):
    """Response schema for top products."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: List[Dict[str, Any]] = Field(..., description="Top products data")


class CategoryAnalyticsResponse(BaseModel):
    """Response schema for category analytics."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Category analytics data")


class InventoryAnalyticsResponse(BaseModel):
    """Response schema for inventory analytics."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Inventory analytics data")


class KPIsResponse(BaseModel):
    """Response schema for KPIs."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="KPI data")


class TrendsResponse(BaseModel):
    """Response schema for trends."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Trend data")


class ReportResponse(BaseModel):
    """Response schema for AI-style report."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Report data")


class InsightsResponse(BaseModel):
    """Response schema for business insights."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: List[Dict[str, Any]] = Field(..., description="Business insights")