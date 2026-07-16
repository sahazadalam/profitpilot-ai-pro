"""
Product model for MongoDB.
Defines the structure of product documents in the database.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId


class Product(BaseModel):
    """
    Product model representing a product in the inventory.
    """
    id: Optional[str] = Field(default=None, alias="_id")
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
    created_by: str = Field(..., description="User ID who created the product")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('status')
    def validate_status(cls, v):
        """Validate product status."""
        allowed_statuses = ['active', 'inactive', 'discontinued']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v
    
    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str},
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


class ProductInDB(Product):
    """
    Product model as stored in the database.
    """
    pass


class ProductResponse(BaseModel):
    """
    Product response model (excludes sensitive data).
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


class LowStockProductResponse(BaseModel):
    """
    Response model for low stock products.
    """
    product_id: str
    name: str
    sku: str
    stock: int
    minimum_stock: int
    shortfall: int
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": "507f1f77bcf86cd799439011",
                "name": "Laptop Pro X",
                "sku": "LAP-001",
                "stock": 5,
                "minimum_stock": 10,
                "shortfall": 5
            }
        }
    }


class ProductSummaryResponse(BaseModel):
    """
    Response model for product summary.
    """
    total_products: int = Field(..., description="Total number of products")
    total_stock: int = Field(..., description="Total stock across all products")
    inventory_value: float = Field(..., description="Total inventory value (stock * purchase_price)")
    out_of_stock_count: int = Field(..., description="Number of products with 0 stock")
    low_stock_count: int = Field(..., description="Number of products below minimum stock")
    total_categories: int = Field(..., description="Number of unique categories")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "total_products": 150,
                "total_stock": 5000,
                "inventory_value": 1500000.00,
                "out_of_stock_count": 5,
                "low_stock_count": 15,
                "total_categories": 12
            }
        }
    }