"""
Market trend simulator for different industries.
"""
from typing import Dict, Any, List
import random
import logging
import pandas as pd
logger = logging.getLogger(__name__)


class MarketSimulator:
    """
    Market trend simulator for different industries.
    """
    
    def __init__(self):
        """Initialize the market simulator."""
        self.industries = {
            "electronics": {
                "growth_rate": 0.12,
                "volatility": 0.3,
                "demand_multiplier": 1.5,
                "risk_factor": 0.4
            },
            "fashion": {
                "growth_rate": 0.08,
                "volatility": 0.4,
                "demand_multiplier": 1.2,
                "risk_factor": 0.5
            },
            "grocery": {
                "growth_rate": 0.05,
                "volatility": 0.2,
                "demand_multiplier": 1.0,
                "risk_factor": 0.2
            },
            "healthcare": {
                "growth_rate": 0.15,
                "volatility": 0.25,
                "demand_multiplier": 1.8,
                "risk_factor": 0.3
            }
        }
    
    def simulate_market_trends(self, sales_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Simulate market trends for different industries.
        
        Args:
            sales_df: Sales DataFrame
            
        Returns:
            Dict[str, Any]: Market trend analysis
        """
        trends = {}
        
        for industry, params in self.industries.items():
            # Get actual sales for this industry if available
            industry_sales = self._get_industry_sales(sales_df, industry)
            
            # Simulate based on industry parameters
            trend = self._simulate_industry_trend(industry, params, industry_sales)
            trends[industry] = trend
        
        return {
            "industries": trends,
            "overall_market": self._calculate_overall_market(trends),
            "recommendations": self._generate_market_recommendations(trends)
        }
    
    def _get_industry_sales(self, sales_df: pd.DataFrame, industry: str) -> float:
        """Get actual sales for an industry."""
        if sales_df.empty or 'category' not in sales_df.columns:
            return 0
        
        industry_df = sales_df[sales_df['category'].str.lower() == industry]
        return float(industry_df['total_sale_amount'].sum()) if not industry_df.empty else 0
    
    def _simulate_industry_trend(self, industry: str, params: Dict, actual_sales: float) -> Dict[str, Any]:
        """Simulate trend for a specific industry."""
        base_demand = 1000 if actual_sales == 0 else actual_sales
        
        # Calculate expected demand
        expected_demand = base_demand * (1 + params['growth_rate'])
        
        # Calculate risk
        risk = params['risk_factor'] * random.uniform(0.8, 1.2)
        
        # Calculate opportunity
        opportunity = params['growth_rate'] * 100 * random.uniform(0.9, 1.1)
        
        return {
            "industry": industry.title(),
            "current_demand": float(round(base_demand, 2)),
            "expected_demand": float(round(expected_demand, 2)),
            "growth_rate": float(round(params['growth_rate'] * 100, 1)),
            "risk_score": float(round(risk * 100, 1)),
            "opportunity_score": float(round(opportunity, 1)),
            "demand_trend": self._get_trend_direction(expected_demand, base_demand),
            "risk_level": self._get_risk_level(risk),
            "recommendation": self._get_industry_recommendation(industry, params, risk)
        }
    
    def _calculate_overall_market(self, trends: Dict) -> Dict[str, Any]:
        """Calculate overall market trends."""
        avg_growth = sum(t['growth_rate'] for t in trends.values()) / len(trends)
        avg_risk = sum(t['risk_score'] for t in trends.values()) / len(trends)
        avg_opportunity = sum(t['opportunity_score'] for t in trends.values()) / len(trends)
        
        return {
            "average_growth": float(round(avg_growth, 1)),
            "average_risk": float(round(avg_risk, 1)),
            "average_opportunity": float(round(avg_opportunity, 1)),
            "market_trend": "growth" if avg_growth > 0 else "decline",
            "market_confidence": float(round(70 + random.uniform(-10, 10), 1))
        }
    
    def _generate_market_recommendations(self, trends: Dict) -> List[Dict[str, Any]]:
        """Generate market recommendations."""
        recommendations = []
        
        # Sort industries by opportunity
        sorted_industries = sorted(
            trends.items(),
            key=lambda x: x[1]['opportunity_score'],
            reverse=True
        )
        
        # Top industry recommendation
        if sorted_industries:
            top_industry = sorted_industries[0]
            recommendations.append({
                "type": "focus",
                "industry": top_industry[0].title(),
                "message": f"Focus on {top_industry[0].title()} - highest opportunity",
                "priority": "high"
            })
        
        # Risk warning
        high_risk = [i for i, t in trends.items() if t['risk_score'] > 50]
        if high_risk:
            recommendations.append({
                "type": "caution",
                "industry": ", ".join([h.title() for h in high_risk]),
                "message": f"High risk in {', '.join(high_risk)} - monitor closely",
                "priority": "medium"
            })
        
        return recommendations
    
    def _get_trend_direction(self, expected: float, current: float) -> str:
        """Get trend direction."""
        if expected > current * 1.05:
            return "increasing"
        elif expected < current * 0.95:
            return "decreasing"
        else:
            return "stable"
    
    def _get_risk_level(self, risk: float) -> str:
        """Get risk level."""
        if risk < 0.3:
            return "Low Risk"
        elif risk < 0.5:
            return "Medium Risk"
        else:
            return "High Risk"
    
    def _get_industry_recommendation(self, industry: str, params: Dict, risk: float) -> str:
        """Get industry-specific recommendation."""
        if params['growth_rate'] > 0.1 and risk < 0.3:
            return f"Strong growth opportunity in {industry.title()}"
        elif params['growth_rate'] > 0.05 and risk < 0.5:
            return f"Steady opportunity in {industry.title()}"
        else:
            return f"Monitor {industry.title()} market - consider selective investment"


# Create singleton instance
market_simulator = MarketSimulator()