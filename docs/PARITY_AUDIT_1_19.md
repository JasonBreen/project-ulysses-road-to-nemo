# Original-content parity audit for the 1.19 continuation

This audit compares the immutable April 5, 2024 extraction at `G:\Project-Ulysses-Continuation\source\baseline\2985041246` with the repaired 1.19 worktree at `G:\Project-Ulysses-Continuation-1.19-repair\mod\2985041246`. It is a static file/hash audit; it does not establish runtime parity.

## Packaging conclusion

The current repository is packaged as a standalone local mod wrapper: `2985041246.mod` points to the nested `mod/2985041246` directory, and the embedded descriptor has no `dependencies=` entry. It is not currently declared as a dependent submod. The 1.19 branch target remains `supported_version="1.19.*"`, but the installed executable metadata does not prove that semantic version.

## File-level inventory

| Classification | Count | Evidence and interpretation |
| --- | ---: | --- |
| Preserved byte-for-byte | 1,452 | Same relative path and SHA-256 as the immutable extraction. |
| Adapted in place | 1,495 | Same relative path exists but hash differs; includes the Claude 1.19 port, prior Ulysses repairs, descriptor changes, and content/localization adaptations. |
| Missing from original path | 157 | Classified below; missing does not automatically mean lost because some files were relocated or intentionally delegated to the game engine. |
| Added | 10 | New repair/continuation files, including validation and documentation. |

### Missing-file classification

- **Intentionally disabled for the no-vanilla-assets boundary — 135 graphics files.** The original aircraft module directory and four copied jet-technology icons were removed. They are visible vanilla UI assets, not Strangereal art. The redundant module sprite override and four technology sprite blocks were removed with them so the engine can provide its own definitions. No suitable original Strangereal replacements exist in the archive; custom replacements require a separate art/design task.
- **Engine-fallback UI overrides disabled — 11 interface files.** These are generic/vanilla interface overrides removed by the Claude port or the asset repair. The mod does not replace them with broken placeholders; the base game is expected to provide those engine UI definitions. Runtime UI verification remains open.
- **Generic engine definitions disabled — 4 common files.** `common/buildings/00_buildings.txt`, `common/country_leader/00_traits.txt`, `common/technologies/land_doctrine.txt`, and `common/technologies/special_forces_doctrine.txt` contain generic HOI4 definitions and no identified Ulysses-specific namespace. They remain disabled to avoid copying vanilla gameplay definitions; base-game fallback is expected.
- **Relocated/adapted localization — 7 files.** The original English localization files were moved under `localisation/english/replace/` and renamed with `pu_` prefixes by the 1.19 port. Their content remains represented, but the path-level parity report correctly marks the original paths missing.

## Content-family status

- **Preserved:** map rasters/definitions, country histories, country definitions, focus/event families, country art, characters, equipment, and most localization content remain present or hash-adapted.
- **Adapted:** descriptors, interfaces, localization paths, technologies, histories, and selected map/building content were changed for the 1.19 port and continuation repairs. Two inherited armor AI date literals were corrected from `20001.1.1`/`1.1.1` to the evidence-supported `2001.1.1`/`1997.1.1`; the technology validator now rejects malformed or out-of-horizon dates without asserting authored coverage through 2065.
- **Disabled:** generic vanilla UI/gameplay overrides and copied aircraft art listed above.
- **Broken defects repaired:** four floating-harbor province associations (`11565`, `12098`, `11683`, `12493`) were mapped from their recorded coordinates to valid province IDs (`10388`, `10703`, `9582`, `10971`); four active `country_event = xxx` calls were removed; duplicate top-level `war_event.1` was renamed to `war_event.2`; and the new Belkan continuation localization was saved with a UTF-8 BOM.
- **Unverified:** parser compatibility, UI fallback behavior, DLC assumptions, focus reachability, event outcomes, AI, save/load stability, and long-run campaign behavior. No HOI4 runtime was launched.
- **Implemented but runtime-unverified:** `common/defines/ac_defines.lua` now sets the next-boundary `NDefines.NGame.END_DATE` to `2066.1.1.1`, intended to permit all of 2065-12-31; the static wrapper asserts this value.
- **Unverified:** parser compatibility, UI fallback behavior, DLC assumptions, focus reachability, event outcomes, AI, save/load stability, long-run campaign behavior, actual runtime acceptance of the 2065-12-31 boundary, meaningful authored content through 2065, and completeness of technology/equipment naming/localization. No HOI4 runtime was launched.

The parity requirement for future work is: preserve every original Ulysses content family, adapt only with a documented 1.19 reason, and distinguish engine fallback from lost content. Do not copy old files wholesale over newer compatible implementations.
