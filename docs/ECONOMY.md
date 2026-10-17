# Experimental fiscal economy

This branch adds an opt-in weekly budget and a small domestic procurement contract to the preserved Ulysses campaign. It does not replace original country, focus, event, map, equipment or technology files. The implementation is statically and offline tested; the HOI4 1.19 parser, UI, native arithmetic, save/load and balance are not runtime accepted.

## Baseline and integration order

- Economy branch: `codex/strangereal-economic-core`.
- Exact base: `c72422d96f6bd9b33e61f725c2cdc8fe198a51d8`, the design/static-validation branch, descended from archive baseline `c452cf3fd3581054c0befd93eb7f32357821423c`.
- The concurrently active `codex/1.19-no-vanilla-assets` branch was observed at `437ed12794c5f496bc5594077bdf553479dac07c` during inspection. That is a recorded observation, not a frozen integration target or an endorsement of its current parity.
- Integrate the reviewed compatibility/asset repair and its original-content parity restorations before attempting economy runtime acceptance. The economy base still has inherited 1.13 descriptors and inherited asset problems. This branch is not a standalone no-vanilla-assets or 1.19 completion claim.
- After the repair branch is stable, apply this additive slice onto it and reconcile DESIGN/ROADMAP/README edits manually. Retain both validation workflows and run the repaired port's no-vanilla-assets validator. Do not restore a whole old descriptor or technology file from this branch.
- The tracking PR targets `codex/static-map-validation` to keep the economy delta reviewable. Ready-for-review status does not imply runtime acceptance. Nothing authorizes merging it or pushing main.

The current compatibility tracking dependency is [PR #2](https://github.com/JasonBreen/project-ulysses-continuation/pull/2); its branch had advanced to `abc0e169fb21783c4f42a752f9fce933a509150c` at the publication preflight. That moving head was not merged into or tested as part of this economy slice. [PR #1](https://github.com/JasonBreen/project-ulysses-continuation/pull/1) tracks the static/design baseline. Roadmap issue creation remains with the separate port/roadmap task.

No active checkout was edited. The MD checkout is read-only source reference. No files from the game installation were imported, and no game, save, playset or settings were opened or changed.

## Dependency map

| Layer | Inputs and consumers | Integration boundary |
| --- | --- | --- |
| Feature gate | New `ac_economy` game rule, disabled by default; owned-state check | No fiscal writes or policy modifier when disabled |
| Initialization | Startup enumerates existing countries; weekly country pulse lazily initializes later releases | `ac_econ_initialized` prevents reseeding; no global country loop in the weekly pulse |
| Capacity | Engine `num_of_controlled_factories`, excluding trade/relationship factory transfers | Uses existing industrial geography; no state ownership, population or GDP seeds |
| Budget quote | Tax and civilian policy levels, war status, outstanding principal | Recomputes estimates; never accrues money or advances an order |
| Settlement | Revenue, operating spending, debt interest, credit ceiling, unpaid bills | Weekly country scope; one native callback is one settlement |
| Policy | New decisions and one dynamic modifier | Additive stability/construction effects; existing economic ideas remain active |
| Debt | Cash, principal, current credit room | Borrow/repay hooks recheck guards; debt survives a falling ceiling |
| Procurement | Existing `infantry_weapons` unlock of `infantry_equipment_0`, military factory, no capitulation | One domestic contract; no MD equipment tags, exports, aircraft variants or new technology |
| UI/testing | English category description and manual refresh, Python stdlib harness, independent CI | Existing top bar and other GUIs are untouched |

The startup and weekly hooks live in a new on-actions file so they do not replace the inherited campaign callbacks. The country effects and triggers use the `ac_econ_` namespace; category/rule identifiers use `ac_economy`.

## Gameplay calibration, not canon

The campaign target is the existing 1991 start through the end of 2065. That horizon is a user-requested simulation span, not a claim that future Project Aces events are known. This slice invents no currency, GDP, tax history, company, border, conflict date, aircraft designation or technology. Every number below is an explicitly provisional gameplay parameter. Existing archive names identify integration dependencies only; their presence is not independent verification of canon.

One fiscal unit (FU) is an abstract accounting unit, not a named Strangereal currency or a real-world billion. Capacity is `min(1000, 5 + num_of_controlled_factories)`. The floor permits a small state to use the prototype; the cap bounds this provisional model through 2065. It is not an assertion about national wealth. Occupation and wartime industry changes influence the engine's controlled-factory count. The factory proxy is not a GDP model and does not separately estimate damage, population, trade, resources, unemployment or productivity.

| Parameter | Provisional implementation |
| --- | --- |
| Initial treasury | Two capacity units; seeded once per country |
| Tax revenue | 15%, 20% (initial), or 25% of capacity each week |
| Civilian services | 12% (initial) or 16% of capacity each week |
| Military operating spending | 4% at peace, 10% at war; an aggregate burden, not a unit-by-unit invoice |
| Interest | 0.1% of principal each week, nominal 5.2% over 52 weeks; no interest on unpaid bills |
| Debt ceiling | 26 weeks of current revenue; maximum 6,500 FU at capacity cap and high tax |
| Voluntary loan | 5 FU of cash for 5 FU of principal; no fee or foreign lender |
| Repayment | Minimum of 5 FU, current principal and available cash |
| Low/high tax effect | +2 / -3 percentage points of stability |
| Additional services effect | +5% construction speed at 16% civilian spending |
| Unpaid bills effect | -5 percentage points of stability and -5% construction speed |
| Policy cooldown | Shared 30-day timer within taxes and within services |
| Infantry contract | 5 FU prepaid, 100 existing basic infantry equipment, four productive weekly pulses |

Operating military spending is separate from contract payments. Native factory production continues: this is a supplemental procurement prototype, not a replacement for the production queue. No bankruptcy, forced territorial changes, automatic sanctions or canon-specific crisis event is attached to arrears.

## Accounting and transaction contract

Weekly settlement computes `net = revenue - civilian spending - military spending - interest`. It snapshots that week, then applies net cash flow. A cash shortfall borrows only the lesser of the shortfall and remaining credit. Any unfunded remainder becomes unpaid bills, and treasury returns to zero. Positive cash pays old unpaid bills before voluntary repayment. AI countries repay up to 5 FU only if cash covers two weeks of operating spending plus 5 FU. AI policy/procurement decisions have zero weights pending balance work.

Cash, principal, unpaid bills and escrow remain separate. The accounting invariant, excluding equipment delivery, is:

`change(treasury + escrow - debt - unpaid bills) = weekly net`

Loans and repayments conserve that financial position. Shrinking credit does not forgive existing principal. A lower capacity cannot cause a divide by zero: this model has no GDP ratio division. Interest is paid as a weekly bill, not silently capitalized into unbounded principal. Arrears grow linearly at the capped operating burden; they do not compound.

A contract moves 5 FU from treasury into escrow immediately. Another click cannot create a second order. Four productive weekly settlements consume escrow and grant exactly 100 `infantry_equipment_0` once. The first pulse may be less than seven days after the order, so four pulses normally span about 21–28 days. Lack of the technology, a military factory or non-capitulated status pauses progress; the prepaid order remains cancelable. Cancellation refunds remaining escrow once; delivered goods cannot be refunded. Arrears block new loans, voluntary debt repayment and new procurement; a prepaid contract can still complete. A cancellation refund becomes available to pay bills at the next settlement.

Public country-scope hooks are `ac_econ_refresh_budget`, `ac_econ_borrow`, `ac_econ_repay`, `ac_econ_order_infantry`, and `ac_econ_cancel_procurement`. Every transaction checks readiness and its own preconditions, including direct scripted calls. Future campaign consumers should call these effects rather than write fiscal balances. `ac_econ_weekly_settlement` and `ac_econ_progress_procurement` are scheduler internals; do not invoke them from focuses, events or UI. The engine schedules the weekly callback; there is no second event timer or daily financial tick.

Current estimates and the last settled week have separate variables. Refreshing the estimate after a war/industry/policy change cannot collect revenue, alter the old snapshot or advance delivery. The UI can briefly show a stale estimate until refresh or the next weekly settlement; the loan effect recalculates credit before granting cash.

## Validation and acceptance

Captured local results and long-run maxima are in [ECONOMY_VALIDATION.md](ECONOMY_VALIDATION.md).

A later detached assessment against port head `92173286b8315e22b3949a98ad6b559225fd0a15`, including the README insertion-conflict fix and the differing asset-audit baseline results, is recorded in [ECONOMY_INTEGRATION.md](ECONOMY_INTEGRATION.md). Issue [#7](https://github.com/JasonBreen/project-ulysses-continuation/issues/7) now tracks this integration; native acceptance remains separate.

Run `tools/Test-UlyssesEconomy.ps1` with an installed Python 3.9+ executable, or `python -m unittest discover -s tools -p test_economy.py -v`. See [IDE_WORKSPACE.md](IDE_WORKSPACE.md) for manual IDE tasks.

The stdlib harness reads the actual authored scripts, retains repeated keys and rejects unknown script commands. It is an intentionally limited interpreter, not Paradox's parser. It checks disabled no-op behavior, initialization, country pulse scope, quote purity, cash/debt conservation, partial credit, arrears priority, AI reserves, tax/service cooldowns, prerequisite failures, duplicate orders, partial repayment, cancellation and one-time delivery. Deliberately malformed braces, misspelled calls, undefined variables, missing English keys and a broken technology-to-equipment binding must fail.

The 2065 stress check runs 3,914 weekly pulses per scenario: maximal peaceful accumulation, continuous war with low taxes and expanded services, and war followed by complete industry loss. It uses an intentionally excessive factory input to exercise the capacity cap. Cash, principal and unpaid bills stay nonnegative and below 1,000,000 FU in these scenarios; principal stays at or below 6,500. A separate 600-week test reconciles each step through war, peace and industry changes. Decimal roundoff tolerance in the long-run invariant is 1e-18 FU. None of this verifies HOI4 fixed-point precision or native overflow limits.

Open runtime gates, coordinated with the port work:

1. Apply the frozen repaired port and parity restorations; pass its asset, map, reference and content checks.
2. On HOI4 1.19, verify both existing bookmarks load with the rule off and on. Inspect parser/error logs and category text; establish the native numeric range/precision.
3. Confirm one weekly settlement per country, after startup and after native save/load. Check a newly released country, civil-war split/reunification, annexation and exile. Preserve balances for the same country; do not assume native variable/flag inheritance or assign a canon debt settlement without evidence.
4. Exercise credit exhaustion, industry loss, peace/war changes, repayment to zero, funded-contract pause/cancel/delivery, and native save/load with a pending order. Verify no treasury or equipment duplication.
5. Run AI and production/balance tests on the repaired original campaign, then a controlled long run through end-2065. Review fixed-point rounding, performance, native production overlap and inherited economic-idea stacking.

No runtime gate is claimed complete. No technology file is modified here. Richer revenue bases, aircraft procurement, international lenders/exports, canon country calibration and future events remain proposed. Add factual country or company content only after primary Project Aces evidence is recorded in the coordinated canon ledger; unknown facts remain unknown.
