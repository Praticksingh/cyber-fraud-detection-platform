class BlacklistChecker:
    """Check phone numbers and messages against blacklist."""
    
    def __init__(self):
        # In-memory blacklist of known scam phone numbers
        self.blacklisted_phones = [
            "0000000000",
            "1111111111",
            "9999999999",
            "1234567890"
        ]
        
        # In-memory blacklist of high-risk keywords
        self.blacklisted_keywords = [
            "nigerian prince",
            "wire transfer",
            "western union",
            "bitcoin wallet",
            "send gift card"
        ]
    
    def check(self, phone_number: str, message: str) -> dict:
        """
        Check if phone number or message contains blacklisted items.
        
        Args:
            phone_number: The phone number to check
            message: The message content to check
            
        Returns:
            Dictionary with risk_boost and reason
        """
        # Clean phone number
        if phone_number:
            clean_phone = phone_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
            clean_phone = ''.join(char for char in clean_phone if char.isdigit())
            
            if clean_phone in self.blacklisted_phones:
                return {"risk_boost": 25, "reason": "Phone number is blacklisted"}
        
        # Check message for blacklisted keywords
        if message:
            message_lower = message.lower()
            for keyword in self.blacklisted_keywords:
                if keyword in message_lower:
                    return {"risk_boost": 25, "reason": f"Blacklisted keyword detected: {keyword}"}
        
        return {"risk_boost": 0, "reason": ""}
