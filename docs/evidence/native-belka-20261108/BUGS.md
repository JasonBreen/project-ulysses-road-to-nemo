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
unkeyed prose after otherwise complete quoted definitions. Reproduced on the
resumed 6636c641 launch, before advancing the clock. Removed exactly 14 orphan
rows; all 107 keyed definitions and the UTF-8 BOM remain. Added row-format
validation to the existing special-project check; the corrected source passes.
Repair d7cedf5c. Fresh c159a742 startup and opening reload produce zero invalid-key
or special-project localization errors. Native retest passed. No localization
wording or project effects changed.

## N003 — Major: starting grand-doctrine assignment failures

The first native mod startup repeatedly reports "set_grand_doctrine: Missing
grand doctrine or folder." Requires inspection against the installed 1.19.4.2
schema and native replay of corrected initialization.

Installed primary definitions are mixed, so a blanket addition/removal of new_
would be incorrect. The installed land definitions include new_mobile_warfare,
superior_firepower, grand_battleplan and mass_assault. Naval definitions are
new_fleet_in_being, new_convoy_raiding and new_base_strike; air definitions are
new_strategic_destruction, new_battlefield_support and new_operational_integrity.
Native replay of the saved 1991 opening at6636c641 confirms that land, naval and
air doctrine screens each show "No Grand Doctrine assigned". Before screenshots:
N003-land-doctrine-unassigned-before.png, N003-naval-doctrine-unassigned-before.png
and N003-air-doctrine-unassigned-before.png. Generator
owners include world_starts/compile.py, world_foundation/build.py and
anea/foundation.py, plus world_legacy/build.py. Source repaired through a shared
whole-token effect mapper, all four owners regenerated, and immutable captures
retained. Regression checks verify valid IDs, idempotence and preservation of
comments/strings and non-doctrine history data. Installed definition headers and
their actual folders were checked read-only. Repairs ba90080d and c159a742.
Fresh c159a742 Belka native start assigns Mobile Warfare, Fleet in Being and
Strategic Destruction. All three persist after native save/reload; zero missing
grand-doctrine assignment errors remain. Screenshots N003-land-doctrine-Mobile-
Warfare-after.png, N003-naval-doctrine-Fleet-in-Being-after.png,
N003-air-doctrine-Strategic-Destruction-after.png and
N003-doctrines-persist-after-reload.png. Initialization and reload retest passed;
longer continuity is blocked by the separate first-daily-rollover crash N006.

## N004 — Minor: overlapping scenario-selection panels

Observed during primary setup at3440x1440/scale1.0 on c6473167 before a country
was started. Reproduce: Single Player, New Game, inspect the first scenario.
Expected: distinct readable scenario panels. Observed: oversized navy panels
overlap the selection layout; the mouse selection controls remain usable.
Evidence: primary-scenario-overlap-before.png. Owning responsive frontend geometry
and bindings require investigation. Artwork replacement is not an authorized
remedy for this finding. Open, no repair or native retest claimed.

## N005 — Major presentation: placeholder panels and incorrect interface icons

Observed at1991.1.1.12 on c159a742, 3440x1440/scale1.0. Open infantry or industry
research and the land/naval/air doctrine screens. Large MOD PLACEHOLDER text
overlaps research trees and clips inside doctrine cards. Numerous construction
buttons and technology connectors show repeated shield icons instead of distinct
functional symbols. Expected readable panels and recognizable controls using
existing project artwork and appropriate functional graphics. Controls remain
usable through tooltips. Evidence: N005-infantry-research-presentation-before.png,
N005-industry-research-presentation-before.png and N003 doctrine after screenshots.
Owning visual-scrub bindings and generated artwork require inspection. Open;
no broad art replacement authorized and no native fix claimed.

## N006 — Critical: crash at first daily rollover

Primary human campaign, c159a742, observed1991.1.2.1 after advancing from the
preserved repaired opening. Before advancement: selected The Crisis Continues,
four research projects, two civilian-factory builds, one additional support-
equipment factory and24 rubber imports from Chopinburg. These choices were not
saved before the crash; the unmodified repaired opening remains available.
Expected ordinary progression through the first day. Observed process exit and
EXCEPTION_ACCESS_VIOLATION C0000005 at0x00007FF64C87CE38. Local crash bundle:
profiles/primary/crashes/hoi4_20261108_141037; raw logs archived under
evidence/logs/c159a742-first-daily-crash. Last error messages reference inherited
SEA_japan_news_events.03's invalid state995 controller and a base-game controller
trigger. Unchanged replay without management choices reproduced the same date and stack
offsets (second bundle hoi4_20261108_141440). Repair candidate8072d3fa adds events
directory isolation to all three descriptors and checks that all mod event calls
resolve inside its authored collection. Native repair retest passed: the same opening progressed to1991.1.6.7, was
saved/reloaded normally, and continued to1991.1.13.19 without a crash. The
previous SEA event/controller errors are absent. Screenshots N006-repair-through-
January-6.png and N006-repair-reload-through-January-13.png. This diagnostic did
not make campaign decisions. Individual event causality was not isolated;
no-mod first-day control remains outstanding. Full static wrapper passed8072d3fa.

## O001 — Observation: coal unavailable in the opening trade list

At1991.1.1.12, c159a742, Belka has a27 coal shortage and the coal supplier list is
empty. A separate construction coal shortage is also displayed. First daily
initialization has not completed because of N006. Inspect compatibility and
initialization before classifying this as a defect or changing resource geography.

## O002 — Observation: infantry upgrade reports1938

Improved Infantry Equipment I appears on the mod's1991 tree position but shows
1938 in its active research card, c159a742 at1991.1.1.12. Inspect the owning
technology declaration and chronology contract before changing dates. Open.

## N007 — Critical economy: fresh full-mode start has no state output

Fresh8072d3fa Belka at1991.1.1.12 and the separate unchanged-opening diagnostic
through1991.1.13.19 both show zero real/nominal GDP, treasury, debt and revenue,
with3.135 monthly obligations. Forecast refresh has no effect. Saved country
has initialized/schema flags and4200 seed GDP but no state real-output variables
or world-started flag. Expected existing fictional opening calibration to seed
state output once and create the opening account. Evidence: N007-zero-GDP-fresh-
start-8072d3fa.png and N007-zero-GDP-after-daily-init-and-refresh.png.

Investigation: the seed gate negates a scripted trigger using '= no', whereas
explicit NOT is required for reliable native inversion. Native logs also reject
'>='/'<=' shorthand in fiscal check_variable blocks. Repair in generator source
is in progress; fresh initialization, transactions and monthly/reload checks are
required before claiming the complete economy path fixed. Native6b350f17 fresh
initialization passed: real GDP4361.99998, cash87.23999 and debt1308.59999 in the
saved opening. Screenshot N007-opening-balances-after-6b350f17.png. Monthly
progression exposed the separate N008 guard failure. Previously initialized zero-output saves cannot
validate a one-time seed repair. No creative GDP calibration changes.

## N008 — Critical economy: monthly settlement guard reads the wrong scope

Primary human campaign6b350f17,1991.2.3.5: balances remain at their opening
values; last revenue, last bill, last settlement and settlement count are zero.
Native ledger explicitly shows no recorded accounts despite February arriving.
Reproduction: start full-mode Belka, advance normally across February1 and open
the fiscal overview/ledger. Save BLK_1991_02_03_05.hoi4 and screenshots
N008-first-month-without-settlement-6b350f17.png and
N008-ledger-empty-February-3-6b350f17.png remain in the disposable session.

The generator reads bare numeric `date` in country/state variable operations.
The installed engine's documentation/dynamic_variables_documentation.md assigns
date to global scope; events/BFTB_Bulgaria.txt uses global.date for a saved date.
Bare date resolves to an unset variable, so the settlement guard compares zero
with zero. Repair qualifies all settlement, state-cycle and allocation receipt
dates as global.date. The offline interpreter now rejects bare numeric date;
regression coverage checks generated syntax and duplicate settlement behavior.
Three focused settlement tests and14 ledger tests pass. Native replay and
save/reload acceptance remain pending. No financial calibration changes.

## N009 — Critical: crash while resuming after naval management

Primary human replay e7fd76f2, paused1991.1.20.2. Assigned Aayden Kreutzberg to
Hochseeflotte and ordered Naval Exercises through the mission button. Clicking
the clock to resume was followed by process exit. Crash bundle
hoi4_20261108_150749 reports E06D7363 at KERNELBASE RaiseException, distinct
from N006's access violation. Last error lines mention a missing
unit_imv_icon_small text icon and a non-44.1kHz blk_idle_008 sound; these are
observations, not an established cause. Logs archived locally under
evidence/logs/e7fd76f2-January20-fleet-crash. Managed January3.5 save remains
intact. An unchanged replay fromJan3.5, assigning the same admiral and exercise
mission, crashes immediately on resuming atJan3.5 (hoi4_20261108_151209), with
the same stack. The exception's catchable type in the local dump is
std::bad_optional_access. The mod's ocean, water_fjords, water_shallow_sea and
water_deep_ocean definitions lack minimum_seazone_dominance. The read-only
installed1.19.4.2 definitions contain250,100,100,250 respectively. This is the
next repair candidate, not a proven fix. A comparable case is documented by
[TNO's own tracker](https://github.com/TNODevs/TNO-Bug-Tracker/issues/5636);
that report is supporting context, not Ulysses runtime acceptance. The user
paused playtesting before any terrain changes were applied. No repair claimed.

## Static follow-up, 9 November 2026

Offline work on a separate branch (`claude/codex-work-fixes-ed7947`), with this
playtest branch merged onto current `main` (2b6610ac). HOI4 was not launched.
Every item below is a static repair or a static finding. None is a native
retest, and none changes the native status recorded above.

- **N009, repair applied, native retest pending.** Added
  `minimum_seazone_dominance` to the four sea terrains in
  `common/terrain/00_terrain.txt` with the installed 1.19.4.2 values: ocean 250,
  water_fjords 100, water_shallow_sea 100, water_deep_ocean 250. No other
  terrain value changed. `tools/Test-NativeCompatibilityContracts.py` now fails
  if a sea terrain, or a `naval_terrain` used by a strategic region, lacks the
  value. This is still the candidate named above, not a proven fix. Replay the
  fleet exercise from the Jan 3.5 managed save to confirm it.
- **N004, root cause found and repaired, native retest pending.** The visual
  scrub bound `GFX_select_date_1936` to `gfx/interface/ac_briefing/select_date.dds`,
  the 780x620 scenario-window background. The bookmark entry that draws it is
  232x211 with the picture at offset 27,28, so each of the two bookmarks drew a
  window-sized navy panel over the screen. The sprite now points at the
  archive's own 180x104 bookmark picture, `gfx/interface/select_date_1936.dds`.
  No artwork was created or replaced. The scrub check rejects a picture that
  overflows the entry.
- **N005, partly repaired, native retest pending.** Two causes were repaired.
  (1) Textures the engine draws behind controls (six technology-tab backgrounds
  and the doctrine/building panel) carried "MOD PLACEHOLDER" text and an
  outline. They are now plain navy. (2) The installed doctrine files request 134
  sprites and the scrub had bound only guessed grand-doctrine names, so 119
  still resolved to engine art; the Operations card photograph in the N003
  screenshots is one of them. All 134 now resolve inside the mod. See
  `docs/VANILLA_VISUAL_SCRUB.md` and `tools/visual_scrub/doctrine_sprites.json`.
  Not repaired: the repeated emblem tiles used as technology-tree connectors
  and the tab icons, which come from the earlier interface rebuild
  (`gfx/interface/ac_expansion/ui/GFX_techtree_line_*.dds`), and the doctrine
  window frame, which is engine chrome.
- **O001, cause identified, no change made.** 1.19 has a factory energy system:
  `ENERGY_RESOURCE = "coal"` in the installed defines, with a per-factory energy
  cost. The mod defines no coal anywhere in `common` or `history`, so every
  country starts with an energy deficit and nobody can export coal. The two
  ways out are a design decision for the owner: switch the energy cost off in
  mod defines (provisional gameplay), or place coal in states (resource
  geography, which needs a source decision under `docs/CANON_POLICY.md`).
- **O002, cause identified, no change made.** `infantry_weapons2` is no longer
  defined by the mod. The archive's `common/technologies/infantry.txt`,
  `armor.txt` and `artillery.txt` were removed in ee82591b (18 October 2026), so
  the installed files of those names load and bring their own years. The 1938
  shown on the card is the engine's value. Restoring mod-owned definitions for
  those three files belongs to issue #5 (technology naming) and issue #4 (1.19
  parity).
- **Review of the repairs recorded above.** `replace_path="events"` (N006), the
  `new_*` doctrine identifiers (N003), the `NOT`/`compare` trigger forms (N007)
  and `global.date` (N008) were read against the installed 1.19.4.2 files and
  merged unchanged. The full static wrapper passes on the merged tree.
- **N008, repair carried to the other date readers.** The session repaired the
  bare `date` operand only in the economy generator. Four other generators
  wrote the same form: `tools/reconstruction/build.py`,
  `tools/superpowers/build.py`, `tools/pacific_nations/build.py` and
  `tools/content_waves/framework.py` (372 operands in twelve generated files,
  for service start, elapsed and due dates). All now write `global.date`; the
  regenerated files differ from the previous ones by that qualifier and nothing
  else. Date triggers such as `date > 1990.12.31` are a different construct and
  are unchanged. Static only: none of these services has been run natively.
- **N003 and N007/N008, preserved-source receipts.** Checks outside the session
  still pinned the pre-repair text. `tools/air_program/reviewed_native_syntax_updates.json`
  now admits the respelled economy and reconstruction effects, and its
  validator proves that undoing the three respellings reproduces the previously
  admitted bytes. The replacement check follows the N003 history receipts in
  `tools/history_data_cleanup_updates.json`. The FATO check had admitted an
  earlier static change to unprefixed doctrine identifiers, which N003 showed
  assign nothing; that admission is retired and the history is back at its
  original capture.
- **N007, same form still present elsewhere, not changed.** The `>=` and `<=`
  `check_variable` shorthand that the native log rejected in the fiscal blocks
  is still written on 533 lines in 28 other files (FATO and South Belka, Anea,
  superpower programmes, factions, politics, minors). Whether the engine
  rejects it there too has not been observed, and the generators and
  hand-written files involved each have their own pinned receipts. Open.
