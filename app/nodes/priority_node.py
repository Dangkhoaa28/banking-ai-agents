class PriorityNode:
    def __init__(self):
        # Keyword scoring system with word variations
        self.high_priority_keywords = {
            "fraud": 10,
            "unauthorized": 10,
            "stolen": 9,
            "stole": 9,
            "lost money": 8,
            "lost": 7,
            "blocked": 7,
            "urgent": 6,
            "emergency": 6,
            "immediately": 5,
            "critical": 5
        }
        
        self.medium_priority_keywords = {
            "transfer": 4,
            "refund": 4,
            "error": 3,
            "fail": 3,
            "failed": 3,
            "not working": 3,
            "problem": 2,
            "issue": 2,
            "concern": 1
        }
        
        self.low_priority_keywords = {
            "inquiry": 0,
            "question": 0,
            "general": 0
        }
    
    def detect_priority(self, message: str) -> str:
        """
        Determines the priority of the issue based on keyword scoring.
        Returns 'HIGH', 'MEDIUM', or 'LOW'.
        """
        msg_lower = message.lower()
        score = 0
        matched_keywords = []
        
        # Score high priority keywords
        for keyword, weight in self.high_priority_keywords.items():
            if keyword in msg_lower:
                score += weight
                matched_keywords.append((keyword, weight))
        
        if score >= 7:
            return "HIGH"
        
        # Score medium priority keywords
        for keyword, weight in self.medium_priority_keywords.items():
            if keyword in msg_lower:
                score += weight
                matched_keywords.append((keyword, weight))
        
        if score >= 5:
            return "MEDIUM"
        
        # Score low priority keywords
        for keyword, weight in self.low_priority_keywords.items():
            if keyword in msg_lower:
                score += weight
        
        return "LOW"
    
    def detect_priority_with_score(self, message: str) -> dict:
        """
        Returns priority with confidence score.
        """
        priority = self.detect_priority(message)
        msg_lower = message.lower()
        
        # Calculate confidence based on keyword matches
        total_score = 0
        matches = 0
        
        for keyword, weight in self.high_priority_keywords.items():
            if keyword in msg_lower:
                total_score += weight
                matches += 1
        
        for keyword, weight in self.medium_priority_keywords.items():
            if keyword in msg_lower:
                total_score += weight
                matches += 1
        
        confidence = min(1.0, total_score / 10.0) if matches > 0 else 0.5
        
        return {
            "priority": priority,
            "confidence": confidence,
            "matches": matches
        }
