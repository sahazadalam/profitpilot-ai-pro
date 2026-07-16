"""
Chat schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Request schema for chat."""
    question: str = Field(..., min_length=1, max_length=1000, description="User question")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "Which product is performing best?",
                "conversation_id": "conv_123456"
            }
        }
    }


class ChatResponse(BaseModel):
    """Response schema for chat."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Chat response data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Business assistant response generated",
                "data": {
                    "answer": "The best performing product is MacBook Pro 2024 with $12,495 in revenue",
                    "confidence": 92,
                    "reasoning": "Based on sales data analysis...",
                    "recommendations": ["Increase stock for this product"],
                    "sources": ["sales", "analytics"],
                    "conversation_id": "conv_123456"
                }
            }
        }
    }


class QueryHistoryResponse(BaseModel):
    """Response schema for query history."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: List[Dict[str, Any]] = Field(..., description="Query history")


class AlertResponse(BaseModel):
    """Response schema for business alerts."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Alert data")


class ActionPlanResponse(BaseModel):
    """Response schema for action plan."""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(..., description="Action plan data")