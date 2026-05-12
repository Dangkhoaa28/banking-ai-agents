from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CustomerQuery(BaseModel):
    message: str
    customer_id: Optional[str] = "unknown"

class NodeTrace(BaseModel):
    # Intent Detection
    intent: Optional[str] = None
    intent_confidence: Optional[float] = None
    
    # Priority Detection
    priority: Optional[str] = None
    priority_confidence: Optional[float] = None
    priority_matches: Optional[int] = None
    
    # Policy Retrieval
    policy_retrieved: Optional[str] = None
    
    # Response Drafting
    draft_response: Optional[str] = None
    draft_length: Optional[int] = None
    
    # Validation
    validation_status: Optional[str] = None
    validation_issues: Optional[List[str]] = None
    validation_confidence: Optional[float] = None
    
    # Routing Decision
    routing_decision: Optional[str] = None
    
    # Meta information
    processing_time_ms: Optional[float] = None
    error_details: Optional[str] = None
    timestamp: Optional[str] = None

class AgentResponse(BaseModel):
    final_reply: str
    escalate: bool
    trace: NodeTrace
