from app.core.schemas import CustomerQuery, AgentResponse, NodeTrace
from app.nodes.intent_node import IntentNode
from app.nodes.priority_node import PriorityNode
from app.nodes.policy_node import PolicyNode
from app.nodes.draft_node import DraftNode
from app.nodes.validation_node import ValidationNode
from app.nodes.router_node import RouterNode
import time
from datetime import datetime

class WorkflowOrchestrator:
    def __init__(self):
        self.intent_node = IntentNode()
        self.priority_node = PriorityNode()
        self.policy_node = PolicyNode()
        self.draft_node = DraftNode()
        self.validation_node = ValidationNode()
        self.router_node = RouterNode()

    def process_request(self, query: CustomerQuery) -> AgentResponse:
        start_time = time.time()
        trace = NodeTrace()
        trace.timestamp = datetime.now().isoformat()
        
        try:
            # 1. Intent Detection
            try:
                intent_result = self.intent_node.detect_intent_with_confidence(query.message)
                trace.intent = intent_result["intent"]
                trace.intent_confidence = intent_result["confidence"]
            except Exception as e:
                trace.intent = "general_inquiry"
                trace.intent_confidence = 0.3
                trace.error_details = f"Intent detection failed: {str(e)}"
                print(f"Intent detection error: {e}")
            
            # 2. Priority Detection
            try:
                priority_result = self.priority_node.detect_priority_with_score(query.message)
                trace.priority = priority_result["priority"]
                trace.priority_confidence = priority_result["confidence"]
                trace.priority_matches = priority_result["matches"]
            except Exception as e:
                trace.priority = "MEDIUM"
                trace.priority_confidence = 0.3
                trace.error_details = f"Priority detection failed: {str(e)}"
                print(f"Priority detection error: {e}")
            
            # 3. Policy Retrieval
            try:
                trace.policy_retrieved = self.policy_node.retrieve_policy(trace.intent)
            except Exception as e:
                trace.policy_retrieved = "General support policy: Please contact our support team for assistance."
                trace.error_details = f"Policy retrieval failed: {str(e)}"
                print(f"Policy retrieval error: {e}")
            
            # 4. Response Drafting
            try:
                draft_result = self.draft_node.generate_draft(
                    query.message, trace.intent, trace.priority, trace.policy_retrieved
                )
                trace.draft_response = draft_result["response"]
                trace.draft_length = draft_result["length"]
            except Exception as e:
                trace.draft_response = "Thank you for contacting us. We appreciate your message. Our support team will review your request and get back to you shortly."
                trace.draft_length = len(trace.draft_response)
                trace.error_details = f"Draft generation failed: {str(e)}"
                print(f"Draft generation error: {e}")
            
            # 5. Validation
            try:
                validation_result = self.validation_node.validate_draft(
                    trace.draft_response, trace.policy_retrieved, trace.intent
                )
                trace.validation_status = validation_result["status"]
                trace.validation_issues = validation_result["issues"]
                trace.validation_confidence = validation_result["confidence"]
            except Exception as e:
                trace.validation_status = "VALID"
                trace.validation_confidence = 0.5
                trace.error_details = f"Validation failed: {str(e)}"
                print(f"Validation error: {e}")
            
            # 6. Routing Decision
            try:
                trace.routing_decision = self.router_node.route(
                    trace.priority, 
                    trace.validation_status,
                    validation_confidence=trace.validation_confidence,
                    intent_confidence=trace.intent_confidence
                )
            except Exception as e:
                trace.routing_decision = "escalate"
                trace.error_details = f"Routing failed: {str(e)}"
                print(f"Routing error: {e}")
            
            # Calculate processing time
            trace.processing_time_ms = (time.time() - start_time) * 1000
            
            # Determine final response
            escalate = trace.routing_decision == "escalate"
            if escalate:
                final_reply = "Your issue has been escalated to a human agent. They will contact you shortly."
            else:
                final_reply = trace.draft_response
            
            return AgentResponse(
                final_reply=final_reply,
                escalate=escalate,
                trace=trace
            )
        
        except Exception as e:
            # Catch-all for unexpected errors
            trace.processing_time_ms = (time.time() - start_time) * 1000
            trace.error_details = f"Unexpected error: {str(e)}"
            print(f"Unexpected error in orchestrator: {e}")
            
            return AgentResponse(
                final_reply="An unexpected error occurred. Please contact support.",
                escalate=True,
                trace=trace
            )
