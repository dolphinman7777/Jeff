from src.memory.chroma.queries.storage import MemoryManager
from src.agent.llm.ollama.client import OllamaAgent
import time
from datetime import datetime
import json

def print_section(title):
    print(f"\n{'='*20} {title} {'='*20}\n")

def test_twitter_memory():
    print_section("Starting Twitter Memory System Test")
    
    memory = MemoryManager()
    ollama = OllamaAgent()
    
    # Test data
    conversation = [
        {
            "user_id": "alice123",
            "message": "Hey! Anyone here interested in AI and crypto? #AI #Crypto",
            "metadata": {
                "is_mention": False,
                "conversation_id": "thread1",
                "user_followers": 1000,
                "engagement_score": 5,
                "hashtags": ["#AI", "#Crypto"],
                "is_reply": False
            }
        },
        {
            "user_id": "bob456",
            "message": "@alice123 Yes! I love machine learning! It's amazing! #ML",
            "metadata": {
                "is_reply": True,
                "is_mention": True,
                "conversation_id": "thread1",
                "reply_to_tweet_id": "t1",
                "user_followers": 500,
                "engagement_score": 3,
                "hashtags": ["#ML"]
            }
        },
        {
            "user_id": "alice123",
            "message": "@bob456 That's great! What resources are you using? I hate outdated tutorials.",
            "metadata": {
                "is_reply": True,
                "is_mention": True,
                "conversation_id": "thread1",
                "reply_to_tweet_id": "t2",
                "user_followers": 1000,
                "engagement_score": 4,
                "hashtags": []
            }
        }
    ]
    
    print_section("1. Testing Tweet Storage and Context")
    
    # Store conversation
    for tweet in conversation:
        print(f"\nProcessing tweet from {tweet['user_id']}: {tweet['message']}")
        
        # Generate embedding
        embedding = ollama.generate_embedding(tweet['message'])
        
        # Store with metadata
        memory.store_interaction(
            tweet['user_id'],
            tweet['message'],
            embedding,
            tweet['metadata']
        )
        
        # Get Twitter context
        context = memory.retrieve_twitter_context(
            tweet['user_id'],
            tweet['metadata']['conversation_id']
        )
        print("\nCurrent context:")
        print(context)
        time.sleep(0.1)
    
    print_section("2. Testing User Behavior Analysis")
    
    # Get behavior analysis for Alice
    alice_behavior = memory.analyze_user_behavior("alice123")
    print("\nAlice's behavior analysis:")
    print(json.dumps(alice_behavior, indent=2))
    
    print_section("3. Testing Sentiment Analysis")
    
    # Get sentiment analysis for both users
    for user in ["alice123", "bob456"]:
        sentiment = memory.track_sentiment(user)
        print(f"\n{user}'s sentiment analysis:")
        print(json.dumps(sentiment, indent=2))
    
    print_section("4. Testing Hashtag Analysis")
    
    # Get hashtag analysis for both users
    for user in ["alice123", "bob456"]:
        hashtags = memory.track_hashtag_usage(user)
        print(f"\n{user}'s hashtag analysis:")
        print(json.dumps(hashtags, indent=2))
    
    print_section("5. Testing Conversation Thread")
    
    # Get full thread history
    thread = memory.track_conversation_thread("thread1")
    print("\nFull conversation thread:")
    for message in thread:
        print(f"\nTimestamp: {message['timestamp']}")
        print(f"User: {message['user_id']}")
        print(f"Message: {message['message']}")
        print(f"Engagement: {message['engagement_score']}")
        if message.get('hashtags'):
            print(f"Hashtags: {', '.join(message['hashtags'])}")
    
    print_section("6. Testing User Engagement Stats")
    
    # Get engagement stats for both users
    for user in ["alice123", "bob456"]:
        stats = memory.get_user_engagement_stats(user)
        print(f"\n{user}'s engagement stats:")
        print(json.dumps(stats, indent=2))
    
    print_section("Test Complete")

if __name__ == "__main__":
    test_twitter_memory() 