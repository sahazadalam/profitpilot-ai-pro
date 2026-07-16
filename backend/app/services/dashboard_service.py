"""
Dashboard service for business intelligence.
Provides summary statistics and analytics for the dashboard.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
from bson import ObjectId
import logging

from app.database.mongodb import mongodb
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class DashboardService:
    """
    Dashboard service providing business intelligence statistics.
    """
    
    def __init__(self):
        """Initialize the dashboard service."""
        self.products_collection = "products"
        self.sales_collection = "sales"
    
    async def get_products_collection(self):
        """Get the products collection from MongoDB."""
        return mongodb.get_collection(self.products_collection)
    
    async def get_sales_collection(self):
        """Get the sales collection from MongoDB."""
        return mongodb.get_collection(self.sales_collection)
    
    async def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard summary.
        
        Returns:
            Dict: Dashboard summary data
        """
        try:
            products_collection = await self.get_products_collection()
            sales_collection = await self.get_sales_collection()
            
            # Get product stats
            product_pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_products": {"$sum": 1},
                        "total_stock": {"$sum": "$stock"},
                        "inventory_value": {"$sum": {"$multiply": ["$stock", "$purchase_price"]}},
                        "out_of_stock": {
                            "$sum": {"$cond": [{"$eq": ["$stock", 0]}, 1, 0]}
                        },
                        "low_stock": {
                            "$sum": {"$cond": [
                                {"$lte": ["$stock", "$minimum_stock"]},
                                1,
                                0
                            ]}
                        }
                    }
                }
            ]
            
            product_result = await products_collection.aggregate(product_pipeline).to_list(length=1)
            product_stats = product_result[0] if product_result else {}
            
            # Get sales stats
            # Today's sales
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            sales_pipeline = [
                {
                    "$match": {
                        "sale_date": {"$gte": today_start}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "today_sales": {"$sum": 1},
                        "revenue": {"$sum": "$total_sale_amount"},
                        "profit": {"$sum": "$profit"}
                    }
                }
            ]
            
            today_result = await sales_collection.aggregate(sales_pipeline).to_list(length=1)
            today_stats = today_result[0] if today_result else {}
            
            # Get total sales and revenue
            total_pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_sales": {"$sum": 1},
                        "total_revenue": {"$sum": "$total_sale_amount"},
                        "total_profit": {"$sum": "$profit"}
                    }
                }
            ]
            
            total_result = await sales_collection.aggregate(total_pipeline).to_list(length=1)
            total_stats = total_result[0] if total_result else {}
            
            return {
                "total_products": product_stats.get("total_products", 0),
                "total_sales": total_stats.get("total_sales", 0),
                "today_sales": today_stats.get("today_sales", 0),
                "revenue": total_stats.get("total_revenue", 0.0),
                "profit": total_stats.get("total_profit", 0.0),
                "inventory_value": product_stats.get("inventory_value", 0.0),
                "out_of_stock": product_stats.get("out_of_stock", 0),
                "low_stock": product_stats.get("low_stock", 0)
            }
            
        except Exception as e:
            logger.error(f"Error in get_dashboard_summary: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to get dashboard summary: {str(e)}",
                status_code=500,
                error_code="DASHBOARD_SUMMARY_FAILED"
            )
    
    async def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top selling products.
        
        Args:
            limit: Number of products to return
            
        Returns:
            List[Dict]: Top products with sales data
        """
        try:
            sales_collection = await self.get_sales_collection()
            
            pipeline = [
                {
                    "$group": {
                        "_id": "$product_id",
                        "product_name": {"$first": "$product_name"},
                        "category": {"$first": "$category"},
                        "total_quantity_sold": {"$sum": "$quantity"},
                        "total_revenue": {"$sum": "$total_sale_amount"},
                        "total_profit": {"$sum": "$profit"}
                    }
                },
                {"$sort": {"total_quantity_sold": -1}},
                {"$limit": limit},
                {
                    "$project": {
                        "product_id": {"$toString": "$_id"},
                        "product_name": 1,
                        "category": 1,
                        "total_quantity_sold": 1,
                        "total_revenue": {"$round": ["$total_revenue", 2]},
                        "total_profit": {"$round": ["$total_profit", 2]}
                    }
                }
            ]
            
            results = await sales_collection.aggregate(pipeline).to_list(length=limit)
            return results
            
        except Exception as e:
            logger.error(f"Error in get_top_products: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to get top products: {str(e)}",
                status_code=500,
                error_code="TOP_PRODUCTS_FAILED"
            )
    
    async def get_recent_sales(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent sales.
        
        Args:
            limit: Number of sales to return
            
        Returns:
            List[Dict]: Recent sales
        """
        try:
            sales_collection = await self.get_sales_collection()
            
            # Simple find with sort and limit
            cursor = sales_collection.find(
                {},
                {
                    "_id": 1,
                    "invoice_number": 1,
                    "product_name": 1,
                    "quantity": 1,
                    "total_sale_amount": 1,
                    "customer_name": 1,
                    "sale_date": 1
                }
            ).sort("sale_date", -1).limit(limit)
            
            results = await cursor.to_list(length=limit)
            
            # Convert to dict with string IDs
            formatted_results = []
            for sale in results:
                formatted_results.append({
                    "id": str(sale["_id"]),
                    "invoice_number": sale.get("invoice_number"),
                    "product_name": sale.get("product_name"),
                    "quantity": sale.get("quantity"),
                    "total_sale_amount": sale.get("total_sale_amount"),
                    "customer_name": sale.get("customer_name"),
                    "sale_date": sale.get("sale_date").strftime("%Y-%m-%d %H:%M") if sale.get("sale_date") else None
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in get_recent_sales: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to get recent sales: {str(e)}",
                status_code=500,
                error_code="RECENT_SALES_FAILED"
            )
    
    async def get_revenue_chart_data(self, days: int = 30) -> Dict[str, Any]:
        """
        Get revenue chart data for the last N days.
        
        Args:
            days: Number of days to include
            
        Returns:
            Dict: Chart data with labels, revenue, profit
        """
        try:
            sales_collection = await self.get_sales_collection()
            
            start_date = datetime.utcnow() - timedelta(days=days)
            
            pipeline = [
                {
                    "$match": {
                        "sale_date": {"$gte": start_date}
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$sale_date"}}
                        },
                        "revenue": {"$sum": "$total_sale_amount"},
                        "profit": {"$sum": "$profit"},
                        "count": {"$sum": 1}
                    }
                },
                {"$sort": {"_id.date": 1}},
                {
                    "$project": {
                        "date": "$_id.date",
                        "revenue": {"$round": ["$revenue", 2]},
                        "profit": {"$round": ["$profit", 2]},
                        "count": 1
                    }
                }
            ]
            
            results = await sales_collection.aggregate(pipeline).to_list(length=days)
            
            # Fill in missing dates
            labels = []
            revenue_data = []
            profit_data = []
            
            # Create a dictionary for quick lookup
            data_dict = {item["date"]: item for item in results}
            
            # Generate all dates in range
            current_date = start_date
            while current_date <= datetime.utcnow():
                date_str = current_date.strftime("%Y-%m-%d")
                labels.append(date_str)
                
                if date_str in data_dict:
                    revenue_data.append(data_dict[date_str]["revenue"])
                    profit_data.append(data_dict[date_str]["profit"])
                else:
                    revenue_data.append(0.0)
                    profit_data.append(0.0)
                
                current_date += timedelta(days=1)
            
            return {
                "labels": labels,
                "revenue": revenue_data,
                "profit": profit_data
            }
            
        except Exception as e:
            logger.error(f"Error in get_revenue_chart_data: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to get revenue chart data: {str(e)}",
                status_code=500,
                error_code="REVENUE_CHART_FAILED"
            )
    
    async def get_profit_summary(self) -> Dict[str, Any]:
        """
        Get profit summary (daily, weekly, monthly).
        
        Returns:
            Dict: Profit summary data
        """
        try:
            sales_collection = await self.get_sales_collection()
            
            now = datetime.utcnow()
            
            # Daily (today)
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Weekly (last 7 days)
            week_start = now - timedelta(days=7)
            
            # Monthly (last 30 days)
            month_start = now - timedelta(days=30)
            
            # Get daily stats
            daily_pipeline = [
                {"$match": {"sale_date": {"$gte": today_start}}},
                {
                    "$group": {
                        "_id": None,
                        "revenue": {"$sum": "$total_sale_amount"},
                        "profit": {"$sum": "$profit"},
                        "count": {"$sum": 1}
                    }
                }
            ]
            daily_result = await sales_collection.aggregate(daily_pipeline).to_list(length=1)
            daily = daily_result[0] if daily_result else {"revenue": 0, "profit": 0, "count": 0}
            
            # Get weekly stats
            weekly_pipeline = [
                {"$match": {"sale_date": {"$gte": week_start}}},
                {
                    "$group": {
                        "_id": None,
                        "revenue": {"$sum": "$total_sale_amount"},
                        "profit": {"$sum": "$profit"},
                        "count": {"$sum": 1}
                    }
                }
            ]
            weekly_result = await sales_collection.aggregate(weekly_pipeline).to_list(length=1)
            weekly = weekly_result[0] if weekly_result else {"revenue": 0, "profit": 0, "count": 0}
            
            # Get monthly stats
            monthly_pipeline = [
                {"$match": {"sale_date": {"$gte": month_start}}},
                {
                    "$group": {
                        "_id": None,
                        "revenue": {"$sum": "$total_sale_amount"},
                        "profit": {"$sum": "$profit"},
                        "count": {"$sum": 1}
                    }
                }
            ]
            monthly_result = await sales_collection.aggregate(monthly_pipeline).to_list(length=1)
            monthly = monthly_result[0] if monthly_result else {"revenue": 0, "profit": 0, "count": 0}
            
            return {
                "daily": {
                    "revenue": round(daily["revenue"], 2),
                    "profit": round(daily["profit"], 2),
                    "count": daily["count"]
                },
                "weekly": {
                    "revenue": round(weekly["revenue"], 2),
                    "profit": round(weekly["profit"], 2),
                    "count": weekly["count"]
                },
                "monthly": {
                    "revenue": round(monthly["revenue"], 2),
                    "profit": round(monthly["profit"], 2),
                    "count": monthly["count"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error in get_profit_summary: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to get profit summary: {str(e)}",
                status_code=500,
                error_code="PROFIT_SUMMARY_FAILED"
            )


# Create singleton instance
dashboard_service = DashboardService()