"""
Prompt templates for the AI Business Assistant.
"""
from typing import Dict, Any


class PromptTemplates:
    """
    Prompt templates for different query types.
    """
    
    @staticmethod
    def get_template(query_type: str) -> str:
        """Get template for query type."""
        templates = {
            "inventory": """
                Business Intelligence Report - Inventory Analysis
                
                Products with Low Stock: {low_stock_count}
                Products with High Stock: {high_stock_count}
                Total Inventory Value: ${inventory_value:,.2f}
                
                Restock Recommendations: {restock_recommendations}
                Dead Stock: {dead_stock}
            """,
            
            "sales": """
                Business Intelligence Report - Sales Analysis
                
                Total Revenue: ${total_revenue:,.2f}
                Total Profit: ${total_profit:,.2f}
                Total Sales: {total_sales}
                Average Order Value: ${avg_order_value:,.2f}
                
                Top Selling Products: {top_products}
                Best Categories: {best_categories}
            """,
            
            "analytics": """
                Business Intelligence Report - Analytics
                
                Revenue Growth: {revenue_growth}%
                Profit Margin: {profit_margin}%
                Business Health Score: {health_score}/100
                
                Business Health Status: {health_status}
                Key Insights: {key_insights}
            """,
            
            "forecasting": """
                Business Intelligence Report - Forecasting
                
                Revenue Forecast: ${revenue_forecast:,.2f}
                Profit Forecast: ${profit_forecast:,.2f}
                Demand Forecast: {demand_forecast}
                
                Forecast Confidence: {confidence}%
                Model Used: {model}
                Explanation: {explanation}
            """,
            
            "recommendation": """
                Business Intelligence Report - Recommendations
                
                {recommendations}
                
                Priority: {priority}
                Expected Impact: {impact}
            """,
            
            "risk": """
                Business Intelligence Report - Risk Assessment
                
                Overall Risk Level: {risk_level}
                Risk Score: {risk_score}/100
                
                Risk Factors: {risk_factors}
                Recommendations: {risk_recommendations}
            """,
            
            "health": """
                Business Intelligence Report - Business Health
                
                Health Score: {health_score}/100
                Status: {health_status}
                
                Revenue Growth: {revenue_growth}%
                Profit Margin: {profit_margin}%
                Inventory Health: {inventory_health}%
                
                Overall Assessment: {assessment}
            """,
            
            "general": """
                Business Intelligence Response
                
                {answer}
                
                Confidence: {confidence}%
                Data Sources: {sources}
            """
        }
        
        return templates.get(query_type, templates["general"])


# Create singleton instance
prompt_templates = PromptTemplates()