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
and added preservation/rebuild regressions. Native restoration retest pending.
Evidence: primary-main-menu-before.png and primary-scenario-overlap-before.png.

## N002 — Minor: malformed special-project localization

The first native mod startup reports an invalid key at line5 of
localisation/english/ac_special_projects_l_english.yml. Source contains orphaned
unkeyed prose after otherwise complete quoted definitions. Not repaired yet.

## N003 — Major: starting grand-doctrine assignment failures

The first native mod startup repeatedly reports "set_grand_doctrine: Missing
grand doctrine or folder." Requires inspection against the installed 1.19.4.2
schema and native replay of corrected initialization. Not repaired yet.

Each entry will record severity, scenario/date/revision, reproduction, expected and
observed behavior, owning IDs, evidence, repair commit and native retest status.
