"""
AI Business Assistant that orchestrates all AI capabilities.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import uuid

from app.ai.query_router import query_router
from app.ai.conversation_memory import conversation_memory
from app.ai.report_generator import report_generator
from app.services.analytics_service import analytics_service
from app.services.intelligence_service import intelligence_service

logger = logging.getLogger(__name__)


class BusinessAssistant:
    """
    AI Business Assistant that answers business questions.
    """
    
    def __init__(self):
        """Initialize the business assistant."""
        pass
    
    async def process_question(
        self,
        user_id: str,
        question: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user question.
        
        Args:
            user_id: User ID
            question: User question
            conversation_id: Optional conversation ID
            
        Returns:
            Dict[str, Any]: Assistant response
        """
        try:
            # Create or get conversation
            if not conversation_id:
                conversation_id = f"conv_{uuid.uuid4().hex[:12]}"
                await conversation_memory.create_conversation(user_id, conversation_id)
            
            # Save user message
            await conversation_memory.add_message(
                conversation_id=conversation_id,
                role="user",
                content=question
            )
            
            # Get conversation context
            history = await conversation_memory.get_history(conversation_id, limit=5)
            
            # Route the query
            result, query_type, metadata = await query_router.route_query(question)
            
            # Extract answer and confidence
            answer = result.get('answer', 'I could not find an answer to your question.')
            confidence = result.get('confidence', 50)
            
            # Generate recommendations if applicable
            recommendations = await self._generate_recommendations(query_type, result)
            
            # Determine data sources
            sources = self._determine_sources(query_type)
            
            # Save assistant response
            response_data = {
                "answer": answer,
                "confidence": confidence,
                "reasoning": result.get('reasoning', 'Analysis based on business data'),
                "recommendations": recommendations,
                "sources": sources,
                "conversation_id": conversation_id,
                "query_type": query_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await conversation_memory.add_message(
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
                metadata={"confidence": confidence, "query_type": query_type}
            )
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {
                "answer": f"I encountered an error processing your question: {str(e)}",
                "confidence": 0,
                "reasoning": "Error occurred during processing",
                "recommendations": [],
                "sources": [],
                "conversation_id": conversation_id,
                "query_type": "error",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _generate_recommendations(self, query_type: str, result: Dict) -> List[str]:
        """Generate recommendations based on query type and result."""
        recommendations = []
        
        try:
            if query_type in ["sales", "analytics"]:
                from app.services.recommendation_service import recommendation_service
                optimizations = await recommendation_service.get_optimization_suggestions()
                recommendations = [opt.get('message') for opt in optimizations[:3]]
            
            elif query_type == "inventory":
                from app.services.recommendation_service import recommendation_service
                restock = await recommendation_service.get_restock_recommendations()
                high_priority = [r for r in restock if r.get('priority') == 'high']
                recommendations = [f"Restock {r.get('product_name')} - {r.get('reason')}" for r in high_priority[:2]]
            
            elif query_type == "forecasting":
                recommendations = [
                    "Monitor forecasted trends closely",
                    "Adjust inventory based on forecast",
                    "Review pricing strategy if forecast shows decline"
                ]
            
            elif query_type == "risk":
                recommendations = [
                    "Review risk factors identified",
                    "Implement risk mitigation strategies",
                    "Monitor high-risk areas daily"
                ]
        except Exception as e:
            logger.warning(f"Could not generate recommendations: {str(e)}")
        
        return recommendations
    
    def _determine_sources(self, query_type: str) -> List[str]:
        """Determine data sources used for the response."""
        sources = ["business_data"]
        
        if query_type in ["sales", "analytics", "health"]:
            sources.append("analytics_engine")
        
        if query_type == "forecasting":
            sources.append("forecasting_engine")
        
        if query_type in ["inventory", "recommendation"]:
            sources.append("recommendation_engine")
        
        if query_type in ["risk", "analytics"]:
            sources.append("intelligence_engine")
        
        return sources


# Create singleton instance
business_assistant = BusinessAssistant()