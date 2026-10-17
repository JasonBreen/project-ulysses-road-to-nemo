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

The audit still reports 64 exact matches inherited from the original baseline, consisting of 63 interface/technology icon files and the empty `map/positions.txt`. These are recorded as inherited matches rather than silently deleted. They are not newly introduced by the 1.19 port.

## Regression check

Run from the repair worktree:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-NoVanillaAssets.ps1 `
  -ModRoot .\mod\2985041246 `
  -ReferenceGameRoot 'G:\steamlbirary\steamapps\common\Hearts of Iron IV' `
  -BaselineRoot 'G:\Project-Ulysses-Continuation\mod\2985041246' `
  -Json
```

The check fails on any exact installed-reference match that was not already present in the baseline. It also checks 1.19 descriptors, absolute installed-game paths, and background-manager references. It does not prove that the game parses or runs the mod.
