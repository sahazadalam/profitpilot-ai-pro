"""
Intelligence schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SimulationRequest(BaseModel):
    """Request schema for business simulation."""
    scenario_type: str = Field(..., description="Type: price_increase, price_decrease, stock_increase, stock_decrease")
    product_id: Optional[str] = Field(None, description="Product ID for product-specific simulation")
    percentage: float = Field(10.0, ge=1, le=50, description="Percentage change")
    days: int = Field(30, ge=7, le=365, description="Simulation period in days")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "scenario_type": "price_increase",
                "product_id": "507f1f77bcf86cd799439011",
                "percentage": 10,
                "days": 30
            }
        }
    }


class ScenarioComparisonRequest(BaseModel):
    """Request schema for scenario comparison."""
    scenario_a: Dict[str, Any] = Field(..., description="Scenario A parameters")
    scenario_b: Dict[str, Any] = Field(..., description="Scenario B parameters")
    days: int = Field(30, ge=7, le=365, description="Comparison period")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "scenario_a": {"price_change": 10, "stock_change": 0},
                "scenario_b": {"price_change": 0, "stock_change": 20},
                "days": 30
            }
        }
    }


class IntelligenceResponse(BaseModel):
    """Response schema for intelligence endpoints."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Intelligence data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "AI intelligence generated successfully",
                "data": {}
            }
        }
    }