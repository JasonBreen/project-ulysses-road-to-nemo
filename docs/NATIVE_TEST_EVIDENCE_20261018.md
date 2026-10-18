# Native HOI4 checkpoint — 2026-10-18

This is a compatibility checkpoint, not a claim that the campaign is runtime-complete or release-ready.

## Source and environment

- Worktree: `G:\Project-Ulysses-Continuation-campaign`
- Active source: `G:\Project-Ulysses-Continuation-campaign\mod\2985041246`
- Archive SHA-256: `e3e2ec384e3f0e4dba6678f76f2520822f85d677be47f418dfc1e39c738c9071`
- Native executable: `G:\steamlbirary\steamapps\common\Hearts of Iron IV\hoi4.exe`
- Native version: `Operation Postern v1.19.3.0.c01a (5632)`
- Isolated payload: `C:\Users\New\Documents\Paradox Interactive\Hearts of Iron IV\mod\ProjectUlysses_Continuation_native_20261018`
- Final isolated profile: `G:\Project-Ulysses-Continuation-native-test-20261018\userdir-native-final17-20261018`
- Launcher backup: `G:\Project-Ulysses-Continuation-native-test-20261018\launcher-settings.before.json`
- Restored launcher SHA-256: `1F51E45EA63AB69D6CEE85749AA9E500B385EB6A8EF372E5D7BA70215446547E`

## Compatibility work exercised

- Quarantined archive-only 1.14 unit/category/AI/technology overrides while preserving them under `inventory/inherited-legacy`.
- Added namespaced native compatibility definitions for the archive’s `ifv`, `imv`, and retained man-portable anti-tank contracts.
- Mapped archive-only history/equipment references to native 1.19 IDs, including mechanized infantry, armored cars, current armor, naval, air, and infantry technology identifiers.
- Hardened `tools/Port-NativeEquipmentReferences.py` to use whole-token, idempotent replacements after detecting a repeated `basic_light_tank` rewrite during controlled testing.
- Removed obsolete descriptor replace paths for quarantined legacy AI/unit schemas.

## Final native checkpoint

The mod activated and reached `[1991.01.01.12]` in the final17 profile. Fresh `error.log` filters reported:

| Filter | Count |
|---|---:|
| Invalid technology | 0 |
| Invalid module | 0 |
| Invalid unit category | 0 |
| Map/state load errors | 0 |
| Unexpected-token diagnostics | 26 |

The 26 parser diagnostics resolve to installed/base files (`common/doctrines/subdoctrines/sea/*`, `portraits/998_scientist_portraits.txt`, and `gfx/loadingscreens/load_7.dds`), not Ulysses-owned source paths. The exact HOI4 process was closed gracefully, no process remained, and the launcher-settings backup hash was restored.

## Controlled no-mod comparison

The no-mod profile `G:\Project-Ulysses-Continuation-native-test-20261018\userdir-native-baseline-20261018` reached `[1936.01.01.12]`. Its observed diagnostics were environment/base-game remote-file allocation exceptions; it produced no invalid-tech, invalid-module, invalid-category, map, or parser matches in the same targeted filters. This control separates the zero Ulysses-owned compatibility counts from general installation diagnostics; it does not make the entire installed-game log clean.

## Static checks

- `Test-UstioContinuity.py`: passed.
- `test_economy.py`: 27 tests passed.
- `Test-UlyssesStatic.ps1`: errors `0`; warnings remain for one placeholder-owned state, 204 placeholder strategic-region files, and the intentionally empty `map/positions.txt` without a vanilla reference root.
- `Validate-UlyssesReferences.ps1`: errors `0`; 666 focus definitions, 620 event definitions, 3,180 warnings, mostly missing localization.
- `Validate-UlyssesTechnologies.ps1`: errors `0`; one provenance/completeness warning.

## Boundaries

This checkpoint does not validate save/reload, bookmark selection, focus reachability, event reachability, economy on/off behavior in native runtime, representative AI, DLC permutations, or long-run continuity. Those remain the next acceptance gates. No downloaded mod code or executable was installed or run; only the local installed HOI4 executable was used in isolated native startup checks.
