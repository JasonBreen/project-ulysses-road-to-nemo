# Content plan: closing the 1991–2020 overhaul

Status: **planning proposal.** This document has not been approved as scope and
nothing in it has been implemented. It does not change the approved budgets in
[STRANGEREAL_OVERHAUL.md](STRANGEREAL_OVERHAUL.md) or
[`release_plan.json`](../tools/overhaul/release_plan.json). It splits the
work those files leave open into reviewable waves. Native testing remains paused
under issue #8.

Planning base, 1 November 2026:

- `main` at `25ab672` (PR #36 merged).
- Open integration PR #59 (`codex/strangereal-naval-systems-review`, head
  `cba5fd1`), which folds the reviewed #33–#57 stack into main.
- Open story PRs #60 (Osean *Second Frequency*) and #61 (Yuktobanian
  *Names on the Board*).

Files named in `code` below without a link exist on the PR #59 head but not yet
on `main`.

## 1. Where the overhaul stands

Counts come from `release_plan.json` on the PR #59 head. They include mutually
exclusive alternatives and do not prove engine reachability.

| Item | On `main` | With #59–#61 | Still open |
| --- | ---: | ---: | --- |
| Country focus additions (of 1,028) | 234 | 572 | **456** |
| SNS, AMB, UGE, DEL, OSE, YUK, NPT, REC, SAP, GEB, FAT, SBK budgets | partial | complete in source | native acceptance |
| ERU / FCU / EMM / EVA / NEC / AUR / LEA budgets | — | ERU 0, FCU 6, others 0 | 90 / 48 / 54 / 66 / 42 / 84 / 72 |
| Independent squadron stories (20 chapters each) | 6 | 8 (OSE, YUK in #60/#61) | AUR, LEA |
| Dated war owners | 1991–2005 (`ac_belkan_*`, `ac_pwi`, `ac_ur`, `ac_ucw`) | same | **every conflict after 2005** |
| Conventional land/air/naval research | — | through 2020, provisional (`ac_air_`, `ac_naval_`, land packet) | sourced projects and naming (#5) |

The remaining work falls into three kinds:

1. **Seven country budgets (456 definitions).** Five are tied to wars after 2005.
   Two (AUR and LEA) have world-start foundations but no tree.
2. **Six conflict owners after 2005.** None exist. The repository has a source
   ledger only up to 2005.
3. **Two stories** (Aurelia, Leasath), plus Anean cast continuations where the
   earlier conclusions allow them.

## 2. Gate 0: the 2006–2020 source ledger

[USEAN_CONTINENTAL_WAR.md](USEAN_CONTINENTAL_WAR.md) gated the 1999–2005 round:
every scripted date had a cited Chronicle row before any script was written. The
same gate is needed for 2006–2020. Today the repository has only the seven
anchors in `release_plan.json` → `chronology`, checked 31 October 2026:

| Anchor | Date in source | Waves |
| --- | --- | --- |
| Free Erusea insurrection | 2006.9.26 | A |
| Estovakian civil war | 2007.6.30 – 2013.10.29 | B |
| Circum-Pacific War | 2010.9.27 – 2010.12.31 | C |
| Emmeria–Estovakia War | 2015.8.30 – 2016.4.1 | E |
| Lighthouse War | 2019.5.15 – 2019.12.1 | F1 |
| Leasath civil war ends | 2019, day unknown | F2 |
| Aurelia–Leasath conflict | 2020.10 – 2020.12, days unknown | F2 |

**Deliverable:** `docs/STRANGEREAL_2006_2020_SOURCES.md`, using the same columns
as the 1994–2005 ledger (claim, exact citation, planned content, disposition).
It covers every [Chronicle](https://acecombat.jp/en/chronicle/details/) entry
from October 2005 to December 2020 and every
[Super Weapons](https://acecombat.jp/en/chronicle/weapons/) entry active in that
period. Each wave below lists the rows it needs. A wave may not script a
participant, date, place, leader or weapon that has no row.

**Blocker:** `acecombat.jp` is not reachable from the current cloud session's
network policy. The ledger needs that host allowed, or page captures supplied by
the user.

## 3. Proposed waves

Every wave follows the existing contracts. Each conflict owner is the only writer
of its calendar, declarations, stage markers and outcome observations. Country
trees read its flags and never write them. Economic effects go through the
guarded macro APIs (`spend`, `receive`, `commitment`, `loan`, `aid`,
`procurement`, `shock`, `readiness`). Focuses default to 35 days, with 70 days
for major commitments. Historical AI follows the sourced route. Alternatives
must be earned. Rewards are guarded against repetition, interruption and late
saves.

The six conflict namespaces below were checked against the PR #59 head and are
unused: `ac_fe`, `ac_ecw`, `ac_cpw`, `ac_eew`, `ac_lhw`, `ac_alc`. Country focus
IDs keep the tag-and-lane pattern (`ERU_fe_*`, `EVA_ecw_*` and so on); existing
tree IDs (`ac_anea_emm_tree`, `ac_anea_eva_tree`, the ERU/FCU trees) are
extended, never replaced.

### Wave A: Free Erusea and the oversight years (2005–2009, Package 3)

- **Budget:** ERU 36, FCU 24 (60).
- **Owner:** `ac_fe`. Armed by the 2006.9.26 anchor only when the live state
  allows it.
- **Reads:** `ac_ucw_outcome_isaf_victory`, `ac_ucw_outcome_erusean_victory`,
  `ac_ucw_outcome_stalemate`, `ac_ucw_war_averted`, `ac_ucw_megalith_destroyed`,
  and the 2005 / 09.26 provisional-government record
  (`ac_ucw_eru_provisional_government`, `ERU_ucw_provisional_government`,
  `ERU_ucw_rebuild_under_oversight`).
- **Routes:**
  - *Sourced:* after an ISAF victory, the insurrection runs against the
    oversight arrangement.
  - *Earned alternatives:* an Erusean-victory administration, armistice-line
    management after a stalemate, and ordinary development after an averted war.
    Each alternative is a mutually exclusive lane counted in the 36.
- **Proposed ERU lanes (about 12 each):** the oversight relationship; the
  security response to the insurrection, set against reconciliation;
  reconstruction and the return of displaced people. The return lane builds on
  the 2000 refugee-closure record without inventing impact zones.
- **Proposed FCU lanes:** oversight administration, or ISAF wind-down where
  there was no ISAF victory; security response; partner burden-sharing that
  reads existing SNS/AMB/UGE/DEL partner flags.
- **Gate 0 rows needed:** everything from 2005.10 to 2009.12 that concerns
  Erusea, FCU or ISAF.
- **Forbidden:** `transfer_state`, new tags, named insurgent leaders, any forced
  government swap.

### Wave B: Estovakian fracture (2007–2013, Package 3)

- **Budget:** EVA 30, EMM 18 (48).
- **Owner:** `ac_ecw`, anchored 2007.6.30 to 2013.10.29.
- **Reads:** the existing Anea flags, including the Chandelier branch
  (`EVA_an_chandelier*`), Emmerian aid posture (`EMM_an_broad_aid`,
  `EMM_an_conditional_aid`, `EMM_an_aid_restraint`), and the 2002 sanctions and
  2004 agency records.
- **Mechanic decision (needed before scripting):**
  - *Option 1, recommended first:* a tagless internal-conflict owner. Contested
    authority is a bounded variable driven by decisions, stability, readiness
    and economy shocks. The map does not change and saves stay safe.
  - *Option 2:* a temporary HOI4 civil-war tag. The release plan permits this
    only with a reviewed source, a state mapping, a lifecycle and a
    save-continuity contract.
- **Proposed EVA lanes:** the conflict owner's government/opposition balance;
  civilian survival and maintenance; the 2013 settlement. Alternatives are an
  earlier earned settlement, earned by strong Anean recovery choices, and
  prolonged instability.
- **Proposed EMM lanes:** a humanitarian corridor, aid conditionality, border
  security. These continue, not replace, the 1998–2004 Anean choices.

### Wave C: Circum-Pacific War (2010, Package 3)

- **Budget:** no focus definitions, because OSE (150) and YUK (120) are complete
  in #59. This wave delivers the war owner, decisions, news and story hooks.
- **Owner:** `ac_cpw`. The consumer contract is already defined in
  `docs/PACIFIC_NATIONAL_CONTINUATIONS.md`:
  - the owner has its own calendar and declarations;
  - the principal pair and immediate participants are inspected for existing
    wars;
  - entry by a third party moves the crisis to external observation;
  - factions or guarantees alone never veto a new declaration;
  - there is no scripted white peace;
  - end news follows actual cessation, not the 2010.12.31 anchor.
- **Reads:** `ac_snc_ose_verification_earned`, `ac_snc_ose_channel_earned`,
  `ac_snc_yuk_verification_earned`, `ac_snc_yuk_channel_earned`, the scientific
  variants, and Arkbird state.
- **Routes:** the sourced war, earned de-escalation (both verification and
  channel records earned), and external observation.
- **Arkbird:** the 1999 `ac_sp_arkbird` project is explicitly non-weapon. Any
  2010 change to Arkbird is a new project state that needs its own Super Weapons
  row. National consumers never create, revive, weaponize or complete it.
- **Stories:** the Osean and Yuktobanian stories in #60/#61 may read CPW
  observations where their contracts allow. Concluded casts are never revived.
- **Gate 0 rows needed:** every 2010 entry, including any non-Osean or
  non-Yuktobanian actors the Chronicle names. Those actors appear only as the
  Chronicle states them.

### Wave D: Nordennavic (1991–2016, Packages 1/3/4)

- **Budget:** NEC 42, proposed as 18 for 1991–2005, 12 for 2006–2013 and 12 for
  2014–2016.
- **Existing hooks:** the world start (regional maritime reserve), the
  institution (scope of consultation) and the guarded 60-day invitation to Anean
  consultative cooperation (`docs/ANEA_EXPANSION_LEDGER.md`).
- **Canon exposure:** low. Unless Gate 0 finds Chronicle rows, the tree is mod
  provenance plus provisional gameplay. That makes it the safest work to run
  alongside the canon-heavy waves.
- **Proposed lanes:** the maritime reserve and harbours; consultation scope with
  Anea (accept, limit or refuse, following the invitation outcome); a technical
  reserve; neutrality during the Anean war (Wave E).

### Wave E: the Anean war (2014–2016, Package 4)

- **Budget:** EMM 36, EVA 36 (72).
- **Owner:** `ac_eew`, anchored 2015.8.30 to 2016.4.1.
- **Reads:** the Wave B outcome, the 1998–2004 Anean choices, NEC consultation,
  and project state.
- **Routes (each tested separately, per Package 4 acceptance):**
  - the sourced war;
  - earned avoidance, from strong recovery plus aid plus consultation;
  - limited divergence;
  - interrupted-country routes, where one side was annexed or made a subject
    earlier.
- **Proposed lanes:**
  - EMM: wartime administration, evacuation built on the 1998 shelter records,
    and recovery;
  - EVA: war government, logistics and maintenance, and aftermath.
- **Squadron continuation:** *The Open Corridor* (EMM) and *The Last Serviceable
  Aircraft* (EVA) continue only for casts whose recorded conclusion permits it.
  The chapter count is a decision for the user (see §6).

### Wave F1: the Lighthouse War (2017–2019, Package 5)

- **Budget:** ERU 54, FCU 24 (78).
- **Owner:** `ac_lhw`, anchored 2019.5.15 to 2019.12.1. Participants, sequence
  and places come from Gate 0 rows, not from this plan.
- **Reads:** the Wave A oversight outcome and Free Erusea record, and the
  Continental War outcome.
- **Proposed ERU lanes:** politics after oversight; renewed tension and the war
  routes; aftermath. Alternatives must follow from Wave A outcomes. A
  stalemate-era or Erusean-victory history cannot fall back into the sourced 2019
  route by date alone.
- **OSE:** OSE is complete at 150 definitions, so Osea takes part through the
  owner's decisions and events only. Any Osean focus additions would need a
  budget change approved by the user.

### Wave F2: the southern theater (1991–2020, Packages 1/5)

- **Budget:** AUR 84, LEA 72 (156). Two 20-chapter original stories, each with
  4 core cast, 4 portraits, 8 illustrations and 1 loading screen, matching the
  first-wave ratio.
- **Owners:** `ac_alc` for the Aurelia–Leasath conflict, plus a Leasath
  civil-war closure owner. The source gives only a month (2020) or a year
  (2019) for these, so they are **state-based**: news fires on observed state,
  never on an invented day, and unknown days stay unknown in the ledger.
- **Parallel start:** the 1991–2018 foundation lanes of both trees depend on no
  post-2005 conflict owner. The existing world starts, institutions and
  political-office systems already provide their entry points, so these lanes
  can start before Gate 0 closes. Only the 2019–2020 crisis lanes wait for it.
- **Technology:** this wave closes Package 5's sourced 2006–2020 project and
  equipment progression together with issue #5.

## 4. Budget allocation

| Tag | Open | A | B | C | D | E | F1 | F2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ERU | 90 | 36 | | | | | 54 | |
| FCU | 48 | 24 | | | | | 24 | |
| EVA | 66 | | 30 | | | 36 | | |
| EMM | 54 | | 18 | | | 36 | | |
| NEC | 42 | | | | 42 | | | |
| AUR | 84 | | | | | | | 84 |
| LEA | 72 | | | | | | | 72 |
| **Total** | **456** | 60 | 48 | 0 | 42 | 72 | 78 | 156 |

These splits are proposals inside the approved per-country totals. They do not
change any total.

## 5. Cross-cutting tracks

- **Belka and Ustio cohesion** (no fixed quota). Carry the outcomes of *The Peace
  We Inherit* into 2006 and later through decisions and narrative consequences
  only. Belkan or Ustian roles in later conflicts appear only where a Gate 0 row
  names them.
- **Joker 1 (issue #6).** Blocked until the user compiles the outline listed in
  [CANON_POLICY.md](CANON_POLICY.md) into dated, sourced private references. No
  wave may use it before then.
- **Special projects after 1999.** Track C gains a project only from a Super
  Weapons row. Chandelier stays as the Anea ledger records it.
- **Save/reload checkpoints** at 2005, 2010, 2016 and 2020 are acceptance gates
  for the waves that cross them. They are native work under #8 and stay paused.
- **Anti-vanilla conversion** remains Package 1 work. It is not content, but
  every new screen must pass the existing strict asset and briefing checks.

## 6. Recommended order and decisions

1. **Gate 0 and the open stack.** Allow `acecombat.jp` or supply captures, and
   land #59–#61 so new waves branch from a current `main`.
2. **Wave A, Wave D, and the F2 foundation lanes in parallel.** Wave A extends
   the most developed owner (`ac_ucw`). D and the F2 foundations depend little
   on canon.
3. **Wave C.** Its consumer API is already published in #59.
4. **Wave B**, once the civil-war mechanic is chosen.
5. **Wave E**, then **F1**, then the **F2 crisis lanes and stories.**

Decisions the user needs to make:

| # | Decision | Recommendation |
| --- | --- | --- |
| 1 | Network access for Gate 0 | Allow `acecombat.jp` for research sessions |
| 2 | Base for new waves | Wait for #59–#61 to merge, or stack on the #61 head |
| 3 | First wave | A + D, with the F2 foundation lanes in parallel |
| 4 | Estovakian civil war mechanic | Tagless owner first; temporary tag only after a source and mapping review |
| 5 | Anean squadron continuation size | Short eligible-cast epilogues, for example 4–6 chapters per story, outside the 20-chapter core |

## 7. Out of scope

- Anything after 2020. The 2065 engine permission is not authored content.
- New borders, cores or `transfer_state`. State 171 and the `XXX` regions stay
  untouched without an approved source-backed geography decision.
- Named canon leaders, biographies or portraits beyond what a Gate 0 row
  supports.
- Native runtime claims of any kind.
