# Usean partner integration review

This candidate combines the four national programmes, both actual shared-system
owners and the additive Erusean foundation. It was assembled in an isolated
review branch from verified main `3810d1a`. The original partner component is
`e7f770f`; the first shared-system integration is `e4f6b2c`, and the Erusean input
is `13c8e48`. The repaired-interface restack is integrated through shared-system
head `8a96ff0` (World `2afd9fa`). Final integrated validation and the refreshed dependency head are
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

A subsequent source review reproduced an interruption bug: when FCU was annexed
and restored before a weekly observer, an old pending offer could still add its
recovery reward (45 → 47 in the actual-source fixture), or an accepted relationship
could remain active. The annex handler previously recognized only the senders.
It now immediately clears FCU's receipts and both sides' diplomatic state through
the existing once-only close path. Pending Amber slots return once; accepted
slots and all paid political/fiscal costs remain spent.

The same direct cleanup is registered for the primary verified immediate
capitulation and subject-annexation scopes. Known puppet, subject-autonomy and
subject-free callbacks close only diplomacy; domestic services remain available
under external constraints. A new war-relation callback revalidates both actual
participants, including entry into an existing war, and preserves relationships
when their parties merely fight unrelated countries. The scope provenance and
installed source hashes are in `tools/usean_partners/engine_contracts.json`.
The immediate callback tests include rapid restoration with no weekly tick,
both recipient and sender, pending/accepted offers, pre/post capitulation or
existence flags, repeated cleanup, retained costs and exact-once slot return.
The national suite now contains thirty cases rather than its original twenty-seven.

Only installed primary callbacks are used: `engine://common/on_actions/00_on_actions.txt`
records annexation, immediate capitulation, peace-conference puppeting and each
new war relation; `engine://common/on_actions/01_tfv_on_actions.txt` records
subject annexation, autonomy changes and liberation scopes. The source tests
exercise those captured contexts, not native callback delivery. A custom status
toggle that emits none of these callbacks is detected at action/reply/completion
revalidation or weekly observation; a transient toggle between every such
observation is not reconstructed. Native relative callback timing remains open.
No Anea owner or established national war/project outcome was changed.

The world/Erusean cherry-pick conflicted in the Erusean history and generated
country registry. Both the economic new-campaign eligibility block and the
Erusean foundation were retained. The actual integrated registry generator was
preserved, including optional metadata for all sixty-nine institutional/fiscal
profiles and its independent registry regressions. Generated world, Anea,
starting-government, macro, institution and partner output was rebuilt, followed
by registry refresh. The Erusean compatibility and conservative primary-source
budget tests remain part of the combined gate. After the repair restack, the
overview source manifest and regional naming overlay were regenerated against
the integrated states; reviewed World labels retain their existing ownership.

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
The thirty-case national suite separately executes prerequisites, policy
alternatives, the Usean owner, preparation handoff, all reward guards, finite
services, bilateral refusal/interruption, late-save adoption and artwork.
Its explicit isolated fiscal/capacity adapters remain identified as such; the
actual-owner suite above provides the additional combined fiscal boundary.

## Delivery accounting and current roster

The release manifest now records SNS 72, AMB 60, UGE 48 and DEL 48 as 228
source-delivered country definitions. Together with the six previously merged
FCU rebellion focuses, 234 of the approved 1,028 additions are delivered and 794
remain. The shared regional 36 belong to their separate institutional framework
and are not counted again. Package 2's story integration remains a separate branch;
this candidate does not claim the complete story/art portfolio is included.

The four partner starting force/industry/logistics rosters come from the
integrated World foundation dependency. This candidate additionally brings in
the reviewed Erusean roster and component logistics, retaining its inherited
28 civilian factories, 23 military factories, 11 dockyards and 16 ports. Existing
leaders/office representations, country ownership and outcome owners remain
unchanged. Neither the registry nor these source tests certify native balance.

## Final combined source results

The retained final run passed all 24 primary commands, including the complete
static wrapper with a read-only installed reference, plus eight additional
compatibility commands. Component counts are national 30, actual-owner 4,
World/Erusean 20, macro 27, shared-owner 4, ledger 14, institutions 20, force-upkeep 8,
focus-screen 9, decision-screen 16 and overhaul 7. Additional suites passed legacy 27,
factions 35 (no skips), Usean expansion 17 and Anea integration 5; campaign,
briefing, typography and Continental War generation checks also passed.

The full wrapper reported map errors 0 and two map warnings (one placeholder-owned
state and 204 placeholder strategic regions), reference warnings 2006 and one
technology warning. This is not a warning-free or universal-playability claim.
No caption/geometry bound was weakened. All thirty resolved focus trees are
covered by the repaired focus-screen geometry loop; actual font advances and
all national decision titles passed their source checks. Native rendering is
still untested.

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
