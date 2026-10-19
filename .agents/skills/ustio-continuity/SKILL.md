---
name: ustio-continuity
description: Repair and extend the inherited Ustio HOI4 scaffold with explicit provenance and guarded postwar handoffs.
---

# Ustio continuity

Use this skill for Ustio focus trees, events, decisions, localization, and
postwar handoffs.

- Read `docs/CANON_POLICY.md`, `docs/CANON_LEDGER.md`, and
  `docs/LORE_EVENT_COVERAGE_BACKLOG.md` first.
- Treat the April 5, 2024 archive and inherited Ustio text as mod provenance;
  do not promote it to official canon.
- Preserve the existing `UST_sold_land_to_ratio_flag` and
  `UST_not_sold_land_to_ratio_flag` outcomes. Do not invent borders, cores,
  geography, or Joker 1 chronology.
- Prefer reconnecting existing IDs over replacing the Ustio scaffold. New
  shared IDs must use the `ac_` namespace and be idempotently guarded.
- Add localization and a static regression contract with each new event/focus
  handoff. Report static validation separately from native playability.

Minimum checks:

```powershell
py tools/Test-UstioContinuity.py
py tools/validate_campaign.py --mod-root mod\2985041246
pwsh tools/Run-UlyssesCampaignChecks.ps1
```
