
# 💻 Client Integration Spec – Concussion App (Updated)

## Modes
- Assess a possible concussion
- Ask about return to play

---

## Flow: Assess a Concussion

### 1. User Enters Freeform Explanation
→ Call `/analyze`

### 2. Agent Extracts Structured Answers
- Returns `draft_responses` and `summary_thought`
- No need to call `/finalize`

### 3. Follow-Up Q&A Loop (Optional)
- Use `/followups` to clarify low-certainty answers

### 4. Generate Return-to-Play Guidance
- Use `/guidance` with finalized bundle

---

## Flow: Ask Return-to-Play Question

- User enters natural language question
- Uses `/rtp/ask` for LLM-powered contextual answer

---

## Removed
- `/finalize` step is deprecated (now merged into `/analyze`)
