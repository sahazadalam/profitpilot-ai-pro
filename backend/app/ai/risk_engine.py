"""
Business risk engine for assessing business risk levels.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class RiskEngine:
    """
    Engine for calculating business risk scores.
    """
    
    def __init__(self):
        """Initialize the risk engine."""
        pass
    
    def calculate_business_risk(
        self,
        products_df: pd.DataFrame,
        sales_df: pd.DataFrame,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate business risk score.
        
        Args:
            products_df: Products DataFrame
            sales_df: Sales DataFrame
            metrics: Business metrics
            
        Returns:
            Dict[str, Any]: Risk analysis
        """
        # Calculate individual risk factors
        inventory_risk = self._calculate_inventory_risk(products_df)
        revenue_risk = self._calculate_revenue_risk(sales_df, metrics)
        profit_risk = self._calculate_profit_risk(sales_df)
        concentration_risk = self._calculate_concentration_risk(sales_df)
        forecast_risk = self._calculate_forecast_risk(metrics)
        
        # Convert to Python native types
        inventory_risk = float(inventory_risk)
        revenue_risk = float(revenue_risk)
        profit_risk = float(profit_risk)
        concentration_risk = float(concentration_risk)
        forecast_risk = float(forecast_risk)
        
        # Combine risks
        total_risk_score = float(
            inventory_risk * 0.25 +
            revenue_risk * 0.25 +
            profit_risk * 0.20 +
            concentration_risk * 0.15 +
            forecast_risk * 0.15
        )
        
        total_risk_score = int(total_risk_score)
        
        # Determine risk level
        if total_risk_score >= 80:
            level = "Low Risk"
            description = "Business is in a healthy position with minimal risk factors"
        elif total_risk_score >= 60:
            level = "Medium Risk"
            description = "Some risk factors present that require monitoring"
        elif total_risk_score >= 40:
            level = "High Risk"
            description = "Significant risk factors identified that need attention"
        else:
            level = "Critical Risk"
            description = "Critical risk factors present - immediate action required"
        
        return {
            "risk_score": int(total_risk_score),
            "risk_level": level,
            "description": description,
            "risk_factors": {
                "inventory_risk": int(inventory_risk),
                "revenue_risk": int(revenue_risk),
                "profit_risk": int(profit_risk),
                "concentration_risk": int(concentration_risk),
                "forecast_risk": int(forecast_risk)
            },
            "recommendations": self._generate_risk_recommendations(
                inventory_risk, revenue_risk, profit_risk,
                concentration_risk, forecast_risk
            )
        }
    
    def _calculate_inventory_risk(self, products_df: pd.DataFrame) -> float:
        """
        Calculate inventory risk score.
        """
        if products_df.empty:
            return 50.0
        
        total_products = len(products_df)
        if total_products == 0:
            return 50.0
        
        # Calculate risk factors
        out_of_stock = len(products_df[products_df['stock'] == 0]) if 'stock' in products_df.columns else 0
        low_stock = len(products_df[products_df['stock'] <= products_df['minimum_stock']]) if 'stock' in products_df.columns and 'minimum_stock' in products_df.columns else 0
        
        # Risk score (higher = lower risk)
        risk = float(100 - (out_of_stock / total_products * 50) - (low_stock / total_products * 30))
        return float(max(0, min(100, risk)))
    
    def _calculate_revenue_risk(self, sales_df: pd.DataFrame, metrics: Dict[str, Any]) -> float:
        """
        Calculate revenue risk score.
        """
        if sales_df.empty:
            return 50.0
        
        # Check revenue trend
        revenue_growth = float(metrics.get('revenue_growth', 0.0))
        
        if revenue_growth > 10:
            return 80.0
        elif revenue_growth > 0:
            return 60.0
        elif revenue_growth > -10:
            return 40.0
        else:
            return 20.0
    
    def _calculate_profit_risk(self, sales_df: pd.DataFrame) -> float:
        """
        Calculate profit risk score.
        """
        if sales_df.empty or 'profit' not in sales_df.columns:
            return 50.0
        
        total_profit = float(sales_df['profit'].sum())
        total_revenue = float(sales_df['total_sale_amount'].sum() if 'total_sale_amount' in sales_df.columns else 1.0)
        
        margin = float((total_profit / total_revenue * 100) if total_revenue > 0 else 0)
        
        if margin > 30:
            return 80.0
        elif margin > 20:
            return 60.0
        elif margin > 10:
            return 40.0
        else:
            return 20.0
    
    def _calculate_concentration_risk(self, sales_df: pd.DataFrame) -> float:
        """
        Calculate customer/product concentration risk.
        """
        if sales_df.empty:
            return 50.0
        
        # Calculate product concentration
        if 'product_id' in sales_df.columns:
            product_sales = sales_df.groupby('product_id')['quantity'].sum() if 'quantity' in sales_df.columns else pd.Series()
            if not product_sales.empty:
                total_sales = float(product_sales.sum())
                if total_sales > 0:
                    top_products_share = float(product_sales.nlargest(3).sum() / total_sales)
                    
                    if top_products_share < 0.5:
                        return 70.0
                    elif top_products_share < 0.7:
                        return 50.0
                    else:
                        return 30.0
        
        return 50.0
    
    def _calculate_forecast_risk(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate forecast accuracy risk.
        """
        # Default to medium risk if no forecast data
        forecast_accuracy = float(metrics.get('forecast_accuracy', 70.0))
        
        if forecast_accuracy > 80:
            return 80.0
        elif forecast_accuracy > 60:
            return 60.0
        elif forecast_accuracy > 40:
            return 40.0
        else:
            return 20.0
    
    def _generate_risk_recommendations(
        self,
        inventory_risk: float,
        revenue_risk: float,
        profit_risk: float,
        concentration_risk: float,
        forecast_risk: float
    ) -> List[str]:
        """
        Generate risk mitigation recommendations.
        """
        recommendations = []
        
        if inventory_risk < 50:
            recommendations.append("Improve inventory management - review stock levels and ordering process")
        
        if revenue_risk < 50:
            recommendations.append("Address revenue decline - consider marketing and sales initiatives")
        
        if profit_risk < 50:
            recommendations.append("Improve profitability - review pricing strategy and cost structure")
        
        if concentration_risk < 50:
            recommendations.append("Reduce concentration risk - diversify product/customer base")
        
        if forecast_risk < 50:
            recommendations.append("Improve forecasting - use more data points and advanced models")
        
        if not recommendations:
            recommendations.append("Maintain current strategy - risk factors are well managed")
        
        return recommendations


# Create singleton instance
risk_engine = RiskEngine()