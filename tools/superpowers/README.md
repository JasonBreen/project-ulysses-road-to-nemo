# Superpower national programmes: SP96

SP96 compiles **96 additional definitions**, forty-eight for Osea and forty-eight
for Yuktobania. They are the first slice of the approved 92/90 additions; a later
slice still owes 44/42. Definitions include mutually exclusive alternatives.
The delivered ledger remains unchanged until this packet's broad gates pass.

Sixteen individual branches connect a register, one of two enduring policies,
an operational protocol, an actual completed-service review and a standing
settlement. Four foundations per country open in 1991; four continuations open
in 2006 and require their matching earned foundation settlement. Ordinary work
takes 35 days; policy and settlement commitments take 70. All conclusions remain
eligible after 2020. Existing Osean alternative trees import the same 48 IDs, so
an inherited election handoff retains earned work. Yuktobania retains its existing
intervention, command-reform and Arkbird choices. This packet owns no war, peace,
leader, border, project, history setup, roster or physical-production grant.

All new institutions, domestic incidents, policy alternatives, indices and values
are original provisional gameplay. They are not canonical constitutional rules,
elections or GDP. The official context anchors in `sources.json` were checked
against the ACES Chronicle; the national procedures remain separately authored.
The next Circum-Pacific owner is a separate package and may read these earned
records; this slice declares no conflict or historical outcome.

## Osea: finite federal commitments

The national register has **three commitment units**. A civil service reserves
one; a protected readiness service reserves two. Several different periods may
run concurrently only within that finite schedule. Each scope has an independent
active receipt and cooldown; one scope cannot be purchased twice in parallel.
Totals are reconstructed from the actual active receipts whenever work starts,
finishes, is cancelled, or the weekly observer repairs the register.

Civil and readiness support begin at 50/100 as bookkeeping for the new register,
not as a historical poll. A civil policy adds 4 civil support and removes 2
readiness support; a protected policy does the reverse. A completed period adds 3
to its own lane and 1 to the other. An interrupted period removes 3 from its lane.
Values remain 0–100. Thirty support is required to authorize that lane's work.
At 65, its PP cost falls from 35 to 30 and it sustains an earned standing mandate
with a continuing political or civilian opportunity cost.

Paid receiving-office hearings restore up to 8 support toward the ordinary
baseline of 50, for 20 PP and 2 institutional capacity. Both hearing routes share a
30-day cooldown. They cannot purchase the earned 65-point mandate. They provide
a useful recovery route after repeated interruption without manufacturing money,
equipment or another commitment unit.

## Yuktobania: allocation and reservations

Civil and command allocation shares always total **100**. The civil share is
bounded 20–80, and the command share is its complement. Every service reserves 25
points from its lane and one of **two national receiving offices**. A reservation
cannot be counted by both lanes. The current shares therefore determine which
portfolio of actual work can be funded.

A policy or narrative choice moves up to 5 existing points toward its selected
priority. Existing active reservations are protected; a clipped movement is not
queued as an invisible future transfer. Explicit reassignment decisions move 10
points for 15 PP and 2 capacity, or 10 PP after the inherited army-reform assessment.
Both directions share a 30-day cooldown. The donating lane must retain at least 20
points and all its active reservations. A 60-point civil or command priority
sustains its corresponding national modifier with a continuing countervailing
cost. No share creates cash, stockpiles, GDP, factories or staff units.

The docket reads the existing intervention and command-reform records without
replacing them. Scientific context reads the established partnership and project
state; there is no new bilateral accord, project payment or project completion.
A useful domestic records route remains when cooperation is absent or interrupted.

## Funded periods and lifecycle

There are **32 named funded scopes**. Authorization costs 35 PP (30 for an earned
Osean lane), 4 institutional capacity and the existing P1 programme fee when its
fiscal owner is ready: 0.002 billion abstract fiscal units in full mode or 2 units
in experimental legacy mode. Disabled fiscal play retains the PP and capacity
costs. Both actual public owners implement payment/capacity; this owner writes
no private fiscal stock. An upfront programme fee is not also billed as a new
annual commitment.

Each scope delivers 90 days of temporary national support and then has its own
90-day cooldown. A hidden day 90 callback validates its specific current/original
host, active receipt, stored start/due dates and actual elapsed days. Its exact
due-date guard rejects an old or delayed callback rather than clearing newer
work. A weekly recovery path can finish genuinely elapsed current work if that
callback was not delivered. Repeated callbacks cannot pay, release or credit a
period twice.

War interrupts an ordinary period through the verified war hook, with weekly
revalidation as a fallback. The same scope can be funded during war as explicit
**domestic continuity**, using modifiers rounded from 65% of the ordinary values.
It does not claim a patrol, flight, foreign delivery or combat result. A wartime
period keeps that reduced mode if peace returns. Further war declarations do not
cancel already-domestic work merely because another participant enters a war.
Annexation, immediate capitulation, subject annexation, loss of all controlled
owned territory, or cancellation ends active work without refund or review credit.
The latest interrupted service and its delivered-day snapshot remain visible,
even after that scope is restarted. Unknown transient control changes before a
weekly observation are not claimed to have native coverage.

Current and original host identity are checked on every owned reward and receipt.
New spirits forbid civil-war inheritance. Subjects retain domestic work.
Initialization sets only missing register bookkeeping once; it grants no old
preparation reward, leader, technology, army, cash seed or factory. There are no
new historical summit invitations to replay in a late save. All national scenes
concern work the government is choosing now.

## Narrative and presentation

**36 original narrative events** provide two opening hearings, sixteen branch
responses, sixteen branch assessments and two national conclusions. Choices
persist and change the support/allocation systems that actually authorize work.
Assessments read those choices, the selected enduring policy, the latest ordinary
or wartime completion, and relevant inherited command/project context. Unanswered
invitations have explicit callbacks and never block the funded branch. Reply
windows last 60 days; sent/answered records, host revalidation and interruption
cleanup prevent stale or repeated benefits. The 32 recurring technical timers
are separate hidden events, not additional narrative chapters.

Player-facing effect tooltips explain commitments and show the appropriate
national-spirit modifiers. Hidden effect blocks keep private counters and public
payment plumbing out of those tooltips. Cost labels resolve to the actual compact
price and fit the existing 180 px row area. The existing focus/detail and decision
GUI control contracts remain intact; no new generic economic GUI is added.

The original art package contains **320 DDS textures**, **114 PNG masters** and
**416 sprite bindings**: 96 distinct focuses, 136 spirits, 68 native 26×29 row icons,
2 categories and 18 briefing illustrations. `assets.json` records hashes, dimensions,
frame counts, alpha, source dependencies, subjects and bindings. The four country
contact sheets and `gallery/index.html` are offline review material. Shared
framing and branch subjects are deliberate; every focus has a distinct three-part
composition. Restrained gold marks settlements; no watermark or baked runtime
localization text is added. No engine/DLC/remote pixels, portrait or flag is copied.

## Reproduce and validate

Use Python 3.12 with Pillow **11.3.0** for exact artwork bytes:

```powershell
python -B tools/superpowers/build.py
python -B tools/superpowers/build_art.py
python -B tools/superpowers/build.py --check
python -B tools/superpowers/build_art.py --check
python -B tools/superpowers/validate.py --report docs/evidence/superpowers/source-gates.json
```

The runtime suite executes generated AST with both actual P1 owners across full,
experimental and disabled modes. Its adapter supplies only engine observations,
dates, queues, focus completion and timed-idea expiry. The separate source/art
suite verifies exact imports, foreign AST preservation, both generator orders,
prerequisites/exclusions, costs, source reproduction, font glyphs, DDS/alpha/frame
closure, actual unprefixed row consumers and resolved panel/caption geometry.
Both suites have separate CI steps. The broader runner retains campaign, economy,
faction, aftermath, project, actor, Anea, briefing, typography and asset checks.

`verify_engine.py --reference <engine-root>` rechecks captured primary 1.19.4.1
contracts read-only. `capture_dependencies.py --reference <engine-root> --output
<report.json>` uses an explicit base-only scenario with exact hash-pinned original
SP96 textures. It reports packet-owned consumers separately from requested-screen
ownership and the full completed-presentation gate. **Full conversion remains a
failing inherited backlog**; packet-owned art closure is not global acceptance.

Development and result ledgers are under `docs/SUPERPOWER_PROGRAMMES_LEDGER.md`
and `docs/evidence/superpowers/`. Decimal execution, copied-state reloads and
source geometry are offline evidence. Native HOI4 arithmetic, actual save/load,
AI selection/pacing, balance and all requested viewport/input configurations
remain untested; native/desktop testing is paused.
