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
