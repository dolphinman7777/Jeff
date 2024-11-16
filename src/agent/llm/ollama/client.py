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

    def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 100) -> str:
        """Generate response using Ollama"""
        try:
            response = self.client.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'num_predict': max_tokens,
                    # Ollama uses different temp scale (0-1)
                    'temperature': min(temperature, 1.0)
                }
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._generate_fallback_response()

    def _generate_fallback_response(self) -> str:
        """Fallback responses if generation fails"""
        fallbacks = [
            "bruh moment... can you say that again?",
            "my bad, glitched out for a sec",
            "hold up, let me reset real quick",
            "ngl something went wrong there",
            "error 404: brain not found. jk, try again?"
        ]
        return random.choice(fallbacks)

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
