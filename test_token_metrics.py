from src.memory.chroma.queries.storage import MemoryManager
import time
from datetime import datetime
import json

def test_token_metrics():
    memory = MemoryManager()
    
    print("\n=== Testing Token Metrics and Social Impact ===\n")
    
    # Test token performance tracking
    print("1. Testing Token Performance Analysis...")
    
    # Store some test metrics
    test_prices = [
        {"price": 1.20, "volume": 900000, "change_24h": 3.0},
        {"price": 1.25, "volume": 1200000, "change_24h": 4.2},
        {"price": 1.23, "volume": 1100000, "change_24h": 3.8},
        {"price": 1.30, "volume": 1500000, "change_24h": 5.7}
    ]
    
    for metrics in test_prices:
        memory.track_token_metrics("JEFF", metrics)
        time.sleep(0.1)
    
    # Analyze performance
    performance = memory.analyze_token_performance("JEFF")
    print("\nToken Performance Analysis:")
    print(json.dumps(performance, indent=2))
    
    # Test social metrics
    print("\n2. Testing Social Metrics...")
    
    # Store some test social impacts
    social_events = [
        {
            "type": "viral_tweet",
            "sentiment": "positive",
            "engagement": 15000,
            "price_impact": 0.08
        },
        {
            "type": "influencer_mention",
            "sentiment": "positive",
            "engagement": 25000,
            "price_impact": 0.12
        },
        {
            "type": "community_discussion",
            "sentiment": "neutral",
            "engagement": 5000,
            "price_impact": 0.02
        }
    ]
    
    for event in social_events:
        memory.track_social_impact("JEFF", event)
        time.sleep(0.1)
    
    # Get social metrics
    social_metrics = memory.track_social_metrics("JEFF")
    print("\nSocial Metrics Analysis:")
    print(json.dumps(social_metrics, indent=2))
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_token_metrics() 