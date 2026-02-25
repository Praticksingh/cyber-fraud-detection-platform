from collections import defaultdict
from typing import List, Dict


class HistoryStore:
    """Store fraud analysis history in memory."""
    
    def __init__(self):
        # Dictionary to store analysis history per phone number
        self.history = defaultdict(list)
    
    def add(self, phone_number: str, analysis_result: Dict):
        """
        Add an analysis result to history.
        
        Args:
            phone_number: The phone number
            analysis_result: Dictionary with risk_score, risk_level, timestamp, etc.
        """
        if not phone_number:
            return
        
        # Clean phone number
        clean_phone = phone_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        clean_phone = ''.join(char for char in clean_phone if char.isdigit())
        
        # Add to history (keep last 10 entries per phone)
        self.history[clean_phone].append(analysis_result)
        if len(self.history[clean_phone]) > 10:
            self.history[clean_phone].pop(0)
    
    def check_previous_risk(self, phone_number: str) -> dict:
        """
        Check if phone number was previously flagged as high risk.
        
        Args:
            phone_number: The phone number to check
            
        Returns:
            Dictionary with risk_boost and reason
        """
        history = self.get_history(phone_number)
        
        if not history:
            return {"risk_boost": 0, "reason": ""}
        
        # Check if any previous analysis was High or Critical
        for entry in history:
            risk_level = entry.get("risk_level", "")
            if risk_level in ["High", "Critical"]:
                return {"risk_boost": 15, "reason": f"Previously flagged as {risk_level} risk"}
        
        return {"risk_boost": 0, "reason": ""}
    
    def get_history(self, phone_number: str) -> List[Dict]:
        """
        Get analysis history for a phone number.
        
        Args:
            phone_number: The phone number to look up
            
        Returns:
            List of previous analysis results
        """
        if not phone_number:
            return []
        
        # Clean phone number
        clean_phone = phone_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        clean_phone = ''.join(char for char in clean_phone if char.isdigit())
        
        return self.history.get(clean_phone, [])
