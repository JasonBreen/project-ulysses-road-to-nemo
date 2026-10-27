# Ulysses fallout and the Usean Continental War — source ledger

Status: **sources and contracts only.** No event, focus, decision or project
described here is implemented yet. This ledger gates the next content round
(Ulysses fallout 2000–2003, Continental War 2003–2005, North Point/Recta/
Yuktobania roles and Strangereal special projects). A date or claim may be
scripted only if it appears below with an official source; everything else is
provisional gameplay and must be labelled as such.

Primary sources, accessed 27 October 2026:

- [Official ACES Chronicle — Details](https://acecombat.jp/en/chronicle/details/), cited as *Chronicle, YYYY / MM.DD*.
- [Official ACES Chronicle — Super Weapons](https://acecombat.jp/en/chronicle/weapons/), cited as *Super Weapons, &lt;name&gt;*.

Entries are paraphrased. "Planned content" names the intended namespace or
track; IDs are reserved, not yet defined.

## Chronology, 1994–2005

| Claim | Layer and exact source | Planned content | Disposition |
| --- | --- | --- | --- |
| Belka completes Excalibur, 23 December 1994; conceived under the 1981 ballistic-missile-defence program | Official; Chronicle, 1994 / 12.23; Super Weapons, Excalibur | Track C `ac_sp_excalibur` | Reference for project framing. The inherited focus-built Excalibur (`BLK_excalibur`, `AWW_excalibur`) and its decisions stay mod provenance. |
| Belkan V2 mass-retaliation plans discovered, 17 May 1995; V2 launch facilities at Avalon Dam attacked, 31 December 1995 | Official; Chronicle, 1995 / 05.17 and 12.31 | Track C `ac_sp_v2` (BLK/AWW) | Bounds the V2 project to the Belkan War and AWWNB window. Links to the inherited nuclear chain (`belka_dlp_war.100/.101`) without changing its triggers. |
| FCU announces Ulysses will strike Earth, 20 April 1996 | Official; Chronicle, 1996 / 04.20 | Existing `ac_pwi.70` | Already implemented by The Peace We Inherit; reference only. |
| A coup breaks out across Usea, 30 May 1997, and is defeated by Unified Command | Official; Chronicle, 1997 / 05.30 | None this round | **Gap.** Falls inside the authored 1991–1999 window but is not scripted. Record only; no actors or outcome are inferred. |
| FCU completes Stonehenge in a desert region of neutral San Salvacion, 19 June 1998; eight railguns, an FCU-led international project | Official; Chronicle, 1998 / 06.19; Super Weapons, Stonehenge | Track C `ac_sp_stonehenge` (FCU) | Project completion target. Its prototype reward may feed existing `ac_pwi_preparedness` / `ac_pwi_relief_capacity`; coefficients are provisional gameplay. |
| Ulysses passes Earth's Roche limit, 8 July 1999 | Official; Chronicle, 1999 / 07.08 | Existing `ac_pwi.71` | Already implemented; it is the hand-off point for the new arc. |
| Osea and Yuktobania cooperate to convert the Arkbird into a debris-clearing platform, 8 October 1999 | Official; Chronicle, 1999 / 10.08 | Track C `ac_sp_arkbird` (OSE, optional YUK co-operation); Track B Yuktobania co-operation branch | In scope as a **non-weapon** orbital debris-clearing project. Its weaponised use belongs to 2010 and is out of scope. |
| Erusea stops taking in refugees, 21 April 2000 | Official; Chronicle, 2000 / 04.21 | Track A slice A1 `ac_ucw` refugee event | Calendar reference. Refugee pressure values are provisional; no invented impact zones or province damage. |
| Erusea invades neutral San Salvacion and seizes Stonehenge, using its railguns against aircraft, summer 2003 | Official; Chronicle, 2003 / SUMMER | Track A slice A2 war start | The source gives a season only, so the exact start day is **provisional gameplay**. The escalation branch may start it earlier; the de-escalation branch may avert or delay it. |
| FCU demands Erusea withdraw from Stonehenge and San Salvacion; FCU President Robert Sinclair establishes the ISAF, 22 August 2003 | Official; Chronicle, 2003 / 08.22 | Track A ISAF formation event | ISAF is built from the existing `FCU_STARTING_FACTION` members, using the faction-charter system merged in #24. Sinclair is named only in localisation unless an FCU leader entry is sourced. |
| ISAF is pushed back to Los Canas by Stonehenge; its first offensive against Stonehenge fails, 14 September 2003 | Official; Chronicle, 2003 / 09.14 | Track A war stage 1 | Stage marker. It does not force territorial results. |
| ISAF establishes its headquarters in North Point, 16 September 2004 | Official; Chronicle, 2004 / 09.16 | Track B North Point "Host ISAF" branch; Track A war stage 2 | The only Chronicle entry naming North Point, and the basis for its active-actor contract. |
| Mount Shezna radar destroyed to cover the ISAF retreat from Saint Ark, 10 October 2004 | Official; Chronicle, 2004 / 10.10 | Track A news/stage event | Reference brief only. |
| ISAF sinks the Aegir fleet at Comberth Harbor, 23 November 2004 | Official; Chronicle, 2004 / 11.23 | Track A stage event | Reference brief; naval losses are not scripted. |
| Large air battle over the Comona Islands, 31 December 2004 | Official; Chronicle, 2004 / 12.31 | Track A stage event | Reference brief. |
| Vincent Harling becomes the 48th President of Osea, 31 December 2004 | Official; Chronicle, 2004 / 12.31 | None | Reference only. The Osean leader and elections are not changed by this round. |
| ISAF lands on the Usean continent, 24 January 2005 | Official; Chronicle, 2005 / 01.24 | Track A war stage 3 (counteroffensive) | Stage marker. |
| ISAF takes Istas Fortress and breaches the Tango Line, 28 February 2005 | Official; Chronicle, 2005 / 02.28 | Track A stage event | Reference brief. |
| Stonehenge engineers and families escape Erusean custody, 14 March 2005 | Official; Chronicle, 2005 / 03.14 | Track A stage event | Reference brief. |
| ISAF destroys Stonehenge, 2 April 2005 | Official; Chronicle, 2005 / 04.02 | Track A; Track C project state | Destruction is reached through war state, not on the date alone. Super Weapons notes seven of eight batteries were destroyed. |
| Northern landing at Ice Creek, 18 June 2005; San Salvacion liberated, 10 July 2005; Whiskey Corridor breached, 15 August 2005 | Official; Chronicle, 2005 / 06.18, 07.10, 08.15 | Track A stage events | Reference briefs. |
| Farbanti falls and Erusea surrenders, ending the Continental War, 19 September 2005 | Official; Chronicle, 2005 / 09.19 | Track A ISAF-victory outcome | The canonical branch. Erusean victory and negotiated stalemate are explicit provisional alternatives. |
| Young Erusean officers seize Megalith, which ISAF destroys; Erusea forms a provisional autonomous government under ISAF oversight, 26 September 2005 | Official; Chronicle, 2005 / 09.26 | Track A post-surrender event; Track C `ac_sp_megalith` (ERU) | Final authored event of the round (2005 assessment). The provisional government is shown through flags and ideas, never `transfer_state` or a forced government swap. |
| Megalith: an Erusean fortress built to bring down orbiting Ulysses fragments | Official; Super Weapons, Megalith | Track C `ac_sp_megalith` | No construction date is published, so project timing is **provisional gameplay**. |

## Out of scope for this round

These Chronicle entries fall in 1998–2005 but concern Anea. They stay
reference-only: 1998 / 07.29 (IAU estimate revision), 1998 / 09.20 (Emmerian
shelter), 2000 / 01.10 (Emmerian aid to Estovakia), 2002 / 03.20 (sanctions
on Estovakia), 2004 / 02.01 (Republic of Anea preparatory agency). The Free
Erusea insurrection (2006 onward), the Circum-Pacific War (2010) and Arkbird's
weaponisation are beyond the 2005 horizon.

## Actor contracts

| Actor | Source layer | Contract | Not allowed |
| --- | --- | --- | --- |
| North Point (NPT) | Official (Chronicle 2004 / 09.16) for ISAF HQ; mod provenance for its 1991 government, ideas and the commented `NPT.txt` sketch | **Active actor.** A neutral stratocracy in 1991 that can align with the FCU and UTO and becomes ISAF's rear base. Track B rebuilds its tree from the commented sketch; the "Host ISAF" branch is gated on Track A war state. | No invented 1991 election result. The sketch's "elections by event on 20 April 1991" stays mod provenance and is shown as a choice, not a fact. |
| Recta (REC) | Mod provenance only. The Chronicle has no Recta entry. | **Postwar consolidation actor, 1995–2005,** inside the states it already gets from `recta.1` (345, 300, 316, plus 293 when Gebet owns it) and the Wacht am Wal transfers. It links to the existing `ac_postwar_local_recovery` → `ac_pwi.76` flow. | No new borders or `transfer_state`, and no canon claims. All Recta content is provisional gameplay or mod provenance. |
| Yuktobania (YUK) | Official for the 1999 / 10.08 Arkbird co-operation; mod provenance for `yuktobania_fp.1`, `yuk_belkan_war_intervention` and `yuk_top_heavy_command_structure` | **Reform actor through 2005.** It builds the army-reform path promised by the `yuktobania_fp.1` "do not intervene" option, a separate post-intervention branch, and the Arkbird co-operation branch. | No Circum-Pacific War foreshadowing, no leader changes and nothing dated after 2005. |

## Pre-existing defects fixed with this ledger

- `recta.1` had no localisation. Added `localisation/english/country_REC_l_english.yml` with text matching the existing `ac_news_event.3` framing (mod provenance).
- `yuktobania_fp.1` referenced `yuktobania_fp.1.desc`, but the defined key is `yuktobania_fp.1_desc`. The event now uses the defined key.
- `history/countries/REC - Recta.txt` set `set_war_support = 5`, outside the 0–1 range. It is now `0.5`, the value used by 47 other country histories. This changes Recta's starting war support from a clamped maximum to 50%.

## Track A implementation (PR A)

Generated by `tools/build_continental_war.py` (run with `--check` to verify); the output files are not hand-edited. Offline test: `tools/Test-ContinentalWar.py`.

| Item | Source layer | IDs and files | Status |
| --- | --- | --- | --- |
| Calendar start after the 1999 assessment, with late-load marking | Provisional gameplay hand-off from `ac_pwi.72` | `ac_ucw_world_start`, `ac_ucw_country_start`, `common/on_actions/ac_ucw.txt` | Static-validated |
| Erusean refugee closure, 21 April 2000 | Official; Chronicle, 2000 / 04.21. The quota option is provisional | `ac_ucw.10`–`.12` | Static-validated |
| Grievance, refugee pressure and recovery indices; mediation; continental accord (averted war) | Provisional gameplay | `ac_ucw_fallout` decisions, `ac_ucw.13`–`.15`, `ac_ucw.25` | Static-validated |
| Invasion of San Salvacion, summer 2003 | Official season; the AI window from 21 June 2003 and the early-escalation route are provisional | `ac_ucw_start_war`, `ac_ucw.20` | Static-validated |
| **Stonehenge location: state 310 "San Salvacion"** | **Provisional gameplay.** The Chronicle names only a desert region of San Salvacion | `ac_ucw_controls_stonehenge`, `ac_ucw_stonehenge_held_by_erusea` (the only place the ID appears) | Static-validated |
| SNS starts as a member of FCU's faction, so the war is continental from its first day | Mod provenance (`history/countries/FCU - Central Usea.txt`) differs from the Chronicle's neutral SNS | — | Recorded difference |
| ISAF founding, 22 August 2003 (Sinclair named only in localisation) | Official; Chronicle, 2003 / 08.22 | `ac_ucw.30`–`.34`, `ac_ucw_form_isaf`, faction renamed `ac_ucw_isaf_faction` | Static-validated. The faction-charter system from #24 creates new blocs only, so ISAF stays the existing FCU faction |
| War stages: Los Canas, North Point HQ, landing, Stonehenge destroyed | Official dates (2003 / 09.14, 2004 / 09.16, 2005 / 01.24, 04.02); stage timings and modifiers are provisional | `ac_ucw_stage_*`, `ac_ucw_order_*`, `ac_ucw.40`–`.44` | Static-validated |
| News briefs: Mount Shezna, Comberth, Comona, Istas and the Tango Line, the engineers' escape, Ice Creek, San Salvacion liberated, the Whiskey Corridor | Official; Chronicle, 2004–2005 | `ac_ucw.70`–`.77` | Static-validated. Each fires only if the war has reached its stage |
| Outcomes: ISAF victory (Farbanti, 19 September 2005), Erusean victory, armistice | ISAF victory is official; the other two are provisional | `ac_ucw_outcome_*`, `ac_ucw.45`–`.52` | Static-validated |
| Megalith seized and destroyed; provisional autonomous government | Official; Chronicle, 2005 / 09.26 | `ac_ucw.60`–`.62`, `ac_ucw_eru_provisional_government` | Static-validated. Shown as a national spirit only |
| 2005 assessment, the new end of authored chronology | Provisional gameplay | `ac_ucw.90`, `ac_ucw_2005_assessed` | Static-validated |
| Erusea and Central Usea/ISAF focus trees (24 + 21 focuses), loaded at calendar start | Provisional gameplay, with Chronicle references in descriptions | `common/national_focus/ERU.txt`, `FCU.txt` | Static-validated |
| Playtest shortcuts game rule | Tooling, not lore | `common/game_rules/ac_playtest_rules.txt`, `ac_playtest` decisions | See [PLAYTEST_CONTINENTAL_WAR.md](PLAYTEST_CONTINENTAL_WAR.md) |

Native status: not tested in HOI4. Native acceptance remains under #8.
