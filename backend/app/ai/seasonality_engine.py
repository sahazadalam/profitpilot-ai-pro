"""
Seasonality detection engine for business patterns.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from statsmodels.tsa.seasonal import seasonal_decompose
import logging

logger = logging.getLogger(__name__)


class SeasonalityEngine:
    """
    Seasonality detection engine.
    """
    
    def __init__(self):
        """Initialize the seasonality engine."""
        pass
    
    def detect_seasonality(self, sales_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect seasonality patterns in sales data.
        
        Args:
            sales_df: Sales DataFrame
            
        Returns:
            Dict[str, Any]: Seasonality patterns
        """
        if sales_df.empty:
            return {"message": "No data available for seasonality detection"}
        
        try:
            # Prepare daily sales data
            daily_sales = self._prepare_daily_sales(sales_df)
            
            if len(daily_sales) < 14:
                return {"message": "Insufficient data for seasonality detection (need at least 14 days)"}
            
            # Detect weekly pattern
            weekly_pattern = self._detect_weekly_pattern(daily_sales)
            
            # Detect monthly pattern
            monthly_pattern = self._detect_monthly_pattern(daily_sales)
            
            # Detect quarterly pattern (if enough data)
            quarterly_pattern = self._detect_quarterly_pattern(daily_sales) if len(daily_sales) > 90 else None
            
            # Find peak and low seasons
            peak_season, low_season = self._find_peak_low_seasons(daily_sales)
            
            return {
                "weekly_pattern": weekly_pattern,
                "monthly_pattern": monthly_pattern,
                "quarterly_pattern": quarterly_pattern,
                "peak_season": peak_season,
                "low_season": low_season,
                "data_points": len(daily_sales),
                "has_seasonality": weekly_pattern.get('has_seasonality', False) or monthly_pattern.get('has_seasonality', False),
                "seasonality_strength": self._calculate_seasonality_strength(daily_sales)
            }
            
        except Exception as e:
            logger.error(f"Error detecting seasonality: {str(e)}")
            return {"message": f"Seasonality detection failed: {str(e)}"}
    
    def _prepare_daily_sales(self, sales_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare daily sales data."""
        if 'sale_date' not in sales_df.columns or 'total_sale_amount' not in sales_df.columns:
            return pd.DataFrame()
        
        df = sales_df.copy()
        df['sale_date'] = pd.to_datetime(df['sale_date'])
        
        # Aggregate daily revenue
        daily_sales = df.groupby('sale_date')['total_sale_amount'].sum().reset_index()
        daily_sales.columns = ['date', 'revenue']
        
        return daily_sales
    
    def _detect_weekly_pattern(self, daily_sales: pd.DataFrame) -> Dict[str, Any]:
        """Detect weekly pattern in sales."""
        # Group by day of week
        daily_sales['day_of_week'] = daily_sales['date'].dt.dayofweek
        daily_sales['day_name'] = daily_sales['date'].dt.day_name()
        
        weekly_avg = daily_sales.groupby('day_of_week')['revenue'].mean().reset_index()
        
        # Find best and worst days
        best_day_idx = weekly_avg['revenue'].idxmax()
        worst_day_idx = weekly_avg['revenue'].idxmin()
        
        best_day = weekly_avg.iloc[best_day_idx]
        worst_day = weekly_avg.iloc[worst_day_idx]
        
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        has_seasonality = (best_day['revenue'] / worst_day['revenue']) > 1.3
        
        return {
            "has_seasonality": bool(has_seasonality),
            "best_day": {
                "name": day_names[int(best_day['day_of_week'])],
                "average_revenue": float(round(best_day['revenue'], 2))
            },
            "worst_day": {
                "name": day_names[int(worst_day['day_of_week'])],
                "average_revenue": float(round(worst_day['revenue'], 2))
            },
            "pattern": self._format_weekly_pattern(weekly_avg, day_names)
        }
    
    def _detect_monthly_pattern(self, daily_sales: pd.DataFrame) -> Dict[str, Any]:
        """Detect monthly pattern in sales."""
        if len(daily_sales) < 30:
            return {"has_seasonality": False}
        
        daily_sales['month'] = daily_sales['date'].dt.month
        daily_sales['month_name'] = daily_sales['date'].dt.strftime('%B')
        
        monthly_avg = daily_sales.groupby('month')['revenue'].mean().reset_index()
        
        # Find best and worst months
        best_month_idx = monthly_avg['revenue'].idxmax()
        worst_month_idx = monthly_avg['revenue'].idxmin()
        
        best_month = monthly_avg.iloc[best_month_idx]
        worst_month = monthly_avg.iloc[worst_month_idx]
        
        has_seasonality = (best_month['revenue'] / worst_month['revenue']) > 1.4
        
        return {
            "has_seasonality": bool(has_seasonality),
            "best_month": {
                "name": self._get_month_name(int(best_month['month'])),
                "average_revenue": float(round(best_month['revenue'], 2))
            },
            "worst_month": {
                "name": self._get_month_name(int(worst_month['month'])),
                "average_revenue": float(round(worst_month['revenue'], 2))
            }
        }
    
    def _detect_quarterly_pattern(self, daily_sales: pd.DataFrame) -> Dict[str, Any]:
        """Detect quarterly pattern in sales."""
        if len(daily_sales) < 90:
            return {"has_seasonality": False}
        
        daily_sales['quarter'] = daily_sales['date'].dt.quarter
        
        quarterly_avg = daily_sales.groupby('quarter')['revenue'].mean().reset_index()
        
        # Find best and worst quarters
        best_q_idx = quarterly_avg['revenue'].idxmax()
        worst_q_idx = quarterly_avg['revenue'].idxmin()
        
        best_q = quarterly_avg.iloc[best_q_idx]
        worst_q = quarterly_avg.iloc[worst_q_idx]
        
        has_seasonality = (best_q['revenue'] / worst_q['revenue']) > 1.5
        
        return {
            "has_seasonality": bool(has_seasonality),
            "best_quarter": {
                "name": f"Q{int(best_q['quarter'])}",
                "average_revenue": float(round(best_q['revenue'], 2))
            },
            "worst_quarter": {
                "name": f"Q{int(worst_q['quarter'])}",
                "average_revenue": float(round(worst_q['revenue'], 2))
            }
        }
    
    def _find_peak_low_seasons(self, daily_sales: pd.DataFrame) -> tuple:
        """Find peak and low seasons."""
        if len(daily_sales) < 30:
            return None, None
        
        # Group by month
        monthly_revenue = daily_sales.groupby(daily_sales['date'].dt.month)['revenue'].sum()
        
        if len(monthly_revenue) < 3:
            return None, None
        
        sorted_months = monthly_revenue.sort_values(ascending=False)
        
        peak_months = sorted_months.head(2).index.tolist()
        low_months = sorted_months.tail(2).index.tolist()
        
        return {
            "months": [self._get_month_name(m) for m in peak_months],
            "average_revenue": float(round(sorted_months.head(2).mean(), 2))
        }, {
            "months": [self._get_month_name(m) for m in low_months],
            "average_revenue": float(round(sorted_months.tail(2).mean(), 2))
        }
    
    def _calculate_seasonality_strength(self, daily_sales: pd.DataFrame) -> float:
        """Calculate seasonality strength (0-100)."""
        if len(daily_sales) < 30:
            return 0
        
        try:
            # Use decomposition
            series = daily_sales.set_index('date')['revenue']
            result = seasonal_decompose(series, model='additive', period=7, extrapolate_trend='freq')
            
            seasonal_variance = result.seasonal.var() if not result.seasonal.isna().all() else 0
            total_variance = series.var() if not series.isna().all() else 1
            
            if total_variance == 0:
                return 0
            
            strength = (seasonal_variance / total_variance) * 100
            return min(100, float(strength))
            
        except Exception:
            return 0
    
    def _format_weekly_pattern(self, weekly_avg: pd.DataFrame, day_names: List[str]) -> List[Dict]:
        """Format weekly pattern for response."""
        pattern = []
        for _, row in weekly_avg.iterrows():
            pattern.append({
                "day": day_names[int(row['day_of_week'])],
                "average_revenue": float(round(row['revenue'], 2))
            })
        return pattern
    
    def _get_month_name(self, month: int) -> str:
        """Get month name from number."""
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
        return months[month - 1] if 1 <= month <= 12 else "Unknown"


# Create singleton instance
seasonality_engine = SeasonalityEngine()