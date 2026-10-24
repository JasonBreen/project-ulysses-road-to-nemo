---
name: native-compatibility
description: Port inherited Project Ulysses HOI4 identifiers to a verified native schema with idempotent tooling and explicit runtime evidence.
---

# Native compatibility

Use this workflow for HOI4 version-porting and startup repair.

1. Read `AGENTS.md`, preserve `source/archive-original` and `source/baseline`, and inspect the current branch/worktree before edits.
2. Inventory active references and definitions. Compare IDs to the installed game’s native files; do not assume a static definition count proves reachability.
3. Prefer a namespaced compatibility definition when the archive ID is gameplay-significant. Otherwise map a history reference to a native ID with a documented rationale.
4. Make porting tools idempotent and whole-token aware. Add a regression check for repeated invocation before applying them to all histories.
5. Run static validators and the narrow repository regression tests. Record warnings separately from errors.
6. For authorized native checks, use a collision-free profile and payload, keep launcher settings backed up, close the exact process gracefully, restore the backup, and hash-verify it.
7. Compare a no-mod control when attributing log errors. Categorize Ulysses-owned errors separately from base-game, installed-DLC, and environment diagnostics.
8. Do not claim focus reachability, save/reload stability, AI behavior, DLC completeness, or long-run continuity from startup evidence alone.

Useful local tooling includes `tools/Port-NativeEquipmentReferences.py`, `Test-UlyssesStatic.ps1`, `Validate-UlyssesReferences.ps1`, `Validate-UlyssesTechnologies.ps1`, `Test-UstioContinuity.py`, and `test_economy.py`.
