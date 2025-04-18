x# 💡 Client-Side Integration Spec: Concussion Assistant (Streamlit)

## 🧠 Purpose
Stitch together the full user-facing experience — collecting info, guiding assessment, asking follow-up questions, and answering RTP queries — into a conversational, friendly experience.

---

## 🌐 Backend Communication

```python
API_URL = "http://localhost:8001"  # FastAPI server endpoint
```

All client logic communicates with the backend via REST calls using this base URL.

---

## 🧭 Core Flow

1. **Welcome screen**
   - Intro + options: “Assess a possible concussion” vs. “Ask about return to play”

2. **Free-form input collection**
   - Collect and send to `/analyze`
   - Display summary + interpreted answers

3. **Review + follow-up**
   - Show follow-up questions one-by-one (conversation loop)
   - Auto-call `/followups` + record responses

4. **Confirm final responses**
   - Merge final data
   - Option to edit/review

5. **Generate guidance**
   - Call `/guidance`
   - Display markdown-safe output in Streamlit

6. **Return-to-Play assistant**
   - Ask: “What activity are you wondering about?”
   - Send to `/rtp`
   - Display friendly, protocol-based reply

---

## 🧩 UI Elements

- `st.chat_input()` + `st.chat_message()` for messaging loop
- Tabs or sidebar to switch between “Assessment” and “Ask a question”
- Markdown previews for guidance and summaries

---

## 📦 State Management

- `st.session_state.assessment_bundle`
- `st.session_state.chat_history`
- `st.session_state.mode` (assessment vs. RTP)


---

## 🔗 API Interface Specs

### `/analyze`
- **POST**
- **Input**: `{ "free_text": str }`
- **Output**:
```json
{
  "draft_responses": {
    "symptoms": { "value": ..., "certainty": ..., "thought": ... },
    ...
  },
  "summary_thought": "..."
}
```

---

### `/finalize`
- **POST**
- **Input**:
```json
{
  "draft_responses": {
    "symptoms": { "value": ..., "certainty": ..., "thought": ... },
    ...
  }
}
```
- **Output**:
```json
{
  "final_responses": { ... },
  "version": "v1",
  "all_thoughts": [ ... ]
}
```

---

### `/followups`
- **POST**
- **Input**:
```json
{
  "final_responses": { ... },
  "question_list": [
    { "id": "symptoms", "prompt": "...", "type": "symptom" },
    ...
  ]
}
```
- **Output**:
```json
{
  "followups": [ "What symptoms are still present?", ... ]
}
```

---

### `/guidance`
- **POST**
- **Input**: `assessment_bundle: { responses, thoughts, summary }`
- **Output**:
```json
{
  "summary_markdown": "...",
  "risk_level": "high|medium|low",
  "stage": "Stage 3"
}
```

---

### `/rtp`
- **POST**
- **Input**:
```json
{
  "activity_name": "soccer",
  "assessment_bundle": { ... }
}
```
- **Output**:
```json
{
  "allowed": "yes|no|uncertain",
  "stage_required": "Stage 5",
  "reason": "...",
  "recommendations": "...",
  "citations": [ ... ]
}
```

---

# 🤖 Client Integration Spec – v4

## 🎯 Purpose
Support conversational Return-to-Play (RTP) questions using an LLM-powered Q&A system.

---

## 🧠 New Feature: Return-to-Play Q&A

### ✅ Feature Description
User can ask free-form questions like:
- “Can my child play soccer this weekend?”
- “Is it safe to bike if symptoms are gone?”

Agent responds using protocol knowledge + user assessment context.

---

## 🔁 Streamlit UI Changes

### 🆕 Add to UI:
- Chat input box: “Ask a question about return to play”
- On submit:
    - Call API: `POST /rtp/ask`
    - Display response message
    - Optionally highlight:
        - ⛔ Allowed or Not Allowed
        - 📌 Protocol Stage
        - 🧠 Reason
        - 📚 Citations

---

## 🔗 API Route

**POST** `/rtp/ask`

**Request Body**
```json
{
  "question": "Can my child go back to gym class?",
  "assessment_bundle": {
    "responses": { ... },
    "thoughts": { ... },
    "summary_thought": "...",
    "symptom_comparison": { ... }
  }
}
```

**Response Body**
```json
{
  "allowed": true,
  "stage_required": "Stage 4",
  "reason": "Light aerobic activity is allowed before full return to sport.",
  "recommendations": ["Start with light jogging", "Avoid contact drills"],
  "citations": ["Parachute Return to Sport Protocol, Stage 4"]
}
```

---

**LLM-Powered**
Uses vector search over `return_to_play.yaml` + user’s `assessment_bundle`.

If unsure → default response: “Please consult a healthcare professional.”