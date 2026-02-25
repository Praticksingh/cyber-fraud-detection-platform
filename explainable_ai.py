class ExplainableAI:
    """Generate human-readable explanations for fraud detection results."""
    
    def generate_explanation(self, score: int, detection_results: dict, phone_analysis: dict = None) -> dict:
        """
        Generate a clear explanation of the fraud detection results.
        
        Args:
            score: Risk score (0-100)
            detection_results: Dictionary with urgency_matches, financial_matches, threat_matches
            phone_analysis: Optional dictionary with phone pattern analysis results
            
        Returns:
            Dictionary with risk_level, primary_reason, contributing_factors, recommendation, threat_category
        """
        # Determine risk level using professional classification bands
        if score <= 30:
            risk_level = "Low"
        elif score <= 60:
            risk_level = "Medium"
        elif score <= 85:
            risk_level = "High"
        else:
            risk_level = "Critical"
        
        # Get matched keywords from results
        urgency_matches = detection_results.get("urgency_matches", [])
        financial_matches = detection_results.get("financial_matches", [])
        threat_matches = detection_results.get("threat_matches", [])
        
        # Determine threat category
        has_phone_issues = False
        if phone_analysis:
            has_phone_issues = (phone_analysis.get("repeated_pattern") or 
                              phone_analysis.get("sequential_pattern") or 
                              phone_analysis.get("invalid_length"))
        
        if financial_matches and urgency_matches:
            threat_category = "Financial Scam"
        elif threat_matches and urgency_matches:
            threat_category = "Extortion Scam"
        elif has_phone_issues and not (urgency_matches or financial_matches or threat_matches):
            threat_category = "Suspicious Sender"
        elif score <= 30:
            threat_category = "Low Risk Communication"
        else:
            threat_category = "Potential Fraud"
        
        # Determine primary reason
        if not urgency_matches and not financial_matches and not threat_matches:
            primary_reason = "No fraud indicators detected"
        elif threat_matches:
            primary_reason = f"Contains threatening language: {', '.join(threat_matches)}"
        elif financial_matches and urgency_matches:
            primary_reason = "Combines financial requests with urgency tactics"
        elif financial_matches:
            primary_reason = f"Requests financial information: {', '.join(financial_matches)}"
        elif urgency_matches:
            primary_reason = f"Uses urgency pressure: {', '.join(urgency_matches)}"
        else:
            primary_reason = "Multiple fraud indicators detected"
        
        # Build contributing factors list
        contributing_factors = []
        if urgency_matches:
            contributing_factors.append(f"Urgency keywords: {', '.join(urgency_matches)}")
        if financial_matches:
            contributing_factors.append(f"Financial keywords: {', '.join(financial_matches)}")
        if threat_matches:
            contributing_factors.append(f"Threat keywords: {', '.join(threat_matches)}")
        
        # Generate recommendation
        if risk_level == "Low":
            recommendation = "Message appears safe, but stay vigilant"
        elif risk_level == "Medium":
            recommendation = "Exercise caution. Verify sender identity before responding"
        elif risk_level == "High":
            recommendation = "High risk of fraud. Do not respond or click any links. Report and delete"
        else:  # Critical
            recommendation = "CRITICAL THREAT. Do not engage. Block sender immediately and report to authorities"
        
        return {
            "risk_level": risk_level,
            "primary_reason": primary_reason,
            "contributing_factors": contributing_factors,
            "recommendation": recommendation,
            "threat_category": threat_category
        }
