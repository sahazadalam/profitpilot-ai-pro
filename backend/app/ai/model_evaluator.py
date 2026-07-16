"""
Model evaluation module for comparing different forecasting models.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import logging

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """
    Evaluate and compare different forecasting models.
    """
    
    def __init__(self):
        """Initialize the model evaluator."""
        pass
    
    def evaluate_models(self, y_true: np.ndarray, predictions: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """
        Evaluate multiple models.
        
        Args:
            y_true: Actual values
            predictions: Dictionary of model predictions
            
        Returns:
            Dict[str, Any]: Evaluation results
        """
        results = {}
        best_model = None
        best_score = -float('inf')
        
        for model_name, y_pred in predictions.items():
            metrics = self.calculate_metrics(y_true, y_pred)
            results[model_name] = metrics
            
            # Find best model based on R2 score
            if metrics.get('r2', -float('inf')) > best_score:
                best_score = metrics['r2']
                best_model = model_name
        
        return {
            "models": results,
            "best_model": best_model,
            "comparison": self._generate_comparison(results)
        }
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate regression metrics.
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
            
        Returns:
            Dict[str, float]: Evaluation metrics
        """
        # Remove NaN values
        mask = ~(np.isnan(y_true) | np.isnan(y_pred))
        y_true_clean = y_true[mask]
        y_pred_clean = y_pred[mask]
        
        if len(y_true_clean) == 0:
            return {"mae": 0, "rmse": 0, "r2": 0, "mape": 0}
        
        mae = mean_absolute_error(y_true_clean, y_pred_clean)
        rmse = np.sqrt(mean_squared_error(y_true_clean, y_pred_clean))
        r2 = r2_score(y_true_clean, y_pred_clean)
        
        # MAPE (Mean Absolute Percentage Error)
        mask_nonzero = y_true_clean != 0
        if mask_nonzero.any():
            mape = np.mean(np.abs((y_true_clean[mask_nonzero] - y_pred_clean[mask_nonzero]) / 
                                 y_true_clean[mask_nonzero])) * 100
        else:
            mape = 0
        
        return {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "r2": round(r2, 4),
            "mape": round(mape, 2)
        }
    
    def _generate_comparison(self, results: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """
        Generate comparison summary.
        
        Args:
            results: Results from different models
            
        Returns:
            List[Dict[str, Any]]: Comparison summary
        """
        comparison = []
        
        for model_name, metrics in results.items():
            comparison.append({
                "model": model_name,
                "mae": metrics.get('mae', 0),
                "rmse": metrics.get('rmse', 0),
                "r2": metrics.get('r2', 0),
                "mape": metrics.get('mape', 0)
            })
        
        # Sort by R2 score (best first)
        comparison.sort(key=lambda x: x['r2'], reverse=True)
        
        return comparison
    
    def generate_explanation(self, forecast_results: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of forecast.
        
        Args:
            forecast_results: Forecast results
            
        Returns:
            str: Human-readable explanation
        """
        try:
            forecast = forecast_results.get('forecast', [])
            if not forecast:
                return "No forecast data available for explanation."
            
            values = [f.get('value', 0) for f in forecast]
            if not values:
                return "No forecast values available."
            
            avg_value = np.mean(values)
            trend = self._detect_trend(values)
            
            explanation = f"Forecast shows {trend} trend with average value of {avg_value:.2f}. "
            
            # Add context based on trend
            if trend == "upward":
                explanation += "This suggests increasing performance in the forecast period."
            elif trend == "downward":
                explanation += "This suggests decreasing performance in the forecast period."
            else:
                explanation += "The forecast indicates stable performance in the forecast period."
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return "Unable to generate explanation for forecast."
    
    def _detect_trend(self, values: List[float]) -> str:
        """
        Detect trend in values.
        
        Args:
            values: List of values
            
        Returns:
            str: Trend direction
        """
        if len(values) < 3:
            return "stable"
        
        # Simple trend detection
        first_third = np.mean(values[:len(values)//3])
        last_third = np.mean(values[-len(values)//3:])
        
        if last_third > first_third * 1.05:
            return "upward"
        elif last_third < first_third * 0.95:
            return "downward"
        else:
            return "stable"


# Create singleton instance
model_evaluator = ModelEvaluator()