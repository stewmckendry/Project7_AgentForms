
# 🧠 LLM-Powered Parsers: Strategy and Lessons Learned

This document outlines how we are using LLMs to intelligently parse user inputs in the Concussion Agent project, and what we've learned in the process.

---

## 🎯 Purpose

We're using OpenAI-powered functions to parse complex, natural user inputs into structured data. This enables:

- 🧾 Smart data collection
- 🔍 Transparency through reasoning
- 🤖 Adaptive follow-up questions
- 📊 Accurate reporting

---

## ⚙️ LLM-Powered Parsers in Use

### 1. `llm_parse_date(input_text)`
- Interprets vague or relative phrases like "last Friday", "this morning"
- Anchors to today's date
- Returns:
  ```json
  {
    "value": "2025-04-15",
    "certainty": "high",
    "thought": "Interpreted 'yesterday' based on today's date (2025-04-16)"
  }
  ```

### 2. `llm_interpret_yes_no(input_text)`
- Handles ambiguity like "I guess so", "probably not", "yes but only for a bit"
- Extracts:
  - intent: `yes`, `no`, `partial`, or `uncertain`
  - certainty: `high`, `medium`, `low`
  - thought: model's reasoning for its decision

### 3. `llm_extract_symptoms(input_text)`
- Extracts symptoms from descriptive text
- Maps free-form input to standard terms like "headache", "dizziness"
- Returns a list + certainty + LLM reasoning

---

## 📚 Lessons Learned from Prompt Tuning

### ✅ 1. Structure matters
- Explicit output format + example responses improve consistency

### ✅ 2. Thoughts are gold
- Capturing reasoning (`thought`) helps us debug, explain, and refine flows

### ✅ 3. Certainty adds intelligence
- Using `certainty` lets us:
  - Trigger follow-up questions
  - Flag vague data
  - Calibrate our advice to risk

### ✅ 4. Avoid assumptions
- Phrases like "he didn't mention it" shouldn't be interpreted as "no"
- We updated prompts to avoid making leaps without data

### ✅ 5. Real-world responses are messy
- Answers are often partial, hesitant, or contextual
- Our parsers treat ambiguity as a feature, not a flaw

---

## 🧪 Next Steps

- Integrate parser certainty + thoughts into dynamic follow-up logic
- Use thoughts in reports for traceability
- Explore LLM self-evaluation (e.g. "What information is still missing?")

---
