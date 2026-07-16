"""
Product endpoints for inventory management.
Handles CRUD operations for products.
"""
from fastapi import APIRouter, Depends, status, Query
from typing import Optional, List

from app.schemas.product import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductFilterParams,
    ProductResponse,
    PaginatedProductResponse,
    ProductSummaryResponse
)
from app.services.product_service import product_service
from app.dependencies.auth import get_current_active_user, require_admin
from app.schemas.auth import UserResponse
from app.core.exceptions import AppException

import logging

logger = logging.getLogger(__name__)

# Create router with prefix and tags
router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    description="Create a new product in the inventory (Admin only)"
)
async def create_product(
    product_data: ProductCreateRequest,
    current_user: UserResponse = Depends(require_admin)
) -> ProductResponse:
    """
    Create a new product.
    
    Args:
        product_data: Product creation data
        current_user: Current admin user (injected)
        
    Returns:
        ProductResponse: Created product
        
    Raises:
        AppException: If duplicate SKU or name exists
    """
    try:
        product = await product_service.create_product(
            user_id=current_user.id,
            product_data=product_data
        )
        logger.info(f"Product created by admin: {current_user.email}")
        return product
        
    except AppException as e:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_product: {str(e)}", exc_info=True)
        raise AppException(
            message="Product creation failed",
            status_code=500,
            error_code="PRODUCT_CREATION_FAILED"
        )


@router.get(
    "/",
    response_model=PaginatedProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all products",
    description="Get all products with pagination, filtering, and sorting"
)
async def get_products(
    current_user: UserResponse = Depends(get_current_active_user),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum selling price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum selling price"),
    low_stock: Optional[bool] = Query(None, description="Filter low stock products"),
    search: Optional[str] = Query(None, description="Search in name, category, sku, supplier"),
    sort_by: Optional[str] = Query("created_at", description="Sort field: name, selling_price, stock, created_at"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
) -> PaginatedProductResponse:
    """
    Get all products with pagination, filtering, and sorting.
    
    Args:
        current_user: Current authenticated user (injected)
        category: Filter by category
        status: Filter by status
        min_price: Minimum selling price
        max_price: Maximum selling price
        low_stock: Filter low stock products
        search: Search term
        sort_by: Sort field
        sort_order: Sort order
        page: Page number
        limit: Items per page
        
    Returns:
        PaginatedProductResponse: List of products with pagination info
    """
    # Create filter parameters
    filters = ProductFilterParams(
        category=category,
        status=status,
        min_price=min_price,
        max_price=max_price,
        low_stock=low_stock,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit
    )
    
    # Get products
    products, pagination = await product_service.get_products(filters)
    
    return PaginatedProductResponse(
        success=True,
        message="Products retrieved successfully",
        data=products,
        pagination=pagination
    )


@router.get(
    "/low-stock",
    status_code=status.HTTP_200_OK,
    summary="Get low stock products",
    description="Get all products with stock below minimum stock level"
)
async def get_low_stock_products(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get all products with low stock.
    
    Args:
        current_user: Current authenticated user (injected)
        
    Returns:
        dict: List of low stock products
    """
    try:
        low_stock_products = await product_service.get_low_stock_products()
        
        return {
            "success": True,
            "message": "Low stock products retrieved successfully",
            "count": len(low_stock_products),
            "data": low_stock_products
        }
        
    except Exception as e:
        logger.error(f"Error in get_low_stock_products: {str(e)}", exc_info=True)
        raise AppException(
            message="Failed to retrieve low stock products",
            status_code=500,
            error_code="LOW_STOCK_RETRIEVAL_FAILED"
        )


@router.get(
    "/summary",
    response_model=ProductSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get product summary",
    description="Get summary statistics for all products"
)
async def get_product_summary(
    current_user: UserResponse = Depends(get_current_active_user)
) -> ProductSummaryResponse:
    """
    Get product summary statistics.
    
    Args:
        current_user: Current authenticated user (injected)
        
    Returns:
        ProductSummaryResponse: Summary statistics
    """
    try:
        summary = await product_service.get_product_summary()
        
        return ProductSummaryResponse(
            success=True,
            message="Summary retrieved successfully",
            data=summary
        )
        
    except Exception as e:
        logger.error(f"Error in get_product_summary: {str(e)}", exc_info=True)
        raise AppException(
            message="Failed to retrieve summary",
            status_code=500,
            error_code="SUMMARY_RETRIEVAL_FAILED"
        )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get product by ID",
    description="Get a single product by its ID"
)
async def get_product_by_id(
    product_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
) -> ProductResponse:
    """
    Get a product by ID.
    
    Args:
        product_id: Product ID
        current_user: Current authenticated user (injected)
        
    Returns:
        ProductResponse: Product data
        
    Raises:
        NotFoundException: If product not found
    """
    try:
        product = await product_service.get_product_by_id(product_id)
        return product
        
    except Exception as e:
        logger.error(f"Error in get_product_by_id: {str(e)}", exc_info=True)
        raise


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update product",
    description="Update a product (Admin only)"
)
async def update_product(
    product_id: str,
    update_data: ProductUpdateRequest,
    current_user: UserResponse = Depends(require_admin)
) -> ProductResponse:
    """
    Update a product.
    
    Args:
        product_id: Product ID
        update_data: Product update data
        current_user: Current admin user (injected)
        
    Returns:
        ProductResponse: Updated product
        
    Raises:
        NotFoundException: If product not found
        AppException: If duplicate name exists
    """
    try:
        product = await product_service.update_product(
            product_id=product_id,
            user_id=current_user.id,
            update_data=update_data
        )
        logger.info(f"Product updated by admin: {current_user.email}")
        return product
        
    except Exception as e:
        logger.error(f"Error in update_product: {str(e)}", exc_info=True)
        raise


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete product",
    description="Delete a product (Admin only)"
)
async def delete_product(
    product_id: str,
    current_user: UserResponse = Depends(require_admin)
) -> dict:
    """
    Delete a product.
    
    Args:
        product_id: Product ID
        current_user: Current admin user (injected)
        
    Returns:
        dict: Success message
        
    Raises:
        NotFoundException: If product not found
    """
    try:
        await product_service.delete_product(product_id)
        logger.info(f"Product deleted by admin: {current_user.email}")
        
        return {
            "success": True,
            "message": "Product deleted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in delete_product: {str(e)}", exc_info=True)
        raise