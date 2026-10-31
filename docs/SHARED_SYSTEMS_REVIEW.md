# Package 1 shared-system integration review

This Package 1 candidate adds the full economy and institutional framework on
the separately reviewable World Foundation prerequisite, PR #33. That prerequisite
includes the repair/privacy package, PR #32; both descend from verified main `3810d1a`.
The economy/institutions components retain their individual commits and their
generated output. This PR adds no partner campaign or squadron story payload.
The evidence is source/offline only; native acceptance remains paused.

## Confirmed defects and corrections

1. **Temporary countries escaped institutional scheduling.** The profile and
   fiscal-receipt owners support `original_tag` identities, but literal
   `on_weekly_TAG` hooks excluded a current `D01` tag. The previous clone test
   changed its engine identity while retaining the original current tag. The
   scheduler now uses the installed engine's country-scoped generic weekly
   callback, guarded by the original-tag profile. The new dispatch test uses
   `D01` with original SNS identity and executes that callback: capacity is
   charged once, a stale review is repaired, and the real new fiscal account
   reserves its own commitment without altering the original account.
2. **Crisis timing did not match the accepted contract.** Warning formerly
   began after failure1 and crisis after failure3. It now begins after two
   failed settlements and allows three subsequent correction settlements.
   `ac_macro_warning_months_left` records3→2→1→0; repeated callbacks and quotes
   cannot advance it. Recovery needs three funded settlements with arrears
   declining or already zero. Unchanged outstanding arrears reset the recovery
   count. Leaving the active crisis preserves remaining arrears and debt.
3. **A leaderless generator seam oscillated around foreign setup.** DEL has
   an established recruited leader and no generated-leader section. The economy
   marker generator appended after `WORLD FOUNDATION`, while that owner restored
   the marker before its section. The economy author now prefers the existing
   world-foundation anchor when no generated-leader anchor exists. A no-leader
   fixture checks ordering, once-only eligibility and stable regeneration.

The shared owner/API names remain unchanged. Institutional capacity is written
by its owner. Financial stocks, commitments, quotes and monthly settlement are
written by the fiscal owner. The legacy experimental account remains in its
original units and retains its original prepaid-contract behavior. New-campaign
eligibility remains a history marker; old saves do not receive starting money,
debt or historical catch-up.

## Combined actual-owner evidence

`tools/Test-SharedSystems.py` runs both generated owner libraries in one
interpreter. It provides political observations/effects missing from the fiscal
interpreter; it does **not** substitute fiscal readiness, commitment arithmetic,
quote recomputation, financial stocks or monthly settlement. Its four cases
cover:

- a real institutional reservation changes the actual monthly quote and settled
  bill, while repeated synchronization/quotes never settle money;
- disabled, experimental and unmarked old-save accounts retain fiscal stocks;
- an actual current-tag clone reserves against its new account and leaves the
  original receipt/account untouched;
- losing all owned territory defers exact reversal until the fiscal owner becomes
  ready again, then reverses that original snapshot once.

The narrower institution suite retains its explicitly labeled API fixture for
standalone component testing; that fixture is under `tools/`, never under the
delivered mod. In this integrated candidate it loads the real narrow owner.
The combined suite above additionally executes the complete real quote path.

Final source checks use Python 3.12, Pillow 11.3.0 and numpy 2.2.6:

| Check | Result |
|---|---|
| Macro source suite | 27 passed, including exact warning/correction/recovery boundaries and duplicate-callback protection. |
| Settled-ledger source suite | 14 passed, including monetary carry, history and five-page geometry. |
| Observable force-upkeep suite | 8 passed, including installed primary contract hashes. |
| Institutions source suite | 20 passed, including real cloned-tag weekly dispatch. |
| Shared real-owner suite | 4 passed. |
| Retained experimental economy suite | 27 passed. |
| Factions with installed reference | 35 passed, no skips. |
| Full `Test-UlyssesStatic.ps1` with installed 1.19.4.1 read-only reference | Passed. Map errors 0; one placeholder-owned state and 204 placeholder strategic regions retained. Reference warnings 2006 and technology warnings 1 remain; no warning-free claim. |
| Authored asset audit `--strict-all` | Passed; zero unresolved texture references and cleaned-family regressions. |
| Anea foundation and starting-government generators `--check` | Passed with the new history eligibility markers. |
| Marker regression after PR33 seam correction | Passed. |

## Separate PR33 composition audit

A disposable detached worktree combined the integration base with world
foundation `39364e6`. DEL's two appended sections produced a normal text merge
conflict; both the economy eligibility block and world setup block were
preserved. The corrected economy marker builder and world generator then
established their common canonical ordering.

Both authoring orders passed generation plus `--check`:

1. Anea → world foundation → starting governments → economy.
2. Economy → starting governments → world foundation → Anea.

All 69 country histories and both logistics files had identical byte hashes
after the two orders. The final review candidate also integrates the newer
World/repair prerequisite `2afd9fa`. Both DEL sections are retained, the owners are
regenerated in their canonical order, and the registry is refreshed against the
combined payload. The registry now joins all 69 actual fiscal and institutional
profiles, leader representation, capital source layer, active/emergent/placeholder
classification and explicit public regional participant declarations. Its source
profile hashes normalize line endings for Windows/Linux reproducibility. The
registry continues to expose incomplete physical country foundations rather than
claiming global native playability.

## Settled ledger and monetary carry follow-up

The following source changes complete the previously recorded page/ledger gap.
The five pages now present Overview, Budget, Industry and readiness, Debt and
contracts, and a twelve-record settled Ledger in an 860×700 window. Ledger
snapshots retain the period's billed bases and actual paid/unpaid flows; the
opening forecast never becomes a historical observation. Only authorized
settlement writes or shifts records. All 33 graph frames are distinct, including
the first nonzero level. Font tests read shipped bitmap advances and actual ink
bounds, including the 19-pixel table rows.

Monthly receipts and bills use a 0.001-billion payment quantum with separate
fractional milli-unit carries. Forecasts remain estimates; settlement floors
whole quanta and retains the remainder. The conservation identity includes
uncollected revenue and unbilled obligation carries. A sub-quantum public spend
is rejected after clearing any stale success result. This approved gameplay
accounting rule cannot recover arithmetic already lost by native precision.

`tools/Test-EconomyLedger.py` adds 14 actual-source/geometry cases: authorized
history recording, twelve-entry order, no fabricated opening, pure UI/quotes,
offline reload copies, clone and release identity, underfunding and arrears
payment, tiny recurring commitments, the largest-profile synthetic 2020 path,
conditional pages, actual glyph ink, and signed graph-frame pixels. The shared
owner test now includes the carried institutional fraction in its comparison,
instead of requiring a sub-quantum bill to be paid prematurely.

## Verified-observable upkeep and period allocation

The operating allowance now reads six land-equipment groups, nine current armor
families and six aircraft role groups through primary documented observations.
`force_observables.json` retains the installed contract file paths and hashes.
Legacy alias names are not charged alongside their current archetypes. Armor
uses a conservative family maximum and aircraft use one total base plus one
maximum role-premium pool, because designer modules can add overlapping role
types. Mixed families/fleets can be underestimated; no per-tail telemetry or
native observation result is asserted. Eight source cases cover all captured
signals, no alias double charge, role differences, the defense floor, physical
stock preservation and installed-contract provenance.

State growth/repair is boundary-bound. More importantly, each authorized period
freezes a state's real output and taxable base to its first settling controller
and date. Later same-boundary ownership or occupation changes cannot settle the
same bases again. Current-controller forecasts remain pure and up to date. The
regression compares summed actual settled GDP, taxable base and accrued receipts
across both transfer cases; next-month allocation and productive growth resume
normally. This is a whole-period gameplay rule, with native country-ID/save
stability, execution order and performance still requiring engine acceptance.

## Final follow-up source checks

The final ledger/upkeep/state-receipt candidate passed 27 macro, 14 ledger,
8 force-upkeep, 20 institution, 4 real-owner integration, 27 retained economy,
35 faction and 8 interface tests. Force/faction provenance checks used the
installed engine only as a read-only script reference. Macro and Anea generated
outputs plus the authored asset audit `--strict-all` passed. A fresh full
`Test-UlyssesStatic.ps1` with the installed read-only reference also passed
after the state-receipt changes: map errors 0, retained placeholder warnings 2,
reference warnings 2006 and technology warnings 1. The retained `results.json`
records each executed command and its source-only coverage.
The retained run tests source commit `8a96ff014412d4ca713ddad99168aa16b48d5485`.
The subsequent review commit adds evidence and the explicitly labeled offline
screen reconstruction; it does not change the delivered economy or institutions.

The selected-screen consumer dependency audit also passes for
`ac_macro_economy.gui` against the installed loose-file reference. This establishes
the inspected screen's resolved source dependencies, not the completed world
anti-vanilla gate. DLC archives and the global unresolved dependency backlog
remain separate acceptance work.

## Native limits

The interpreters use Decimal/ordinal-date models. They do not prove HOI4 fixed
point precision, dynamic-variable observations, native save inheritance,
serialization, GUI behavior, natural AI pace or economic balance. Native engine
checks, all three display configurations, real save/reload, sustained wartime
budgets, occupation/release and smallest/largest-payment probes remain pending.
No game, desktop, installation synchronization or user-save action was performed.
