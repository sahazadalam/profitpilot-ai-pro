"""
Machine Learning utilities for data preparation and evaluation.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def prepare_time_series_data(data: List[Dict], date_column: str, value_column: str) -> pd.DataFrame:
    """
    Prepare time series data for forecasting.
    
    Args:
        data: List of dictionaries containing time series data
        date_column: Name of the date column
        value_column: Name of the value column
        
    Returns:
        pd.DataFrame: Prepared time series data
    """
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    
    # Convert date column to datetime
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column])
    
    # Ensure proper sorting
    df = df.sort_values(by=date_column)
    
    # Handle missing values
    if value_column in df.columns:
        df[value_column] = df[value_column].fillna(0)
    
    return df


def create_features(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    """
    Create features for machine learning models.
    
    Args:
        df: DataFrame with time series data
        target_column: Name of the target column
        
    Returns:
        pd.DataFrame: DataFrame with engineered features
    """
    if df.empty:
        return df
    
    df_copy = df.copy()
    
    # Date features
    if 'sale_date' in df_copy.columns:
        df_copy['year'] = df_copy['sale_date'].dt.year
        df_copy['month'] = df_copy['sale_date'].dt.month
        df_copy['day'] = df_copy['sale_date'].dt.day
        df_copy['day_of_week'] = df_copy['sale_date'].dt.dayofweek
        df_copy['quarter'] = df_copy['sale_date'].dt.quarter
    
    # Lag features
    if target_column in df_copy.columns:
        for lag in [1, 2, 3, 7, 14, 30]:
            df_copy[f'lag_{lag}'] = df_copy[target_column].shift(lag)
    
    # Rolling statistics
    if target_column in df_copy.columns:
        for window in [3, 7, 14, 30]:
            df_copy[f'rolling_mean_{window}'] = df_copy[target_column].rolling(window=window).mean()
            df_copy[f'rolling_std_{window}'] = df_copy[target_column].rolling(window=window).std()
    
    return df_copy


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate regression metrics.
    
    Args:
        y_true: Actual values
        y_pred: Predicted values
        
    Returns:
        Dict[str, float]: Dictionary of metrics
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
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
    mask = y_true_clean != 0
    if mask.any():
        mape = np.mean(np.abs((y_true_clean[mask] - y_pred_clean[mask]) / y_true_clean[mask])) * 100
    else:
        mape = 0
    
    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 4),
        "mape": round(mape, 2)
    }


def evaluate_forecast(forecast: List[Dict]) -> Dict[str, Any]:
    """
    Evaluate forecast quality.
    
    Args:
        forecast: List of forecast dictionaries
        
    Returns:
        Dict[str, Any]: Evaluation metrics
    """
    if not forecast:
        return {"message": "No forecast data available"}
    
    values = [f.get('value', 0) for f in forecast]
    
    return {
        "total": sum(values),
        "average": np.mean(values),
        "max": max(values),
        "min": min(values),
        "std": np.std(values),
        "count": len(values)
    }


def detect_seasonality(data: pd.Series) -> Dict[str, Any]:
    """
    Detect seasonality patterns in time series data.
    
    Args:
        data: Time series data
        
    Returns:
        Dict[str, Any]: Seasonality patterns
    """
    if data.empty:
        return {"message": "No data available"}
    
    from statsmodels.tsa.seasonal import seasonal_decompose
    
    try:
        # Need at least 2 periods for decomposition
        if len(data) < 14:
            return {"message": "Insufficient data for seasonality detection"}
        
        # Decompose time series
        result = seasonal_decompose(data, model='additive', period=7, extrapolate_trend='freq')
        
        # Extract components
        trend = result.trend.dropna()
        seasonal = result.seasonal.dropna()
        residual = result.resid.dropna()
        
        return {
            "has_seasonality": seasonal.std() > (0.1 * data.std()),
            "seasonality_strength": round(seasonal.std() / data.std(), 3),
            "trend_strength": round(trend.std() / data.std(), 3) if not trend.empty else 0,
            "residual_strength": round(residual.std() / data.std(), 3) if not residual.empty else 0,
            "peak_days": self._find_peak_days(seasonal),
            "low_days": self._find_low_days(seasonal)
        }
    except Exception as e:
        logger.error(f"Error detecting seasonality: {str(e)}")
        return {"message": f"Seasonality detection failed: {str(e)}"}


def _find_peak_days(seasonal: pd.Series) -> List[int]:
    """Find days with highest seasonal values."""
    if seasonal.empty:
        return []
    
    # Group by day of week
    daily_values = {}
    for idx, val in seasonal.items():
        day = idx.dayofweek
        daily_values[day] = daily_values.get(day, 0) + val
    
    # Sort by value and get top 2 days
    sorted_days = sorted(daily_values.items(), key=lambda x: x[1], reverse=True)
    return [day for day, _ in sorted_days[:2]]


def _find_low_days(seasonal: pd.Series) -> List[int]:
    """Find days with lowest seasonal values."""
    if seasonal.empty:
        return []
    
    # Group by day of week
    daily_values = {}
    for idx, val in seasonal.items():
        day = idx.dayofweek
        daily_values[day] = daily_values.get(day, 0) + val
    
    # Sort by value and get bottom 2 days
    sorted_days = sorted(daily_values.items(), key=lambda x: x[1])
    return [day for day, _ in sorted_days[:2]]