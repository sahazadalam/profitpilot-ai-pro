"""
Dynamic pricing engine for product pricing recommendations.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PricingEngine:
    """
    Engine for generating dynamic pricing recommendations.
    """
    
    def __init__(self):
        """Initialize the pricing engine."""
        pass
    
    def generate_pricing_recommendations(
        self,
        products_df: pd.DataFrame,
        sales_df: pd.DataFrame,
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate pricing recommendations for products.
        
        Args:
            products_df: Products DataFrame
            sales_df: Sales DataFrame
            metrics: Business metrics
            
        Returns:
            List[Dict[str, Any]]: Pricing recommendations
        """
        recommendations = []
        
        if products_df.empty or sales_df.empty:
            return recommendations
        
        # Get sales velocity per product
        sales_velocity = self._calculate_sales_velocity(sales_df)
        
        # Get product profitability
        product_profitability = self._calculate_product_profitability(sales_df)
        
        for _, product in products_df.iterrows():
            product_id = str(product['_id'])
            product_name = product.get('name', 'Unknown')
            current_price = float(product.get('selling_price', 0))
            purchase_price = float(product.get('purchase_price', 0))
            stock = int(product.get('stock', 0))
            
            # Get metrics
            velocity = sales_velocity.get(product_id, 0)
            margin = product_profitability.get(product_id, {}).get('margin', 0)
            total_revenue = product_profitability.get(product_id, {}).get('revenue', 0)
            
            # Determine pricing action
            action, suggested_price, reason = self._determine_pricing_action(
                current_price=current_price,
                purchase_price=purchase_price,
                velocity=velocity,
                margin=margin,
                stock=stock,
                total_revenue=total_revenue
            )
            
            if action != "keep":
                # Calculate expected impact
                expected_revenue, expected_profit = self._calculate_expected_impact(
                    action=action,
                    current_price=current_price,
                    suggested_price=suggested_price,
                    purchase_price=purchase_price,
                    velocity=velocity,
                    price_elasticity=-1.5  # Default elasticity
                )
                
                recommendations.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "current_price": current_price,
                    "suggested_price": suggested_price,
                    "action": action,
                    "expected_revenue": expected_revenue,
                    "expected_profit": expected_profit,
                    "reason": reason
                })
        
        return recommendations
    
    def _calculate_sales_velocity(self, sales_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate sales velocity per product."""
        velocity = {}
        
        if sales_df.empty or 'product_id' not in sales_df.columns or 'quantity' not in sales_df.columns:
            return velocity
        
        if 'sale_date' in sales_df.columns:
            sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
            date_range = (sales_df['sale_date'].max() - sales_df['sale_date'].min()).days
            if date_range > 0:
                for product_id in sales_df['product_id'].unique():
                    product_sales = sales_df[sales_df['product_id'] == product_id]
                    velocity[product_id] = float(product_sales['quantity'].sum() / date_range)
            else:
                for product_id in sales_df['product_id'].unique():
                    product_sales = sales_df[sales_df['product_id'] == product_id]
                    velocity[product_id] = float(product_sales['quantity'].sum())
        else:
            for product_id in sales_df['product_id'].unique():
                product_sales = sales_df[sales_df['product_id'] == product_id]
                velocity[product_id] = float(product_sales['quantity'].sum())
        
        return velocity
    
    def _calculate_product_profitability(self, sales_df: pd.DataFrame) -> Dict[str, Dict]:
        """Calculate profitability per product."""
        profitability = {}
        
        if sales_df.empty:
            return profitability
        
        for product_id in sales_df['product_id'].unique():
            product_sales = sales_df[sales_df['product_id'] == product_id]
            revenue = float(product_sales['total_sale_amount'].sum() if 'total_sale_amount' in product_sales.columns else 0)
            profit = float(product_sales['profit'].sum() if 'profit' in product_sales.columns else 0)
            
            margin = (profit / revenue * 100) if revenue > 0 else 0
            
            profitability[product_id] = {
                'revenue': revenue,
                'profit': profit,
                'margin': float(margin)
            }
        
        return profitability
    
    def _determine_pricing_action(
        self,
        current_price: float,
        purchase_price: float,
        velocity: float,
        margin: float,
        stock: int,
        total_revenue: float
    ) -> tuple:
        """
        Determine pricing action for a product.
        """
        # Calculate current margin
        current_margin = ((current_price - purchase_price) / current_price * 100) if current_price > 0 else 0
        
        # High margin, low velocity -> consider price decrease
        if current_margin > 40 and velocity < 1:
            suggested_price = max(purchase_price * 1.2, current_price * 0.9)
            return "decrease", round(float(suggested_price), 2), "Low sales velocity with high margin - decreasing price may increase sales"
        
        # Low margin, high velocity -> consider price increase
        if current_margin < 20 and velocity > 5:
            suggested_price = current_price * 1.1
            return "increase", round(float(suggested_price), 2), "High sales velocity with low margin - increasing price may improve profitability"
        
        # High stock, low velocity -> consider discount
        if stock > 100 and velocity < 0.5:
            suggested_price = current_price * 0.85
            return "decrease", round(float(suggested_price), 2), "High stock with low sales - discount needed to move inventory"
        
        # Low stock, high velocity -> consider price increase
        if stock < 20 and velocity > 3:
            suggested_price = current_price * 1.15
            return "increase", round(float(suggested_price), 2), "Low stock with high demand - price increase can maximize profit"
        
        # Default: keep price
        return "keep", current_price, "Current pricing is optimal"
    
    def _calculate_expected_impact(
        self,
        action: str,
        current_price: float,
        suggested_price: float,
        purchase_price: float,
        velocity: float,
        price_elasticity: float = -1.5
    ) -> tuple:
        """
        Calculate expected revenue and profit impact.
        """
        # Estimate new quantity based on price elasticity
        price_change_pct = (suggested_price - current_price) / current_price if current_price > 0 else 0
        quantity_change_pct = price_elasticity * price_change_pct
        
        # Current quantity (assuming 30 days)
        current_quantity = velocity * 30
        
        # New quantity
        new_quantity = current_quantity * (1 + quantity_change_pct)
        new_quantity = max(0, new_quantity)
        
        # Calculate revenue and profit
        expected_revenue = float(new_quantity * suggested_price)
        expected_profit = float(new_quantity * (suggested_price - purchase_price))
        
        return round(expected_revenue, 2), round(expected_profit, 2)


# Create singleton instance
pricing_engine = PricingEngine()