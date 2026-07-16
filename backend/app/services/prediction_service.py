"""
Prediction service for machine learning forecasting.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

from app.database.mongodb import mongodb
from app.ai.forecast_engine import forecast_engine
from app.ai.model_evaluator import model_evaluator
from app.ai.model_trainer import model_trainer
from app.utils.ml_utils import prepare_time_series_data
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class PredictionService:
    """
    Service for generating predictions using ML models.
    """
    
    def __init__(self):
        """Initialize the prediction service."""
        self.sales_collection = "sales"
    
    async def get_collection(self, collection_name: str):
        """Get a collection from MongoDB."""
        return mongodb.get_collection(collection_name)
    
    async def get_sales_data(self, product_id: Optional[str] = None) -> pd.DataFrame:
        """
        Get sales data from MongoDB.
        
        Args:
            product_id: Optional product ID to filter
            
        Returns:
            pd.DataFrame: Sales data
        """
        try:
            collection = await self.get_collection(self.sales_collection)
            
            # Build query
            query = {}
            if product_id:
                query["product_id"] = product_id
            
            # Get sales data
            cursor = collection.find(query, {
                "sale_date": 1,
                "total_sale_amount": 1,
                "profit": 1,
                "quantity": 1,
                "product_id": 1,
                "product_name": 1,
                "category": 1
            }).sort("sale_date", 1)
            
            sales_data = await cursor.to_list(length=None)
            
            if not sales_data:
                # Return empty DataFrame
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(sales_data)
            
            # Convert date
            if 'sale_date' in df.columns:
                df['sale_date'] = pd.to_datetime(df['sale_date'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting sales data: {str(e)}")
            return pd.DataFrame()
    
    async def predict_demand(self, product_id: Optional[str] = None, 
                            days: int = 30, 
                            model: str = "prophet") -> Dict[str, Any]:
        """
        Predict demand for products.
        
        Args:
            product_id: Product ID for specific product
            days: Number of days to forecast
            model: Model to use
            
        Returns:
            Dict[str, Any]: Prediction results
        """
        try:
            # Get sales data
            df = await self.get_sales_data(product_id)
            
            if df.empty:
                return {
                    "message": "No sales data available for demand prediction",
                    "forecast": [],
                    "model": model
                }
            
            # Aggregate daily demand
            if 'sale_date' in df.columns and 'quantity' in df.columns:
                daily_demand = df.groupby(df['sale_date'].dt.date)['quantity'].sum().reset_index()
                daily_demand.columns = ['date', 'value']
                
                # Add missing dates
                date_range = pd.date_range(daily_demand['date'].min(), daily_demand['date'].max())
                daily_demand = daily_demand.set_index('date').reindex(date_range, fill_value=0).reset_index()
                daily_demand.columns = ['date', 'value']
                
                # Generate forecast
                if model == "prophet":
                    result = forecast_engine.forecast_prophet(
                        daily_demand, periods=days, date_col='date', value_col='value'
                    )
                elif model == "arima":
                    result = forecast_engine.forecast_arima(
                        daily_demand, periods=days, date_col='date', value_col='value'
                    )
                else:
                    result = forecast_engine.forecast_linear(
                        daily_demand, periods=days, date_col='date', value_col='value'
                    )
                
                # Add explanation
                if not result.get('error'):
                    explanation = model_evaluator.generate_explanation(result)
                    result['explanation'] = explanation
                
                return result
            else:
                return {"message": "Insufficient data for demand prediction", "forecast": []}
            
        except Exception as e:
            logger.error(f"Error predicting demand: {str(e)}")
            raise AppException(
                message=f"Demand prediction failed: {str(e)}",
                status_code=500,
                error_code="DEMAND_PREDICTION_FAILED"
            )
    
    async def predict_revenue(self, days: int = 30, model: str = "prophet") -> Dict[str, Any]:
        """
        Predict revenue.
        
        Args:
            days: Number of days to forecast
            model: Model to use
            
        Returns:
            Dict[str, Any]: Prediction results
        """
        try:
            # Get sales data
            df = await self.get_sales_data()
            
            if df.empty:
                return {
                    "message": "No sales data available for revenue prediction",
                    "forecast": [],
                    "model": model
                }
            
            # Aggregate daily revenue
            if 'sale_date' in df.columns and 'total_sale_amount' in df.columns:
                daily_revenue = df.groupby(df['sale_date'].dt.date)['total_sale_amount'].sum().reset_index()
                daily_revenue.columns = ['date', 'value']
                
                # Add missing dates
                date_range = pd.date_range(daily_revenue['date'].min(), daily_revenue['date'].max())
                daily_revenue = daily_revenue.set_index('date').reindex(date_range, fill_value=0).reset_index()
                daily_revenue.columns = ['date', 'value']
                
                # Generate forecast
                if model == "prophet":
                    result = forecast_engine.forecast_prophet(
                        daily_revenue, periods=days, date_col='date', value_col='value'
                    )
                elif model == "arima":
                    result = forecast_engine.forecast_arima(
                        daily_revenue, periods=days, date_col='date', value_col='value'
                    )
                else:
                    result = forecast_engine.forecast_linear(
                        daily_revenue, periods=days, date_col='date', value_col='value'
                    )
                
                # Add explanation
                if not result.get('error'):
                    explanation = model_evaluator.generate_explanation(result)
                    result['explanation'] = explanation
                
                return result
            else:
                return {"message": "Insufficient data for revenue prediction", "forecast": []}
            
        except Exception as e:
            logger.error(f"Error predicting revenue: {str(e)}")
            raise AppException(
                message=f"Revenue prediction failed: {str(e)}",
                status_code=500,
                error_code="REVENUE_PREDICTION_FAILED"
            )
    
    async def predict_profit(self, days: int = 30, model: str = "prophet") -> Dict[str, Any]:
        """
        Predict profit.
        
        Args:
            days: Number of days to forecast
            model: Model to use
            
        Returns:
            Dict[str, Any]: Prediction results
        """
        try:
            # Get sales data
            df = await self.get_sales_data()
            
            if df.empty:
                return {
                    "message": "No sales data available for profit prediction",
                    "forecast": [],
                    "model": model
                }
            
            # Aggregate daily profit
            if 'sale_date' in df.columns and 'profit' in df.columns:
                daily_profit = df.groupby(df['sale_date'].dt.date)['profit'].sum().reset_index()
                daily_profit.columns = ['date', 'value']
                
                # Add missing dates
                date_range = pd.date_range(daily_profit['date'].min(), daily_profit['date'].max())
                daily_profit = daily_profit.set_index('date').reindex(date_range, fill_value=0).reset_index()
                daily_profit.columns = ['date', 'value']
                
                # Generate forecast
                if model == "prophet":
                    result = forecast_engine.forecast_prophet(
                        daily_profit, periods=days, date_col='date', value_col='value'
                    )
                elif model == "arima":
                    result = forecast_engine.forecast_arima(
                        daily_profit, periods=days, date_col='date', value_col='value'
                    )
                else:
                    result = forecast_engine.forecast_linear(
                        daily_profit, periods=days, date_col='date', value_col='value'
                    )
                
                # Add explanation
                if not result.get('error'):
                    explanation = model_evaluator.generate_explanation(result)
                    result['explanation'] = explanation
                
                return result
            else:
                return {"message": "Insufficient data for profit prediction", "forecast": []}
            
        except Exception as e:
            logger.error(f"Error predicting profit: {str(e)}")
            raise AppException(
                message=f"Profit prediction failed: {str(e)}",
                status_code=500,
                error_code="PROFIT_PREDICTION_FAILED"
            )
    
    async def get_inventory_forecast(self) -> Dict[str, Any]:
        """
        Get inventory forecast including stock depletion dates.
        
        Returns:
            Dict[str, Any]: Inventory forecast
        """
        try:
            products_collection = await self.get_collection("products")
            sales_collection = await self.get_collection(self.sales_collection)
            
            # Get all products
            products = await products_collection.find({}).to_list(length=None)
            
            if not products:
                return {"message": "No products found", "data": []}
            
            results = []
            
            for product in products:
                # Get sales data for this product
                sales = await sales_collection.find({"product_id": product["_id"]}).to_list(length=None)
                
                if not sales:
                    # No sales data, skip
                    continue
                
                # Calculate average daily sales
                df = pd.DataFrame(sales)
                if 'sale_date' in df.columns:
                    df['sale_date'] = pd.to_datetime(df['sale_date'])
                    daily_sales = df.groupby(df['sale_date'].dt.date)['quantity'].sum()
                    avg_daily_sales = daily_sales.mean()
                else:
                    avg_daily_sales = 0
                
                if avg_daily_sales == 0:
                    continue
                
                current_stock = product.get('stock', 0)
                days_until_depletion = int(current_stock / avg_daily_sales) if avg_daily_sales > 0 else 0
                
                results.append({
                    "product_id": str(product["_id"]),
                    "product_name": product.get('name', 'Unknown'),
                    "category": product.get('category', 'Unknown'),
                    "current_stock": current_stock,
                    "avg_daily_sales": round(avg_daily_sales, 2),
                    "days_until_depletion": days_until_depletion,
                    "depletion_date": (datetime.utcnow() + timedelta(days=days_until_depletion)).strftime('%Y-%m-%d'),
                    "recommended_reorder_date": (datetime.utcnow() + timedelta(days=max(0, days_until_depletion - 7))).strftime('%Y-%m-%d'),
                    "reorder_quantity": int(avg_daily_sales * 30)  # 30-day supply
                })
            
            return {
                "data": results,
                "total_products": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error getting inventory forecast: {str(e)}")
            raise AppException(
                message=f"Inventory forecast failed: {str(e)}",
                status_code=500,
                error_code="INVENTORY_FORECAST_FAILED"
            )
    
    async def detect_seasonality(self) -> Dict[str, Any]:
        """
        Detect seasonality in sales data.
        
        Returns:
            Dict[str, Any]: Seasonality information
        """
        try:
            # Get sales data
            df = await self.get_sales_data()
            
            if df.empty:
                return {"message": "No sales data available for seasonality detection"}
            
            # Aggregate daily revenue
            if 'sale_date' in df.columns and 'total_sale_amount' in df.columns:
                daily_revenue = df.groupby(df['sale_date'].dt.date)['total_sale_amount'].sum().reset_index()
                daily_revenue.columns = ['date', 'value']
                
                # Detect seasonality
                seasonality = forecast_engine.detect_seasonality(daily_revenue, 'date', 'value')
                
                return seasonality
            else:
                return {"message": "Insufficient data for seasonality detection"}
            
        except Exception as e:
            logger.error(f"Error detecting seasonality: {str(e)}")
            raise AppException(
                message=f"Seasonality detection failed: {str(e)}",
                status_code=500,
                error_code="SEASONALITY_DETECTION_FAILED"
            )
    
    async def get_moving_average(self, window: int = 7) -> Dict[str, Any]:
        """
        Calculate moving average of revenue.
        
        Args:
            window: Window size for moving average
            
        Returns:
            Dict[str, Any]: Moving average results
        """
        try:
            # Get sales data
            df = await self.get_sales_data()
            
            if df.empty:
                return {"message": "No sales data available", "data": []}
            
            # Aggregate daily revenue
            if 'sale_date' in df.columns and 'total_sale_amount' in df.columns:
                daily_revenue = df.groupby(df['sale_date'].dt.date)['total_sale_amount'].sum().reset_index()
                daily_revenue.columns = ['date', 'value']
                
                # Calculate moving average
                results = forecast_engine.calculate_moving_average(daily_revenue, window, 'date', 'value')
                
                return {
                    "data": results[-window:],  # Return last window days
                    "window": window,
                    "total_periods": len(results)
                }
            else:
                return {"message": "Insufficient data for moving average calculation", "data": []}
            
        except Exception as e:
            logger.error(f"Error calculating moving average: {str(e)}")
            raise AppException(
                message=f"Moving average calculation failed: {str(e)}",
                status_code=500,
                error_code="MOVING_AVERAGE_FAILED"
            )
    
    async def compare_models(self, days: int = 30) -> Dict[str, Any]:
        """
        Compare different forecasting models.
        
        Args:
            days: Number of days to forecast
            
        Returns:
            Dict[str, Any]: Comparison results
        """
        try:
            # Get sales data
            df = await self.get_sales_data()
            
            if df.empty:
                return {"message": "No sales data available for model comparison"}
            
            # Prepare data
            if 'sale_date' in df.columns and 'total_sale_amount' in df.columns:
                daily_revenue = df.groupby(df['sale_date'].dt.date)['total_sale_amount'].sum().reset_index()
                daily_revenue.columns = ['date', 'value']
                
                # Split data (80% train, 20% test)
                train_size = int(len(daily_revenue) * 0.8)
                train_data = daily_revenue.iloc[:train_size]
                test_data = daily_revenue.iloc[train_size:]
                
                # Predictions from different models
                predictions = {}
                
                # Prophet
                prophet_result = forecast_engine.forecast_prophet(
                    train_data, periods=len(test_data), date_col='date', value_col='value'
                )
                if not prophet_result.get('error'):
                    predictions['prophet'] = np.array([f.get('value', 0) for f in prophet_result.get('forecast', [])])
                
                # ARIMA
                arima_result = forecast_engine.forecast_arima(
                    train_data, periods=len(test_data), date_col='date', value_col='value'
                )
                if not arima_result.get('error'):
                    predictions['arima'] = np.array([f.get('value', 0) for f in arima_result.get('forecast', [])])
                
                # Linear
                linear_result = forecast_engine.forecast_linear(
                    train_data, periods=len(test_data), date_col='date', value_col='value'
                )
                if not linear_result.get('error'):
                    predictions['linear'] = np.array([f.get('value', 0) for f in linear_result.get('forecast', [])])
                
                if not predictions:
                    return {"message": "No models could make predictions"}
                
                # Evaluate models
                y_true = test_data['value'].values
                evaluation = model_evaluator.evaluate_models(y_true, predictions)
                
                return evaluation
            else:
                return {"message": "Insufficient data for model comparison"}
            
        except Exception as e:
            logger.error(f"Error comparing models: {str(e)}")
            raise AppException(
                message=f"Model comparison failed: {str(e)}",
                status_code=500,
                error_code="MODEL_COMPARISON_FAILED"
            )
    
    async def evaluate_model(self, model_name: str = "prophet") -> Dict[str, Any]:
        """
        Evaluate a specific model.
        
        Args:
            model_name: Name of the model to evaluate
            
        Returns:
            Dict[str, Any]: Evaluation results
        """
        try:
            # Get sales data
            df = await self.get_sales_data()
            
            if df.empty:
                return {"message": "No sales data available for model evaluation"}
            
            # Prepare data
            if 'sale_date' in df.columns and 'total_sale_amount' in df.columns:
                daily_revenue = df.groupby(df['sale_date'].dt.date)['total_sale_amount'].sum().reset_index()
                daily_revenue.columns = ['date', 'value']
                
                # Split data (80% train, 20% test)
                train_size = int(len(daily_revenue) * 0.8)
                train_data = daily_revenue.iloc[:train_size]
                test_data = daily_revenue.iloc[train_size:]
                
                # Get predictions from specified model
                if model_name == "prophet":
                    result = forecast_engine.forecast_prophet(
                        train_data, periods=len(test_data), date_col='date', value_col='value'
                    )
                elif model_name == "arima":
                    result = forecast_engine.forecast_arima(
                        train_data, periods=len(test_data), date_col='date', value_col='value'
                    )
                elif model_name == "linear":
                    result = forecast_engine.forecast_linear(
                        train_data, periods=len(test_data), date_col='date', value_col='value'
                    )
                else:
                    return {"message": f"Model '{model_name}' not recognized"}
                
                if result.get('error'):
                    return {"message": f"Model evaluation failed: {result['error']}"}
                
                # Calculate metrics
                y_true = test_data['value'].values
                y_pred = np.array([f.get('value', 0) for f in result.get('forecast', [])])
                
                metrics = model_evaluator.calculate_metrics(y_true, y_pred)
                
                return {
                    "model": model_name,
                    "metrics": metrics,
                    "train_size": len(train_data),
                    "test_size": len(test_data),
                    "forecast": result.get('forecast', []),
                    "explanation": model_evaluator.generate_explanation(result)
                }
            else:
                return {"message": "Insufficient data for model evaluation"}
            
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            raise AppException(
                message=f"Model evaluation failed: {str(e)}",
                status_code=500,
                error_code="MODEL_EVALUATION_FAILED"
            )


# Create singleton instance
prediction_service = PredictionService()