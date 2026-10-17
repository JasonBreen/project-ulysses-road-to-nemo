# Original-content parity audit for the 1.19 continuation

This audit compares the immutable April 5, 2024 extraction at `G:\Project-Ulysses-Continuation\source\baseline\2985041246` with the isolated integrated 1.19 worktree at `G:\Project-Ulysses-Continuation-integration\mod\2985041246`. It is a static file/hash audit; it does not establish runtime parity.

## Packaging conclusion

The current repository is packaged as a standalone local mod wrapper: `2985041246.mod` points to the nested `mod/2985041246` directory, and the embedded descriptor has no `dependencies=` entry. It is not currently declared as a dependent submod. The 1.19 branch target remains `supported_version="1.19.*"`, but the installed executable metadata does not prove that semantic version.

## File-level inventory

| Classification | Count | Evidence and interpretation |
| --- | ---: | --- |
| Preserved byte-for-byte | 1,423 | Same relative path and SHA-256 as the immutable extraction. |
| Adapted in place | 1,505 | Same relative path exists but hash differs; includes the Claude 1.19 port, local repair commits, descriptor changes, content/localization adaptations, and integrated economy work. |
| Missing from original path | 176 | Classified below; missing does not automatically mean lost because some files were relocated or intentionally delegated to the game engine. |
| Added | 30 | New port, continuation, economy, validation, workspace, and documentation files. |

### Missing-file classification

- **Intentionally disabled for the no-vanilla-assets boundary — 156 graphics files.** The original aircraft module directory and four copied jet-technology icons were removed, along with 21 additional inherited exact copies found by the path-independent asset audit: six generic industry textures, one copied tile, three Osea generic navy portraits, one empty-leader texture, eight generic model texture files, and two Ustian infantry material maps. They are visible vanilla or placeholder assets, not Strangereal art. Custom aircraft-module aliases and technology definitions were retained where needed, but point explicitly to engine textures. No suitable original Strangereal replacements exist in the archive for the Osea or Ustian gaps; custom replacements require a separate art/design task.
- **Engine-fallback UI overrides disabled — 9 interface files.** These are generic/vanilla interface overrides removed by the Claude port or the asset repair. The mod does not replace them with broken placeholders; the base game is expected to provide those engine UI definitions. Runtime UI verification remains open.
- **Generic engine definitions disabled — 4 common files.** `common/buildings/00_buildings.txt`, `common/country_leader/00_traits.txt`, `common/technologies/land_doctrine.txt`, and `common/technologies/special_forces_doctrine.txt` contain generic HOI4 definitions and no identified Ulysses-specific namespace. They remain disabled to avoid copying vanilla gameplay definitions; base-game fallback is expected.
- **Relocated/adapted localization — 7 files.** The original English localization files were moved under `localisation/english/replace/` and renamed with `pu_` prefixes by the 1.19 port. Their content remains represented, but the path-level parity report correctly marks the original paths missing.

## Content-family status

- **Preserved:** map rasters/definitions, country histories, country definitions, focus/event families, country art, characters, equipment, and most localization content remain present or hash-adapted.
- **Adapted:** descriptors, interfaces, localization paths, technologies, histories, and selected map/building content were changed for the 1.19 port and continuation repairs. Two inherited armor AI date literals were corrected from `20001.1.1`/`1.1.1` to the evidence-supported `2001.1.1`/`1997.1.1`; the technology validator now rejects malformed or out-of-horizon dates without asserting authored coverage through 2065.
- **Disabled:** generic vanilla UI/gameplay overrides and copied aircraft art listed above.
- **Broken defects repaired:** four floating-harbor province associations (`11565`, `12098`, `11683`, `12493`) were mapped from their recorded coordinates to valid province IDs (`10388`, `10703`, `9582`, `10971`); four active `country_event = xxx` calls were removed; duplicate top-level `war_event.1` was renamed to `war_event.2`; and the new Belkan continuation localization was saved with a UTF-8 BOM.
- **Implemented but runtime-unverified:** `common/defines/ac_defines.lua` now sets the next-boundary `NDefines.NGame.END_DATE` to `2066.1.1.1`, intended to permit all of 2065-12-31; the static wrapper asserts this value.
- **Unverified:** parser compatibility, UI fallback behavior, DLC assumptions, focus reachability, event outcomes, AI, save/load stability, long-run campaign behavior, actual runtime acceptance of the 2065-12-31 boundary, meaningful authored content through 2065, and completeness of technology/equipment naming/localization. No HOI4 runtime was launched.

### Substantive remaining parity gaps

- The 156 intentionally removed graphics files have no archive-provided Strangereal replacements: 131 aircraft-module files, 4 copied jet-technology icons, 3 Osea generic navy portraits, 2 Ustian infantry material maps, 6 generic industry textures, 1 copied tile, 1 empty-leader texture, and 8 generic model textures. Engine fallback is expected only where an explicit engine path is documented; Osea and Ustian art remain open replacement tasks. UI/model behavior is not runtime-verified.
- The 50 custom aircraft-module aliases are retained in `interface/ac_plane_modules_icons.gfx` and currently map to 17 existing base-game icon paths by function. This is an explicit temporary fallback, not authored Strangereal art; replace it as a dedicated art task before any release-quality packaging.
- Nine generic/vanilla interface overrides and four generic common definitions remain disabled or delegated to the base game; this is a packaging choice, not proof that every downstream screen or rule behaves identically.
- Seven localization files are represented under adapted `localisation/english/replace/pu_*.yml` paths rather than their original archive paths.
- Placeholder art, leaders/advisors, and ship names remain; North Point's focus file is fully commented, Recta/Yuktobania lack dedicated focus files, Osea elections and Canon AI focuses contain unfinished content, and state 171 remains a `PLH` placeholder.
- The archive's 1991–2005 technology content is not yet a complete authored path to 2065; names, localization, dates, and later equipment provenance remain open work.

The parity requirement for future work is: preserve every original Ulysses content family, adapt only with a documented 1.19 reason, and distinguish engine fallback from lost content. Do not copy old files wholesale over newer compatible implementations.
