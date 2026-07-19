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
    
    # ... rest of the code remains the same
