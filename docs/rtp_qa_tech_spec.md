# 🛠️ Technical Spec: Return-to-Play Q&A Feature

## ✨ Purpose
Let users ask RTP-related questions (e.g., “Can they skate today?”) and get structured, evidence-based responses based on `return_to_play.yaml`.

This supports user goal #2: **"What can my child do now?"**

---

## 🔁 Flow Summary
1. User enters a free-form RTP question (e.g., “Can my son play soccer?”)
2. System searches `return_to_play.yaml` to find matching activity
3. Determines the stage required for that activity
4. Uses current assessment status (if available) to determine if it's safe to proceed
5. Responds with personalized, protocol-grounded advice

---

## 🧩 Dependencies & Reusable Code

### ✅ Files / Data Already Available
- `return_to_play.yaml` — structured YAML of stages, activities, progression, risks
- `assessment_bundle` — contains:
  - Final responses (e.g. `cleared_to_play`, `still_symptomatic`, `symptoms`)
  - Reasoning + certainty
  - Follow-up log

### ✅ Relevant Utilities
- `find_current_stage(responses)` *(to be implemented)* — logic to infer current RTP stage
- `generate_guidance()` — can be reused if full guidance is needed
- `generate_followup_question()` — can be called if more info is needed

---

## 🧠 New Function to Build

```python
def generate_rtp_response(activity_name: str, assessment_bundle: dict) -> dict:
    '''
    Returns protocol-aware recommendation for activity, including:
    - activity_match: True/False
    - stage_required: Stage name / ID
    - allowed: Yes/No/Unclear
    - reason: Summary of decision logic
    - recommendations: Markdown-safe string to show user
    '''
```

---

## ✅ Output Goals

| Field | Description |
|-------|-------------|
| `allowed` | `"yes"`, `"no"`, or `"uncertain"` |
| `stage_required` | Which protocol stage the activity appears in |
| `reason` | Brief justification (e.g., “Still symptomatic, and activity not permitted until Stage 5”) |
| `recommendations` | Full LLM-generated answer |
| `citations` | (Optional) protocol source citation from YAML |

---

## 📣 Notes
- Add a disclaimer: “This is not a medical diagnosis. Please consult a healthcare professional.”
- Responses should be markdown-safe (for app display + reports)