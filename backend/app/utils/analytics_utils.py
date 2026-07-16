"""
Analytics utilities for data processing and calculations.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)


def create_dataframe(data: List[Dict], columns: List[str] = None) -> pd.DataFrame:
    """
    Create a pandas DataFrame from data.
    
    Args:
        data: List of dictionaries
        columns: List of column names to include
        
    Returns:
        pd.DataFrame: DataFrame with the data
    """
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    
    if columns:
        # Only keep specified columns that exist
        existing_columns = [col for col in columns if col in df.columns]
        df = df[existing_columns]
    
    return df


def calculate_growth(current: float, previous: float) -> float:
    """
    Calculate growth percentage.
    
    Args:
        current: Current value
        previous: Previous value
        
    Returns:
        float: Growth percentage
    """
    if previous == 0:
        return 0.0 if current == 0 else 100.0
    return ((current - previous) / abs(previous)) * 100


def calculate_moving_average(data: List[float], window: int = 7) -> List[float]:
    """
    Calculate moving average.
    
    Args:
        data: List of values
        window: Window size for moving average
        
    Returns:
        List[float]: Moving average values
    """
    if not data:
        return []
    
    series = pd.Series(data)
    return series.rolling(window=window, min_periods=1).mean().tolist()


def calculate_margin(revenue: float, cost: float) -> float:
    """
    Calculate profit margin.
    
    Args:
        revenue: Total revenue
        cost: Total cost
        
    Returns:
        float: Profit margin percentage
    """
    if revenue == 0:
        return 0.0
    return ((revenue - cost) / revenue) * 100


def aggregate_by_period(df: pd.DataFrame, date_column: str, value_column: str, period: str = 'D') -> pd.Series:
    """
    Aggregate data by time period.
    
    Args:
        df: DataFrame with data
        date_column: Name of the date column
        value_column: Name of the value column
        period: Period for aggregation ('D', 'W', 'M', 'Y')
        
    Returns:
        pd.Series: Aggregated data
    """
    if df.empty:
        return pd.Series()
    
    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Set date as index
    df = df.set_index(date_column)
    
    # Resample and aggregate
    return df[value_column].resample(period).sum()


def get_date_range(start_date: datetime, end_date: datetime, period: str = 'D') -> List[str]:
    """
    Generate a list of dates between start and end.
    
    Args:
        start_date: Start date
        end_date: End date
        period: Period for date range
        
    Returns:
        List[str]: List of formatted dates
    """
    dates = []
    current = start_date
    
    while current <= end_date:
        dates.append(current.strftime('%Y-%m-%d'))
        
        if period == 'D':
            current += timedelta(days=1)
        elif period == 'W':
            current += timedelta(days=7)
        elif period == 'M':
            current += timedelta(days=30)
        else:
            current += timedelta(days=1)
    
    return dates


def calculate_percentile(data: List[float], percentile: float) -> float:
    """
    Calculate percentile of data.
    
    Args:
        data: List of values
        percentile: Percentile to calculate (0-100)
        
    Returns:
        float: Percentile value
    """
    if not data:
        return 0.0
    
    return np.percentile(data, percentile)


def detect_outliers(data: List[float], threshold: float = 1.5) -> List[bool]:
    """
    Detect outliers using IQR method.
    
    Args:
        data: List of values
        threshold: IQR multiplier threshold
        
    Returns:
        List[bool]: True for outliers
    """
    if not data:
        return []
    
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    
    lower_bound = q1 - (threshold * iqr)
    upper_bound = q3 + (threshold * iqr)
    
    return [x < lower_bound or x > upper_bound for x in data]


def format_currency(value: float) -> str:
    """
    Format value as currency.
    
    Args:
        value: Numeric value
        
    Returns:
        str: Formatted currency string
    """
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """
    Format value as percentage.
    
    Args:
        value: Numeric value
        
    Returns:
        str: Formatted percentage string
    """
    return f"{value:.1f}%"