---
name: campaign-validation
description: Validate the Project Ulysses Belkan campaign contract and report static versus native evidence.
---

# Campaign validation

Use this skill for campaign-arc changes touching focuses, decisions, events,
ideas, on_actions, or their localization.

1. Run `python tools/validate_campaign.py --mod-root mod/2985041246`.
2. Run `python tools/analysis/campaign_path_report.py --mod-root mod/2985041246`.
3. Run `powershell -NoProfile -ExecutionPolicy Bypass -File tools/Test-UlyssesStatic.ps1 -ModRoot mod/2985041246`.
4. Run `python tools/test_economy.py` when economy hooks are touched.
5. Run `powershell -NoProfile -ExecutionPolicy Bypass -File tools/Test-NoVanillaProvenance.ps1` when provenance tooling changes.
6. Inspect the diff for duplicate IDs, missing localization, developer paths,
   and unguarded repeat effects.

These checks are static/offline. They do not establish that HOI4 can load the
mod, that a focus is reachable in a real save, or that AI and save/load behavior
are correct. Native testing requires a separately approved isolated workflow.
