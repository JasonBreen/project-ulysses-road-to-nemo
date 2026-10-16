# Testing checklist

This is a test plan, not a report of passed tests. No runtime tests have been run or claimed.

## Static checks first

- [ ] Record archive, baseline, and working-copy hashes before edits.
- [ ] Compare the working copy against the immutable baseline and report intentional changes only.
- [ ] Parse braces and top-level blocks with a non-executing text checker.
- [ ] Check duplicate IDs for focuses, events, decisions, ideas, characters, technologies, states, and strategic regions.
- [ ] Check references to country tags, focus IDs, event IDs, scripted effects/triggers, technologies, equipment, GFX, sounds, and localization keys.
- [ ] Check dates, bookmark definitions, state ownership/core assignments, province membership, and map definitions.
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
- [ ] Repeat a representative run after every compatibility or map change.

## Evidence to retain

- Version/build metadata, mod descriptor hash, save names, logs, date checkpoints, branch/choice path, and a concise result for every checklist item.
- Never describe static inspection as runtime compatibility, and never treat a definition count as proof of reachability.
