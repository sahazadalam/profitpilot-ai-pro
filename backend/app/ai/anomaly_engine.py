"""
Anomaly detection engine for sales data.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AnomalyEngine:
    """
    Sales anomaly detection using Isolation Forest, Z-Score, and IQR.
    """
    
    def __init__(self):
        """Initialize the anomaly engine."""
        pass
    
    def detect_anomalies(self, sales_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect anomalies in sales data.
        
        Args:
            sales_df: Sales DataFrame
            
        Returns:
            List[Dict[str, Any]]: Detected anomalies
        """
        if sales_df.empty:
            return []
        
        anomalies = []
        
        try:
            # Prepare daily sales data
            daily_sales = self._prepare_daily_sales(sales_df)
            
            if daily_sales.empty:
                return []
            
            # Method 1: Isolation Forest
            isolation_anomalies = self._detect_isolation_forest(daily_sales)
            
            # Method 2: Z-Score
            zscore_anomalies = self._detect_zscore(daily_sales)
            
            # Method 3: IQR
            iqr_anomalies = self._detect_iqr(daily_sales)
            
            # Combine anomalies
            all_anomalies = set()
            all_anomalies.update(isolation_anomalies)
            all_anomalies.update(zscore_anomalies)
            all_anomalies.update(iqr_anomalies)
            
            # Create anomaly records
            for date_idx in all_anomalies:
                if date_idx < len(daily_sales):
                    date = daily_sales.iloc[date_idx]['date']
                    revenue = daily_sales.iloc[date_idx]['revenue']
                    
                    # Determine anomaly type
                    is_spike = revenue > daily_sales['revenue'].mean() + 2 * daily_sales['revenue'].std()
                    is_drop = revenue < daily_sales['revenue'].mean() - 2 * daily_sales['revenue'].std()
                    
                    anomaly_type = "spike" if is_spike else "drop" if is_drop else "outlier"
                    
                    anomalies.append({
                        "date": date.strftime('%Y-%m-%d'),
                        "revenue": float(round(revenue, 2)),
                        "anomaly_type": anomaly_type,
                        "severity": self._calculate_severity(revenue, daily_sales['revenue']),
                        "expected_revenue": float(round(daily_sales['revenue'].mean(), 2)),
                        "deviation": float(round(revenue - daily_sales['revenue'].mean(), 2)),
                        "detection_methods": [
                            "isolation_forest" if date_idx in isolation_anomalies else None,
                            "zscore" if date_idx in zscore_anomalies else None,
                            "iqr" if date_idx in iqr_anomalies else None
                        ],
                        "explanation": self._generate_explanation(anomaly_type, revenue, daily_sales['revenue'])
                    })
            
            # Sort by date
            anomalies.sort(key=lambda x: x['date'])
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return []
    
    def _prepare_daily_sales(self, sales_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare daily sales data for anomaly detection."""
        if 'sale_date' not in sales_df.columns or 'total_sale_amount' not in sales_df.columns:
            return pd.DataFrame()
        
        sales_df_copy = sales_df.copy()
        sales_df_copy['sale_date'] = pd.to_datetime(sales_df_copy['sale_date'])
        
        # Aggregate daily revenue
        daily_sales = sales_df_copy.groupby('sale_date')['total_sale_amount'].sum().reset_index()
        daily_sales.columns = ['date', 'revenue']
        
        return daily_sales
    
    def _detect_isolation_forest(self, daily_sales: pd.DataFrame) -> set:
        """Detect anomalies using Isolation Forest."""
        anomalies = set()
        
        if len(daily_sales) < 10:
            return anomalies
        
        try:
            # Prepare data
            data = daily_sales[['revenue']].values
            
            # Fit Isolation Forest
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            predictions = iso_forest.fit_predict(data)
            
            # Identify anomalies (-1 indicates anomaly)
            for idx, pred in enumerate(predictions):
                if pred == -1:
                    anomalies.add(idx)
                    
        except Exception as e:
            logger.error(f"Isolation Forest error: {str(e)}")
        
        return anomalies
    
    def _detect_zscore(self, daily_sales: pd.DataFrame, threshold: float = 2.5) -> set:
        """Detect anomalies using Z-Score method."""
        anomalies = set()
        
        if len(daily_sales) < 5:
            return anomalies
        
        try:
            mean = daily_sales['revenue'].mean()
            std = daily_sales['revenue'].std()
            
            if std == 0:
                return anomalies
            
            for idx, row in daily_sales.iterrows():
                zscore = (row['revenue'] - mean) / std
                if abs(zscore) > threshold:
                    anomalies.add(idx)
                    
        except Exception as e:
            logger.error(f"Z-Score error: {str(e)}")
        
        return anomalies
    
    def _detect_iqr(self, daily_sales: pd.DataFrame) -> set:
        """Detect anomalies using IQR method."""
        anomalies = set()
        
        if len(daily_sales) < 5:
            return anomalies
        
        try:
            q1 = daily_sales['revenue'].quantile(0.25)
            q3 = daily_sales['revenue'].quantile(0.75)
            iqr = q3 - q1
            
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            for idx, row in daily_sales.iterrows():
                if row['revenue'] < lower_bound or row['revenue'] > upper_bound:
                    anomalies.add(idx)
                    
        except Exception as e:
            logger.error(f"IQR error: {str(e)}")
        
        return anomalies
    
    def _calculate_severity(self, value: float, series: pd.Series) -> str:
        """Calculate anomaly severity."""
        mean = series.mean()
        std = series.std()
        
        if std == 0:
            return "low"
        
        deviation = abs(value - mean) / std
        
        if deviation > 5:
            return "critical"
        elif deviation > 3:
            return "high"
        elif deviation > 2:
            return "medium"
        else:
            return "low"
    
    def _generate_explanation(self, anomaly_type: str, value: float, series: pd.Series) -> str:
        """Generate explanation for anomaly."""
        mean = series.mean()
        
        if anomaly_type == "spike":
            percentage = ((value - mean) / mean * 100) if mean > 0 else 0
            return f"Revenue spiked {percentage:.1f}% above average, indicating unusual sales activity"
        elif anomaly_type == "drop":
            percentage = ((mean - value) / mean * 100) if mean > 0 else 0
            return f"Revenue dropped {percentage:.1f}% below average, indicating unusual sales decline"
        else:
            return "Unusual sales pattern detected that deviates from normal behavior"


# Create singleton instance
anomaly_engine = AnomalyEngine()