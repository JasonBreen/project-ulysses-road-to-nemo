# Belkan War playtest plan

Plan for the first native HOI4 1.19.3 run that confirms the Belkan War and
postwar branches in `mod/2985041246` are reachable. It expands
[NATIVE_PLAYTEST_CHECKLIST.md](NATIVE_PLAYTEST_CHECKLIST.md) into concrete
routes, conditions and console steps for issue #8.

**Status: plan only.** Written from static reading of `main` at
`2a55a2f`. HOI4 was not launched. Per `AGENTS.md`, nothing here is run until
the owner approves an isolated native test. Every result below starts as
"not exercised".

## How to read this plan

- **Natural route**: what a player or AI does to reach the branch without
  cheats. A branch counts as *reachable* only when the natural route works.
- **Forced route**: console steps that jump to the branch so its downstream
  content can be checked quickly. A forced pass proves the content works, not
  that it is reachable. Record it as `native-pass (forced)`.
- **Check**: what to inspect before calling the step a pass.
- File references are relative to `mod/2985041246/`.

### Open PR #13 changes some of this

PR #13 (`codex/review-reconciliation`) is open and edits the same campaign
files. Where it changes a condition, the step shows **main** and **PR #13**
side by side. Test whichever head the owner approves, and record its SHA.

## 0. Preflight

1. Copy the approved commit into an isolated HOI4 user directory or playset
   that contains only this descriptor. Do not touch existing saves or settings.
2. Record: HOI4 build (1.19.3 checksum), DLC list, mod commit SHA, game rules,
   OS, and the playset contents.
3. Launch with `-debug` so the console and `error.log` are available, then
   open the console (`` ` `` or `~`).
4. **Confirm the console commands.** Run `help` and check that each command in
   the [cheat sheet](#console-cheat-sheet) exists in this build. Note any
   substitute before using it. The command names below are standard HOI4
   commands but were not checked against 1.19.3 here.
5. Clear `error.log`, start the 1991 Belka bookmark, pause on day one and save
   as `pt0_start`.
6. Pass: no parser errors from `ac_*` files, Belka focus tree shows both
   `BLK_the_crisis_continues` and the campaign opening, no missing icons or
   localisation keys on the campaign focuses.

Name every save `pt<step>_<short label>` so failures can be replayed.

## 1. Branch map

```
1991 start (belka_start tree)
├─ Crisis chain: BLK_the_crisis_continues ... → belka.12 → (35 days) → belka.13 election
│     └─ loads belka_dlp_pre_war (BLK_DLP tree, coup chain, Wacht counter)
└─ Campaign opening: ac_belkan_prewar_briefing → 3 preparations → ac_belkan_ultimatum
      → ac_belkan_council_mandate (flag ac_campaign_prepared)
         └─ decision ac_belkan_war_council → belka_dlp_war.1 → 60-day mission
War start: BLK_war_start_timer_dec timeout → war on UST/OSE/SAP/FAT/GEB/REC,
           flag belkan_war_is_happening, belka_dlp_war.2 loads war tree
├─ Campaign stages (player decisions or AI weekly fallback)
├─ Victory: BLK_force_osea_to_peace → belka_dlp_war.102 → won tree → Rhongomyniad → world_event.2
├─ South Belka split (south_belka.2/.3/.4) → belka_dlp_war.99
│   ├─ a) nuclear ending: 14-day mission → belka_dlp_war.100 → .101 → lost tree
│   └─ b) Wacht am Wal (needs counter = 5 and FAT/GEB/REC subjects) → wacht tree → hold 60 days → wacht.8 → world_event.2
└─ Defeat flag path: belka_dlp_war.103 (no caller found, see section 6)
Postwar: world_event.2 → ac_continuation.1 → one of four outcomes → ac_belkan_postwar tree + decisions
```

## 2. Prewar

### P1. Campaign opening focuses

- **Natural route.** Play Belka. Take `ac_belkan_prewar_briefing`, then
  `ac_belkan_industrial_mobilization`, `ac_belkan_logistics_network`,
  `ac_belkan_security_mandate`, then `ac_belkan_ultimatum`, then
  `ac_belkan_council_mandate`. Total cost 16.5 focus-weeks (about 116 days).
- **Conditions.** BLK, war not yet happening.
  - main: the briefing has no prerequisite and sits at the tree root.
  - PR #13: the briefing requires `BLK_the_crisis_continues`.
- **Check.** Events `ac_campaign.1` to `.6` fire once each. Ideas
  `ac_prewar_cabinet`, `ac_industrial_preparations`, `ac_frontline_logistics`,
  `ac_security_mandate` appear. Country flags `ac_campaign_started`,
  `ac_campaign_ultimatum_issued`, `ac_campaign_prepared` are set (check with
  `list_flags` while playing BLK; see the cheat sheet).
- **Forced route.** `focus.autocomplete`, then click each focus in order.
- **Risk to watch.** The crisis chain ends in `belka.13`, which loads
  `belka_dlp_pre_war` with `keep_completed = yes`. Any campaign focus not yet
  completed at that moment disappears with the old tree. Run this twice:
  once finishing the campaign opening first (expected pass), once leaving it
  half done when `belka.13` fires (record whether the council decision is
  stranded). Save `pt1_prepared` once `ac_campaign_prepared` is set.

### P2. DLP election and coup chain

- **Natural route.** Finish the crisis chain to `BLK_wait_for_profit` and its
  follow-up so `belka.12` fires; `belka.13` follows 35 days later.
- **Check.** `belka.13` sets fascism, flag `BLK_DLP_won_flag`, and loads the
  `BLK_DLP` tree. `BLK_pull_the_trigger` sets `BLK_wacht_am_wal_var = 0`.
- **Forced route.** `event belka.13 BLK`.
- Save `pt2_dlp` after the election. Most later branches start from this save.

## 3. War start

### W1. War Council start (campaign route)

- **Natural route.** From `pt1_prepared`, take decision
  `ac_belkan_war_council` (50 PP).
- **Conditions.** Flag `ac_campaign_prepared`; none of
  `belkan_war_is_happening`, `belka_won_belkan_war`, `belka_lost_belkan_war`,
  `belka_won_belkan_war_wacht_am_wal`.
- **Check.**
  1. Flags `ac_campaign_war_committed` (country) and `ac_campaign_arc_started`
     (global) set (`list_flags`); variable `ac_campaign_war_weeks = 0` (`get_var`).
  2. `belka_dlp_war.1` fires exactly once and starts mission
     `BLK_war_start_timer_dec` (60 days). `osea.75` fires for Osea.
  3. On timeout: wars on OSE, UST, SAP, FAT, GEB, REC; `belka_dlp_war.2`
     loads `belka_dlp_belkan_war`; mission `BLK_belkan_war_collapse` (player)
     or `BLK_belkan_war_collapse_AI` (AI) starts; global flag
     `belkan_war_is_happening` set; news `ac_news_event.7`.
- **Forced route.** `pp 100`, then click the decision; or skip the decision
  and run `event belka_dlp_war.1 BLK` (this skips the campaign flags, so it
  tests W2 instead).
- Run it both before and after the DLP election (`pt1_prepared` and
  `pt2_dlp`). Main lets the council fire before the election; record what the
  war tree looks like under a non-DLP government.
- Save `pt3_war_day1` the day the war starts.

### W2. Legacy start (`world_event.1`)

- **Natural route.** After 1995-01-15, the weekly on-action fires
  `world_event.1` for whoever controls state 358. If Belka exists and is
  fascist, it fires `belka_dlp_war.1`.
- **Check.** War starts the same way as W1, but `ac_campaign_war_committed` is
  not set, so the stage decisions in section 4 never appear and the weekly
  counter never runs. Record whether that is acceptable or a gap.
- Also check that W1 followed later by `world_event.1` does not restart the
  timer mission or fire `belka_dlp_war.1` twice.
- **Forced route.** `event world_event.1 BLK` from `pt2_dlp`.

## 4. War stages

All from `pt3_war_day1` with Belka played by a human.

| Stage | Decisions (one per stage) | Event | Flag and idea |
| --- | --- | --- | --- |
| 1 | `ac_belkan_logistics_requisition` or `ac_belkan_civilian_reserve` | `ac_campaign.20` / `.21` | `ac_campaign_stage_one` plus `ac_war_supply_drive` or `ac_war_civilian_reserve` |
| 2 | `ac_belkan_front_command` | `ac_campaign.22` | `ac_campaign_stage_two`, `ac_war_front_command` |
| 3 | `ac_belkan_endurance_program` | `ac_campaign.23` | `ac_campaign_stage_three`, `ac_war_endurance` |

- **Check.** Each decision appears only after the previous stage flag. Take
  military economy in one run and civilian reserve in another; confirm the
  other stage-one decision disappears. Economy effects apply only when
  `ac_econ_ready` is true. No idea is added twice.
- main: both stage-one decisions can be taken at once; record if that
  happens. PR #13 blocks the sibling with a pending flag.

### W4. AI fallback

- Run Belka as AI from a separate prewar save, switching away (`observe`,
  or `tag OSE`) before the 60-day `BLK_war_start_timer_dec` mission expires.
  Its timeout checks `is_ai` once: it schedules the AI-only events below and
  picks the player or AI collapse mission. A save made after the war starts
  under human control keeps the player mission and lacks the AI events, so
  it cannot test this step.
- main: fallback events fire after more than 6, 12 and 20 war-weeks.
- PR #13: more than 18 weeks for stage one, then 22 and 26 weeks with the
  counter reset each stage.
- **Check.** Each fallback event fires once; no spam once the stage flag is
  set. Record dates and the war state at 30, 90 and 180 days (supply,
  equipment, stability, war support).
- Also note the legacy AI timers that run in parallel: `belka_dlp_war.5`
  (Excalibur, day 90), `belka_dlp_war.106` (day 270),
  `BLK_belkan_war_collapse_AI` (day 450 → `belka_dlp_war.105`).

## 5. Outcomes

### O1. Conventional victory and Rhongomyniad

- **Natural route.** Decision `BLK_force_osea_to_peace` becomes available when
  Belka controls the heartland, south, north and Ustio state sets in
  `common/scripted_triggers/ac_BLK_scripted_triggers.txt`, with UST
  capitulated and FAT, GEB, REC as Belkan puppets.
- **Chain.** `belka_dlp_war.102` (annex UST, white peace, flag
  `belka_won_belkan_war`) → `belka_dlp_war.104` loads `belka_belkan_war_won` →
  `BLK_war_won` fires `belka_dlp_won.1` → ... → `BLK_project_rhongomyniad`
  fires `belka_dlp_won.9` → `world_event.2` → `ac_continuation.1` option a.
- **Forced route.** From `pt3_war_day1`: `event belka_dlp_war.102 BLK`, then
  `focus.autocomplete` through the won tree. To test the decision itself, use
  a state-control command (for example `occupy`, confirm in preflight) on the
  listed states. The north set also needs FAT, GEB and REC as puppets, and
  the Ustio set needs UST capitulated, so record how much of this the forced
  setup had to fake.
- **Check.** The won tree loads once; Rhongomyniad branch completes;
  `world_event.2` fires once; postwar outcome is "victory" (section 7).
- Save `pt5_o1_won_tree` and `pt5_o1_handoff`.

### O2. South Belka split

Three triggers lead to the same follow-up `belka_dlp_war.99`:

| Event | Condition |
| --- | --- |
| `south_belka.2` | Player Belka, at war with OSE, surrender progress above 20% (weekly) |
| `south_belka.3` | Player mission `BLK_belkan_war_collapse` times out (180 days, extended by `BLK_use_locals`) |
| `south_belka.4` | AI Belka at war with OSE, and either collapse flag plus surrender above 25%, or surrender above 15% without states 302 and 364 |

- **Check.** SBK receives states 330, 369, 302, 8, 364 and part of the army;
  `south_belka.1` adds SBK to Osea's faction (`.4` does this directly);
  `belka_dlp_war.99` fires the next day with option a always shown and option
  b only when Wacht am Wal is possible.
- **Forced route.** `event south_belka.3 BLK`.
- Save `pt5_o2_split` on the `belka_dlp_war.99` popup; O3 and O4 both start
  here.

### O3. Nuclear ending (option a)

- **Chain.** `BLK_cook_nukes_timer_dec` (14 days) → `belka_dlp_war.100`
  (nuclear strikes) → `belka_dlp_war.101` (white peace, puppets released,
  states to SBK/GEB/REC/FAT, loads `belka_belkan_war_lost`).
  - main: `.101` also fires `world_event.2` the next day.
  - PR #13: `.101` sets `ac_postwar_wait_for_defeat_tree`; `world_event.2`
    waits for `belka_dlp_lost.7` at the end of the lost tree.
- **Check on main.** Watch for the postwar tree replacing
  `belka_belkan_war_lost` about two days after it loads, before the player can
  take `BLK_war_lost`. If that happens, record it as a native fail matching
  the PR #13 finding.
- **Check on PR #13.** The lost tree stays; complete it with
  `focus.autocomplete` up to the Return of the King (`belka_dlp_lost.7`), then
  confirm `world_event.2` fires once.
- **Outcome.** Either way `belka_lost_belkan_war` is not set, so
  `ac_continuation.1` takes option d (unclassified). Confirm which option
  actually shows.

### O4. Wacht am Wal (option b)

- **Natural route.** In the DLP coup chain take the options that add to
  `BLK_wacht_am_wal_var`: `belka_dlp_coup.8` b, `.9` b, `.10` a (counter 3 by
  war start, which schedules `belka_dlp_coup.14` 95 days after the war
  begins), then `.14` b and `.15` a (counter 5). Keep FAT, GEB, REC as
  subjects. Reach O2 and pick option b.
- **Chain.** `belka_wacht_am_wal.1` → `.2` (global flag
  `wacht_am_wal_is_happening`, loads `belka_wach_am_wal`, check in 75 days) →
  complete the plan focuses and `BLK_to_hold_the_line` (needs
  `BLK_wacht_am_wall_state_control`) → mission
  `BLK_wacht_am_wal_hold_timer` (60 days).
  - Timeout while holding: `.6` → `.8` (white peace with SAP, OSE, UST; flag
    `belka_won_belkan_war_wacht_am_wal`) → `world_event.2` → option b.
  - Losing a held state cancels the mission: `.7` adds
    `BLK_last_order_lost_hope`. No scripted ending follows; record how the war
    ends and which postwar option (if any) appears.
  - Skipping plan focuses for 75 days: `.4` failure event.
  - SBK surrender above 50% after `BLK_plan_oberon`: `south_belka.5`, Belka
    annexes SBK.
- **Forced route.** Option b also needs FAT, GEB and REC to be subjects of
  Belka, which `event south_belka.3 BLK` from `pt3_war_day1` does not set up.
  Start from a save where they were puppeted in play (or puppet them with a
  console command confirmed in preflight). Then run
  `set_var BLK_wacht_am_wal_var 5` if the build has it, otherwise replay the
  coup options, and run `event belka_dlp_war.99 BLK` and pick b. Confirm
  with `get_var` that the counter is 5 before firing `.99`.
- Save `pt5_o4_wacht_start` and `pt5_o4_handoff`.

### O5. Defeat flag (forced only)

`belka_lost_belkan_war` is set only by `belka_dlp_war.103`, and no event,
focus, decision or on-action fires `.103` (static search of `common/` and
`events/`). This means option c of `ac_continuation.1`, the defeat settlement
focus and decision, and the Osean guarantor event `ac_continuation.11` look
unreachable in normal play. Confirm in game, then test the content:

- **Forced route.** From `pt3_war_day1`: `event belka_dlp_war.103 BLK`, then
  `event world_event.2 BLK`.
- **Check.** White peace, state transfers, option c shows, OSE gets
  `ac_postwar_guarantor` and `ac_continuation.11` after 7 days.
- Record as `native-pass (forced)` at best; reachability stays open.

### O6. Unclassified fallback

Reached naturally by O3; use the post-`belka_dlp_war.101` save for postwar
continuity. Forcing it from `pt3_war_day1` with `event world_event.2 BLK`
only checks that option d shows. The war is still running and
`belkan_war_is_happening` is still set, so the collapse mission can fire the
South Belka split over the postwar tree. Do not count anything downstream of
that forced run as a postwar pass.

## 6. Static findings to confirm in game

| # | Finding | Where | Affects |
| --- | --- | --- | --- |
| 1 | `belka_dlp_war.103` has no caller, so the defeat outcome flag is never set naturally | `events/Belka.txt`, `events/ac_continuation.txt` | O5, defeat postwar branch |
| 2 | On main, the nuclear ending fires `world_event.2` right after loading the lost tree, and the postwar tree replaces it | `events/Belka.txt` (`belka_dlp_war.101`) | O3; fixed by PR #13 |
| 3 | Uncompleted campaign opening focuses vanish when `belka.13` loads the DLP tree | `events/Belka.txt` (`belka.13`), `common/national_focus/BLK.txt` | P1 |
| 4 | The legacy war start (`world_event.1`, 1995+) skips the campaign stage decisions | `events/ac_world_events.txt`, `common/decisions/ac_belkan_campaign.txt` | W2 |
| 5 | Wacht am Wal failure (`belka_wacht_am_wal.7`) has no scripted ending | `events/Belka.txt` | O4 |
| 6 | `world_event.2` is `fire_only_once` and `ac_continuation.1` is blocked once the contract starts, so only the first ending reaches the postwar tree | `events/ac_world_events.txt`, `events/ac_continuation.txt` | all outcomes |

These are read from the scripts, not observed in game. Each needs a native
result before anyone changes the code.

## 7. Postwar (run once per outcome reached)

From each handoff save (`pt5_o1_handoff`, O3, `pt5_o4_handoff`, O5, O6):

1. `world_event.2` sets `ac_continuation_active`; `ac_continuation.1` shows
   only the option matching the outcome flag; global flag
   `ac_postwar_contract_started` and country flag `ac_postwar_ready` are set;
   `ac_belkan_postwar` loads.
2. Focus chain: `ac_postwar_reconstruction` → `ac_postwar_recovery_budget`
   (fires `ac_continuation.2`, one factory) → `ac_postwar_demobilization`.
   Then only the matching settlement is available:
   victory and Wacht → `ac_postwar_victory_settlement` → legacy;
   unclassified → `ac_postwar_unclassified_settlement` → legacy;
   defeat → `ac_postwar_defeat_settlement` → legacy. The defeat settlement
   needs only `ac_postwar_recovery_budget`, not demobilization, so check it
   right after the recovery budget and record whether that earlier opening
   is intended.
   The other two settlement focuses stay locked.
3. Decisions: `ac_postwar_reconstruction_program`, then
   `ac_postwar_demobilization` and, for victory or Wacht,
   `ac_postwar_ratify_victory`. On defeat, `ac_postwar_political_settlement`
   needs only `ac_postwar_ready`, so check it on the handoff day, before
   reconstruction, and record whether it running in parallel is intended.
   Each decision fires once.
4. Affected countries: on victory or Wacht, FAT, GEB, REC get
   `ac_postwar_occupation_burden`, `ac_continuation.10` after 7 days, and the
   `ac_postwar_local_recovery` decision. Switch with `tag FAT` and take it.
   No new wars, ownership changes or deadlocks.
5. Save and reload after the handoff and after the legacy focus. Flags, ideas
   and focus progress persist.

## 8. Long run and AI observer

- From `pt0_start`, `observe` with all AI to 1992-01-01 and 1995-01-01. Record
  whether AI Belka takes the campaign opening, starts the war, which outcome
  it reaches, and whether the postwar tree loads.
- At each checkpoint: save, reload, scan `error.log` and `game.log`, note
  stalled focuses, supply, and diplomacy.

## Console cheat sheet

Confirm each in preflight; mark missing ones in the run log.

| Command | Use here |
| --- | --- |
| `tag BLK` / `tag FAT` | Switch country |
| `observe` | AI-only run |
| `event <id> BLK` | Fire an event for Belka |
| `focus.autocomplete` | Focuses complete instantly |
| `pp <n>` | Afford decisions |
| `debug_mode` | Show IDs and object data on hover (not flags or variables) |
| `list_flags` | List active flags; run while playing BLK for country flags |
| `get_var <var>` / `list_vars` | Read `ac_campaign_war_weeks`, `BLK_wacht_am_wal_var` |
| `set_var <var> <value>` | Set the Wacht counter (may not exist) |
| `occupy` or equivalent | Force state control for O1 (name unverified) |
| `help` | List commands available in this build |

## Recording each result

For every step record: step ID, head SHA, natural or forced, save name,
date in game, result (`native-pass`, `native-pass (forced)`, `native-fail`,
`not exercised`), and for failures the event/focus/decision ID, `error.log`
excerpt and steps to reproduce. Never record a static check as a runtime
pass.
