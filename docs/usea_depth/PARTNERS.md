# Usea Depth: Usean partners

Package `partners` of [Usea Depth](README.md): San Salvacion (SNS), Amber (AMB), Ugellas (UGE) and Delarus (DEL). Event namespace `ac_ud_up`, marker `USEA DEPTH PARTNERS`, nodes at x 28–94 in the existing partner trees (`ac_up_sns_tree`, `ac_up_amb_tree`, `ac_up_uge_tree`, `ac_up_del_tree`).

**Native status: not tested in HOI4.** Every check below is static or offline. Native acceptance remains under #8.

## Contents

| Country | New focuses | Events | Provisional political paths (player only) | AI default |
| --- | --- | --- | --- | --- |
| San Salvacion | 80 | 16 (`ac_ud_up.1`–`.16`) | Charter Assembly; Civil Protection Directorate; District Water Councils | Keep the National Administration |
| Amber | 60 | 12 (`.17`–`.28`) | Chartered Development Board; Labour Compact Cabinet; Sovereign Contracts League | Keep the Contracting Cabinet |
| Ugellas | 60 | 12 (`.29`–`.40`) | Reserve Council; Federal Parliament | Keep the National Administration |
| Delarus | 60 | 12 (`.41`–`.52`) | Inspectorate Cabinet; Command Council | Keep the Present Government |
| **Total** | **260** | **52** | 10 governments | |

Each tree runs in era lanes. Each lane opens with a long-form event and splits into mutually exclusive choices:

- **Politics, 1991:** a root question, a continuity lane and two or three regime paths.
- **Treaty role or neutrality, 1991–1998:** the official anchors below gate it.
- **Ulysses preparation and relief, 1996–2002:** shelter or dispersal, open or rationed relief, and settlement or transit for refugees.
- **Wartime exposure, 2003–2005:** San Salvacion's occupation or free districts, then liberation, the Erusean settlement or the armistice.
- **Postwar reconstruction:** gated by `ac_ud_partners_postwar`, which also opens if the war is averted.

### Files

The package owns these files:

- `tools/usea_depth/partners/`: `content.py`, `narrative*.py`, `build.py`, `build_art.py`, `test_partners.py`, `budget.json`, `assets.json`
- `mod/2985041246/`:
  - `common/{national_focus,ideas,scripted_effects,scripted_triggers,characters}/ac_ud_partners.txt`
  - `events/ac_ud_partners.txt`
  - `localisation/english/ac_ud_partners_l_english.yml`
  - `interface/ac_ud_partners.gfx`
  - `gfx/AC_usea_depth/partners/**`

### Mechanics

- **Existing partner contract.** Rewards add to the partner programme's indices (`ac_up_<tag>_<axis>`) and to the bounded `ac_up_preparedness` credit, which only counts before 8 July 1999. The owner's `ac_up_bound` and `ac_up_recalculate` then clamp and recalculate them. Neither variable is redefined.
- **Spirits.** National spirits (`<TAG>_ud_*_spirit`) are swapped or dropped as eras change.
- **Small rewards.** A few rewards are one-use technology bonuses, army experience, or stability and war-support changes.
- **Not used:**
  - factories, buildings or equipment
  - political-power grants
  - decisions
  - fiscal calls

## Source ledger

Layers follow [CANON_POLICY.md](../CANON_POLICY.md). Chronicle citations are to the [official ACES Chronicle](https://acecombat.jp/en/chronicle/details/) and [Super Weapons](https://acecombat.jp/en/chronicle/weapons/), as compiled in [USEAN_CONTINENTAL_WAR.md](../USEAN_CONTINENTAL_WAR.md).

| Claim or content | Source layer | Exact citation or reference | Affected IDs | Status |
| --- | --- | --- | --- | --- |
| Robert Tyler's FCU Army Southern District eliminates a rebel base in the Skully Islands. Unified Command defeats the rebels with Scarface Squadron. | Official | Chronicle, 1995 / 12.31 | `SNS_ud_skully_islands_watch` (gate `date > 1995.12.30`), `ac_ud_up.7` | Static. San Salvacion's border response is provisional gameplay. Tyler and Scarface are named in text only. |
| Central Usea announces that Ulysses will strike the Earth. | Official | Chronicle, 1996 / 04.20 | Gate `date > 1996.4.19`. Focuses `SNS_ud_read_the_warning`, `AMB_ud_warning_contracts`, `UGE_ud_warning_reserves`, `DEL_ud_warning_dockets`. Events `ac_ud_up.8`, `.23`, `.34`, `.46` | Static. Every national response is provisional gameplay. |
| A coup breaks out across Usea and is defeated by Unified Command with Scarface 1. | Official | Chronicle, 1997 / 05.30 | Gate `date > 1997.5.29`. Focuses `SNS_ud_coup_night`, `AMB_ud_coup_contracts`, `UGE_ud_coup_depots`, `DEL_ud_coup_dockets`. Events `.9`, `.24`, `.35`, `.47` | Static. No rebel country, arrest list or border change. The events inside each partner are provisional. |
| Stonehenge is an FCU-led international project of eight railguns in a desert region of neutral San Salvacion, completed 19 June 1998. | Official | Chronicle, 1998 / 06.19; Super Weapons, Stonehenge | SNS host lane: `SNS_ud_host_terms` through `SNS_ud_host_ledger`, gates `warn` and `henge`, events `.10`, `.11`. Also `AMB_ud_battery_service_bids`, `UGE_ud_battery_and_the_reserve` (`.36`) and `DEL_ud_battery_verification` (`.48`) | Static. **No construction dates.** The host terms are provisional and open after the warning, matching the existing provisional `ac_sp_stonehenge` gate. No state is scoped. State 310 is only read through the `ac_ucw` owner's flags. |
| Ulysses passes the Roche limit (the impact). | Official | Chronicle, 1999 / 07.08 | Gate `date > 1999.7.7`. Preparation records are bypassed afterwards (gate `date < 1999.7.8`). Focuses `*_impact_*`; events `.12`, `.25`, `.37`, `.49` | Static. Relief policies are provisional. |
| Erusea stops taking in refugees. | Official | Chronicle, 2000 / 04.21 | Gate `date > 2000.4.20`. Refugee lanes; events `.13`, `.26`, `.38`, `.50` | Static. The refugee routes to the partners and their policies are provisional. |
| Erusea invades neutral San Salvacion and seizes Stonehenge, summer 2003. | Official, season only | Chronicle, 2003 / SUMMER | Read-only gates `ac_ucw_war_started` and `ac_ucw_stonehenge_seized`. Focuses `SNS_ud_invasion_summer`, `SNS_ud_free_districts` / `SNS_ud_quiet_ministries`, `AMB_ud_war_comes_to_the_yards`, `UGE_ud_reserves_called`, `DEL_ud_war_obligations`. Events `.14`, `.27`, `.39`, `.51` | Static. The start day belongs to the `ac_ucw` owner. Amber, Ugellas and Delarus are at war through their FCU faction membership, which is mod provenance. |
| The Stonehenge engineers and their families escape Erusean custody. | Official | Chronicle, 2005 / 03.14 | `SNS_ud_engineers_families`, read-only gate `ac_ucw_brief_engineers` | Static. Their route through San Salvacion is provisional. |
| ISAF destroys Stonehenge; seven of the eight batteries are destroyed. | Official | Chronicle, 2005 / 04.02; Super Weapons, Stonehenge | `ac_ud_up.16` text | Static. The text covers both the historical course and the alternatives. The site's future is provisional. |
| San Salvacion is liberated. | Official | Chronicle, 2005 / 07.10 | `SNS_ud_liberation_day`, read-only gate `ac_ucw_brief_san_salvacion` or `ac_ucw_outcome_isaf_victory`; `ac_ud_up.15` | Static |
| Erusean victory and armistice outcomes | Provisional gameplay on the `ac_ucw` outcome flags | [USEAN_CONTINENTAL_WAR.md](../USEAN_CONTINENTAL_WAR.md), Track A outcomes | `SNS_ud_erusean_settlement`, `SNS_ud_armistice_watch` | Static. These are explicit alternate branches and are never presented as history. |
| San Salvacion's neutrality | Official for neutrality. Mod provenance for its FCU faction membership. | Chronicle, 1998 / 06.19 and 2003 / SUMMER ("neutral San Salvacion"); `history/countries/FCU - Central Usea.txt` | `SNS_ud_neutral_ledger`, `SNS_ud_usean_correspondence`, `SNS_ud_neutral_again` | The text treats neutrality as a policy and never claims San Salvacion is outside a bloc. The faction difference is already recorded in USEAN_CONTINENTAL_WAR.md. |
| San Salvacion's 1991 national administration governs without elections. | Mod provenance | `history/countries/SNS - San Salvacion.txt` (`elections_allowed = no`); `SNS_ac_government_office` in `tools/usea_expansion/leaders.json` | `SNS_ud_national_question`, `ac_ud_up.1`, `ac_ud_up.5` | Static. The administration's internal debate is provisional. |
| Delarus's sitting government | Mod provenance | `history/countries/DEL - Delarus.txt` (`ruling_party = neutrality`) | `DEL_ud_keep_the_present_government`, `ac_ud_up.44` | Static. The text names no leader. |
| All Amber, Ugellas and Delarus content: politics, treaty roles, relief, wartime exposure and postwar | Provisional gameplay | No official source covers these countries. Authored in `tools/usea_depth/partners/content.py` and `narrative_*.py`. | All `AMB_ud_*`, `UGE_ud_*`, `DEL_ud_*` | Static. Every event ends in a source-layer line that says so. |
| Ten provisional governments (below) | Provisional gameplay | `REGIMES` in `content.py`; built with `seams.regime_effect()` and `seams.office_character()` | `ac_ud_partners_regime_*`, `<TAG>_ud_*_office` | Static. These are unnamed offices with generated cards: no faces, flags or captions. |
| Programme indices and preparation credit | Existing contract (provisional gameplay) | `tools/usean_partners/build.py` (`ac_up_bound`, `ac_up_recalculate`, `ac_up_preparedness`) | Reward blocks in `common/national_focus/ac_ud_partners.txt` | Static. Only the owner's two effects are called, guarded by `has_country_flag = ac_up_initialized`. |

## Provisional governments

Each path's opener, middle focus and formation focus have `ai_will_do = { factor = 0 }`. Only the formation focus calls a regime effect, and no event option reaches one. Popularities are seeded only inside these effects. The partner history files stay frozen by `tools/world_foundation/original_four.json`, and no mechanic reads a popularity.

| Effect | Formation focus | Ruling party / sub-ideology | Elections | Office leader | Popularity seed |
| --- | --- | --- | --- | --- | --- |
| `ac_ud_partners_regime_sns_charter` | `SNS_ud_charter_assembly` | democratic / liberalism | yes | `SNS_ud_charter_presidium_office` | democratic 55, neutrality 30, fascism 10, communism 5 |
| `ac_ud_partners_regime_sns_directorate` | `SNS_ud_directorate_formed` | neutrality / conservatism_na | no | `SNS_ud_protection_directorate_office` | neutrality 55, fascism 25, democratic 15, communism 5 |
| `ac_ud_partners_regime_sns_councils` | `SNS_ud_councils_take_office` | communism / democratic_socialism | yes | `SNS_ud_council_committee_office` | communism 45, democratic 25, neutrality 20, fascism 10 |
| `ac_ud_partners_regime_amb_board` | `AMB_ud_development_board` | neutrality / oligarchism | no | `AMB_ud_development_board_office` | neutrality 50, fascism 25, democratic 20, communism 5 |
| `ac_ud_partners_regime_amb_compact` | `AMB_ud_labour_compact_cabinet` | democratic / social_democracy | yes | `AMB_ud_compact_cabinet_office` | democratic 50, communism 20, neutrality 15, fascism 15 |
| `ac_ud_partners_regime_amb_league` | `AMB_ud_league_government` | fascism / ultranationalism | no | `AMB_ud_league_directorate_office` | fascism 60, neutrality 20, democratic 15, communism 5 |
| `ac_ud_partners_regime_uge_council` | `UGE_ud_reserve_council` | neutrality / stratocracy | no | `UGE_ud_reserve_council_office` | neutrality 55, fascism 25, democratic 15, communism 5 |
| `ac_ud_partners_regime_uge_federation` | `UGE_ud_federal_parliament` | democratic / liberalism | yes | `UGE_ud_federal_cabinet_office` | democratic 55, neutrality 20, fascism 15, communism 10 |
| `ac_ud_partners_regime_del_inspectorate` | `DEL_ud_inspectorate_cabinet` | democratic / conservatism | yes | `DEL_ud_inspectorate_cabinet_office` | democratic 50, neutrality 35, communism 10, fascism 5 |
| `ac_ud_partners_regime_del_command` | `DEL_ud_command_council` | fascism / stratocracy_fascism | no | `DEL_ud_command_council_office` | fascism 50, neutrality 35, democratic 10, communism 5 |

## The Continental War still starts

`test_partners.py` runs this package's real script inside the `World` harness from `tools/Test-ContinentalWar.py`. It ticks weekly from 1 January 1991 and lets a deterministic AI take the highest-weighted available focus in each partner tree. It then compares the result with the same harness without this package.

- **War start:** 24 June 2003 in both runs.
- **Grievance:** Erusea's never falls below 45.
- **Governments:** no AI government changes.
- **Flags:** this package writes no `ac_ucw_*` flag.

This is an offline executor, not the engine. It stubs the partner owner's `ac_up_bound` and `ac_up_recalculate` after checking they exist.

## Art

All art is original and code-drawn with the shared glyph library and Pillow 11.3.0. No installed-game pixels are used. `build_art.py` packages:

- **Focus icons:** 260 unique 96×96 icons. Each shine reuses the same texture.
- **Idea icons:** 63, at 75×75.
- **Office cards:** 10, at 156×210.
- **Event scenes:** 11, at 210×176.

Hashes are recorded in `tools/usea_depth/partners/assets.json`.

## Reproduce

Static checks only:

```
python -B tools/usea_depth/partners/build.py
python -B tools/usea_depth/partners/build_art.py
cd tools/usean_partners && python -B build.py
python -B tools/usea_depth/partners/test_partners.py
```
