"""
Sale model for MongoDB.
Defines the structure of sale documents in the database.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId


class Sale(BaseModel):
    """
    Sale model representing a sales transaction.
    """
    id: Optional[str] = Field(default=None, alias="_id")
    product_id: str = Field(..., description="Product ID being sold")
    product_name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    quantity: int = Field(..., gt=0, description="Quantity sold")
    unit_purchase_price: float = Field(..., ge=0, description="Purchase price per unit")
    unit_selling_price: float = Field(..., gt=0, description="Selling price per unit")
    total_purchase_cost: float = Field(..., ge=0, description="Total purchase cost")
    total_sale_amount: float = Field(..., gt=0, description="Total sale amount")
    profit: float = Field(..., description="Profit from sale")
    customer_name: Optional[str] = Field(None, description="Customer name")
    payment_method: str = Field(default="cash", description="Payment method: cash/card/online")
    invoice_number: str = Field(..., description="Unique invoice number")
    sale_date: datetime = Field(default_factory=datetime.utcnow, description="Sale date")
    created_by: str = Field(..., description="User ID who created the sale")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('payment_method')
    def validate_payment_method(cls, v):
        """Validate payment method."""
        allowed_methods = ['cash', 'card', 'online', 'credit']
        if v.lower() not in allowed_methods:
            raise ValueError(f'Payment method must be one of: {", ".join(allowed_methods)}')
        return v.lower()
    
    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "product_id": "507f1f77bcf86cd799439011",
                "quantity": 2,
                "customer_name": "John Doe",
                "payment_method": "card",
                "invoice_number": "INV-2024-001"
            }
        }
    }


class SaleInDB(Sale):
    """
    Sale model as stored in the database.
    """
    pass


class SaleResponse(BaseModel):
    """
    Sale response model.
    """
    id: str = Field(..., description="Sale ID")
    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    quantity: int = Field(..., description="Quantity sold")
    unit_purchase_price: float = Field(..., description="Purchase price per unit")
    unit_selling_price: float = Field(..., description="Selling price per unit")
    total_purchase_cost: float = Field(..., description="Total purchase cost")
    total_sale_amount: float = Field(..., description="Total sale amount")
    profit: float = Field(..., description="Profit from sale")
    customer_name: Optional[str] = Field(None, description="Customer name")
    payment_method: str = Field(..., description="Payment method")
    invoice_number: str = Field(..., description="Invoice number")
    sale_date: str = Field(..., description="Sale date")
    created_by: str = Field(..., description="User ID who created the sale")
    created_at: str = Field(..., description="Creation timestamp")
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "product_id": "507f1f77bcf86cd799439012",
                "product_name": "MacBook Pro 2024",
                "category": "Electronics",
                "quantity": 2,
                "unit_purchase_price": 2000.0,
                "unit_selling_price": 2499.0,
                "total_purchase_cost": 4000.0,
                "total_sale_amount": 4998.0,
                "profit": 998.0,
                "customer_name": "John Doe",
                "payment_method": "card",
                "invoice_number": "INV-2024-001",
                "sale_date": "2026-07-16T10:30:00",
                "created_by": "507f1f77bcf86cd799439013",
                "created_at": "2026-07-16T10:30:00"
            }
        }
    }