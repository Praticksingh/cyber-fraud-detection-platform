class IPAnalyzer:
    """Analyze IP addresses for suspicious patterns."""
    
    def analyze(self, ip_address: str) -> dict:
        """
        Analyze an IP address and return risk score adjustment with reason.
        
        Args:
            ip_address: The IP address to analyze
            
        Returns:
            Dictionary with risk_adjustment and reason
        """
        if not ip_address:
            return {"risk_adjustment": 0, "reason": ""}
        
        risk_adjustment = 0
        reasons = []
        
        # Check for localhost
        if ip_address in ["127.0.0.1", "localhost", "::1"]:
            risk_adjustment += 15
            reasons.append("Localhost access detected")
        
        # Check for private IP ranges
        # 10.0.0.0 - 10.255.255.255
        if ip_address.startswith("10."):
            risk_adjustment += 10
            reasons.append("Private network IP (10.x.x.x)")
        
        # 172.16.0.0 - 172.31.255.255
        if ip_address.startswith("172."):
            parts = ip_address.split(".")
            if len(parts) >= 2 and parts[1].isdigit():
                second_octet = int(parts[1])
                if 16 <= second_octet <= 31:
                    risk_adjustment += 10
                    reasons.append("Private network IP (172.16-31.x.x)")
        
        # 192.168.0.0 - 192.168.255.255
        if ip_address.startswith("192.168."):
            risk_adjustment += 10
            reasons.append("Private network IP (192.168.x.x)")
        
        reason = "; ".join(reasons) if reasons else ""
        
        return {"risk_adjustment": risk_adjustment, "reason": reason}
