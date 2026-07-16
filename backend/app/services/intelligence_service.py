"""
Intelligence service for advanced AI intelligence.
"""
import pandas as pd
from typing import Dict, Any, List
import logging

from app.database.mongodb import mongodb
from app.ai.customer_segmentation import customer_segmentation
from app.ai.anomaly_engine import anomaly_engine
from app.ai.simulation_engine import simulation_engine
from app.ai.explainable_ai import explainable_ai
from app.ai.seasonality_engine import seasonality_engine
from app.ai.market_simulator import market_simulator
from app.ai.risk_prediction import risk_prediction
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class IntelligenceService:
    """
    Advanced AI intelligence service.
    """
    
    def __init__(self):
        """Initialize the intelligence service."""
        self.sales_collection = "sales"
        self.products_collection = "products"
    
    async def get_collection(self, collection_name: str):
        """Get a collection from MongoDB."""
        return mongodb.get_collection(collection_name)
    
    async def _load_data(self) -> tuple:
        """Load product and sales data."""
        try:
            sales_collection = await self.get_collection(self.sales_collection)
            products_collection = await self.get_collection(self.products_collection)
            
            sales_cursor = sales_collection.find({})
            sales_data = await sales_cursor.to_list(length=None)
            
            products_cursor = products_collection.find({})
            products_data = await products_cursor.to_list(length=None)
            
            sales_df = pd.DataFrame(sales_data) if sales_data else pd.DataFrame()
            products_df = pd.DataFrame(products_data) if products_data else pd.DataFrame()
            
            return sales_df, products_df
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    async def get_customer_segments(self) -> List[Dict[str, Any]]:
        """Get customer segments."""
        try:
            sales_df, _ = await self._load_data()
            return customer_segmentation.segment_customers(sales_df)
        except Exception as e:
            logger.error(f"Error getting customer segments: {str(e)}")
            raise AppException(
                message=f"Failed to get customer segments: {str(e)}",
                status_code=500,
                error_code="CUSTOMER_SEGMENTATION_FAILED"
            )
    
    async def get_anomalies(self) -> List[Dict[str, Any]]:
        """Get sales anomalies."""
        try:
            sales_df, _ = await self._load_data()
            return anomaly_engine.detect_anomalies(sales_df)
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            raise AppException(
                message=f"Failed to detect anomalies: {str(e)}",
                status_code=500,
                error_code="ANOMALY_DETECTION_FAILED"
            )
    
    async def simulate_scenario(
        self,
        scenario_type: str,
        product_id: str = None,
        percentage: float = 10.0,
        days: int = 30
    ) -> Dict[str, Any]:
        """Simulate a business scenario."""
        try:
            sales_df, products_df = await self._load_data()
            return simulation_engine.simulate_scenario(
                sales_df, products_df, scenario_type, product_id, percentage, days
            )
        except Exception as e:
            logger.error(f"Error simulating scenario: {str(e)}")
            raise AppException(
                message=f"Failed to simulate scenario: {str(e)}",
                status_code=500,
                error_code="SIMULATION_FAILED"
            )
    
    async def explain_intelligence(self) -> Dict[str, Any]:
        """Generate explainable AI insights."""
        try:
            sales_df, products_df = await self._load_data()
            
            # Prepare context
            context = self._prepare_context(sales_df, products_df)
            
            # Generate explanations
            explanations = explainable_ai.explain_prediction(
                prediction={"value": sales_df['total_sale_amount'].sum() if not sales_df.empty else 0},
                context=context
            )
            
            return explanations
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            raise AppException(
                message=f"Failed to generate explanation: {str(e)}",
                status_code=500,
                error_code="EXPLAINABLE_AI_FAILED"
            )
    
    async def detect_seasonality(self) -> Dict[str, Any]:
        """Detect seasonality patterns."""
        try:
            sales_df, _ = await self._load_data()
            return seasonality_engine.detect_seasonality(sales_df)
        except Exception as e:
            logger.error(f"Error detecting seasonality: {str(e)}")
            raise AppException(
                message=f"Failed to detect seasonality: {str(e)}",
                status_code=500,
                error_code="SEASONALITY_DETECTION_FAILED"
            )
    
    async def get_market_trends(self) -> Dict[str, Any]:
        """Get market trend simulation."""
        try:
            sales_df, _ = await self._load_data()
            return market_simulator.simulate_market_trends(sales_df)
        except Exception as e:
            logger.error(f"Error getting market trends: {str(e)}")
            raise AppException(
                message=f"Failed to get market trends: {str(e)}",
                status_code=500,
                error_code="MARKET_TRENDS_FAILED"
            )
    
    async def predict_risks(self) -> Dict[str, Any]:
        """Predict business risks."""
        try:
            sales_df, products_df = await self._load_data()
            return risk_prediction.predict_business_risk(sales_df, products_df)
        except Exception as e:
            logger.error(f"Error predicting risks: {str(e)}")
            raise AppException(
                message=f"Failed to predict risks: {str(e)}",
                status_code=500,
                error_code="RISK_PREDICTION_FAILED"
            )
    
    async def generate_insights(self) -> List[Dict[str, Any]]:
        """Generate AI insights."""
        try:
            sales_df, products_df = await self._load_data()
            
            insights = []
            
            # 1. Revenue insights
            if not sales_df.empty:
                total_revenue = sales_df['total_sale_amount'].sum()
                insights.append({
                    "type": "positive" if total_revenue > 0 else "neutral",
                    "category": "revenue",
                    "message": f"Total revenue: ${total_revenue:,.2f}",
                    "priority": "low"
                })
            
            # 2. Customer insights
            segments = customer_segmentation.segment_customers(sales_df)
            if segments:
                top_segment = segments[0]
                insights.append({
                    "type": "positive",
                    "category": "customer",
                    "message": f"Top customer segment: {top_segment['segment_name']} ({top_segment['customer_count']} customers)",
                    "priority": "medium"
                })
            
            # 3. Anomaly insights
            anomalies = anomaly_engine.detect_anomalies(sales_df)
            critical_anomalies = [a for a in anomalies if a.get('severity') == 'critical']
            if critical_anomalies:
                insights.append({
                    "type": "negative",
                    "category": "anomaly",
                    "message": f"Critical anomalies detected: {len(critical_anomalies)}",
                    "priority": "high"
                })
            
            # 4. Seasonality insights
            seasonality = seasonality_engine.detect_seasonality(sales_df)
            if seasonality.get('has_seasonality'):
                insights.append({
                    "type": "neutral",
                    "category": "seasonality",
                    "message": "Seasonal patterns detected in sales data",
                    "priority": "medium"
                })
            
            # 5. Risk insights
            risks = risk_prediction.predict_business_risk(sales_df, products_df)
            overall_risk = risks.get('overall_risk', {})
            if overall_risk.get('level') in ['High Risk', 'Critical Risk']:
                insights.append({
                    "type": "negative",
                    "category": "risk",
                    "message": f"Overall business risk: {overall_risk.get('level', 'Unknown')}",
                    "priority": "high"
                })
            
            if not insights:
                insights.append({
                    "type": "neutral",
                    "category": "general",
                    "message": "No significant insights to report",
                    "priority": "low"
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            raise AppException(
                message=f"Failed to generate insights: {str(e)}",
                status_code=500,
                error_code="INSIGHTS_GENERATION_FAILED"
            )
    
    async def compare_scenarios(self, scenario_a: Dict, scenario_b: Dict, days: int = 30) -> Dict[str, Any]:
        """Compare business scenarios."""
        try:
            sales_df, products_df = await self._load_data()
            
            # Run simulations for both scenarios
            result_a = simulation_engine.simulate_scenario(
                sales_df, products_df,
                scenario_a.get('type', 'price_increase'),
                scenario_a.get('product_id'),
                scenario_a.get('percentage', 10),
                days
            )
            
            result_b = simulation_engine.simulate_scenario(
                sales_df, products_df,
                scenario_b.get('type', 'price_decrease'),
                scenario_b.get('product_id'),
                scenario_b.get('percentage', 10),
                days
            )
            
            # Compare results
            comparison = {
                "scenario_a": {
                    "name": "Scenario A",
                    "projected_revenue": result_a.get('projected', {}).get('revenue', 0),
                    "projected_profit": result_a.get('projected', {}).get('profit', 0),
                    "impact": result_a.get('impact', {})
                },
                "scenario_b": {
                    "name": "Scenario B",
                    "projected_revenue": result_b.get('projected', {}).get('revenue', 0),
                    "projected_profit": result_b.get('projected', {}).get('profit', 0),
                    "impact": result_b.get('impact', {})
                },
                "recommendation": self._determine_better_scenario(result_a, result_b),
                "confidence_score": 75
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing scenarios: {str(e)}")
            raise AppException(
                message=f"Failed to compare scenarios: {str(e)}",
                status_code=500,
                error_code="SCENARIO_COMPARISON_FAILED"
            )
    
    def _prepare_context(self, sales_df: pd.DataFrame, products_df: pd.DataFrame) -> Dict[str, Any]:
        """Prepare context for explainable AI."""
        context = {}
        
        if not sales_df.empty:
            # Sales trend
            if 'sale_date' in sales_df.columns:
                sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
                if len(sales_df) > 1:
                    monthly = sales_df.groupby(sales_df['sale_date'].dt.month)['total_sale_amount'].sum()
                    if len(monthly) > 1:
                        growth = (monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2] * 100
                        context['sales_trend'] = "upward" if growth > 0 else "downward"
            
            # Profit margin
            if 'profit' in sales_df.columns:
                total_revenue = sales_df['total_sale_amount'].sum()
                total_profit = sales_df['profit'].sum()
                if total_revenue > 0:
                    context['profit_margin'] = (total_profit / total_revenue) * 100
        
        if not products_df.empty:
            # Inventory health
            if 'stock' in products_df.columns and 'minimum_stock' in products_df.columns:
                total = len(products_df)
                low_stock = len(products_df[products_df['stock'] <= products_df['minimum_stock']])
                if total > 0:
                    context['inventory_health'] = (1 - low_stock / total) * 100
        
        # Customer health
        if not sales_df.empty and 'customer_name' in sales_df.columns:
            customer_counts = sales_df['customer_name'].value_counts()
            repeat_customers = len(customer_counts[customer_counts > 1])
            total_customers = len(customer_counts)
            if total_customers > 0:
                context['customer_health'] = (repeat_customers / total_customers) * 100
        
        context['data_quality'] = 80  # Default
        
        return context
    
    def _determine_better_scenario(self, result_a: Dict, result_b: Dict) -> Dict[str, Any]:
        """Determine which scenario is better."""
        revenue_a = result_a.get('projected', {}).get('revenue', 0)
        revenue_b = result_b.get('projected', {}).get('revenue', 0)
        
        profit_a = result_a.get('projected', {}).get('profit', 0)
        profit_b = result_b.get('projected', {}).get('profit', 0)
        
        if revenue_a > revenue_b and profit_a > profit_b:
            return {
                "better_scenario": "Scenario A",
                "reason": "Higher projected revenue and profit",
                "confidence": 85
            }
        elif revenue_b > revenue_a and profit_b > profit_a:
            return {
                "better_scenario": "Scenario B",
                "reason": "Higher projected revenue and profit",
                "confidence": 85
            }
        elif revenue_a > revenue_b:
            return {
                "better_scenario": "Scenario A",
                "reason": "Higher projected revenue",
                "confidence": 70
            }
        elif profit_a > profit_b:
            return {
                "better_scenario": "Scenario A",
                "reason": "Higher projected profit",
                "confidence": 70
            }
        else:
            return {
                "better_scenario": "Neither",
                "reason": "Scenarios are comparable",
                "confidence": 60
            }


# Create singleton instance
intelligence_service = IntelligenceService()