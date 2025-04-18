# ✍️ CONTRIBUTING.md – AI-Native Delivery

Welcome to our human + AI delivery system! This guide defines how each pod (and human) contributes code, content, and structured reasoning artifacts in a traceable, collaborative way.

---

## 🧠 General Guidelines

- All meaningful contributions — whether code, markdown, YAML, JSON, prompts, or protocols — are submitted via `.diff` patch files into `.patches/`
- This includes **features, tests, prompts, documentation, structured flows, and specs**
- Each patch must include:
  - 📒 `docs/changelog.md` entry – what changed and why
  - 🧠 `logs/thought_trace.md` entry – how it was reasoned
  - 🔁 `docs/wow/handoff_log.yaml` entry – **only if** the work is being handed off to another pod
- GitHub Actions will auto-apply the patch, create a feature branch, and open a pull request with these logs included

---

## 🧰 Folder Structure

| Folder | Purpose |
|--------|---------|
| `.patches/` | Patch files dropped by pods (e.g. `gpt_patch_f3.1_dev.diff`) |
| `docs/` | Changelog, specs, markdown outputs, delivery SOPs |
| `logs/` | Reasoning traces for decisions or logic |
| `scripts/` | Tools for automation (e.g. `generate_patch.py`) |
| `.github/workflows/` | GitHub Action to apply patches + open PRs |

---

## 📦 Patch Naming Convention

- Format: `gpt_patch_<feature_id>_<pod_type>.diff`
- Example: `gpt_patch_f4.3_dev.diff`
- One patch per feature, fix, or deliverable (code, content, YAML, or flow)

---

## 📋 Log Files – Format and Behavior

| Log File | Type | Format | Behavior |
|----------|------|--------|----------|
| `changelog.md` | Append-only | Markdown | Shared master file — 1 section per change or sprint |
| `thought_trace.md` | Append-only | Markdown | Shared master — entries added per patch |
| `handoff_log.yaml` | Append-only | YAML | Shared master — each handoff is a new item if a file is passed to another pod |

> These are not overwritten or per-feature files. The GitHub Action reads the latest entries per patch and includes them in the PR.

**To view recent entries**: scroll to the bottom of each file (most recent entries are always added last).

If a change does **not involve a handoff** (e.g., a dev pod updates a YAML spec but no other pod is involved), the contributor **only needs to update `changelog.md` and `thought_trace.md`.** The `handoff_log.yaml` can be left unchanged.

---

## 🤖 Pod Responsibilities

### `dev_pod`
- Writes or modifies code, prompts, or structured YAML specs
- Uses `generate_patch.py` before submission
- Appends changelog and thought trace entries

### `qa_pod`
- Creates test plans, validation cases, and regression probes
- Documents test logic and risk reasoning in `thought_trace.md`

### `research_pod`
- Investigates external references, extracts structured data
- Produces YAML specs, markdown briefs, or prompt suggestions
- Explains synthesis logic and references in `thought_trace.md`

### `wow_pod`
- Improves delivery model, tools, or process rituals
- Maintains docs under `docs/wow/` and pod SOPs

---

## ✅ Submission Checklist

- [x] `.diff` file dropped into `.patches/`
- [x] `docs/changelog.md` updated (append at bottom)
- [x] `logs/thought_trace.md` updated (append at bottom)
- [x] `docs/wow/handoff_log.yaml` updated **only if files are handed off to another pod**
- [x] Pull request is created by GitHub Action and includes all logs

---

Thank you for helping build the world’s most collaborative, traceable AI delivery system. 🧠⚡

