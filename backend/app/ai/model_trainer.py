"""
Model training module for machine learning models.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

MODEL_PATH = "ml_models"


class ModelTrainer:
    """
    Train and save machine learning models.
    """
    
    def __init__(self):
        """Initialize the model trainer."""
        os.makedirs(MODEL_PATH, exist_ok=True)
    
    def train_linear_regression(self, X: np.ndarray, y: np.ndarray, model_name: str = "linear") -> Dict[str, Any]:
        """
        Train linear regression model.
        
        Args:
            X: Features
            y: Target values
            model_name: Name for the model
            
        Returns:
            Dict[str, Any]: Training results
        """
        try:
            logger.info(f"Training Linear Regression model: {model_name}")
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train model
            model = LinearRegression()
            model.fit(X_scaled, y)
            
            # Save model
            model_path = os.path.join(MODEL_PATH, f"{model_name}_linear.joblib")
            scaler_path = os.path.join(MODEL_PATH, f"{model_name}_scaler.joblib")
            
            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)
            
            logger.info(f"Linear Regression model saved to {model_path}")
            
            return {
                "model": model,
                "scaler": scaler,
                "model_path": model_path,
                "scaler_path": scaler_path,
                "coefficients": model.coef_.tolist(),
                "intercept": model.intercept_
            }
            
        except Exception as e:
            logger.error(f"Error training Linear Regression: {str(e)}")
            raise
    
    def train_random_forest(self, X: np.ndarray, y: np.ndarray, model_name: str = "forest") -> Dict[str, Any]:
        """
        Train Random Forest model.
        
        Args:
            X: Features
            y: Target values
            model_name: Name for the model
            
        Returns:
            Dict[str, Any]: Training results
        """
        try:
            logger.info(f"Training Random Forest model: {model_name}")
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_scaled, y)
            
            # Save model
            model_path = os.path.join(MODEL_PATH, f"{model_name}_forest.joblib")
            scaler_path = os.path.join(MODEL_PATH, f"{model_name}_scaler.joblib")
            
            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)
            
            logger.info(f"Random Forest model saved to {model_path}")
            
            return {
                "model": model,
                "scaler": scaler,
                "model_path": model_path,
                "scaler_path": scaler_path,
                "feature_importance": model.feature_importances_.tolist()
            }
            
        except Exception as e:
            logger.error(f"Error training Random Forest: {str(e)}")
            raise
    
    def load_model(self, model_name: str, model_type: str = "linear") -> Dict[str, Any]:
        """
        Load a trained model.
        
        Args:
            model_name: Name of the model
            model_type: Type of model (linear, forest)
            
        Returns:
            Dict[str, Any]: Loaded model and scaler
        """
        try:
            model_path = os.path.join(MODEL_PATH, f"{model_name}_{model_type}.joblib")
            scaler_path = os.path.join(MODEL_PATH, f"{model_name}_scaler.joblib")
            
            if not os.path.exists(model_path):
                return {"error": f"Model {model_name}_{model_type} not found"}
            
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None
            
            return {"model": model, "scaler": scaler}
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return {"error": str(e)}
    
    def list_models(self) -> list[Dict[str, Any]]:
        """
        List all available models.
        
        Returns:
            List[Dict[str, Any]]: List of models
        """
        models = []
        
        for file in os.listdir(MODEL_PATH):
            if file.endswith('.joblib'):
                name = file.replace('_linear.joblib', '').replace('_forest.joblib', '').replace('_scaler.joblib', '')
                models.append({
                    "name": name,
                    "file": file,
                    "type": "linear" if "linear" in file else "forest" if "forest" in file else "scaler",
                    "path": os.path.join(MODEL_PATH, file)
                })
        
        return models


# Create singleton instance
model_trainer = ModelTrainer()