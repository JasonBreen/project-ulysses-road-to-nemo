# Native bug ledger

## N001 — Major: original animated globe replaced with a placeholder

Observed on the primary native main menu at 3440x1440/scale1.0, payload c6473167.
The menu showed a large "MOD PLACEHOLDER / MAIN MENU" panel instead of the
original globe, with black uncovered viewport area. The scenario background also
showed overlapping panels; that is a separate presentation finding.

Root cause: the prior frontend repair replaced the archive's 35 animated tile
containers with one fallback canvas, and commit55c90935's visual-scrub generator
overwrote the archived fallback image. Owner explicitly requested globe restoration.
Recovered the exact archive fallback and layout; verified all35 animated textures
against preserved baseline hashes; stopped placeholder generation for this asset
and added preservation/rebuild regressions. Repairs: 08b156fe and 6636c641.
Native retest passed at 6636c641: the original globe renders and rotates across
separate captured frames; no frontend_background lookup warning remains. The
full static wrapper with installed reference and preserved baseline passed.
Preservation audit at 18:11:32 UTC: 838 protected files unchanged, zero additions.
Evidence in the local session: primary-main-menu-before.png,
restored-globe-frame-a.png, restored-globe-frame-b.png and
restored-globe-final-native.png. Scenario overlap remains a separate open finding.

## N002 — Minor: malformed special-project localization

The first native mod startup reports an invalid key at line5 of
localisation/english/ac_special_projects_l_english.yml. Source contains orphaned
unkeyed prose after otherwise complete quoted definitions. Not repaired yet.

## N003 — Major: starting grand-doctrine assignment failures

The first native mod startup repeatedly reports "set_grand_doctrine: Missing
grand doctrine or folder." Requires inspection against the installed 1.19.4.2
schema and native replay of corrected initialization. Not repaired yet.

Installed primary definitions are mixed, so a blanket addition/removal of new_
would be incorrect. The installed land definitions include new_mobile_warfare,
superior_firepower, grand_battleplan and mass_assault. Naval definitions are
new_fleet_in_being, new_convoy_raiding and new_base_strike; air definitions are
new_strategic_destruction, new_battlefield_support and new_operational_integrity.
The native errors establish failed assignments; the doctrine UI still needs
inspection before claiming the extent of missing starting bonuses. Generator
owners include world_starts/compile.py, world_foundation/build.py and
anea/foundation.py; preserve their source captures and provenance receipts.

## N004 — Minor: overlapping scenario-selection panels

Observed during primary setup at3440x1440/scale1.0 on c6473167 before a country
was started. Reproduce: Single Player, New Game, inspect the first scenario.
Expected: distinct readable scenario panels. Observed: oversized navy panels
overlap the selection layout; the mouse selection controls remain usable.
Evidence: primary-scenario-overlap-before.png. Owning responsive frontend geometry
and bindings require investigation. Artwork replacement is not an authorized
remedy for this finding. Open, no repair or native retest claimed.

Each entry will record severity, scenario/date/revision, reproduction, expected and
observed behavior, owning IDs, evidence, repair commit and native retest status.
