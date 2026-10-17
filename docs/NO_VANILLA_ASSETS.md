# 1.19 no-vanilla-assets policy

The 1.19 port must not ship copied vanilla HOI4 content or assets. This policy is about files delivered by the mod, not the game engine's normal ability to supply vanilla functionality when the mod does not replace it.

## Audit scope

- Candidate inspected: PR #9 Claude baseline at `G:\Project-Ulysses-Continuation\.claude\worktrees\playable-state-ace-combat-readme-73a736`
- Isolated integration worktree: `G:\Project-Ulysses-Continuation-integration`
- Repair source retained separately at `G:\Project-Ulysses-Continuation-1.19-repair`; this integration does not modify that worktree.
- Comparison baseline for this repair: immutable April extraction at `G:\Project-Ulysses-Continuation\source\baseline\2985041246`
- The economy branch's separate ledger used the older frozen `c72422d96f6bd9b33e61f725c2cdc8fe198a51d8` working-copy baseline. That snapshot reported 13 inherited plaintext/config matches (12 also matched the April archive); it is not the current repair baseline.
- Installed reference: `G:\steamlbirary\steamapps\common\Hearts of Iron IV`
- Audit method: SHA-256 comparison by relative path, with baseline comparison to distinguish inherited archive files from newly imported files, plus a path-independent SHA-256 audit for visible/audio asset extensions. The latter uses file size only as a candidate prefilter, then compares full hashes.

## Findings and repairs

The candidate contained 12 newly changed files that exactly matched installed HOI4 files: `common/units/equipment/convoys.txt`, `common/units/equipment/upgrades/air_upgrades.txt`, seven vanilla division-name files, and `map/cities.txt`, `map/colors.txt`, and `map/seasons.txt`. They were restored from the verified Ulysses working copy in the repair branch.

The integrated port retains PR #9's seven full-size loading screens and seven `_small.dds` picker thumbnails because no exact installed-game match was found for them. The background-manager configuration lists `load_1.dds` through `load_7.dds`. Their presence is a packaging result, not proof that the loading-screen UI or runtime picker works; PR #9's loading-screen behavior remains author-reported evidence and was not reproduced locally in this integration pass.

The candidate's inherited exact-match count was **64**: 59 aircraft-module DDS files, 4 jet-technology DDS files, and 1 empty `map/positions.txt`. A second audit found **21 additional inherited visible/audio assets** whose filenames or directories differed from the installed reference, including generic industry/model textures, Osea navy portraits, the empty-leader texture, and Ustian infantry material maps. Those 21 files were removed after their references were either re-pointed to explicit engine paths, removed as unused, or documented as an art gap. The current repair reports **1** inherited exact path match, the retained engine/config `map/positions.txt`; it reports **0** new exact path matches and **0** path-independent exact asset matches. This hash audit does not prove that a visually similar or version-mismatched derivative is absent; it proves the documented exact-match boundary only.

Remaining fallback dependencies are deliberate but runtime-unverified: the base game is expected to supply the aircraft-module textures referenced by the restored custom aliases, the base technology UI after the four copied jet icon blocks were removed, the two technology-specialization tag textures, and generic interface/common definitions that were disabled. The mod still delivers its remaining Ulysses/adapted art and definitions. The background manager depends on `gfx/loadingscreens/load_1.dds` through `load_7.dds`; the integrated worktree retains their `_small.dds` picker thumbnails. Their picker/runtime behavior remains unverified.

The inherited exact matches were classified as follows:

| Count | Files | Purpose | Repair decision |
| ---: | --- | --- | --- |
| 59 | `gfx/interface/equipmentdesigner/planes/modules/*.dds` | Visible aircraft-module UI art; 58 were referenced by the historical module sprite file, one (`airplane_armor_plate_medium_icon.dds`) was unused | Removed the copied art; restored custom `GFX_EMI_*` aliases point explicitly to engine textures in `interface/plane_modules_icons.gfx`. No suitable Strangereal replacements exist in the archive. |
| 4 | `gfx/interface/technologies/jet_{strategic,tactical}_bomber*.dds` | Visible technology-tree icons, all referenced by the mod’s sprite override | Removed the copied art and four override blocks; the game engine supplies the base definitions. No suitable Strangereal replacements exist in the archive. |
| 1 | `map/positions.txt` | Empty engine/config file; not visible, audio, or game-world art | Retained because it matches the installed game’s empty format and preserves the map contract. |

The additional path-independent matches removed from the repair branch were:

| Count | Asset family | Repair decision |
| ---: | --- | --- |
| 6 | Generic industry technology textures | Re-pointed the icon definitions to explicit technology paths and removed the copied `industry/` textures. |
| 1 | `tiled_window_original.dds` | Removed as an unused exact copied tile. |
| 3 | Osea generic navy portraits | Removed the random portrait references; no archive-provided Strangereal replacement was silently substituted. |
| 1 | `portrait_empty_leader.dds` | Re-pointed the empty-leader definition to the explicit engine fallback `gfx/leaders/operative_unknown.dds`. |
| 8 | Generic building/map-object `nonormal.dds` and `nospec.dds` pairs | Re-pointed map-object definitions to explicit engine model paths and removed copied pairs. |
| 2 | Ustian infantry normal/spec material maps | Removed exact copied maps; custom Ustian mesh/diffuse assets remain, while replacement material-map art is an open design task. |

The remaining art gaps are therefore explicit decisions, not hidden vanilla fallbacks: Osea generic navy portrait art, Ustian material-map art, and the 50 custom aircraft-module icons need future Strangereal designs if those assets are required. Until then, the module aliases use 17 existing base-game icon paths grouped by function (radar, weapons, armor, and airframe category); this is a visible temporary fallback and remains runtime-unverified.

The integrated candidate keeps the seven PR #9 thumbnail files alongside the seven full-size loading screens. They are not exact installed-game matches in the static audit, but their picker/runtime behavior remains unverified.

## Regression check

Run from the repair worktree:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-NoVanillaAssets.ps1 `
  -ModRoot .\mod\2985041246 `
  -ReferenceGameRoot 'G:\steamlbirary\steamapps\common\Hearts of Iron IV' `
  -BaselineRoot 'G:\Project-Ulysses-Continuation\source\baseline\2985041246' `
  -Json
```

The check fails on any exact installed-reference match that was not already present in the baseline, fails if an inherited visible/audio asset remains even when it was renamed, and fails on missing or absolute installed-game references. It allows the documented engine/config `map/positions.txt` match. The isolated integration result is `InheritedVanillaMatches=1`, `NewVanillaMatches=0`, `PathIndependentVanillaMatches=0`, and `Warnings=0`. The one inherited match is the retained engine/config `map/positions.txt`; the seven loading thumbnails are present and therefore do not generate missing-thumbnail warnings. This does not prove that the game parses or runs the mod.
