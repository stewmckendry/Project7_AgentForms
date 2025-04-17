# 🧠 AgentForms: Smarter Data Collection in an AI Agentic World

**What if the future of forms… isn’t a form at all?**

This project reimagines data collection by replacing static web forms with adaptive, AI-powered agents. Our first prototype tackles **concussion assessment and return-to-play guidance** in youth sports — helping coaches and parents gather critical info, adapt based on risks, and make safer decisions.

---

## ✅ Key Features

### 🔍 Conversational Concussion Assessment
- LLM-powered interpretation of free-form input
- Structured reasoning over protocols (e.g., SCAT6, ONF)
- Dynamic follow-up questions based on uncertainty or risk
- Transparent decision traces (“thoughts”) captured at every step

### 🏃 Return-to-Play Protocol Checker
- YAML-based evidence-informed return-to-play guidance
- Ask free-form questions like: “Can they bike today?”
- LLM + retrieval logic provides protocol-aligned, human answers

### 📦 Outputs
- Structured JSON data (for systems)
- Markdown + PDF summaries (for people)
- Optional citations + reasoning for each stage

---

## 📁 Folder Structure

```plaintext
src/
├── client/        # Streamlit UI
├── server/        # FastAPI backend (API routes)
├── models/        # LLM reasoning and validation logic
├── utils/         # YAML parsing, formatters, loaders
data/
├── protocols/     # Assessment flows and RTP reference
├── samples/       # Example inputs
outputs/           # Saved evaluations and summaries
logs/              # Structured logs + token usage
test/              # Pytest tests
notebooks/         # Experimental workflows
scripts/           # CLI helpers (build, run, deploy)
```

---

## 🚀 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start app
./scripts/run-dev.sh
```

---

## 📌 Status
Phase 1 complete: End-to-end pipeline working with real protocols, LLM reasoning, and human-friendly reports.  
Phase 2 underway: Smarter follow-ups, return-to-play Q&A, and deployment polish.

---

## 🛡️ Disclaimer
This app is a **decision support tool**, not a medical device. For any suspected concussion, consult a licensed healthcare provider.

---

## 👋 Get Involved
Want to test, contribute, or explore similar ideas in education, public health, or citizen services?  
Let’s connect: [LinkedIn](https://www.linkedin.com/in/stewmckendry)