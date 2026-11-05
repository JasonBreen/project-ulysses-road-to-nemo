# Belkan War continuation trace

This is a static control-flow trace from the preserved archive. It does not prove that the branch is reachable in-game.

## Current contract

The archive calls below are historical. Live Belkan outcome paths no longer schedule `world_event.2`. `belka_dlp_won.9`, `belka_wacht_am_wal.8`, and `belka_dlp_lost.7` call `ac_dispatch_belkan_war_outcome`, which fires `ac_continuation.1` only when `belka_won_belkan_war`, `belka_won_belkan_war_wacht_am_wal`, or `belka_lost_belkan_war` is already set. `belka_dlp_lost.7` sets the defeat flag only after `ac_postwar_wait_for_defeat_tree`. That glue is provisional gameplay. Native HOI4 reachability is untested.

## Established flow

- `common/national_focus/BLK_war_won.txt` starts the Belkan victory branch with `BLK_war_won`, whose completion fires `belka_dlp_won.1`.
- The postwar focus chain continues through celebration, demobilization, occupation, home-front, Ustio, Excalibur, and Rhongomyniad branches. `BLK_project_rhongomyniad` fires `belka_dlp_won.9` and then schedules `world_event.2`.
- `events/Belka.txt` also schedules `world_event.2` from several other Belkan outcome paths, including the Wacht am Wal branch and other victory/outcome branches. These calls establish that the popup was a shared endpoint, not evidence of a stopped game clock.
- `events/ac_world_events.txt` defines `world_event.2` as triggered-only. Its option now sets `ac_continuation_active`; no downstream consumer of that flag exists yet.

## Repairs made

- Removed the active Ustio call to `ustio_na.10`; the only definition in the archive is fully commented out and its option had no established effect.
- Removed the active `UST_guns_for_hire` mutual-exclusion references; the only focus definition is fully commented out, while the existing `UST_expand_militia_program` and `UST_national_army` focuses remain active.
- The reference validator now confirms zero unresolved owned focus or event references after these repairs.

## Explicit gaps

The archive does not establish the postwar countries, borders, diplomacy, or later-war content that should consume `ac_continuation_active`. Implementing those would require design direction rather than a mechanical repair. The next safe slice is to map existing victory flags and postwar focuses into a documented continuation contract, then add only transitions supported by existing content.

CI source protection: `tools/air_program/reviewed_outcome_updates.json` records the additive outcome dispatcher against current main, separately from the earlier shared campaign-commit receipt. Aviation and naval checks validate the chained digest, every existing effect AST, and the sole approved dispatcher; original captured manifests remain unchanged. Mutation checks reject existing-effect edits and unregistered additions even when a file digest is refreshed. These are offline checks, with native acceptance still pending.

The release lifecycle compiler also composes the four existing reviewed Belkan outcome hooks from PR #71 without recapturing `event_inputs.json`. Its independent validator removes only their exact approved AST suffixes before the original complete ordered comparison, retaining all settlement scopes, state transfers, option ownership, rewards, and once-only release guards. Missing, moved, duplicate, extra-reward and altered defeat-guard mutations remain rejected. The dormant-release inventory is regenerated from this actual source; its release contracts stay unchanged, with only the changed `Belka.txt` source fingerprint updated.
