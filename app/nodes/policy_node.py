from app.data.policies import get_policy

class PolicyNode:
    def retrieve_policy(self, intent: str) -> str:
        """
        Retrieves the relevant policy based on the intent.
        """
        return get_policy(intent)
