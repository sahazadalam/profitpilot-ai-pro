"""
Dashboard endpoints for business intelligence.
"""
from fastapi import APIRouter, Depends, status, Query
from typing import Optional

from app.services.dashboard_service import dashboard_service
from app.dependencies.auth import get_current_active_user
from app.schemas.auth import UserResponse
from app.core.exceptions import AppException

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get dashboard summary",
    description="Get comprehensive dashboard summary with key metrics"
)
async def get_dashboard_summary(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get dashboard summary.
    """
    try:
        summary = await dashboard_service.get_dashboard_summary()
        
        return {
            "success": True,
            "message": "Dashboard summary retrieved successfully",
            "data": summary
        }
        
    except Exception as e:
        logger.error(f"Error in get_dashboard_summary: {str(e)}", exc_info=True)
        raise AppException(
            message="Failed to get dashboard summary",
            status_code=500,
            error_code="DASHBOARD_SUMMARY_FAILED"
        )


@router.get(
    "/top-products",
    status_code=status.HTTP_200_OK,
    summary="Get top selling products",
    description="Get top 10 selling products by quantity"
)
async def get_top_products(
    limit: int = Query(10, ge=1, le=50, description="Number of products to return"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get top selling products.
    """
    try:
        products = await dashboard_service.get_top_products(limit)
        
        return {
            "success": True,
            "message": "Top products retrieved successfully",
            "count": len(products),
            "data": products
        }
        
    except Exception as e:
        logger.error(f"Error in get_top_products: {str(e)}", exc_info=True)
        raise AppException(
            message="Failed to get top products",
            status_code=500,
            error_code="TOP_PRODUCTS_FAILED"
        )


@router.get(
    "/recent-sales",
    status_code=status.HTTP_200_OK,
    summary="Get recent sales",
    description="Get the most recent sales"
)
async def get_recent_sales(
    limit: int = Query(10, ge=1, le=50, description="Number of sales to return"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get recent sales.
    """
    try:
        sales = await dashboard_service.get_recent_sales(limit)
        
        return {
            "success": True,
            "message": "Recent sales retrieved successfully",
            "count": len(sales),
            "data": sales
        }
        
    except Exception as e:
        logger.error(f"Error in get_recent_sales: {str(e)}", exc_info=True)
        raise AppException(
            message="Failed to get recent sales",
            status_code=500,
            error_code="RECENT_SALES_FAILED"
        )


@router.get(
    "/revenue-chart",
    status_code=status.HTTP_200_OK,
    summary="Get revenue chart data",
    description="Get revenue and profit data for the last N days"
)
async def get_revenue_chart(
    days: int = Query(30, ge=1, le=365, description="Number of days"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get revenue chart data.
    """
    try:
        chart_data = await dashboard_service.get_revenue_chart_data(days)
        
        return {
            "success": True,
            "message": "Revenue chart data retrieved successfully",
            "data": chart_data
        }
        
    except Exception as e:
        logger.error(f"Error in get_revenue_chart: {str(e)}", exc_info=True)
        raise AppException(
            message="Failed to get revenue chart data",
            status_code=500,
            error_code="REVENUE_CHART_FAILED"
        )


@router.get(
    "/profit-summary",
    status_code=status.HTTP_200_OK,
    summary="Get profit summary",
    description="Get daily, weekly, and monthly profit summary"
)
async def get_profit_summary(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get profit summary.
    """
    try:
        summary = await dashboard_service.get_profit_summary()
        
        return {
            "success": True,
            "message": "Profit summary retrieved successfully",
            "data": summary
        }
        
    except Exception as e:
        logger.error(f"Error in get_profit_summary: {str(e)}", exc_info=True)
        raise AppException(
            message="Failed to get profit summary",
            status_code=500,
            error_code="PROFIT_SUMMARY_FAILED"
        )