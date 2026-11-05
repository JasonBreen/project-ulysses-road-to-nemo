# Native playtest checklist — Belkan campaign arc

This is a future, separately approved HOI4 test plan. It must be run in an
isolated local environment and recorded as native evidence. Do not infer a pass
from `Test-UlyssesStatic.ps1`, the campaign contract checker, or the path report.

Routes, conditions and console steps for each branch are in
[BELKAN_WAR_PLAYTEST_PLAN.md](BELKAN_WAR_PLAYTEST_PLAN.md).

## Launch and baseline

- [ ] Record HOI4 executable/build, descriptor hash, branch commit, DLC/rules, and clean save/playset context.
- [ ] Launch only the approved local continuation descriptor; do not enable the original archive or unrelated mods.
- [ ] Confirm the 1991 Belka bookmark loads without parser errors, missing localization, or missing focus-tree icons.
- [ ] Confirm the existing Belkan War event chain is unchanged before the new campaign handoff is exercised.

## Prewar preparation

- [ ] Complete `ac_belkan_prewar_briefing` and each of the three preparation branches.
- [ ] Confirm the ultimatum and council focuses become reachable in the intended order.
- [ ] Repeat the natural `belka.13.a` election swap before selecting `ac_belkan_prewar_briefing`, while it is in progress, and after completion. This is the sole scripted load of `belka_dlp_pre_war` and uses `keep_completed = yes`; the war-outcome handoff instead loads `ac_belkan_postwar`.
- [ ] Confirm the same briefing chain mounted on both prewar trees stays visible without duplicates or lost completion. Verify that `BLK_the_crisis_continues`, completed on the natural route but not remounted on the DLP tree, still satisfies the briefing prerequisite and that the inherited relative-position anchor renders correctly.
- [ ] Save/reload around the election swap, complete the remaining preparation chain, and confirm `ac_campaign_prepared` and `ac_belkan_war_council` remain reachable. The earlier missing-mount note was superseded by merged PR #65; this [static audit](NEXT_TASKS.md#dlp-election-tree-swap-and-briefing-continuity) does not establish a native pass.
- [ ] Confirm the War Council decision calls the existing `belka_dlp_war.1` chain exactly once.
- [ ] Save/reload before the war-start decision and verify the flags and focus progress persist.

## War progression and AI

- [ ] Exercise the military-economy and civilian-reserve choices separately.
- [ ] Verify economy effects occur only when `ac_econ_ready` is true and do not break the default-off economy rule.
- [ ] Exercise front command and endurance choices; verify each is one-shot and stage-ordered.
- [ ] Run an AI Belka or observer case long enough to verify weekly fallback events fire once per stage and do not spam.
- [ ] Record supply, equipment, stability, war support, and focus progression at 30/90/180 days.

## Outcome and postwar continuity

- [ ] Exercise conventional victory, Wacht am Wal, and defeat outcomes using controlled saves.
- [ ] Play Belka until one war outcome flag fires. Confirm `world_event.2` never fires, `ac_continuation.1` hands off once from that flag, and `ac_belkan_postwar` loads. Confirm `error.log` is clean of new handoff errors.
- [ ] Complete reconstruction, recovery budget, and demobilization focuses.
- [ ] Exercise victory and defeat settlement branches; confirm the unavailable branch remains gated.
- [ ] Complete both legacy outcomes and verify ideas, flags, stability, and economy state persist after save/reload.
- [ ] Confirm affected-country settlement hooks do not create unintended wars, ownership changes, or deadlocks.

## Long-run and evidence

- [ ] Advance to 1992 and 1995 checkpoints with AI on; inspect error.log, game.log, supply, diplomacy, and stalled focuses.
- [ ] Save/reload before and after each major branch.
- [ ] Record every failure with commit, save, event/focus/decision ID, log excerpt, and reproduction steps.
- [ ] Mark each result as native-pass, native-fail, or not exercised. Never report static validation as runtime success.
