class ScamDetectionEngine:
    """Simple scam detection engine that analyzes messages for fraud indicators."""
    
    def __init__(self):
        # Define keyword categories
        self.urgency_keywords = ["urgent", "immediately", "now", "act fast"]
        self.financial_keywords = ["bank", "account", "verify", "credit", "debit"]
        self.threat_keywords = ["suspended", "blocked", "penalty", "legal action"]
    
    def analyze(self, message: str) -> dict:
        """
        Analyze a message for scam indicators.
        
        Args:
            message: The message text to analyze
            
        Returns:
            Dictionary with matched keywords by category
        """
        # Convert message to lowercase for case-insensitive matching
        message_lower = message.lower()
        
        # Find matching keywords in each category
        urgency_matches = []
        for keyword in self.urgency_keywords:
            if keyword in message_lower:
                urgency_matches.append(keyword)
        
        financial_matches = []
        for keyword in self.financial_keywords:
            if keyword in message_lower:
                financial_matches.append(keyword)
        
        threat_matches = []
        for keyword in self.threat_keywords:
            if keyword in message_lower:
                threat_matches.append(keyword)
        
        # Return results
        return {
            "urgency_matches": urgency_matches,
            "financial_matches": financial_matches,
            "threat_matches": threat_matches
        }
