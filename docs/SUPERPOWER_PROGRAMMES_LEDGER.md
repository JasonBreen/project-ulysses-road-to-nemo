# Osea and Yuktobania: national programmes, first 96 definitions

SP96 is implemented and ready for source review. The integrated full phase passed
57 commands; current superpower and affected-parent follow-ups also pass. Those
phases cover all 59 unique commands in the final runner. Native gameplay remains
pending. No native game, desktop, user profile, normal installation or save has
been opened or changed during this packet. The roadmap now records 390 delivered
additions and 638 outstanding, including 48 new definitions per superpower. The
remaining approved additions are 44 Osean and 42 Yuktobanian. The separate 36-focus
regional framework is not counted again.

## Source and authorship boundaries

The [official ACES Chronicle](https://acecombat.jp/en/chronicle/details/) supplies
context: the Osea–Yuktobania Cold War in the 1980s, their October 1999 Arkbird
debris-clearance cooperation, the August 2008 summit, and the September–December
2010 Circum-Pacific War. These anchors do not establish the new institutions,
domestic incidents, policy alternatives, support measures, allocations or fees.
Those are original provisional gameplay. `tools/superpowers/sources.json` records
each anchor and its restricted adaptation separately.

No historical summit invitation, new officeholder, protected character continuity,
canonical capital assignment, war outcome or operational strategic weapon is
authored here. New dialogue comes from unnamed clerks, researchers, inspectors and
liaisons. Existing trees, elections, intervention and command-reform choices,
Arkbird cooperation and strategic projects retain their authoritative owners.
The namespace is `ac_snp`; `ac_sp` remains the inherited strategic-project owner.
All owned IDs use `ac_snp_`, `OSE_snp_` or `YUK_snp_`.

## National content and consequences

Each row contains six definitions: register, mutually exclusive civil/protected
policy, protocol, completed-service review and standing settlement. Each row also
has two specifically named funded 90-day service scopes and a branch response plus
assessment. Ordinary focuses take 35 days; the two policy alternatives and the
standing settlement take 70. Descriptions retain at least 90 words. A review
requires an actual completed funded period; a conclusion never requires foreign
acceptance. Later branches open in 2006 after the corresponding foundation.
Conclusions remain usable after 2020.

| Country | Opens | Branch | Continuing choice | Later dependency |
|---|---|---|---|---|
| Osea | 1991 | Appropriations | Public receiving hearings / protected federal mandate | None |
| Osea | 1991 | Productive capacity | Apprenticeship and civil repair / replacement readiness | None |
| Osea | 1991 | Continental transport | Civil dispatch windows / protected support schedules | None |
| Osea | 1991 | Air watch | Civil safety reporting / protected readiness returns | None |
| Osea | 2006 | Guarantor review | Public renewal hearings / limited guarantor mandate | Appropriations settlement |
| Osea | 2006 | Civil space | Public research methods / bounded protected testing | Air-watch settlement |
| Osea | 2006 | Procurement scrutiny | Independent acceptance tests / replacement priority | Productive-capacity settlement |
| Osea | 2006 | Crisis authority | Civil verification / bounded emergency mandate | Continental-transport settlement |
| Yuktobania | 1991 | Allocation | Civil receiving discretion / command reservations | None |
| Yuktobania | 1991 | Industrial orders | Civil workshop duties / protected replacements | None |
| Yuktobania | 1991 | Logistics | Civil route windows / staff-directed support | None |
| Yuktobania | 1991 | Training | Professional instruction / protected command lessons | None |
| Yuktobania | 2006 | Distribution review | Civil inspection / corrective command priority | Allocation settlement |
| Yuktobania | 2006 | Maritime support | Civil port windows / bounded fleet maintenance | Logistics settlement |
| Yuktobania | 2006 | Technical cooperation | Public scientific methods / protected examination | Industrial-orders settlement |
| Yuktobania | 2006 | Orders review | Ministerial verification / limited command return | Training settlement |

Osea has three finite commitment units. A civil period reserves one and a
protected period two. Separate civil and readiness support lanes authorize actual
services at 30, reduce their political price at 65, and sustain earned national
mandates. Policy choices, completed work, interruption and narrative choices change
those lanes. A paid hearing can repair support only toward the ordinary baseline
of 50. It cannot buy a high-support mandate or another commitment unit.

Yuktobania has civil and command allocation shares summing to 100. Each period
reserves 25 from its lane and one of two offices. Shares stay within 20–80; policy,
narrative and paid reassignment changes protect active reservations. The existing
army-reform conclusion reduces the reassignment price. Neither lane manufactures
cash, staff, factories, equipment or readiness telemetry.

All 72 non-service spirits have a distinct favorable and unfavorable modifier.
Standing settlements improve their selected policy benefit by 20% while keeping
the same continuing cost. The 64 ordinary/domestic service variants are temporary,
paid periods. Wartime domestic continuity uses 65% of the ordinary modifiers,
rounded to three decimal places; it describes records, training liaison and
maintenance administration. It asserts no flight or foreign delivery.

Future national/conflict content may read the following surface after checking
`ac_snp_active = yes`. These remain owned state; consumers must not write their
values or independently release reservations.

| Read surface | Meaning |
|---|---|
| `ac_snp_ose_public`, `ac_snp_ose_security` | Osean support lanes, 0–100 |
| `ac_snp_ose_used` | Reconstructed active federal commitment units, at most three |
| `ac_snp_yuk_civil`, `ac_snp_yuk_command` | Complementary allocation shares, total 100 |
| `ac_snp_yuk_civil_used`, `ac_snp_yuk_command_used` | Active reserved shares in 25-point units |
| `ac_snp_yuk_offices` | Reconstructed active receiving offices, at most two |
| `ac_snp_completed` | Number of genuinely completed funded periods |
| `<TAG>_snp_<branch>_service_completed` | At least one qualifying service in that branch |
| `<TAG>_snp_<branch>_reply_civil` / `_reply_protected` | Persistent branch-response choice |
| `<TAG>_snp_<branch>_last_domestic` | Latest qualifying branch completion used wartime domestic continuity |

The owner maintains these through `ac_snp_reconcile` and the guarded service
lifecycle. Its verified interruption hooks remain authoritative. Future consumers
can use the recorded choices without redefining an existing war or project result.

## Payment, capacity and lifecycle contracts

Every service costs 35 political power, or 30 under its earned Osean support lane,
and four institutional-capacity points. Public `ac_econ_can_pay_programme` and
`ac_econ_pay_programme` apply the existing fee only when the corresponding fiscal
owner is ready: 0.002 billion abstract units in full mode or two provisional units
in experimental legacy mode. Disabled fiscal play still pays PP and capacity.
The capacity delta goes through `ac_pol_change_capacity`. No private fiscal
balance is written and no fee is charged again as an annual commitment.

The current/original host, controlled owned land, focus unlock, reservation room,
support/allocation, political price, capacity and applicable affordability are
revalidated before payment or rewards. A private payment receipt is cleared before
each attempt. An ordinary period interrupted by war is cancelled; the same scope
can then be explicitly funded as reduced domestic continuity. Existing domestic
work survives additional war declarations. Completion releases its reservation,
records one branch credit and begins its own 90-day cooldown. Cancellation,
annexation, immediate capitulation, subject annexation or loss of all controlled
owned territory gives no refund or completion credit.

Each technical callback checks the specific host and active service, stored start
and due dates, exact current due date and at least 90 actually elapsed days. An old
callback cannot release or finish newer work. A weekly recovery path handles
current work whose valid callback was not delivered. The latest interrupted
period keeps a separate delivered-days snapshot when a new attempt starts.
Known interruption hooks act immediately; unobserved transient control changes
between weekly observations remain a native coverage limitation.

Initialization sets only missing register bookkeeping once. It grants no historical
preparation, cash, research, divisions, equipment, factories or leaders. Existing
save content stays intact. Late saves may choose present domestic work and finish
earned conclusions; they receive no expired summit opening. Civil-war copies with
the wrong current/original identity cannot authorize receipts or rewards, and all
new spirits forbid civil-war inheritance.

## Narrative and artwork

There are 36 substantive scenes: two openings, sixteen branch choices, sixteen
assessments and two national conclusions. Choices persist, affect the systems
that actually authorize work, and appear in later callbacks. Unanswered replies
have a 60-day window and an explicit later perspective. They cannot block the
funded tree. Assessments read selected policy, prior reply or unanswered record,
latest ordinary/domestic completion and relevant inherited context. The 32 hidden
service timers are not additional narrative scenes.

The original package contains 320 DDS textures, 114 editable PNG masters and 416
sprite bindings: 96 distinct focus compositions, 136 spirits, 68 decision rows at
26×29, two 100×100 categories and eighteen 640×260 briefing illustrations. The
shared original glyph library supplies subjects; navy/cyan framing and restrained
gold settlement details tie the packet together. No engine/DLC/remote pixels,
leader portraits, official emblems or baked localization text were imported.
`assets.json` records dimensions, frame counts, alpha bounds, SHA-256 hashes,
source dependencies and every binding. `audit_profile.json` pins exactly these 320
authored resources with no family wildcard exceptions. Pillow 11.3.0 is required
for byte reproduction. Four contact sheets and an all-assets HTML gallery are
retained; both foundation and continuation sheets and a representative technical
briefing image were inspected offline.

## Validation and limits

The actual-source runtime suite executes generated AST with both real P1 owners
across full, experimental and disabled fiscal modes. Its adapter supplies engine
observations, dates, focus-completion observations, event queues and timed-idea
expiry. It does not substitute payment, capacity, reservation or narrative rules.
Coverage includes all 32 services and both policy paths through the 96 definitions,
cost failure, repeat calls, cooldowns, lane/reservation bounds, war continuity,
immediate interruptions, stale timers, wrong identities, late initialization,
after-2020 conclusions, narrative windows and copied-state reloads.

The separate source/art gate verifies exact counts/imports, all three inherited
tree alternatives, foreign AST preservation, both generator orders, prerequisites,
exclusions, dates, English, shipped font glyphs, effect-tooltip boundaries, every
unprefixed decision-row binding, DDS/frame/alpha contracts, distinct compositions
and continuous-panel/resolved-node geometry. Primary modifier, hook, cost and
presentation-form metadata is rechecked read-only against installed HOI4 1.19.4.1.

The broader capture initially recorded 47 passing commands and one failing
inherited blanket startup-order assertion. That initial record is retained. The
separate chronology follow-up replaces that assertion with actual selected DLC/AI
startup consumers, including conditional OOB effects; its 16 regressions include
real AMB mutations. Exact World checkpoint `79993ca` passes 1,120 selected cases.
The final candidate merges the later world/legacy owners and passes those same
1,120 selected cases plus the stronger whole-mod compatibility gate. The initial
47-pass/one-failure capture remains a historical record; the full integrated
57-command pass and current follow-ups supersede it. No historical setup is
silently exempted to obtain a green result.

Current focused coverage is 14 actual-owner runtime tests, 14 source/art tests and
16 startup-chronology regressions. The added AI regression starts a support lane
at zero, executes the paid hearings through their actual effects and cooldowns,
restores service eligibility at 32, and confirms the authored AI weight then stops.
It also verifies political-power and capacity failures. Natural AI behavior is
still a separate native gate.

The final parent also contains the bounded decision-row repair. Its review
renderer was regenerated against this payload without recapturing original art
or before-state hashes: 623 conservative row variants, 73 previous source-bound
failures, zero current failures. The increase from its standalone inventory is
exactly 68 superpower rows plus six replacement-note rows. Garrison localization,
all actual conditional alternatives/defaults, first-frame dimensions and the
three inherited row templates pass. The inherited garrison `SPR_*` flags, map-only
behavior and legacy variable syntax remain separate gameplay gaps, not UI repair
acceptance. News retirement preserves the authored superpower scenes; the final
seven-case retired-news source suite and malformed-presentation fixtures pass.
Reference-only checks and their skipped cases remain visible in the recorded
suite outputs; skipped checks are not counted as executed native coverage. The
separate primary-contract report verifies the new modifier, hook, cost and
presentation-form facts against the installed reference read-only.

Packet-owned effective dependencies resolve all 338 runtime consumers to the 320
original textures. Requested decision/macro ownership gates pass. The full
completed-presentation graph remains a failing inherited backlog: 20,426 failing
presentation-gate entries in this explicit base-only scenario. The capture also
records 18 engine-only reader parse failures. These are not distinct-image counts
or proof of engine defects. There
are no authored parse failures in that capture. Installed profiles and archive
inventory do not imply enabled DLC. `effective-dependencies.json` retains the
exact scope and counts separately from the successful packet/selected-screen gates.

Native HOI4 arithmetic and performance, actual save/reload, AI selection and pacing,
balance, DLC-enabled gameplay, focus/detail scrolling and all three requested
viewport/input configurations remain pending: 3440×1440 at scale 1.0,
1920×1080 at 1.0, and 2560×1440 at 1.25. Native/desktop testing is paused.
Source checks, Python Decimal execution, geometry and galleries establish only
their stated offline properties. Final evidence lives in
`docs/evidence/superpowers/`; reproduction commands are in
`tools/superpowers/README.md`.
