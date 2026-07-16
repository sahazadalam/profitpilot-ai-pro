"""
Conversation model for chat history.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId


class ConversationMessage(BaseModel):
    """Message in a conversation."""
    role: str = Field(..., description="Role: user or assistant")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "user",
                "content": "Which product is performing best?",
                "timestamp": "2026-07-16T10:30:00"
            }
        }
    }


class Conversation(BaseModel):
    """Conversation model."""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str = Field(..., description="User ID")
    conversation_id: str = Field(..., description="Unique conversation ID")
    messages: List[ConversationMessage] = Field(default_factory=list, description="Conversation messages")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    summary: Optional[str] = Field(None, description="Conversation summary")
    
    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "conversation_id": "conv_123456",
                "messages": [],
                "summary": "User asked about product performance"
            }
        }
    }