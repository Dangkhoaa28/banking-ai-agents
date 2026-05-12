class ValidationNode:
    def validate_draft(self, draft: str, policy: str, intent: str = None) -> dict:
        """
        Validates the generated draft with semantic checks.
        Returns dict with 'status', 'issues', and 'confidence'.
        """
        issues = []
        
        # Check 1: Basic length
        if not draft or len(draft.strip()) < 20:
            issues.append("Response too brief or empty")
        
        # Check 2: Fallback detection
        if "fallback generated response" in draft.lower():
            issues.append("Fallback response detected - LLM unavailable")
        
        # Check 3: Empathetic language
        empathetic_markers = ["understand", "apologize", "appreciate", "help", "concern", "issue"]
        has_empathy = any(marker in draft.lower() for marker in empathetic_markers)
        if not has_empathy and len(draft) > 50:
            issues.append("Missing empathetic language")
        
        # Check 4: Action-oriented
        action_markers = ["will", "can", "next step", "please", "contact", "visit", "call"]
        has_action = any(marker in draft.lower() for marker in action_markers)
        if not has_action:
            issues.append("Missing clear action items")
        
        # Check 5: Policy alignment
        if policy:
            if "day" in policy.lower() or "hour" in policy.lower():
                timeframe_in_draft = any(word in draft.lower() for word in ["day", "hour", "business"])
                if not timeframe_in_draft and len(draft) > 80:
                    issues.append("Response lacks mentioned timeframe from policy")
        
        # Check 6: Length balance (not too long)
        if len(draft) > 500:
            issues.append("Response too long - should be concise")
        
        # Determine status and confidence
        status = "VALID" if len(issues) == 0 else "INVALID"
        confidence = max(0.0, 1.0 - (len(issues) * 0.2))
        
        return {
            "status": status,
            "issues": issues,
            "confidence": confidence
        }
