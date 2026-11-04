# Wave C, the Circum-Pacific War: source and implementation ledger

Status: **implemented in source; offline checks pass; native acceptance pending.**
Generator: `tools/content_waves/circum_pacific.py`, the first owner-only wave.
Plan: [CONTENT_PLAN_2006_2020.md](CONTENT_PLAN_2006_2020.md). Sources:
[STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md). Consumer
contract: [PACIFIC_NATIONAL_CONTINUATIONS.md](PACIFIC_NATIONAL_CONTINUATIONS.md).
No HOI4 installation, profile, save or desktop was touched; native testing
remains paused under issue #8.

| Wave | Countries | Tree | Definitions | Horizon | Release-plan effect |
| --- | --- | --- | ---: | --- | --- |
| C | Osea (`OSE`), Yuktobania (`YUK`) | none; owner only | 0 | 2008–2010 | none: both budgets were complete. The owner is recorded under Package 3 |

The ledger stays at **776 delivered and 252 remaining** (`tools/overhaul/release_plan.json`).

## Source layers

| Claim or material | Layer and exact reference | Affected IDs | Status |
| --- | --- | --- | --- |
| The Arkbird Summit, 21 August 2008 | Official: Chronicle, 2008 / 08.21 | `ac_cpw.14`, flag `ac_cpw_summit_held` | News only, and only if `ac_sp_arkbird_complete`. No agenda or result is asserted |
| Unidentified aircraft at Cape Landers; an SR-71 over Osea, 23–24 September 2010 | Official: Chronicle, 2010 / 09.23, 09.24 | `ac_cpw.1`, `ac_cpw.2` | News only; no owner of the aircraft is named |
| Yuktobania declares war on Osea and attacks Port Saint Hewlett, 27 September 2010 | Official: Chronicle, 2010 / 09.27 | `ac_cpw_declare`, `ac_cpw.5` (Yuktobanian decision event, AI always), `ac_cpw.3`, flag `ac_cpw_started` | The owner's only declaration. The Chronicle gives no reason and none is asserted |
| Scinfaxi's first use; the carriers Vulture and Buzzard sunk in the Eaglin Straits; the Arkbird sent to the front, 30 September 2010 | Official: Chronicle, 2010 / 09.30 | `ac_cpw.20`, `ac_cpw.6`, `ac_cpw.15`, flag `ac_cpw_arkbird_committed` | The Arkbird goes to the front only if the project is complete and Osea sends it (AI always) |
| Scinfaxi sunk at Sand Island; Hrimfaxi sunk in the Razgriz Straits | Official: Chronicle, 2010 / 10.04, 11.14; Super Weapons, Scinfaxi & Hrimfaxi | `ac_cpw.21`, `ac_cpw.27`; ideas `ac_cpw_yuk_submarine_carriers`, `ac_cpw_yuk_submarine_carrier` | The carriers exist only as Yuktobanian wartime ideas; no ship is created |
| The Akerson Hill Incident; the Battle of Ceres Ocean | Official: Chronicle, 2010 / 10.22, 12.29 | `ac_cpw.22`, `ac_cpw.33` | Name only, as the source gives it |
| The Arkbird's engines destroyed; the Arkbird, carrying a nuclear weapon, shot down over Okchabursk | Official: Chronicle, 2010 / 10.25, 12.19; Super Weapons, Arkbird | `ac_cpw.23`, `ac_cpw.31`, flags `ac_cpw_arkbird_sabotaged`, `ac_cpw_arkbird_lost` | Only if the Arkbird was committed. On the loss the two Arkbird ideas are removed from Osea and Yuktobania; `ac_sp_arkbird` is never created, revived, weaponized or completed by script |
| Osea lands on the Bastok Peninsula; Cruik Fortress falls | Official: Chronicle, 2010 / 11.01, 12.06 | `ac_cpw.24`, `ac_cpw.29` | Reported only once Osean forces actually control Yuktobanian territory (`ac_cpw_osean_foothold`). No state is moved or mapped |
| Dresdene; nerve gas in Bana and the attack on Apito International Airport; the attack on the peace ceremony in November City | Official: Chronicle, 2010 / 11.02, 11.04, 11.29 | `ac_cpw.25`, `ac_cpw.26`, `ac_cpw.28` | News with timed Osean ideas |
| President Harling rescued from Stier Castle in Belka; Razgriz Squadron forms; former Prime Minister Nikanor rescued | Official: Chronicle, 2010 / 12.09, 12.23 | `ac_cpw.30`, `ac_cpw.32` | News only. Harling and Nikanor are named as the Chronicle names them; no character, leader, portrait or unit changes. Belka appears only as the place named |
| The Osean carrier Kestrel sunk; Harling and Nikanor make a televised address asking their militaries to disarm; a joint force inspects Gründer Industries in the Osean trust territory of Sudentor, North Osea | Official: Chronicle, 2010 / 12.30 | `ac_cpw.34`, flag `ac_cpw_appeal_made`, idea `ac_cpw_disarmament_appeal` | The appeal weighs on both countries' war support. It ends nothing by script |
| The SOLG falls; Razgriz destroys the former Belkan Grabacr and Ofnir squadrons and the SOLG; the war ends, 31 December 2010 | Official: Chronicle, 2010 / 12.31; Super Weapons, SOLG | `ac_cpw.35` | The SOLG is reported as named, with the Gray Men as the Super Weapons row names them. The war's end is **not** scripted on this date |
| The war's end | Official end date, 2010 / 12.31; actual end observed | `ac_cpw_record_end`, `ac_cpw.10`–`.13`, flags `ac_cpw_ended`, `ac_cpw_outcome_*`, `ac_cpw_historical_course` | Recorded when the fighting between Osea and Yuktobania actually stops or a principal falls, never on the anchor |
| Peter N. Beagle, Albert Genette, Captain Marcus Snow (2010 / 12.07); Talisman (2013 / 12.23) | Official, reference only | none | Not used |
| The reciprocal exchange, the withheld declaration, the fourteen-day declaration window, external observation, every idea value and decision | Provisional gameplay | `ac_cpw_prevent`, `ac_cpw_withhold`, `ac_cpw_taint`, `ac_cpw_*` ideas, `OSE_cpw_*`, `YUK_cpw_*` | Implemented and labelled in-game |
| Osean and Yuktobanian continuation records; the Arkbird project | Mod provenance, read only | `ac_snc_ose_*`, `ac_snc_yuk_*`, `ac_sp_arkbird_complete` | Read through the real triggers; never written |

## The owner (`ac_cpw`)

**Calendar.** The Yuktobanian weekly pulse runs the owner. The calendar opens on
1 September 2010 if both principals exist; a save whose first observation falls
on or after 27 September 2010 closes the owner without replaying any expired
date (`ac_cpw_late_start_skipped`), so no prelude, declaration or stage is ever
delivered in bulk. The prelude news (23 and 24 September) fires once each while
the two are at peace.

**The declaration, 27 September 2010.** In order:

1. If Osea and Yuktobania are already at war with each other, the owner records
   the war it did not start (`ac_cpw_started`, `ac_cpw_existing_war_observed`,
   news `ac_cpw.8`) and observes it from outside. It is not marked as expanded:
   the stories read it as a real war between the two, and the dated course is
   never asserted for it.
2. If both governments have earned verified contact and open channels
   (`ac_snc_ose_verification_earned`, `ac_snc_ose_channel_earned`,
   `ac_snc_yuk_verification_earned`, `ac_snc_yuk_channel_earned`), the reciprocal
   exchange closes the route: `ac_cpw_prevented`, news `ac_cpw.4`, a standing idea
   for each. This is the earned de-escalation the stories call "the exchange".
3. Otherwise, if Yuktobania can declare (exists, not capitulated, not a subject,
   Osea likewise, not already at war), the Yuktobanian government gets
   `ac_cpw.5`: declare (historical, AI always) or withhold under its mandate,
   available only when `ac_snc_yuk_verification_earned` holds
   (`ac_cpw_declaration_withheld`, news `ac_cpw.7`). If the event is left
   unanswered for fourteen days, the owner declares.
4. Otherwise the owner closes (`ac_cpw_principal_unable`).

`ac_cpw_declare` issues the only `declare_war_on` in the content waves
(`target = OSE`, `topple_government`) and writes the owner's state only if the
engine actually created the war; otherwise it closes with
`ac_cpw_declaration_refused`. If either principal was already at war with
someone else, the crisis is observed externally from the start
(`ac_cpw_pre_existing_war`, `ac_cpw_tainted`). Factions and guarantees are never
consulted.

**External observation.** Every week while the war runs, if any country other
than the two principals and their own subjects is at war with Osea or
Yuktobania (faction members count), `ac_cpw_tainted` is set once (news
`ac_cpw.9`) and the dated course stops. The war footing ideas remain until the
end.

**Stages.** Each fires once, only while the owned war runs untainted:

| Date | Stage | Effect |
| --- | --- | --- |
| 30 Sep | Eaglin Straits | Osea: carrier losses idea (90 days); the Arkbird decision `ac_cpw.6` if the project is complete. An answer left until 25 October holds the Arkbird back instead of replaying its fate |
| 4 Oct | Sand Island | Yuktobania: two carriers → one |
| 22 Oct | Akerson Hill | name only |
| 25 Oct | Arkbird sabotage | Osea: grounded idea (56 days); only if committed |
| 1 Nov | Bastok Peninsula | only once Osea controls Yuktobanian territory; Osea: expeditionary strain (90 days) |
| 2 Nov | Dresdene | after Bastok; Osea: inquiry (60 days) |
| 4 Nov | Bana and Apito | Osea: home front alert (60 days) |
| 14 Nov | Razgriz Straits | Yuktobania: no carriers remain |
| 29 Nov | November City | Osea: home front alert renewed |
| 6 Dec | Cruik Fortress | gated like Bastok; Yuktobania: stronghold lost (90 days) |
| 9 Dec | Harling rescued | Osea: the president returns (90 days) |
| 19 Dec | Arkbird shot down | only if committed; `ac_cpw_arkbird_lost`; the two Arkbird ideas removed |
| 23 Dec | Nikanor rescued | Yuktobania: leadership question (60 days) |
| 29 Dec | Ceres Ocean | name only |
| 30 Dec | Kestrel; the joint appeal | both: disarmament appeal idea until the end |
| 31 Dec | The SOLG falls | after the appeal; news only |

**The end.** When the two are no longer at war, or a principal capitulated or
was annexed (the `on_capitulation_immediate`, `on_annex` and
`on_subject_annexed` hooks mark `ac_cpw_ose_fallen` / `ac_cpw_yuk_fallen`; only
the principal tags themselves count, never a breakaway sharing their original
tag), the owner records `ac_cpw_ended` and exactly one outcome:
`ac_cpw_outcome_osean_victory` (`ac_cpw.11`), `ac_cpw_outcome_yuktobanian_victory`
(`ac_cpw.12`), or `ac_cpw_outcome_cessation`: with `ac_cpw_historical_course`
only when the owner's own war ran untainted all the way to the SOLG stage
(`ac_cpw.10`, also used for an earlier untainted end without the flag), and
`ac_cpw.13` when the war was observed from outside. A victory is recorded only
when a principal fell to the other principal in their own war; a principal
annexed by a third party, or capitulating after the pair had already made
peace, is marked `ac_cpw_external_fall` and ends the war under observation.
End news is scheduled by a surviving principal, so a fallen scope never owns
it. All untimed war ideas are removed, and a declaration still pending when a
route settles is cleared. An Osean weekly fallback records the end if
Yuktobania no longer exists. There is no `white_peace`; see the open items.

**Decisions.** Each principal has a crisis category with two once-only
decisions: mobilise the home front during the war (50 political power, 120-day
idea) and compile the war record after it (25 political power, 180-day idea).
The category description reads `ac_cpw_status_text`.

**AI.** `ac_cpw_yuk_tension` (antagonize Osea while the route is open),
`ac_cpw_yuk_war` (conquer Osea 150) and `ac_cpw_ose_war` (conquer Yuktobania
120) while the war runs; all abort when disabled.

**Story hooks.** The Pacific squadron stories read only the four published
flags; their own harness still loads no `ac_cpw_*` library and is unchanged.

## Counts and artwork

| Content | Wave C |
| --- | --- |
| Events | 31: 29 news, 2 decision events (`ac_cpw.5`, `ac_cpw.6`) |
| Ideas | 21 |
| Decisions | 4 in 2 categories |
| Effects / triggers | 22 / 11 |
| Words of original English text | about 3,300 |

53 new original DDS textures (696 across all waves): 21 idea icons, 4 decision
rows, 2 categories, 2 event pictures and 24 news pictures, with new Osean and
Yuktobanian frames and colours. The generator gained `empty_wave`, owner hooks,
`COUNTRIES`, `EVENT_ART` and an `ai_strategy` output for owner-only waves.

## Validation

```text
python -B tools/content_waves/build.py --check
python -B tools/content_waves/build_art.py --check
python -B tools/content_waves/test_waves.py
python -B tools/content_waves/refresh_records.py --check
python -B tools/overhaul/check_release_plan.py
python -B tools/world_foundation/test_foundation.py
python -B tools/squadrons/pacific/test_runtime.py
```

`test_waves.py` has 42 tests. The offline world now observes wars
(`declare_war_on`, `has_war_with`, `has_war`, `any_country`,
`any_controlled_state`, `is_subject`, `is_subject_of`), honours event and option
triggers when a test chooses an option, can model an engine that refuses a
declaration, and loads the real Osean and Yuktobanian continuation triggers, so
the earned routes are tested against the actual records they require. Its
states carry the cores from `history/states`, so the Osean foothold is tested
against real cores: Yuktobanian-owned state 515, which has no Yuktobanian core,
is the negative case and core state 125 the positive one.

**Wave C runtime cases:**
- the Arkbird Summit needs the completed project and fires once;
- the prelude and the declaration follow the anchor; a first observation on or
  after the anchor (27 September 2010, 15 October 2010, 1 October 2011) closes
  the owner and replays nothing; a missing principal closes the owner;
- the declaration window falls back to history; withholding needs the real
  mandate, and without it the option is not even offered;
- a capitulated or subject principal closes the owner (`ac_cpw_principal_unable`),
  and a declaration the engine does not turn into a war closes it without any
  war state (`ac_cpw_declaration_refused`);
- the reciprocal exchange prevents the declaration and is earned, not partial;
- the historical course fires each stage once, needs the observed foothold for
  the territorial rows, loses the Arkbird only if it was committed, and ends
  on observed cessation with every `ac_snc_*`/`ac_snp_*` record untouched;
- the Arkbird stages need the project and the commitment; an answer after
  25 October holds the Arkbird back;
- pre-existing or third-party wars move the crisis to external observation; a
  war the pair already fought is started but not expanded and a reload adds no
  ideas; a principal's own subject is not a third party;
- capitulation and annexation record the actual outcome, with the end news
  scheduled by the survivor; a breakaway with a principal's original tag does
  not count as the principal falling; a principal annexed by a third party, or
  capitulating after the pair made peace, ends the war under observation;
- the status text follows each route, `ac_cpw_historical_course` needs the SOLG
  stage, timed ideas expire, and the foreign Pacific records are byte-identical
  before and after the whole course;
- the crisis decisions are charged once by the engine and follow the phase.

**Source checks:** the only `declare_war_on` in the waves targets Osea with
`topple_government`; no `white_peace`, faction or guarantee check, assumed end
date, `ac_snc_`/`ac_snp_`/`ac_sp_` flag or variable write; named canon appears
only in event text and in the idea and flag tooltips derived from it, never in
a script identifier.

These are source and offline checks, not native acceptance.

## Open items

- **A peace route.** The published contract forbids a scripted white peace in
  the first owner, so a war between two AI countries ends only through
  capitulation or the engine's own peace. A reviewed, earned route (for
  example after the joint appeal to disarm) is decision 6 in the content plan.
- Native parsing, AI pacing across the ocean, balance and save/reload (#8).
- Bastok, Cruik, Dresdene, Bana, Okchabursk, Sudentor and the straits are not
  mapped to states; the territorial rows use the observed foothold instead.
- Wave E (Emmeria–Estovakia War), Wave F1 (Lighthouse War) and Wave F2
  (Leasath and the 2019–2020 crisis lanes) remain.
