"""
Bundle recommendation engine for product bundles.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from itertools import combinations
import logging

logger = logging.getLogger(__name__)


class BundleEngine:
    """
    Engine for generating product bundle recommendations.
    """
    
    def __init__(self):
        """Initialize the bundle engine."""
        pass
    
    def generate_bundle_recommendations(
        self,
        sales_df: pd.DataFrame,
        products_df: pd.DataFrame
    ) -> List[Dict[str, Any]]:
        """
        Generate bundle recommendations.
        
        Args:
            sales_df: Sales DataFrame
            products_df: Products DataFrame
            
        Returns:
            List[Dict[str, Any]]: Bundle recommendations
        """
        recommendations = []
        
        if sales_df.empty or products_df.empty:
            return recommendations
        
        # Get product pairs that are frequently bought together
        product_pairs = self._find_frequent_pairs(sales_df)
        
        for pair in product_pairs[:10]:  # Top 10 pairs
            product1_id, product2_id, frequency = pair
            
            # Get product details
            product1 = products_df[products_df['_id'].astype(str) == product1_id]
            product2 = products_df[products_df['_id'].astype(str) == product2_id]
            
            if product1.empty or product2.empty:
                continue
            
            product1_name = product1.iloc[0].get('name', 'Unknown')
            product2_name = product2.iloc[0].get('name', 'Unknown')
            product1_price = product1.iloc[0].get('selling_price', 0)
            product2_price = product2.iloc[0].get('selling_price', 0)
            
            # Calculate bundle price (10% discount)
            total_price = product1_price + product2_price
            bundle_price = total_price * 0.9
            
            # Calculate expected profit
            product1_cost = product1.iloc[0].get('purchase_price', 0)
            product2_cost = product2.iloc[0].get('purchase_price', 0)
            total_cost = product1_cost + product2_cost
            expected_profit = bundle_price - total_cost
            
            recommendations.append({
                "bundle_name": f"{product1_name} + {product2_name}",
                "products": [product1_name, product2_name],
                "product_ids": [product1_id, product2_id],
                "individual_price": total_price,
                "bundle_price": round(bundle_price, 2),
                "discount_percentage": 10,
                "expected_profit": round(expected_profit, 2),
                "frequency": frequency,
                "reason": f"These products are frequently bought together ({frequency} times)"
            })
        
        return recommendations
    
    def _find_frequent_pairs(self, sales_df: pd.DataFrame, min_frequency: int = 2) -> List[Tuple[str, str, int]]:
        """
        Find product pairs that are frequently bought together.
        
        Args:
            sales_df: Sales DataFrame
            min_frequency: Minimum frequency to consider
            
        Returns:
            List[Tuple[str, str, int]]: Product pairs with frequency
        """
        pairs = []
        
        if sales_df.empty:
            return pairs
        
        # Group sales by invoice to find products bought together
        if 'invoice_number' in sales_df.columns and 'product_id' in sales_df.columns:
            invoice_products = sales_df.groupby('invoice_number')['product_id'].apply(list)
            
            # Count product pairs
            pair_counts = {}
            for products in invoice_products:
                if len(products) >= 2:
                    # Get unique product combinations
                    unique_products = list(set(products))
                    for pair in combinations(unique_products, 2):
                        pair_key = tuple(sorted(pair))
                        pair_counts[pair_key] = pair_counts.get(pair_key, 0) + 1
            
            # Filter by minimum frequency
            for pair, count in pair_counts.items():
                if count >= min_frequency:
                    pairs.append((pair[0], pair[1], count))
            
            # Sort by frequency
            pairs.sort(key=lambda x: x[2], reverse=True)
        
        return pairs


# Create singleton instance
bundle_engine = BundleEngine()