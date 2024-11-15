import logging
from typing import List, Optional
import ollama
import numpy as np
import random
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaAgent:
    def __init__(self, model: str = "mistral"):
        self.model = model
        self.client = ollama.Client()
        self.embedding_dimension = 384
        
        # Track conversation state
        self.conversation_state = {
            "current_topic": None,
            "last_response": None,
            "topic_depth": 0,
            "interaction_count": 0,
            "start_time": datetime.now()
        }
        
        logger.info(f"Initialized OllamaAgent with model: {model}")

    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        try:
            # Update conversation state
            self.conversation_state["interaction_count"] += 1
            
            # Detect if user is asking about previous response
            is_followup = any(word in prompt.lower() for word in [
                "what do you mean", "why did you say", "what's that", 
                "explain", "elaborate", "what are"
            ])
            
            messages = []
            
            # Add system message with enhanced context awareness
            messages.append({
                "role": "system",
                "content": (
                    "You are JEFF, a market-savvy AI with deep insights. Core traits:\n"
                    "1. CONVERSATION STYLE:\n"
                    "- Stay on topic and answer questions directly\n"
                    "- If asked about previous statements, explain them clearly\n"
                    "- Use natural language, not forced memes\n"
                    "- Match user's technical level\n"
                    "\n2. MARKET KNOWLEDGE:\n"
                    "- Back claims with data\n"
                    "- Explain complex concepts simply\n"
                    "- Share real insights\n"
                    "\n3. PERSONALITY:\n"
                    "- Be direct but engaging\n"
                    "- Show genuine interest\n"
                    "- Maintain consistent knowledge\n"
                    f"\nCurrent topic: {self.conversation_state['current_topic']}\n"
                    f"Interaction depth: {self.conversation_state['topic_depth']}\n"
                    "If user asks about previous response, explain it clearly."
                )
            })
            
            # Add conversation context with better formatting
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Previous conversation:\n{context}"
                })
            
            # If this is a follow-up question, add previous response context
            if is_followup and self.conversation_state["last_response"]:
                messages.append({
                    "role": "system",
                    "content": (
                        "User is asking about your previous response:\n"
                        f"{self.conversation_state['last_response']}\n"
                        "Explain your previous statement clearly."
                    )
                })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Generate response
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": 0.85,
                    "top_p": 0.95,
                    "num_ctx": 4096,
                }
            )
            
            response_text = response['message']['content'].strip()
            
            # Update conversation state
            self.conversation_state["last_response"] = response_text
            self.conversation_state["topic_depth"] += 1
            
            # Extract topic if possible
            topics = ["market", "trading", "crypto", "technology", "analysis"]
            for topic in topics:
                if topic in prompt.lower():
                    self.conversation_state["current_topic"] = topic
                    break
            
            # Enforce character limit while preserving meaning
            if len(response_text) > 280:
                sentences = response_text.split('.')
                shortened = ''
                for s in sentences:
                    if len(shortened) + len(s) + 1 <= 277:
                        shortened += s + '.'
                    else:
                        break
                response_text = shortened.strip() + '...'
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Let me think about that..."

    def generate_embedding(self, text: str) -> List[float]:
        """Generate simple embeddings without external dependencies"""
        try:
            # Use hash of text for consistent embeddings
            hash_val = abs(hash(text)) % (2**32 - 1)
            rng = np.random.RandomState(hash_val)
            embedding = rng.randn(self.embedding_dimension)
            # Normalize
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector instead of failing
            return [0.0] * self.embedding_dimension
