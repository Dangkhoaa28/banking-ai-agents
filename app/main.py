from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.schemas import CustomerQuery, AgentResponse
from app.agent.orchestrator import WorkflowOrchestrator

app = FastAPI(title="Banking AI-Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = WorkflowOrchestrator()

@app.post("/api/chat", response_model=AgentResponse)
async def chat_endpoint(query: CustomerQuery):
    response = orchestrator.process_request(query)
    return response

@app.get("/health")
def health_check():
    return {"status": "healthy"}
