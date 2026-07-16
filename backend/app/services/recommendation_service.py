"""
Recommendation service for business recommendations.
"""
import pandas as pd
from typing import Dict, Any, List
import logging

from app.database.mongodb import mongodb
from app.ai.recommendation_engine import recommendation_engine
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class RecommendationService:
    """
    Service for generating business recommendations.
    """
    
    def __init__(self):
        """Initialize the recommendation service."""
        self.sales_collection = "sales"
        self.products_collection = "products"
    
    async def get_collection(self, collection_name: str):
        """Get a collection from MongoDB."""
        return mongodb.get_collection(collection_name)
    
    async def _load_data(self) -> tuple:
        """Load product and sales data."""
        try:
            sales_collection = await self.get_collection(self.sales_collection)
            products_collection = await self.get_collection(self.products_collection)
            
            # Get all sales data
            sales_cursor = sales_collection.find({})
            sales_data = await sales_cursor.to_list(length=None)
            
            # Get all products data
            products_cursor = products_collection.find({})
            products_data = await products_cursor.to_list(length=None)
            
            # Convert to DataFrames
            sales_df = pd.DataFrame(sales_data) if sales_data else pd.DataFrame()
            products_df = pd.DataFrame(products_data) if products_data else pd.DataFrame()
            
            return sales_df, products_df
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    async def _calculate_metrics(self, sales_df: pd.DataFrame, products_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate business metrics from sales and products data.
        
        Args:
            sales_df: Sales DataFrame
            products_df: Products DataFrame
            
        Returns:
            Dict[str, Any]: Calculated metrics
        """
        metrics = {
            'revenue_growth': 0.0,
            'forecast_accuracy': 70.0,
            'total_revenue': 0.0,
            'total_profit': 0.0,
            'profit_margin': 0.0,
            'total_products': len(products_df) if not products_df.empty else 0,
            'total_sales': len(sales_df) if not sales_df.empty else 0
        }
        
        if not sales_df.empty and 'total_sale_amount' in sales_df.columns:
            # Calculate total revenue
            total_revenue = float(sales_df['total_sale_amount'].sum())
            metrics['total_revenue'] = total_revenue
            
            # Calculate profit
            if 'profit' in sales_df.columns:
                total_profit = float(sales_df['profit'].sum())
                metrics['total_profit'] = total_profit
                metrics['profit_margin'] = float((total_profit / total_revenue * 100) if total_revenue > 0 else 0)
            
            # Calculate growth (compare last 7 days to previous 7 days)
            if 'sale_date' in sales_df.columns:
                try:
                    sales_df_copy = sales_df.copy()
                    sales_df_copy['sale_date'] = pd.to_datetime(sales_df_copy['sale_date'])
                    
                    # Get date range
                    if not sales_df_copy.empty:
                        today = sales_df_copy['sale_date'].max()
                        last_7_days = sales_df_copy[sales_df_copy['sale_date'] >= today - pd.Timedelta(days=7)]
                        previous_7_days = sales_df_copy[
                            (sales_df_copy['sale_date'] >= today - pd.Timedelta(days=14)) & 
                            (sales_df_copy['sale_date'] < today - pd.Timedelta(days=7))
                        ]
                        
                        last_7_revenue = float(last_7_days['total_sale_amount'].sum())
                        prev_7_revenue = float(previous_7_days['total_sale_amount'].sum())
                        
                        if prev_7_revenue > 0:
                            metrics['revenue_growth'] = float(((last_7_revenue - prev_7_revenue) / prev_7_revenue) * 100)
                        elif last_7_revenue > 0:
                            metrics['revenue_growth'] = 100.0  # New business with growth
                except Exception as e:
                    logger.warning(f"Could not calculate revenue growth: {str(e)}")
        
        # Calculate additional metrics from products
        if not products_df.empty:
            if 'stock' in products_df.columns:
                total_stock = int(products_df['stock'].sum())
                metrics['total_stock'] = total_stock
                
                # Calculate inventory value if purchase_price exists
                if 'purchase_price' in products_df.columns:
                    inventory_value = float((products_df['stock'] * products_df['purchase_price']).sum())
                    metrics['inventory_value'] = inventory_value
            
            # Count active products
            if 'status' in products_df.columns:
                active_products = len(products_df[products_df['status'] == 'active'])
                metrics['active_products'] = active_products
        
        # Calculate average order value
        if not sales_df.empty and 'total_sale_amount' in sales_df.columns:
            if 'invoice_number' in sales_df.columns:
                unique_invoices = sales_df['invoice_number'].nunique()
                if unique_invoices > 0:
                    metrics['average_order_value'] = float(total_revenue / unique_invoices)
        
        return metrics
    
    async def get_all_recommendations(self) -> Dict[str, Any]:
        """
        Get all recommendations.
        
        Returns:
            Dict[str, Any]: All recommendations
        """
        try:
            # Load data
            sales_df, products_df = await self._load_data()
            
            # Calculate metrics
            metrics = await self._calculate_metrics(sales_df, products_df)
            
            # Generate recommendations
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, metrics
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            raise AppException(
                message=f"Failed to generate recommendations: {str(e)}",
                status_code=500,
                error_code="RECOMMENDATION_FAILED"
            )
    
    async def get_restock_recommendations(self) -> List[Dict[str, Any]]:
        """Get restock recommendations."""
        try:
            sales_df, products_df = await self._load_data()
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, {}
            )
            return recommendations.get('restock', [])
        except Exception as e:
            logger.error(f"Error getting restock recommendations: {str(e)}")
            raise
    
    async def get_pricing_recommendations(self) -> List[Dict[str, Any]]:
        """Get pricing recommendations."""
        try:
            sales_df, products_df = await self._load_data()
            metrics = await self._calculate_metrics(sales_df, products_df)
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, metrics
            )
            return recommendations.get('pricing', [])
        except Exception as e:
            logger.error(f"Error getting pricing recommendations: {str(e)}")
            raise
    
    async def get_dead_stock(self) -> List[Dict[str, Any]]:
        """Get dead stock products."""
        try:
            sales_df, products_df = await self._load_data()
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, {}
            )
            # Dead stock are products with very low performance scores
            performance = recommendations.get('performance_scores', [])
            dead_stock = [p for p in performance if p.get('score', 0) < 30]
            return dead_stock
        except Exception as e:
            logger.error(f"Error getting dead stock: {str(e)}")
            raise
    
    async def get_loss_products(self) -> List[Dict[str, Any]]:
        """Get loss-making products."""
        try:
            sales_df, products_df = await self._load_data()
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, {}
            )
            return recommendations.get('loss_products', [])
        except Exception as e:
            logger.error(f"Error getting loss products: {str(e)}")
            raise
    
    async def get_bundle_recommendations(self) -> List[Dict[str, Any]]:
        """Get bundle recommendations."""
        try:
            sales_df, products_df = await self._load_data()
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, {}
            )
            return recommendations.get('bundles', [])
        except Exception as e:
            logger.error(f"Error getting bundle recommendations: {str(e)}")
            raise
    
    async def get_performance_scores(self) -> List[Dict[str, Any]]:
        """Get product performance scores."""
        try:
            sales_df, products_df = await self._load_data()
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, {}
            )
            return recommendations.get('performance_scores', [])
        except Exception as e:
            logger.error(f"Error getting performance scores: {str(e)}")
            raise
    
    async def get_business_risk(self) -> Dict[str, Any]:
        """Get business risk analysis."""
        try:
            sales_df, products_df = await self._load_data()
            metrics = await self._calculate_metrics(sales_df, products_df)
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, metrics
            )
            return recommendations.get('business_risk', {})
        except Exception as e:
            logger.error(f"Error getting business risk: {str(e)}")
            raise
    
    async def get_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """Get optimization suggestions."""
        try:
            sales_df, products_df = await self._load_data()
            metrics = await self._calculate_metrics(sales_df, products_df)
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, metrics
            )
            return recommendations.get('optimizations', [])
        except Exception as e:
            logger.error(f"Error getting optimization suggestions: {str(e)}")
            raise
    
    async def get_executive_summary(self) -> Dict[str, Any]:
        """
        Generate executive summary.
        
        Returns:
            Dict[str, Any]: Executive summary
        """
        try:
            sales_df, products_df = await self._load_data()
            metrics = await self._calculate_metrics(sales_df, products_df)
            recommendations = await recommendation_engine.generate_all_recommendations(
                products_df, sales_df, metrics
            )
            
            # Extract key information
            restock_count = len(recommendations.get('restock', []))
            pricing_count = len(recommendations.get('pricing', []))
            loss_count = len(recommendations.get('loss_products', []))
            risk = recommendations.get('business_risk', {})
            
            # Count high priority recommendations
            high_priority = 0
            for key, value in recommendations.items():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and item.get('priority') == 'high':
                            high_priority += 1
            
            # Get top performing products
            performance = recommendations.get('performance_scores', [])
            top_products = performance[:3] if performance else []
            
            summary = {
                "period": "daily",
                "generated_at": recommendations.get('generated_at', ''),
                "total_recommendations": recommendations.get('total_recommendations', 0),
                "high_priority": high_priority,
                "restock_needed": restock_count,
                "pricing_suggestions": pricing_count,
                "loss_products": loss_count,
                "business_risk": risk.get('risk_level', 'Unknown'),
                "risk_score": risk.get('risk_score', 0),
                "total_products": metrics.get('total_products', 0),
                "total_sales": metrics.get('total_sales', 0),
                "total_revenue": metrics.get('total_revenue', 0),
                "total_profit": metrics.get('total_profit', 0),
                "profit_margin": metrics.get('profit_margin', 0),
                "top_products": top_products,
                "summary": self._generate_summary_text(
                    restock_count=restock_count,
                    pricing_count=pricing_count,
                    loss_count=loss_count,
                    risk=risk,
                    metrics=metrics
                )
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            raise AppException(
                message=f"Failed to generate executive summary: {str(e)}",
                status_code=500,
                error_code="EXECUTIVE_SUMMARY_FAILED"
            )
    
    def _generate_summary_text(
        self,
        restock_count: int,
        pricing_count: int,
        loss_count: int,
        risk: Dict[str, Any],
        metrics: Dict[str, Any]
    ) -> str:
        """
        Generate human-readable summary text.
        
        Args:
            restock_count: Number of restock recommendations
            pricing_count: Number of pricing recommendations
            loss_count: Number of loss products
            risk: Business risk data
            metrics: Business metrics
            
        Returns:
            str: Summary text
        """
        summary_parts = []
        
        # Revenue and profit
        revenue = metrics.get('total_revenue', 0)
        profit = metrics.get('total_profit', 0)
        margin = metrics.get('profit_margin', 0)
        
        if revenue > 0:
            summary_parts.append(f"Total revenue: ${revenue:,.2f}")
        if profit > 0:
            summary_parts.append(f"Total profit: ${profit:,.2f}")
        if margin > 0:
            summary_parts.append(f"Profit margin: {margin:.1f}%")
        
        # Risk level
        risk_level = risk.get('risk_level', 'Unknown')
        summary_parts.append(f"Business risk: {risk_level}")
        
        # Recommendations
        if restock_count > 0:
            summary_parts.append(f"{restock_count} products need restocking")
        if pricing_count > 0:
            summary_parts.append(f"{pricing_count} products have pricing recommendations")
        if loss_count > 0:
            summary_parts.append(f"{loss_count} products are making losses")
        
        # Overall assessment
        if risk_level == "Low Risk" and restock_count == 0 and loss_count == 0:
            summary_parts.append("Business is performing well - maintain current strategy")
        elif risk_level == "Critical Risk" or loss_count > 3:
            summary_parts.append("⚠️ Critical issues detected - immediate action required")
        else:
            summary_parts.append("📈 Some improvements needed - review recommendations")
        
        return ". ".join(summary_parts)


# Create singleton instance
recommendation_service = RecommendationService()