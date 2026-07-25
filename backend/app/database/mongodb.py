"""
MongoDB connection module for ProfitPilot AI Pro.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    """
    MongoDB connection manager.
    """

    def __init__(self):
        """Initialize the MongoDB connection manager."""
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self._is_connected: bool = False

    async def connect(self) -> None:
        """
        Establish connection to MongoDB.
        """
        try:
            logger.info("Connecting to MongoDB...")

            mongodb_url = settings.MONGODB_URL

            if "mongodb+srv" in mongodb_url:
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

            # Verify connection
            await self.client.admin.command("ping")

            # Select database
            self.db = self.client[settings.MONGODB_DB_NAME]
            self._is_connected = True

            logger.info(
                f"Successfully connected to MongoDB database: {settings.MONGODB_DB_NAME}"
            )

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
            # Users collection
            users_collection = self.db["users"]

            await users_collection.create_index("email", unique=True)
            await users_collection.create_index("role")
            await users_collection.create_index("is_active")

            # Products collection
            products_collection = self.db["products"]

            await products_collection.create_index("sku", unique=True)
            await products_collection.create_index("name", unique=True)

            await products_collection.create_index("category")
            await products_collection.create_index("status")
            await products_collection.create_index("supplier")

            await products_collection.create_index([
                ("category", 1),
                ("status", 1),
                ("selling_price", 1)
            ])

            await products_collection.create_index([
                ("stock", 1),
                ("minimum_stock", 1)
            ])

            await products_collection.create_index([
                ("name", "text"),
                ("description", "text"),
                ("category", "text"),
                ("sku", "text"),
                ("supplier", "text")
            ])

            # Sales collection
            sales_collection = self.db["sales"]

            await sales_collection.create_index("invoice_number", unique=True)
            await sales_collection.create_index("sale_date")
            await sales_collection.create_index("product_id")
            await sales_collection.create_index("category")
            await sales_collection.create_index("customer_name")

            await sales_collection.create_index([
                ("sale_date", -1),
                ("category", 1)
            ])

            await sales_collection.create_index([
                ("customer_name", "text"),
                ("product_name", "text"),
                ("invoice_number", "text")
            ])

            logger.info("MongoDB indexes created successfully")

        except Exception as e:
            logger.warning(f"Failed to create indexes: {str(e)}")

    def get_collection(self, collection_name: str):
        """
        Get a MongoDB collection.
        """
        if self.db is None:
            raise Exception("Database not connected")

        return self.db[collection_name]

    @property
    def is_connected(self) -> bool:
        """
        Check whether MongoDB is connected.
        """
        return self._is_connected and self.db is not None


# Singleton instance
mongodb = MongoDB()


async def get_database() -> MongoDB:
    """
    Dependency function.
    """
    return mongodb
