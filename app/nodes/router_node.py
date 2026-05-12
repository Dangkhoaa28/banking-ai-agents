class RouterNode:
    def route(self, priority: str, validation_status: str, validation_confidence: float = None, intent_confidence: float = None) -> str:
        """
        Decides the final routing: 'direct_reply', 'escalate', or 'request_info'.
        
        Rules:
        - HIGH priority always escalates
        - INVALID validation status escalates
        - Low confidence in key decisions triggers escalation
        """
        # Rule 1: High priority always escalates
        if priority == "HIGH":
            return "escalate"
        
        # Rule 2: Invalid validation escalates
        if validation_status == "INVALID" or (isinstance(validation_status, str) and validation_status.startswith("INVALID")):
            return "escalate"
        
        # Rule 3: Low confidence in validation escalates
        if validation_confidence is not None and validation_confidence < 0.4:
            return "escalate"
        
        # Rule 4: Very low intent confidence on medium priority issues
        if priority == "MEDIUM" and intent_confidence is not None and intent_confidence < 0.5:
            return "escalate"
        
        # Default: direct reply for valid responses
        return "direct_reply"
