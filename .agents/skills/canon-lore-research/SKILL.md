---
name: canon-lore-research
description: Build source-traceable Project Ulysses lore and event coverage without conflating official ACE COMBAT material, Sam's continuity, archive provenance, or gameplay abstractions.
---

# Canon and lore research

Use this skill for lore, chronology, character, faction, organization, technology, border, or event work.

- Read `docs/CANON_POLICY.md`, `docs/CANON_LEDGER.md`, and `docs/LORE_EVENT_COVERAGE_BACKLOG.md` first.
- Search the existing repository before proposing new IDs: `Get-ChildItem mod\2985041246 -File -Recurse | Select-String -Pattern '<term>'`.
- Prefer primary Project Aces/ACE COMBAT sources for dates, borders, names, characters, equipment, and established relationships. Record the exact URL or private source reference in the ledger/backlog.
- Keep the four source layers separate: official, user-authored continuity, mod provenance, and provisional gameplay. Archive text is evidence of what the old mod attempted, not official canon.
- Do not infer Joker 1 dates, motives, locations, or causal links beyond the supplied user-authored outline. Do not fabricate 2006–2065 history merely because the engine cutoff is 2065.
- Treat “implemented,” “static-reference-validated,” “reachable,” and “native-tested” as different statuses.

Acceptance: every new lore claim has provenance, affected files/IDs, and a clear unresolved/open state where evidence is incomplete.
