class PhoneAnalyzer:
    """Analyze phone numbers for suspicious patterns."""
    
    def analyze(self, phone_number: str) -> dict:
        """
        Analyze a phone number for suspicious patterns.
        
        Args:
            phone_number: The phone number to analyze
            
        Returns:
            Dictionary with repeated_pattern, sequential_pattern, invalid_length flags
        """
        # If no phone number provided, return all False
        if not phone_number:
            return {
                "repeated_pattern": False,
                "sequential_pattern": False,
                "invalid_length": False
            }
        
        # Clean the phone number (remove spaces, dashes, parentheses)
        clean_number = phone_number.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        
        # Remove any non-digit characters
        clean_number = ''.join(char for char in clean_number if char.isdigit())
        
        # Check for invalid length (less than 8 digits)
        invalid_length = len(clean_number) < 8
        
        # Check for repeated digits (same digit repeated 4+ times in a row)
        repeated_pattern = False
        if len(clean_number) >= 4:
            for i in range(len(clean_number) - 3):
                if clean_number[i] == clean_number[i+1] == clean_number[i+2] == clean_number[i+3]:
                    repeated_pattern = True
                    break
        
        # Check for sequential digits (4+ consecutive ascending or descending digits)
        sequential_pattern = False
        if len(clean_number) >= 4:
            for i in range(len(clean_number) - 3):
                # Check ascending sequence (e.g., 1234)
                if (int(clean_number[i+1]) == int(clean_number[i]) + 1 and
                    int(clean_number[i+2]) == int(clean_number[i]) + 2 and
                    int(clean_number[i+3]) == int(clean_number[i]) + 3):
                    sequential_pattern = True
                    break
                # Check descending sequence (e.g., 4321)
                if (int(clean_number[i+1]) == int(clean_number[i]) - 1 and
                    int(clean_number[i+2]) == int(clean_number[i]) - 2 and
                    int(clean_number[i+3]) == int(clean_number[i]) - 3):
                    sequential_pattern = True
                    break
        
        return {
            "repeated_pattern": repeated_pattern,
            "sequential_pattern": sequential_pattern,
            "invalid_length": invalid_length
        }
