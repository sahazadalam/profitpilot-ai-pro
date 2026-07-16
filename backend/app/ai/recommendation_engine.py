"""
Main recommendation engine orchestrating all AI recommendations.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
import logging

from app.ai.restock_engine import restock_engine
from app.ai.pricing_engine import pricing_engine
from app.ai.loss_engine import loss_engine
from app.ai.bundle_engine import bundle_engine
from app.ai.risk_engine import risk_engine
from app.utils.recommendation_utils import (
    calculate_performance_score,
    generate_optimization_suggestions
)

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Orchestrates all recommendation engines.
    """
    
    def __init__(self):
        """Initialize the recommendation engine."""
        pass
    
    async def generate_all_recommendations(
        self,
        products_df: pd.DataFrame,
        sales_df: pd.DataFrame,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate all types of recommendations.
        
        Args:
            products_df: Products DataFrame
            sales_df: Sales DataFrame
            metrics: Business metrics
            
        Returns:
            Dict[str, Any]: All recommendations
        """
        recommendations = {}
        
        # 1. Restock recommendations
        recommendations['restock'] = restock_engine.generate_restock_recommendations(
            products_df, sales_df
        )
        
        # 2. Pricing recommendations
        recommendations['pricing'] = pricing_engine.generate_pricing_recommendations(
            products_df, sales_df, metrics
        )
        
        # 3. Loss products
        recommendations['loss_products'] = loss_engine.detect_loss_products(
            products_df, sales_df
        )
        
        # 4. Bundle recommendations
        recommendations['bundles'] = bundle_engine.generate_bundle_recommendations(
            sales_df, products_df
        )
        
        # 5. Performance scores
        recommendations['performance_scores'] = self._calculate_performance_scores(
            products_df, sales_df, metrics
        )
        
        # 6. Business risk
        recommendations['business_risk'] = risk_engine.calculate_business_risk(
            products_df, sales_df, metrics
        )
        
        # 7. Optimization suggestions
        recommendations['optimizations'] = generate_optimization_suggestions(
            products_df, sales_df, metrics
        )
        
        # Add metadata
        recommendations['generated_at'] = datetime.utcnow().isoformat()
        recommendations['total_recommendations'] = sum(
            len(v) for k, v in recommendations.items() 
            if k not in ['generated_at', 'total_recommendations'] and isinstance(v, list)
        )
        
        return recommendations
    
    def _calculate_performance_scores(
        self,
        products_df: pd.DataFrame,
        sales_df: pd.DataFrame,
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Calculate performance scores for all products.
        """
        performance_scores = []
        
        if products_df.empty:
            return performance_scores
        
        # Calculate sales velocity per product
        sales_velocity = self._calculate_sales_velocity(sales_df) if not sales_df.empty else {}
        
        # Calculate profitability per product
        profitability = self._calculate_profitability(sales_df) if not sales_df.empty else {}
        
        for _, product in products_df.iterrows():
            try:
                # Convert all values to Python native types
                product_id = str(product.get('_id', ''))
                product_name = str(product.get('name', 'Unknown'))
                category = str(product.get('category', 'Unknown'))
                
                # Get metrics with proper type conversion
                velocity = float(sales_velocity.get(product_id, 0.0))
                margin = float(profitability.get(product_id, {}).get('margin', 0.0))
                revenue_growth = float(profitability.get(product_id, {}).get('growth', 0.0))
                
                # Calculate stock health
                stock = int(product.get('stock', 0))
                min_stock = int(product.get('minimum_stock', 5))
                stock_health = float(min(100.0, (stock / (min_stock * 2)) * 100)) if min_stock > 0 else 50.0
                
                # Calculate demand forecast (using velocity as proxy)
                demand_forecast = float(velocity * 30)
                
                # Calculate performance score
                score = int(calculate_performance_score(
                    sales_velocity=velocity,
                    profit_margin=margin,
                    growth_rate=revenue_growth,
                    stock_health=stock_health,
                    demand_forecast=demand_forecast
                ))
                
                performance_scores.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "category": category,
                    "score": int(score),
                    "metrics": {
                        "sales_velocity": float(round(velocity, 2)),
                        "profit_margin": float(round(margin, 2)),
                        "growth_rate": float(round(revenue_growth, 2)),
                        "stock_health": float(round(stock_health, 2)),
                        "demand_forecast": float(round(demand_forecast, 2))
                    }
                })
            except Exception as e:
                logger.error(f"Error calculating performance for product: {str(e)}")
                continue
        
        # Sort by score (best first)
        performance_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return performance_scores
    
    def _calculate_sales_velocity(self, sales_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate sales velocity per product."""
        velocity = {}
        
        if sales_df.empty or 'product_id' not in sales_df.columns or 'quantity' not in sales_df.columns:
            return velocity
        
        try:
            if 'sale_date' in sales_df.columns:
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
            else:
                for product_id in sales_df['product_id'].unique():
                    product_sales = sales_df[sales_df['product_id'] == product_id]
                    velocity[str(product_id)] = float(product_sales['quantity'].sum())
        except Exception as e:
            logger.error(f"Error calculating sales velocity: {str(e)}")
        
        return velocity
    
    def _calculate_profitability(self, sales_df: pd.DataFrame) -> Dict[str, Dict]:
        """Calculate profitability per product."""
        profitability = {}
        
        if sales_df.empty:
            return profitability
        
        try:
            for product_id in sales_df['product_id'].unique():
                product_sales = sales_df[sales_df['product_id'] == product_id]
                revenue = float(product_sales['total_sale_amount'].sum() if 'total_sale_amount' in product_sales.columns else 0)
                profit = float(product_sales['profit'].sum() if 'profit' in product_sales.columns else 0)
                
                margin = float((profit / revenue * 100) if revenue > 0 else 0)
                
                profitability[str(product_id)] = {
                    'revenue': float(revenue),
                    'profit': float(profit),
                    'margin': float(margin),
                    'growth': 0.0  # Placeholder for growth
                }
        except Exception as e:
            logger.error(f"Error calculating profitability: {str(e)}")
        
        return profitability


# Create singleton instance
recommendation_engine = RecommendationEngine()