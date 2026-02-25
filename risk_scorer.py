class RiskScorer:
    """Calculate risk scores based on detection results."""
    
    def __init__(self):
        # Define point values for each category
        self.urgency_points = 15
        self.financial_points = 20
        self.threat_points = 25
    
    def calculate_score(self, detection_results: dict, phone_analysis: dict = None) -> dict:
        """
        Calculate risk score and confidence based on detected keywords and phone analysis.
        
        Args:
            detection_results: Dictionary with urgency_matches, financial_matches, threat_matches
            phone_analysis: Optional dictionary with phone pattern analysis results
            
        Returns:
            Dictionary with score (0-100), risk_level (Low/Medium/High/Critical), and confidence (%)
        """
        score = 0
        
        # Add points for urgency keywords
        urgency_count = len(detection_results.get("urgency_matches", []))
        score += urgency_count * self.urgency_points
        
        # Add points for financial keywords
        financial_count = len(detection_results.get("financial_matches", []))
        score += financial_count * self.financial_points
        
        # Add points for threat keywords
        threat_count = len(detection_results.get("threat_matches", []))
        score += threat_count * self.threat_points
        
        # Add points for suspicious phone patterns
        if phone_analysis:
            if phone_analysis.get("repeated_pattern"):
                score += 10
            if phone_analysis.get("sequential_pattern"):
                score += 10
            if phone_analysis.get("invalid_length"):
                score += 15
        
        # Cap score at 100
        if score > 100:
            score = 100
        
        # Determine risk level based on professional classification bands
        if score <= 30:
            risk_level = "Low"
        elif score <= 60:
            risk_level = "Medium"
        elif score <= 85:
            risk_level = "High"
        else:
            risk_level = "Critical"
        
        # Calculate confidence based on number of categories matched
        categories_matched = 0
        if urgency_count > 0:
            categories_matched += 1
        if financial_count > 0:
            categories_matched += 1
        if threat_count > 0:
            categories_matched += 1
        
        if categories_matched >= 3:
            confidence = 85
        elif categories_matched == 2:
            confidence = 65
        elif categories_matched == 1:
            confidence = 45
        else:
            confidence = 10
        
        return {
            "score": score,
            "risk_level": risk_level,
            "confidence": confidence
        }
