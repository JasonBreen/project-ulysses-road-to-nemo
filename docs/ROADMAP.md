# Implementation roadmap

The current user-approved program is [Strangereal overhaul: 1991–2020](STRANGEREAL_OVERHAUL.md),
with machine-readable budgets and honest package status. The implementation
records below remain historical evidence; they do not supersede that roadmap
or establish native acceptance for its pending packages.

## Flight cadence

Osea, Yuktobania, and Erusea can static-fire rockets from 1991, lose a flight, and lock in a cadence that raises one pad. The result is checked on 8 July 1999 and does not replace Stonehenge, Megalith, or Arkbird. Belka is unchanged. [Source layers, affected IDs, and acceptance status](CANON_LEDGER.md#flight-cadence-campaign) distinguish the official Ulysses date from the authored launch programs. Native play is still unverified.

## Anea — The Burden of Recovery

The Emmerian/Estovakian 1991–2005 foundation is authored on the merged PR#29
base, with108 focuses, national starting setups, bounded civil preparedness and
recovery, renewable aid services, actual-outcome sanctions and consultative
cooperation. [Contracts and provenance](ANEA_EXPANSION_LEDGER.md),
[offline/native acceptance](evidence/anea/ACCEPTANCE.md), and the
[original artwork gallery](evidence/anea/artwork-gallery.html) accompany it.
Native acceptance remains open and desktop interaction is stopped. The older
entries below retain their historical branch context and are not fresh counts
of the combined current repository.

## The Peace We Inherit — authored expansion

All four approved slices are present in source: Belka's outcome and policy
branches; Osea/Ustio; Sapin/Gebet and local responses; and the 1996–1999
preparedness/relief arc. [Content, provenance, coefficients and acceptance](PEACE_WE_INHERIT.md).
Static tests cover transitions and references; native parsing, rendering,
save/load, AI and balance remain open under issue #8. No game installation or
playset has been changed by this content work.

## Economic foundation and IDE workspace

Implemented in the isolated `codex/strangereal-economic-core` slice from exact base `c72422d96f6bd9b33e61f725c2cdc8fe198a51d8`:

- Default-off fiscal prototype: weekly revenue/spending, treasury, interest, bounded borrowing, repayment, unpaid bills, guarded policy decisions and one prepaid domestic infantry contract.
- Additive namespaced files; original country/focus/event/technology/map content is preserved. Calibration is explicitly non-canonical, with no invented GDP, currency, companies, borders or future Project Aces history.
- Dependency/provenance/acceptance contracts in [ECONOMY.md](ECONOMY.md) and [ECONOMY_PROVENANCE.md](ECONOMY_PROVENANCE.md), plus actual-script offline regression and deliberate-error tests.
- Full-horizon offline stress tests through end-2065 (3,914 weekly pulses per scenario); bounded capacity/credit and non-compounding unpaid bills. Native fixed-point behavior is still untested.
- Portable [VS Code workspace](../Project-Ulysses.code-workspace), manual validation tasks, and [opening instructions](IDE_WORKSPACE.md). Antigravity compatibility is unverified.

Integration order: freeze/review the separate 1.19 port, asset cleanup and original-content parity restoration; apply this additive slice; reconcile shared docs; run both static workflows and the port's no-vanilla-assets checks; then perform coordinated native parser/UI/save/load/AI tests. Do not replace original technology or descriptor files with this branch's inherited base. The separate port/roadmap task owns technology names, end dates and roadmap issues; this slice does not duplicate those issues.

Next economy slices remain proposed: native 1.19 acceptance, AI and campaign balance, canon-evidence-backed country calibration, richer revenue bases, and aircraft/international procurement after equipment and technology dependencies are stable. Existing content remains the campaign foundation. No future canon is inferred from the requested 2065 horizon. A ready-for-review tracking PR is not merge authority or runtime acceptance.

## Completed in this session

- Created and verified the private GitHub repository.
- Removed the historical developer-local absolute path from the editable embedded descriptor; the immutable baseline is unchanged.
- Sanitized tracked evidence so the repository does not retain the original user's local Downloads path.
- Added a repeatable static map validator covering province definitions, state assignments, strategic-region coverage, adjacency endpoints, airport/rocket references, building and unit-stack coordinate bounds, railway/supply-node references, province RGB coverage, raster headers, and known placeholders.
- Added a static regression wrapper and private CI workflow; the checks do not launch HOI4.
- Replaced the preserved demo-end event's no-op option with an explicit `ac_continuation_active` global handoff flag and neutral continuation wording. Existing gameplay continuation remains unverified.
- Added a conservative static reference audit for focus/event IDs, country-history localization coverage, and event/focus localization keys.
- Repaired two demonstrated stale references to fully commented-out Ustio content and documented the Belkan War continuation trace.
- Added repository-grounded English labels/descriptions for the seven Belkan defeat-branch events; broader missing localization remains an explicit inventory item.
- Added the repository design contract in `docs/DESIGN.md` and linked it from the README.

## Continuation and agent tooling added in the postwar slice

- Added docs/LORE_EVENT_COVERAGE_BACKLOG.md with source layers, nation/character/organization/conflict coverage, and explicit 2065/Joker 1 gaps.
- Added root AGENTS.md and project-local skills under .agents/skills/ for canon research, HOI4 scripting, map/assets, localization, validation/integration, campaign path audit and validation, native compatibility, and Ustio continuity.
- Added a Ustio-specific continuity agent and skill, plus a dependency-free Ustio regression check wired into the campaign wrapper; this is the repo-local MD-OEM-style tooling requested for the continuation.
- Connected world_event.2 to branch-aware postwar handoff events for conventional victory, Wacht am Wal, and defeat.
- Reconnected the inherited Ustio opening focus nodes, repaired a malformed focus coordinate, and added a guarded postwar event that reloads the existing Ustio branch based on its pre-existing Ratio outcome flags. No new Ustio border or core was authored.
- Added provisional reconstruction, demobilization, political-settlement, and affected-country settlement decisions. These are gameplay branches, not official canon claims.
- Restored twelve pre-existing exact vanilla-file matches from the immutable Ulysses baseline; the no-vanilla audit now reports one allowed inherited map/positions.txt match and zero new matches.

## Belkan campaign arc slice

On the isolated campaign branch, the static campaign contract now covers:

- a six-focus prewar preparation path attached to Belka's existing focus tree;
- a War Council decision that calls the existing Belkan War start event;
- three war-stage decisions with guarded economy hooks and AI weekly fallbacks;
- branch-aware postwar focus progression for reconstruction, demobilization,
  victory/defeat settlements, and legacy outcomes;
- complete English localization, a native playtest checklist, and a static path
  report that distinguishes references from engine reachability.

The MD-OEM audit pattern was ported selectively as dependency-free repository
tooling: `tools/validate_campaign.py`,
`tools/analysis/campaign_path_report.py`, and
`tools/Run-UlyssesCampaignChecks.ps1`. Repo-local agent profiles and skills now
live under `.agents/agents/` and `.agents/skills/`. MD-OEM gameplay or executable
code was not copied. The campaign branch has not been native-playtested in this
task.

## Next implementation slices

1. Extend the reference audit to scripted effect/trigger calls and country-tag consumers; keep inherited vanilla namespaces explicitly allowlisted.
2. Decide the target HOI4 branch from the installed build evidence before changing `supported_version` or branch-specific syntax.
3. Resolve state 171 only after the user supplies intended geography/ownership; do not invent a replacement.
4. Classify the 203 `XXX` strategic regions and rename only where lore-backed intent is established.
5. Trace the 1991 Belkan War event/focus graph beyond the new handoff contract and replace remaining demo-terminal transitions with explicit continuation contracts.
6. Resolve state 171 and the 203 XXX strategic regions only after source-backed geography decisions.
7. Run the approved isolated runtime smoke test once a safe non-destructive HOI4 launch method is verified.
