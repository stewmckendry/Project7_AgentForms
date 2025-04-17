
# 🧠 Symptom Reference Guide for Concussion Agent

This document explains how the `symptom_reference.yaml` file enhances the intelligence and reliability of our AI-powered concussion assessment system.

---

## 📌 Purpose

The symptom reference serves as a **structured knowledge base** of clinically recognized concussion symptoms. It enables our AI agent to:
- Interpret user-reported symptoms with greater precision
- Detect red flags and assign severity
- Ask better follow-up questions
- Generate more personalized, evidence-informed guidance

---

## 📂 File Location

```text
data/reference/symptom_reference.yaml
```

---

## 🧱 Structure of Each Symptom Entry

Each symptom is represented as a YAML object with the following fields:

```yaml
- name: headache
  category: physical
  severity: moderate
  description: Pressure or pain in the head, may worsen with activity or light
  flags:
    - worsening
    - sensitivity to light
  guidance: Monitor; seek care if persistent or worsening
```

### Fields:
- `name`: Canonical symptom name (used for matching)
- `category`: Type of symptom (physical, cognitive, emotional, sleep, red flag)
- `severity`: Clinical importance (low, moderate, high)
- `description`: What the symptom typically means
- `flags`: Conditions that may escalate risk
- `guidance`: General recommendation for this symptom

---

## 🔄 How It’s Used in the System

### ✅ 1. In `llm_extract_symptoms()`
- The LLM is optionally provided with this reference to match against
- User inputs like "felt weird" or "got dizzy" are mapped to structured symptoms
- Severity and flags are attached to parsed results

### ✅ 2. In follow-up generation
- Follow-up questions are dynamically shaped by the category or severity of symptoms
- E.g. “You mentioned dizziness — did they lose their balance or fall down?”

### ✅ 3. In `generate_guidance()`
- Red flags trigger stronger recommendations to seek care
- Persistent symptoms influence advice to delay return to play

---

## 🧪 Future Enhancements

- Add `aliases` for better matching (e.g., "blurred vision" → "vision problems")
- Tag symptoms with example phrasings from youth athletes
- Link symptoms to protocol-based return-to-play staging

---

## 💡 Summary

By grounding symptom reasoning in a structured medical reference, we help ensure:
- Greater **accuracy**
- Smarter **AI decisions**
- More **trustworthy** experiences for parents, coaches, and caregivers
