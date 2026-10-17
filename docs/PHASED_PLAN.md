# Phased development plan

Guiding priority: make a coherent, playable private continuation before pursuing public-release polish. Preserve the static baseline and keep each phase independently reviewable.

## Phase 0 — Reproducible baseline and compatibility diagnosis

1. Freeze the source archive and baseline; record hashes and the exact HOI4/Steam build used for every later report.
2. Decide the target game branch (initially diagnose against local Steam build `25205862`) and reconcile the two descriptors: `2985041246.mod` says `1.13.*`, while embedded `ProjectUlysses.mod` says `1.14.3` and contains an obsolete developer path.
3. Build a static reference map of all `replace_path` entries, country tags, focus trees, events, scripted effects, state ownership, map definitions, and localization keys.
4. Determine DLC/feature assumptions from syntax and replace paths before any runtime launch.
5. Establish a minimal static validation harness; do not treat it as a runtime test.

Exit criteria: one documented target branch, no ambiguous descriptor/path behavior, an actionable list of hard parse blockers, and a clean first local commit.

## Phase 1 — Viable 1991 Belkan War campaign

1. Make the two Jan 1, 1991 bookmarks deterministic and selectable.
2. Make Belka, Ustio, Sapin, Gebet, Osea, and A World With No Boundaries focus trees loadable and reachable from their country setup.
3. Verify initial country histories, OOBs, leaders/advisors, diplomacy, starting wars, and AI strategy plans as one coherent scenario.
4. Resolve map/state blockers first: state 171 placeholder ownership/manpower, empty `map\positions.txt`, and any missing province/strategic-region references.
5. Give AI a safe opening plan for the Belkan War and ensure supply/rail/airfield data is coherent.

Exit criteria: the 1991 scenario reaches the first major branch without parse errors, missing references, or immediate deadlocks in a controlled runtime test.

## Phase 2 — Postwar continuity after demo branches

Current slice: world_event.2 now dispatches branch-aware postwar handoff events for conventional victory, Wacht am Wal, and defeat. Provisional reconstruction, demobilization, political-settlement, and affected-country administration decisions are available from the handoff flags. Native reachability, save/load, and long-run behavior remain unverified.

1. Replace the demo-only `world_event.2` terminal outcome with explicit, branch-aware continuation states.
2. Preserve Belkan victory/defeat, Rhongomyniad, Osea election, Sapin, Gebet, and Ustio consequences in a shared continuity ledger.
3. Make postwar focus trees, events, AI plans, decisions, and country history agree on ownership, cores, governments, and dates.
4. Add save/load checkpoints at the Belkan War end and the first postwar year.

Exit criteria: every supported demo branch has a declared postwar destination and can be saved, loaded, and advanced without silently returning to a dead-end event.

## Phase 3 — Wider Usea and later wars

1. Expand Recta/Yuktobania and other Usean content only after their branch contracts are written.
2. Reconcile the 1991–2005 technology span, inherited armor/naval dates, properly localized technology/equipment names, and any later-war equipment gates against the 2065-12-31 inclusive campaign contract.
3. Replace placeholder art, names, leaders, advisors, and ship names in priority order of player visibility.
4. Compile Sam's established Joker 1 continuity as a separately attributed user-authored source before implementing it; do not invent future lore to fill the 2065 horizon.
5. Integrate the child task's Markdown economy model and portable VS Code/Antigravity-compatible workspace only after reviewing its separate branch/worktree and static assumptions.
6. Add long-run AI, supply, diplomacy, peace conference, and save stability coverage.

Exit criteria: later-war content is reachable from validated prior branches and does not require undocumented assumptions.

The 2065 target has two separate exit questions: (a) the engine/scripts permit advancement through 2065-12-31, and (b) the authored content and canon/provenance ledger provide meaningful, tested content through that date. Passing (a) never implies (b).
