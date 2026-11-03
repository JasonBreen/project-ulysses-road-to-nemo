# Wave B and Aurelia's foundation: source and implementation ledger

Status: **implemented in source; offline checks pass; native acceptance pending.**
Generator: `tools/content_waves/` (modules `estovakia.py`, `aurelia.py`). Plan:
[CONTENT_PLAN_2006_2020.md](CONTENT_PLAN_2006_2020.md). Sources:
[STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md). No HOI4
installation, profile, save or desktop was touched; native testing remains
paused under issue #8.

| Wave | Country | Tree | Definitions | Horizon | Release-plan effect |
| --- | --- | --- | ---: | --- | --- |
| B | Estovakia (`EVA`) | existing `ac_anea_eva_tree` | 30 | 2007–2013 | 84 of 120; 36 left for Wave E |
| B | Emmeria (`EMM`) | existing `ac_anea_emm_tree` | 18 | 2007–2013 | 72 of 108; 36 left for Wave E |
| Aurelia | Aurelia (`AUR`) | new `aur_national_campaign` | 54 | 1991–2018 | 54 of 84; 30 left for the 2019–2020 crisis lanes |

Counts include mutually exclusive alternatives. The ledger now records **776
delivered and 252 remaining** country additions (`tools/overhaul/release_plan.json`).

## Source layers

| Claim or material | Layer and exact reference | Affected IDs | Status |
| --- | --- | --- | --- |
| Lyes Faction seizes the capital, 3 April 2007 | Official: Chronicle, 2007 / 04.03 | `ac_ecw_begin`, `ac_ecw.1`, flag `ac_ecw_capital_seized` | Implemented |
| Civil war begins, 30 June 2007 | Official: Chronicle, 2007 / 06.30 | `ac_ecw.2`, flag `ac_ecw_war_running` | Implemented |
| Eastern Faction takes the northeastern oil platforms, 15 July 2008 | Official: Chronicle, 2008 / 07.15 | `ac_ecw.3`, flag `ac_ecw_stage_oil` | Implemented; the faction's gain depends on the Estovakian oil lane |
| Republic of Anea Initiative put on hold, 23 October 2008 | Official: Chronicle, 2008 / 10.23 | `ac_ecw.4`, flag `ac_ecw_anea_initiative_on_hold` | Implemented; news fires only if the Anean bureau or accord exists. No `ac_anea_*` state is written |
| Emmeria ends aid for the LUF's reconstruction programme, 19 February 2010 | Official: Chronicle, 2010 / 02.19 | `ac_ecw.5` (Emmeria), flags `ac_ecw_emm_aid_ended_luf` / `ac_ecw_emm_aid_conditional` | Historical option (AI always); conditional continuation is an earned alternative |
| Emmeria ends aid for Estovakia's reconstruction, 9 May 2011 | Official: Chronicle, 2011 / 05.09 | `ac_ecw.6` (Emmeria), flags `ac_ecw_emm_aid_ended_all` / `ac_ecw_emm_channel_kept` | Historical option (AI always); a humanitarian channel is an earned alternative |
| Eastern Faction offensive; LUF loses about 80 percent of its territory, 15 January 2013 | Official: Chronicle, 2013 / 01.15 | `ac_ecw.7`, flag `ac_ecw_stage_offensive` | Implemented as a loss of LUF authority; no map change |
| General Lyes killed; the civil war ends, 29 October 2013 | Official: Chronicle, 2013 / 10.29 | `ac_ecw_end_historical`, `ac_ecw.9` | Historical outcome |
| Aftermath: Arensky attacked (2013 / 11.25), his death withheld (12.02) and announced with Koznick named (2014 / 02.03); the Vistoc attack (2014 / 02.04) | Official: Chronicle entries as dated | `ac_ecw.10`–`.12` | News only, after the historical end; no character, leader or portrait |
| Chandelier incomplete when Ulysses arrived | Official: Super Weapons, Chandelier | `EVA_ecw_chandelier_*` | Custody only; weaponization belongs to Wave E |
| Factions and people: the Lyes United Front, the Eastern Faction, the Northern Highlands Faction, General Lyes, Isaac Arensky, Antonina Koznick | Official, as the Chronicle names them | News text only | Not units, characters or tags |
| Negotiated settlement; prolonged war; authority and strength values; every focus, policy, service, dialogue and number | Provisional gameplay | `ac_ecw_*`, `EVA_ecw_*`, `EMM_ecw_*` | Implemented and labelled in-game where it diverges from the record |
| Aurelia's foundation, 1991–2018 | Mod provenance (history, office, world start, institution profile) plus provisional gameplay | `AUR_au_*`, `ac_aur_*` | Implemented. The Chronicle names Aurelia only for 2020; no 2020 place, person or weapon is used |
| Leasath's complaint about trade terms | Context from Chronicle, 2020 / 10.XX ("years of exploitation"), recorded as Leasath's claim | `AUR_au_trade_*` | The lane reviews the terms; the game does not rule on the claim, and the word itself is not used |
| Leasath civil war, about 2009–2019 | Derived from Chronicle, 2019 / XX.XX ("after 10 years of fighting") | `AUR_au_leasath_war_*` (from 2010) | Context only; Leasath's own content belongs to Wave F2 |

## Wave B owner (`ac_ecw`), tagless

- **State:** two Estovakian variables, LUF authority (starts at 75) and Eastern
  Faction strength (starts at 20). Idea tiers by authority: the LUF holds the
  capital (60 or more), a divided country (30–59), the LUF in retreat (below 30).
- **Start:** the first Estovakian weekly pulse on or after 3 April 2007. A first
  observation on or after 3 April 2008 closes the owner without replaying it
  (`ac_ecw_late_start_skipped`).
- **Stages, each once, while the owner runs:**

  | Date | Effect |
  | --- | --- |
  | 30 June 2007 | War begins; authority −5 |
  | 15 July 2008 | Eastern strength +15 and authority −5, or only +5 if Estovakia took the platforms into state custody first |
  | 23 October 2008 | Anea Initiative on hold |
  | 19 February 2010 | Emmerian aid decision; ending it costs the LUF 5 authority |
  | 9 May 2011 | Emmerian aid decision |
  | 15 January 2013 | Offensive: authority −40 if Eastern strength is 30 or more, otherwise the prolonged war begins |
  | 29 October 2013 | Historical end if authority is below 40, otherwise the prolonged war begins |

- **Policies:** accommodation lowers authority (−5, Eastern −3); suppression raises
  it (+8, Eastern +5); the cities lane has smaller versions (−2/−1 and +3/+3).
- **Negotiated settlement (earned):** the Estovakian decision
  `EVA_ecw_negotiate` needs the negotiated-settlement course, an accommodating
  government, either Emmerian conditional aid or Anean recovery of 40 or more,
  and Eastern strength of 20 or more. It costs 50 political power and ends the war
  without the historical aftermath news.
- **Prolonged war (provisional):** authority drifts down 0.1 a week (0.05 under
  suppression) and Eastern strength rises 0.05; the war ends when authority falls
  below 20 (`ac_ecw.13`) or by negotiation.
- **Closure:** annexation, capitulation or subject annexation of Estovakia closes
  the owner and removes the tiers.
- **Attachment:** the Estovakian and Emmerian branches join the existing Anea
  trees through a `# BEGIN ESTOVAKIAN FRACTURE IMPORTS` block, which
  `tools/anea/build_campaign.py` now preserves. New rows start at y 31.

**Branches:**
- **Estovakia:** authority in the capital; the cities that resisted; the
  northeastern platforms; the unfinished railgun (custody only); talks across
  the lines (from 2010).
- **Emmeria:** conditions for reconstruction aid; the eastern border; the
  suspended Anea Initiative (opens only after it is put on hold).

## Aurelia

| Stage | Opens | Branches |
| --- | --- | --- |
| 1 | 1991 | public services; the southern trade relationship; weather and air warning |
| 2 | 2006, after any stage-1 settlement | the war in Leasath (from 2010); development finance; arms export and procurement rules |
| 3 | 2014, after any stage-2 settlement | relations with Leasath; a readiness review; the public account |

The new tree is selected for Aurelia at game start (weight 45, above the regional
framework's 5). Saves holding the generic or regional tree can adopt it with
`AUR_au_adopt_campaign` under the shared idle guard. The relations and readiness
policy flags (`AUR_au_relations_policy_a_done`, `..._policy_b_done`,
`AUR_au_readiness_policy_a_done`, `..._policy_b_done`) are the hand-off interface
for the 2019–2020 crisis lanes.

## Shared shape, counts and artwork

Every branch follows the reviewed six-node shape with two funded 90-day services
paid through the real P1 owners. Policy choices that move the civil war use the
framework's new `policy_effects`; Waves A and D are unchanged by it.

| Content | Wave B | Aurelia |
| --- | --- | --- |
| Events | 34 (20 narrative, 12 news, 2 Emmerian decisions) | 20 |
| Ideas | 77 | 76 |
| Decisions | 19 | 20 |
| Words of original English text | about 11,500 | about 10,400 |

The two modules add 323 original DDS textures, generated in code from the
existing glyph library (643 across all waves): 102 focus icons, 153 idea icons,
39 decision rows, three categories, 20 event pictures and six news pictures. New
frames and colours distinguish Estovakia, Emmeria and Aurelia.

## Validation

```text
python -B tools/content_waves/build.py --check
python -B tools/content_waves/build_art.py --check
python -B tools/content_waves/test_waves.py
python -B tools/content_waves/refresh_records.py --check
python -B tools/anea/build_campaign.py --check
python -B tools/overhaul/check_release_plan.py
python -B tools/world_foundation/test_foundation.py
```

`test_waves.py` has 30 tests across all waves.

**Wave B and Aurelia runtime cases**, executed through the real P1 owners:
- the civil war starts on its anchor, and late saves never replay it;
- the historical chain fires each anchor once, ends on 29 October 2013 and
  leaves every `ac_anea_*` and `EVA_an_*` flag untouched;
- the Emmerian alternatives need the conditional-aid policy, and the AI follows
  history;
- the negotiated settlement is earned, not free;
- a weak Eastern Faction gives the prolonged war, which never shows the
  historical aftermath;
- policies move the balance, and annexation closes the owner;
- Aurelia's stage dates and prerequisites, adoption and hand-off flags behave
  as described.

The service, policy and settlement tests cover every branch in full,
experimental and disabled fiscal modes.

**Other checks:**
- The existing focus-screen, Anea campaign/integration/systems/art,
  asset-dependency, presentation, startup-chronology, institutions and overhaul
  checks pass in the Linux session.
- The shared records were regenerated: decision rows 1,015 → 1,054 variants,
  event style 2,376 → 2,484 fields, with no clipping and additions only.

These are source and offline checks, not native acceptance.

## Open items

- Native parsing, focus-screen rendering, AI pacing, balance and save/reload (#8).
- Wave E (Emmeria–Estovakia War); Wave F1 (Lighthouse War); Wave F2 (Leasath and the
  2019–2020 crisis lanes). Wave C is delivered in [CONTENT_WAVE_C.md](CONTENT_WAVE_C.md).
