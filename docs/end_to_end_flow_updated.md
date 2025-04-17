
# 🧠 Concussion Agent – Updated End-to-End Flow

## Overview
The Concussion Agent processes free-form incident descriptions and produces structured assessments, clarifications, and guidance grounded in return-to-play protocols.

---

## 🧭 Step-by-Step Flow

### 1. Input Collection
- A parent or coach enters a free-form explanation of the incident
- Example: "My son hit his head during hockey yesterday. He was dizzy today."

### 2. Freeform Analysis
- `analyze_freeform_input(agent, user_input)` runs:
  - LLM-based structured reasoning over all question fields
  - Refines certain fields using:
    - `llm_extract_symptoms()` (symptoms)
    - `llm_parse_date()` (dates)
    - `llm_interpret_yes_no()` (booleans)
  - Output:
    ```json
    {
      "draft_responses": {
        "symptoms": {
          "value": ["dizziness"],
          "certainty": "medium",
          "thought": "User said 'dizzy today'",
          "parsed_by": "llm_extract_symptoms"
        },
        ...
      },
      "summary_thought": "The player is symptomatic and likely in early recovery."
    }
    ```

### 3. Follow-Up Conversation Loop
- For each low-certainty field:
  - Generate contextual question using `generate_followup_question()`
  - Re-parse user reply using the appropriate typed parser
  - Store updated responses and reasoning trail

### 4. Return-to-Play Guidance
- Bundle final responses into `assessment_bundle`
- Use `generate_guidance(assessment_bundle)` to generate:
  - Stage recommendation
  - Risk warnings
  - Markdown-safe instructions

### 5. Optional RTP Q&A
- Users can ask follow-up questions like “Can they go to gym class?”
- Handled by `generate_rtp_response_llm()` using current bundle and protocol

---

## ✅ Summary
- The finalization step is now embedded in `analyze_freeform_input`
- Simplifies API and client logic
- Enables faster, more accurate responses with less user overhead
