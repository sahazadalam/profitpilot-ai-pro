"""
Product service for inventory management.
Handles business logic for product CRUD operations.
"""
from datetime import datetime
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
from app.schemas.product import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductFilterParams,
    ProductResponse,
    ProductSummaryResponse
)
from app.models.product import Product

logger = logging.getLogger(__name__)


class ProductService:
    """
    Product service handling inventory management operations.
    """
    
    def __init__(self):
        """Initialize the product service."""
        self.collection_name = "products"
    
    async def get_collection(self):
        """
        Get the products collection from MongoDB.
        
        Returns:
            Collection: MongoDB products collection
        """
        return mongodb.get_collection(self.collection_name)
    
    async def create_product(self, user_id: str, product_data: ProductCreateRequest) -> ProductResponse:
        """
        Create a new product.
        
        Args:
            user_id: ID of the user creating the product
            product_data: Product creation data
            
        Returns:
            ProductResponse: Created product
            
        Raises:
            AppException: If duplicate SKU or name exists
        """
        try:
            collection = await self.get_collection()
            
            # Check duplicate SKU
            existing_sku = await collection.find_one({"sku": product_data.sku})
            if existing_sku:
                logger.warning(f"Duplicate SKU attempt: {product_data.sku}")
                raise AppException(
                    message=f"Product with SKU '{product_data.sku}' already exists",
                    status_code=409,
                    error_code="DUPLICATE_SKU"
                )
            
            # Check duplicate name
            existing_name = await collection.find_one({"name": product_data.name})
            if existing_name:
                logger.warning(f"Duplicate product name attempt: {product_data.name}")
                raise AppException(
                    message=f"Product with name '{product_data.name}' already exists",
                    status_code=409,
                    error_code="DUPLICATE_NAME"
                )
            
            # Create product document
            product_dict = product_data.model_dump()
            product_dict.update({
                "created_by": user_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            
            # Insert product
            result = await collection.insert_one(product_dict)
            created_product = await collection.find_one({"_id": result.inserted_id})
            
            logger.info(f"Product created successfully: {product_data.name} (SKU: {product_data.sku})")
            
            return ProductResponse(
                id=str(created_product["_id"]),
                name=created_product["name"],
                description=created_product.get("description"),
                category=created_product["category"],
                sku=created_product["sku"],
                supplier=created_product.get("supplier"),
                purchase_price=created_product["purchase_price"],
                selling_price=created_product["selling_price"],
                stock=created_product["stock"],
                minimum_stock=created_product["minimum_stock"],
                status=created_product["status"],
                image_url=created_product.get("image_url"),
                created_by=created_product["created_by"],
                created_at=created_product["created_at"].isoformat(),
                updated_at=created_product["updated_at"].isoformat()
            )
            
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in create_product: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to create product: {str(e)}",
                status_code=500,
                error_code="PRODUCT_CREATION_FAILED"
            )
    
    async def get_products(
        self,
        filters: ProductFilterParams
    ) -> Tuple[List[ProductResponse], Dict[str, Any]]:
        """
        Get products with filtering, pagination, sorting.
        
        Args:
            filters: Filter parameters
            
        Returns:
            Tuple[List[ProductResponse], Dict]: Products and pagination info
        """
        try:
            collection = await self.get_collection()
            
            # Build query
            query = {}
            
            # Category filter
            if filters.category:
                query["category"] = {"$regex": filters.category, "$options": "i"}
            
            # Status filter
            if filters.status:
                query["status"] = filters.status
            
            # Price range filter
            if filters.min_price is not None or filters.max_price is not None:
                price_filter = {}
                if filters.min_price is not None:
                    price_filter["$gte"] = filters.min_price
                if filters.max_price is not None:
                    price_filter["$lte"] = filters.max_price
                query["selling_price"] = price_filter
            
            # Low stock filter
            if filters.low_stock:
                query["$expr"] = {"$lte": ["$stock", "$minimum_stock"]}
            
            # Search filter
            if filters.search:
                search_term = filters.search
                query["$or"] = [
                    {"name": {"$regex": search_term, "$options": "i"}},
                    {"category": {"$regex": search_term, "$options": "i"}},
                    {"sku": {"$regex": search_term, "$options": "i"}},
                    {"supplier": {"$regex": search_term, "$options": "i"}}
                ]
            
            # Get total count
            total_records = await collection.count_documents(query)
            
            # Build sort
            sort_field = filters.sort_by
            sort_order = -1 if filters.sort_order == "desc" else 1
            
            # Get products with pagination
            skip = (filters.page - 1) * filters.limit
            
            cursor = collection.find(query)
            cursor = cursor.sort(sort_field, sort_order)
            cursor = cursor.skip(skip).limit(filters.limit)
            
            products = await cursor.to_list(length=filters.limit)
            
            # Convert to response models
            product_responses = []
            for product in products:
                product_responses.append(
                    ProductResponse(
                        id=str(product["_id"]),
                        name=product["name"],
                        description=product.get("description"),
                        category=product["category"],
                        sku=product["sku"],
                        supplier=product.get("supplier"),
                        purchase_price=product["purchase_price"],
                        selling_price=product["selling_price"],
                        stock=product["stock"],
                        minimum_stock=product["minimum_stock"],
                        status=product["status"],
                        image_url=product.get("image_url"),
                        created_by=product["created_by"],
                        created_at=product["created_at"].isoformat(),
                        updated_at=product["updated_at"].isoformat()
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
            
            logger.info(f"Retrieved {len(product_responses)} products")
            
            return product_responses, pagination
            
        except Exception as e:
            logger.error(f"Error in get_products: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to retrieve products: {str(e)}",
                status_code=500,
                error_code="PRODUCT_RETRIEVAL_FAILED"
            )
    
    async def get_product_by_id(self, product_id: str) -> ProductResponse:
        """
        Get a product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            ProductResponse: Product data
            
        Raises:
            NotFoundException: If product not found
        """
        try:
            collection = await self.get_collection()
            
            try:
                product = await collection.find_one({"_id": ObjectId(product_id)})
            except:
                raise NotFoundException(message="Product not found")
            
            if not product:
                raise NotFoundException(message="Product not found")
            
            return ProductResponse(
                id=str(product["_id"]),
                name=product["name"],
                description=product.get("description"),
                category=product["category"],
                sku=product["sku"],
                supplier=product.get("supplier"),
                purchase_price=product["purchase_price"],
                selling_price=product["selling_price"],
                stock=product["stock"],
                minimum_stock=product["minimum_stock"],
                status=product["status"],
                image_url=product.get("image_url"),
                created_by=product["created_by"],
                created_at=product["created_at"].isoformat(),
                updated_at=product["updated_at"].isoformat()
            )
            
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in get_product_by_id: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to retrieve product: {str(e)}",
                status_code=500,
                error_code="PRODUCT_RETRIEVAL_FAILED"
            )
    
    async def update_product(
        self,
        product_id: str,
        user_id: str,
        update_data: ProductUpdateRequest
    ) -> ProductResponse:
        """
        Update a product.
        
        Args:
            product_id: Product ID
            user_id: ID of the user updating
            update_data: Product update data
            
        Returns:
            ProductResponse: Updated product
            
        Raises:
            NotFoundException: If product not found
            AppException: If duplicate name exists
        """
        try:
            collection = await self.get_collection()
            
            # Get existing product
            try:
                product = await collection.find_one({"_id": ObjectId(product_id)})
            except:
                raise NotFoundException(message="Product not found")
            
            if not product:
                raise NotFoundException(message="Product not found")
            
            # Prepare update data
            update_dict = update_data.model_dump(exclude_unset=True)
            
            # Check duplicate name if updating
            if "name" in update_dict:
                existing_name = await collection.find_one({
                    "name": update_dict["name"],
                    "_id": {"$ne": ObjectId(product_id)}
                })
                if existing_name:
                    raise AppException(
                        message=f"Product with name '{update_dict['name']}' already exists",
                        status_code=409,
                        error_code="DUPLICATE_NAME"
                    )
            
            # Update timestamp
            update_dict["updated_at"] = datetime.utcnow()
            
            # Update product
            await collection.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": update_dict}
            )
            
            # Get updated product
            updated_product = await collection.find_one({"_id": ObjectId(product_id)})
            
            logger.info(f"Product updated: {updated_product['name']} (ID: {product_id})")
            
            return ProductResponse(
                id=str(updated_product["_id"]),
                name=updated_product["name"],
                description=updated_product.get("description"),
                category=updated_product["category"],
                sku=updated_product["sku"],
                supplier=updated_product.get("supplier"),
                purchase_price=updated_product["purchase_price"],
                selling_price=updated_product["selling_price"],
                stock=updated_product["stock"],
                minimum_stock=updated_product["minimum_stock"],
                status=updated_product["status"],
                image_url=updated_product.get("image_url"),
                created_by=updated_product["created_by"],
                created_at=updated_product["created_at"].isoformat(),
                updated_at=updated_product["updated_at"].isoformat()
            )
            
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in update_product: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to update product: {str(e)}",
                status_code=500,
                error_code="PRODUCT_UPDATE_FAILED"
            )
    
    async def delete_product(self, product_id: str) -> bool:
        """
        Delete a product.
        
        Args:
            product_id: Product ID
            
        Returns:
            bool: True if deleted
            
        Raises:
            NotFoundException: If product not found
        """
        try:
            collection = await self.get_collection()
            
            try:
                result = await collection.delete_one({"_id": ObjectId(product_id)})
            except:
                raise NotFoundException(message="Product not found")
            
            if result.deleted_count == 0:
                raise NotFoundException(message="Product not found")
            
            logger.info(f"Product deleted: {product_id}")
            return True
            
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_product: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to delete product: {str(e)}",
                status_code=500,
                error_code="PRODUCT_DELETE_FAILED"
            )
    
    async def get_low_stock_products(self) -> List[Dict[str, Any]]:
        """
        Get all products with low stock.
        
        Returns:
            List[Dict]: List of low stock products
        """
        try:
            collection = await self.get_collection()
            
            # Query products where stock <= minimum_stock
            products = await collection.find({
                "$expr": {"$lte": ["$stock", "$minimum_stock"]}
            }).to_list(length=1000)
            
            low_stock_products = []
            for product in products:
                low_stock_products.append({
                    "product_id": str(product["_id"]),
                    "name": product["name"],
                    "sku": product["sku"],
                    "stock": product["stock"],
                    "minimum_stock": product["minimum_stock"],
                    "shortfall": product["minimum_stock"] - product["stock"]
                })
            
            logger.info(f"Found {len(low_stock_products)} low stock products")
            return low_stock_products
            
        except Exception as e:
            logger.error(f"Error in get_low_stock_products: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to get low stock products: {str(e)}",
                status_code=500,
                error_code="LOW_STOCK_RETRIEVAL_FAILED"
            )
    
    async def get_product_summary(self) -> Dict[str, Any]:
        """
        Get product summary statistics.
        
        Returns:
            Dict: Summary statistics
        """
        try:
            collection = await self.get_collection()
            
            # Aggregation pipeline
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_products": {"$sum": 1},
                        "total_stock": {"$sum": "$stock"},
                        "inventory_value": {"$sum": {"$multiply": ["$stock", "$purchase_price"]}},
                        "out_of_stock_count": {
                            "$sum": {"$cond": [{"$eq": ["$stock", 0]}, 1, 0]}
                        },
                        "low_stock_count": {
                            "$sum": {"$cond": [
                                {"$lte": ["$stock", "$minimum_stock"]},
                                1,
                                0
                            ]}
                        },
                        "total_categories": {"$addToSet": "$category"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "total_products": 1,
                        "total_stock": 1,
                        "inventory_value": {"$round": ["$inventory_value", 2]},
                        "out_of_stock_count": 1,
                        "low_stock_count": 1,
                        "total_categories": {"$size": "$total_categories"}
                    }
                }
            ]
            
            cursor = collection.aggregate(pipeline)
            summary = await cursor.to_list(length=1)
            
            if not summary:
                return {
                    "total_products": 0,
                    "total_stock": 0,
                    "inventory_value": 0.0,
                    "out_of_stock_count": 0,
                    "low_stock_count": 0,
                    "total_categories": 0
                }
            
            logger.info("Product summary retrieved successfully")
            return summary[0]
            
        except Exception as e:
            logger.error(f"Error in get_product_summary: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to get product summary: {str(e)}",
                status_code=500,
                error_code="SUMMARY_RETRIEVAL_FAILED"
            )


# Create singleton instance
product_service = ProductService()