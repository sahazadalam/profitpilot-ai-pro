"""
Intelligence endpoints for advanced AI intelligence.
"""
from fastapi import APIRouter, Depends, status, Query
from typing import Optional

from app.services.intelligence_service import intelligence_service
from app.dependencies.auth import get_current_active_user
from app.schemas.auth import UserResponse
from app.core.exceptions import AppException
from app.schemas.intelligence import SimulationRequest, ScenarioComparisonRequest

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/intelligence", tags=["intelligence"])


@router.get(
    "/customer-segments",
    status_code=status.HTTP_200_OK,
    summary="Get customer segments",
    description="AI-powered customer segmentation using K-Means clustering"
)
async def get_customer_segments(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get customer segments.
    """
    try:
        data = await intelligence_service.get_customer_segments()
        return {
            "success": True,
            "message": "Customer segments generated successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_customer_segments: {str(e)}")
        raise


@router.get(
    "/anomalies",
    status_code=status.HTTP_200_OK,
    summary="Detect sales anomalies",
    description="Detect sales anomalies using Isolation Forest, Z-Score, and IQR"
)
async def get_anomalies(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Detect sales anomalies.
    """
    try:
        data = await intelligence_service.get_anomalies()
        return {
            "success": True,
            "message": "Anomaly detection completed",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_anomalies: {str(e)}")
        raise


@router.post(
    "/simulate",
    status_code=status.HTTP_200_OK,
    summary="Simulate business scenario",
    description="What-if business simulation for price and stock changes"
)
async def simulate_scenario(
    request: SimulationRequest,
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Simulate a business scenario.
    """
    try:
        data = await intelligence_service.simulate_scenario(
            scenario_type=request.scenario_type,
            product_id=request.product_id,
            percentage=request.percentage,
            days=request.days
        )
        return {
            "success": True,
            "message": "Simulation completed successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in simulate_scenario: {str(e)}")
        raise


@router.get(
    "/explain",
    status_code=status.HTTP_200_OK,
    summary="Generate explainable AI insights",
    description="Generate human-readable explanations for AI predictions"
)
async def explain_intelligence(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate explainable AI insights.
    """
    try:
        data = await intelligence_service.explain_intelligence()
        return {
            "success": True,
            "message": "Explanation generated successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in explain_intelligence: {str(e)}")
        raise


@router.get(
    "/seasonality",
    status_code=status.HTTP_200_OK,
    summary="Detect seasonality",
    description="Detect seasonal patterns in sales data"
)
async def detect_seasonality(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Detect seasonality patterns.
    """
    try:
        data = await intelligence_service.detect_seasonality()
        return {
            "success": True,
            "message": "Seasonality detection completed",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in detect_seasonality: {str(e)}")
        raise


@router.get(
    "/market-trends",
    status_code=status.HTTP_200_OK,
    summary="Get market trends",
    description="Simulate market trends for different industries"
)
async def get_market_trends(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get market trend simulation.
    """
    try:
        data = await intelligence_service.get_market_trends()
        return {
            "success": True,
            "message": "Market trends generated successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_market_trends: {str(e)}")
        raise


@router.get(
    "/risk-prediction",
    status_code=status.HTTP_200_OK,
    summary="Predict business risks",
    description="Predict inventory, revenue, profit, and overall business risks"
)
async def predict_risks(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Predict business risks.
    """
    try:
        data = await intelligence_service.predict_risks()
        return {
            "success": True,
            "message": "Risk prediction completed",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in predict_risks: {str(e)}")
        raise


@router.get(
    "/insights",
    status_code=status.HTTP_200_OK,
    summary="Generate AI insights",
    description="Automatically generate positive, negative, and actionable insights"
)
async def generate_insights(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate AI insights.
    """
    try:
        data = await intelligence_service.generate_insights()
        return {
            "success": True,
            "message": "Insights generated successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in generate_insights: {str(e)}")
        raise


@router.post(
    "/compare-scenarios",
    status_code=status.HTTP_200_OK,
    summary="Compare business scenarios",
    description="Compare two business scenarios and recommend the better one"
)
async def compare_scenarios(
    request: ScenarioComparisonRequest,
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Compare business scenarios.
    """
    try:
        data = await intelligence_service.compare_scenarios(
            scenario_a=request.scenario_a,
            scenario_b=request.scenario_b,
            days=request.days
        )
        return {
            "success": True,
            "message": "Scenario comparison completed",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in compare_scenarios: {str(e)}")
        raise