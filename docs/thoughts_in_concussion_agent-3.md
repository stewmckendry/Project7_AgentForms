
# 🧠 Capturing and Using Thoughts in the Concussion Agent

In this project, "thoughts" are the reasoning traces captured from each step of the AI’s decision-making process. They make the agent more intelligent, auditable, and trustworthy.

---

## ✅ What Are "Thoughts"?

A **thought** is a natural language explanation of *how* or *why* the agent arrived at a particular answer. It's not just the *what*, but the *why* — and that changes everything.

---

## 🧩 Where Thoughts Are Used

### 1. 📝 **Freeform Draft Inference**
When the user shares a narrative:
- LLM generates draft responses to known questions
- Each response includes a `thought`, e.g.:

```json
{
  "value": "yesterday",
  "thought": "The user said the injury happened during practice yesterday.",
  "certainty": "high"
}
```

### 2. 🔍 **LLM Parsing of Drafts**
Each draft is then passed through specialized parsers (`llm_parse_date`, `llm_extract_symptoms`, etc.). Each parser returns:
- Final value
- Updated certainty
- New thought

We store both the **draft** and **parsed** thoughts in a response history log.

### 3. 🤔 **Follow-Up Question Generation (Next Step)**
The thoughts help us:
- Identify ambiguity (e.g. “they seemed off” → unclear symptom)
- Justify follow-up questions ("You mentioned a headache — could you clarify how long it lasted?")
- Explain uncertainty

---

## 🧠 Layers of Thought

| Layer | Source | Purpose |
|-------|--------|---------|
| **Draft Thought** | From LLM initial inference | Reflects how the agent mapped user story to questions |
| **Parsed Thought** | From parser function | Shows how raw input was interpreted, validated |
| **Follow-up Thought** *(planned)* | Meta-reasoning | Guides the next question, based on gaps or contradictions |

---

## 🧬 Why This Matters (Reasoning Theory)

This mirrors cognitive psychology and reasoning frameworks like:

- **Chain of Thought** prompting — break complex problems into interpretable steps
- **Transparent AI** — surfacing rationale builds trust and enables correction
- **Reflective Reasoning** — lets us revise answers based on deeper inspection

In essence, thoughts are the building blocks of **explainable agentic reasoning**.

---

## 💡 Future Uses

- Show thoughts in final guidance summary for transparency
- Use thoughts to drive explanation-based feedback (“We suggested rest because the player reported symptoms including... ”)
- Detect contradictions or gaps in reasoning

---

---

## 📘 Thoughts Beyond Follow-Up

These captured thoughts aren’t just useful during the conversation. They become foundational throughout the entire lifecycle of this data:

### ✅ 1. Personalized Guidance
Thoughts enrich final guidance by grounding advice in what was said:
> _"Because the player reported dizziness and no medical evaluation yet, we recommend..."_

### ✅ 2. Explainable Reports
Reports for coaches, parents, or providers can show:
- What was said
- What the AI interpreted
- Why the AI gave the guidance it did

### ✅ 3. System Integration / Audit Logs
If responses are sent to a downstream medical or incident system:
- Thoughts provide **context** and **confidence**
- Helps humans triage, override, or act with understanding

---

## 🔄 Summary

> Thoughts = "memory of reasoning"

They form a traceable narrative that makes this system:
- More helpful to users
- More explainable to humans
- More trustworthy over time


---

## 🛠 Implementation Details

### 📂 Where Thoughts Are Captured

Thoughts are created in multiple stages of the agent pipeline:

| Stage | Module | Function |
|-------|--------|----------|
| Draft response generation | `analyze_freeform_input()` | Captured per question from LLM |
| Response validation | `finalize_draft_responses()` | Parsed thoughts added by specialized LLM parsers |
| History tracking | `agent.responses[q_id]["history"]` | Stores all thoughts for a given question |

---

### 🧱 Thoughts Schema

Each thought object follows a common pattern:

```json
{
  "value": ...,              // final or intermediate value
  "certainty": "low|medium|high",
  "thought": "...",          // LLM’s reasoning
  "source": "draft_inference | llm_parse_date | llm_interpret_yes_no | ..."
}
```

These are stored in:

```python
agent.responses[question_id] = {
  "value": ...,              # final value after parsing
  "certainty": ...,          # final certainty
  "thought": ...,            # final thought (from parser)
  "parsed_by": ...,          # which function generated this value
  "original_input": ...,     # raw string or user input
  "history": [               # versioned trace of all reasoning steps
    { "source": ..., "value": ..., "thought": ..., "certainty": ... },
    ...
  ]
}
```

---

### 🧪 Access and Usage

- **To inspect a final thought**:
  ```python
  agent.responses["symptoms"]["thought"]
  ```

- **To get reasoning history**:
  ```python
  for entry in agent.responses["symptoms"]["history"]:
      print(entry["source"], "→", entry["thought"])
  ```

- **To trace how guidance was formed**: 
  - Link thoughts to guidance recommendations
  - Highlight which symptoms or flags triggered which part of the advice

---

This consistent schema and tracking lets the agent reason transparently — and gives us a strong foundation for follow-ups, summaries, and reporting.

