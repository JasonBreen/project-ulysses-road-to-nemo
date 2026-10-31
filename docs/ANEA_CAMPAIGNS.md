# Anea campaigns — national content and implementation ledger

Status: **implemented in source; offline regression coverage; native acceptance pending**.
Base: merged PR #29, `cf8fec41abe5080b1af66eb86189b35c7af522f6`.
This ledger covers the national campaigns. [Foundation](ANEA_FOUNDATION.md)
and the shared regional owner retain their separate contracts and evidence.
Nothing in this content authorizes normal-install synchronization or resumes
the paused native testing session.

## Delivered national content

| Country | Persistent tree | Foundation | Warning/preparation | Crisis/recovery | Total |
| --- | --- | ---: | ---: | ---: | ---: |
| Emmeria, `EMM` | `ac_anea_emm_tree` | 18 | 18 | 18 | 54 |
| Estovakia, `EVA` | `ac_anea_eva_tree` | 18 | 18 | 18 | 54 |

The 108 definitions include exclusive alternatives. They are not 108 focuses
that a single playthrough must complete. Every focus has an individual name,
substantial description, explicit position, reward, eligibility and artwork
binding. Standard costs are five weeks/35 days; major institutional commitments
cost ten weeks/70 days. Definitions and text are authored in
`tools/anea/content.py`; `tools/anea/build_campaign.py` generates the shipped
bundle and verifies its bytes with `--check`.

The additional bundle contains **31 enduring national spirits**, each with a
countervailing modifier, **16 substantive narrative events**, two historical
focus-priority plans, and `ac_anea_campaign_weekly`, called after the regional
owner has initialized the country and resolved its calendar.

### Emmeria

The foundation connects an honest national account to protected civilian or
defence allocations. Four independently useful programmes develop government,
workshops and freight, military sustainment, and civilian diplomatic contacts.
Military readiness improvements do not add civilian preparedness.

The warning act has four programmes: shelters and evacuation records; emergency
freight, medical stores and essential-service teams; sustainable military
readiness; and public warning/relief contacts. The capital-shelter commitment
waits for 20 September 1998. Military programmes remain available after the
crisis, while civil preparation rewards expire on 8 July 1999.

The recovery act preserves domestic services while confronting the limits of
foreign assistance. Broad assistance and conditional assistance are exclusive
national mandates; actual aid still requires the shared owner's bilateral offer,
recipient consent, paid service authorization and staged deliveries. Domestic
repair, defence, receiving-liaison and consultative conclusions remain useful if
the partner refuses, disappears, becomes a subject, capitulates or enters war.

### Estovakia

The foundation presents **audited civilian distribution versus command-directed
distribution** as an enduring choice with opposing civilian/military benefits.
Industrial maintenance, military repair capability and practical civilian foreign
contacts form the other independent programmes.

The warning act separates practical civil protection from military preparation.
The Chandelier branch offers retaining an unfinished research team or redirecting
engineers to civilian protection. The routes join at preservation of the technical
record. Neither route unlocks an operational weapon, removes the crisis or grants
an invented installation on the map.

The recovery act offers monitored civil access or domestic self-reliance, with
useful repair and military conclusions in either case. Narrative event
`ac_anea.206` permits a costly explicit reform of earlier command-directed
distribution; it changes the national policy, not the shared diplomatic offer.
Such a reform does not erase completed focus history. The shared owner evaluates
whether the reforms and actual monitored deliveries earn an alternative at the
sanctions review.

## Graph and save contracts

Each tree has three root entry points. The warning root requires the international
announcement period; the recovery root requires the resolved regional crisis.
No recovery root requires completing every foundation or preparation node.
Short prerequisites connect related work, and a common child after two exclusive
alternatives uses an **OR prerequisite block**.

The concluding assessment instead has **four separate prerequisite blocks**:
the civilian, military, aid/receiving and consultation lanes must each finish.
Every lane has a domestic conclusion. The assessment requires the 2005 reporting
period but has no upper date limit. Actual work finishing in January 2006 remains
eligible; setting the ready flag or firing the event early is not an acceptance
shortcut in the shipped content.

Every reward repeats its country, eligibility, phase/date and once-only guard.
Capitulation or an expired civil-preparation period therefore blocks even a
manually repeated completion effect. Research bonuses are single-use and use
existing `industry`, `electronics` or `naval_equipment` technology categories.

Expired civil preparation has `bypass` only when the regional owner has set
`ac_anea_late_crisis` on **first initialization after the crisis**. The bypass
contains no reward. A normal campaign arriving at the crisis with unfinished
work receives no automatic completion or preparedness. Military warning nodes
have no preparation bypass because they remain evergreen.

Narrative dispatch uses separate sent and answered flags. Both options share
the same answered guard, preventing a repeated event/other option from granting
another reward. Historical briefs respect the owner's specific `*_past` flags;
they do not treat an old save initialized in 1992 as if all later history had
already expired. The starting account/allocation briefs additionally require a
new-campaign opening. The assessment remains tied to actual completed work.

## Narrative and public interfaces

| Subject | Emmerian event | Estovakian event | Effect of the choice |
| --- | --- | --- | --- |
| Opening account | `ac_anea.101` | `ac_anea.201` | Public confidence versus coordinating discretion, with political cost |
| Domestic allocation | `ac_anea.102` | `ac_anea.202` | Public budget/complaints review versus departmental or command discretion |
| International warning | `ac_anea.103` | `ac_anea.203` | Civil preparedness versus trained military staff |
| Revised Anean preparations | `ac_anea.104` | `ac_anea.204` | Shelter/transport checks versus retained military or technical personnel |
| Crisis assessment | `ac_anea.105` | `ac_anea.205` | Civil repair capacity versus military maintenance/training |
| Assistance policy | `ac_anea.106` | `ac_anea.206` | Delivery preparation/domestic reserve; costly audited reform/domestic repair |
| Sanctions response | `ac_anea.107` | `ac_anea.207` | Independent review/checkable repairs versus readiness staff |
| Concluding assessment | `ac_anea.108` | `ac_anea.208` | Permanent recovery institution with recurring cost versus immediate recovery |

Each country uses four related narrative compositions: events 1–2 share its
domestic scene, 3–4 its preparation scene, 5–6 its crisis/aid scene, and 7–8 its
recovery scene. Their art references are `GFX_ac_anea_event_emm_1`–`_4` and
`GFX_ac_anea_event_eva_1`–`_4`.

The campaign's public policy flags are:

- `EMM_an_civil_priority` / `EMM_an_defence_priority`.
- `EMM_an_broad_aid` / `EMM_an_conditional_aid`.
- `EVA_an_audited_distribution` / `EVA_an_command_distribution`.
- `EVA_an_aid_open` / `EVA_an_self_reliance`.

Matching policy spirit IDs append `_spirit`. Other enduring service policies
are enumerated in `POLICIES`, including exact modifiers and ongoing costs.
`EMM_an_bureau_ready` and `TAG_an_assessment_ready` identify completed national
work. They do not themselves create a bureau or a foreign agreement.

The campaign calls only the shared public offer effect when appropriate and
reads the shared calendar/outcome flags. It never writes the shared accord,
service, sanctions or bureau outcomes. The two sanctions-response events select
their text from the actual active, avoided, subsequently lifted or
limited/ineligible outcome. A date
alone cannot produce a false announcement that sanctions were imposed.

## Source and adaptation ledger

Sources checked 30 October 2026. Entries paraphrase official sources; all
institutions, programme titles, numeric rewards, policy weights, milestones'
gameplay gates and alternative outcomes are **provisional gameplay**, unless a
specific source row below establishes the underlying historical claim.

| Claim or content | Source layer and exact reference | Affected IDs | Disposition |
| --- | --- | --- | --- |
| International discovery/announcement period, 10 December 1994 | Official: [Chronicle, 1994 / 12.10](https://acecombat.jp/en/chronicle/details/) | `EMM_an_scientific_desk`, `EVA_an_risk_office` and warning act eligibility | The date opens authored technical/planning work; no invented local prediction. |
| FCU public impact warning, 20 April 1996 | Official: [Chronicle, 1996 / 04.20](https://acecombat.jp/en/chronicle/details/) | `ac_anea.103`, `.203`; shared `ac_anea_warning` | National response choices and their costs are authored alternatives. |
| Risk estimate includes eastern Anea, 29 July 1998 | Official: [Chronicle, 1998 / 07.29](https://acecombat.jp/en/chronicle/details/) | `ac_anea.104`, `.204`, late district shelter/freight gates | No exact impact footprint or province damage is inferred. |
| Emmerian capital shelter construction begins, 20 September 1998 | Official: [Chronicle, 1998 / 09.20](https://acecombat.jp/en/chronicle/details/) | `EMM_an_shelter_refit`, `ac_anea.104` | Represented by a civil-preparedness commitment; no unsupported map landmark or city mapping. |
| Ulysses Roche-limit crossing, 8 July 1999 | Official: [Chronicle, 1999 / 07.08](https://acecombat.jp/en/chronicle/details/) | Warning cutoffs, `ac_anea.105`, `.205` | The same-day regional crisis resolution is an existing campaign gameplay handoff, not an assertion that this is the exact local impact timestamp. |
| Emmerian aid begins 10 January 2000 and is later frozen amid failed reconstruction/distribution | Official: [Chronicle, 2000 / 01.10](https://acecombat.jp/en/chronicle/details/) | `EMM_an_aid_review` branch, `EVA_an_aid_position` branch, `ac_anea.106`, `.206` | Offer/service duration, domestic mandates and earned alternatives are provisional; shared owner controls the accord. |
| Sanctions against Estovakia, 20 March 2002 | Official: [Chronicle, 2002 / 03.20](https://acecombat.jp/en/chronicle/details/) | Review branches and `ac_anea.107`, `.207` | Historical preference, with visible earned alternative; shared review outcome determines narrative wording. |
| Republic of Anea preparatory agency, 1 February 2004 | Official: [Chronicle, 2004 / 02.01](https://acecombat.jp/en/chronicle/details/) | `EMM_an_consultative_agency`, `EVA_an_anea_delegation` | Authored civilian consultation; no forced merger, common state, faction or Nordennavic participation. |
| Chandelier incomplete when Ulysses arrived | Official: [Super Weapons, Chandelier](https://acecombat.jp/en/chronicle/weapons/) | `EVA_an_chandelier_account`, `_chandelier_research`, `_redirect_engineers`, `_technical_archive`, `_civilian_salvage`; `.204` | Unfinished research/redirection/civil engineering only; operational and later wartime uses excluded. |
| Office leaders, tags and existing flags | Mod provenance and user-approved office representation from PR #29 | `EMM`, `EVA` identities | Preserved; no named leaders, biographies, borders or dates of office invented. |
| All remaining 1991 domestic/governance, military, industrial and recovery policy | Provisional gameplay: approved Anea plan, 30 October 2026; explicit rows in `tools/anea/content.py` and `POLICIES` | All `EMM_an_*`, `EVA_an_*`, national narratives and priority plans | Implemented as authored alternatives. No claim that these programmes are official historical institutions. |

## Verification and reproducibility

```powershell
python -B tools/anea/build_campaign.py --check
python -B tools/Test-AneaCampaign.py
```

The focused suite has eight tests covering all 108 rewards with fiscal simulation
on/off, graph references and positions, exclusive policy joins, domestic recovery
completion after refusal/war/annexation/subject status, all four capstone lanes,
January 2006 assessments, preparation expiry/late bypass, evergreen military
work, narrative expiry and actual-outcome text, duplicate dispatch/option rewards,
BOM localization and generated consistency.

The suite executes the shipped Clausewitz subset through the existing offline
campaign harness. It deliberately isolates the national bundle from bilateral
transactions; its offer trigger is false and the shared-owner suite tests actual
aid delivery. Deep-copy checkpoints in related suites represent offline state
restoration, not native save serialization. This is not native parser, UI, AI,
balance, campaign pacing or save/load acceptance.

`python -B tools/Test-AneaIntegration.py` additionally executes the actual national
focuses and narrative options against the shared regional owner. Its five tests
cover the preferred historical policy course reaching suspended aid and sanctions,
the audited/conditional route earning two actual service periods and an alternative
review under all fiscal/council rule combinations, self-reliance withdrawing a
live service/bureau, annexation followed by release cleaning stale service ideas,
and a newly selected generic focus at zero progress deferring opt-in tree entry.
The last check uses the installed engine's documented
`has_shine_effect_on_focus` trigger; the model does not establish native rendering
or engine execution. These are explicit scripted branch checks. They do not model
natural production, political-power accrual or stochastic AI selection.

Native follow-up must exercise both national allocation routes, the research/
redirection choice, refusal and interruption, each assessment, actual AI selection
across date gates, long descriptions and focus states. Preserve the paused native
session and the existing PR #29 acceptance debt until separately authorized.
