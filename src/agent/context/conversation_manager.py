from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}
        
    def add_message(self, user_id: str, message: str, role: str = "user"):
        """Add message to conversation history"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
            
        self.conversations[user_id].append({
            "role": role,
            "content": message,
            "timestamp": datetime.now()
        })
        
        # Keep only last 10 messages
        self.conversations[user_id] = self.conversations[user_id][-10:]
        
    def get_context(self, user_id: str, limit: int = 5) -> str:
        """Get recent conversation context"""
        if user_id not in self.conversations:
            return ""
            
        messages = self.conversations[user_id][-limit:]
        return "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in messages
        ])
        
    def get_last_message(self, user_id: str) -> Optional[str]:
        """Get last message from conversation"""
        if user_id not in self.conversations:
            return None
            
        messages = self.conversations[user_id]
        return messages[-1]["content"] if messages else None 