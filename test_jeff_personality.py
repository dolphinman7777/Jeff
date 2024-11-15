from src.agent.llm.ollama.client import OllamaAgent
from src.memory.chroma.queries.storage import MemoryManager
import time
import json

def print_section(title):
    print(f"\n{'='*20} {title} {'='*20}\n")

def test_jeff_personality():
    jeff = OllamaAgent()
    memory = MemoryManager()
    
    print_section("1. Testing Basic Conversation")
    
    basic_convo = [
        "hey there",
        "what do you know about crypto?",
        "that's interesting, tell me more",
        "what makes you different from other AIs?",
        "why should I trust your analysis?"
    ]
    
    for msg in basic_convo:
        print(f"\nUser: {msg}")
        # Store interaction
        embedding = jeff.generate_embedding(msg)
        memory.store_interaction("test_user", msg, embedding)
        # Get context
        context = memory.retrieve_context("test_user")
        # Get response
        response = jeff.generate_response(msg, context)
        print(f"JEFF: {response}\n")
        time.sleep(1)  # Give time to read responses

    print_section("2. Testing Technical Knowledge")
    
    tech_questions = [
        "explain blockchain like I'm 5",
        "what's your take on Layer 2 solutions?",
        "how does tokenomics work?",
        "what's the difference between CEX and DEX?"
    ]
    
    for question in tech_questions:
        print(f"\nUser: {question}")
        embedding = jeff.generate_embedding(question)
        memory.store_interaction("test_user", question, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(question, context)
        print(f"JEFF: {response}\n")
        time.sleep(1)

    print_section("3. Testing Personality Adaptation")
    
    scenarios = [
        "you're not very smart",
        "wow, that's actually really insightful",
        "can you help me understand defi?",
        "what's your opinion on the market?",
        "are you just another chatbot?"
    ]
    
    for scenario in scenarios:
        print(f"\nUser: {scenario}")
        embedding = jeff.generate_embedding(scenario)
        memory.store_interaction("test_user", scenario, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(scenario, context)
        print(f"JEFF: {response}\n")
        time.sleep(1)

    print_section("4. Testing Memory and Context")
    
    memory_test = [
        "let's talk about ethereum",
        "what are its main advantages?",
        "how does that compare to solana?",
        "which one would you recommend?",
        "why did you mention that earlier?"
    ]
    
    for msg in memory_test:
        print(f"\nUser: {msg}")
        embedding = jeff.generate_embedding(msg)
        memory.store_interaction("test_user", msg, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(msg, context)
        print(f"JEFF: {response}")
        print(f"Context Length: {len(context.split())}")
        time.sleep(1)

    print_section("5. Testing Short Responses")
    
    short_prompts = [
        "thoughts?",
        "based",
        "cap",
        "fud",
        "ngmi"
    ]
    
    for prompt in short_prompts:
        print(f"\nUser: {prompt}")
        embedding = jeff.generate_embedding(prompt)
        memory.store_interaction("test_user", prompt, embedding)
        context = memory.retrieve_context("test_user")
        response = jeff.generate_response(prompt, context)
        print(f"JEFF: {response}\n")
        time.sleep(0.5)

    print_section("Test Complete")

if __name__ == "__main__":
    test_jeff_personality() 