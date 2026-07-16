"""
Forecasting engine using Prophet, ARIMA, and Linear Regression.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
import logging
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class ForecastEngine:
    """
    Engine for generating forecasts using multiple models.
    """
    
    def __init__(self):
        """Initialize the forecast engine."""
        self.models = {}
    
    def forecast_prophet(self, df: pd.DataFrame, periods: int, 
                         date_col: str = 'ds', value_col: str = 'y') -> Dict[str, Any]:
        """
        Generate forecast using Prophet.
        
        Args:
            df: DataFrame with historical data
            periods: Number of periods to forecast
            date_col: Name of date column
            value_col: Name of value column
            
        Returns:
            Dict[str, Any]: Forecast results
        """
        try:
            # Prepare data for Prophet
            prophet_df = df[[date_col, value_col]].copy()
            prophet_df.columns = ['ds', 'y']
            
            # Initialize and fit Prophet
            model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
            model.fit(prophet_df)
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=periods)
            
            # Generate forecast
            forecast = model.predict(future)
            
            # Extract forecast for future periods
            forecast_data = forecast.tail(periods)
            
            # Format results
            results = []
            for _, row in forecast_data.iterrows():
                results.append({
                    "date": row['ds'].strftime('%Y-%m-%d'),
                    "value": round(row['yhat'], 2),
                    "lower": round(row['yhat_lower'], 2) if 'yhat_lower' in row else None,
                    "upper": round(row['yhat_upper'], 2) if 'yhat_upper' in row else None
                })
            
            return {
                "forecast": results,
                "model": "prophet",
                "details": {
                    "seasonality": {
                        "yearly": True,
                        "weekly": True,
                        "daily": False
                    },
                    "periods": periods
                }
            }
            
        except Exception as e:
            logger.error(f"Prophet forecast failed: {str(e)}")
            return {"error": str(e)}
    
    def forecast_arima(self, df: pd.DataFrame, periods: int, 
                       date_col: str = 'date', value_col: str = 'value') -> Dict[str, Any]:
        """
        Generate forecast using ARIMA.
        
        Args:
            df: DataFrame with historical data
            periods: Number of periods to forecast
            date_col: Name of date column
            value_col: Name of value column
            
        Returns:
            Dict[str, Any]: Forecast results
        """
        try:
            # Prepare data
            data = df[[value_col]].values.flatten()
            
            # Fit ARIMA model
            model = ARIMA(data, order=(5, 1, 0))
            model_fit = model.fit()
            
            # Generate forecast
            forecast_result = model_fit.forecast(steps=periods)
            forecast_values = forecast_result.tolist()
            
            # Get last date and generate future dates
            last_date = pd.to_datetime(df[date_col].iloc[-1])
            future_dates = [last_date + timedelta(days=i+1) for i in range(periods)]
            
            # Format results
            results = []
            for i, (date, value) in enumerate(zip(future_dates, forecast_values)):
                results.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "value": round(float(value), 2),
                    "lower": None,
                    "upper": None
                })
            
            return {
                "forecast": results,
                "model": "arima",
                "details": {
                    "order": "(5,1,0)",
                    "periods": periods
                }
            }
            
        except Exception as e:
            logger.error(f"ARIMA forecast failed: {str(e)}")
            return {"error": str(e)}
    
    def forecast_linear(self, df: pd.DataFrame, periods: int,
                        date_col: str = 'date', value_col: str = 'value') -> Dict[str, Any]:
        """
        Generate forecast using Linear Regression.
        
        Args:
            df: DataFrame with historical data
            periods: Number of periods to forecast
            date_col: Name of date column
            value_col: Name of value column
            
        Returns:
            Dict[str, Any]: Forecast results
        """
        try:
            # Prepare features (days since start)
            df = df.sort_values(by=date_col)
            days_since_start = (pd.to_datetime(df[date_col]) - pd.to_datetime(df[date_col]).min()).dt.days
            
            X = days_since_start.values.reshape(-1, 1)
            y = df[value_col].values
            
            # Train linear regression
            model = LinearRegression()
            model.fit(X, y)
            
            # Generate future dates
            last_date = pd.to_datetime(df[date_col].iloc[-1])
            future_dates = [last_date + timedelta(days=i+1) for i in range(periods)]
            
            # Predict future values
            last_day = days_since_start.iloc[-1]
            future_days = np.array([last_day + i + 1 for i in range(periods)]).reshape(-1, 1)
            predictions = model.predict(future_days)
            
            # Format results
            results = []
            for i, (date, value) in enumerate(zip(future_dates, predictions)):
                results.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "value": round(float(value), 2),
                    "lower": None,
                    "upper": None
                })
            
            return {
                "forecast": results,
                "model": "linear",
                "details": {
                    "slope": round(float(model.coef_[0]), 4),
                    "intercept": round(float(model.intercept_), 2),
                    "periods": periods
                }
            }
            
        except Exception as e:
            logger.error(f"Linear forecast failed: {str(e)}")
            return {"error": str(e)}
    
    def calculate_moving_average(self, df: pd.DataFrame, window: int, 
                                 date_col: str = 'date', value_col: str = 'value') -> List[Dict[str, Any]]:
        """
        Calculate moving average.
        
        Args:
            df: DataFrame with historical data
            window: Window size for moving average
            date_col: Name of date column
            value_col: Name of value column
            
        Returns:
            List[Dict[str, Any]]: Moving average results
        """
        try:
            df = df.sort_values(by=date_col)
            df['moving_avg'] = df[value_col].rolling(window=window, min_periods=1).mean()
            
            results = []
            for _, row in df.iterrows():
                results.append({
                    "date": row[date_col].strftime('%Y-%m-%d') if isinstance(row[date_col], pd.Timestamp) else str(row[date_col]),
                    "value": round(row[value_col], 2),
                    "moving_avg": round(row['moving_avg'], 2)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Moving average calculation failed: {str(e)}")
            return []
    
    def detect_seasonality(self, df: pd.DataFrame, date_col: str = 'date', value_col: str = 'value') -> Dict[str, Any]:
        """
        Detect seasonality in time series data.
        
        Args:
            df: DataFrame with historical data
            date_col: Name of date column
            value_col: Name of value column
            
        Returns:
            Dict[str, Any]: Seasonality information
        """
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
            
            # Ensure data is sorted and has datetime index
            df = df.sort_values(by=date_col)
            df['date'] = pd.to_datetime(df[date_col])
            df = df.set_index('date')
            
            # Need at least 14 data points for seasonality detection
            if len(df) < 14:
                return {"message": "Insufficient data for seasonality detection (need at least 14 points)"}
            
            # Decompose time series
            result = seasonal_decompose(df[value_col], model='additive', period=7, extrapolate_trend='freq')
            
            # Extract components
            trend = result.trend.dropna()
            seasonal = result.seasonal.dropna()
            residual = result.resid.dropna()
            
            # Find peak and low periods
            seasonal_series = seasonal.reset_index(drop=False)
            seasonal_series.columns = ['date', 'seasonal']
            seasonal_series['day_of_week'] = seasonal_series['date'].dt.dayofweek
            
            # Group by day of week
            daily_seasonality = seasonal_series.groupby('day_of_week')['seasonal'].mean()
            peak_days = daily_seasonality.nlargest(2).index.tolist()
            low_days = daily_seasonality.nsmallest(2).index.tolist()
            
            # Day names
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
            return {
                "has_seasonality": bool(seasonal.std() > 0.1 * df[value_col].std()),
                "seasonality_strength": round(float(seasonal.std() / df[value_col].std()), 3),
                "trend_strength": round(float(trend.std() / df[value_col].std()), 3),
                "peak_days": [day_names[d] for d in peak_days],
                "low_days": [day_names[d] for d in low_days],
                "data_points": len(df)
            }
            
        except Exception as e:
            logger.error(f"Seasonality detection failed: {str(e)}")
            return {"message": f"Seasonality detection failed: {str(e)}"}


# Create singleton instance
forecast_engine = ForecastEngine()