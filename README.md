# AgentForms: Smarter Data Collection in an AI Agentic World

**What if the future of forms… isn’t a form at all?**

This project reimagines data collection by replacing static web forms with adaptive AI-powered agents. Our first prototype explores **concussion reporting and return-to-play** in youth sports, helping coaches and parents gather the right info, at the right time — with less guesswork and greater safety.

## 🌱 Phase 1: Concussion Reporting Agent
- Conversational intake agent using Streamlit
- Validates and adapts based on responses
- Outputs structured data (JSON, optional PDF)
- Guided return-to-play logic based on real protocols

## 📁 Folder Structure
- `src/client` — Streamlit interface
- `src/server` — FastAPI backend (if needed later)
- `src/utils` — Protocol logic, validation, formatting
- `data/` — Protocols, schemas, sample inputs
- `outputs/` — Run outputs and structured reports
- `logs/` — Logs for debugging and tracing
- `test/` — Unit and integration tests
- `notebooks/` — Exploratory dev
- `scripts/` — CLI helpers
