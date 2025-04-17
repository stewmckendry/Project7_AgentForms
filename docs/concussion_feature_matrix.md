# 🧩 Concussion Agent – Feature & Function Matrix

| Feature                            | Function(s) / Module                      | Purpose                                                                 |
|------------------------------------|-------------------------------------------|-------------------------------------------------------------------------|
| **Freeform Situation Intake**      | `analyze_freeform_input()`                | Extracts structured assessment answers from a natural language story   |
| **Assessment Flow Engine**         | `ConcussionAgent`, `concussion_assessment.yaml` | Walks user through staged question flow with memory + reasoning      |
| **LLM-Powered Parsers**            | `llm_parse_date`, `llm_extract_symptoms`, `llm_interpret_yes_no` | Extract structured responses from messy user input                      |
| **Symptom Comparison & Lookup**    | `compare_symptoms_to_reference()`         | Checks symptom severity & match vs evidence-based references           |
| **Follow-up Question Generation**  | `generate_followup_question()`            | Probes for more info to raise certainty, Socratic-style                |
| **AI Guidance Generator**          | `generate_guidance()`                     | Summarizes status and produces empathetic, evidence-backed guidance    |
| **Return-to-Play Q&A**             | `generate_rtp_response_llm()`             | Answers RTP questions based on protocol and user context               |
| **YAML-Driven Logic**              | `concussion_assessment.yaml`, `symptoms_reference.yaml`, `return_to_play.yaml` | Modularize knowledge + logic                                          |
| **PDF/Markdown Reporting**         | `generate_report()`, `generate_summary()` | Output user-friendly assessment summaries                             |
| **Logging & Debugging**            | `logger`, `logs/app.log`                  | Track every decision, prompt, and parse for traceability               |
| **API Backend**                    | FastAPI (`/evaluate`, `/rtp/ask`, etc.)   | Bridge between client and reasoning logic                              |
| **Client UI**                      | Streamlit                                 | Conversational UI for user interaction                                 |