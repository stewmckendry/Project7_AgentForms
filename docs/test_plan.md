# ✅ Concussion Agent – QA Pod Test Plan

Welcome to the QA mission for the **Concussion Agent** app. This test plan outlines our approach to ensuring the app is accurate, reliable, and user-friendly for parents and coaches.

---

## 🎯 Mission Overview

The Concussion Agent helps assess potential concussions and guides safe return-to-play using:
- AI-driven parsing and reasoning
- YAML-based logic
- Conversational UI (Streamlit)
- API backend (FastAPI)
- Evidence-based protocols (SCAT6, ONF)

---

## 🧪 Test Plan Structure

### 🔍 1. Functional QA – Core Flows

| Test Case | Description |
|-----------|-------------|
| F1.1 | Freeform story → Extracted structured responses |
| F1.2 | Correct validator called per question type (date, symptoms, boolean) |
| F1.3 | Follow-up generation when certainty is low |
| F1.4 | Guidance summarizes inputs with empathy and logic |
| F1.5 | RTP questions return correct structured response from protocol |

---

### 🚨 2. Edge Case & Negative Testing

| Test Case | Description |
|-----------|-------------|
| E2.1 | Vague or contradictory input (e.g., "maybe yesterday or today") |
| E2.2 | Missing or malformed inputs |
| E2.3 | Multiple symptom mentions with mixed severity |
| E2.4 | User reverses earlier input later in conversation |
| E2.5 | Empty response to follow-up questions |

---

### 🎨 3. UX & Communication Testing

| Test Case | Description |
|-----------|-------------|
| U3.1 | Prompts are friendly and understandable |
| U3.2 | Certainty and logic are explained transparently |
| U3.3 | Guidance avoids medical advice but feels actionable |
| U3.4 | User can clearly follow what stage they’re in |

---

### 🧰 4. Integration QA

| Test Case | Description |
|-----------|-------------|
| I4.1 | Thought traces align with flow logic |
| I4.2 | Symptom match severity correct against reference YAML |
| I4.3 | Full chat + logs captured in `logs/app.log` |
| I4.4 | Follow-up question reasons match strategy YAML |
| I4.5 | Re-parsed responses overwrite older versions cleanly |

---

## 🧭 Execution Approach

We will:
- Start with high-priority functional flows (F1.1 to F1.5)
- Run manually via UI or scripted with `pytest`
- Log all feedback for debrief + iteration
- Automate stable flows for CI

---

## 🧠 Next Step

1. Begin with **F1.1: Freeform story to structured responses**
2. Test manually or request a `test_case_bundle_f1_1` to simulate inputs
3. Report findings → Iterate → Automate

---

Let’s ship a better, safer AI tool for parents and coaches.

– QA Pod 🧠🔍