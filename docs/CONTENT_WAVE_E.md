# Wave E, the Emmeria–Estovakia War: source and implementation ledger

Status: **source delivered, offline validated, native untested (#8).** Generated
by `tools/content_waves/anean_war.py` through the content-wave framework; every
focus, policy, service, dialogue, idea value, window and decision is
**provisional gameplay**.

| Wave | Countries | Tree | Definitions | Horizon | Release-plan effect |
| --- | --- | --- | ---: | --- | --- |
| E | Emmeria (`EMM`), Estovakia (`EVA`) | `ANEAN WAR` import block in `EMM.txt` and `EVA.txt`, after the `ESTOVAKIAN FRACTURE` block | 72 (EMM 36, EVA 36) | 2014–2016 | Emmeria 108 of 108 and Estovakia 120 of 120 delivered; the ledger moves to **926 delivered and 102 remaining** |

## Source layers

| Claim or material | Layer and exact reference | Affected IDs | Status |
| --- | --- | --- | --- |
| Yuktobanian spy satellites spot a massive aircraft signature off Estovakia's southeast coast, 21 April 2015 | Official: Chronicle, 2015 / 04.21 | `ac_eew.16`, flag `ac_eew_signature_seen` | News inside a 30-day window; the signature is not attributed |
| Estovakia invades Gracemeria; the Aigaion cannot be countered; Emmerian forces retreat to western Anea; the war begins, 30 August 2015 | Official: Chronicle, 2015 / 08.30; Abstracts, ACE COMBAT 6 | `ac_eew_declare`, `ac_eew.5` (Estovakian decision event, AI always), `ac_eew.1`, `ac_eew.20`, idea `ac_eew_emm_capital_occupied` | The owner's only declaration. The capital's fall is reported only when Estovakia controls Emmeria's capital (state 154). No reason is asserted |
| Fireballs attack retreating Emmerian forces, November 2015 (no day) | Official: Chronicle, 2015 / 11.XX | `ac_eew.21` | Reported inside November 2015 only; skipped if the month passes. The Chronicle does not say what they were, so the brief is not tied to the Chandelier project |
| Vitoze intercept, Sipli Field, Bartolomeo Fortress and Khesed Island, Rargom Beach, the Selumna Peaks, Cavallia, Ragno Fortress, the Moloch Desert, Fort Norton | Official: Chronicle, 2015 / 11.24, 11.27, 12.27; 2016 / 01.26, 02.12, 02.15, 03.06, 03.25, 03.26 | `ac_eew.22`–`.27`, `.29`–`.31`; ideas `ac_eew_emm_khesed_secured`, `ac_eew_eva_moloch_retreat` | News on the untainted course, two timed ideas. None of these places is mapped; no territory changes hands by script |
| The Emmerian Air Force destroys the Aerial Fleet, 20 February 2016 | Official: Chronicle, 2016 / 02.20; Super Weapons, Aigaion, Kottos, Gyges | `ac_eew.28`, flag `ac_eew_aerial_fleet_lost` | Reported only if `ac_sp_aerial_fleet` was completed; its reward is removed and the project can never complete afterwards |
| Gracemeria liberated; cruise missiles shot down that night, 31 March 2016 | Official: Chronicle, 2016 / 03.31; Abstracts, ACE COMBAT 6 | `ac_eew.32` | Only when Emmeria controls its capital again after the observed fall; the occupation idea is removed |
| The Chandelier destroyed on Sonne Island; Gustav Dvornik dies; an antigovernment coup leaves Estovakia unable to fight; a ceasefire agreement follows, 1 April 2016 | Official: Chronicle, 2016 / 04.01; Abstracts, ACE COMBAT 6; Super Weapons, Chandelier | `ac_eew.33` (coup, idea `ac_eew_eva_coup`), `ac_eew.34` (only if `ac_sp_chandelier` was completed), `ac_eew_ceasefire_tick`, `ac_eew.6` (Estovakian decision event, AI always signs), `ac_eew_sign_ceasefire`, `ac_eew.7` | **User decision (5 November 2026): scripted ceasefire.** Written only if the engine actually ended the war (`ac_eew_ceasefire_not_made` otherwise). The coup changes no politics; Dvornik is named in text only |
| Aerial Fleet (Aigaion, Kottos, Gyges) and the Chandelier | Official: Super Weapons, Aigaion, Kottos, Gyges, Chandelier | projects `ac_sp_aerial_fleet`, `ac_sp_chandelier` (EVA); ideas `ac_sp_aerial_fleet_initiative`, `ac_sp_chandelier_railgun`; fallbacks `ac_superweapons_aerial_fleet`, `ac_superweapons_chandelier`; tags `ac_sp_tag_aerial_fleet` (new), `ac_sp_tag_railgun` (Track C) | **User decision: projects.** The Aerial Fleet needs the Eastern Faction's victory and the maintenance base rebuilt (`EVA_ew_logistics_operations_done`); the Chandelier needs its files reopened and a funded construction period (`EVA_ew_chandelier_operations_done`). Both are cancelled on their sourced destruction. Never deployed or fired by script |
| The withheld invasion, the divergent and unreachable routes, the early settlement, fighting on, every branch | Provisional gameplay | `ac_eew_withhold`, `ac_eew.2`, `ac_eew.14`, `EMM_ew_early_settlement`, `ac_eew_fight_on`, `EMM_ew_*`, `EVA_ew_*` | Implemented and labelled in-game |
| Estovakian civil war record; Anea accord, bureau and Nordennavic consultation; Wave B and Anea focus records | Mod provenance, read only | `ac_ecw_eastern_victory`, `ac_ecw_negotiated`, `ac_ecw_running`, `ac_anea_accord`, `ac_anea_bureau`, `ac_anea_nec_participates`, `EMM_ecw_aid_policy_a_done`, `EVA_ecw_talks_policy_a_done`, `EVA_ecw_chandelier_policy_b_done`, `EVA_an_chandelier_research_done` | Read, never written. The Anea flags are snapshotted at the calendar opening into `ac_eew_had_accord`, `ac_eew_had_bureau` and `ac_eew_nec_consulted`, because `ac_anea_daily` clears them once the pair is at war |

Reference only, not scripted: Ed Alverez and the Gavial battalion (2015 / 06.10),
Freddie Durand (2015 / 09.12), Garuda Team and every pilot.

## The owner (`ac_eew`)

- **Calendar.** Opens on 20 April 2015 when both countries exist and the
  sourced route holds (the Eastern Faction won Estovakia's civil war,
  `ac_ecw_eastern_victory`). A negotiated civil war closes the owner as
  `ac_eew_route_divergent` and publishes `ac_eew.14`; any other civil-war state
  closes it as `ac_eew_route_unreachable`. A first observation on or after
  30 August 2015 closes it as `ac_eew_late_start_skipped` and replays nothing.
- **Invasion.** On 30 August Estovakia receives `ac_eew.5` (fourteen-day window,
  AI always invades). The state is written only if the engine created the war;
  otherwise `ac_eew_declaration_refused`. A war the pair already fights is
  observed (`ac_eew.3`); a third party at war with either moves the owner to
  external observation (`ac_eew.4`) and stops the dated news.
- **Earned withholding.** Option `ac_eew.5.b` needs Estovakia's civil-war talks
  settled on a negotiated peace, Emmeria's aid kept with monitors, and the
  snapshot of the Anea accord or Nordennavic's consultation
  (`ac_eew_restraint_earned`).
- **Stages.** Each fires once on the untainted course, in its source order;
  the capital's fall and liberation, the Aerial Fleet and the Chandelier are
  state-gated as above.
- **Ceasefire.** After the coup stage, Estovakia receives `ac_eew.6`; the
  fallback signs after fourteen days. Emmeria's earned early settlement
  (`EMM_ew_early_settlement`) needs the liberation and the return with terms as
  policy. Fighting on (`ac_eew.13`) and engine refusal are recorded honestly.
- **Ends.** Capitulation to the other principal (`ac_eew.9`, `.10`), the
  ceasefire (`ac_eew.7`; `ac_eew_historical_course` after the coup on the
  untainted course), the early settlement (`ac_eew.8`), or cessation (`.11`,
  `.12`). War ideas are removed at the end.

## The branches

| Branch | Gate | Notes |
| --- | --- | --- |
| `EMM_ew_evacuation` | 2015 | Registers, district evacuation or shelter, the western rail corridor |
| `EMM_ew_administration` | the war started | Government abroad or in the western provinces |
| `EMM_ew_reserve` | the war started | The western reserve: volunteers or call-up |
| `EMM_ew_airforce` | the war started | Fighters first or bases first |
| `EMM_ew_liberation` | the war started | Return with or without terms; policy A earns the early settlement |
| `EMM_ew_peace` | the invasion withheld or the route divergent | A peace that held |
| `EVA_ew_government` | the war started | Rule by the general staff or the cabinet |
| `EVA_ew_logistics` | the Eastern Faction's victory | The maintenance base; `operations_done` gates the Aerial Fleet |
| `EVA_ew_chandelier` | 2015 and the retained research team (Wave B policy B or the Anea research focus) | First purpose or weapon; `operations_done` gates the project, `settlement_done` weights its reward |
| `EVA_ew_occupation` | the war started | Humanitarian or martial administration |
| `EVA_ew_aftermath` | the coup stage | Transitional government or officers |
| `EVA_ew_republic` | the invasion withheld or the route divergent | Federal reconciliation or a centralised republic |

## Verification (static/offline)

```text
python -B tools/content_waves/build.py --check
python -B tools/content_waves/build_art.py --check        # pinned Pillow 11.3.0
python -B tools/content_waves/test_waves.py               # 65 tests, six for Wave E
python -B tools/anea/build_campaign.py --check            # both import blocks preserved
python -B tools/Test-StrangerealProjects.py               # 10 projects
python -B tools/overhaul/check_release_plan.py
python -B tools/content_waves/refresh_records.py --check
```

Native parsing, AI pacing, balance and save/reload are untested (#8).
