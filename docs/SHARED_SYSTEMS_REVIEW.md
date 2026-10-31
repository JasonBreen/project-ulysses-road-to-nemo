# Package 1 shared-system integration review

This candidate integrates economy component `7dffa0f` and the reviewed
institutions components `b66fde0` / `e42a64e` on verified main `3810d1a`.
The integration branch contains no world-foundation, partner-campaign or squadron
story payload. This is source/offline evidence; native acceptance remains paused.

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

Local checks with Python3.12, Pillow11.3.0 and numpy2.2.6:

| Check | Result |
|---|---|
| Macro source suite | 27 passed, including exact warning/correction/recovery boundaries and duplicate-callback protection. |
| Institutions source suite | 19 passed, including real cloned-tag weekly dispatch. |
| Shared real-owner suite | 4 passed. |
| Retained experimental economy suite | 27 passed. |
| Factions with installed reference | 35 passed, no skips. |
| Full `Test-UlyssesStatic.ps1` with installed1.19.4.1 read-only reference | Passed. Map errors0; one placeholder-owned state and204 placeholder strategic regions retained. Reference warnings2007 and technology warnings1 remain; no warning-free claim. |
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

All69 country histories and both logistics files had identical byte hashes
after the two orders. These composition observations do not import world setup
into this PR. When PR33 is integrated, retain both DEL sections, regenerate with
the corrected marker owner, and refresh any derived world registry against the
combined payload.

## Required follow-up and native limits

The current five-page interface still differs from the accepted Overview,
Budget, Industry and readiness, Debt and contracts, and Ledger arrangement. The
rolling12-month settled ledger and history graphs are a separate required
follow-up; this integration does not claim that interface contract complete.

The interpreters use Decimal/ordinal-date models. They do not prove HOI4 fixed
point precision, dynamic-variable observations, native save inheritance,
serialization, GUI behavior, natural AI pace or economic balance. Native engine
checks, all three display configurations, real save/reload, sustained wartime
budgets, occupation/release and smallest/largest-payment probes remain pending.
No game, desktop, installation synchronization or user-save action was performed.
