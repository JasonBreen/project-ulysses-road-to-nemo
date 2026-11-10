# Vanilla visual scrub

Static inventory for the player-visible vanilla and Earth art still reachable
after the 1.19 port. This pass did not launch HOI4. A sprite listed here is
rebound in `interface/zz_ac_visual_scrub.gfx`, or it is called out below as
still blocked. Placeholders are provisional presentation. They are not
official Project Aces art.

Regenerate the override and the machine list with:

```bash
python3 -B tools/visual_scrub/build_fallthroughs.py
python3 -B tools/visual_scrub/build_fallthroughs.py --check
```

`tools/visual_scrub/inventory.json` is the full sprite list (893 names). The
check is part of `tools/Test-UlyssesStatic.ps1`.

## Why a slot still showed vanilla art

Two mechanisms, both outside `tools/audit_visual_dependencies.py` (that audit
only checks texture paths inside mod `.gfx` files, and it reports 0 missing
files):

1. A screen asks for a `GFX_` name that no mod file defined, so the engine
   definition is used. That covers manufacturer traits, generic and Earth
   idea pictures, Earth event photographs, Earth portraits, the German agency
   logo, the shared building strip, and the 1936 bookmark picture.
2. An engine `.gfx` the mod does not replace points at a path the mod does
   ship, and the file at that path was an Earth photograph. Rebinding the
   sprite name is not enough. The bytes at the path have to change too.

`zz_ac_visual_scrub.gfx` sorts after the engine interface files and only
defines names the mod did not already define, so it does not replace art the
mod already drew.

## What was on screen, and what it uses now

| Slot | What it showed | Why | Now |
| --- | --- | --- | --- |
| `gfx/interface/techtree/{infantry,air,naval,industry,support}_techtree_bg.dds` | Earth photographs (soldier, jets, carrier, factory, AWACS crew), 959×715 | Engine `countrytechnologyview.gfx` uses these paths. The mod does not ship that file | Same paths overwritten with a labelled navy placeholder. Sprites `GFX_*_techtree_bg` are defined in the mod |
| `gfx/interface/armortech_bg.dds` | Tanks in a European street | Same engine file, sprite `GFX_armortech_bg` | Same path overwritten with a labelled placeholder |
| `gfx/interface/techtree/artillery_techtree_bg.dds` | Futuristic gun firing into a ring, already packaged with the mod | Same engine lookup | Kept. `GFX_artillery_techtree_bg` is now defined so the lookup stays in the mod. Reviewers should say if this still reads as Earth |
| `GFX_buildings_strip` | Vanilla 31-frame building strip, including 1.15+ frames | Unreplaced engine sprite. The mod already drew the same strip as `GFX_ac_ui_buildings_strip` | Aliased to that strip, `noOfFrames = 31` |
| `GFX_naval_headquarter_buildings_bg` | Engine naval-headquarters card | Unreplaced engine sprite | Placeholder panel |
| `GFX_specialization_{air,land,naval,nuclear}`, `GFX_dam_icon_small`, `GFX_canal_icon_small` | Engine facility, dam, and canal icons | Names are not the technology-specialisation sprites the mod already defined | Existing specialisation, industry, and navy icons |
| `GFX_goal_*` / `GFX_idea_*` / `GFX_focus_*` for continuous focuses, including `repairments`, `research`, `increase_nu`, and the Danish and Ethiopian names | Vanilla continuous-focus icons | The campaign file already uses `GFX_ac_exp_continuous_*`. The vanilla names were still defined only by the engine | The 11 existing continuous icons under `gfx/interface/ac_expansion/continuous/` |
| Grand-doctrine names used by campaign history (`mobile_warfare`, `superior_firepower`, `grand_battleplan`, `mass_assault`, `fleet_in_being`, `trade_interdiction`, `base_strike`, `strategic_destruction`, `battlefield_support`, `operational_integrity`, and the `new_*` forms) | Engine doctrine cards and backgrounds, where those sprite names exist | The mod does not ship `common/doctrines` or a doctrine `.gfx`. Existing `GFX_*_medium` technology icons in `Technologies.gfx` were left alone | `GFX_<id>`, `GFX_<id>_medium` when missing, `GFX_doctrine_<id>`, `GFX_doctrine_icon_<id>`, and `*_bg` aliases. Icons use existing land, navy, or air briefing art. Backgrounds use the placeholder panel |
| Undefined `GFX_idea_*`, `GFX_generic_mio_*`, and Earth focus pictures (FRA, SOV, SPR, POL, and the other Earth tokens the mod still references) | Earth idea and manufacturer icons, or the error dog | No mod sprite | Existing briefing icons (`idea_air`, `idea_navy`, `idea_military`, `idea_industry`, `idea_economy`, `idea_assembly`) by keyword |
| Undefined `GFX_report_event_*` | Earth news photographs (parliaments, civil-war scenes, and similar) | No mod sprite | `report_event_blk_parliament.dds`, `report_event_army_issues_1.dds`, or `report_event_bad_news_1.dds` |
| Undefined `GFX_news_event_*` | Earth news photographs | No mod sprite | `gfx/AC_event_style/news_default.dds`, the existing mod-owned 397×153 news-format picture; country-event art is not stretched into the news layout |
| `GFX_Portrait_Europe_Generic_*`, Polish and British portraits, `GFX_portrait_unknown*`, `GFX_leader_unknown` | Earth or generic leader portraits | No mod sprite | `gfx/interface/ac_visual_scrub/portrait_placeholder.dds` (156×210, labelled) |
| `GFX_TC_*`, `GFX_TM_*`, `GFX_TC_large_plane_airframe_*`, `GFX_SD_tv_*`, `GFX_SM_*`, including unsuffixed and `eng`/`fra`/`ger`/`ita`/`jap`/`sov`/`usa` suffixes from the dependency samples | WWII tank, aircraft, and ship designer icons | Engine designer sprites. The land, air, and naval programs left this presentation open | Existing 2006 research cards, land modules, naval modules, and ship blueprints. `noOfFrames = 1` |
| `GFX_axis_album_art`, `GFX_allied_faceplate`, `GFX_comintern_album_art` | WWII faction music-player art | Engine music UI | `superevent_station_album_art.dds`, 2 frames, matching the mod station |
| `GFX_goal_generic_trade`, `GFX_raid_unit_icon_nuclear_raids` | Generic trade and nuclear-raid icons | Engine goals | Economy and radar briefing icons |
| `GFX_intelligence_agency_logo_ger` | German agency seal on Belka | Belka's agency entry used the engine sprite | `gfx/interface/ac_visual_scrub/agency_placeholder.dds`, 2 frames. The on-screen name in `common/intelligence_agencies/ac_intelligence_agencies.txt` and `history/countries/BLK - Belka.txt` is the placeholder label "Belkan intelligence office". That label is not a canon service. `tools/world_legacy/baseline` was not edited. The history-cleanup receipt and the world-foundation source digest record that label change; country rows in the registry were not rewritten |
| `GFX_select_date_1936` | Vanilla 1936 bookmark art on both 1991 bookmarks | The bookmark files still use that sprite name | Existing `gfx/interface/ac_briefing/select_date.dds` |
| `GFX_frontend_bg` | Archived Project Ulysses globe fallback | The prior scrub misclassified the existing menu artwork and overwrote it; a frontend repair also removed the original animated tile layout | Owner explicitly directed restoration on 8 November 2026. Restored the exact archive fallback and 35-tile layout, preserved all 35 original animation textures byte-for-byte, and removed the menu asset from placeholder generation. This is retained mod presentation/provenance, not a setting-geography claim. |
| `GFX_frontend_game_logo` | Engine logo sprite; the conventional texture path was not the wordmark file | Undefined in the mod | Existing `gfx/interface/logo_game.dds` Project Ulysses wordmark |

Named manufacturer marks already in `interface/ac_mio_icons.gfx` (Grunder, Colt,
and the other abstract marks) were left. They are geometric, not Earth
logotypes. The organization names were not renamed.

Special-project icons, rewards, blueprints, and the scientist portrait pool
in `interface/ac_special_projects.gfx` were already mod art. The appended
1.19 blocks in `Technologies.gfx`, `countrytechtreeview.gfx`,
`ac_plane_modules_icons.gfx`, and `subuniticons.gfx` already point at files
that exist in the mod. Focus-tree icons and the economy dashboard were
already clean in `audit_visual_dependencies.py`.

## Left on purpose, or blocked on missing art

These are not silent leftovers:

- **3D map buildings.** `gfx/entities/e_buildings.gfx` only has the Stonehenge
  and Megalith meshes. Ordinary buildings and the 1.15+ facility, stronghold,
  and naval-headquarters meshes are still the engine models. The repo has no
  replacement meshes. `map/buildings.txt` was not edited.
- **Unconfirmed grand-doctrine sprite names.** There is no HOI4 1.19 install
  here, and a lookup of the installed `common/doctrines` / doctrine interface
  was rate-limited. Aliases cover the campaign keys under the patterns above.
  A subdoctrine card whose sprite name does not match those patterns can
  still show engine art. That needs an installed-reference pass. Doctrine
  gameplay and AI keys were not changed.
- **Designer frame counts.** The aliases use one frame. If an engine sprite
  is a strip, the icon will be sliced. The dependency samples that supplied
  these names were also truncated to the first failures on each screen, and
  only the recorded tags were expanded.
- **Interface chrome.** Buttons, flags, the minimap, scrollbars, difficulty
  marks, diplomacy-action glyphs, and the Paradox logos (`GFX_clausewitz_logo`,
  `GFX_pdx_int_logo`) were not rebound. Replacing them would throw away the
  original Project Ulysses interface. They are not the photographs above.
- **Frontend animation tiles.** `GFX_frontend_bg_tile_*` are abstract dark
  frames. The current `frontendmainview.gui` does not reference them, so they
  were not rewired.
- **Native rendering.** None of the rebinding was viewed in HOI4.

The retained world-legacy history capture remains immutable. Its compiler now projects only the reviewed Belkan agency caption from `Bundesnachrichtendienst` to `Belkan intelligence office`; the agency icon and every other nonmilitary history field remain subject to the original comparisons. A focused regression rejects unexpected source/icon changes and verifies that the projection changes only that one name. This is a presentation repair, with no new historical claim or native acceptance.
