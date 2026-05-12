# Banking AI-Agent System

## Project Overview

This project implements a complete **AI agentic workflow** for customer support in the banking domain, fulfilling the requirements of the NLP in Industry course project.

The system intelligently processes customer inquiries through a structured 6-node pipeline:
1. **Intent Detection** → Classify banking issue (transfer failure, blocked account, etc.)
2. **Priority Assessment** → Determine urgency (LOW/MEDIUM/HIGH)
3. **Policy Retrieval** → Fetch relevant FAQ and support guidelines
4. **Response Drafting** → Generate professional reply using LLM
5. **Validation** → Check response quality and completeness
6. **Routing Decision** → Send response or escalate to human agent

---

## System Architecture

```
Customer Message
    ↓
┌─────────────────────────────────────┐
│   Intent Detection Node             │
│   (Uses Lab 2 fine-tuned model)     │
└────────────────┬────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Priority Detection Node           │
│   (Keyword-based scoring)           │
└────────────────┬────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Policy Retrieval Node             │
│   (Intent → FAQ mapping)            │
└────────────────┬────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Draft Response Node               │
│   (Ollama LLM - gpt-oss-20b)        │
└────────────────┬────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Validation Node                   │
│   (Quality & completeness checks)   │
└────────────────┬────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Router/Escalation Node            │
│   (Direct reply or escalate?)       │
└────────────────┬────────────────────┘
    ↓
Customer Response or Escalation
```

---

## Quick Start

### Prerequisites
- Python 3.9+
- 10GB+ disk space
- Ollama running locally or accessible via URL

### Installation

```bash
# 1. Clone/extract project
cd project_3

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup Ollama (in separate terminal)
ollama pull gpt-oss-20b
ollama serve

# 5. Configure environment
# Copy .env.example to .env and set your Ollama URL
copy .env.example .env

# 6. Run the server
python run.py
```

Server starts at: **http://localhost:8000**

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. **POST `/api/chat`** - Process Customer Message
Send a banking customer inquiry and receive AI-generated response with full trace.

**Request:**
```json
{
  "message": "I can't log in to my account, it says blocked.",
  "customer_id": "CUST_004"
}
```

**Response:**
```json
{
  "final_reply": "I understand how frustrating this is. Accounts are typically blocked due to security...",
  "escalate": true,
  "trace": {
    "intent": "blocked_account",
    "intent_confidence": 0.95,
    "priority": "HIGH",
    "priority_confidence": 0.92,
    "policy_retrieved": "Accounts may be blocked due to suspicious activity...",
    "draft_response": "I understand your concern. Your account security is important to us...",
    "validation_status": "VALID",
    "validation_issues": [],
    "validation_confidence": 0.85,
    "routing_decision": "escalate",
    "processing_time_ms": 1234.5,
    "timestamp": "2026-05-11T10:30:45.123456"
  }
}
```

#### 2. **GET `/health`** - Health Check
Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Testing

### Interactive API Testing
1. Open http://localhost:8000/docs
2. Click **Try it out** on `/api/chat`
3. Use examples from `examples/sample_requests.json`

### Command Line Testing

```bash
# Transfer failure example
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I tried to transfer money but it failed", "customer_id": "CUST_001"}'

# Fraud case (HIGH priority - will escalate)
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Someone stole my card, there are unauthorized charges", "customer_id": "CUST_003"}'
```

### Python Testing
```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "My card hasn't arrived", "customer_id": "CUST_002"}
)

data = response.json()
print(f"Final Response: {data['final_reply']}")
print(f"Escalated: {data['escalate']}")
print(f"Intent: {data['trace']['intent']}")
print(f"Processing Time: {data['trace']['processing_time_ms']}ms")
```

---

## Project Structure

```
project_3/
├── run.py                          # Entry point - starts FastAPI server
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment configuration template
├── README.md                      # This file
├── SETUP_GUIDE.md                # Detailed setup instructions
│
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application setup
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py           # Configuration & environment variables
│   │   └── schemas.py            # Pydantic data models
│   │
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── base.py               # Abstract LLM client interface
│   │   └── ollama_client.py      # Ollama implementation
│   │
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── intent_node.py        # Intent detection (Lab 2 model)
│   │   ├── priority_node.py      # ority/risk scoring
│   │   ├── policy_node.py        # Policy retrieval
│   │   ├── draft_node.py         # LLM response generation
│   │   ├── validation_node.py    # Quality validation
│   │   └── router_node.py        # Routing/escalation logic
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   └── orchestrator.py       # Main workflow controller
│   │
│   └── data/
│       ├── __init__.py
│       └── policies.py           # Policy/FAQ database
│
├── models/
│   └── intent_model/             # Lab 2 fine-tuned model
│       └── checkpoint-157/       # LoRA adapter checkpoint
│           ├── adapter_config.json
│           ├── adapter_model.safetensors
│           ├── tokenizer.json
│           └── ...
│
├── examples/
│   └── sample_requests.json      # Test case examples
│
└── outputs/                      # Generated artifacts (if any)
```

---

## 🔧 Configuration

### Environment Variables (.env)

Create `.env` file from `.env.example`:

```env
# Ollama Configuration
# For local Ollama (development):
OLLAMA_BASE_URL=http://localhost:11434
# For Google Colab + Pinggy (cloud):
# OLLAMA_BASE_URL=https://xxxx-xxx-xxx-xxx.run.pinggy-free.link

MODEL_NAME=gpt-oss-20b
LAB_2_MODEL_PATH=./models/intent_model/checkpoint-157

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

---

## ⚙️ System Components
System Components

### 1.s**: Fine-tuned model from Lab 2
- **Input**: Customer message
- **Output**: Intent classification + confidence
- **Supported Intents**:
  - `transfer_failure` - Money transfer issues
  - `card_not_received` - Delayed card delivery
  - `blocked_account` - Login/access issues
  - `refund_request` - Refund/refund request
  - `general_inquiry` - Other questions

### 2. Priority Detection Node
- **Method**: Keyword-based scoring
- **Output**: Priority level (HIGH/MEDIUM/LOW)
- **Escalation**: HIGH priority issues trigger automatic escalation
- **Keywords**:
  - HIGH: fraud, stolen, unauthorized, blocked, urgent
  - MEDIUM: transfer, refund, error, fail, problem
  - LOW: inquiry, question, general

### 3. Policy Retrieval Node
- **Database**: Dummy policies (easily replaceable with real database)
- **Mapping**: Intent → FAQ/Policy snippet
- **Usage**: Provides context for response generation

### 4. Response Drafting Node
- **LLM**: Ollama with gpt-oss-20b
- **Inputs**: Message, intent, priority, policy
- **Output**: Professional, context-aware response
- **Prompt**: Optimized for banking domain

### 5. Validation Node
- **Checks**:
  1. Response not too brief (>20 chars)
  2. Fallback detection (LLM unavailable)
  3. Empathetic language present
  4. Action-oriented content
  5. Policy alignment
  6. Length balance (<500 chars)
- **Output**: VALID/INVALID + issues + confidence

### 6. Router/Escalation Node
- **Rules**:
  - HIGH priority → Escalate
  - INVALID response → Escalate
  - Low confidence → Escalate
  - Low intent confidence (MEDIUM priority) → Escalate
- **Output**: `direct_reply` or `escalate`

---

## Troubleshooting

### Ollama Connection Error
```
Cannot connect to Ollama at http://localhost:11434
```
**Solution:**
```bash
# In separate terminal, ensure Ollama is running:
ollama serve
```

### Model Not Found
```
Model not found: gpt-oss-20b
```
**Solution:**
```bash
ollama pull gpt-oss-20b
# Wait for download (~5GB)
```

### Intent Model Loading Failed
```
Model loading failed: Model path not found
```
**Solution:**
```bash
# Verify checkpoint exists
ls -la models/intent_model/checkpoint-157/

# Should contain: adapter_config.json, adapter_model.safetensors, tokenizer.json
```

### Slow Responses (>10 seconds)
- Normal on CPU
- Run on GPU if available
- Increase timeout in `.env` if needed

### Port Already in Use
```
ERROR: [Errno 48] Address already in use
```
**Solution:**
```bash
# Change port in .env or kill existing process
# Windows: netstat -ano | findstr :8000
# Kill: taskkill /PID <PID> /F
```

---

## Performance

| Component | Time |
|-----------|------|
| Intent Detection (Lab 2 model) | ~200ms |
| Priority Detection | ~5ms |
| Policy Retrieval | ~1ms |
| LLM Response Generation | 2-10s |
| Validation | ~50ms |
| Total (cold start) | 5-20s |
| Total (warm) | 2-5s |

**Factors affecting speed:**
- Hardware (GPU 10x faster than CPU)
- Model size
- Internet latency (if using Pinggy)
- Ollama queue (other requests running)

---

## Lab Integration

**From Lab 2 (Project 2):**
- Uses fine-tuned intent classification model
- Located at: `project_3/models/intent_model/checkpoint-157/`
- Supported by LoRA adapter
- Can be re-trained or replaced

**To use different Lab 2 model:**
1. Copy new checkpoint to `models/intent_model/`
2. Update `LAB_2_MODEL_PATH` in `.env`
3. Restart the server

---

## Requirements Compliance

- [x] AI agentic pipeline for banking customer support
- [x] Intent Detection Node (uses Lab 2 fine-tuned model)
- [x] Priority/Risk Detection Node
- [x] Policy Retrieval Node
- [x] Response Drafting Node (Ollama LLM)
- [x] Validation Node
- [x] Escalation/Router Node
- [x] Ollama integration (gpt-oss-20b)
- [x] Example test requests
- [x] System design documentation
- [x] Complete folder structure
- [x] FastAPI server

---

## Next Steps

**To submit project:**
1. Ensure all nodes are working
2. Record video demonstration (2-5 minutes)
3. Push to GitHub
4. Include video URL in README

**Production improvements:**
- [ ] Add database backend for policies
- [ ] Implement user authentication
- [ ] Add request logging/analytics
- [ ] Create unit tests
- [ ] Deploy with Docker
- [ ] Add CI/CD pipeline

---

## Support

**For issues:**
1. Run `python check_startup.py` to diagnose
2. Check `SETUP_GUIDE.md` for detailed steps
3. Review error messages in terminal
4. Verify `.env` configuration

---

## License

This project is part of the NLP in Industry course at University of Science, HCMC.

**Course**: Applications of Natural Language Processing in Industry  
**Lecturer**: Dr. Nguyen Hong Buu Long  
**Date**: April 2026
