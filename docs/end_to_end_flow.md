# 🔄 Concussion Agent – End-to-End Flow

This document describes the complete user journey and backend logic flow.

---

## 🧠 Main Use Cases

1. **Does my child have a concussion?**
2. **What can my child safely do (Return to Play)?**

---

## 🔁 Full Flow Overview

### 1. ✅ User opens the app
- Greeted by agent
- Prompted to explain what happened

---

### 2. 📝 User submits free-form story
- Example: "My son was hit in the head during baseball practice yesterday and had a headache last night."

---

### 3. 🔍 AI triages story
- `analyze_freeform_input()`
- Extracts draft responses per question
- Adds reasoning (`thoughts`) + overall summary

---

### 4. 🧪 Parsed answers go through LLM validation
- Per question type (date, yes/no, symptoms)
- Calls: `llm_parse_date`, `llm_extract_symptoms`, `llm_interpret_yes_no`

---

### 5. 🧠 Follow-up question loop
- For each low-certainty or missing item:
  - Generate: `generate_followup_question()`
  - Capture user input
  - Re-parse and record with versioning + thoughts

---

### 6. 📚 Compare symptoms to reference
- `compare_symptoms_to_reference()`
- Adds match data by severity category

---

### 7. 💡 Generate AI-powered guidance
- `generate_guidance()`
- Combines:
  - Validated responses
  - Summary thought
  - Symptom match
  - Follow-up insights
- Returns: plain-language summary, not medical advice

---

### 8. 🧾 User receives summary
- Shown in app
- Optionally exported as Markdown, HTML, or PDF

---

## 🧠 Optional Add-On: Return to Play Q&A

At any time, user may ask:
- "Can they go to gym class?"
- "When can they play soccer again?"

App calls:
- `generate_rtp_response_llm(question, assessment_bundle)`
- Uses protocol from `return_to_play.yaml` + embedded context

Returns structured response:
- ✅ Allowed (bool)
- 📌 Stage required
- 📋 Recommendations
- 📚 Citations

---

## 📦 Artifacts Logged

- Full chat history
- Inputs, parsed values, certainty
- Thoughts + follow-up chain
- Final guidance
- Logs: `logs/app.log`

---

This flow ensures:
- Contextual AI
- Transparent reasoning
- Guided, friendly experience