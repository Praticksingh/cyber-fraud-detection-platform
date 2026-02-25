import time
from collections import defaultdict


class RateLimiter:
    """Track request rates per phone number."""
    
    def __init__(self):
        # Dictionary to store request timestamps per phone number
        self.request_history = defaultdict(list)
        # Time window in seconds (e.g., 60 seconds)
        self.time_window = 60
        # Maximum requests allowed in time window
        self.max_requests = 5
    
    def check(self, phone_number: str) -> dict:
        """
        Check if phone number has exceeded rate limit.
        
        Args:
            phone_number: The phone number to check
            
        Returns:
            Dictionary with risk_boost and reason
        """
        if not phone_number:
            return {"risk_boost": 0, "reason": ""}
        
        current_time = time.time()
        
        # Clean phone number
        clean_phone = phone_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        clean_phone = ''.join(char for char in clean_phone if char.isdigit())
        
        # Get request history for this phone number
        timestamps = self.request_history[clean_phone]
        
        # Remove old timestamps outside the time window
        timestamps[:] = [ts for ts in timestamps if current_time - ts < self.time_window]
        
        # Add current request timestamp
        timestamps.append(current_time)
        
        # Check if rate limit exceeded
        if len(timestamps) > self.max_requests:
            return {"risk_boost": 20, "reason": f"Rate limit exceeded ({len(timestamps)} requests in {self.time_window}s)"}
        
        return {"risk_boost": 0, "reason": ""}
