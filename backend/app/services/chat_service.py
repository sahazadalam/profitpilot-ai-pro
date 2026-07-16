"""
Chat service for AI Business Assistant.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.ai.business_assistant import business_assistant
from app.ai.conversation_memory import conversation_memory
from app.ai.report_generator import report_generator
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class ChatService:
    """
    Chat service for AI Business Assistant.
    """
    
    def __init__(self):
        """Initialize the chat service."""
        pass
    
    async def process_chat(
        self,
        user_id: str,
        question: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message.
        
        Args:
            user_id: User ID
            question: User question
            conversation_id: Optional conversation ID
            
        Returns:
            Dict[str, Any]: Chat response
        """
        try:
            return await business_assistant.process_question(
                user_id=user_id,
                question=question,
                conversation_id=conversation_id
            )
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            raise AppException(
                message=f"Failed to process chat: {str(e)}",
                status_code=500,
                error_code="CHAT_PROCESSING_FAILED"
            )
    
    async def get_history(self, conversation_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get chat history.
        
        Args:
            conversation_id: Conversation ID
            limit: Number of messages to return
            
        Returns:
            List[Dict[str, Any]]: Chat history
        """
        try:
            return await conversation_memory.get_history(conversation_id, limit)
        except Exception as e:
            logger.error(f"Error getting history: {str(e)}")
            raise AppException(
                message=f"Failed to get history: {str(e)}",
                status_code=500,
                error_code="HISTORY_RETRIEVAL_FAILED"
            )
    
    async def clear_history(self, conversation_id: str) -> bool:
        """
        Clear chat history.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            bool: Success status
        """
        try:
            return await conversation_memory.clear_history(conversation_id)
        except Exception as e:
            logger.error(f"Error clearing history: {str(e)}")
            raise AppException(
                message=f"Failed to clear history: {str(e)}",
                status_code=500,
                error_code="HISTORY_CLEAR_FAILED"
            )
    
    async def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily report."""
        try:
            return await report_generator.generate_daily_report()
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}")
            raise AppException(
                message=f"Failed to generate daily report: {str(e)}",
                status_code=500,
                error_code="REPORT_GENERATION_FAILED"
            )
    
    async def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly report."""
        try:
            return await report_generator.generate_weekly_report()
        except Exception as e:
            logger.error(f"Error generating weekly report: {str(e)}")
            raise AppException(
                message=f"Failed to generate weekly report: {str(e)}",
                status_code=500,
                error_code="REPORT_GENERATION_FAILED"
            )
    
    async def generate_monthly_report(self) -> Dict[str, Any]:
        """Generate monthly report."""
        try:
            return await report_generator.generate_monthly_report()
        except Exception as e:
            logger.error(f"Error generating monthly report: {str(e)}")
            raise AppException(
                message=f"Failed to generate monthly report: {str(e)}",
                status_code=500,
                error_code="REPORT_GENERATION_FAILED"
            )
    
    async def generate_quarterly_report(self) -> Dict[str, Any]:
        """Generate quarterly report."""
        try:
            return await report_generator.generate_quarterly_report()
        except Exception as e:
            logger.error(f"Error generating quarterly report: {str(e)}")
            raise AppException(
                message=f"Failed to generate quarterly report: {str(e)}",
                status_code=500,
                error_code="REPORT_GENERATION_FAILED"
            )
    
    async def generate_yearly_report(self) -> Dict[str, Any]:
        """Generate yearly report."""
        try:
            return await report_generator.generate_yearly_report()
        except Exception as e:
            logger.error(f"Error generating yearly report: {str(e)}")
            raise AppException(
                message=f"Failed to generate yearly report: {str(e)}",
                status_code=500,
                error_code="REPORT_GENERATION_FAILED"
            )
    
    async def generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary."""
        try:
            return await report_generator.generate_executive_summary()
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            raise AppException(
                message=f"Failed to generate executive summary: {str(e)}",
                status_code=500,
                error_code="EXECUTIVE_SUMMARY_FAILED"
            )
    
    async def get_business_alerts(self) -> Dict[str, Any]:
        """
        Get business alerts.
        
        Returns:
            Dict[str, Any]: Business alerts
        """
        try:
            from app.services.analytics_service import analytics_service
            from app.services.recommendation_service import recommendation_service
            
            alerts = {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            }
            
            # Get inventory alerts
            inventory = await analytics_service.get_inventory_analytics()
            if inventory.get('out_of_stock', 0) > 0:
                alerts["critical"].append({
                    "type": "inventory",
                    "message": f"{inventory['out_of_stock']} products are out of stock",
                    "action": "Immediately restock out-of-stock items"
                })
            
            if inventory.get('low_stock', 0) > 3:
                alerts["high"].append({
                    "type": "inventory",
                    "message": f"{inventory['low_stock']} products are low on stock",
                    "action": "Review and restock low-stock items"
                })
            
            # Get revenue alerts
            revenue = await analytics_service.get_revenue_analytics()
            if revenue.get('today', 0) < revenue.get('weekly', 0) / 7 * 0.5 and revenue.get('weekly', 0) > 0:
                alerts["high"].append({
                    "type": "revenue",
                    "message": "Today's revenue is significantly below daily average",
                    "action": "Review sales performance and consider promotions"
                })
            
            # Get health alerts
            health = await analytics_service.get_business_health()
            if health.get('score', 0) < 50:
                alerts["critical"].append({
                    "type": "health",
                    "message": f"Business health score is low ({health['score']}/100)",
                    "action": "Immediate business review required"
                })
            elif health.get('score', 0) < 65:
                alerts["medium"].append({
                    "type": "health",
                    "message": f"Business health score needs improvement ({health['score']}/100)",
                    "action": "Review and address weak areas"
                })
            
            # Get restock alerts
            restock = await recommendation_service.get_restock_recommendations()
            high_priority = [r for r in restock if r.get('priority') == 'high']
            for rec in high_priority[:3]:
                alerts["high"].append({
                    "type": "restock",
                    "message": f"Restock needed for {rec.get('product_name')} - {rec.get('reason')}",
                    "action": f"Order {rec.get('recommended_quantity')} units"
                })
            
            # Count alerts
            alert_counts = {key: len(value) for key, value in alerts.items()}
            alert_counts['total'] = sum(alert_counts.values())
            
            return {
                "alerts": alerts,
                "counts": alert_counts,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting business alerts: {str(e)}")
            raise AppException(
                message=f"Failed to get business alerts: {str(e)}",
                status_code=500,
                error_code="ALERTS_GENERATION_FAILED"
            )
    
    async def get_action_plan(self) -> Dict[str, Any]:
        """
        Get prioritized action plan.
        
        Returns:
            Dict[str, Any]: Action plan
        """
        try:
            from app.services.recommendation_service import recommendation_service
            from app.services.analytics_service import analytics_service
            
            actions = {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            }
            
            # Get recommendations
            restock = await recommendation_service.get_restock_recommendations()
            high_priority = [r for r in restock if r.get('priority') == 'high']
            
            for rec in high_priority:
                actions["high"].append({
                    "action": f"Restock {rec.get('product_name')}",
                    "details": rec.get('reason'),
                    "expected_benefit": "Prevent stockout and maintain sales",
                    "estimated_impact": "Revenue protection"
                })
            
            # Get optimization suggestions
            optimization = await recommendation_service.get_optimization_suggestions()
            for opt in optimization:
                priority = opt.get('priority', 'medium')
                actions[priority].append({
                    "action": opt.get('message'),
                    "details": f"Impact: {opt.get('impact')}",
                    "expected_benefit": "Improve business efficiency",
                    "estimated_impact": "Operational improvement"
                })
            
            # Add risk-based actions
            health = await analytics_service.get_business_health()
            if health.get('score', 0) < 50:
                actions["critical"].append({
                    "action": "Urgent Business Review",
                    "details": f"Health score is {health.get('score', 0)}/100",
                    "expected_benefit": "Identify and address critical issues",
                    "estimated_impact": "Business recovery"
                })
            
            return {
                "actions": actions,
                "generated_at": datetime.utcnow().isoformat(),
                "total_actions": sum(len(v) for v in actions.values())
            }
            
        except Exception as e:
            logger.error(f"Error getting action plan: {str(e)}")
            raise AppException(
                message=f"Failed to get action plan: {str(e)}",
                status_code=500,
                error_code="ACTION_PLAN_FAILED"
            )


# Create singleton instance
chat_service = ChatService()