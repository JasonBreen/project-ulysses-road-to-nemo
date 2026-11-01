# Prioritized next tasks

Status as of 2026-10-17: the mod loads, starts the 1991 campaign and runs for over a year on HOI4 1.19.3. See [PORT_1_19.md](PORT_1_19.md) for what was done.

Standing rules: keep the original Project Ulysses look and layouts; **no HOI4 vanilla (WWII) visuals** anywhere; 1.15–1.19 mechanics are welcome.

Current continuation slice: the former demo handoff now consumes conventional victory, Wacht am Wal, and defeat outcome flags. It exposes provisional reconstruction, demobilization, political-settlement, affected-country administration decisions, and a guarded Ustio handoff that reconnects the inherited branch graph. See [LORE_EVENT_COVERAGE_BACKLOG.md](LORE_EVENT_COVERAGE_BACKLOG.md). Static validation is required; native reachability remains unverified.

1. **Vanilla-visuals audit**
   - List every sprite on screen that resolves to a vanilla texture: continuous focuses, grand doctrines, 1.15+ buildings, special projects, appended `.gfx` entries, MIO icons.
   - Replace each with Strangereal art, or with mod placeholders until art exists.
2. **Silence vanilla content**
   - Empty-override the Earth-country focus, event, decision, scripted-effect and MIO files that error against the Strangereal setup (~3,300 log lines).
   - Keep generic files that 1.19 systems rely on.
3. **Strangereal special projects — done (static).** The vanilla WWII projects and scientist traits are replaced by `ac_sp_excalibur`, `ac_sp_v2`, `ac_sp_stonehenge`, `ac_sp_arkbird`, `ac_sp_megalith` and `ac_sp_rhongomyniad`, with `ac_superweapons` no-DLC fallback decisions. See the Track C section of [USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md). Native reachability is unverified.
4. **AI templates and doctrines**
   - Rewrite `common/ai_templates/generic.txt` in 1.19 syntax.
   - Retarget subdoctrine unit bonuses to the mod's modern unit types.
5. **History cleanup** — partially done on `claude/fill-open-gaps` (static, `tools/Test-HistoryDataCleanup.py`):
   - Ship name groups (Sapin, FATO). Done: `common/units/names/00_SAP_names.txt` and `00_FAT_names.txt` define the starting-fleet ship types with the fleet names already in the SAP/FAT navy histories (mod provenance).
   - `xxx` equipment icons. Done: Belka Guinevere Mark II stray duplicate `icon = "xxx"` removed; ADB-00 now uses `GFX_BLK_iw_medium_plane_medium`; FATO Hugo Havel's `large="xxx"` portrait block removed (generic fallback, as with the other portraitless FATO leaders); Perbla/Spayca `division_names_group = xxx` replaced by defined `PBL_*`/`SYC_*` groups.
   - P-3 Orion module layout. Still open: the variant's slots are statically consistent with the installed large-airframe archetype, so the exact invalid module needs a native error log to pin down.
   - Nordennavic popularities. Done: 7+82+7+2 summed to 98; neutrality raised to 9 (ruling monarchism unchanged).
   - DEL/SHI character conflict. Done: Shilage no longer recruits Delarus's `DEL_artur_clarkson`; it now recruits the generated `SHI_ac_government_office` (unnamed office, no invented person) via `tools/usea_expansion/build_leaders.py`.
   - Duplicate unit id `48100001`. Still open: no duplicate legacy unit/ship id was found by static scan on this branch; needs the native log line to locate.
6. **Bookmarks.** The two Jan 1, 1991 bookmarks are contract-locked: `tools/Test-AneaPresentation.py` requires both files to offer EMM/EVA. Left as-is; do not merge without updating that contract.
7. **Belkan War branch graph and postwar continuity.** Static campaign arc is now implemented on the campaign branch: prewar preparation, war start, three war-stage decisions/AI fallbacks, existing outcome branches, postwar focus/decision continuity, and the repaired Ustio opening/postwar handoff. Native reachability and balance are still open.
8. **Native playtest when approved.** Follow [NATIVE_PLAYTEST_CHECKLIST.md](NATIVE_PLAYTEST_CHECKLIST.md) and the per-branch routes in [BELKAN_WAR_PLAYTEST_PLAN.md](BELKAN_WAR_PLAYTEST_PLAN.md); do not treat this branch as playtested until the user approves an isolated HOI4 run.
9. **Long-run test.** Run to 1995 with AI on: save and reload at each checkpoint, check other nations (Osea, Ustio, Sapin, Gebet), and log results in the testing checklist.
10. **Technology/name provenance pass.** Name and localize authored technology and equipment, classify inherited engine IDs, and reconcile 1991–2005 content with the inclusive 2065 campaign end (`END_DATE = 2066.1.1.1`).
11. **Canon ledger and Joker 1 compilation.** Collect primary Project Aces citations for lore-sensitive claims ([CANON_POLICY.md](CANON_POLICY.md), [CANON_LEDGER.md](CANON_LEDGER.md)) and the supplied Joker 1 source material separately; do not invent missing dates or future events.
12. **Economy/IDE integration.** Review the separate economy model and portable workspace work, then integrate only its documented IDs and validation assumptions.
13. **Keep static validation green.** Run `tools/Test-UlyssesStatic.ps1` before every runtime test; CI runs it on every push.
