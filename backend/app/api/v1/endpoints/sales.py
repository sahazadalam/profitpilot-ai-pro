"""
Sales endpoints for managing sales transactions.
"""
from fastapi import APIRouter, Depends, status, Query
from typing import Optional

from app.schemas.sale import (
    SaleCreateRequest,
    SaleFilterParams,
    SaleResponse,
    PaginatedSaleResponse
)
from app.services.sales_service import sales_service
from app.dependencies.auth import get_current_active_user, require_admin
from app.schemas.auth import UserResponse
from app.core.exceptions import AppException

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post(
    "/",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new sale",
    description="Create a new sale and automatically update inventory"
)
async def create_sale(
    sale_data: SaleCreateRequest,
    current_user: UserResponse = Depends(get_current_active_user)
) -> SaleResponse:
    """
    Create a new sale.
    
    Args:
        sale_data: Sale creation data
        current_user: Current authenticated user
        
    Returns:
        SaleResponse: Created sale
    """
    try:
        sale = await sales_service.create_sale(
            user_id=current_user.id,
            sale_data=sale_data
        )
        logger.info(f"Sale created by user: {current_user.email}")
        return sale
        
    except AppException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_sale: {str(e)}", exc_info=True)
        raise AppException(
            message="Sale creation failed",
            status_code=500,
            error_code="SALE_CREATION_FAILED"
        )


@router.get(
    "/",
    response_model=PaginatedSaleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all sales",
    description="Get all sales with pagination, filtering, and sorting"
)
async def get_sales(
    current_user: UserResponse = Depends(get_current_active_user),
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    payment_method: Optional[str] = Query(None, description="Filter by payment method"),
    customer_name: Optional[str] = Query(None, description="Filter by customer name"),
    product_name: Optional[str] = Query(None, description="Filter by product name"),
    invoice_number: Optional[str] = Query(None, description="Filter by invoice number"),
    search: Optional[str] = Query(None, description="Search in invoice, customer, product"),
    sort_by: Optional[str] = Query("sale_date", description="Sort field"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
) -> PaginatedSaleResponse:
    """
    Get all sales with pagination, filtering, and sorting.
    """
    # Parse dates if provided
    from datetime import datetime
    start_date_obj = None
    end_date_obj = None
    
    if start_date:
        try:
            start_date_obj = datetime.fromisoformat(start_date)
        except:
            pass
    
    if end_date:
        try:
            end_date_obj = datetime.fromisoformat(end_date)
        except:
            pass
    
    filters = SaleFilterParams(
        start_date=start_date_obj,
        end_date=end_date_obj,
        category=category,
        payment_method=payment_method,
        customer_name=customer_name,
        product_name=product_name,
        invoice_number=invoice_number,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit
    )
    
    sales, pagination = await sales_service.get_sales(filters)
    
    return PaginatedSaleResponse(
        success=True,
        message="Sales retrieved successfully",
        data=sales,
        pagination=pagination
    )


@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get sale by ID",
    description="Get a single sale by its ID"
)
async def get_sale_by_id(
    sale_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
) -> SaleResponse:
    """
    Get a sale by ID.
    """
    try:
        sale = await sales_service.get_sale_by_id(sale_id)
        return sale
    except Exception as e:
        logger.error(f"Error in get_sale_by_id: {str(e)}", exc_info=True)
        raise


@router.delete(
    "/{sale_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete sale",
    description="Delete a sale and restore product stock (Admin only)"
)
async def delete_sale(
    sale_id: str,
    current_user: UserResponse = Depends(require_admin)
) -> dict:
    """
    Delete a sale (Admin only).
    """
    try:
        await sales_service.delete_sale(sale_id)
        logger.info(f"Sale deleted by admin: {current_user.email}")
        
        return {
            "success": True,
            "message": "Sale deleted successfully and stock restored"
        }
        
    except Exception as e:
        logger.error(f"Error in delete_sale: {str(e)}", exc_info=True)
        raise