# Content waves

Generator for the 2006–2020 content waves planned in
[docs/CONTENT_PLAN_2006_2020.md](../../docs/CONTENT_PLAN_2006_2020.md), sourced
from [docs/STRANGEREAL_2006_2020_SOURCES.md](../../docs/STRANGEREAL_2006_2020_SOURCES.md).

| Wave | Module | Focuses | Ledger |
| --- | --- | --- | --- |
| A, the oversight years | `free_erusea.py` | Erusea 36, Central Usea 24 | [CONTENT_WAVES_A_D.md](../../docs/CONTENT_WAVES_A_D.md) |
| D, the northern reserve | `nordennavic.py` | Nordennavic 42 | [CONTENT_WAVES_A_D.md](../../docs/CONTENT_WAVES_A_D.md) |
| B, the Estovakian civil war | `estovakia.py` | Estovakia 30, Emmeria 18 | [CONTENT_WAVES_B_AUR.md](../../docs/CONTENT_WAVES_B_AUR.md) |
| Aurelia's foundation | `aurelia.py` | Aurelia 54 | [CONTENT_WAVES_B_AUR.md](../../docs/CONTENT_WAVES_B_AUR.md) |
| C, the Circum-Pacific War | `circum_pacific.py` | none: owner only (Osea and Yuktobania are complete) | [CONTENT_WAVE_C.md](../../docs/CONTENT_WAVE_C.md) |
| F1, the Lighthouse War | `lighthouse.py` | Erusea 54, Central Usea 24, plus two special projects | [CONTENT_WAVE_F1.md](../../docs/CONTENT_WAVE_F1.md) |
| The Belkan War record | `belkan_record.py` | none: thirteen observed reference briefs, 1991–1999 (`ac_bwr`) | [BELKAN_WAR_SOURCES.md](../../docs/BELKAN_WAR_SOURCES.md) |

| File | Role |
| --- | --- |
| `framework.py` | Six-node branch compiler: focuses, policies, funded services, narrative, defined texts, weekly and interruption hooks; `empty_wave` for owner-only waves |
| `registry.py` | The registered wave modules, in build order |
| wave modules | Branches, owner (dated events, flags, ideas, decisions, hooks by on_action, AI strategy, projects) and registry declarations: `KEY`, `NAME`, `IMPORTS` or `TREES` (`COUNTRIES` for extra category art), `LEDGER`, `SOURCES`, `NEWS_ART`, `EVENT_ART`, `OWNER_ART`, `PROJECT_ART` |
| `build.py` | Writes script, localization, new trees and the import blocks in existing trees; writes `manifest.json` |
| `build_art.py` | Writes DDS textures, `interface/ac_content_waves.gfx`, `assets.json`, event masters and galleries |
| `refresh_records.py` | Regenerates the shared country registry, decision-row bounds, event-style measurements and decision-category text measurements after content changes |
| `test_waves.py` | Source checks and actual-script offline runtime tests |

```text
python -B tools/content_waves/build.py              # regenerate script and localization
python -B tools/content_waves/build_art.py          # regenerate artwork (Pillow 11.3.0)
python -B tools/content_waves/refresh_records.py    # refresh the shared review records
python -B tools/content_waves/build.py --check      # read-only
python -B tools/content_waves/build_art.py --check
python -B tools/content_waves/refresh_records.py --check
python -B tools/content_waves/test_waves.py
```

Dated content cites the [official lore record](../../docs/research/STRANGEREAL_LORE_1991_2020.md),
regenerated with `python -B tools/lore/chronicle_index.py`.

Edit a wave module, then regenerate script, artwork and the shared records and
commit them together. Existing trees keep their own generators:
`tools/build_continental_war.py` preserves the `OVERSIGHT YEARS` and
`LIGHTHOUSE WAR` blocks in `ERU.txt`/`FCU.txt`, and `tools/anea/build_campaign.py`
preserves the `ESTOVAKIAN FRACTURE` block in `EVA.txt`/`EMM.txt`. This generator
owns those blocks' contents; a later wave attaches its block to the tree as the
earlier waves rewrote it. An owner may declare `projects` and `project_tags`,
written to its own files under `common/special_projects/`. Values are provisional gameplay unless the source ledger says
a row is official.
