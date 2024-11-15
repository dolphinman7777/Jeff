import time
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class RateLimit:
    max_requests: int
    time_window: int  # in seconds
    
class RateLimiter:
    def __init__(self, limits: dict[str, RateLimit]):
        self.limits = limits
        self.requests = {key: [] for key in limits.keys()}
        
    def check_rate_limit(self, limit_type: str) -> bool:
        if limit_type not in self.limits:
            return True
            
        limit = self.limits[limit_type]
        current_time = datetime.now()
        window_start = current_time - timedelta(seconds=limit.time_window)
        
        # Clean up old requests
        self.requests[limit_type] = [
            req_time for req_time in self.requests[limit_type] 
            if req_time > window_start
        ]
        
        # Check if we're within limits
        if len(self.requests[limit_type]) >= limit.max_requests:
            logger.warning(f"Rate limit exceeded for {limit_type}")
            return False
            
        self.requests[limit_type].append(current_time)
        return True 