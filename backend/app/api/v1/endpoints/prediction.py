"""
Prediction endpoints for machine learning forecasting.
"""
from fastapi import APIRouter, Depends, status, Query
from typing import Optional

from app.services.prediction_service import prediction_service
from app.dependencies.auth import get_current_active_user
from app.schemas.auth import UserResponse
from app.core.exceptions import AppException
from app.schemas.prediction import (
    DemandPredictionRequest,
    RevenuePredictionRequest,
    ProfitPredictionRequest,
    PredictionResponse,
    ModelComparisonResponse
)

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predict", tags=["prediction"])


@router.post(
    "/demand",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict demand",
    description="Predict product demand using machine learning"
)
async def predict_demand(
    request: DemandPredictionRequest,
    current_user: UserResponse = Depends(get_current_active_user)
) -> PredictionResponse:
    """
    Predict demand for products.
    """
    try:
        result = await prediction_service.predict_demand(
            product_id=request.product_id,
            days=request.days,
            model=request.model
        )
        
        return PredictionResponse(
            success=True,
            message="Demand prediction completed successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Error in predict_demand: {str(e)}")
        raise


@router.post(
    "/revenue",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict revenue",
    description="Predict future revenue using machine learning"
)
async def predict_revenue(
    request: RevenuePredictionRequest,
    current_user: UserResponse = Depends(get_current_active_user)
) -> PredictionResponse:
    """
    Predict future revenue.
    """
    try:
        result = await prediction_service.predict_revenue(
            days=request.days,
            model=request.model
        )
        
        return PredictionResponse(
            success=True,
            message="Revenue prediction completed successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Error in predict_revenue: {str(e)}")
        raise


@router.post(
    "/profit",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict profit",
    description="Predict future profit using machine learning"
)
async def predict_profit(
    request: ProfitPredictionRequest,
    current_user: UserResponse = Depends(get_current_active_user)
) -> PredictionResponse:
    """
    Predict future profit.
    """
    try:
        result = await prediction_service.predict_profit(
            days=request.days,
            model=request.model
        )
        
        return PredictionResponse(
            success=True,
            message="Profit prediction completed successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Error in predict_profit: {str(e)}")
        raise


@router.get(
    "/inventory",
    status_code=status.HTTP_200_OK,
    summary="Get inventory forecast",
    description="Get inventory forecast including stock depletion dates"
)
async def get_inventory_forecast(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get inventory forecast.
    """
    try:
        result = await prediction_service.get_inventory_forecast()
        return {
            "success": True,
            "message": "Inventory forecast retrieved successfully",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_inventory_forecast: {str(e)}")
        raise


@router.get(
    "/seasonality",
    status_code=status.HTTP_200_OK,
    summary="Detect seasonality",
    description="Detect seasonality patterns in sales data"
)
async def detect_seasonality(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Detect seasonality in sales data.
    """
    try:
        result = await prediction_service.detect_seasonality()
        return {
            "success": True,
            "message": "Seasonality detection completed",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in detect_seasonality: {str(e)}")
        raise


@router.get(
    "/moving-average",
    status_code=status.HTTP_200_OK,
    summary="Get moving average",
    description="Calculate moving average of revenue"
)
async def get_moving_average(
    window: int = Query(7, ge=3, le=90, description="Window size for moving average"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Calculate moving average of revenue.
    """
    try:
        result = await prediction_service.get_moving_average(window)
        return {
            "success": True,
            "message": "Moving average calculated successfully",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in get_moving_average: {str(e)}")
        raise


@router.get(
    "/models/compare",
    status_code=status.HTTP_200_OK,
    summary="Compare models",
    description="Compare different forecasting models"
)
async def compare_models(
    days: int = Query(30, ge=7, le=90, description="Days to forecast"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Compare different forecasting models.
    """
    try:
        result = await prediction_service.compare_models(days)
        return {
            "success": True,
            "message": "Model comparison completed",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in compare_models: {str(e)}")
        raise


@router.get(
    "/models/evaluate",
    status_code=status.HTTP_200_OK,
    summary="Evaluate model",
    description="Evaluate a specific forecasting model"
)
async def evaluate_model(
    model_name: str = Query("prophet", description="Model name: prophet, arima, linear"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Evaluate a specific model.
    """
    try:
        result = await prediction_service.evaluate_model(model_name)
        return {
            "success": True,
            "message": f"Model '{model_name}' evaluated successfully",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in evaluate_model: {str(e)}")
        raise


@router.get(
    "/models",
    status_code=status.HTTP_200_OK,
    summary="List available models",
    description="List all available trained models"
)
async def list_models(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    List available models.
    """
    try:
        from app.ai.model_trainer import model_trainer
        models = model_trainer.list_models()
        return {
            "success": True,
            "message": "Models retrieved successfully",
            "data": {
                "models": models,
                "count": len(models)
            }
        }
    except Exception as e:
        logger.error(f"Error in list_models: {str(e)}")
        raise