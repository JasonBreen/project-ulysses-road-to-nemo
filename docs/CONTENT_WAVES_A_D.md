# Content waves A and D: source and implementation ledger

Status: **implemented in source; offline checks pass; native acceptance pending.**
Generator: `tools/content_waves/`. Plan: [CONTENT_PLAN_2006_2020.md](CONTENT_PLAN_2006_2020.md).
Base: `main` at `978ef9e` (PRs #59–#62 merged). No HOI4 installation, profile, save
or desktop was touched. Native testing remains paused under issue #8.

| Wave | Country | Tree | Definitions | Horizon | Release-plan effect |
| --- | --- | --- | ---: | --- | --- |
| A | Erusea (`ERU`) | existing `ac_ucw_eru_tree` | 36 | 2005–2009 | ERU 36 of 90 delivered; 54 left for Wave F1 |
| A | Central Usea (`FCU`) | existing `ac_ucw_fcu_tree` | 24 | 2005–2009 | FCU 30 of 54 delivered; 24 left for Wave F1 |
| D | Nordennavic (`NEC`) | new `nec_national_campaign` | 42 | 1991–2016 | NEC budget complete |

Counts include mutually exclusive alternatives and route-exclusive branches, so a
single playthrough sees fewer of them. The ledger now records **674 delivered and
354 remaining** country additions (`tools/overhaul/release_plan.json`).

## Source layers

| Claim or material | Layer and exact reference | Affected IDs and files | Status |
| --- | --- | --- | --- |
| Provisional autonomous Erusean government under ISAF oversight, 26 September 2005 | Official: ACES Chronicle 2005 / 09.26, already cited in [USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md) | Context for the ISAF-victory lanes `ERU_fe_oversight_*`, `FCU_fe_oversight_*` | Read-only use of existing `ac_ucw` outcome flags |
| Free Erusea's armed insurrection and its defeat by Mobius 1, 26 September 2006 | Official: Chronicle, 2006 / 09.26, in [STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md) | `ac_fe.1`, `ac_fe.5`, `ac_fe.6`, `ac_fe_begin`, `ac_fe_defeat`, flags `ac_fe_insurrection_started` and `ac_fe_insurrection_defeated` | Implemented as the historical route. Mobius 1 is named only in text; nothing else about the insurrection is asserted. |
| Continental War outcomes (ISAF victory, Erusean victory, stalemate, averted war) | Mod provenance plus provisional gameplay (`ac_ucw`) | Route gates on every Wave A register | Unchanged; read only |
| Nordennavic's country history, office, world start, institution profile and 2004 Anean bureau invitation | Mod provenance | `NEC_nc_*` entry context; `NEC_nc_anean_record` reads `ac_anea_nec_participates` / `ac_anea_nec_closed` | Unchanged; read only |
| All focuses, policies, services, dialogue and numbers, and the prolonged-insurrection alternative (pressure model, crisis review, containment) | Provisional gameplay | `tools/content_waves/free_erusea.py`, `nordennavic.py`, `framework.py` | Implemented; labelled in-game where it touches chronology |

No place, unit, battle, alliance, border, core, country tag, civil war or force
grant is added, and Mobius 1 is the only named individual, mentioned in text as
the Chronicle names them. The Gate 0 ledger
([STRANGEREAL_2006_2020_SOURCES.md](STRANGEREAL_2006_2020_SOURCES.md), compiled
3 November 2026) found that the insurrection was defeated on its outbreak date,
so the owner was reconciled: the defeat is the historical route and the long
insurrection is a labelled alternative.

## Branch shape and services

Every branch has six nodes: a register, two mutually exclusive enduring policies
(70 days each), an operational step, a review that needs a genuinely completed
funded service, and a standing settlement (70 days) that improves the chosen
policy by 20 percent and keeps its cost. Each branch owns two ninety-day services:
the first unlocks with the register, the second with the operational step.

A service costs 35 political power, four institutional-capacity points and the
shared programme fee through the real P1 owners (`ac_econ_pay_programme`,
`ac_pol_change_capacity`); disabled fiscal play keeps the political and
institutional costs. One service runs per country, followed by a ninety-day
cooldown. War, capitulation, annexation or cancellation ends a period without
completion credit or refund. Each branch has a scene with two replies and a
final assessment; each country has an opening and a national conclusion.
Unanswered messages are recorded as unanswered rather than invented.

Wave A: 30 events (24 narrative, 6 owner), 94 ideas, 22 decisions.
Wave D: 16 events, 60 ideas, 16 decisions (including tree adoption).
About 21,000 words of original English text.

## Wave A: the oversight years

| Branch | Country | Opens when | Lanes |
| --- | --- | --- | --- |
| `oversight` | ERU | ISAF victory, after `ERU_ucw_exp_settlement_assessment` | Civil ministries first / supervised security directorate |
| `insurrection` | ERU | ISAF victory and the insurrection has begun | District hearings / security cordons |
| `return` | ERU | Any outcome, after `ERU_ucw_exp_resettlement` | District return registers / central resettlement schedule |
| `victor` | ERU | Erusean victory | Local civil authority / standing garrison line |
| `armistice` | ERU | Stalemate | Joint line commission / fortified line posture |
| `ordinary` | ERU | War averted | Civil investment / standing readiness review |
| `oversight` | FCU | ISAF victory | Advisory oversight / supervising commission |
| `security` | FCU | ISAF victory and the insurrection has begun | Civil police liaison / rapid response detachments |
| `partners` | FCU | Any outcome | Published burden formula / Central Usean carriage |
| `drawdown` | FCU | Any outcome except ISAF victory | Peacetime duties / coalition reserve |

All registers also require `date > 2005.9.25`. The branches attach to the
existing trees through a marked `# BEGIN OVERSIGHT YEARS IMPORTS` block.
`tools/build_continental_war.py` now preserves marked import blocks owned by
later packages, so both generators' `--check` modes agree. No existing focus,
tree ID, position or continuous-focus position changed.

### The Free Erusea owner (`ac_fe`), tagless

- **Start:** the first Erusean weekly pulse on or after 26 September 2006 when
  `ac_ucw_outcome_isaf_victory` is set and Erusea owns land. `ac_fe.1` (major news)
  reports the outbreak and cites the Chronicle's record of its defeat.
- **Historical route:** Central Usea receives `ac_fe.5`. "Send Mobius 1" (AI
  always) sets `ac_fe_insurrection_defeated`, removes the tiers and issues
  `ac_fe.6`, which states the defeat as the Chronicle does. The pressure model
  never runs.
- **Provisional prolonged route:** "Leave the response to the provisional
  government", a Central Usea that cannot answer (absent, capitulated or at war
  with Erusea), or a 30-day window left unanswered sets `ac_fe_prolonged`. The
  answer re-checks that Central Usea can still respond: a Central Usea that
  capitulated or went to war with Erusea after `ac_fe.5` was queued sees no
  "Send Mobius 1" option and `ac_fe_defeat` stays inert, so the window lapses
  into the prolonged route.
  Pressure then starts at 55 of 100 and the rules below apply.
- **Late saves:** a first observation on or after 26 September 2007 closes the
  owner (`ac_fe_late_start_skipped`) without replaying the outbreak.
- **Other routes:** after an Erusean victory, stalemate or averted war the owner
  never starts.
- **Weekly drift:** +0.4. District hearings −0.7 and security cordons −0.9
  (settled versions too); an administrative emergency or partner assistance −0.5
  each; stability below 35 percent +0.3. Clamped to 0–100.
- **Relief:** a completed insurrection service −8; the insurrection settlement −8;
  the oversight settlement −3; a completed return service −3; a completed
  Central Usean security service −6; the Central Usean oversight settlement −3.
- **Tiers:** severe above 70, active above 35, residual otherwise. Each tier is a
  national spirit with stability and political-power penalties.
- **Crisis review:** above 85, at most once a year, `ac_fe.2` offers partner
  assistance under Erusean command (Central Usea answers in `ac_fe.4`: 40 political
  power and a six-month commitment, or a refusal) or a six-month administrative
  emergency.
- **Containment:** below 5 the owner records `ac_fe_insurrection_contained`,
  removes the tiers and issues `ac_fe.3`, which names the official defeat date.
- **Closure:** annexation, capitulation or subject annexation of Erusea closes
  the owner and removes the tiers.

## Wave D: the northern reserve

| Stage | Opens | Branches |
| --- | --- | --- |
| 1 | 1991 | `harbours`, `reserve`, `consultation` |
| 2 | 2006, after any stage-1 settlement | `technical_reserve`, `northern_routes` |
| 3 | 2014, after any stage-2 settlement | `neutral_waters`, `account` |

The new tree is selected for Nordennavic at game start (weight 45, above the
regional framework's 5). Saves that already hold the generic or regional tree can
adopt it with `NEC_nc_adopt_campaign`, under the same idle guard
(`ac_pol_previous_tree_idle`) used by FATO. Completed focuses are kept. The
consultation conclusion reads the existing Anean bureau invitation and never
writes it. The neutrality lane prepares rules for a neighbour's conflict without
assuming that the 2015–2016 war happens; Wave E owns that war.

## Artwork

320 original DDS textures, generated in code from the existing Ulysses glyph
library (`tools/content_waves/build_art.py`): 102 focus icons (96×96), 154 idea
icons (75×75), 38 decision rows (26×29), three categories (100×100), 20 country
event pictures fitted to 210×176 and three news pictures fitted to 397×153 with the
shared `event_picture_fit` helper. Hashes and roles are in
`tools/content_waves/assets.json`; galleries are in `tools/content_waves/gallery/`.
There are no engine, DLC or remote pixels, no portraits, flags or baked text, and
no watermarks.

## Validation

Run from the repository root with Python 3.12+ and Pillow 11.3.0 (CI-pinned):

```text
python -B tools/content_waves/build.py --check
python -B tools/content_waves/build_art.py --check
python -B tools/content_waves/test_waves.py
python -B tools/overhaul/check_release_plan.py
```

`test_waves.py` has 22 tests. The source half checks budgets, globally unique
IDs, localization (with BOM) for every focus, idea, decision and event, every
called scripted effect and trigger, sprite bindings, DDS dimensions, event-picture
fit through the shared audit, the import block preserved by the Continental War
generator, and the absence of territory, tag, war, faction, force and leader
effects. The runtime half executes the generated effects through the real P1
political and fiscal owners (`tools/Test-SharedSystems.py`) in full, experimental
and disabled fiscal modes:

- every service pays once and completes after 90 days, never earlier;
- shortfalls never authorize a service;
- policies exclude each other and reviews need a completed service;
- settlements swap the policy for its settled version exactly once;
- Nordennavic's stage dates and prerequisites are enforced;
- Erusean routes follow each Continental War outcome;
- the Erusean and Central Usean openings describe the actual war outcome;
- the insurrection starts only on or after the anchor after an ISAF victory;
- Central Usea's answer records the historical defeat by Mobius 1, and the AI always gives it;
- declining, being unable to answer or letting the window lapse gives the provisional prolonged route;
- a late first observation never replays the outbreak;
- policies and services reduce pressure, and containment freezes it;
- the crisis review fires once and its options have bounded costs;
- annexation closes the owner.

These are source and actual-script offline checks, not native acceptance.

Three shared review records count every country, decision or event, so they are
regenerated with every content change by `tools/content_waves/refresh_records.py`: `tools/world_foundation/country_registry.json`
(focus counts per country), `docs/evidence/decision-rows/consumer-bounds.json`
(977 → 1,015 row variants) and `docs/evidence/event-style/measurements.json`
(2,284 → 2,372 measured fields, with no title, body or parent-clearance clips).
The event-style record was produced with Windows path ordering, because the
generator sorts event files with platform path ordering. That ordering
reproduces the committed `main` record byte-for-byte, and the change consists
only of additions. PNG review sheets were left as committed; their pixels are
unchanged.

All 78 workflow Python steps were run in the Linux cloud session with the
CI-pinned Pillow 11.3.0. Apart from the two pull-request-only scan steps, the
following fail there on untouched `main` as well, with identical results:
`usean_partners/test_content.py`, `Test-AneaPresentation.py`,
`Test-InterfaceRepairs.py`, `Test-DecisionUI.py` (one PNG-sheet case),
`Test-EventStyle.py`, `build_continental_war.py --check`,
`Test-ReconstructionAssets.py`, `Test-SuperpowerAssets.py` and
`fato_south_belka/run_checks.py`. Each comes from PNG compression or path
ordering in that environment. The PR scan against `main` is clean. The
PowerShell static suite could not run because no PowerShell host is installed;
its Python checks were run directly and pass, except the Continental War check
listed above. The Windows CI run is the authority.

## Open items

- Native parsing, focus-screen rendering, AI pacing, balance and save/reload
  (issue #8).
- Gate 0: compile the 2005–2009 Chronicle rows and reconcile the insurrection
  owner with them.
- Waves B (Estovakian civil war, tagless first), C (Circum-Pacific War), E and F
  remain unimplemented.
