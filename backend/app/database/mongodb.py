"""
MongoDB connection module for ProfitPilot AI Pro.
Handles asynchronous database connections using Motor.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    """
    MongoDB connection manager.
    Handles connection lifecycle and provides database access.
    """
    
    def __init__(self):
        """Initialize the MongoDB connection manager."""
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self._is_connected: bool = False
    
    async def connect(self) -> None:
        """
        Establish connection to MongoDB.
        Raises exception if connection fails.
        """
        try:
            logger.info(f"Connecting to MongoDB...")
            
            # Use the connection string from settings
            mongodb_url = settings.MONGODB_URL
            
            # For Atlas, ensure proper SSL settings
            if 'mongodb+srv' in mongodb_url:
                self.client = AsyncIOMotorClient(
                    mongodb_url,
                    serverSelectionTimeoutMS=5000,
                    maxPoolSize=10,
                    minPoolSize=1,
                    maxIdleTimeMS=30000,
                    waitQueueTimeoutMS=5000,
                )
            else:
                self.client = AsyncIOMotorClient(
                    mongodb_url,
                    serverSelectionTimeoutMS=5000,
                )
            
            # Ping the database to verify connection
            await self.client.admin.command('ping')
            
            # Get the database
            self.db = self.client[settings.MONGODB_DB_NAME]
            self._is_connected = True
            
            logger.info(f"Successfully connected to MongoDB database: {settings.MONGODB_DB_NAME}")
            
            # Create indexes
            await self._create_indexes()
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            self._is_connected = False
            raise
    
    async def disconnect(self) -> None:
        """
        Close MongoDB connection.
        """
        if self.client:
            self.client.close()
            self._is_connected = False
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self) -> None:
        """
        Create database indexes for better query performance.
        """
        try:
            # Users collection indexes
            users_collection = self.db["users"]
            
            # Unique index on email for fast lookup and duplicate prevention
            await users_collection.create_index("email", unique=True)
            
            # Index on role for role-based queries
            await users_collection.create_index("role")
            
            # Index on is_active for filtering active users
            await users_collection.create_index("is_active")
            
            # Products collection indexes
            products_collection = self.db["products"]
            
            # Unique indexes
            await products_collection.create_index("sku", unique=True)
            await products_collection.create_index("name", unique=True)
            
            # Search and filter indexes
            await products_collection.create_index("category")
            await products_collection.create_index("status")
            await products_collection.create_index("supplier")
            
            # Compound indexes for common queries
            await products_collection.create_index([
                ("category", 1),
                ("status", 1),
                ("selling_price", 1)
            ])
            
            await products_collection.create_index([
                ("stock", 1),
                ("minimum_stock", 1)
            ])
            
            # Text search index
            await products_collection.create_index([
                ("name", "text"),
                ("description", "text"),
                ("category", "text"),
                ("sku", "text"),
                ("supplier", "text")
            ])
            
            # Sales collection indexes
            sales_collection = self.db["sales"]
            
            # Unique index on invoice number
            await sales_collection.create_index("invoice_number", unique=True)
            
            # Index for date range queries
            await sales_collection.create_index("sale_date")
            
            # Index for product lookups
            await sales_collection.create_index("product_id")
            
            # Index for category filtering
            await sales_collection.create_index("category")
            
            # Index for customer lookups
            await sales_collection.create_index("customer_name")
            
            # Compound indexes for common queries
            await sales_collection.create_index([
                ("sale_date", -1),
                ("category", 1)
            ])
            
            # Text search indexes
            await sales_collection.create_index([
                ("customer_name", "text"),
                ("product_name", "text"),
                ("invoice_number", "text")
            ])
            
            logger.debug("All indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Failed to create indexes: {str(e)}")
    
    def get_collection(self, collection_name: str):
        """
        Get a collection from the database.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection object
            
        Raises:
            Exception: If database is not connected
        """
        if self.db is None:
            raise Exception("Database not connected")
        return self.db[collection_name]
    
    @property
    def is_connected(self) -> bool:
        """
        Check if database is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self._is_connected and self.db is not None


# Create a singleton instance
mongodb = MongoDB()


async def get_database() -> MongoDB:
    """
    Dependency injection function to get MongoDB instance.
    
    Returns:
        MongoDB: MongoDB connection manager instance
    """
    return mongodb
