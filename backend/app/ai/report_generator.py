"""
Report generator for business reports.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging

from app.services.analytics_service import analytics_service
from app.services.prediction_service import prediction_service
from app.services.recommendation_service import recommendation_service
from app.services.intelligence_service import intelligence_service

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates business reports in natural language.
    """
    
    def __init__(self):
        """Initialize the report generator."""
        pass
    
    async def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily business report."""
        return await self._generate_period_report("daily", 1)
    
    async def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly business report."""
        return await self._generate_period_report("weekly", 7)
    
    async def generate_monthly_report(self) -> Dict[str, Any]:
        """Generate monthly business report."""
        return await self._generate_period_report("monthly", 30)
    
    async def generate_quarterly_report(self) -> Dict[str, Any]:
        """Generate quarterly business report."""
        return await self._generate_period_report("quarterly", 90)
    
    async def generate_yearly_report(self) -> Dict[str, Any]:
        """Generate yearly business report."""
        return await self._generate_period_report("yearly", 365)
    
    async def generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary report."""
        try:
            # Gather data
            health = await analytics_service.get_business_health()
            revenue = await analytics_service.get_revenue_analytics()
            profit = await analytics_service.get_profit_analytics()
            kpis = await analytics_service.get_kpis()
            insights = await analytics_service.generate_insights()
            inventory = await analytics_service.get_inventory_analytics()
            
            # Generate summary
            summary = f"Executive Business Summary\n\n"
            summary += f"{'='*50}\n"
            summary += f"BUSINESS OVERVIEW\n"
            summary += f"{'='*50}\n"
            summary += f"Health Score: {health.get('score', 0)}/100 ({health.get('status', 'Unknown')})\n"
            summary += f"Revenue: ${revenue.get('total', 0):,.2f}\n"
            summary += f"Profit: ${profit.get('total', 0):,.2f}\n"
            summary += f"Total Sales: {kpis.get('sales', 0)}\n\n"
            
            summary += f"{'='*50}\n"
            summary += f"KEY METRICS\n"
            summary += f"{'='*50}\n"
            summary += f"Revenue Growth: {health.get('details', {}).get('revenue_growth', 0):.1f}%\n"
            summary += f"Profit Margin: {health.get('details', {}).get('profit_margin', 0):.1f}%\n"
            summary += f"Inventory Value: ${inventory.get('inventory_value', 0):,.2f}\n"
            summary += f"Average Order Value: ${kpis.get('average_order_value', 0):,.2f}\n\n"
            
            summary += f"{'='*50}\n"
            summary += f"INSIGHTS\n"
            summary += f"{'='*50}\n"
            for insight in insights[:5]:
                summary += f"- {insight.get('message')}\n"
            
            summary += f"\n{'='*50}\n"
            summary += f"RECOMMENDATIONS\n"
            summary += f"{'='*50}\n"
            
            optimization = await recommendation_service.get_optimization_suggestions()
            for opt in optimization[:3]:
                summary += f"- {opt.get('message')}\n"
            
            return {
                "summary": summary,
                "generated_at": datetime.utcnow().isoformat(),
                "period": "executive"
            }
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            return {
                "error": f"Failed to generate executive summary: {str(e)}",
                "generated_at": datetime.utcnow().isoformat()
            }
    
    async def _generate_period_report(self, period: str, days: int) -> Dict[str, Any]:
        """Generate report for a specific period."""
        try:
            # Get period data
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Gather metrics
            health = await analytics_service.get_business_health()
            revenue = await analytics_service.get_revenue_analytics()
            profit = await analytics_service.get_profit_analytics()
            kpis = await analytics_service.get_kpis()
            insights = await analytics_service.generate_insights()
            
            # Get period-specific metrics
            period_revenue = revenue.get('total', 0)
            period_profit = profit.get('total', 0)
            
            # Generate forecast for next period
            forecast = await prediction_service.predict_revenue(days=days)
            
            # Build report
            report = f"{period.title()} Business Report\n"
            report += f"{'='*50}\n"
            report += f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n\n"
            
            report += f"Revenue: ${period_revenue:,.2f}\n"
            report += f"Profit: ${period_profit:,.2f}\n"
            report += f"Sales: {kpis.get('sales', 0)}\n"
            report += f"Health Score: {health.get('score', 0)}/100 ({health.get('status', 'Unknown')})\n\n"
            
            if forecast.get('forecast'):
                total_forecast = sum(f.get('value', 0) for f in forecast['forecast'])
                report += f"Revenue Forecast (next {period}): ${total_forecast:,.2f}\n"
                if forecast.get('explanation'):
                    report += f"Forecast Explanation: {forecast['explanation']}\n\n"
            
            report += f"{'='*50}\n"
            report += f"Key Insights for this {period}:\n"
            for insight in insights[:3]:
                report += f"- {insight.get('message')}\n"
            
            return {
                "report": report,
                "generated_at": datetime.utcnow().isoformat(),
                "period": period,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating {period} report: {str(e)}")
            return {
                "error": f"Failed to generate {period} report: {str(e)}",
                "generated_at": datetime.utcnow().isoformat()
            }


# Create singleton instance
report_generator = ReportGenerator()