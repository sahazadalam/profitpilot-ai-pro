"""
Recommendation endpoints for AI-powered business recommendations.
"""
from fastapi import APIRouter, Depends, status
from typing import Optional

from app.services.recommendation_service import recommendation_service
from app.dependencies.auth import get_current_active_user
from app.schemas.auth import UserResponse
from app.core.exceptions import AppException

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommend", tags=["recommendation"])


@router.get(
    "/restock",
    status_code=status.HTTP_200_OK,
    summary="Get restock recommendations",
    description="AI-powered restock recommendations based on sales velocity and stock levels"
)
async def get_restock_recommendations(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get restock recommendations.
    """
    try:
        data = await recommendation_service.get_restock_recommendations()
        return {
            "success": True,
            "message": "Restock recommendations generated successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_restock_recommendations: {str(e)}")
        raise


@router.get(
    "/pricing",
    status_code=status.HTTP_200_OK,
    summary="Get pricing recommendations",
    description="AI-powered dynamic pricing recommendations"
)
async def get_pricing_recommendations(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get pricing recommendations.
    """
    try:
        data = await recommendation_service.get_pricing_recommendations()
        return {
            "success": True,
            "message": "Pricing recommendations generated successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_pricing_recommendations: {str(e)}")
        raise


@router.get(
    "/dead-stock",
    status_code=status.HTTP_200_OK,
    summary="Get dead stock products",
    description="Identify products with little or no sales"
)
async def get_dead_stock(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get dead stock products.
    """
    try:
        data = await recommendation_service.get_dead_stock()
        return {
            "success": True,
            "message": "Dead stock analysis completed",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_dead_stock: {str(e)}")
        raise


@router.get(
    "/loss-products",
    status_code=status.HTTP_200_OK,
    summary="Get loss-making products",
    description="Identify products that are reducing profit"
)
async def get_loss_products(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get loss-making products.
    """
    try:
        data = await recommendation_service.get_loss_products()
        return {
            "success": True,
            "message": "Loss products analysis completed",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_loss_products: {str(e)}")
        raise


@router.get(
    "/bundles",
    status_code=status.HTTP_200_OK,
    summary="Get bundle recommendations",
    description="Product bundle recommendations based on purchase patterns"
)
async def get_bundle_recommendations(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get bundle recommendations.
    """
    try:
        data = await recommendation_service.get_bundle_recommendations()
        return {
            "success": True,
            "message": "Bundle recommendations generated successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_bundle_recommendations: {str(e)}")
        raise


@router.get(
    "/performance",
    status_code=status.HTTP_200_OK,
    summary="Get product performance scores",
    description="Get performance scores (0-100) for all products"
)
async def get_performance_scores(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get product performance scores.
    """
    try:
        data = await recommendation_service.get_performance_scores()
        return {
            "success": True,
            "message": "Performance scores calculated successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_performance_scores: {str(e)}")
        raise


@router.get(
    "/business-risk",
    status_code=status.HTTP_200_OK,
    summary="Get business risk analysis",
    description="Calculate business risk score and provide recommendations"
)
async def get_business_risk(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get business risk analysis.
    """
    try:
        data = await recommendation_service.get_business_risk()
        return {
            "success": True,
            "message": "Business risk analysis completed",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_business_risk: {str(e)}")
        raise


@router.get(
    "/optimization",
    status_code=status.HTTP_200_OK,
    summary="Get optimization suggestions",
    description="AI-powered business optimization suggestions"
)
async def get_optimization_suggestions(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get optimization suggestions.
    """
    try:
        data = await recommendation_service.get_optimization_suggestions()
        return {
            "success": True,
            "message": "Optimization suggestions generated successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_optimization_suggestions: {str(e)}")
        raise


@router.get(
    "/executive-summary",
    status_code=status.HTTP_200_OK,
    summary="Get executive summary",
    description="AI-generated executive summary with key recommendations"
)
async def get_executive_summary(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get executive summary.
    """
    try:
        data = await recommendation_service.get_executive_summary()
        return {
            "success": True,
            "message": "Executive summary generated successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_executive_summary: {str(e)}")
        raise