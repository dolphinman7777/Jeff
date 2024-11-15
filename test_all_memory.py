from src.memory.chroma.queries.storage import MemoryManager
from src.agent.llm.ollama.client import OllamaAgent
import time
from datetime import datetime
import json

def print_section(title):
    print(f"\n{'='*20} {title} {'='*20}\n")

def test_all_memory():
    memory = MemoryManager()
    ollama = OllamaAgent()

    print_section("1. Testing Direct Chat Memory")
    
    # Simulate a direct chat conversation
    chat_messages = [
        "Hi! I'm new here and interested in AI.",
        "Can you tell me about machine learning?",
        "That's interesting! How does Python fit into this?",
        "Thanks for the great explanation!"
    ]
    
    for msg in chat_messages:
        print(f"\nUser: {msg}")
        embedding = ollama.generate_embedding(msg)
        memory.store_interaction("direct_user", msg, embedding)
        context = memory.retrieve_context("direct_user")
        print(f"Context: {context}")
    
    print_section("2. Testing Twitter Memory")
    
    # Simulate Twitter conversation
    tweets = [
        {
            "user_id": "tech_user",
            "message": "Just started learning about #AI and #MachineLearning! 🚀",
            "metadata": {
                "is_mention": False,
                "conversation_id": "tech_thread",
                "hashtags": ["#AI", "#MachineLearning"],
                "engagement_score": 10
            }
        },
        {
            "user_id": "ai_expert",
            "message": "@tech_user Great choice! I love working with neural networks! #DeepLearning",
            "metadata": {
                "is_reply": True,
                "is_mention": True,
                "conversation_id": "tech_thread",
                "hashtags": ["#DeepLearning"],
                "engagement_score": 8
            }
        }
    ]
    
    for tweet in tweets:
        print(f"\nProcessing tweet: {tweet['message']}")
        embedding = ollama.generate_embedding(tweet['message'])
        memory.store_interaction(tweet['user_id'], tweet['message'], embedding, tweet['metadata'])
        
        # Test Twitter-specific context
        context = memory.retrieve_twitter_context(tweet['user_id'], tweet['metadata']['conversation_id'])
        print(f"Twitter Context: {context}")
    
    print_section("3. Testing Analytics")
    
    # Test user behavior analysis
    behavior = memory.analyze_user_behavior("tech_user")
    print("\nUser Behavior Analysis:")
    print(json.dumps(behavior, indent=2))
    
    # Test sentiment analysis
    sentiment = memory.track_sentiment("tech_user")
    print("\nSentiment Analysis:")
    print(json.dumps(sentiment, indent=2))
    
    # Test hashtag analysis
    hashtags = memory.track_hashtag_usage("tech_user")
    print("\nHashtag Analysis:")
    print(json.dumps(hashtags, indent=2))
    
    print_section("4. Testing Memory Integration")
    
    # Test combined context retrieval
    print("\nTesting context retrieval for all users:")
    for user_id in ["direct_user", "tech_user", "ai_expert"]:
        context = memory.retrieve_context(user_id)
        print(f"\nContext for {user_id}:")
        print(context)
    
    print_section("Test Complete")

if __name__ == "__main__":
    test_all_memory() 