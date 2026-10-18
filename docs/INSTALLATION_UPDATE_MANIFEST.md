# Deferred installation update manifest

This is a source-side checklist only. It deliberately does not modify the
active HOI4 Documents installation while the user is in multiplayer.

## Source to install later

- Source worktree: `G:\Project-Ulysses-Continuation-campaign`
- Branch: `codex/ustio-continuity-slice`
- Current source head: record the final commit hash immediately before the
  approved installation window.
- Target mod payload: `mod\2985041246`
- Immutable source baseline: `source\baseline`
- Immutable original archive: `source\archive-original`

## Deferred copy checklist

1. Confirm the user is out of HOI4 multiplayer and has approved a local
   installation sync.
2. Re-run `tools\Run-UlyssesCampaignChecks.ps1` against the exact source head.
3. Copy only the reviewed `mod\2985041246` payload into the private local mod
   staging location; do not touch saves, settings, playsets, or unrelated mods.
4. Preserve a pre-sync manifest and SHA-256 inventory of the destination.
5. Verify descriptor paths and supported-version text before opening the launcher.
6. If native testing is approved, use `docs\NATIVE_PLAYTEST_CHECKLIST.md` and
   report runtime results separately from static checks.

## Explicitly out of scope

- No HOI4 or launcher launch during this source task.
- No Documents installation change in this source task.
- No downloaded code execution, remote publication, push, release, or developer contact.
