# Banking AI-Agent - Setup and Run Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.9+
- ~10GB disk space (for models)
- Ollama running locally or accessible via URL

### 1️⃣ Install Dependencies
```powershell
cd project_3
pip install -r requirements.txt
```

### 2️⃣ Setup Ollama

**Local Setup (Recommended)**
```bash
# Download: https://ollama.ai
# After installing, open terminal and run:
ollama pull gpt-oss-20b
ollama serve  # Runs on http://localhost:11434
```

**Or use Google Colab + Pinggy**
- See `Ollama-Pinggy.ipynb` in project_2

### 3️⃣ Configure Environment
Copy `.env.example` to `.env` and set your Ollama URL:
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=gpt-oss-20b
```

### 4️⃣ Run the Server
```powershell
python run.py
```

### 5️⃣ Test the API
Visit: http://localhost:8000/docs

---

## Workflow Pipeline

```
Customer Message
        ↓
[Intent Node] → Detect banking intent (using Lab 2 model)
        ↓
[Priority Node] → Determine urgency (HIGH/MEDIUM/LOW)
        ↓
[Policy Node] → Retrieve relevant FAQ/policy
        ↓
[Draft Node] → Generate response using Ollama LLM
        ↓
[Validation Node] → Check quality & completeness
        ↓
[Router Node] → Decide: Send response OR Escalate?
        ↓
Customer Response
```

---

## API Endpoints

### POST `/api/chat`
Send a customer message and get AI agent response.

**Request:**
```json
{
  "message": "I can't log in to my account",
  "customer_id": "CUST_123"
}
```

**Response:**
```json
{
  "final_reply": "I understand your concern...",
  "escalate": false,
  "trace": {
    "intent": "blocked_account",
    "intent_confidence": 0.95,
    "priority": "HIGH",
    "priority_confidence": 0.88,
    "policy_retrieved": "Accounts may be blocked due to...",
    "draft_response": "I understand...",
    "validation_status": "VALID",
    "validation_issues": [],
    "routing_decision": "escalate",
    "processing_time_ms": 1234.56
  }
}
```

### GET `/health`
Check API health status.

---

## Testing Examples

See `examples/sample_requests.json` for 5 pre-made test cases:

1. **Transfer Failure** - Money not received
2. **Card Not Received** - Delayed card delivery  
3. **Fraud Suspected** - Unauthorized charges (HIGH PRIORITY)
4. **Blocked Account** - Login issues (ESCALATES)
5. **General Inquiry** - Branch hours question

---

## Troubleshooting

**Error: "Ollama not reachable"**
- Make sure `ollama serve` is running in another terminal
- Check OLLAMA_BASE_URL in .env matches your setup
- For Colab: Verify Pinggy tunnel is active

**Error: "Model not found"**
- Run: `ollama pull gpt-oss-20b`
- Wait for download to complete

**Error: "Intent model checkpoint not found"**
- Ensure `models/intent_model/checkpoint-157/` exists
- Should contain: `adapter_config.json`, `adapter_model.safetensors`, etc.

**Slow responses (>10 seconds)**
- Normal on CPU, faster on GPU
- Increase model inference timeout if needed

---

## Project Structure

```
project_3/
├── run.py                    # FastAPI entry point
├── requirements.txt          # Dependencies
├── .env                     # Configuration (create from .env.example)
├── README.md                # Project overview
├── SETUP_GUIDE.md          # This file
├── app/
│   ├── main.py             # FastAPI app setup
│   ├── core/
│   │   ├── settings.py      # Configuration
│   │   └── schemas.py       # Pydantic models
│   ├── clients/
│   │   ├── base.py          # LLM client interface
│   │   └── ollama_client.py # Ollama implementation
│   ├── nodes/
│   │   ├── intent_node.py   # Intent detection (uses Lab 2 model)
│   │   ├── priority_node.py # Priority scoring
│   │   ├── policy_node.py   # Policy retrieval
│   │   ├── draft_node.py    # Response generation
│   │   ├── validation_node.py # Quality checks
│   │   └── router_node.py   # Escalation logic
│   ├── agent/
│   │   └── orchestrator.py  # Workflow controller
│   ├── data/
│   │   └── policies.py      # Policy database (dummy)
│   └── __init__.py
├── models/
│   └── intent_model/        # Lab 2 fine-tuned model
│       └── checkpoint-157/
├── examples/
│   └── sample_requests.json # Test cases
└── outputs/                 # Generated artifacts
```

---

## Performance Notes

- **First request**: 5-15 seconds (model initialization)
- **Subsequent requests**: 2-5 seconds (on CPU), <1 second (on GPU)
- **Intent detection**: ~200ms (from Lab 2 model)
- **LLM response generation**: 1-10 seconds (depends on Ollama)

---

## Next Steps for Production

- [ ] Add database for policies (currently hardcoded)
- [ ] Implement user authentication
- [ ] Add request logging/analytics
- [ ] Create unit tests
- [ ] Deploy with Docker
- [ ] Setup CI/CD pipeline
- [ ] Create video demonstration (required for submission)

