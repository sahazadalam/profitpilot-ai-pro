"""
Analytics service for business intelligence.
"""
from typing import Dict, Any, List
import logging

from app.database.mongodb import mongodb
from app.ai.analytics_engine import analytics_engine
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Analytics service handling business intelligence operations.
    """
    
    def __init__(self):
        """Initialize the analytics service."""
        self.sales_collection = "sales"
        self.products_collection = "products"
    
    async def get_collection(self, collection_name: str):
        """Get a collection from MongoDB."""
        return mongodb.get_collection(collection_name)
    
    async def _load_data(self):
        """Load sales and product data into analytics engine."""
        try:
            sales_collection = await self.get_collection(self.sales_collection)
            products_collection = await self.get_collection(self.products_collection)
            
            # Get all sales data
            sales_cursor = sales_collection.find({})
            sales_data = await sales_cursor.to_list(length=None)
            
            # Get all products data
            products_cursor = products_collection.find({})
            products_data = await products_cursor.to_list(length=None)
            
            # Load data into engine
            await analytics_engine.load_data(sales_data, products_data)
            
        except Exception as e:
            logger.error(f"Error loading data for analytics: {str(e)}")
            raise AppException(
                message=f"Failed to load data for analytics: {str(e)}",
                status_code=500,
                error_code="ANALYTICS_DATA_LOAD_FAILED"
            )
    
    async def get_revenue_analytics(self) -> Dict[str, Any]:
        """
        Get revenue analytics.
        
        Returns:
            Dict: Revenue analytics data
        """
        try:
            await self._load_data()
            return analytics_engine.get_revenue_analytics()
        except Exception as e:
            logger.error(f"Error getting revenue analytics: {str(e)}")
            raise
    
    async def get_profit_analytics(self) -> Dict[str, Any]:
        """
        Get profit analytics.
        
        Returns:
            Dict: Profit analytics data
        """
        try:
            await self._load_data()
            return analytics_engine.get_profit_analytics()
        except Exception as e:
            logger.error(f"Error getting profit analytics: {str(e)}")
            raise
    
    async def get_growth_analytics(self) -> Dict[str, Any]:
        """
        Get growth analytics.
        
        Returns:
            Dict: Growth analytics data
        """
        try:
            await self._load_data()
            return analytics_engine.get_growth_analytics()
        except Exception as e:
            logger.error(f"Error getting growth analytics: {str(e)}")
            raise
    
    async def get_business_health(self) -> Dict[str, Any]:
        """
        Get business health.
        
        Returns:
            Dict: Business health data
        """
        try:
            await self._load_data()
            return analytics_engine.get_business_health()
        except Exception as e:
            logger.error(f"Error getting business health: {str(e)}")
            raise
    
    async def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            List[Dict]: Top products data
        """
        try:
            await self._load_data()
            return analytics_engine.get_top_products(limit)
        except Exception as e:
            logger.error(f"Error getting top products: {str(e)}")
            raise
    
    async def get_worst_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get worst products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            List[Dict]: Worst products data
        """
        try:
            await self._load_data()
            return analytics_engine.get_worst_products(limit)
        except Exception as e:
            logger.error(f"Error getting worst products: {str(e)}")
            raise
    
    async def get_category_analytics(self) -> Dict[str, Any]:
        """
        Get category analytics.
        
        Returns:
            Dict: Category analytics data
        """
        try:
            await self._load_data()
            return analytics_engine.get_category_analytics()
        except Exception as e:
            logger.error(f"Error getting category analytics: {str(e)}")
            raise
    
    async def get_inventory_analytics(self) -> Dict[str, Any]:
        """
        Get inventory analytics.
        
        Returns:
            Dict: Inventory analytics data
        """
        try:
            await self._load_data()
            return analytics_engine.get_inventory_analytics()
        except Exception as e:
            logger.error(f"Error getting inventory analytics: {str(e)}")
            raise
    
    async def get_kpis(self) -> Dict[str, Any]:
        """
        Get KPIs.
        
        Returns:
            Dict: KPI data
        """
        try:
            await self._load_data()
            return analytics_engine.get_kpis()
        except Exception as e:
            logger.error(f"Error getting KPIs: {str(e)}")
            raise
    
    async def get_trends(self) -> Dict[str, Any]:
        """
        Get trends.
        
        Returns:
            Dict: Trend data
        """
        try:
            await self._load_data()
            return analytics_engine.get_trends()
        except Exception as e:
            logger.error(f"Error getting trends: {str(e)}")
            raise
    
    async def generate_report(self) -> Dict[str, Any]:
        """
        Generate AI-style report.
        
        Returns:
            Dict: Report data
        """
        try:
            await self._load_data()
            return analytics_engine.generate_report()
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
    
    async def generate_insights(self) -> List[Dict[str, Any]]:
        """
        Generate business insights.
        
        Returns:
            List[Dict]: Business insights
        """
        try:
            await self._load_data()
            return analytics_engine.generate_insights()
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            raise


# Create singleton instance
analytics_service = AnalyticsService()