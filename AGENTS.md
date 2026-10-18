# Project Ulysses agent instructions

## Scope and safety

- This repository is a private, local continuation of the April 5, 2024 Project Ulysses archive. Preserve `source/archive-original` and `source/baseline`; never rewrite either.
- Keep work in an isolated Git worktree/branch. Do not force-push, merge automatically, change repository visibility, publish a release, contact the original developers, or alter `G:\Project-Swallow`.
- Do not launch HOI4, change display settings, alter user saves/settings, or run downloaded mod code unless the user separately approves native testing. Static inspection and static validators are the default.
- Do not invent official ACE COMBAT history, postwar borders, corporate history, or future events to fill the 2065 engineering horizon. Label archive material as mod provenance, Sam's material as user-authored continuity, and balance mechanics as provisional gameplay.

## Canon and content workflow

1. Read `docs/CANON_POLICY.md`, `docs/CANON_LEDGER.md`, and `.agents/skills/canon-lore-research/SKILL.md` before adding lore-sensitive content.
2. Inspect existing focus/event/decision IDs and open GitHub issues before creating new work. Extend an existing contract when possible; do not duplicate issue #6 (canon/Joker 1), #8 (native runtime), #5 (2065/technology), #7 (economy/workspace), or #4 (1.19 parity).
3. Every new lore-sensitive row or implementation must state source layer, exact citation/private reference, affected IDs/files, and status.
4. Keep the 1991 bookmark as the campaign start without implying that every Belkan War event occurred on that date. Preserve alternate outcomes as explicit gameplay branches.

## HOI4 implementation

- Use stable `ac_` IDs for new shared systems and tag-prefixed IDs for country-specific content.
- Add event, focus, decision, idea, and localization definitions together; use the existing namespace and localization conventions.
- Prefer idempotent flags and guarded effects. Do not repurpose existing IDs or resolve state 171/`XXX` geography without an approved source-backed decision.
- Use `.agents/skills/hoi4-content-scripting/SKILL.md` for scripting changes and `.agents/skills/map-asset-provenance/SKILL.md` for map or asset changes.

## Validation and evidence

From the repository root, run static checks with the current PowerShell host:

```powershell
$mod = Join-Path $PWD 'mod\2985041246'
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Test-UlyssesStatic.ps1 -ModRoot $mod
```

If a read-only installed reference is available, add `-ReferenceGameRoot $env:ULYSSES_GAME_ROOT`. Record command, commit, warnings, and whether a check is static or native. Native runtime claims require an approved isolated workflow and must be reported separately.

Use `.agents/skills/validation-integration/SKILL.md` for checks, PR review, exact-head CI, and worktree handoff. Use `.agents/skills/localization-evidence/SKILL.md` for localization additions and BOM/reference checks.

## Collaboration

- Preserve other agents' branches and worktrees; inspect before touching overlapping files.
- Keep commits narrow enough to review, but do not split a single event contract from its ideas, decisions, localization, tests, and documentation.
- Before opening a PR, confirm the diff is based on current `origin/main`, static checks pass, no forbidden assets were added, the worktree is clean except for intended changes, and the PR is left open for review.
