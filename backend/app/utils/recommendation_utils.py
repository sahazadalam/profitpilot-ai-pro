"""
Recommendation utilities for business recommendations.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def calculate_performance_score(
    sales_velocity: float,
    profit_margin: float,
    growth_rate: float,
    stock_health: float,
    demand_forecast: float
) -> int:
    """
    Calculate product performance score (0-100).
    
    Args:
        sales_velocity: Number of units sold per day
        profit_margin: Profit margin percentage
        growth_rate: Sales growth rate percentage
        stock_health: Stock health score (0-100)
        demand_forecast: Forecasted demand
        
    Returns:
        int: Performance score (0-100)
    """
    weights = {
        'sales_velocity': 0.25,
        'profit_margin': 0.25,
        'growth_rate': 0.20,
        'stock_health': 0.15,
        'demand_forecast': 0.15
    }
    
    # Convert all values to float
    sales_velocity = float(sales_velocity)
    profit_margin = float(profit_margin)
    growth_rate = float(growth_rate)
    stock_health = float(stock_health)
    demand_forecast = float(demand_forecast)
    
    # Normalize each metric to 0-100
    scores = {}
    
    # Sales velocity (normalize: 0-100, assuming max 100 units/day)
    scores['sales_velocity'] = float(min(100.0, sales_velocity * 10)) if sales_velocity > 0 else 0.0
    
    # Profit margin (0-100)
    scores['profit_margin'] = float(min(100.0, profit_margin * 2)) if profit_margin > 0 else 0.0
    
    # Growth rate (0-100)
    scores['growth_rate'] = float(min(100.0, growth_rate * 5 + 50)) if growth_rate != 0 else 50.0
    
    # Stock health
    scores['stock_health'] = float(stock_health)
    
    # Demand forecast
    scores['demand_forecast'] = float(min(100.0, demand_forecast * 2)) if demand_forecast > 0 else 50.0
    
    # Calculate weighted score
    weighted_score = sum(float(scores[key]) * float(weights[key]) for key in weights.keys())
    
    return int(weighted_score)


def generate_optimization_suggestions(
    products_df: pd.DataFrame,
    sales_df: pd.DataFrame,
    metrics: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Generate business optimization suggestions.
    
    Args:
        products_df: Products DataFrame
        sales_df: Sales DataFrame
        metrics: Business metrics
        
    Returns:
        List[Dict[str, Any]]: Optimization suggestions
    """
    suggestions = []
    
    # 1. Inventory suggestions
    if products_df is not None and not products_df.empty:
        # Check low stock
        if 'stock' in products_df.columns and 'minimum_stock' in products_df.columns:
            low_stock = products_df[products_df['stock'] <= products_df['minimum_stock']]
            if len(low_stock) > 0:
                suggestions.append({
                    "category": "inventory",
                    "message": f"Increase inventory for {len(low_stock)} products with low stock",
                    "priority": "high",
                    "impact": "prevent stockouts"
                })
            
            # Check excess stock
            high_stock = products_df[products_df['stock'] > products_df['minimum_stock'] * 3]
            if len(high_stock) > 0:
                suggestions.append({
                    "category": "inventory",
                    "message": f"Reduce inventory for {len(high_stock)} products with excess stock",
                    "priority": "medium",
                    "impact": "free up capital"
                })
    
    # 2. Pricing suggestions
    if sales_df is not None and not sales_df.empty:
        # Analyze margin
        if 'profit' in sales_df.columns and 'total_sale_amount' in sales_df.columns:
            total_revenue = float(sales_df['total_sale_amount'].sum())
            total_profit = float(sales_df['profit'].sum())
            margin = float((total_profit / total_revenue * 100) if total_revenue > 0 else 0)
            
            if margin < 20:
                suggestions.append({
                    "category": "pricing",
                    "message": "Consider increasing prices to improve profit margins",
                    "priority": "high",
                    "impact": "increase profitability"
                })
            elif margin > 40:
                suggestions.append({
                    "category": "pricing",
                    "message": "Consider lowering prices to increase sales volume",
                    "priority": "medium",
                    "impact": "increase market share"
                })
    
    # 3. Category focus suggestions
    if sales_df is not None and not sales_df.empty and 'category' in sales_df.columns:
        category_performance = sales_df.groupby('category')['total_sale_amount'].sum().sort_values(ascending=False)
        if len(category_performance) > 1:
            best_category = str(category_performance.index[0])
            worst_category = str(category_performance.index[-1])
            
            suggestions.append({
                "category": "strategy",
                "message": f"Focus on {best_category} category - it's the best performer",
                "priority": "medium",
                "impact": "maximize revenue"
            })
            
            suggestions.append({
                "category": "strategy",
                "message": f"Review {worst_category} category - it's underperforming",
                "priority": "low",
                "impact": "improve weak areas"
            })
    
    # 4. Growth suggestions
    if metrics.get('revenue_growth', 0) < 0:
        suggestions.append({
            "category": "growth",
            "message": "Revenue is declining - consider promotional campaigns",
            "priority": "high",
            "impact": "reverse decline"
        })
    
    return suggestions