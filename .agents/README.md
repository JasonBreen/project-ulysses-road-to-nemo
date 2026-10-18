# Project Ulysses agents and skills

Repo-local agent profiles live in `.agents/agents/`. Reusable workflows live in
`.agents/skills/`. The campaign-specific validation and path-audit skills are
adapted from the useful static-review pattern used in MD-OEM, while remaining
dependency-free and specific to this repository.

Available campaign workflows:

- `campaign-validation`: static contract, repository validation, and evidence boundaries.
- `campaign-path-audit`: focus/decision/event graph inspection.
- `canon-lore-research`: source-layer and canon policy review.
- `hoi4-content-scripting`: safe HOI4 scripting conventions.
- `localization-evidence`: localization integrity and source evidence.
- `map-asset-provenance`: map and asset provenance constraints.
- `validation-integration`: worktree, checks, and PR handoff rules.
- `ustio-continuity`: provenance-aware repair of the inherited Ustio focus/event handoff.
- `native-compatibility`: idempotent native-schema porting, isolated startup evidence, and base-vs-mod diagnostics.
