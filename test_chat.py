from src.agent.llm.ollama.client import OllamaAgent
from src.memory.chroma.queries.storage import MemoryManager
from src.agent.personality.engine import PersonalityEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_chat_system():
    print("\n=== Starting Chat System Test ===\n")
    
    # Initialize components
    print("1. Initializing Components...")
    ollama = OllamaAgent(model="mistral")
    memory = MemoryManager()
    personality = PersonalityEngine("default")
    print("✓ Components initialized\n")
    
    # Test natural conversation flow
    conversation = [
        ("Hi there! I'm interested in learning about AI and coding.", 
         "Test greeting and topic introduction"),
        
        ("Can you explain in simple terms what machine learning is?",
         "Test technical explanation"),
        
        ("That makes sense. What programming language should I start with?",
         "Test follow-up question with context"),
        
        ("I heard Python is good for AI. Is that true?",
         "Test domain-specific question"),
        
        ("Could you show me a simple Python example for machine learning?",
         "Test code example request"),
        
        ("Thanks! One last question - how does this relate to neural networks?",
         "Test conceptual connection"),
    ]
    
    print("2. Starting Conversation Test\n")
    
    for i, (message, test_desc) in enumerate(conversation, 1):
        print(f"\n--- Test {i}: {test_desc} ---")
        print(f"\033[34mUser: {message}\033[0m")  # Blue for user
        
        # Process message
        embedding = ollama.generate_embedding(message)
        memory.store_interaction("test_user", message, embedding)
        context = memory.retrieve_context("test_user")
        llm_response = ollama.generate_response(message, context)
        final_response = personality.generate_response(llm_response, {
            "user_id": "test_user",
            "context": context,
            "original_message": message
        })
        
        print(f"\033[32mAI: {final_response}\033[0m")  # Green for AI
        
        # Show context length for debugging
        print(f"\033[90mContext tokens: {len(context.split())}\033[0m")  # Gray for debug
        print()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_chat_system() 