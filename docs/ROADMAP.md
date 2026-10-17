# Implementation roadmap

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

## Next implementation slices

1. Extend the reference audit to scripted effect/trigger calls and country-tag consumers; keep inherited vanilla namespaces explicitly allowlisted.
2. Decide the target HOI4 branch from the installed build evidence before changing `supported_version` or branch-specific syntax.
3. Resolve state 171 only after Sam supplies intended geography/ownership; do not invent a replacement.
4. Classify the 203 `XXX` strategic regions and rename only where lore-backed intent is established.
5. Trace the 1991 Belkan War event/focus graph beyond the new handoff contract and replace remaining demo-terminal transitions with explicit continuation contracts.
6. Run the approved isolated runtime smoke test once a safe non-destructive HOI4 launch method is verified.
