from src.memory.chroma.queries.storage import MemoryManager
import json

def test_twitter_formats():
    memory = MemoryManager()
    
    print("\n=== Testing Twitter Format Templates ===\n")
    
    # Test price alert format
    print("1. Testing Price Alert Format")
    alert = {
        "type": "price_alert",
        "threshold": 1.500,
        "current_value": 1.525,
        "symbol": "JEFF"
    }
    price_alert_tweet = memory.format_token_alert_tweet(alert)
    print("\nPrice Alert Tweet:")
    print(price_alert_tweet)
    
    # Test volume alert format
    print("\n2. Testing Volume Alert Format")
    volume_alert = {
        "type": "volume_alert",
        "threshold": 2_000_000,
        "current_value": 2_500_000,
        "symbol": "JEFF"
    }
    volume_alert_tweet = memory.format_token_alert_tweet(volume_alert)
    print("\nVolume Alert Tweet:")
    print(volume_alert_tweet)
    
    # Test metrics update format
    print("\n3. Testing Metrics Update Format")
    metrics = {
        "current_price": 1.234,
        "price_change_24h": 5.67,
        "volume_24h": 1_500_000,
        "price_trend": "up"
    }
    metrics_tweet = memory.format_token_update_tweet(metrics)
    print("\nMetrics Update Tweet:")
    print(metrics_tweet)
    
    # Test social impact format
    print("\n4. Testing Social Impact Format")
    social_metrics = {
        "total_mentions": 1234,
        "total_engagement": 50000,
        "sentiment_score": 0.8,
        "viral_tweets": 5
    }
    social_tweet = memory.format_social_impact_report(social_metrics)
    print("\nSocial Impact Tweet:")
    print(social_tweet)
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_twitter_formats() 