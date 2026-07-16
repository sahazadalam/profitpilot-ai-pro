"""
Business Health Score calculation engine.
"""
import numpy as np
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class BusinessHealthCalculator:
    """
    Calculate business health score based on multiple metrics.
    """
    
    def __init__(self):
        """Initialize the business health calculator."""
        self.weights = {
            "revenue_growth": 0.25,
            "profitability": 0.25,
            "inventory_health": 0.20,
            "sales_volume": 0.15,
            "customer_health": 0.15
        }
    
    def calculate_score(self, metrics: Dict[str, Any]) -> Tuple[int, str, str]:
        """
        Calculate business health score.
        
        Args:
            metrics: Dictionary of business metrics
            
        Returns:
            Tuple[int, str, str]: Score, status, and explanation
        """
        try:
            # Calculate individual scores (0-100)
            scores = {}
            explanations = []
            
            # 1. Revenue Growth Score
            revenue_growth = metrics.get('revenue_growth', 0)
            scores['revenue_growth'] = self._score_revenue_growth(revenue_growth)
            explanations.append(self._explain_revenue_growth(revenue_growth))
            
            # 2. Profitability Score
            profit_margin = metrics.get('profit_margin', 0)
            scores['profitability'] = self._score_profitability(profit_margin)
            explanations.append(self._explain_profitability(profit_margin))
            
            # 3. Inventory Health Score
            inventory_health = metrics.get('inventory_health', 0)
            scores['inventory_health'] = self._score_inventory_health(inventory_health)
            explanations.append(self._explain_inventory_health(inventory_health))
            
            # 4. Sales Volume Score
            sales_volume = metrics.get('sales_volume', 0)
            scores['sales_volume'] = self._score_sales_volume(sales_volume)
            explanations.append(self._explain_sales_volume(sales_volume))
            
            # 5. Customer Health Score
            customer_health = metrics.get('customer_health', 0)
            scores['customer_health'] = self._score_customer_health(customer_health)
            explanations.append(self._explain_customer_health(customer_health))
            
            # Calculate weighted score
            weighted_score = sum(
                scores[key] * self.weights[key] 
                for key in self.weights.keys()
            )
            
            final_score = int(weighted_score)
            status = self._get_status(final_score)
            explanation = self._generate_explanation(final_score, scores, explanations)
            
            return final_score, status, explanation
            
        except Exception as e:
            logger.error(f"Error calculating business health: {str(e)}")
            return 0, "Unknown", "Unable to calculate business health score"
    
    def _score_revenue_growth(self, growth: float) -> float:
        """Score revenue growth."""
        if growth >= 20:
            return 100
        elif growth >= 10:
            return 80
        elif growth >= 5:
            return 60
        elif growth >= 0:
            return 40
        else:
            return max(0, 40 + growth)
    
    def _score_profitability(self, margin: float) -> float:
        """Score profitability."""
        if margin >= 30:
            return 100
        elif margin >= 20:
            return 80
        elif margin >= 10:
            return 60
        elif margin >= 5:
            return 40
        else:
            return max(0, 40 + margin * 2)
    
    def _score_inventory_health(self, health: float) -> float:
        """Score inventory health."""
        return min(100, health)
    
    def _score_sales_volume(self, volume: float) -> float:
        """Score sales volume."""
        if volume >= 1000:
            return 100
        elif volume >= 500:
            return 80
        elif volume >= 100:
            return 60
        elif volume >= 50:
            return 40
        else:
            return 20
    
    def _score_customer_health(self, health: float) -> float:
        """Score customer health."""
        return min(100, health)
    
    def _get_status(self, score: int) -> str:
        """Get status based on score."""
        if score >= 80:
            return "Excellent"
        elif score >= 65:
            return "Good"
        elif score >= 50:
            return "Average"
        elif score >= 35:
            return "Poor"
        else:
            return "Critical"
    
    def _explain_revenue_growth(self, growth: float) -> str:
        """Explain revenue growth."""
        if growth >= 20:
            return f"Revenue is growing strongly at {growth:.1f}%"
        elif growth >= 10:
            return f"Revenue is growing well at {growth:.1f}%"
        elif growth >= 5:
            return f"Revenue is growing moderately at {growth:.1f}%"
        elif growth >= 0:
            return f"Revenue is stable with {growth:.1f}% growth"
        else:
            return f"Revenue is declining at {abs(growth):.1f}% - needs attention"
    
    def _explain_profitability(self, margin: float) -> str:
        """Explain profitability."""
        if margin >= 30:
            return f"Profit margin is excellent at {margin:.1f}%"
        elif margin >= 20:
            return f"Profit margin is good at {margin:.1f}%"
        elif margin >= 10:
            return f"Profit margin is average at {margin:.1f}%"
        elif margin >= 5:
            return f"Profit margin is low at {margin:.1f}% - needs improvement"
        else:
            return f"Profit margin is critical at {margin:.1f}% - immediate action needed"
    
    def _explain_inventory_health(self, health: float) -> str:
        """Explain inventory health."""
        if health >= 80:
            return "Inventory health is excellent"
        elif health >= 60:
            return "Inventory health is good"
        elif health >= 40:
            return "Inventory health is average - some optimization needed"
        else:
            return "Inventory health is poor - immediate review needed"
    
    def _explain_sales_volume(self, volume: float) -> str:
        """Explain sales volume."""
        if volume >= 1000:
            return "Sales volume is high - excellent performance"
        elif volume >= 500:
            return "Sales volume is good"
        elif volume >= 100:
            return "Sales volume is average"
        else:
            return "Sales volume is low - need to boost sales"
    
    def _explain_customer_health(self, health: float) -> str:
        """Explain customer health."""
        if health >= 80:
            return "Customer health is excellent"
        elif health >= 60:
            return "Customer health is good"
        elif health >= 40:
            return "Customer health is average"
        else:
            return "Customer health is poor - retention needs focus"
    
    def _generate_explanation(self, score: int, scores: Dict, explanations: List) -> str:
        """Generate comprehensive explanation."""
        status = self._get_status(score)
        
        explanation = f"Business Health Score: {score}/100 - {status}\n\n"
        explanation += "Detailed Breakdown:\n"
        
        for key, value in scores.items():
            explanation += f"- {key.replace('_', ' ').title()}: {value:.0f}/100\n"
        
        explanation += "\nKey Insights:\n"
        for exp in explanations[:3]:  # Top 3 insights
            explanation += f"- {exp}\n"
        
        if score < 50:
            explanation += "\n⚠️ Priority Action Required: Address declining metrics immediately."
        elif score < 65:
            explanation += "\n📈 Improvement Opportunities: Focus on strengthening weak areas."
        else:
            explanation += "\n✅ Maintain current strategy and look for optimization opportunities."
        
        return explanation


# Create singleton instance
business_health_calculator = BusinessHealthCalculator()