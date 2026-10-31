# Anea — The Burden of Recovery

Implementation base: `cf8fec41abe5080b1af66eb86189b35c7af522f6` (merged PR #29).
This package adds Emmeria (`EMM`) and Estovakia (`EVA`) from January 1991 through
the covered 2005 recovery assessments. Source/offline validation and native
acceptance are separate. The ordinary installation and user saves are untouched.

## Source ledger

| Claim / subject | Layer | Exact reference | Affected content / disposition |
| --- | --- | --- | --- |
| 1991 start, tags, borders, cores, province assignments and manpower | Mod provenance | Implementation base, `history/countries/EMM - Emmeria.txt`, `EVA - Estovakia.txt`, 76 owned state histories | Preserved identities and territory; inherited demographic values are not canon evidence. |
| Revised risk includes eastern Anea, 29 July 1998 | Official | [ACES Chronicle Details](https://acecombat.jp/en/chronicle/details/), 1998 / 07.29, verified 30 October 2026 | `ac_anea_risk_revised`, narrative104/204, preparation branches; no invented impact provinces. |
| Capital shelter construction in Emmeria, 20 September 1998 | Official | Same primary source, 1998 / 09.20 | Emmerian shelter narrative/branch framing; placements and rewards are provisional. |
| Roche-limit crossing, 8 July 1999 | Official | Same primary source, 1999 / 07.08 | Crisis handoff date inherited from existing campaign convention. The handoff is a gameplay timing choice, not a claim of an exact impact timestamp. |
| Emmerian assistance to Estovakia from 10 January 2000; later frozen amid reconstruction failure/diversion | Official | Same primary source, 2000 / 01.10 | Aid initiative and historical AI course. Exact offer expiry, service intervals and suspension tests are authored gameplay. |
| Osea, Emmeria and other countries impose sanctions, 20 March 2002 | Official | Same primary source, 2002 / 03.20 | Emmerian sanctions-review framing, news10. This package does not commandeer Osean policy or force an Osean government event. Earned alternatives/news11 and later lifting/news12 are provisional. |
| Republic of Anea preparatory agency, 1 February 2004 | Official | Same primary source, 2004 / 02.01 | Consultative-bureau framing. Membership, consent and benefits are provisional; no constitutional union is implemented. |
| Chandelier incomplete when Ulysses arrived | Official | [ACES Super Weapons](https://acecombat.jp/en/chronicle/weapons/), Chandelier entry, verified 30 October 2026 | Estovakian technical branches; no operational weapon, anti-asteroid interception reward or later attack. |
| National administration / unknown 1991 individual | User-approved office representation | 30 October approved plan and `tools/usea_expansion/leaders.json` | Retain office characters and national flags; no invented human portraits, names or biographies. |
| All national policies, numerical rewards, alternate outcomes, forces, industry, resources, provisional regional labels, placement and AI weights | Provisional gameplay | User-approved Anea plan, `tools/anea/content.py`, `foundation.json`, `build_system.py` | Implemented game calibration; not new official-history claims. |

The [foundation record](ANEA_FOUNDATION.md) contains exact placements, industry,
rosters and conservation checks. The [campaign record](ANEA_CAMPAIGNS.md) lists
the 108 focuses, national policies and narrative gates. The artwork record and
`tools/anea/original_art.json` retain sources, full prompts, hashes and packaging.

## Public contracts and ownership

`ac_anea_` owns regional initialization, bounded measures, calendar, consent,
services, sanctions and bureau state. National focuses use `EMM_an_` / `EVA_an_`.
Events1–99 are shared;101–108 and201–208 are the eight narratives per country.
One tree per country (`ac_anea_emm_tree`, `ac_anea_eva_tree`) persists throughout.

Neither country joins `ac_pwi_participant` or `ac_ucw_participant`. Anea never
reseeds their variables, changes Continental War outcomes, creates an ISAF or
faction membership, or writes special-project state. Fiscal and faction councils
can each remain disabled. The regional system has no treasury, loan or money
transfer effects. Actual costs are political authority and national modifiers.

Initialization precedes all national reward application and never repeats.
Preparedness and recovery start at0 and clamp0–100. The crisis transition sets
recovery once: EMM `min(90,70+floor(preparedness/5))`; EVA
`min(40,15+floor(preparedness/4))`. Threshold additions implement floor using
known engine primitives, avoiding assumptions about engine rounding.

Military training and military policy affect experience, production or readiness
modifiers. They do not increase civil preparedness without a specifically
authored dual-use civil benefit. The measures are visible in decision-category
descriptions, with delivery counts and actual diplomatic status.

## Bilateral service lifecycle

- The founding offer is attempted once from10 January through10 March2000 and
  has a60-day reply window. The pending flag is set before scheduling the reply.
  Eligibility is checked again by the reply effect. Refusal, expiry and invalid
  participants close it without aid, equipment or invented money.
- Both countries must exist, be independent, uncapitulated and at peace with
  one another. A self-reliant Estovakian policy cannot accept or maintain aid.
  A conditional Emmerian mandate requires audited Estovakian distribution.
- An accepted accord permits separately authorised180-day services. EMM pays
 25PP upfront and carries1% consumer goods while a service is active. Audited
  EVA participation pays15PP upfront and carries a small administrative cost.
  Neither payment repeats on daily checks or reload.
- Prepare, repair and training allocations are mutually exclusive for180days,
  so their shared construction burden cannot be paid once for concurrent jobs.
- Deliveries occur at60,120 and180days. An uninterrupted monitored service gives
 4 recovery per delivery; command distribution gives2. A mid-service loss of
  audit status permanently downgrades that service's monitored result.
- A completed service has a180-day cooldown. Monitored completion increments
  EMM's cycle count; command-distributed completion freezes further assistance.
  Audited reform can reopen a frozen programme for25PP; actual service costs
  remain separate. One founding-offer guard does not prevent service renewal.
- Daily maintenance on EMM, EVA and NEC catches annexation even when the donor
  no longer receives callbacks. Interruption removes only owned temporary
  bilateral modifiers and future deliveries. Costs and delivered aid remain.

On the2002 review, audited EVA distribution, two completed monitored services,
EVA recovery>=40 and a valid accord enable the alternate outcome. The review
flag is separate from active sanctions. News follows actual policy. Later
verified reform can lift active sanctions once without replaying the review.
Historical AI supplies policy preferences, not a forced result after player
intervention. Exact-date gates are serviced by the existing weekly convention;
dispatch can occur on the following weekly callback.

The2004 bureau requires a valid accepted accord and no active sanctions.
Nordennavic receives a separately guarded60-day invitation. Refusal or expiry
preserves the bilateral bureau. Benefits concern civilian infrastructure only.
No state, border, faction, war or common government is created.

## Save and campaign boundaries

New campaigns receive the complete history/OOB foundation. No startup effect
injects factories, resources, technology, forces or stockpiles into saved games.
Late first initialization records passed milestones and neutral current-phase
recovery. It grants no expired preparedness, old aid initiative or historic
review reward. Before1999, eligible future civil preparations remain available.

An explicit entry decision lets existing generic-tree saves adopt the national
tree, retaining completed content. Its focus-progress guards defer switching
while a generic or continuous focus is in progress. Native validation of this
engine behaviour remains on the acceptance checklist. No weekly effect swaps
an old save's tree automatically.

Expired preparation nodes bypass without payout only for late crisis entry.
Normal campaigns receive no automatic preparation reward. Recovery branches do
not require completing all preparations. Domestic conclusions survive refusal,
isolation and interruption. A genuinely completed final chain can be assessed
after2005; already authorised service deliveries can also finish after year-end.
New service authorisations close at the2005 cutoff. No later war is authored.

## Builder and reproducible workflow

The user-supplied installed Mod Builder was opened for a scratch compatibility
check. Its payload reports0.4.4. Window capture timed out twice; no import,
export, installation write or project change was made. Desktop interaction
stopped when the user requested their PC back. Authoring uses repository
generators; builder compatibility is unverified and is not a build dependency.

From repository root, reproduce in this order:

```powershell
python -B tools/anea/foundation.py
python -B tools/anea/build_campaign.py
python -B tools/anea/build_system.py
python -B tools/anea/build_art.py
python -B tools/usea_expansion/build_leaders.py
python -B tools/anea/build_briefs_ui.py
```

Each supports `--check` without rewriting tracked output. Requirements are pinned
in CI; artwork sources are committed, so reproduction requires no image service.
See [acceptance and native gaps](evidence/anea/ACCEPTANCE.md) for measured coverage.
