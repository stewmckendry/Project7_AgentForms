# 📦 generate_patch.py
# Tool to auto-generate a patch and associated delivery logs from a pod

import os
import subprocess
from datetime import datetime
from pathlib import Path

# === CONFIG ===
PATCHES_DIR = Path(".patches")
CHANGELOG = Path("docs/changelog.md")
THOUGHT_TRACE = Path("logs/thought_trace.md")
HANDOFF_LOG = Path("docs/wow/handoff_log.yaml")

os.makedirs(PATCHES_DIR, exist_ok=True)

# === INPUTS ===
feature_id = input("Feature ID (e.g. f4.3): ").strip()
pod_type = input("Pod type (dev, qa, research): ").strip().lower()
author = input("Author (e.g. dev_pod, human): ").strip()
description = input("Short summary of change: ").strip()

patch_name = f"gpt_patch_{feature_id}_{pod_type}.diff"
branch_name = f"chatgpt/dev/{feature_id}_{pod_type}"

# === STEP 1: Create patch ===
print("🧠 Creating git diff patch...")
subprocess.run(["git", "diff"], stdout=open(PATCHES_DIR / patch_name, "w"))

# === STEP 2: Append changelog ===
sprint_label = f"Sprint {datetime.now().strftime('%W')} – {datetime.now().strftime('%B %d')}"
with open(CHANGELOG, "a") as f:
    f.write(f"\n### {sprint_label}\n\n")
    f.write(f"#### ✨ Added\n- Patch `{patch_name}` – {description}\n\n")
    f.write(f"#### 🧠 Reasoning\nSee thought_trace.md\n\n")

# === STEP 3: Append thought trace ===
with open(THOUGHT_TRACE, "a") as f:
    f.write(f"\n---\n### Patch: {patch_name}\n**Author:** {author}\n**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
    f.write(f"**Reasoning:**\n> {description}\n\n")

# === STEP 4: Optional handoff log ===
handoff = input("Add handoff log entry? (y/n): ").strip().lower()
if handoff == "y":
    to = input("To which pod?: ").strip()
    files = input("Comma-separated file paths to hand off: ").strip().split(',')
    reason = input("Reason for handoff: ").strip()
    with open(HANDOFF_LOG, "a") as f:
        f.write(f"\n  - from: {author}\n")
        f.write(f"    to: {to}\n")
        f.write(f"    date: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"    files:\n")
        for file in files:
            f.write(f"      - {file.strip()}\n")
        f.write(f"    reason: \"{reason}\"\n")
        f.write(f"    related_patch: {patch_name}\n")

print(f"✅ Patch created: {PATCHES_DIR / patch_name}")
print("📒 Changelog, 🧠 Thought trace, and 🔁 Handoff log updated.")
print("🚀 Ready for delivery!")