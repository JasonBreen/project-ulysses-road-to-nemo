# Usean partner integration review

This candidate combines the four national programmes, both actual shared-system
owners and the additive Erusean foundation. It was assembled in an isolated
review branch from verified main `3810d1a`. The original partner component is
`e7f770f`; the first shared-system integration is `e4f6b2c`, and the Erusean input
is `13c8e48`. Final integrated validation and the refreshed dependency head are
recorded under `docs/evidence/usean-partners/integration/results.json`.
Publication and exact-head remote CI remain separate owner actions.

## Contracts inspected and corrected

The national generators retain the stable `ac_up` namespace and read the
existing Usean war/project/calendar state. Paid actions call the actual
`ac_pol_change_capacity` and `ac_econ_pay_programme` owners after their readiness
and affordability conditions. There is no delivered substitute fiscal owner,
quote function or capacity setter. The optional fiscal mode still leaves the
political, institutional, time and civilian-allocation costs in force.

The originally unexecuted combined adapter incorrectly converted a repeated
HOI4 effect block into a unique-key mapping. Valid owner blocks repeat
`set_variable`, so the run stopped before reaching any contract test. The
adapter now extracts only the `limit` node, just as the owning executor does;
unknown operations still fail closed. No fiscal formula was altered to make
the integration pass.

Thirty-nine paid temporary service/scope spirits now publish
`allowed_civil_war = { always = no }`, matching the existing thirty-two enduring
policies. A civil-war clone must not inherit an unfunded paid allocation. The
source regression checks the actual seventy-one idea definitions. This is a
source inheritance guard, not observed native country-creation behavior.
The artwork manifest's source hashes were refreshed after the generator edit;
all DDS, PNG, binding and gallery bytes were independently compared and remained
identical. No image source or composition was changed.

The world/Erusean cherry-pick conflicted in the Erusean history and generated
country registry. Both the economic new-campaign eligibility block and the
Erusean foundation were retained. The actual integrated registry generator was
preserved, including optional metadata for all sixty-nine institutional/fiscal
profiles and its independent registry regressions. Generated world, Anea,
starting-government, macro, institution and partner output was rebuilt, followed
by registry refresh. The Erusean compatibility and conservative primary-source
budget tests remain part of the combined gate.

## Actual-owner and tree-priority coverage

`tools/usean_partners/test_integration.py` loads both complete real P1 libraries.
It adds only interpretation of national variables; it installs no readiness,
payment, capacity or quotation substitute. Its four tests cover:

- All twenty-nine operational scopes in full, retained experimental and disabled
  fiscal modes: eighty-seven paid starts, correct actual charge, finite resource
  use, capacity debit and duplicate-call protection.
- All scopes blocked by insufficient cash, fiscal arrears, exhausted capacity
  or capitulation, with no partial charge or reward.
- Authorisation and repeated quote refresh do not settle the budget or fabricate
  ledger history; the real monthly owner creates the next observation once.
- Actual country-selection ASTs give each current/original national host weight
  forty versus the eligible regional tree's five. Other national trees have
  zero weight. A clone retaining only the original tag, or another identity
  occupying the current tag, receives no national priority.

The last test is a source selection-weight assertion. It does not claim that
native focus assignment, AI selection, search, zoom or rendering was observed.
The twenty-seven-case national suite separately executes prerequisites, policy
alternatives, the Usean owner, preparation handoff, all reward guards, finite
services, bilateral refusal/interruption, late-save adoption and artwork.
Its explicit isolated fiscal/capacity adapters remain identified as such; the
actual-owner suite above provides the additional combined fiscal boundary.

## Reproduction and open acceptance

Use Python 3.12 with Pillow 11.3.0 and numpy 2.2.6, as pinned in CI:

```powershell
python -B tools/usean_partners/run_checks.py --engine '<read-only installed HOI4 root>' --core
```

The runner retains separate logs for the national and real-owner suites,
world/Erusean foundations, macro/ledger/forces, institutions, generated output,
registry, strict authored assets, available repaired-screen suites and the full
static wrapper. Commands and exit codes are recorded with repository and engine
paths redacted. Rerun after integrating a new dependency head. The real-owner CI
step runs independently so an earlier failure cannot be hidden by a later check.

Native testing remains paused. Decimal execution, deterministic chronological
focus courses, fixture outcomes and copied state do not establish native fixed
point arithmetic, actual AI pace, ownership/save serialization, military fuel
throughput or balance. The three required displays, long text, tree selection,
focus states, decisions and real save/reload remain open native acceptance.
The ordinary installation, launcher, settings and user saves were untouched.
