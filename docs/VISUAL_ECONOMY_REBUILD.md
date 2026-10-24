# Remove vanilla visuals and rebuild economic management

Working branch: `codex/remove-vanilla-visuals-economy-rebuild`.

## Changes

- Focus artwork is now explicitly resolved to the existing Project Ulysses
  Strangereal textures across every authored focus tree. 387 explicit vanilla
  icon references in Belka, Osea, Sapin, Gebet, Ustio, and the generic tree
  were replaced. All 170 focus sprites in `ac_goals.gfx` resolve to committed
  mod art files. This is temporary art reuse where a unique new icon is unavailable,
  not an endorsement of generic repeated artwork as final.
- The old country politics-tab economy popup was removed. Its MILS/CIVS/DOCKS
  status panel is replaced by an independently opened HUD-anchored fiscal
  directorate with Overview / Budget / Credit pages. Numeric fields use live
  `ac_econ_` variables. Buttons call the existing protected economy effects;
  no new money model or GDP values were invented.
- The legacy economy decision category is hidden, while the decision scripts
  remain available to the offline behavioral harness until refactored.
- 170 module sprite definitions and five technology art paths were redirected
  from vanilla engine textures to packaged Ulysses art.

## What remains unresolved

The old no-vanilla hash audit never checked references to engine-owned
art. Direct paths are still present in large inherited files, including the
technology database, research view and unit counters; the aircraft role and
eight-frame niche strips also require appropriately framed custom sprites.
Those need dedicated, visually faithful replacements and native testing,
rather than indiscriminately repointing every GUI control and animated strip to
one unrelated image.

**Not a completed no-vanilla-visuals certification.** Run
`python tools/audit_visual_dependencies.py --json` for an accurate source
inventory, and use `--strict-all` to fail until no authored interface GFX
entry resolves outside the mod. This strict-all gate is not yet passing.

## Validation scope

The standard static runner checks that all national-focus icons and all new
economy dashboard sprites resolve to packaged art, that the old country-tab
panel is gone, and that all fiscal UI actions are bound. That does not test
layout at different resolutions, UI frame counts, HOI4 parser acceptance,
save/reload, or any native graphical rendering. No user playsets, saves,
baselines, or installed games are edited by this branch.
