"""
Explainable AI for providing business explanations.
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ExplainableAI:
    """
    Explainable AI engine for providing business explanations.
    """
    
    def __init__(self):
        """Initialize the explainable AI engine."""
        pass
    
    def explain_prediction(
        self,
        prediction: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate explanation for a prediction.
        
        Args:
            prediction: Prediction data
            context: Context data
            
        Returns:
            Dict[str, Any]: Explanation
        """
        try:
            # Extract key factors
            factors = self._extract_factors(prediction, context)
            
            # Generate explanation
            explanation = self._generate_explanation(prediction, factors, context)
            
            return {
                "prediction": prediction,
                "explanation": explanation,
                "factors": factors,
                "confidence": self._calculate_confidence(prediction, context),
                "importance": self._calculate_importance(factors)
            }
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return {
                "prediction": prediction,
                "explanation": "Unable to generate detailed explanation",
                "factors": [],
                "confidence": 50,
                "importance": []
            }
    
    def _extract_factors(self, prediction: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract important factors from context."""
        factors = []
        
        if context.get('sales_trend'):
            factors.append({
                "name": "Sales Trend",
                "value": context['sales_trend'],
                "impact": "high" if context['sales_trend'] == "upward" else "medium"
            })
        
        if context.get('profit_margin'):
            factors.append({
                "name": "Profit Margin",
                "value": f"{context['profit_margin']:.1f}%",
                "impact": "high" if context['profit_margin'] > 20 else "medium"
            })
        
        if context.get('inventory_health'):
            factors.append({
                "name": "Inventory Health",
                "value": f"{context['inventory_health']:.0f}%",
                "impact": "high" if context['inventory_health'] > 70 else "medium"
            })
        
        if context.get('customer_health'):
            factors.append({
                "name": "Customer Health",
                "value": f"{context['customer_health']:.0f}%",
                "impact": "high" if context['customer_health'] > 70 else "medium"
            })
        
        if context.get('seasonality'):
            factors.append({
                "name": "Seasonality",
                "value": context['seasonality'],
                "impact": "medium"
            })
        
        return factors
    
    def _generate_explanation(self, prediction: Dict[str, Any], factors: List[Dict], context: Dict[str, Any]) -> str:
        """Generate human-readable explanation."""
        if not factors:
            return "No sufficient data to generate explanation"
        
        explanation_parts = []
        
        # Start with overall trend
        if context.get('sales_trend'):
            trend = context['sales_trend']
            if trend == "upward":
                explanation_parts.append("Revenue is showing an upward trend")
            elif trend == "downward":
                explanation_parts.append("Revenue is showing a downward trend")
            else:
                explanation_parts.append("Revenue is stable")
        
        # Add profit context
        if context.get('profit_margin'):
            margin = context['profit_margin']
            if margin > 20:
                explanation_parts.append("with healthy profit margins")
            elif margin > 10:
                explanation_parts.append("with moderate profit margins")
            else:
                explanation_parts.append("with low profit margins that need attention")
        
        # Add inventory context
        if context.get('inventory_health'):
            health = context['inventory_health']
            if health > 70:
                explanation_parts.append("and strong inventory health")
            else:
                explanation_parts.append("and inventory levels need monitoring")
        
        # Add prediction context
        if prediction.get('value'):
            value = prediction['value']
            if value > 0:
                explanation_parts.append(f"with predicted value of {value:.2f}")
        
        explanation = " ".join(explanation_parts) if explanation_parts else "No clear explanation available"
        
        # Add confidence
        if prediction.get('confidence'):
            explanation += f" (Confidence: {prediction['confidence']:.0f}%)"
        
        return explanation
    
    def _calculate_confidence(self, prediction: Dict[str, Any], context: Dict[str, Any]) -> int:
        """Calculate confidence score."""
        base_confidence = 70
        
        # Adjust based on data quality
        if context.get('data_quality'):
            if context['data_quality'] > 80:
                base_confidence += 10
            elif context['data_quality'] < 50:
                base_confidence -= 20
        
        # Adjust based on factors
        if len(self._extract_factors(prediction, context)) > 3:
            base_confidence += 10
        
        # Adjust based on seasonality
        if context.get('seasonality'):
            base_confidence += 5
        
        return min(95, max(30, base_confidence))
    
    def _calculate_importance(self, factors: List[Dict]) -> List[Dict[str, Any]]:
        """Calculate importance of factors."""
        importance = []
        
        for factor in factors:
            impact_score = {
                "high": 80,
                "medium": 60,
                "low": 40
            }.get(factor.get('impact', 'medium'), 60)
            
            importance.append({
                "factor": factor['name'],
                "value": factor['value'],
                "importance_score": impact_score,
                "weight": impact_score / 100
            })
        
        return importance


# Create singleton instance
explainable_ai = ExplainableAI()