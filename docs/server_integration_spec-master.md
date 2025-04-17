# 🔧 Server-Side Integration Spec: Concussion Agent App (FastAPI)

## 🧠 Purpose
Stitch together the full end-to-end assessment and return-to-play (RTP) features behind a structured API interface.

---

## 🚦 Routes

### `/ping` — Health check
**Method**: GET  
**Returns**: `{"status": "ok"}`

---

### `/analyze` — Analyze free-form input  
**Method**: POST  
**Input**: `{ "free_text": str }`  
**Output**:
```json
{
  "draft_responses": { ... },
  "summary_thought": "..."
}
```
**Uses**: `analyze_freeform_input(free_text: str, question_list: list) -> dict`

---

### `/finalize` — Finalize responses  
**Method**: POST  
**Input**: `{ "draft_responses": {...} }`  
**Output**: Final responses with metadata  
**Uses**: `finalize_draft_responses(draft: dict, question_list: list) -> dict`

---

### `/followups` — Generate follow-up questions  
**Method**: POST  
**Input**:
```json
{
  "final_responses": { ... },
  "question_list": [ { "id": ..., "prompt": ..., "type": ... } ]
}
```  
**Output**: `{ "followups": [str, ...] }`  
**Uses**: `generate_followup_question(...)`

---

### `/guidance` — Generate overall guidance  
**Method**: POST  
**Input**: `assessment_bundle` dict  
**Output**: `{ "summary_markdown": ..., "risk_level": ..., "stage": ... }`  
**Uses**: `generate_guidance(bundle: dict) -> str`

---

### `/rtp` — Return-to-play Q&A  
**Method**: POST  
**Input**:
```json
{
  "activity_name": "hockey",
  "assessment_bundle": { ... }
}
```  
**Output**:
```json
{
  "allowed": "yes|no|uncertain",
  "stage_required": "Stage 5",
  "reason": "...",
  "recommendations": "...",
  "citations": [...]
}
```
**Uses**: `generate_rtp_response(activity_name: str, bundle: dict) -> dict`

---

## 📁 File / Data Loaders

- `load_yaml("data/protocols/concussion_assessment.yaml")`
- `load_yaml("data/protocols/return_to_play.yaml")`
- `load_yaml("data/protocols/symptoms_reference.yaml")`

Use caching where appropriate to avoid reloading on each request.

---

# 🧠 Server Integration Spec – v3

## 🧩 Overview
Expose RTP Q&A route that uses LLM-powered reasoning over protocol reference and user context.

---

## 🔗 Route: `POST /rtp/ask`

### ✅ Description
Takes a natural-language question and user assessment bundle.
Returns structured RTP response based on embedded protocol logic.

---

## 📥 Request Body
```json
{
  "question": "Is it safe to do light exercise?",
  "assessment_bundle": {
    "responses": { ... },
    "thoughts": { ... },
    "summary_thought": "...",
    "symptom_comparison": { ... }
  }
}
```

---

## 📤 Response Body
```json
{
  "allowed": false,
  "stage_required": "Stage 2",
  "reason": "Light aerobic activity is only recommended after 24-48 hours of rest.",
  "recommendations": ["Start with walking or stationary bike", "Monitor for symptoms"],
  "citations": ["Parachute Return to Sport Protocol, Stage 2"]
}
```

---

## 🔍 Function to Call

```python
from src.models.rtp_qa import generate_rtp_response_llm
```

---

## 🧱 Dependencies

- `return_to_play.yaml` in `data/protocols/`
- `assessment_bundle` generated earlier in the app
- `symptoms_reference.yaml` optionally used in reasoning

---

## 🛡️ Guardrails

If no match is found or response is unclear:
```json
{
  "allowed": null,
  "reason": "Unable to determine an answer from the protocol. Please consult a healthcare provider.",
  "citations": []
}
```