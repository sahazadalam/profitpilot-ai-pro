"""
Business risk prediction engine.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class RiskPrediction:
    """
    Business risk prediction engine.
    """
    
    def __init__(self):
        """Initialize the risk prediction engine."""
        pass
    
    def predict_business_risk(self, sales_df: pd.DataFrame, products_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Predict business risks.
        
        Args:
            sales_df: Sales DataFrame
            products_df: Products DataFrame
            
        Returns:
            Dict[str, Any]: Risk predictions
        """
        risks = {
            "inventory_risk": self._predict_inventory_risk(products_df),
            "revenue_risk": self._predict_revenue_risk(sales_df),
            "profit_risk": self._predict_profit_risk(sales_df),
            "overall_risk": {}
        }
        
        # Calculate overall risk
        risk_scores = [
            risks["inventory_risk"].get("score", 0),
            risks["revenue_risk"].get("score", 0),
            risks["profit_risk"].get("score", 0)
        ]
        
        overall_score = sum(risk_scores) / len(risk_scores)
        
        risks["overall_risk"] = {
            "score": int(overall_score),
            "level": self._get_risk_level(overall_score),
            "recommendations": self._generate_risk_recommendations(risks)
        }
        
        return risks
    
    def _predict_inventory_risk(self, products_df: pd.DataFrame) -> Dict[str, Any]:
        """Predict inventory risk."""
        if products_df.empty:
            return {
                "score": 0,
                "level": "Unknown",
                "factors": ["No inventory data available"],
                "recommendations": ["Collect inventory data for risk assessment"]
            }
        
        total_products = len(products_df)
        if total_products == 0:
            return {"score": 0, "level": "Unknown", "factors": [], "recommendations": []}
        
        # Calculate risk factors
        out_of_stock = len(products_df[products_df['stock'] == 0]) if 'stock' in products_df.columns else 0
        low_stock = len(products_df[products_df['stock'] <= products_df['minimum_stock']]) if 'stock' in products_df.columns else 0
        excess_stock = len(products_df[products_df['stock'] > products_df['minimum_stock'] * 3]) if 'stock' in products_df.columns else 0
        
        risk_score = (
            (out_of_stock / total_products * 40) +
            (low_stock / total_products * 30) +
            (excess_stock / total_products * 30)
        )
        
        risk_score = min(100, risk_score)
        
        factors = []
        if out_of_stock > 0:
            factors.append(f"{out_of_stock} products out of stock")
        if low_stock > 0:
            factors.append(f"{low_stock} products low on stock")
        if excess_stock > 0:
            factors.append(f"{excess_stock} products with excess stock")
        
        if not factors:
            factors.append("Inventory levels are healthy")
        
        return {
            "score": int(risk_score),
            "level": self._get_risk_level(risk_score),
            "factors": factors,
            "recommendations": self._get_inventory_recommendations(risk_score, out_of_stock, low_stock)
        }
    
    def _predict_revenue_risk(self, sales_df: pd.DataFrame) -> Dict[str, Any]:
        """Predict revenue risk."""
        if sales_df.empty:
            return {
                "score": 0,
                "level": "Unknown",
                "factors": ["No revenue data available"],
                "recommendations": ["Collect revenue data for risk assessment"]
            }
        
        # Calculate revenue trend
        if 'sale_date' in sales_df.columns:
            sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
            monthly_revenue = sales_df.groupby(sales_df['sale_date'].dt.month)['total_sale_amount'].sum()
            
            if len(monthly_revenue) >= 2:
                revenue_growth = (monthly_revenue.iloc[-1] - monthly_revenue.iloc[-2]) / monthly_revenue.iloc[-2] * 100
            else:
                revenue_growth = 0
        else:
            revenue_growth = 0
        
        # Calculate volatility
        if 'total_sale_amount' in sales_df.columns:
            volatility = sales_df['total_sale_amount'].std() / sales_df['total_sale_amount'].mean() * 100
        else:
            volatility = 0
        
        # Calculate risk score
        risk_score = 0
        factors = []
        
        if revenue_growth < -5:
            risk_score += 40
            factors.append(f"Revenue declining ({revenue_growth:.1f}%)")
        elif revenue_growth < 0:
            risk_score += 20
            factors.append(f"Revenue slightly declining ({revenue_growth:.1f}%)")
        elif revenue_growth > 15:
            risk_score += 10
            factors.append("Revenue growing strongly")
        
        if volatility > 30:
            risk_score += 30
            factors.append(f"High revenue volatility ({volatility:.1f}%)")
        elif volatility > 20:
            risk_score += 20
            factors.append(f"Moderate revenue volatility ({volatility:.1f}%)")
        
        risk_score = min(100, risk_score)
        
        if not factors:
            factors.append("Revenue is stable and growing")
        
        return {
            "score": int(risk_score),
            "level": self._get_risk_level(risk_score),
            "factors": factors,
            "recommendations": self._get_revenue_recommendations(risk_score, revenue_growth)
        }
    
    def _predict_profit_risk(self, sales_df: pd.DataFrame) -> Dict[str, Any]:
        """Predict profit risk."""
        if sales_df.empty or 'profit' not in sales_df.columns:
            return {
                "score": 0,
                "level": "Unknown",
                "factors": ["No profit data available"],
                "recommendations": ["Collect profit data for risk assessment"]
            }
        
        total_profit = sales_df['profit'].sum()
        total_revenue = sales_df['total_sale_amount'].sum()
        
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Calculate risk score
        risk_score = 0
        factors = []
        
        if profit_margin < 5:
            risk_score += 50
            factors.append(f"Very low profit margin ({profit_margin:.1f}%)")
        elif profit_margin < 10:
            risk_score += 30
            factors.append(f"Low profit margin ({profit_margin:.1f}%)")
        elif profit_margin < 20:
            risk_score += 15
            factors.append(f"Average profit margin ({profit_margin:.1f}%)")
        else:
            factors.append(f"Healthy profit margin ({profit_margin:.1f}%)")
        
        # Check for loss-making products
        if 'profit' in sales_df.columns:
            loss_count = len(sales_df[sales_df['profit'] < 0])
            if loss_count > 0:
                risk_score += min(30, loss_count * 5)
                factors.append(f"{loss_count} sales transactions with negative profit")
        
        risk_score = min(100, risk_score)
        
        return {
            "score": int(risk_score),
            "level": self._get_risk_level(risk_score),
            "factors": factors,
            "recommendations": self._get_profit_recommendations(risk_score, profit_margin)
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level from score."""
        if score < 25:
            return "Low Risk"
        elif score < 50:
            return "Medium Risk"
        elif score < 75:
            return "High Risk"
        else:
            return "Critical Risk"
    
    def _get_inventory_recommendations(self, risk_score: float, out_of_stock: int, low_stock: int) -> List[str]:
        """Get inventory risk recommendations."""
        recommendations = []
        
        if out_of_stock > 0:
            recommendations.append(f"Immediately restock {out_of_stock} out-of-stock products")
        if low_stock > 0:
            recommendations.append(f"Review stock levels for {low_stock} low-stock products")
        if risk_score > 50:
            recommendations.append("Implement inventory optimization system")
        if not recommendations:
            recommendations.append("Maintain current inventory strategy")
        
        return recommendations
    
    def _get_revenue_recommendations(self, risk_score: float, growth: float) -> List[str]:
        """Get revenue risk recommendations."""
        recommendations = []
        
        if growth < 0:
            recommendations.append("Implement marketing campaigns to boost revenue")
            recommendations.append("Review pricing strategy")
        if risk_score > 50:
            recommendations.append("Diversify revenue streams")
        if not recommendations:
            recommendations.append("Maintain current revenue strategy")
        
        return recommendations
    
    def _get_profit_recommendations(self, risk_score: float, margin: float) -> List[str]:
        """Get profit risk recommendations."""
        recommendations = []
        
        if margin < 10:
            recommendations.append("Review cost structure and pricing strategy")
        if risk_score > 50:
            recommendations.append("Identify and address loss-making products")
        if not recommendations:
            recommendations.append("Maintain current profit strategy")
        
        return recommendations
    
    def _generate_risk_recommendations(self, risks: Dict) -> List[str]:
        """Generate overall risk recommendations."""
        recommendations = []
        
        inventory_risk = risks["inventory_risk"].get("score", 0)
        revenue_risk = risks["revenue_risk"].get("score", 0)
        profit_risk = risks["profit_risk"].get("score", 0)
        
        if inventory_risk > 50:
            recommendations.append("Review inventory management - high inventory risk")
        if revenue_risk > 50:
            recommendations.append("Address revenue decline - high revenue risk")
        if profit_risk > 50:
            recommendations.append("Improve profitability - high profit risk")
        
        if not recommendations:
            recommendations.append("Business risks are well managed - maintain current strategy")
        
        return recommendations


# Create singleton instance
risk_prediction = RiskPrediction()