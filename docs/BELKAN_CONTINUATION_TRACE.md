# Belkan War continuation trace

This is a static control-flow trace from the preserved archive. It does not prove that the branch is reachable in-game.

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
