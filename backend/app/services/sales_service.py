"""
Sales service for managing sales transactions.
Handles business logic for sales operations and inventory updates.
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from bson import ObjectId
import logging

from app.database.mongodb import mongodb
from app.core.exceptions import (
    AppException,
    NotFoundException,
    ValidationException,
    ForbiddenException
)
from app.schemas.sale import (
    SaleCreateRequest,
    SaleUpdateRequest,
    SaleFilterParams,
    SaleResponse
)
from app.models.sale import Sale

logger = logging.getLogger(__name__)


class SalesService:
    """
    Sales service handling sales operations and inventory updates.
    """
    
    def __init__(self):
        """Initialize the sales service."""
        self.collection_name = "sales"
        self.products_collection = "products"
    
    async def get_collection(self):
        """Get the sales collection from MongoDB."""
        return mongodb.get_collection(self.collection_name)
    
    async def get_products_collection(self):
        """Get the products collection from MongoDB."""
        return mongodb.get_collection(self.products_collection)
    
    async def create_sale(self, user_id: str, sale_data: SaleCreateRequest) -> SaleResponse:
        """
        Create a new sale and update inventory.
        
        Args:
            user_id: ID of the user creating the sale
            sale_data: Sale creation data
            
        Returns:
            SaleResponse: Created sale
            
        Raises:
            NotFoundException: If product not found
            ValidationException: If insufficient stock
            AppException: If duplicate invoice number
        """
        try:
            sales_collection = await self.get_collection()
            products_collection = await self.get_products_collection()
            
            # Check if invoice number already exists
            existing_invoice = await sales_collection.find_one(
                {"invoice_number": sale_data.invoice_number}
            )
            if existing_invoice:
                logger.warning(f"Duplicate invoice number: {sale_data.invoice_number}")
                raise AppException(
                    message=f"Invoice number '{sale_data.invoice_number}' already exists",
                    status_code=409,
                    error_code="DUPLICATE_INVOICE"
                )
            
            # Get product
            try:
                product = await products_collection.find_one(
                    {"_id": ObjectId(sale_data.product_id)}
                )
            except:
                raise NotFoundException(message="Product not found")
            
            if not product:
                raise NotFoundException(message="Product not found")
            
            # Check stock availability
            if product["stock"] < sale_data.quantity:
                raise ValidationException(
                    message=f"Insufficient stock. Available: {product['stock']}, Requested: {sale_data.quantity}"
                )
            
            # Calculate values
            unit_purchase_price = product["purchase_price"]
            unit_selling_price = product["selling_price"]
            total_purchase_cost = unit_purchase_price * sale_data.quantity
            total_sale_amount = unit_selling_price * sale_data.quantity
            profit = total_sale_amount - total_purchase_cost
            
            # Create sale document
            sale_dict = {
                "product_id": sale_data.product_id,
                "product_name": product["name"],
                "category": product["category"],
                "quantity": sale_data.quantity,
                "unit_purchase_price": unit_purchase_price,
                "unit_selling_price": unit_selling_price,
                "total_purchase_cost": total_purchase_cost,
                "total_sale_amount": total_sale_amount,
                "profit": profit,
                "customer_name": sale_data.customer_name,
                "payment_method": sale_data.payment_method or "cash",
                "invoice_number": sale_data.invoice_number,
                "sale_date": sale_data.sale_date or datetime.utcnow(),
                "created_by": user_id,
                "created_at": datetime.utcnow()
            }
            
            # Insert sale
            result = await sales_collection.insert_one(sale_dict)
            created_sale = await sales_collection.find_one({"_id": result.inserted_id})
            
            # Update product stock
            await products_collection.update_one(
                {"_id": ObjectId(sale_data.product_id)},
                {
                    "$inc": {"stock": -sale_data.quantity},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            logger.info(
                f"Sale created: {sale_data.invoice_number} "
                f"(Product: {product['name']}, Qty: {sale_data.quantity})"
            )
            
            return SaleResponse(
                id=str(created_sale["_id"]),
                product_id=created_sale["product_id"],
                product_name=created_sale["product_name"],
                category=created_sale["category"],
                quantity=created_sale["quantity"],
                unit_purchase_price=created_sale["unit_purchase_price"],
                unit_selling_price=created_sale["unit_selling_price"],
                total_purchase_cost=created_sale["total_purchase_cost"],
                total_sale_amount=created_sale["total_sale_amount"],
                profit=created_sale["profit"],
                customer_name=created_sale.get("customer_name"),
                payment_method=created_sale["payment_method"],
                invoice_number=created_sale["invoice_number"],
                sale_date=created_sale["sale_date"].isoformat(),
                created_by=created_sale["created_by"],
                created_at=created_sale["created_at"].isoformat()
            )
            
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in create_sale: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to create sale: {str(e)}",
                status_code=500,
                error_code="SALE_CREATION_FAILED"
            )
    
    async def get_sales(
        self,
        filters: SaleFilterParams
    ) -> Tuple[List[SaleResponse], Dict[str, Any]]:
        """
        Get sales with filtering, pagination, sorting.
        
        Args:
            filters: Filter parameters
            
        Returns:
            Tuple[List[SaleResponse], Dict]: Sales and pagination info
        """
        try:
            collection = await self.get_collection()
            
            # Build query
            query = {}
            
            # Date range filter
            if filters.start_date or filters.end_date:
                date_filter = {}
                if filters.start_date:
                    date_filter["$gte"] = filters.start_date
                if filters.end_date:
                    date_filter["$lte"] = filters.end_date
                query["sale_date"] = date_filter
            
            # Category filter
            if filters.category:
                query["category"] = {"$regex": filters.category, "$options": "i"}
            
            # Payment method filter
            if filters.payment_method:
                query["payment_method"] = filters.payment_method
            
            # Customer name filter
            if filters.customer_name:
                query["customer_name"] = {"$regex": filters.customer_name, "$options": "i"}
            
            # Product name filter
            if filters.product_name:
                query["product_name"] = {"$regex": filters.product_name, "$options": "i"}
            
            # Invoice number filter
            if filters.invoice_number:
                query["invoice_number"] = {"$regex": filters.invoice_number, "$options": "i"}
            
            # Search filter
            if filters.search:
                search_term = filters.search
                query["$or"] = [
                    {"invoice_number": {"$regex": search_term, "$options": "i"}},
                    {"customer_name": {"$regex": search_term, "$options": "i"}},
                    {"product_name": {"$regex": search_term, "$options": "i"}},
                    {"category": {"$regex": search_term, "$options": "i"}}
                ]
            
            # Get total count
            total_records = await collection.count_documents(query)
            
            # Build sort
            sort_field = filters.sort_by
            sort_order = -1 if filters.sort_order == "desc" else 1
            
            # Get sales with pagination
            skip = (filters.page - 1) * filters.limit
            
            cursor = collection.find(query)
            cursor = cursor.sort(sort_field, sort_order)
            cursor = cursor.skip(skip).limit(filters.limit)
            
            sales = await cursor.to_list(length=filters.limit)
            
            # Convert to response models
            sale_responses = []
            for sale in sales:
                sale_responses.append(
                    SaleResponse(
                        id=str(sale["_id"]),
                        product_id=sale["product_id"],
                        product_name=sale["product_name"],
                        category=sale["category"],
                        quantity=sale["quantity"],
                        unit_purchase_price=sale["unit_purchase_price"],
                        unit_selling_price=sale["unit_selling_price"],
                        total_purchase_cost=sale["total_purchase_cost"],
                        total_sale_amount=sale["total_sale_amount"],
                        profit=sale["profit"],
                        customer_name=sale.get("customer_name"),
                        payment_method=sale["payment_method"],
                        invoice_number=sale["invoice_number"],
                        sale_date=sale["sale_date"].isoformat(),
                        created_by=sale["created_by"],
                        created_at=sale["created_at"].isoformat()
                    )
                )
            
            # Pagination info
            total_pages = (total_records + filters.limit - 1) // filters.limit
            pagination = {
                "page": filters.page,
                "limit": filters.limit,
                "total_pages": total_pages,
                "total_records": total_records
            }
            
            logger.info(f"Retrieved {len(sale_responses)} sales")
            
            return sale_responses, pagination
            
        except Exception as e:
            logger.error(f"Error in get_sales: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to retrieve sales: {str(e)}",
                status_code=500,
                error_code="SALE_RETRIEVAL_FAILED"
            )
    
    async def get_sale_by_id(self, sale_id: str) -> SaleResponse:
        """
        Get a sale by ID.
        
        Args:
            sale_id: Sale ID
            
        Returns:
            SaleResponse: Sale data
            
        Raises:
            NotFoundException: If sale not found
        """
        try:
            collection = await self.get_collection()
            
            try:
                sale = await collection.find_one({"_id": ObjectId(sale_id)})
            except:
                raise NotFoundException(message="Sale not found")
            
            if not sale:
                raise NotFoundException(message="Sale not found")
            
            return SaleResponse(
                id=str(sale["_id"]),
                product_id=sale["product_id"],
                product_name=sale["product_name"],
                category=sale["category"],
                quantity=sale["quantity"],
                unit_purchase_price=sale["unit_purchase_price"],
                unit_selling_price=sale["unit_selling_price"],
                total_purchase_cost=sale["total_purchase_cost"],
                total_sale_amount=sale["total_sale_amount"],
                profit=sale["profit"],
                customer_name=sale.get("customer_name"),
                payment_method=sale["payment_method"],
                invoice_number=sale["invoice_number"],
                sale_date=sale["sale_date"].isoformat(),
                created_by=sale["created_by"],
                created_at=sale["created_at"].isoformat()
            )
            
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in get_sale_by_id: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to retrieve sale: {str(e)}",
                status_code=500,
                error_code="SALE_RETRIEVAL_FAILED"
            )
    
    async def delete_sale(self, sale_id: str) -> bool:
        """
        Delete a sale and restore product stock.
        
        Args:
            sale_id: Sale ID
            
        Returns:
            bool: True if deleted
            
        Raises:
            NotFoundException: If sale not found
        """
        try:
            sales_collection = await self.get_collection()
            products_collection = await self.get_products_collection()
            
            # Get the sale
            try:
                sale = await sales_collection.find_one({"_id": ObjectId(sale_id)})
            except:
                raise NotFoundException(message="Sale not found")
            
            if not sale:
                raise NotFoundException(message="Sale not found")
            
            # Restore product stock
            await products_collection.update_one(
                {"_id": ObjectId(sale["product_id"])},
                {
                    "$inc": {"stock": sale["quantity"]},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            # Delete the sale
            result = await sales_collection.delete_one({"_id": ObjectId(sale_id)})
            
            if result.deleted_count == 0:
                raise NotFoundException(message="Sale not found")
            
            logger.info(f"Sale deleted and stock restored: {sale_id}")
            return True
            
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_sale: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to delete sale: {str(e)}",
                status_code=500,
                error_code="SALE_DELETE_FAILED"
            )


# Create singleton instance
sales_service = SalesService()