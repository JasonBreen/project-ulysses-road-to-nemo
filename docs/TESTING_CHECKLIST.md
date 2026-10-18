# Testing checklist

Runtime results are recorded inline with dates. Static inspection is never counted as a runtime result.

## Current campaign branch status

The Belkan campaign-arc branch has not been launched or playtested in HOI4 in
this task. Its evidence is limited to offline static contract, path-reference,
repository, economy, and no-vanilla checks. The checklist below is the required
native handoff, not a claim that any item has passed on this branch.

## Runtime results — 2026-10-17, HOI4 1.19.3 (Operation Postern), mod 0.3-dev, debug mode, mod enabled alone

- [x] Main menu loads and stays stable (no GPU device-removed crash) — original Project Ulysses menu.
- [x] Jan 1, 1991 bookmark selectable; country select renders (original layout).
- [x] Belka campaign starts (map loads after the weather/spawn-point/rivers fixes) and runs to Feb 1992 at speed 5 with AI on, no crash.
- [x] Research panel incl. Experimental Facilities tab, tech-tree tabs, government view, decisions panel, national focus tree + continuous focuses open and render.
- [ ] Save/reload, other nations, Belkan War trigger, branch outcomes — not yet exercised.

Logs from these runs were kept outside the repo (scratchpad); counts are summarized in [PORT_1_19.md](PORT_1_19.md).

## Static checks first

- [ ] Record archive, baseline, and working-copy hashes before edits.
- [ ] Compare the working copy against the immutable baseline and report intentional changes only.
- [ ] Parse braces and top-level blocks with a non-executing text checker.
- [ ] Check duplicate IDs for focuses, events, decisions, ideas, characters, technologies, states, and strategic regions.
- [ ] Check references to country tags, focus IDs, event IDs, scripted effects/triggers, technologies, equipment, GFX, sounds, and localization keys.
- [ ] Check dates, bookmark definitions, state ownership/core assignments, province membership, and map definitions.
- [ ] Check all `replace_path` targets and all absolute paths.
- [x] Validate all technology date literals and `start_year` values against the 1900–2065 static horizon; record inherited date repairs separately from authored content.
- [ ] Audit technology/equipment names and localization keys, classifying base-game inherited names, mod provenance, canon-backed names, and provisional gameplay abstractions.
- [ ] Advance a controlled run through 2065-12-31; separately report clock reachability, authored content coverage, and canon/provenance status.
- [ ] Verify Joker 1 content only against the compiled user-authored continuity source; do not treat it as official Project Aces canon.

Static checks are automated by `tools/Test-UlyssesStatic.ps1` (CI: `.github/workflows/static-validation.yml`); see [VALIDATION.md](VALIDATION.md).

## Controlled runtime smoke tests (future, with separate approval)

- [x] Launch only the approved local target branch with the local mod; capture the game/log version and command context. (1.19.3, `hoi4.exe -gdpr-compliant -debug_mode`, `dlc_load.json` = dev descriptor only, restored afterwards)
- [~] Load each Jan 1, 1991 bookmark. (first bookmark verified; the second is a duplicate)
- [x] Confirm country selection, map render, focus tree render, basic diplomacy, and first-day tick.
- [x] Advance 30 days and 180 days with AI on; inspect error logs and major country stability. (ran ~13 months; no crash)
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
