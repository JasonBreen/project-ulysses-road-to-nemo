# HOI4 1.19 port log

Target: Hearts of Iron IV **1.19.3 "Operation Postern"** (local Steam install). Source: Project Ulysses open alpha v0.2 (April 2024), built for 1.13/1.14.

Policy decisions made during the port:

- **Original look wins.** Where the mod overrides a vanilla GUI with its own layout (main menu, scenario/country select, tech tree), the original Project Ulysses file is kept. Elements the 1.19 engine looks up but the old file lacks are added as **hidden stubs** (moved to `x = -20000`). Invisible `positionType` anchors keep their vanilla coordinates, because the engine moves windows to them.
- **No vanilla (WWII) visuals.** Anything the player sees should be Strangereal or mod art. Vanilla sprites still visible are listed under "Open items".
- **Vanilla mechanics are welcome.** Stale 1.14 copies of vanilla rules files are dropped, so 1.19 rules (traits, buildings, abilities) apply.

Migration scripts live in [`tools/port_1_19/`](../tools/port_1_19/). They are one-off and read HOI4 from `G:\steamlbirary\steamapps\common\Hearts of Iron IV`.

## Verified in game (2026-10-17)

Belka, 1 Jan 1991 bookmark: menu → scenario → country select → campaign start → ran to Feb 1992 at speed 5 with no crash. Checked the research panel (Experimental Facilities tab), tech tree tabs (infantry, armour), the government view, decisions, and the national focus tree with continuous focuses.

`error.log` comparison against the untouched v0.2 on 1.19:

| | v0.2 on 1.19 | after port |
|---|---:|---:|
| Total lines | 14,786 | 12,710 (including a year of runtime) |
| "will most likely crash the game" warnings | 24 | 2 |
| Errors attributed to mod files | 264 | 175 |
| Errors attributed to vanilla files | 5,484 | 3,312 |

## Changes

### Descriptors and fork identity
- `supported_version="1.19.*"`, version `0.3-dev`, name **Project Ulysses: Continuation**. The stale developer `path=` and the original team's `remote_file_id` are removed from the embedded descriptors.
- The main-menu version label is now localisation key `PU_MAIN_MENU_VERSION`: "CONTINUATION FORK v.0.3-dev ---------- ROAD TO ITHACA" (Aces font, original position).
- The welcome screen header is now `PU_WELCOME_HEADER`. A fork note crediting the original team is appended to the welcome text.

### Crash fixes
- **Main menu GPU crash (~20 s after the menu appears).** 1.15+ has a background manager that rotates menu backgrounds from `gfx/loadingscreens`, which the mod `replace_path`s. Fixes:
  - The original menu is restored with no `Background` element, as in v0.2.
  - `common/frontend/backgrounds/base_backgrounds.txt` lists only the mod's `load_1`–`load_7`.
  - `load_1`–`load_3` are re-encoded from 24-bit RGB (no D3D11 format exists for it) to 32-bit BGRA.
  - `load_N_small.dds` thumbnails are generated.
- **Undefined GUI types** (`mainmenu_dlc_ownership`, `owned_dlc_item`, `change_background`, `country_filter`, …) are added as hidden stubs. See `restore_original_gui.py`.
- **Tech tree tabs not switching.** `nsb_armour_folder` is defined in `technology_tags` again (with `available = { always = no }`). The 1.19 engine and scripts expect it, and the folder never shows.
- **Music player:** `superevent_station` (from `music/superevent_music.txt`) had no `<station>_faceplate` / `_stations_entry` GUI. Added `interface/pu_superevent_music_station.gui`, hidden, with album art built from the mod's Belkan War superevent picture.

### Map: "Failed to load the map"
- All 326 strategic regions had empty `weather={}`. Each now gets the weather of the vanilla region with the closest mean latitude and the same land/sea type, measured on `provinces.bmp` (both maps are 5632×2048). Script: `gen_weather.py`.
- `rivers.bmp` header `biClrUsed`/`biClrImportant` changed from 256 to 0. The engine checks `GetColors() == 0` ("Palette in rivers.bmp is probably not correct").
- `map/buildings.txt` is migrated to 1.15+ spawn points by `migrate_map_buildings.py`:
  - `naval_base`, `rocket_site` and `nuclear_reactor` become `*_spawn`.
  - `naval_headquarters` and `naval_supply_hub` are added at naval bases.
  - `special_project_facility_spawn` goes on every land province.
  - `stronghold_network` goes on every state.
- Positions are added for state 367 (rocket site, which the mega gun emplacement also uses, and fuel silo) and for 26 states without a radar station.
- Six lake provinces are removed from state 541.

### Rules rebased on 1.19
- Removed the old-vanilla copies `common/country_leader/00_traits.txt` (the source of 147 `command_cap` errors) and `common/buildings/00_buildings.txt` (1.14 building syntax, missing all 1.15+ buildings).
- `generic_leader_abilities.txt` is now the 1.19 file plus the mod's `has_cheap_*` exclusions. In `cheap_leader_abilities.txt`, the removed `add_temporary_buff_to_units` became `unit_modifiers`.
- Air modifiers removed in 1.15+ (`air_<mission>_attack/defence/agility_factor`) are mapped to `air_superiority_efficiency`, `air_cas_efficiency`, `air_intercept_efficiency` and `air_strategic_bomber_bombing_factor`/`_defence_factor`. Changed files: `ideas/sapin.txt`, `ideas/gebet.txt`, `dynamic_modifiers/ac_dynamic_modifiers.txt`. Values that collided in the same block are summed.
- The anti-air construction in the Gebet focus no longer passes `province =`, because AA is a state building in 1.19.
- `technology_tags`: added the 1.15–1.19 categories referenced by vanilla doctrines, MIOs and special projects.

### Doctrines (1.17+ system)
- Removed the old `land_doctrine.txt` / `special_forces_doctrine.txt` techs and the `countrydoctrinetreeview.gui` override.
- Starting grand doctrines:

| Nation | Land | Naval | Air |
|---|---|---|---|
| Belka | Mobile Warfare | Fleet in Being | Strategic Destruction |
| FATO | Mobile Warfare | Base Strike | Operational Integrity |
| Gebet | Grand Battleplan | Fleet in Being | Battlefield Support |
| Osea | Superior Firepower | Base Strike | Operational Integrity |
| Ustio | Superior Firepower | Convoy Raiding | Operational Integrity |

### GUI, sprites, localisation
- Dropped stale 1.14 copies of vanilla views (diplomacy, politics, production, state, trade, division designer, unit view, in-game menu). 1.19 versions load instead; the mod made no visual changes to them.
- The `.gfx` overrides (`Technologies`, `countrytechtreeview`, `plane_modules_icons`, `subuniticons`) keep the mod sprites, with the 1.19 sprite names they lacked appended so lookups resolve.
- Partial localisation overrides (`core`, `equipment`, `research`, `unit`, `plane_designer`, `factions`, `parties`) moved to `localisation/english/replace/pu_*.yml`, so 1.19's new UI strings exist. Mod keys still win.

## Open items

1. **Vanilla visuals still on screen.** Continuous focus icons, grand doctrine icons, 1.15+ building icons, special-project art, and the vanilla sprites appended to the `.gfx` files. Needs an art audit and Strangereal replacements or placeholders.
2. **Vanilla-content noise.** ~3,300 errors from Earth-country focuses, events, decisions, scripted effects, special projects and MIOs that reference removed tags and equipment. Silence them with empty overrides, and replace special projects with Strangereal superweapon projects.
3. **AI templates** (`common/ai_templates/generic.txt`) use deprecated syntax: `roles`, `target_width`, `allowed_types`, `production_prio`.
4. **History data.**
   - Invalid ship name groups (Sapin, FATO).
   - Equipment variants with icon `xxx` (Belka ADB-N, Gebet Merlin).
   - The P-3 Orion has an invalid module layout.
   - Nordennavic popularities don't add to 100.
   - DEL/SHI character conflict.
5. **Subdoctrine bonuses** target vanilla unit types (`super_heavy_artillery`, `support_ship`, …). Mod units need their own subdoctrine tuning.
6. **Two identical 1991 bookmarks** in `common/bookmarks`. Only one is shown by the original setup screen.
7. Test-only `events/crowbuildingdebugevents.txt` references undefined `stonehenge`/`megalith` buildings.
8. Remaining crash warnings: `id 48100001 50 already exists` (a duplicate unit or ship id in history) and a parse quirk on `gfx/loadingscreens/load_7.dds`. Neither crashed in testing.
