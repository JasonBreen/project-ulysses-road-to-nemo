# Prioritized next tasks

Status as of 2026-10-17: the mod loads, starts the 1991 campaign and runs for over a year on HOI4 1.19.3. See [PORT_1_19.md](PORT_1_19.md) for what was done.

Standing rules: keep the original Project Ulysses look and layouts; **no HOI4 vanilla (WWII) visuals** anywhere; 1.15–1.19 mechanics are welcome.

Current continuation slice: the former demo handoff now consumes conventional victory, Wacht am Wal, and defeat outcome flags. It exposes provisional reconstruction, demobilization, political-settlement, and affected-country administration decisions. See [LORE_EVENT_COVERAGE_BACKLOG.md](LORE_EVENT_COVERAGE_BACKLOG.md). Static validation is required; native reachability remains unverified.

1. **Vanilla-visuals audit**
   - List every sprite on screen that resolves to a vanilla texture: continuous focuses, grand doctrines, 1.15+ buildings, special projects, appended `.gfx` entries, MIO icons.
   - Replace each with Strangereal art, or with mod placeholders until art exists.
2. **Silence vanilla content**
   - Empty-override the Earth-country focus, event, decision, scripted-effect and MIO files that error against the Strangereal setup (~3,300 log lines).
   - Keep generic files that 1.19 systems rely on.
3. **Strangereal special projects.** Replace vanilla WWII projects with Ace Combat superweapons: Excalibur, V2, Stonehenge, Megalith, Arkbird and others. These build on the new `special_project_facility_spawn` positions.
4. **AI templates and doctrines**
   - Rewrite `common/ai_templates/generic.txt` in 1.19 syntax.
   - Retarget subdoctrine unit bonuses to the mod's modern unit types.
5. **History cleanup**
   - Ship name groups (Sapin, FATO).
   - `xxx` equipment icons.
   - P-3 Orion module layout.
   - Nordennavic popularities.
   - DEL/SHI character conflict.
   - Duplicate unit id `48100001`.
6. **Bookmarks.** Merge or differentiate the two identical Jan 1, 1991 bookmarks.
7. **Belkan War branch graph and postwar continuity.** Static campaign arc is now implemented on the campaign branch: prewar preparation, war start, three war-stage decisions/AI fallbacks, existing outcome branches, and postwar focus/decision continuity. Native reachability and balance are still open.
8. **Native playtest when approved.** Follow [NATIVE_PLAYTEST_CHECKLIST.md](NATIVE_PLAYTEST_CHECKLIST.md) and the per-branch routes in [BELKAN_WAR_PLAYTEST_PLAN.md](BELKAN_WAR_PLAYTEST_PLAN.md); do not treat this branch as playtested until the user approves an isolated HOI4 run.
9. **Long-run test.** Run to 1995 with AI on: save and reload at each checkpoint, check other nations (Osea, Ustio, Sapin, Gebet), and log results in the testing checklist.
10. **Technology/name provenance pass.** Name and localize authored technology and equipment, classify inherited engine IDs, and reconcile 1991–2005 content with the inclusive 2065 campaign end (`END_DATE = 2066.1.1.1`).
11. **Canon ledger and Joker 1 compilation.** Collect primary Project Aces citations for lore-sensitive claims ([CANON_POLICY.md](CANON_POLICY.md), [CANON_LEDGER.md](CANON_LEDGER.md)) and Sam's Joker 1 source material separately; do not invent missing dates or future events.
12. **Economy/IDE integration.** Review the separate economy model and portable workspace work, then integrate only its documented IDs and validation assumptions.
13. **Keep static validation green.** Run `tools/Test-UlyssesStatic.ps1` before every runtime test; CI runs it on every push.
