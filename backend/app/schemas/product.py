"""
Product schemas for request/response validation.
Defines Pydantic models for product endpoints.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class ProductCreateRequest(BaseModel):
    """
    Request schema for creating a product.
    """
    name: str = Field(..., min_length=3, max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: str = Field(..., min_length=2, description="Product category")
    sku: str = Field(..., min_length=3, description="Stock Keeping Unit (unique)")
    supplier: Optional[str] = Field(None, description="Supplier name")
    purchase_price: float = Field(default=0.0, ge=0, description="Purchase price")
    selling_price: float = Field(..., gt=0, description="Selling price")
    stock: int = Field(default=0, ge=0, description="Current stock quantity")
    minimum_stock: int = Field(default=5, ge=0, description="Minimum stock alert level")
    status: str = Field(default="active", description="Product status: active/inactive/discontinued")
    image_url: Optional[str] = Field(None, description="Product image URL")
    
    @validator('status')
    def validate_status(cls, v):
        """Validate product status."""
        allowed_statuses = ['active', 'inactive', 'discontinued']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v
    
    @validator('selling_price')
    def validate_selling_price(cls, v):
        """Validate selling price is positive."""
        if v <= 0:
            raise ValueError('Selling price must be greater than 0')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laptop Pro X",
                "description": "High-performance laptop with 16GB RAM",
                "category": "Electronics",
                "sku": "LAP-001",
                "supplier": "TechCorp",
                "purchase_price": 800.00,
                "selling_price": 1200.00,
                "stock": 50,
                "minimum_stock": 10,
                "status": "active",
                "image_url": "https://example.com/laptop.jpg"
            }
        }
    }


class ProductUpdateRequest(BaseModel):
    """
    Request schema for updating a product.
    All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=3, max_length=200, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, min_length=2, description="Product category")
    supplier: Optional[str] = Field(None, description="Supplier name")
    purchase_price: Optional[float] = Field(None, ge=0, description="Purchase price")
    selling_price: Optional[float] = Field(None, gt=0, description="Selling price")
    stock: Optional[int] = Field(None, ge=0, description="Current stock quantity")
    minimum_stock: Optional[int] = Field(None, ge=0, description="Minimum stock alert level")
    status: Optional[str] = Field(None, description="Product status: active/inactive/discontinued")
    image_url: Optional[str] = Field(None, description="Product image URL")
    
    @validator('status')
    def validate_status(cls, v):
        """Validate product status."""
        if v is not None:
            allowed_statuses = ['active', 'inactive', 'discontinued']
            if v not in allowed_statuses:
                raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laptop Pro X Updated",
                "selling_price": 1300.00,
                "stock": 45,
                "status": "active"
            }
        }
    }


class ProductFilterParams(BaseModel):
    """
    Query parameters for filtering products.
    """
    category: Optional[str] = Field(None, description="Filter by category")
    status: Optional[str] = Field(None, description="Filter by status")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum selling price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum selling price")
    low_stock: Optional[bool] = Field(None, description="Filter low stock products")
    search: Optional[str] = Field(None, description="Search in name, category, sku, supplier")
    sort_by: Optional[str] = Field("created_at", description="Sort field: name, selling_price, stock, created_at")
    sort_order: Optional[str] = Field("desc", description="Sort order: asc or desc")
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Items per page")


class ProductResponse(BaseModel):
    """
    Response schema for product data.
    """
    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: str = Field(..., description="Product category")
    sku: str = Field(..., description="Stock Keeping Unit")
    supplier: Optional[str] = Field(None, description="Supplier name")
    purchase_price: float = Field(..., description="Purchase price")
    selling_price: float = Field(..., description="Selling price")
    stock: int = Field(..., description="Current stock quantity")
    minimum_stock: int = Field(..., description="Minimum stock alert level")
    status: str = Field(..., description="Product status")
    image_url: Optional[str] = Field(None, description="Product image URL")
    created_by: str = Field(..., description="User ID who created the product")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "Laptop Pro X",
                "description": "High-performance laptop with 16GB RAM",
                "category": "Electronics",
                "sku": "LAP-001",
                "supplier": "TechCorp",
                "purchase_price": 800.00,
                "selling_price": 1200.00,
                "stock": 50,
                "minimum_stock": 10,
                "status": "active",
                "image_url": "https://example.com/laptop.jpg",
                "created_by": "507f1f77bcf86cd799439012",
                "created_at": "2026-07-15T12:00:00",
                "updated_at": "2026-07-15T12:00:00"
            }
        }
    }


class PaginatedProductResponse(BaseModel):
    """
    Response schema for paginated product list.
    """
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: list[ProductResponse] = Field(..., description="List of products")
    pagination: dict = Field(..., description="Pagination metadata")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Products retrieved successfully",
                "data": [],
                "pagination": {
                    "page": 1,
                    "limit": 10,
                    "total_pages": 5,
                    "total_records": 50
                }
            }
        }
    }


class ProductSummaryResponse(BaseModel):
    """
    Response schema for product summary.
    """
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: dict = Field(..., description="Summary data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Summary retrieved successfully",
                "data": {
                    "total_products": 150,
                    "total_stock": 5000,
                    "inventory_value": 1500000.00,
                    "out_of_stock_count": 5,
                    "low_stock_count": 15,
                    "total_categories": 12
                }
            }
        }
    }