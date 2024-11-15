from src.memory.chroma.queries.storage import MemoryManager
import time
from datetime import datetime
import json

def test_token_social_features():
    memory = MemoryManager()
    
    print("\n=== Testing Token Social Features ===\n")
    
    # Test alert system
    print("1. Creating Token Alerts...")
    alerts = [
        ("JEFF", "price", 1.30),  # Price above $1.30
        ("JEFF", "volume", 2000000)  # Volume above 2M
    ]
    
    for symbol, alert_type, threshold in alerts:
        success = memory.create_token_alert(symbol, alert_type, threshold)
        print(f"Created {alert_type} alert for {symbol}: {'Success' if success else 'Failed'}")
    
    # Test alert checking
    print("\n2. Checking Alerts...")
    triggered = memory.check_token_alerts("JEFF", 1.35, 2500000)
    print(f"Triggered alerts: {json.dumps(triggered, indent=2)}")
    
    # Test social impact
    print("\n3. Tracking Social Impact...")
    social_events = [
        {
            "platform": "twitter",
            "type": "viral_tweet",
            "sentiment": "positive",
            "engagement": 5000,
            "price_impact": 0.05
        },
        {
            "platform": "twitter",
            "type": "influencer_mention",
            "sentiment": "neutral",
            "engagement": 10000,
            "price_impact": 0.02
        }
    ]
    
    for event in social_events:
        impact = memory.track_social_impact("JEFF", event)
        print(f"\nTracked impact: {json.dumps(impact, indent=2)}")
    
    # Test correlation analysis
    print("\n4. Analyzing Social Correlation...")
    correlation = memory.analyze_social_correlation("JEFF", timeframe_hours=1)
    print(f"Correlation results: {json.dumps(correlation, indent=2)}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_token_social_features() 