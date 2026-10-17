# Testing checklist

This is a test plan, not a report of passed tests. No runtime tests have been run or claimed.

## Static checks first

- [ ] Record archive, baseline, and working-copy hashes before edits.
- [ ] Compare the working copy against the immutable baseline and report intentional changes only.
- [ ] Parse braces and top-level blocks with a non-executing text checker.
- [ ] Check duplicate IDs for focuses, events, decisions, ideas, characters, technologies, states, and strategic regions.
- [ ] Check references to country tags, focus IDs, event IDs, scripted effects/triggers, technologies, equipment, GFX, sounds, and localization keys.
- [ ] Check dates, bookmark definitions, state ownership/core assignments, province membership, and map definitions.
- [x] Validate all technology date literals and `start_year` values against the 1900–2065 static horizon; record inherited date repairs separately from authored content.
- [ ] Audit technology/equipment names and localization keys, classifying base-game inherited names, mod provenance, canon-backed names, and provisional gameplay abstractions.
- [ ] Check all `replace_path` targets and all absolute paths.

## Controlled runtime smoke tests (future, with separate approval)

- [ ] Launch only the approved local target branch with the local mod; capture the game/log version and command context.
- [ ] Load each Jan 1, 1991 bookmark.
- [ ] Confirm country selection, map render, focus tree render, basic diplomacy, and first-day tick.
- [ ] Advance 30 days and 180 days with AI on; inspect error logs and major country stability.
- [ ] Trigger a Belkan War opening and confirm focus/event/war/OOB continuity.
- [ ] Exercise Belka victory, Belka defeat, Rhongomyniad, Osea election, and Ustio/Sapin/Gebet branches where reachable.
- [ ] Save and reload before and after each major branch.

## Long-run behavior (future)

- [ ] Advance to 1992 and 1995 checkpoints with AI on; record deadlocks, runaway wars, supply collapse, and focus stalls.
- [ ] Exercise peace conferences, faction changes, occupation, capitulation, and state transfers.
- [ ] Exercise later technology gates and ensure 1991–2005 content does not unlock unexpectedly.
- [ ] Advance a controlled run through 2065-12-31 when runtime approval exists; separately report clock reachability, authored content coverage, and canon/provenance status.
- [ ] Verify Joker 1 content only against the compiled user-authored continuity source; do not treat it as official Project Aces canon.
- [ ] Repeat a representative run after every compatibility or map change.

## Evidence to retain

- Version/build metadata, mod descriptor hash, save names, logs, date checkpoints, branch/choice path, and a concise result for every checklist item.
- Never describe static inspection as runtime compatibility, and never treat a definition count as proof of reachability.
