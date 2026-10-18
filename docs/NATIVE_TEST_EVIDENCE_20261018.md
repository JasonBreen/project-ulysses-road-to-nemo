# Native HOI4 Checkpoint — 2026-10-18

This records the local native startup checkpoint for the Project Ulysses continuation work. It is evidence for compatibility triage, not a claim that the campaign is runtime-complete or release-ready.

## Source and environment

- Source worktree: `G:\Project-Ulysses-Continuation-campaign`
- Active source mod: `G:\Project-Ulysses-Continuation-campaign\mod\2985041246`
- Local repair commit: `ee82591` (`Quarantine legacy schema and repair campaign scripts`)
- Archived source revision SHA-256: `e3e2ec384e3f0e4dba6678f76f2520822f85d677be47f418dfc1e39c738c9071`
- Native game executable: `G:\steamlbirary\steamapps\common\Hearts of Iron IV\hoi4.exe`
- Detected native version: `Operation Postern v1.19.3.0.c01a (5632)`
- Isolated test payload: `C:\Users\New\Documents\Paradox Interactive\Hearts of Iron IV\mod\ProjectUlysses_Continuation_native_20261018`
- Isolated test profile: `G:\Project-Ulysses-Continuation-native-test-20261018\userdir-native-final6-20261018`

## Observed native checkpoint

- The isolated profile activated `Project Ulysses: Continuation`.
- The game reached the 1991 history execution point (`[1991.01.01.12] Executing History`).
- The final run reported zero invalid module/category/map errors from the Ulysses-owned content filters.
- The exact HOI4 process was closed gracefully after the checkpoint.
- The game-root `launcher-settings.json` was restored byte-for-byte to the backup SHA-256 `1F51E45EA63AB69D6CEE85749AA9E500B385EB6A8EF372E5D7BA70215446547E`.
- No `hoi4` process remained after cleanup.

## Static and regression checks

- `tools\Test-UstioContinuity.py`: passed.
- `tools\test_economy.py`: 27 tests passed.
- `tools\Test-UlyssesStatic.ps1`: errors `0`; remaining warnings are one placeholder-owned state, 204 placeholder strategic-region files, and an empty `map/positions.txt` without a vanilla reference root.

## Known boundaries

- This was a native startup/activation checkpoint, not a long-run campaign, save/reload, AI, DLC, focus-reachability, or continuity test.
- The installed/base game produced 469 total `error.log` entries during the run, mostly outside the Ulysses source tree. These remain an environment/install compatibility issue and prevent calling the runtime log clean.
- The first non-isolated native attempt touched one existing career-profile file; saves, playsets, DLC configuration, and launcher settings were preserved/restored as recorded in the task evidence.
