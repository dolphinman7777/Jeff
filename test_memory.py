from src.memory.chroma.queries.storage import MemoryManager
from src.agent.llm.ollama.client import OllamaAgent
import time

def test_memory_system():
    print("\n=== Testing Memory System ===\n")
    
    memory = MemoryManager()
    ollama = OllamaAgent()
    
    # Test conversation
    conversation = [
        "Hi, I'm Alice!",
        "What can you tell me about machine learning?",
        "That's interesting. How does it relate to neural networks?",
        "Can you give me a simple example?",
        "Thanks! Now, remember I'm Alice from earlier?",
    ]
    
    print("Testing conversation memory...\n")
    
    for message in conversation:
        print(f"\nUser message: {message}")
        
        # Store interaction
        embedding = ollama.generate_embedding(message)
        memory.store_interaction("test_user", message, embedding)
        
        # Get context
        context = memory.retrieve_context("test_user")
        print("\nCurrent context:")
        print(context)
        print("\n" + "-"*50)
        
        # Small delay to ensure timestamp ordering
        time.sleep(0.1)
    
    print("\n=== Memory Test Complete ===")

if __name__ == "__main__":
    test_memory_system() 