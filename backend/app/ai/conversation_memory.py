"""
Conversation memory for maintaining chat context.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.database.mongodb import mongodb
from app.models.conversation import Conversation, ConversationMessage

logger = logging.getLogger(__name__)


class ConversationMemory:
    """
    Manages conversation history and context.
    """
    
    def __init__(self):
        """Initialize the conversation memory."""
        self.collection_name = "conversations"
    
    async def get_collection(self):
        """Get the conversations collection from MongoDB."""
        return mongodb.get_collection(self.collection_name)
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Optional[Conversation]: Conversation data
        """
        try:
            collection = await self.get_collection()
            data = await collection.find_one({"conversation_id": conversation_id})
            
            if not data:
                return None
            
            # Convert to Conversation model
            return Conversation(**data)
            
        except Exception as e:
            logger.error(f"Error getting conversation: {str(e)}")
            return None
    
    async def create_conversation(self, user_id: str, conversation_id: str) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            user_id: User ID
            conversation_id: Conversation ID
            
        Returns:
            Conversation: Created conversation
        """
        try:
            collection = await self.get_collection()
            
            conversation = Conversation(
                user_id=user_id,
                conversation_id=conversation_id,
                messages=[],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            await collection.insert_one(conversation.model_dump(by_alias=True))
            
            return conversation
            
        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}")
            raise
    
    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: Conversation ID
            role: Message role (user/assistant)
            content: Message content
            metadata: Additional metadata
            
        Returns:
            bool: Success status
        """
        try:
            collection = await self.get_collection()
            
            message = ConversationMessage(
                role=role,
                content=content,
                timestamp=datetime.utcnow(),
                metadata=metadata or {}
            )
            
            result = await collection.update_one(
                {"conversation_id": conversation_id},
                {
                    "$push": {"messages": message.model_dump()},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            return False
    
    async def get_history(self, conversation_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get conversation history.
        
        Args:
            conversation_id: Conversation ID
            limit: Number of messages to return
            
        Returns:
            List[Dict[str, Any]]: Conversation history
        """
        try:
            collection = await self.get_collection()
            conversation = await collection.find_one({"conversation_id": conversation_id})
            
            if not conversation:
                return []
            
            messages = conversation.get('messages', [])
            return messages[-limit:] if limit > 0 else messages
            
        except Exception as e:
            logger.error(f"Error getting history: {str(e)}")
            return []
    
    async def clear_history(self, conversation_id: str) -> bool:
        """
        Clear conversation history.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            bool: Success status
        """
        try:
            collection = await self.get_collection()
            result = await collection.update_one(
                {"conversation_id": conversation_id},
                {"$set": {"messages": [], "updated_at": datetime.utcnow()}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error clearing history: {str(e)}")
            return False
    
    async def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            bool: Success status
        """
        try:
            collection = await self.get_collection()
            result = await collection.delete_one({"conversation_id": conversation_id})
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting conversation: {str(e)}")
            return False


# Create singleton instance
conversation_memory = ConversationMemory()