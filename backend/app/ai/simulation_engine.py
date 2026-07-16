"""
What-If Business Simulation Engine.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class SimulationEngine:
    """
    What-If business simulation engine.
    """
    
    def __init__(self):
        """Initialize the simulation engine."""
        pass
    
    def simulate_scenario(
        self,
        sales_df: pd.DataFrame,
        products_df: pd.DataFrame,
        scenario_type: str,
        product_id: str = None,
        percentage: float = 10.0,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Simulate a business scenario.
        
        Args:
            sales_df: Sales DataFrame
            products_df: Products DataFrame
            scenario_type: Type of scenario
            product_id: Product ID for product-specific simulation
            percentage: Percentage change
            days: Simulation period
            
        Returns:
            Dict[str, Any]: Simulation results
        """
        # Get historical data
        historical_data = self._get_historical_data(sales_df, product_id, days)
        
        if historical_data.empty:
            return {
                "error": "Insufficient historical data for simulation",
                "scenario": scenario_type,
                "expected_impact": "unknown"
            }
        
        # Calculate baseline metrics
        baseline_revenue = historical_data['total_sale_amount'].sum()
        baseline_profit = historical_data['profit'].sum() if 'profit' in historical_data.columns else baseline_revenue * 0.2
        baseline_quantity = historical_data['quantity'].sum() if 'quantity' in historical_data.columns else 0
        
        # Simulate based on scenario type
        if scenario_type == "price_increase":
            return self._simulate_price_change(
                historical_data, percentage, "increase", baseline_revenue, baseline_profit, baseline_quantity
            )
        elif scenario_type == "price_decrease":
            return self._simulate_price_change(
                historical_data, percentage, "decrease", baseline_revenue, baseline_profit, baseline_quantity
            )
        elif scenario_type == "stock_increase":
            return self._simulate_stock_change(
                historical_data, percentage, "increase", baseline_revenue, baseline_profit
            )
        elif scenario_type == "stock_decrease":
            return self._simulate_stock_change(
                historical_data, percentage, "decrease", baseline_revenue, baseline_profit
            )
        else:
            return {"error": f"Unknown scenario type: {scenario_type}"}
    
    def _get_historical_data(self, sales_df: pd.DataFrame, product_id: str, days: int) -> pd.DataFrame:
        """Get historical data for simulation."""
        if sales_df.empty:
            return pd.DataFrame()
        
        df = sales_df.copy()
        
        # Filter by product if specified
        if product_id:
            df = df[df['product_id'] == product_id]
        
        # Filter by date range (last N days)
        if 'sale_date' in df.columns:
            df['sale_date'] = pd.to_datetime(df['sale_date'])
            cutoff = df['sale_date'].max() - pd.Timedelta(days=days)
            df = df[df['sale_date'] >= cutoff]
        
        return df
    
    def _simulate_price_change(
        self,
        df: pd.DataFrame,
        percentage: float,
        direction: str,
        baseline_revenue: float,
        baseline_profit: float,
        baseline_quantity: float
    ) -> Dict[str, Any]:
        """Simulate price change."""
        price_elasticity = -1.5  # Typical price elasticity
        
        # Calculate price change factor
        price_change = percentage / 100 * (1 if direction == "increase" else -1)
        quantity_change = price_elasticity * price_change
        
        # Apply to baseline
        new_quantity = baseline_quantity * (1 + quantity_change)
        new_revenue = baseline_revenue * (1 + price_change) * (1 + quantity_change * 0.5)
        new_profit = new_revenue - (baseline_revenue - baseline_profit) * (new_quantity / baseline_quantity)
        
        return {
            "scenario": f"price_{direction}",
            "percentage": percentage,
            "baseline": {
                "revenue": float(round(baseline_revenue, 2)),
                "profit": float(round(baseline_profit, 2)),
                "quantity": int(baseline_quantity)
            },
            "projected": {
                "revenue": float(round(new_revenue, 2)),
                "profit": float(round(new_profit, 2)),
                "quantity": int(new_quantity)
            },
            "impact": {
                "revenue_change_percent": float(round(((new_revenue - baseline_revenue) / baseline_revenue * 100) if baseline_revenue > 0 else 0, 1)),
                "profit_change_percent": float(round(((new_profit - baseline_profit) / baseline_profit * 100) if baseline_profit > 0 else 0, 1)),
                "recommendation": self._generate_recommendation(
                    direction, ((new_revenue - baseline_revenue) / baseline_revenue * 100) if baseline_revenue > 0 else 0
                )
            },
            "confidence_score": 75
        }
    
    def _simulate_stock_change(
        self,
        df: pd.DataFrame,
        percentage: float,
        direction: str,
        baseline_revenue: float,
        baseline_profit: float
    ) -> Dict[str, Any]:
        """Simulate stock change."""
        # Stock changes affect ability to fulfill demand
        stock_elasticity = 0.3
        
        stock_change = percentage / 100 * (1 if direction == "increase" else -1)
        demand_change = stock_elasticity * stock_change
        
        new_revenue = baseline_revenue * (1 + demand_change)
        new_profit = baseline_profit * (1 + demand_change * 0.8)  # Profit margin slightly affected
        
        return {
            "scenario": f"stock_{direction}",
            "percentage": percentage,
            "baseline": {
                "revenue": float(round(baseline_revenue, 2)),
                "profit": float(round(baseline_profit, 2))
            },
            "projected": {
                "revenue": float(round(new_revenue, 2)),
                "profit": float(round(new_profit, 2))
            },
            "impact": {
                "revenue_change_percent": float(round(((new_revenue - baseline_revenue) / baseline_revenue * 100) if baseline_revenue > 0 else 0, 1)),
                "profit_change_percent": float(round(((new_profit - baseline_profit) / baseline_profit * 100) if baseline_profit > 0 else 0, 1)),
                "recommendation": self._generate_recommendation(
                    direction, ((new_revenue - baseline_revenue) / baseline_revenue * 100) if baseline_revenue > 0 else 0
                )
            },
            "confidence_score": 70
        }
    
    def _generate_recommendation(self, direction: str, impact: float) -> str:
        """Generate recommendation based on simulation."""
        if direction == "increase":
            if impact > 5:
                return "Price increase is recommended - expected positive impact on revenue"
            elif impact > 0:
                return "Price increase may have moderate impact - consider implementing"
            else:
                return "Price increase may negatively impact revenue - consider alternatives"
        else:
            if impact > 5:
                return "Price decrease recommended - expected to boost sales and revenue"
            elif impact > 0:
                return "Price decrease may have moderate impact - consider implementing"
            else:
                return "Price decrease may not be beneficial - consider alternatives"


# Create singleton instance
simulation_engine = SimulationEngine()