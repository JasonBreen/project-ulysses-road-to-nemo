# Compatibility checklist

Status legend: `[ ]` not checked, `[S]` static-only evidence collected, `[R]` requires runtime verification. No `[R]` item is claimed complete.

## Descriptor and path resolution

- [S] Preserve and compare both descriptors; they disagree on supported version (`1.13.*` vs `1.14.3`).
- [x] Choose and document the target HOI4 branch/build: **1.19.3 Operation Postern**; descriptors say `1.19.*`.
- [x] Remove or quarantine the obsolete absolute developer path before any launcher/runtime use.
- [ ] Decide whether the wrapper `replace_path` set is intentional for the target branch and whether each path still exists.
- [ ] Confirm the launcher resolves the wrapper and content directory exactly once, with no duplicate mod registration.

## Game/DLC syntax surface

- [ ] Identify DLC-gated syntax and content in AI, equipment, naval, agency, MIO, occupation, and on-action files.
- [ ] Check that all referenced scripted effects, triggers, modifiers, technologies, equipment types, and GUI assets exist in the target branch.
- [ ] Check localization key coverage for focus, event, decision, country, state, character, equipment, and achievement IDs.
- [ ] Check icon/portrait/model/sound paths case-insensitively and against actual files.

## Scenario and map integrity

- [~] Verify both 1991 bookmarks load the expected start date, countries, wars, focus trees, OOBs, and AI plans. (Belka start verified at runtime; the two bookmarks are duplicates)
- [ ] Resolve `PLH`/state 171 placeholder ownership, core, manpower, and geography.
- [x] Verify every province belongs to exactly one state and every state references valid provinces/strategic regions. (static check 2026-10-17; 6 lakes removed from state 541)
- [x] Investigate empty `map\positions.txt` before runtime testing. (vanilla 1.19 ships an empty positions.txt too — not a blocker)
- [ ] Verify strategic regions, supply areas/nodes, railways, airports, naval bases, and map rasters agree with province definitions.

## Focus/event/AI continuity

- [ ] Build a focus ID/reference graph and flag missing prerequisites, relative positions, duplicate IDs, and unreachable roots.
- [ ] Build an event ID/reference graph; especially trace Belkan outcomes, Rhongomyniad, Osea elections, and `world_event.2`.
- [ ] Replace demo-terminal behavior with explicit continuation contracts before claiming postwar support.
- [ ] Check AI strategy plans against actual focus IDs and country tags; do not infer reachability from definition counts.
- [ ] Review Osea election branches and the commented North Point tree as intentional design decisions.

## Save stability and packaging

- [ ] Confirm a save created at each phase checkpoint can reload after descriptor/path changes.
- [ ] Confirm no absolute local paths, remote workshop assumptions, or installation-specific generated files remain.
- [ ] Confirm source archive and baseline remain unchanged after every working-copy edit.
