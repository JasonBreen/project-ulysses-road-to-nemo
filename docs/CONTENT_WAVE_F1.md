# Wave F1, the Lighthouse War: source and implementation ledger

Status: **implemented in source; offline checks pass; native acceptance pending.**
Generator: `tools/content_waves/lighthouse.py`. Plan: [CONTENT_PLAN_2006_2020.md](CONTENT_PLAN_2006_2020.md).
Sources: [STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md). No HOI4 installation,
profile, save or desktop was touched; native testing remains paused under issue #8.

| Wave | Countries | Tree | Definitions | Horizon | Release-plan effect |
| --- | --- | --- | ---: | --- | --- |
| F1 | Erusea (`ERU`), Central Usea (`FCU`); Osea (`OSE`) through the owner's decisions | `LIGHTHOUSE WAR` import block in `ERU.txt` and `FCU.txt` | 78 (ERU 54, FCU 24) | 2010–2019 | Erusea 144 of 144 and Central Usea 108 of 108 delivered; the ledger moves to **854 delivered and 174 remaining** |

Both budgets are now complete. Osea stays at its 150 definitions; it takes part
through three crisis decisions, as the plan required.

## Source layers

| Claim or material | Layer and exact reference | Affected IDs | Status |
| --- | --- | --- | --- |
| Drone strikes at four major naval ports in Osea; the Kingdom of Erusea declares war on the Osean Federation and captures the International Space Elevator; the Lighthouse War begins, 15 May 2019 | Official: Chronicle, 2019 / 05.15; Abstracts, ACE COMBAT 7 (Erusea seizes control of the Arsenal Birds with the elevator); Product, ACE COMBAT 7 (Erusea accuses Osea of massive overreach in their joint international projects) | `ac_lhw_declare`, `ac_lhw.5` (Erusean decision event, AI always), `ac_lhw.1`, `ac_lhw.29`, flags `ac_lhw_started`, `ac_lhw_birds_over_elevator` | The owner's only declaration. The stated grievance is quoted as the source states it; no cause is asserted. The seized Arsenal Birds exist only if `ac_sp_arsenal_birds` was completed |
| Osea and the IUN Peacekeeping Force begin Operation Eastern Wind, 17 May 2019 | Official: Chronicle, 2019 / 05.17 | `ac_lhw.20`, idea `ac_lhw_ose_eastern_wind` | News with a timed Osean idea; no force or faction is created |
| The two-pronged offensive on Chopinburg airspace and Farbanti fails; Kestrel II is sunk, 30 May 2019 | Official: Chronicle, 2019 / 05.30 | `ac_lhw.21`, idea `ac_lhw_ose_kestrel_ii_lost` | News; no ship is represented and no state changes hands |
| Former president Vincent Harling dies in a rescue attempt at the space elevator, 6 June 2019 | Official: Chronicle, 2019 / 06.06; Abstracts, ACE COMBAT 7 ("a botched attempt") | `ac_lhw.22` | News only; whose attack it was is not stated and not asserted |
| Osea forms the Long Range Strategic Strike Group, 10 August 2019 | Official: Chronicle, 2019 / 08.10 | decision `OSE_lw_strike_group`, `ac_lhw.23`, idea `ac_lhw_ose_strike_group`, flag `ac_lhw_lrssg_formed` | An Osean decision available from the date; no unit is created |
| Osea reactivates one of Stonehenge's batteries and shoots down the Arsenal Bird Liberty, 19 August 2019 | Official: Chronicle, 2019 / 08.19; Super Weapons, Arsenal Birds | `ac_lhw.24`, idea `ac_lhw_ose_stonehenge_battery`, flags `ac_lhw_stonehenge_battery_reactivated`, `ac_lhw_liberty_lost` | Only if Stonehenge was ever built (`ac_ucw_stonehenge_operational`). The Liberty is lost only if the birds were seized; `[ac_lhw_liberty_text]` says which |
| Osea attacks Farbanti; destroying military satellites cuts communications across Usea, 19 September 2019 | Official: Chronicle, 2019 / 09.19 | `ac_lhw.25`, ideas `ac_lhw_eru_capital_attacked`, `ac_lhw_usea_blackout` (ERU, FCU, SNS, AMB, UGE, DEL, NPT), flag `ac_lhw_usea_blackout` | Reported only once Osean forces actually control an Erusean core (`ac_lhw_osean_foothold`). Whose operation it was is not stated. Farbanti is not mapped to a state |
| Shilage and other small nations annexed by Erusea declare independence; Erusea refuses and internal conflict follows, 1 October 2019 | Official: Chronicle, 2019 / 10.01 | `ac_lhw.26`, idea `ac_lhw_eru_internal_conflict`, `[ac_lhw_shilage_text]`; branch `ERU_lw_secession_*` | News and a timed idea. The Shilage release flags and `country_exists = SHI` are read for text only; nothing is released, annexed, cored or moved |
| General Édouard Labarthe is killed by Osean forces, 10 October 2019 | Official: Chronicle, 2019 / 10.10 | `ac_lhw.27` | News only, as the source names him |
| Osean and Erusean forces clash at the space elevator; the Arsenal Bird Justice is shot down, 31 October 2019 | Official: Chronicle, 2019 / 10.31; Abstracts, ACE COMBAT 7 (the voluntary coalition of Osean forces and a traditionalist sect of the Erusean Army; the surrender of the Erusean Army radicals) | `ac_lhw.28`, flag `ac_lhw_arsenal_birds_lost` | News; the coalition and the sect are named only in text and no faction is created |
| Osea and Erusea sign a ceasefire at the Expo City Conference, 1 December 2019 | Official: Chronicle, 2019 / 12.01; Abstracts, ACE COMBAT 7 | `ac_lhw_ceasefire_tick`, `ac_lhw.6` (Erusean decision event, AI always signs), `ac_lhw_sign_ceasefire`, `ac_lhw.7`, flags `ac_lhw_ceasefire_signed`, `ac_lhw_outcome_ceasefire`, `ac_lhw_historical_course` | **User decision 7:** the only `white_peace` in the content waves. The owner's state is written only if the engine actually ended the war; otherwise the war is observed to its real end (`ac_lhw_ceasefire_not_made`) |
| Arsenal Birds Liberty and Justice | Official: Super Weapons, Arsenal Birds | project `ac_sp_arsenal_birds` (OSE), idea `ac_sp_arsenal_birds_elevator_screen`, fallback `ac_superweapons_arsenal_birds`, tag `ac_sp_tag_unmanned_aviation` | **User decision 8.** Available from 2015 (provisional); cancelled and never completed after the sourced loss; the seizure, the Liberty and the Justice follow the owner's course |
| Alicorn | Official: Super Weapons, Alicorn | project `ac_sp_alicorn` (ERU), idea `ac_sp_alicorn_cruiser`, fallback `ac_superweapons_alicorn`, tag `ac_sp_tag_submarine_aviation`; branch `ERU_lw_alicorn_*` | **User decision 8.** Construction and custody only, gated on the authorised cruiser and its custody rules; never deployed, never disappears by script. Its captain is not named outside the branch's narrative, which names no one |
| The withheld declaration, the early ceasefire, fighting on past Expo City, the fourteen-day windows, every idea value, decision and branch | Provisional gameplay | `ac_lhw_withhold`, `ERU_lw_early_ceasefire`, `ac_lhw_fight_on`, `ac_lhw_*` ideas, `OSE_lw_*`, `ERU_lw_*`, `FCU_lw_*` | Implemented and labelled in-game |
| Continental War outcomes, Free Erusea records, Shilage release flags, the Stonehenge project state | Mod provenance, read only | `ac_ucw_outcome_*`, `ac_ucw_stonehenge_operational`, `ERU_fe_*`, `FCU_fe_*`, `ac_release_SHI_*` | Read through the real flags; never written. The owner's only writes outside its namespace are the two projects' completion flags and the removal of Osea's screen idea at the capture |

## The owner (`ac_lhw`)

**Calendar.** The Erusean weekly pulse runs the owner. The calendar opens on
1 February 2019 only when both principals exist **and** the Continental War
ended in the ISAF victory (`ac_ucw_outcome_isaf_victory`): the sourced 2019
route needs the sourced 2005 history, so any other outcome closes the owner
with `ac_lhw_route_unreachable` and no war is invented in its place. A save
whose first observation falls on or after 15 May 2019 closes the owner without
replaying any expired date (`ac_lhw_late_start_skipped`).

**The declaration, 15 May 2019.** If Osea and Erusea are already at war with
each other, the owner records the war it did not start and observes it from
outside (`ac_lhw_existing_war_observed`, `ac_lhw.3`). Otherwise, if Erusea can
declare (exists, not capitulated, not a subject, Osea likewise, not already at
war), the Erusean government gets `ac_lhw.5`: declare (historical, AI always)
or withhold under the treaty obligations it chose to keep, offered only with
`ERU_fe_oversight_settlement_done` and `ERU_lw_sovereignty_policy_a_done`
(`ac_lhw_declaration_withheld`, `ac_lhw.2`). Left unanswered for fourteen days,
the owner declares. `ac_lhw_declare` issues the waves' second `declare_war_on`
(`target = OSE`, `topple_government`) and writes the owner's state only if the
engine created the war (else `ac_lhw_declaration_refused`). A principal already
at war with someone else is observed externally from the start. If
`ac_sp_arsenal_birds_complete` holds, Erusea takes the two birds with the
elevator (`ac_lhw_birds_over_elevator`, `ac_lhw.29`) and Osea loses its screen
idea. Factions and guarantees are never consulted.

**External observation.** Any country other than the two principals and their
own subjects at war with either one taints the course (`ac_lhw_tainted`,
`ac_lhw.4`) and the dated news stops; the war footings stay until the end.

**Stages.** Each fires once, only while the owned war runs untainted:

| Date | Stage | Effect |
| --- | --- | --- |
| 17 May | Operation Eastern Wind | Osea: supply strain (90 days) |
| 30 May | Kestrel II | Osea: carrier lost (90 days); no foothold needed, the offensive fails |
| 6 Jun | Harling | news only |
| 19 Aug | Stonehenge | only if Stonehenge was ever built; Osea: battery (120 days); Liberty lost if the birds were seized (two → one) |
| 19 Sep | Farbanti and the blackout | only once Osea controls an Erusean core; Erusea: capital attacked (60 days); the blackout idea on the seven Continental War participants (90 days) |
| 1 Oct | Declarations of independence | Erusea: internal conflict (120 days); Shilage text only |
| 10 Oct | Labarthe | news only |
| 31 Oct | The clash at the elevator | Justice lost; the remaining bird idea removed; `ac_lhw_arsenal_birds_lost` |

**The ceasefire, 1 December 2019.** While the course is open, Erusea gets
`ac_lhw.6`: sign (historical, AI always) or fight on (`ac_lhw_ceasefire_refused`,
`ac_lhw.13`, after which the owner issues no further dated news). Left
unanswered for fourteen days, the owner signs. `ac_lhw_sign_ceasefire` issues
`white_peace = OSE` and records `ac_lhw_ceasefire_signed` only if the war is
gone; if the engine keeps the war, `ac_lhw_ceasefire_not_made` moves the crisis
to external observation. An earned early ceasefire is the Erusean decision
`ERU_lw_early_ceasefire` (50 political power; needs the elevator kept running
as policy, `ERU_lw_lighthouse_policy_b_done`), which signs the same way and is
recorded as `ac_lhw_ceasefire_early` (`ac_lhw.8`). Switching the owner to
observation only is a one-effect change.

**The end.** When the two are no longer at war, or a principal capitulated or
was annexed, the owner records `ac_lhw_ended` and exactly one outcome:
`ac_lhw_outcome_osean_victory` (`ac_lhw.9`), `ac_lhw_outcome_erusean_victory`
(`ac_lhw.10`), `ac_lhw_outcome_ceasefire` (`ac_lhw.7`, with
`ac_lhw_historical_course` only when the untainted course reached the clash at
the elevator; `ac_lhw.8` for the early ceasefire), or `ac_lhw_outcome_cessation`
(`ac_lhw.11` untainted, `ac_lhw.12` observed). Every hook dispatches on the
winner in `FROM`, so a fall to a third party, or outside the pair's own war, is
`ac_lhw_external_fall` under observation; only the principal tags count, never
a breakaway. End news is scheduled by a surviving principal; all untimed war
ideas are removed; an Osean weekly fallback records the end if Erusea no longer
exists; `ac_lhw_restore` re-adds the footings on load.

**Decisions.** Osea's crisis category (`ac_lhw_ose_crisis`): form the Long
Range Strategic Strike Group (50, from 10 August), repair the struck ports (25),
compile the war record after the end (25). Erusea's services category also
carries the early ceasefire. The two no-DLC project fallbacks sit under the
shared `ac_superweapons` category. The engine charges every cost once.

**AI.** `ac_lhw_eru_tension` (antagonize Osea while the route is open),
`ac_lhw_eru_war` (conquer Osea 150) and `ac_lhw_ose_war` (conquer Erusea 120);
all abort when disabled.

## The branches

Nine Erusean and four Central Usean six-focus lanes, all provisional
gameplay. Every stage-1 Erusean lane also opens from
`ERU_ucw_exp_settlement_assessment`, so an AI Erusea reaches them without a
Wave A settlement.

| Branch | Entry and gate | What it is drawn on |
| --- | --- | --- |
| `ERU_lw_sovereignty` | Wave A oversight, insurrection or return settlement; ISAF victory; 2010 | the 2005 oversight context; policy A is the withheld-declaration record |
| `ERU_lw_standing` | victor, armistice, ordinary or return settlement; not ISAF victory; 2010 | the route-exclusive alternative; its text says the sourced 2019 route needs the ISAF history |
| `ERU_lw_elevator` | any Wave A settlement; 2014 | 05.15 and the Arsenal Birds row establish the elevator by 2019; its location, operator and date are unsourced and unmapped |
| `ERU_lw_alicorn` | any Wave A settlement; 2013 | Super Weapons, Alicorn; `operations_done` gates the project, `settlement_done` weights its reward |
| `ERU_lw_drones` | any Wave A settlement; 2017 | 05.15 says only "drone strikes"; the "clean war" of the abstract is what the rules of engagement would rest on |
| `ERU_lw_lighthouse` | elevator settlement; `ac_lhw_started` | 05.15 and 10.31; policy B earns the early ceasefire |
| `ERU_lw_capital` | sovereignty settlement; `ac_lhw_started` | 05.30 and 09.19; the second service clears Erusea's blackout idea |
| `ERU_lw_ceasefire` | sovereignty or elevator settlement; `ac_lhw_ended` | 12.01 when the outcome is the ceasefire; neutral across outcomes |
| `ERU_lw_secession` | same; `ac_lhw_stage_secession` | 10.01; releases nothing |
| `FCU_lw_airspace` | any Wave A settlement; 2019 | closed airspace or a declared corridor; no membership or access is granted |
| `FCU_lw_corridor` | same; `ac_lhw_started` | a humanitarian corridor under federal escort or neutral flags |
| `FCU_lw_blackout` | same; `ac_lhw_stage_farbanti` | ground relays or a replacement satellite programme; the first service clears the federation's blackout idea |
| `FCU_lw_settlement` | same; `ac_lhw_ended` | guarantor or convenor; Expo City is not claimed as Central Usean |

Services need `has_war = no`, so every war lane's review and settlement are
postwar by construction. Layout: Erusean row 1 at y 22 (x 6, 12, 18, 24, 30),
row 2 at y 28 (x 6, 12, 18, 24); Central Usean row at y 22 (x 8, 14, 20, 26);
nothing overlaps the native rows or Wave A.

## Counts and artwork

| Content | Wave F1 |
| --- | --- |
| Focuses | 78 (ERU 54, FCU 24) in 13 branches |
| Events | 53: 21 news, 2 decision events (`ac_lhw.5`, `ac_lhw.6`), 30 narrative |
| Ideas | 130 (18 owner and project ideas) |
| Decisions | 34 in 4 categories (26 services, 2 cancellations, 3 Osean, the early ceasefire, 2 project fallbacks) |
| Special projects | 2, with 2 tags and 2 unique rewards |
| Effects / triggers | 209 / 46 |
| Words of original English text | about 20,000 |

282 new original DDS textures (978 across all waves): 78 focus icons, 130 idea
icons, 34 decision rows, 3 categories, 17 event pictures, 16 news pictures, 2
project icons and 2 reward icons; the Erusean sheet is `lighthouse-eru-focuses.png`.
The generator gained merged hooks, chained import blocks, owner projects and
project art (see the Part B1 commit).

## Validation

```text
python -B tools/content_waves/build.py --check
python -B tools/content_waves/build_art.py --check
python -B tools/content_waves/test_waves.py
python -B tools/content_waves/refresh_records.py --check
python -B tools/Test-StrangerealProjects.py
python -B tools/overhaul/check_release_plan.py
python -B tools/world_foundation/test_foundation.py
```

`test_waves.py` has 51 tests. The offline world now models `white_peace`
(and an engine that refuses it), and its helpers take a module name, so the
Wave C cases and the Wave F1 cases run on the same harness.

**Wave F1 runtime cases:**
- the calendar needs the ISAF history; other outcomes close the owner with
  `ac_lhw_route_unreachable` and never declare; a first observation on or after
  15 May 2019 replays nothing; a missing principal closes the owner;
- the declaration window falls back to history on the fourteenth day; the
  same pulse delivers the stages whose dates have passed; withholding needs
  the oversight file and the obligations kept, and is not even offered without
  them; a capitulated or subject principal closes the owner; a refused engine
  war writes no state;
- the course fires each stage once; Stonehenge needs the built railguns;
  Farbanti needs Osean control of an Erusean core (an Erusean-owned non-core
  state is not one); the blackout falls on exactly the seven participants; the
  Expo City event removes the war and records the ceasefire with the official
  course, and the fourteen-day window signs on its own; every foreign record
  is byte-identical before and after;
- the Arsenal Birds follow the Osean project: seized at the declaration, the
  Liberty lost only with Stonehenge, both lost at the clash, and the project
  never completes after the loss; the Alicorn completion is idempotent;
- a refused peace moves the war to observation and ends on actual cessation;
  fighting on issues no further dated news; the early ceasefire is earned by
  the elevator policy and costs nothing twice;
- pre-existing and third-party wars taint the course; a principal's subject
  does not; a war the pair already fought is observed and a reload adds no
  ideas; capitulation, annexation and subject annexation record the actual
  outcome with the survivor's news; third parties, breakaways and a principal
  that falls alone are handled as in Wave C;
- the Osean decisions are charged once and follow the phase; the Shilage text
  follows `SHI` and the release flags; the branch gates follow the history and
  the owner's state; the blackout-clearing services clear it.

**Source checks:** the anchors, the citations (every 2019 entry, both Super
Weapons rows, the abstract), the single `white_peace` in `ac_lhw_sign_ceasefire`,
no faction or guarantee check, no assumed end date, the only foreign writes
being the two completion flags, the hash-pinned Track C files unchanged, and
named canon only in event and idea text.

These are source and offline checks, not native acceptance.

## Open items

- Native parsing, AI pacing, the projects' engine behaviour, balance and
  save/reload (#8).
- Farbanti, Chopinburg, Expo City, the elevator, Tyler Island and the
  seceding nations are not mapped to states; the territorial row uses the
  observed foothold.
- Wave E (Emmeria–Estovakia War) and Wave F2 (Leasath and the 2019–2020
  crisis lanes) remain; the Chronicle's 2019 / XX.XX Leasath entry stays with F2.
