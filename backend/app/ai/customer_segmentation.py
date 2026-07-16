"""
Customer segmentation using K-Means clustering.
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class CustomerSegmentation:
    """
    Customer segmentation engine using K-Means clustering.
    """
    
    def __init__(self):
        """Initialize the customer segmentation engine."""
        self.scaler = StandardScaler()
        self.kmeans = None
        self.segment_names = {
            0: "VIP Customer",
            1: "High Value Customer",
            2: "Medium Value Customer",
            3: "Low Value Customer",
            4: "New Customer"
        }
    
    def segment_customers(self, sales_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Segment customers based on their purchase behavior.
        
        Args:
            sales_df: Sales DataFrame
            
        Returns:
            List[Dict[str, Any]]: Customer segments
        """
        if sales_df.empty or 'customer_name' not in sales_df.columns:
            return []
        
        try:
            # Aggregate customer data
            customer_data = self._aggregate_customer_data(sales_df)
            
            if len(customer_data) < 5:
                return self._create_default_segments(customer_data)
            
            # Prepare features for clustering
            features = self._prepare_features(customer_data)
            
            # Determine optimal number of clusters (max 5)
            n_clusters = min(5, len(customer_data))
            if n_clusters < 2:
                return self._create_default_segments(customer_data)
            
            # Scale features
            scaled_features = self.scaler.fit_transform(features)
            
            # Apply K-Means clustering
            self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = self.kmeans.fit_predict(scaled_features)
            
            # Add cluster labels to customer data
            customer_data['segment'] = labels
            
            # Create segment summaries
            segments = []
            for cluster_id in range(n_clusters):
                cluster_data = customer_data[customer_data['segment'] == cluster_id]
                
                # Calculate metrics for this segment
                avg_spend = cluster_data['total_spent'].mean()
                avg_orders = cluster_data['order_count'].mean()
                avg_frequency = cluster_data['purchase_frequency'].mean()
                customer_count = len(cluster_data)
                
                # Determine segment name based on average spend
                if avg_spend > 1000:
                    segment_name = "VIP Customer"
                elif avg_spend > 500:
                    segment_name = "High Value Customer"
                elif avg_spend > 200:
                    segment_name = "Medium Value Customer"
                elif avg_spend > 50:
                    segment_name = "Low Value Customer"
                else:
                    segment_name = "New Customer"
                
                segments.append({
                    "segment_id": int(cluster_id),
                    "segment_name": segment_name,
                    "customer_count": int(customer_count),
                    "average_spend": float(round(avg_spend, 2)),
                    "average_orders": float(round(avg_orders, 2)),
                    "purchase_frequency": float(round(avg_frequency, 2)),
                    "total_revenue": float(round(cluster_data['total_spent'].sum(), 2)),
                    "percentage": float(round((customer_count / len(customer_data)) * 100, 1))
                })
            
            # Sort by average spend (descending)
            segments.sort(key=lambda x: x['average_spend'], reverse=True)
            
            return segments
            
        except Exception as e:
            logger.error(f"Error in customer segmentation: {str(e)}")
            return []
    
    def _aggregate_customer_data(self, sales_df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate customer purchase data."""
        # Group by customer
        customer_groups = sales_df.groupby('customer_name')
        
        data = []
        for customer, group in customer_groups:
            total_spent = group['total_sale_amount'].sum()
            order_count = group['invoice_number'].nunique()
            total_items = group['quantity'].sum()
            
            # Calculate purchase frequency (days between purchases)
            if 'sale_date' in group.columns and len(group) > 1:
                group = group.sort_values('sale_date')
                date_diff = group['sale_date'].diff().dt.days
                frequency = date_diff.mean() if not date_diff.isna().all() else 30
            else:
                frequency = 30  # Default
            
            data.append({
                'customer': customer,
                'total_spent': total_spent,
                'order_count': order_count,
                'total_items': total_items,
                'purchase_frequency': frequency
            })
        
        return pd.DataFrame(data)
    
    def _prepare_features(self, customer_data: pd.DataFrame) -> np.ndarray:
        """Prepare features for clustering."""
        # Select features for clustering
        features = customer_data[['total_spent', 'order_count', 'total_items']].values
        return features
    
    def _create_default_segments(self, customer_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Create default segments when clustering is not possible."""
        if customer_data.empty:
            return []
        
        total_customers = len(customer_data)
        total_revenue = customer_data['total_spent'].sum()
        
        return [{
            "segment_id": 0,
            "segment_name": "All Customers",
            "customer_count": total_customers,
            "average_spend": float(round(total_revenue / total_customers, 2)),
            "average_orders": float(round(customer_data['order_count'].mean(), 2)),
            "purchase_frequency": float(round(customer_data['purchase_frequency'].mean(), 2)),
            "total_revenue": float(round(total_revenue, 2)),
            "percentage": 100.0
        }]


# Create singleton instance
customer_segmentation = CustomerSegmentation()