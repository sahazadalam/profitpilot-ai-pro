"""
Analytics endpoints for business intelligence.
"""
from fastapi import APIRouter, Depends, status, Query
from typing import Optional

from app.services.analytics_service import analytics_service
from app.dependencies.auth import get_current_active_user
from app.schemas.auth import UserResponse
from app.core.exceptions import AppException

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/revenue",
    status_code=status.HTTP_200_OK,
    summary="Get revenue analytics",
    description="Get revenue analytics including today, weekly, monthly, yearly, and total"
)
async def get_revenue_analytics(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get revenue analytics.
    """
    try:
        data = await analytics_service.get_revenue_analytics()
        return {
            "success": True,
            "message": "Revenue analytics retrieved successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_revenue_analytics: {str(e)}")
        raise


@router.get(
    "/profit",
    status_code=status.HTTP_200_OK,
    summary="Get profit analytics",
    description="Get profit analytics including today, weekly, monthly, yearly, and total"
)
async def get_profit_analytics(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get profit analytics.
    """
    try:
        data = await analytics_service.get_profit_analytics()
        return {
            "success": True,
            "message": "Profit analytics retrieved successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_profit_analytics: {str(e)}")
        raise


@router.get(
    "/growth",
    status_code=status.HTTP_200_OK,
    summary="Get growth analytics",
    description="Get growth analytics including daily, weekly, and monthly growth rates"
)
async def get_growth_analytics(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get growth analytics.
    """
    try:
        data = await analytics_service.get_growth_analytics()
        return {
            "success": True,
            "message": "Growth analytics retrieved successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_growth_analytics: {str(e)}")
        raise


@router.get(
    "/business-health",
    status_code=status.HTTP_200_OK,
    summary="Get business health score",
    description="Get comprehensive business health score (0-100) with detailed explanation"
)
async def get_business_health(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get business health score.
    """
    try:
        data = await analytics_service.get_business_health()
        return {
            "success": True,
            "message": "Business health calculated successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_business_health: {str(e)}")
        raise


@router.get(
    "/top-products",
    status_code=status.HTTP_200_OK,
    summary="Get top products",
    description="Get top selling products by quantity, revenue, and profit"
)
async def get_top_products(
    limit: int = Query(10, ge=1, le=50, description="Number of products to return"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get top products.
    """
    try:
        data = await analytics_service.get_top_products(limit)
        return {
            "success": True,
            "message": "Top products retrieved successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_top_products: {str(e)}")
        raise


@router.get(
    "/worst-products",
    status_code=status.HTTP_200_OK,
    summary="Get worst products",
    description="Get worst selling products by quantity, revenue, and profit"
)
async def get_worst_products(
    limit: int = Query(10, ge=1, le=50, description="Number of products to return"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get worst products.
    """
    try:
        data = await analytics_service.get_worst_products(limit)
        return {
            "success": True,
            "message": "Worst products retrieved successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_worst_products: {str(e)}")
        raise


@router.get(
    "/category",
    status_code=status.HTTP_200_OK,
    summary="Get category analytics",
    description="Get revenue and profit analytics by category"
)
async def get_category_analytics(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get category analytics.
    """
    try:
        data = await analytics_service.get_category_analytics()
        return {
            "success": True,
            "message": "Category analytics retrieved successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_category_analytics: {str(e)}")
        raise


@router.get(
    "/inventory",
    status_code=status.HTTP_200_OK,
    summary="Get inventory analytics",
    description="Get inventory analytics including value, stock levels, and health"
)
async def get_inventory_analytics(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get inventory analytics.
    """
    try:
        data = await analytics_service.get_inventory_analytics()
        return {
            "success": True,
            "message": "Inventory analytics retrieved successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_inventory_analytics: {str(e)}")
        raise


@router.get(
    "/kpis",
    status_code=status.HTTP_200_OK,
    summary="Get KPIs",
    description="Get key performance indicators including revenue, profit, sales, orders, and averages"
)
async def get_kpis(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get KPIs.
    """
    try:
        data = await analytics_service.get_kpis()
        return {
            "success": True,
            "message": "KPIs retrieved successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_kpis: {str(e)}")
        raise


@router.get(
    "/trends",
    status_code=status.HTTP_200_OK,
    summary="Get trends",
    description="Get daily, weekly, and monthly trends for revenue and profit"
)
async def get_trends(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get trends.
    """
    try:
        data = await analytics_service.get_trends()
        return {
            "success": True,
            "message": "Trends retrieved successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_trends: {str(e)}")
        raise


@router.get(
    "/report",
    status_code=status.HTTP_200_OK,
    summary="Generate AI-style report",
    description="Generate a comprehensive AI-style business report"
)
async def generate_report(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate AI-style report.
    """
    try:
        data = await analytics_service.generate_report()
        return {
            "success": True,
            "message": "Report generated successfully",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        raise


@router.get(
    "/insights",
    status_code=status.HTTP_200_OK,
    summary="Get business insights",
    description="Get automated business insights and recommendations"
)
async def get_insights(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get business insights.
    """
    try:
        data = await analytics_service.generate_insights()
        return {
            "success": True,
            "message": "Insights generated successfully",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"Error in get_insights: {str(e)}")
        raise