
# 🚀 Server Integration Spec – Concussion Agent (Updated)

## API Routes

### ✅ `/ping`
Simple health check

---

### ✅ `/analyze` — ⛏️ Runs full freeform assessment analysis
- Input:
```json
{
  "free_text": "My daughter hit her head and was dizzy after school."
}
```

- Output:
```json
{
  "draft_responses": {
    "symptoms": {
      "value": ["dizziness"],
      "certainty": "medium",
      "thought": "User mentioned dizziness.",
      "parsed_by": "llm_extract_symptoms"
    },
    ...
  },
  "summary_thought": "Likely recent concussion with mild symptoms."
}
```

- Notes:
  - No separate `/finalize` call needed
  - Embeds typed parsing logic (symptoms, dates, yes/no)
  - Uses `agent.known_questions` internally

---

### ✅ `/followups`
Generates follow-up questions for low-certainty fields

### ✅ `/guidance`
Returns markdown-safe return-to-play guidance based on `assessment_bundle`

### ✅ `/rtp`
Checks whether a specific activity is allowed given current stage

### ✅ `/rtp/ask`
LLM-powered Q&A about recovery and return-to-play timing
