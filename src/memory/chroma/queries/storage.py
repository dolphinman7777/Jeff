import chromadb
import logging
from typing import List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        try:
            self.client = chromadb.Client()
            # Get or create collection for storing chat history
            self.collection = self.client.get_or_create_collection(
                name="chat_history",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("MemoryManager initialized with ChromaDB")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            raise

    def store_interaction(self, user_id: str, message: str, embedding: List[float]):
        """Store a chat interaction in ChromaDB"""
        try:
            # Generate unique ID for the interaction
            interaction_id = f"interaction_{datetime.now().timestamp()}"
            
            # Store the interaction
            self.collection.add(
                embeddings=[embedding],
                documents=[message],
                metadatas=[{
                    "user_id": str(user_id),
                    "timestamp": datetime.now().isoformat(),
                    "type": "chat"
                }],
                ids=[interaction_id]
            )
            logger.info(f"Stored Twitter interaction for user {user_id}")
        except Exception as e:
            logger.error(f"Error storing interaction: {e}")

    def retrieve_context(self, user_id: str, limit: int = 5) -> str:
        """Retrieve recent context for a user"""
        try:
            # Get recent interactions
            results = self.collection.query(
                query_texts=[f"user:{user_id}"],
                n_results=limit,
                where={"user_id": str(user_id)}
            )
            
            if not results or not results['documents']:
                return ""
                
            # Format as conversation history
            conversation = []
            for doc in results['documents'][0]:
                conversation.append(doc)
                
            # Return most recent context first
            return "\n".join(reversed(conversation[-3:]))
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return ""
