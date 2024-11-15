from src.agent.llm.ollama.client import OllamaAgent
from src.memory.chroma.queries.storage import MemoryManager
import time
import json

def print_section(title):
    print(f"\n{'='*20} {title} {'='*20}\n")

def test_jeff_conversation():
    jeff = OllamaAgent()
    memory = MemoryManager()
    
    print_section("1. Testing Basic Conversation Flow")
    
    # Test natural conversation progression
    conversation = [
        "hey jeff, what's happening in the markets?",
        "interesting, tell me more about those levels",
        "what makes you so sure?",
        "okay, what would you do in this situation?",
        "why do you think that's the best move?"
    ]
    
    for msg in conversation:
        print(f"\nUser: {msg}")
        embedding = jeff.generate_embedding(msg)
        memory.store_interaction("test_user", msg, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(msg, context)
        print(f"JEFF: {response}")
        print(f"Context State: {jeff.conversation_state}")
        time.sleep(1)

    print_section("2. Testing Topic Awareness")
    
    # Test how JEFF maintains topic focus
    topic_test = [
        "what do you think about Bitcoin's price action?",
        "how does that affect altcoins?",
        "what about the overall market sentiment?",
        "interesting, any specific tokens you're watching?",
        "why those specifically?"
    ]
    
    for msg in topic_test:
        print(f"\nUser: {msg}")
        embedding = jeff.generate_embedding(msg)
        memory.store_interaction("test_user", msg, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(msg, context)
        print(f"JEFF: {response}")
        print(f"Current Topic: {jeff.conversation_state['current_topic']}")
        time.sleep(1)

    print_section("3. Testing Follow-up Understanding")
    
    # Test JEFF's ability to handle follow-up questions
    followups = [
        "what's your take on DeFi?",
        "why do you say that?",
        "can you explain that more simply?",
        "what do you mean by that?",
        "how does that work exactly?"
    ]
    
    for msg in followups:
        print(f"\nUser: {msg}")
        embedding = jeff.generate_embedding(msg)
        memory.store_interaction("test_user", msg, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(msg, context)
        print(f"JEFF: {response}")
        print(f"Last Response: {jeff.conversation_state['last_response']}")
        time.sleep(1)

    print_section("4. Testing Engagement Levels")
    
    # Test different types of engagement
    engagement_test = [
        "gm",
        "what's your analysis on market trends?",
        "that's interesting",
        "why though?",
        "makes sense"
    ]
    
    for msg in engagement_test:
        print(f"\nUser: {msg}")
        embedding = jeff.generate_embedding(msg)
        memory.store_interaction("test_user", msg, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(msg, context)
        print(f"JEFF: {response}")
        print(f"Interaction Count: {jeff.conversation_state['interaction_count']}")
        time.sleep(1)

    print_section("5. Testing Memory Retention")
    
    # Test how well JEFF remembers previous context
    memory_test = [
        "remember what we discussed about Bitcoin?",
        "what was your view on DeFi again?",
        "what levels were you watching?",
        "and what about those tokens you mentioned?",
        "what was your main concern about the market?"
    ]
    
    for msg in memory_test:
        print(f"\nUser: {msg}")
        embedding = jeff.generate_embedding(msg)
        memory.store_interaction("test_user", msg, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(msg, context)
        print(f"JEFF: {response}")
        print(f"Topic Depth: {jeff.conversation_state['topic_depth']}")
        time.sleep(1)

    print_section("Test Complete")

if __name__ == "__main__":
    test_jeff_conversation() 