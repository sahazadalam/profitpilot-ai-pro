"""
Loss detection engine for identifying unprofitable products.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class LossEngine:
    """
    Engine for detecting loss-making products and suggesting actions.
    """
    
    def __init__(self):
        """Initialize the loss engine."""
        pass
    
    def detect_loss_products(
        self,
        products_df: pd.DataFrame,
        sales_df: pd.DataFrame
    ) -> List[Dict[str, Any]]:
        """
        Detect loss-making products.
        
        Args:
            products_df: Products DataFrame
            sales_df: Sales DataFrame
            
        Returns:
            List[Dict[str, Any]]: Loss products analysis
        """
        loss_products = []
        
        if products_df.empty or sales_df.empty:
            return loss_products
        
        # Calculate profitability per product
        product_profitability = self._calculate_profitability(sales_df)
        
        for _, product in products_df.iterrows():
            product_id = str(product['_id'])
            product_name = product.get('name', 'Unknown')
            category = product.get('category', 'Unknown')
            current_price = product.get('selling_price', 0)
            purchase_price = product.get('purchase_price', 0)
            stock = product.get('stock', 0)
            
            # Get profitability metrics
            profit_metrics = product_profitability.get(product_id, {})
            total_profit = profit_metrics.get('total_profit', 0)
            margin = profit_metrics.get('margin', 0)
            revenue = profit_metrics.get('revenue', 0)
            quantity_sold = profit_metrics.get('quantity', 0)
            
            # Determine if product is making a loss
            if total_profit < 0 and revenue > 0:
                loss_products.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "category": category,
                    "current_price": current_price,
                    "purchase_price": purchase_price,
                    "margin": round(margin, 2),
                    "total_profit": round(total_profit, 2),
                    "total_revenue": round(revenue, 2),
                    "quantity_sold": quantity_sold,
                    "stock": stock,
                    "reason": f"Product is making a loss of ${abs(total_profit):.2f} with {quantity_sold} units sold",
                    "recommendation": self._suggest_action(
                        margin=margin,
                        stock=stock,
                        quantity_sold=quantity_sold
                    )
                })
        
        # Sort by profit (worst first)
        loss_products.sort(key=lambda x: x['total_profit'])
        
        return loss_products
    
    def _calculate_profitability(self, sales_df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Calculate profitability per product.
        """
        profitability = {}
        
        if sales_df.empty:
            return profitability
        
        for product_id in sales_df['product_id'].unique():
            product_sales = sales_df[sales_df['product_id'] == product_id]
            revenue = product_sales['total_sale_amount'].sum() if 'total_sale_amount' in product_sales.columns else 0
            profit = product_sales['profit'].sum() if 'profit' in product_sales.columns else 0
            quantity = product_sales['quantity'].sum() if 'quantity' in product_sales.columns else 0
            
            margin = (profit / revenue * 100) if revenue > 0 else 0
            
            profitability[product_id] = {
                'revenue': revenue,
                'total_profit': profit,
                'margin': margin,
                'quantity': quantity
            }
        
        return profitability
    
    def _suggest_action(self, margin: float, stock: int, quantity_sold: int) -> str:
        """
        Suggest action for loss-making product.
        """
        if margin > 0 and quantity_sold > 0:
            return "REVIEW - Product may need pricing adjustment"
        elif stock > 50:
            return "DISCOUNT - Clear excess inventory to minimize losses"
        elif quantity_sold < 5:
            return "REMOVE - Consider discontinuing this product"
        else:
            return "ANALYZE - Investigate cost structure and pricing strategy"


# Create singleton instance
loss_engine = LossEngine()