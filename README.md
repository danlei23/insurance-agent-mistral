
# 🏠 Insurance Coverage Checker (Local Mistral)

This is a production-ready agent system that helps users automatically determine whether a given insurance policy covers a specific situation — based on natural language questions and a text version of the insurance policy.

## ✅ Problem This Project Solves

Insurance policy documents are often long, legalistic, and hard to understand. Policyholders may struggle to know what is covered or excluded.

This project solves that problem using a locally running LLM agent that can:

- Read and understand a policy document
- Accept natural language questions from the user
- Respond with whether the situation is covered or not
- Justify the answer and explain any deductible involved

---

## 🤖 Agent Application and LLM Flow

### Architecture Overview

```
User Query ──> Streamlit UI ──> Agent (LangGraph Workflow)
                                     │
                                     ├── classify_intent
                                     ├── retrieve_policy_text
                                     ├── prompt LLM (Mistral via Ollama)
                                     ├── parse JSON output
                                     └── format final answer (✅ / ❌)
```

### LLM

- This agent uses a **local Mistral model** (run through [Ollama](https://ollama.com)) to ensure privacy and offline usage.
- The prompt format strictly requests valid JSON responses.

### Agent Logic

Implemented using `langgraph`. The main workflow:

1. **Intent classification** – detect whether the user is asking about insurance coverage
2. **Policy analysis** – feed question + policy into Mistral
3. **Output formatting** – show a nice message like:

```
✅ Covered  
Explanation: Sewer backup is covered if the rider is present.  
Deductible: $1000
```

---

## 🖥️ How to Run

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running (`ollama run mistral`)
- Streamlit installed

### Setup

```bash
git clone https://github.com/your-username/insurance-agent-mistral-local.git
cd insurance-agent-mistral-local

# Optional: create venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Start Ollama (once)

```bash
ollama run mistral
```

### Run UI

```bash
streamlit run app.py
```

---

## 📝 Assumptions

- The insurance policy is stored as a plain `.txt` file (`example_policy.txt`)
- The user asks one question at a time
- The model will not guess — only answers if the policy clearly includes/excludes the situation
- Output from the LLM is expected to be **strict JSON** and parsed

---

## 📁 Project Structure

```
.
├── agents/
│   └── insurance_agent_mistral.py   # Core LangGraph agent logic
├── app.py                           # Streamlit UI
├── test_local_agent_ollama.py      # CLI test interface
├── example_policy.txt              # Sample insurance policy
├── requirements.txt
└── README.md                        # This file
```

---

## 📦 Production Notes

- The system is modular: you can swap in any LLM backend (e.g., Bedrock, Gemini)
- Errors and parsing failures are handled gracefully
- Streamlit UI uses `chat_message` interface for clean display
- Full Mistral prompts are designed for interpretability and reliability

---

## 👤 Author

Danlei Geng  

