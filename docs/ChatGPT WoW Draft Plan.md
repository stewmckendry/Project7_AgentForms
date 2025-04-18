# 🤖🧠 ChatGPT WoW Pod: Operating Model for AI-Native Delivery

## 1. 🔁 Shared Memory Structure
A single source of truth, always accessible, and traceable across pods.

### 📂 Structure:
```
/docs/
  wow/                      # Operating model & pod roles
  specs/                    # Markdown specs per feature or module
  flows/                    # Flow maps for end-to-end journeys
  data_models/              # YAMLs for structured knowledge, config
  prompts/                  # Prompt templates per pod/task
  changelog.md              # Manual or auto-updated release log
```

### 🔄 Update Routines:
- Use versioned file names or Git history
- Each pod updates their outputs (e.g. QA writes test results to /docs/qa/)
- A `docbot` assistant tracks updates and alerts if stale

---

## 2. ✍️ Prompt Templates Per Pod
Reusable and optimized prompt formats to align with pod purpose.

### 🧪 QA Pod
```
You're a QA agent. Your job is to:
- Identify edge cases and failure points
- Test recent features
- Output reproducible test cases + observed vs expected results

Inputs:
- Feature spec
- Sample inputs/outputs
- Prior issues if relevant
```

### 🧑‍💻 Dev Pod
```
You're a Dev agent. Your job is to:
- Implement a new feature based on spec
- Update relevant interface definitions
- Add comments + call trace points
- Return updated code block and brief changelog

Inputs:
- Feature spec
- Flow diagram or interfaces
- Test coverage notes (if any)
```

### 📚 Research Pod
```
You're a Research agent. Your job is to:
- Gather domain-specific references
- Structure findings (lists, YAML, tables)
- Recommend ways to integrate it into product logic

Inputs:
- Research brief
- Target format (YAML, Markdown, JSON)
- Context or examples
```

### 📦 Delivery Lead Pod
```
You're a Delivery Lead. Your job is to:
- Track progress across pods
- Identify blockers or missing inputs
- Align documentation, versioning, flow
- Suggest next best action for each pod

Inputs:
- Current pod outputs
- Spec/flow status
- Prior changelog
```

---

## 3. ⚙️ Recommended AI-Powered Delivery Process

### ⛏ LLM Code Generation
- All code outputs traceable to a Markdown spec + feature ID
- Use templated function interface specs
- Store generated snippets + tests side-by-side for QA reuse

### 🧪 Testing / QA
- Auto-gen test harnesses from YAML specs
- Validate edge cases with LLM help (e.g. malformed, incomplete input)
- Save failed prompts to `test_fails/` for retraining or deeper probes

### 🧠 Multi-Agent Systems
- Delivery Lead orchestrates using a `pod_status.yaml`
- Each pod works asynchronously, stores checkpoints
- AI router (future) helps triage between pods

### 🧾 Documentation
- Every pod contributes Markdown to `/docs/`
- Delivery Lead bundles + pushes changelogs
- All prompt templates versioned in `/prompts/`

### 🤝 Dev Handoff
- Dev Pod outputs:
  - Updated code block
  - Interface spec
  - Prompt history (optional)
  - What changed, what needs QA
- QA Pod starts from `dev_output.md`
- Handoff tracked in `handoff_log.yaml`

---

## 🧭 Final Notes
You’re designing not just how we build one app — but a playbook for *any* AI-native product team.

Next steps:
- Wire up shared folder structure
- Kick off each pod with their template
- Pilot with a new feature cycle
- Log learnings in `/docs/wow/retrospectives.md`

Let’s build the operating system for building smart things. 🚀

