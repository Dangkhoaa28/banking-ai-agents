POLICIES = {
    "transfer_failure": "If a transfer fails, verify the recipient's details. If funds were deducted, they will be automatically refunded within 3-5 business days. Do not attempt the transfer again immediately.",
    "card_not_received": "New cards typically arrive within 7-10 business days. If it has been longer, we will cancel the lost card and issue a replacement free of charge.",
    "blocked_account": "Accounts may be blocked due to suspicious activity or multiple incorrect login attempts. The customer must verify their identity via phone call or visiting a branch to unblock the account.",
    "refund_request": "Refund requests for unauthorized transactions must be filed within 60 days of the statement date. We will investigate and issue a provisional credit within 10 business days.",
    "general_inquiry": "Thank you for contacting us. For general inquiries, please visit our FAQ page on the website or speak to a representative for specific details."
}

def get_policy(intent: str) -> str:
    """Returns the policy snippet for a given intent."""
    return POLICIES.get(intent, POLICIES["general_inquiry"])
