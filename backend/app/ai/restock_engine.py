"""
Restock recommendation engine for inventory management.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class RestockEngine:
    """
    Engine for generating restock recommendations.
    """
    
    def __init__(self):
        """Initialize the restock engine."""
        pass
    
    def generate_restock_recommendations(
        self,
        products_df: pd.DataFrame,
        sales_df: pd.DataFrame,
        lead_time_days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Generate restock recommendations for products.
        
        Args:
            products_df: Products DataFrame
            sales_df: Sales DataFrame
            lead_time_days: Supplier lead time in days
            
        Returns:
            List[Dict[str, Any]]: Restock recommendations
        """
        recommendations = []
        
        if products_df.empty or sales_df.empty:
            return recommendations
        
        # Calculate sales velocity per product
        sales_velocity = self._calculate_sales_velocity(sales_df)
        
        for _, product in products_df.iterrows():
            try:
                product_id = str(product.get('_id', ''))
                product_name = str(product.get('name', 'Unknown'))
                current_stock = int(product.get('stock', 0))
                minimum_stock = int(product.get('minimum_stock', 5))
                
                # Get sales velocity for this product
                velocity = float(sales_velocity.get(product_id, 0.0))
                
                if velocity > 0:
                    # Calculate days until depletion
                    days_until_depletion = int(current_stock / velocity) if velocity > 0 else 0
                    
                    # Calculate recommended order quantity (30 days worth + safety stock)
                    recommended_quantity = int(velocity * 30 + minimum_stock)
                    
                    # Calculate reorder date
                    reorder_date = datetime.utcnow() + timedelta(days=max(0, days_until_depletion - lead_time_days))
                    
                    # Determine priority
                    if days_until_depletion < lead_time_days + 3:
                        priority = "high"
                        reason = f"Stock will deplete in {days_until_depletion} days (less than lead time of {lead_time_days} days)"
                    elif days_until_depletion < lead_time_days + 7:
                        priority = "medium"
                        reason = f"Stock will deplete in {days_until_depletion} days. Consider ordering soon."
                    else:
                        priority = "low"
                        reason = f"Stock is sufficient for {days_until_depletion} days"
                    
                    recommendations.append({
                        "product_id": product_id,
                        "product_name": product_name,
                        "current_stock": int(current_stock),
                        "recommended_quantity": int(recommended_quantity),
                        "recommended_date": reorder_date.strftime('%Y-%m-%d'),
                        "priority": priority,
                        "reason": reason,
                        "days_until_depletion": int(days_until_depletion),
                        "sales_velocity": float(round(velocity, 2))
                    })
            except Exception as e:
                logger.error(f"Error generating restock for product: {str(e)}")
                continue
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
        
        return recommendations
    
    def _calculate_sales_velocity(self, sales_df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate sales velocity per product (units sold per day).
        
        Args:
            sales_df: Sales DataFrame
            
        Returns:
            Dict[str, float]: Sales velocity per product
        """
        velocity = {}
        
        if sales_df.empty:
            return velocity
        
        try:
            if 'product_id' in sales_df.columns and 'quantity' in sales_df.columns and 'sale_date' in sales_df.columns:
                sales_df_copy = sales_df.copy()
                sales_df_copy['sale_date'] = pd.to_datetime(sales_df_copy['sale_date'])
                date_range = (sales_df_copy['sale_date'].max() - sales_df_copy['sale_date'].min()).days
                
                if date_range > 0:
                    for product_id in sales_df_copy['product_id'].unique():
                        product_sales = sales_df_copy[sales_df_copy['product_id'] == product_id]
                        total_quantity = float(product_sales['quantity'].sum())
                        velocity[str(product_id)] = float(total_quantity / date_range)
                else:
                    for product_id in sales_df_copy['product_id'].unique():
                        product_sales = sales_df_copy[sales_df_copy['product_id'] == product_id]
                        velocity[str(product_id)] = float(product_sales['quantity'].sum())
        except Exception as e:
            logger.error(f"Error calculating sales velocity: {str(e)}")
        
        return velocity


# Create singleton instance
restock_engine = RestockEngine()