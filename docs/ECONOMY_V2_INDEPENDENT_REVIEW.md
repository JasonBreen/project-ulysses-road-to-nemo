# Independent source review of economy v2

Read-only review on 31 October 2026 covered the generated fiscal owner, generator,
legacy dispatchers, identity/readiness triggers, on-actions, dynamic modifiers,
five-page GUI source, actual-script interpreter and regression cases. No foreign
worktree file, desktop, game, installed payload or user save was changed.

Two substantive findings were sent to the economy owner and corrected there:

1. **Stale transaction success after readiness loss.** The public spend method
   originally cleared `ac_macro_transaction_succeeded` only inside its readiness
   guard. A successful payment followed by a disabled or landless retry retained
   a true result from the preceding call. The result now clears before guarded
   financial mutation. The owner added success → disabled/unowned → retry cases;
   monetary stocks remain unchanged when the model is unavailable.
2. **A released country's first settlement depended on startup/reload.** A
   February 28 release initialized during startup recorded that date and settled
   on March 1. The same release first discovered by March 1's monthly callback
   initialized its last-settlement date to March 1 and skipped that settlement.
   Executing the actual scripts reproduced one versus zero settlements, including
   different cash. Initialization now records an unsettled period, the original
   January 1991 opening is explicitly excluded, and March discovery and prior
   startup have identical results. Startup still does not settle.

The corrected owner is
`common/scripted_effects/ac_macro_effects.txt` (`ac_macro_try_spend`,
`ac_macro_initialize`, `ac_macro_settle_month`); scheduling remains in
`common/on_actions/ac_macro_on_actions.txt`. Source and committed output were
updated together by their owner.

The independent rerun passed these four actual-script regressions:

```text
Macro.test_release_first_calendar_settlement_is_independent_of_startup
Macro.test_shared_programme_payment_and_policy_transactions_recheck_cash
Macro.test_disabled_and_old_save_full_mode_have_no_fiscal_writes
Macro.test_refresh_startup_and_reload_never_reseed_cash_or_settle
```

The narrow commitment API correctly applies a signed annual amount and refreshes
quotes without settlement. The consumer must own exact once-only application,
reversal and account identity. The reciprocal review found and fixed two consumer
issues in the institutional package: rejected pending reviews could strand a
flag, and a cloned clean commitment receipt could belong to the original fiscal
account. Both now have actual-script regressions; see `INSTITUTIONS.md`.

No further confirmed source defect was found in the reviewed scope. Important
limits remain explicit rather than being promoted to acceptance:

- The interpreter executes shipped formulas but uses unrestricted Decimal
  arithmetic and ordinal dates. It does not prove native numeric range,
  fractional rounding, remainder handling or save serialization. Small amounts
  and per-state growth require the planned native precision probe. For example,
  GDP-scaled political commitments can be much smaller than one thousandth of
  a billion; their effective engine resolution remains unverified.
- The 30-year all-country regression uses synthetic observations, mostly peace
  with no authored force observations. The separate upkeep case verifies force
  inputs and the war multiplier, but it does not establish that natural OOBs,
  wartime production, territorial loss and AI budget recovery balance together.
  Representative sustained-war/occupation fixtures would strengthen offline
  coverage; natural gameplay and balance remain native acceptance gates.
- Source visibility and click eligibility are checked for direct page controls.
  The reviewed geometry fits the stated window. Actual text rendering, native
  observation values, interaction and the three display configurations remain
  pending; offline rectangle checks are not screenshots.

The installed 1.19 reference's generated dynamic-variable documentation lists
the force and production observation names used by the new owner. Installed
on-action examples also confirm the country scope of monthly callbacks. This
is read-only syntax/reference evidence, not proof that every observation has the
intended runtime semantics in the candidate.
