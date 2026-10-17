# 1.19 no-vanilla-assets policy

The 1.19 port must not ship copied vanilla HOI4 content or assets. This policy is about files delivered by the mod, not the game engine's normal ability to supply vanilla functionality when the mod does not replace it.

## Audit scope

- Candidate inspected: `G:\Project-Ulysses-Continuation\.claude\worktrees\playable-state-ace-combat-readme-73a736`
- Repair branch/worktree: `codex/1.19-no-vanilla-assets` at `G:\Project-Ulysses-Continuation-1.19-repair`
- Comparison baseline: verified `c72422d96f6bd9b33e61f725c2cdc8fe198a51d8` working copy
- Installed reference: `G:\steamlbirary\steamapps\common\Hearts of Iron IV`
- Audit method: SHA-256 comparison by relative path, with baseline comparison to distinguish inherited archive files from newly imported files

## Findings and repairs

The candidate contained 12 newly changed files that exactly matched installed HOI4 files: `common/units/equipment/convoys.txt`, `common/units/equipment/upgrades/air_upgrades.txt`, seven vanilla division-name files, and `map/cities.txt`, `map/colors.txt`, and `map/seasons.txt`. They were restored from the verified Ulysses working copy in the repair branch.

The candidate also changed the three existing Ulysses loading screens and added seven `_small.dds` files. The three full-size files were restored from the verified working copy; the seven unverified thumbnails were not carried into the repair branch. The 1.19 background-manager configuration now lists only the three existing mod textures. Thumbnail availability remains a runtime warning, not a claim of runtime compatibility.

The candidate's inherited exact-match count was **64**: 59 aircraft-module DDS files, 4 jet-technology DDS files, and 1 empty `map/positions.txt`. The current repair reports **1** inherited exact match, the retained engine/config `map/positions.txt`; the 63 visible copied-asset matches were removed, and the validator reports 0 new exact matches. This hash audit does not prove that a visually similar or version-mismatched derivative is absent; it proves the documented exact-match boundary only.

Remaining fallback dependencies are deliberate but runtime-unverified: the base game is expected to supply the aircraft-module UI after the copied module art/override was removed, the base technology UI after the four copied jet icon blocks were removed, and generic interface/common definitions that were disabled. The mod still delivers its remaining Ulysses/adapted art and definitions. The background manager depends on `gfx/loadingscreens/load_1.dds` through `load_3.dds`; their `_small.dds` picker thumbnails are absent and remain warnings.

The inherited exact matches were classified as follows:

| Count | Files | Purpose | Repair decision |
| ---: | --- | --- | --- |
| 59 | `gfx/interface/equipmentdesigner/planes/modules/*.dds` | Visible aircraft-module UI art; 58 were referenced by `plane_modules_icons.gfx`, one (`airplane_armor_plate_medium_icon.dds`) was unused | Removed the copied art and redundant override; the game engine supplies its own module UI. No suitable Strangereal replacements exist in the archive. |
| 4 | `gfx/interface/technologies/jet_{strategic,tactical}_bomber*.dds` | Visible technology-tree icons, all referenced by the mod’s sprite override | Removed the copied art and four override blocks; the game engine supplies the base definitions. No suitable Strangereal replacements exist in the archive. |
| 1 | `map/positions.txt` | Empty engine/config file; not visible, audio, or game-world art | Retained because it matches the installed game’s empty format and preserves the map contract. |

The candidate also changed the three existing Ulysses loading screens and added seven `_small.dds` files. The three full-size files were restored from the verified working copy; the seven unverified thumbnails were not carried into the repair branch. The 1.19 background-manager configuration now lists only the three existing mod textures. Thumbnail availability remains a runtime warning, not a claim of runtime compatibility.

## Regression check

Run from the repair worktree:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-NoVanillaAssets.ps1 `
  -ModRoot .\mod\2985041246 `
  -ReferenceGameRoot 'G:\steamlbirary\steamapps\common\Hearts of Iron IV' `
  -BaselineRoot 'G:\Project-Ulysses-Continuation\mod\2985041246' `
  -Json
```

The check fails on any exact installed-reference match that was not already present in the baseline, and now also fails if an inherited visible/audio asset remains. It allows the documented engine/config `map/positions.txt` match. It also checks 1.19 descriptors, absolute installed-game paths, and background-manager references. It does not prove that the game parses or runs the mod.
