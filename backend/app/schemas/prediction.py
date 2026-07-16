"""
Prediction schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DemandPredictionRequest(BaseModel):
    """Request schema for demand prediction."""
    product_id: Optional[str] = Field(None, description="Product ID for specific product")
    category: Optional[str] = Field(None, description="Category for demand prediction")
    days: int = Field(30, ge=7, le=365, description="Number of days to forecast")
    model: Optional[str] = Field("prophet", description="Model to use: prophet, arima, linear")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": "507f1f77bcf86cd799439011",
                "days": 30,
                "model": "prophet"
            }
        }
    }


class RevenuePredictionRequest(BaseModel):
    """Request schema for revenue prediction."""
    days: int = Field(30, ge=7, le=365, description="Number of days to forecast")
    model: Optional[str] = Field("prophet", description="Model to use: prophet, arima, linear")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "days": 30,
                "model": "prophet"
            }
        }
    }


class ProfitPredictionRequest(BaseModel):
    """Request schema for profit prediction."""
    days: int = Field(30, ge=7, le=365, description="Number of days to forecast")
    model: Optional[str] = Field("prophet", description="Model to use: prophet, arima, linear")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "days": 30,
                "model": "prophet"
            }
        }
    }


class PredictionResponse(BaseModel):
    """Response schema for prediction."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Prediction data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Prediction completed successfully",
                "data": {
                    "forecast": [
                        {"date": "2026-07-16", "value": 150.0, "lower": 120.0, "upper": 180.0}
                    ],
                    "summary": {
                        "total": 4500.0,
                        "average": 150.0,
                        "trend": "upward"
                    },
                    "model": "prophet",
                    "metrics": {
                        "mae": 15.2,
                        "rmse": 20.5
                    }
                }
            }
        }
    }


class ModelComparisonResponse(BaseModel):
    """Response schema for model comparison."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Comparison data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Model comparison completed",
                "data": {
                    "models": {
                        "prophet": {
                            "mae": 12.5,
                            "rmse": 18.3,
                            "r2": 0.85,
                            "mape": 8.2
                        },
                        "arima": {
                            "mae": 15.2,
                            "rmse": 22.1,
                            "r2": 0.78,
                            "mape": 10.5
                        },
                        "linear": {
                            "mae": 20.1,
                            "rmse": 28.4,
                            "r2": 0.65,
                            "mape": 14.3
                        }
                    },
                    "best_model": "prophet"
                }
            }
        }
    }