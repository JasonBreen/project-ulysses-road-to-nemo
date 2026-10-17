# Static content inventory

Inventory subject: `G:\Project-Ulysses-Continuation\mod\2985041246\` (editable copy), compared with the read-only baseline and source archive.

## Descriptor and source

- Wrapper descriptor: `G:\Project-Ulysses-Continuation\mod\2985041246.mod`
  - `version="0.1"`
  - `supported_version="1.13.*"`
  - multiple `replace_path` directives for map, history, countries, bookmarks, AI, characters, loadingscreens, units, and equipment.
- Embedded descriptor: `G:\Project-Ulysses-Continuation\mod\2985041246\ProjectUlysses.mod`
  - `version="0.1"`
  - `supported_version="1.14.3"`
  - obsolete developer path: `C:/Users/Adam/Documents/Paradox Interactive/Hearts of Iron IV/mod/ProjectUlyssesMain`
  - `remote_file_id="2985041246"`
- Archive: 3,104 files in the extracted mod tree; 1,524 are text-like source/localization files.

## Focus and scenario content

There are 19 national-focus files. Counts below are non-comment `focus`/`shared_focus` blocks, not proof of reachability:

| Area | Files | Blocks |
| --- | --- | ---: |
| Belka | `BLK_DLP.txt`, `BLK_election_tree.txt`, `BLK_start.txt`, `BLK_war_lost.txt`, `BLK_war_won.txt` | 139 |
| Ustio | `UST_shared.txt` | 161 |
| Sapin | `SAP_pre_belkan_war.txt` | 96 |
| Gebet | `GEB_pre_belkan_war.txt` | 67 |
| Osea | `OSE_pre_belkan_war.txt` | 50 |
| A World With No Boundaries | `AWW_shared.txt` | 25 |
| Generic | `generic.txt` | 54 |

Additional observations:

- `NPT.txt` and `NPT_pre_continental_war.txt` are entirely commented/empty by static non-comment-line count.
- No dedicated Recta or Yuktobania national-focus file was found; related country/event/decision content exists.
- Two bookmark files exist, each containing a Jan 1, 1991 date: `common\bookmarks\blitzkrieg.txt` and `common\bookmarks\the_gathering_storm.txt`.
- Osea's default focus tree comments out election branches while `ose_mac_won` includes them; the Osea AI plan names election and post-election focuses. Reachability and completion behavior are unverified.

## Events and continuity

- `events\ac_world_events.txt:30-40` defines `world_event.2`, titled/described as a demo-ending event with `fire_only_once = yes` and `is_triggered_only = yes`.
- It is called from `common\national_focus\BLK_war_won.txt:646` and four Belka event outcomes at `events\Belka.txt:1164, 1580, 1726, 1891`.
- Rhongomyniad content is present in `common\national_focus\BLK_war_won.txt:625-648` and `events\Belka.txt:1880`; this is evidence of branch coupling, not proof that the game clock stops.

## Map, history, and technology

- 69 country history files under `history\countries`.
- 326 strategic-region files under `map\strategicregions`.
- 356 map files total, including terrain/raster assets, `definition.csv`, railways, supply nodes, airports, and province/building data.
- `map\positions.txt` exists but is zero bytes; HOI4 1.19.3 vanilla ships it empty too, so it is not a blocker.
- 15 technology files under `common\technologies`; static date markers span approximately 1910–2005 depending on file, including inherited armor/naval dates that need deliberate review before being called defects.
- `history\states\171-State_171.txt` assigns owner/core `PLH`, manpower `1`, zero resources, zero listed buildings, `state_category=town`, and a large province list. Geography and intended ownership are not established.

## Placeholder and polish debt

Static search finds 157 case-insensitive `placeholder` matches, including placeholder leaders/advisors/chiefs/theorists, decision icons, and placeholder ship-class names. These are triage signals only; each must be classified as intentional, temporary, or broken before replacement.
