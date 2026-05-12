from app.clients.ollama_client import OllamaClient

class DraftNode:
    def __init__(self):
        self.client = OllamaClient()

    def generate_draft(self, message: str, intent: str, priority: str, policy: str) -> dict:
        """
        Generates a draft response using the LLM based on the context.
        Returns dict with 'response' and 'length'.
        """
        prompt = self._build_prompt(message, intent, priority, policy)
        response = self.client.generate(prompt)
        
        return {
            "response": response.strip(),
            "length": len(response.strip())
        }
    
    def _build_prompt(self, message: str, intent: str, priority: str, policy: str) -> str:
        """
        Builds an optimized prompt for the LLM with better structure and guidance.
        """
        priority_guidance = {
            "HIGH": "This is a HIGH priority issue. Acknowledge urgency and provide immediate next steps.",
            "MEDIUM": "This is a MEDIUM priority issue. Provide clear resolution steps and timeline.",
            "LOW": "This is a LOW priority issue. Provide helpful information and guidance."
        }
        
        guidance = priority_guidance.get(priority, "Provide helpful information and guidance.")
        
        prompt = f"""You are a professional and empathetic banking customer support representative.

=== CUSTOMER MESSAGE ===
{message}

=== ISSUE CLASSIFICATION ===
Issue Type: {intent}
Priority Level: {priority}
Guidance: {guidance}

=== RELEVANT POLICY ===
{policy}

=== RESPONSE REQUIREMENTS ===
1. Acknowledge the customer's specific concern with empathetic language
2. Reference the relevant policy or resolution timeline
3. Provide 1-2 clear, actionable next steps
4. Maintain a professional, helpful, and friendly tone
5. Keep the response concise (2-3 sentences max)
6. Do NOT include internal notes, placeholders, or disclaimers

=== DRAFT RESPONSE ===
"""
        return prompt
