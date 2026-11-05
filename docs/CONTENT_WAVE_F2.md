# Wave F2, Leasath and the Aurelia–Leasath war: source and implementation ledger

Status: **source delivered, offline validated, native untested (#8).** Two
modules through the content-wave framework: `tools/content_waves/leasath.py`
(F2a) and `tools/content_waves/southern_theater.py` (F2b). Every focus, policy,
service, dialogue, idea value, window and decision is **provisional gameplay**.

| Wave | Countries | Tree | Definitions | Horizon | Release-plan effect |
| --- | --- | --- | ---: | --- | --- |
| F2a | Leasath (`LEA`) | new national tree `lea_national_campaign` (`LEA.txt`) with an adopt decision | 42 | 1991–2019 | — |
| F2b | Aurelia (`AUR`), Leasath (`LEA`) | `SOUTHERN THEATER` import blocks in `AUR.txt` and `LEA.txt` | 60 (AUR 30, LEA 30) | 2019–2020 | Aurelia 84 of 84 and Leasath 72 of 72; the ledger reaches **1,028 delivered and 0 remaining** |

## Source layers

| Claim or material | Layer and exact reference | Affected IDs | Status |
| --- | --- | --- | --- |
| The Leasath Civil War ends after ten years of fighting | Official: Chronicle, 2019 / XX.XX | owner `ac_lcw`, `ac_lcw.1`–`.6`, idea `ac_lcw_civil_war`, variable `ac_lcw_authority`, decision `LEA_le_negotiate_settlement` | The 2009 start is **derived** from "ten years". The historical end comes within 2019 only when the government's authority (raised by the civil-war branches) reaches 50; never before 2019. Prolonged and earned negotiated endings are provisional. The record names no winner; none is named |
| Leasath declares war on Aurelia citing years of exploitation and invades with the Gleipnir; almost all of Aurelia falls | Official: Chronicle, 2020 / 10.XX; Abstracts and Product, ACE COMBAT X | `ac_alc_declare`, `ac_alc.5` (AI always), `ac_alc.1`, `ac_alc.15`, `ac_alc.20`, ideas `ac_alc_lea_gleipnir_over_aurelia`, `ac_alc_aur_griswall_occupied` | The route needs the civil war over (any ending). The declaration comes in October (no day). The grievance is quoted as Leasath's stated claim. The Gleipnir flies only if its project was built; the occupation is reported only when Leasath controls Griswall (state 120) |
| Aubrey Base holds; Port Patterson; the Gleipnir shot down and Santa Elva; Sachana Air Base | Official: Chronicle, 2020 / 10.XX, 11.XX, 11.XX, 12.XX | `ac_alc.21`–`.24` | Month windows: each fires on the first observation inside its month or is skipped. Port Patterson and Sachana need the observed occupation; the Gleipnir needs the project. Places are unmapped |
| Griswall retaken; Leasath regroups at Archelon | Official: Chronicle, 2020 / XX.XX | `ac_alc.25` | No month: fires when Aurelia controls its capital again after the observed occupation |
| Archelon destroyed; Diego Navarro removed; the war ends | Official: Chronicle, 2020 / 12.XX; Abstracts, ACE COMBAT X | `ac_alc.26` (idea `ac_alc_lea_commander_removed`), `ac_alc.27` (only if built), `ac_alc.6`, `ac_alc_sign_ceasefire`, `ac_alc.7` | The scripted ceasefire follows the removal (the Wave E pattern), written only if the engine ended the war. Navarro is named in text only; no politics change |
| Gleipnir; Archelon Fortress | Official: Super Weapons | projects `ac_sp_gleipnir`, `ac_sp_archelon` (LEA), ideas `ac_sp_gleipnir_fortress`, `ac_sp_archelon_works`, fallbacks, tag `ac_sp_tag_aerial_fortress` | Gated on Leasath's army defined (`LEA_le_army_operations_done`) and its front held (`LEA_le_front_operations_done`); cancelled on their sourced loss; never deployed |
| Nevera Jammer; Meson Cannons; Gandr; Fenrir | Official: Super Weapons | none | Reference only: no dates and no mapped places |
| The withheld declaration, early settlement, fighting on, every branch | Provisional gameplay | `ac_alc_withhold`, `AUR_sw_early_settlement`, `ac_alc_fight_on`, `AUR_sw_*`, `LEA_sw_*`, `LEA_le_*` | Implemented and labelled in-game |
| Aurelia's foundation records | Mod provenance, read only | `AUR_au_relations_policy_a_done`, `AUR_au_readiness_settlement_done` | Part of the earned withholding with Leasath's `LEA_sw_restraint_policy_a_done` |

Naming: the Super Weapons record calls Leasath the "Democratic Republic of
Leasath"; the mod's democratic name is "Federal Republic of Leasath" and its
communist name "Democratic Republic of Leasath". The names are recorded, not
changed. Aurelia's foundation (`aurelia.py`) stays free of every 2020 name.

## The owners

- **`ac_lcw` (tagless civil war).** Opens on the first observation in 2009;
  a first observation in 2010 or later closes it without a war. The
  government's authority starts at 40 and rises with the civil-war branches'
  policies and settlements. In 2019, at 50 or more, the war ends historically;
  if 2019 passes, it is prolonged until authority reaches 50 (late end); the
  talks branch's policy A and funded rounds earn a negotiated settlement at
  any time. A capitulation or annexation of Leasath closes it as interrupted.
- **`ac_alc` (the 2020 war).** Opens in September 2020 if both countries exist
  and the civil war is over; a civil war still being fought closes it as
  unreachable; a first observation after October replays nothing. The stages,
  external observation, capitulation outcomes and survivor news follow the
  F1/E pattern.

## Verification (static/offline)

```text
python -B tools/content_waves/build.py --check
python -B tools/content_waves/build_art.py --check        # pinned Pillow 11.3.0
python -B tools/content_waves/test_waves.py               # 70 tests, five for F2
python -B tools/Test-StrangerealProjects.py               # 12 projects
python -B tools/overhaul/check_release_plan.py            # 1,028 of 1,028
python -B tools/content_waves/refresh_records.py --check
```

Native parsing, AI pacing, balance and save/reload are untested (#8). The
Aurelian and Leasathian stories (release plan `later_story_hosts`) are a
separate component, [`tools/squadrons/southern`](../tools/squadrons/southern/README.md):
text and script complete and tested offline, not admitted until their art
masters are generated and reviewed.
