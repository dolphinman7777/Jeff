from src.memory.chroma.queries.storage import MemoryManager
import time
from datetime import datetime
import json

def print_section(title):
    print(f"\n{'='*20} {title} {'='*20}\n")

def test_realtime_features():
    memory = MemoryManager()
    
    print_section("1. Testing Token Metrics")
    
    # Simulate token price updates
    token_updates = [
        {"price": 1.23, "volume": 1000000, "change_24h": 5.2},
        {"price": 1.25, "volume": 1200000, "change_24h": 6.1},
        {"price": 1.22, "volume": 900000, "change_24h": 4.8}
    ]
    
    print("\nStoring token metrics...")
    for update in token_updates:
        metrics = memory.track_token_metrics("JEFF", update)
        print(f"\nStored metrics: {json.dumps(metrics, indent=2)}")
        time.sleep(0.1)
    
    # Get token history
    history = memory.get_token_history("JEFF")
    print(f"\nToken history retrieved: {len(history)} records")
    for record in history:
        print(f"\nTimestamp: {record['timestamp']}")
        print(f"Price: ${record['price']}")
        print(f"Volume: {record['volume']}")
        print(f"24h Change: {record['change_24h']}%")
    
    print_section("2. Testing Real-time Events")
    
    # Simulate various events
    events = [
        {
            "type": "price_alert",
            "data": {"symbol": "JEFF", "price": 1.25, "alert_type": "ath"},
            "importance": "high"
        },
        {
            "type": "volume_spike",
            "data": {"symbol": "JEFF", "volume": 1500000},
            "importance": "normal"
        },
        {
            "type": "social_mention",
            "data": {"platform": "twitter", "sentiment": "positive"},
            "importance": "low"
        }
    ]
    
    print("\nStoring events...")
    for event in events:
        success = memory.store_realtime_event(
            event['type'],
            event['data'],
            event['importance']
        )
        print(f"\nStored {event['type']}: {'Success' if success else 'Failed'}")
        time.sleep(0.1)
    
    # Monitor events
    monitoring = memory.monitor_realtime_events()
    print("\nReal-time monitoring results:")
    print(json.dumps(monitoring, indent=2))
    
    print_section("Test Complete")

if __name__ == "__main__":
    test_realtime_features() 