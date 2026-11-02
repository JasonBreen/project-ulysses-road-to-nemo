# Release-foundation review corrections

This narrow successor starts at reviewed source`00b8936714804657f73985e3e67268f9846a6a9e`.
It addresses review threads[r4434365194](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/47#discussion_r4434365194),
[r4434365212](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/47#discussion_r4434365212),
[r4434365225](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/47#discussion_r4434365225)
and[r4434372194](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/47#discussion_r4434372194).
Native testing is paused. No source/archive/baseline or intake/capture is repinned.

## Account preservation

The V2 generator inventories the actual initializer's persisted variables,
including expanded money/ledger fields and country receipt flags. Only UI page
selection and the new-campaign history-eligibility marker are excluded. Any
retained record sends a released country through adoption/review rather than
destructive fresh initialization. This includes zero-valued receipt fragments.

Incomplete accounts keep every existing variable and receipt flag. A review lock
blocks readiness; it cannot disappear on repeated initialization. Reattachment
requires matching identity/schema and all mandatory stocks, carries and settlement
receipts. A valid complete account can reattach without a cash/debt seed. The
ordinary69-country initialization and separate legacy units are unchanged.
Source regressions exercise every inventoried fragment, arrears-only/commitment-only/
escrow-only cases across all seven releases, missing required fields, repeated
callbacks, and genuine history-marker/UI-only fresh admission.

## Ordered source contract

`tools/release_foundations/event_contract.py` is independent of the authoring
transforms. It verifies and removes only the exact reviewed snapshot, once guards,
transfer wrapper and observation hooks, then compares the entire ordered AST with
the original captured script. Country scopes, options, event fields/order, command
values/order, triggers and other rewards remain significant. It rejects missing
guards as well as extra or moved commands. The original `event_inputs.json` and
624 protected state/history inputs retain their existing bytes.

Negative cases include REC's`load_oob` scope changed toGEB, runtime command order,
option ownership, extra political rewards, altered guard conditions, transfer-guard
removal, snapshot order, treaty state values and army transfer fractions.

## Honest production fallback

The former total-industry-minus-cumulative-purchase calculation could neither
observe current allocation nor reconcile deleted lines. Installed primary files
declare country-scope `num_of_available_military_factories` and
`num_of_available_naval_factories` at `dynamic_variables_documentation.md:596–602`
and `triggers_documentation.md:6721–6736`. Their descriptions only say “available”.
A read-only scan found no consumer under installed`common`/`events` that establishes
unallocated-versus-total semantics. This remains an explicit native acceptance gap.

The approved fallback retires automatic line purchases from visible play. Stable
IDs and historical receipts/counters survive as inert compatibility data. Direct
or stale completions change no money/PP, capacity, production, equipment, resources
or receipt. Existing Production lines are untouched. The genuine5 PP per-DLC
certification still unlocks valid technology/design recipes; actual allocation,
manufacturing and rotation belong to the Production screen and normal AI.
Materials/imports/fuel remain player obligations, not grants or guaranteed trade.

## Evidence boundary

The focused suites and broader gates execute generated source with explicit
native observations. They do not establish native free-capacity semantics,
production scheduling, DLC loads, save serialization or AI pacing. Final exact
commands/results are recorded separately under `docs/evidence/release-review`.
The Anea dormant source/evidence checkpoint remains clean at`9f53d1a6`; its new
national content has not been authored during this priority review correction.
