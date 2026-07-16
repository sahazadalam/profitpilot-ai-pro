"""
Recommendation schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class RestockRecommendation(BaseModel):
    """Schema for restock recommendation."""
    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    current_stock: int = Field(..., description="Current stock quantity")
    recommended_quantity: int = Field(..., description="Recommended order quantity")
    recommended_date: str = Field(..., description="Recommended reorder date")
    priority: str = Field(..., description="Priority: high, medium, low")
    reason: str = Field(..., description="Reason for recommendation")
    days_until_depletion: int = Field(..., description="Days until stock runs out")


class PricingRecommendation(BaseModel):
    """Schema for pricing recommendation."""
    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    current_price: float = Field(..., description="Current selling price")
    suggested_price: float = Field(..., description="Suggested new price")
    action: str = Field(..., description="Action: increase, decrease, keep")
    expected_revenue: float = Field(..., description="Expected revenue after change")
    expected_profit: float = Field(..., description="Expected profit after change")
    reason: str = Field(..., description="Reason for recommendation")


class PerformanceScore(BaseModel):
    """Schema for product performance score."""
    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    score: int = Field(..., description="Performance score (0-100)")
    category: str = Field(..., description="Category")
    metrics: Dict[str, Any] = Field(..., description="Individual metrics")


class RecommendationResponse(BaseModel):
    """Response schema for recommendations."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Recommendation data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Recommendations generated successfully",
                "data": {
                    "recommendations": [],
                    "count": 0,
                    "generated_at": "2026-07-16T10:30:00"
                }
            }
        }
    }