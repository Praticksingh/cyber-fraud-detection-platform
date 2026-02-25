from datetime import datetime


class FraudLogger:
    """Log fraud analysis results to file."""
    
    def __init__(self, log_file: str = "fraud_logs.txt"):
        self.log_file = log_file
    
    def log(self, phone_number: str, risk_score: int, risk_level: str):
        """
        Log fraud analysis result to file.
        
        Args:
            phone_number: The phone number analyzed
            risk_score: The calculated risk score
            risk_level: The risk level (Low/Medium/High/Critical)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        phone = phone_number if phone_number else "N/A"
        
        log_entry = f"{timestamp} | Phone: {phone} | Score: {risk_score} | Level: {risk_level}\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            # Silently fail if logging fails (don't break the API)
            print(f"Logging error: {e}")
