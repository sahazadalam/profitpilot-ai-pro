"""
Query Router for routing questions to appropriate AI modules.
"""
from typing import Dict, Any, Tuple
import logging

from app.ai.nl_query_engine import nl_query_engine
from app.services.analytics_service import analytics_service
from app.services.prediction_service import prediction_service
from app.services.recommendation_service import recommendation_service
from app.services.intelligence_service import intelligence_service
from app.services.dashboard_service import dashboard_service

logger = logging.getLogger(__name__)


class QueryRouter:
    """
    Routes user questions to appropriate AI modules.
    """
    
    def __init__(self):
        """Initialize the query router."""
        self.routes = {
            "inventory": self._handle_inventory_query,
            "sales": self._handle_sales_query,
            "analytics": self._handle_analytics_query,
            "forecasting": self._handle_forecasting_query,
            "recommendation": self._handle_recommendation_query,
            "risk": self._handle_risk_query,
            "health": self._handle_health_query,
            "report": self._handle_report_query,
            "general": self._handle_general_query
        }
    
    async def route_query(self, question: str) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        """
        Route query to appropriate handler.
        
        Args:
            question: User question
            
        Returns:
            Tuple[Dict, str, Dict]: Response data, query type, and metadata
        """
        # Classify the query
        query_type, metadata = nl_query_engine.classify_query(question)
        
        logger.info(f"Routing query: '{question}' -> {query_type}")
        
        # Get the appropriate handler
        handler = self.routes.get(query_type, self._handle_general_query)
        
        # Execute the handler
        try:
            result = await handler(question, metadata)
            return result, query_type, metadata
        except Exception as e:
            logger.error(f"Error handling query '{query_type}': {str(e)}")
            return {
                "answer": f"I encountered an error while processing your question. Please try again.",
                "confidence": 0,
                "error": str(e)
            }, query_type, metadata
    
    async def _handle_inventory_query(self, question: str, metadata: Dict) -> Dict:
        """Handle inventory-related queries."""
        # Get inventory analytics
        inventory = await analytics_service.get_inventory_analytics()
        restock = await recommendation_service.get_restock_recommendations()
        
        answer = f"Inventory Analysis:\n"
        answer += f"- Total Products: {inventory.get('total_products', 0)}\n"
        answer += f"- Inventory Value: ${inventory.get('inventory_value', 0):,.2f}\n"
        answer += f"- Out of Stock: {inventory.get('out_of_stock', 0)}\n"
        answer += f"- Low Stock: {inventory.get('low_stock', 0)}\n\n"
        
        if restock and len(restock) > 0:
            answer += "Restock Recommendations:\n"
            for rec in restock[:3]:
                answer += f"- {rec.get('product_name')}: Order {rec.get('recommended_quantity')} units (Priority: {rec.get('priority')})\n"
        
        return {
            "answer": answer,
            "confidence": 85,
            "data": inventory
        }
    
    async def _handle_sales_query(self, question: str, metadata: Dict) -> Dict:
        """Handle sales-related queries."""
        # Get sales analytics
        revenue = await analytics_service.get_revenue_analytics()
        profit = await analytics_service.get_profit_analytics()
        kpis = await analytics_service.get_kpis()
        
        answer = f"Sales Analysis:\n"
        answer += f"- Total Revenue: ${revenue.get('total', 0):,.2f}\n"
        answer += f"- Total Profit: ${profit.get('total', 0):,.2f}\n"
        answer += f"- Total Sales: {kpis.get('sales', 0)}\n"
        answer += f"- Average Order Value: ${kpis.get('average_order_value', 0):,.2f}\n"
        answer += f"- Monthly Revenue: ${revenue.get('monthly', 0):,.2f}\n"
        answer += f"- Weekly Revenue: ${revenue.get('weekly', 0):,.2f}\n"
        answer += f"- Today's Revenue: ${revenue.get('today', 0):,.2f}\n"
        
        # Check if asking about best product
        if "best" in question.lower() or "top" in question.lower():
            top_products = await analytics_service.get_top_products(5)
            if top_products:
                answer += "\nTop Products:\n"
                for i, product in enumerate(top_products[:3], 1):
                    answer += f"{i}. {product.get('product_name')} - ${product.get('total_revenue', 0):,.2f}\n"
        
        return {
            "answer": answer,
            "confidence": 90,
            "data": {"revenue": revenue, "profit": profit, "kpis": kpis}
        }
    
    async def _handle_analytics_query(self, question: str, metadata: Dict) -> Dict:
        """Handle analytics-related queries."""
        # Get analytics data
        health = await analytics_service.get_business_health()
        insights = await analytics_service.generate_insights()
        growth = await analytics_service.get_growth_analytics()
        
        answer = f"Business Analytics:\n"
        answer += f"- Health Score: {health.get('score', 0)}/100 ({health.get('status', 'Unknown')})\n"
        answer += f"- Revenue Growth: {growth.get('weekly_growth', {}).get('revenue', 0):.1f}%\n"
        answer += f"- Profit Margin: {health.get('details', {}).get('profit_margin', 0):.1f}%\n"
        answer += f"- Inventory Health: {health.get('details', {}).get('inventory_health', 0):.1f}%\n\n"
        
        if insights:
            answer += "Key Insights:\n"
            for insight in insights[:3]:
                answer += f"- {insight.get('message')}\n"
        
        return {
            "answer": answer,
            "confidence": 88,
            "data": {"health": health, "insights": insights}
        }
    
    async def _handle_forecasting_query(self, question: str, metadata: Dict) -> Dict:
        """Handle forecasting-related queries."""
        # Get predictions
        revenue_forecast = await prediction_service.predict_revenue(days=30)
        profit_forecast = await prediction_service.predict_profit(days=30)
        demand_forecast = await prediction_service.predict_demand(days=30)
        
        answer = f"Business Forecast:\n"
        
        if revenue_forecast.get('forecast'):
            total_revenue = sum(f.get('value', 0) for f in revenue_forecast['forecast'])
            answer += f"- Revenue Forecast (30 days): ${total_revenue:,.2f}\n"
        
        if profit_forecast.get('forecast'):
            total_profit = sum(f.get('value', 0) for f in profit_forecast['forecast'])
            answer += f"- Profit Forecast (30 days): ${total_profit:,.2f}\n"
        
        if demand_forecast.get('forecast'):
            total_demand = sum(f.get('value', 0) for f in demand_forecast['forecast'])
            answer += f"- Demand Forecast (30 days): {total_demand:,.0f} units\n"
        
        if revenue_forecast.get('explanation'):
            answer += f"\n{revenue_forecast.get('explanation')}"
        
        return {
            "answer": answer,
            "confidence": 80,
            "data": {
                "revenue_forecast": revenue_forecast,
                "profit_forecast": profit_forecast,
                "demand_forecast": demand_forecast
            }
        }
    
    async def _handle_recommendation_query(self, question: str, metadata: Dict) -> Dict:
        """Handle recommendation-related queries."""
        # Get recommendations
        restock = await recommendation_service.get_restock_recommendations()
        pricing = await recommendation_service.get_pricing_recommendations()
        optimization = await recommendation_service.get_optimization_suggestions()
        
        answer = f"Business Recommendations:\n\n"
        
        # Priority recommendations
        if restock:
            high_priority = [r for r in restock if r.get('priority') == 'high']
            if high_priority:
                answer += "High Priority Actions:\n"
                for rec in high_priority[:3]:
                    answer += f"- Restock {rec.get('product_name')}: {rec.get('reason')}\n"
                answer += "\n"
        
        if optimization:
            answer += "Optimization Suggestions:\n"
            for opt in optimization[:3]:
                answer += f"- {opt.get('message')} (Priority: {opt.get('priority')})\n"
        
        if pricing and len(pricing) > 0:
            answer += f"\nPricing Recommendations:\n"
            for p in pricing[:2]:
                answer += f"- {p.get('product_name')}: {p.get('action')} price to ${p.get('suggested_price'):,.2f}\n"
        
        return {
            "answer": answer,
            "confidence": 85,
            "data": {"restock": restock, "pricing": pricing, "optimization": optimization}
        }
    
    async def _handle_risk_query(self, question: str, metadata: Dict) -> Dict:
        """Handle risk-related queries."""
        # Get risk analysis
        risk = await analytics_service.get_business_health()
        insights = await analytics_service.generate_insights()
        
        answer = f"Business Risk Assessment:\n"
        answer += f"- Risk Score: {risk.get('score', 0)}/100\n"
        answer += f"- Risk Level: {risk.get('status', 'Unknown')}\n"
        answer += f"- Profit Margin: {risk.get('details', {}).get('profit_margin', 0):.1f}%\n"
        answer += f"- Revenue Growth: {risk.get('details', {}).get('revenue_growth', 0):.1f}%\n"
        answer += f"- Inventory Health: {risk.get('details', {}).get('inventory_health', 0):.1f}%\n\n"
        
        critical_insights = [i for i in insights if i.get('priority') in ['high', 'critical']]
        if critical_insights:
            answer += "Critical Risks:\n"
            for insight in critical_insights[:3]:
                answer += f"- {insight.get('message')}\n"
        
        return {
            "answer": answer,
            "confidence": 82,
            "data": {"risk": risk, "insights": insights}
        }
    
    async def _handle_health_query(self, question: str, metadata: Dict) -> Dict:
        """Handle business health-related queries."""
        # Get health data
        health = await analytics_service.get_business_health()
        kpis = await analytics_service.get_kpis()
        
        answer = f"Business Health Report:\n"
        answer += f"- Health Score: {health.get('score', 0)}/100\n"
        answer += f"- Status: {health.get('status', 'Unknown')}\n\n"
        answer += f"Key Metrics:\n"
        answer += f"- Revenue: ${kpis.get('revenue', 0):,.2f}\n"
        answer += f"- Profit: ${kpis.get('profit', 0):,.2f}\n"
        answer += f"- Sales: {kpis.get('sales', 0)}\n"
        answer += f"- Average Order Value: ${kpis.get('average_order_value', 0):,.2f}\n\n"
        
        if health.get('explanation'):
            answer += f"Health Assessment: {health.get('explanation')[:200]}...\n"
        
        return {
            "answer": answer,
            "confidence": 90,
            "data": {"health": health, "kpis": kpis}
        }
    
    async def _handle_report_query(self, question: str, metadata: Dict) -> Dict:
        """Handle report-related queries."""
        # Generate comprehensive report
        health = await analytics_service.get_business_health()
        revenue = await analytics_service.get_revenue_analytics()
        profit = await analytics_service.get_profit_analytics()
        kpis = await analytics_service.get_kpis()
        insights = await analytics_service.generate_insights()
        
        answer = f"Executive Business Report:\n\n"
        answer += f"{'='*50}\n"
        answer += f"PERFORMANCE SUMMARY\n"
        answer += f"{'='*50}\n"
        answer += f"Health Score: {health.get('score', 0)}/100 ({health.get('status', 'Unknown')})\n"
        answer += f"Total Revenue: ${revenue.get('total', 0):,.2f}\n"
        answer += f"Total Profit: ${profit.get('total', 0):,.2f}\n"
        answer += f"Total Sales: {kpis.get('sales', 0)}\n\n"
        
        answer += f"{'='*50}\n"
        answer += f"KEY INSIGHTS\n"
        answer += f"{'='*50}\n"
        for insight in insights[:5]:
            answer += f"- {insight.get('message')}\n"
        
        answer += f"\n{'='*50}\n"
        answer += f"RECOMMENDATIONS\n"
        answer += f"{'='*50}\n"
        
        # Get recommendations
        optimization = await recommendation_service.get_optimization_suggestions()
        for opt in optimization[:3]:
            answer += f"- {opt.get('message')}\n"
        
        return {
            "answer": answer,
            "confidence": 92,
            "data": {
                "health": health,
                "revenue": revenue,
                "profit": profit,
                "kpis": kpis,
                "insights": insights
            }
        }
    
    async def _handle_general_query(self, question: str, metadata: Dict) -> Dict:
        """Handle general queries."""
        answer = f"I understand you're asking about: '{question}'\n\n"
        answer += "I can help you with questions about:\n"
        answer += "- Business performance and metrics\n"
        answer += "- Inventory management\n"
        answer += "- Sales and revenue analysis\n"
        answer += "- Profitability and growth\n"
        answer += "- Forecasting and predictions\n"
        answer += "- Business recommendations\n"
        answer += "- Risk assessment\n\n"
        answer += "Please rephrase your question or ask a more specific business question."
        
        return {
            "answer": answer,
            "confidence": 60,
            "data": {"guidance": "Please ask a more specific business question"}
        }


# Create singleton instance
query_router = QueryRouter()