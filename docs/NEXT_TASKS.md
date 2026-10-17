# Prioritized next tasks

Status as of 2026-10-17: the mod loads, starts the 1991 campaign and runs for over a year on HOI4 1.19.3. See [PORT_1_19.md](PORT_1_19.md) for what was done.

Standing rules: keep the original Project Ulysses look and layouts; **no HOI4 vanilla (WWII) visuals** anywhere; 1.15–1.19 mechanics are welcome.

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
7. **Belkan War branch graph and postwar continuity.** Unchanged from the phased plan; replace the `world_event.2` demo terminal.
8. **Long-run test.** Run to 1995 with AI on: save and reload at each checkpoint, check other nations (Osea, Ustio, Sapin, Gebet), and log results in the testing checklist.
