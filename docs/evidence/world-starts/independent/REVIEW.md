# Independent WorldStarts source review

Reviewed detached checkpoint **7e01e9b65b6fc1aa6ff269d3605c66252db96285**:
43 WorldStarts profiles, the existing five-country/Anea owners, and the recorded
P1 integration. This review changed no country, OOB, technology, profile,
placement, map, generator or normal installation file. Native testing remains
paused. Pending retained/legacy authoring is not treated as a missing-content
defect in this checkpoint.

The installed-primary source suite passes all **15 tests**, including recapture.
The independent review nevertheless found three calibration defects that those
tests do not detect. They should be addressed before claiming complete physical
start/input/personnel accounting. No crash-level defect was established.

## Findings

### 1. Non-core state modifiers are missing from usable capacity and input coverage

`tools/world_starts/placement.py` distributes industry by raw owned-state
building totals and computes retained inputs using infrastructure and a fixed
trade fraction. `compile.py:state_output` and the state-preservation test also
check raw category capacity without the non-core controller modifier.

The effective mod's `common/modifiers/00_static_modifiers.txt:202–207` explicitly
sets `non_core_controller` to `local_factories = -0.75`,
`local_resources = -0.65`, and `local_building_slots_factor = -0.5`.
Compliance effects are separate; the source worksheet does not model them.

At this checkpoint:

- YUK adds **3 civilian and 2 military factories** in state **515**, whose core
  remains KLG. It then requests all **45 raw military factories** in its opening
  production plan. The five new factories cause the raw category to become
  `large_town` with five base shared slots; the test does not account for the
  state's negative slot modifier.
- DOR's **10 raw military factories** include **3 inherited factories** in
  state **487**, whose core remains FRU. Its new resource additions also use
  that state. The worksheet reports zero steel, rubber and tungsten input
  margins without applying the non-core resource modifier.

This is a source accounting omission, not a claim about an observed native
factory count or exact rounding/compliance throughput. Avoid relying on new
non-core industry/resources, and discount or explicitly segregate inherited
non-core capacity when backing production. Preserve the inherited buildings,
cores, borders and ownership; changing a core is not a valid accounting fix.

The existing raw-total assertions remain useful preservation checks, but they
do not prove usable factories, buildable slots or domestic industrial inputs.

### 2. FRU's retained trade/economic policies and resource penalty contradict its green worksheet

`history/countries/FRU - Ferustia.txt:137–138` retains
`low_economic_mobilisation` and `free_trade`. It also retains
`FRU_industry_stolen`. In the effective authored definitions:

- `_economic.txt:free_trade` has `min_export = 0.75`, leaving a nominal
  **25% domestic fraction**, rather than the hardcoded 50% used by
  `placement.py:264–265`.
- `ideas/ferustia.txt:FRU_industry_stolen` has
  `local_resources_factor = -0.5` and an industrial output penalty.
- The inherited economic law has `fuel_gain_factor = -0.25`; the worksheet
  instead selects `civilian_economy`, with `-0.5`, for every country and labels
  every country's laws as the preserved defaults (`worksheet.py:29–30,95`).

FRU's worksheet currently claims zero aluminium/rubber/steel margins for inputs
of **4 / 2 / 6**. Even before applying its negative resource spirit, the
floating infrastructure extraction at 25% retention is only
**2.3 / 1.85 / 4.4**. The aluminium and steel shortfalls exist before native
rounding becomes relevant. There are no authored starting imports.

Derive actual opening laws and relevant spirits per tag, preserving those
policies. Either calibrate resource provision against their real effects or
record explicit import deficits, eligibility and civilian-factory costs. A
common base-output sensitivity can remain separately labeled, but it cannot
establish these countries' domestic input coverage or actual fuel income.

The uncommitted 50-profile observation also finds UST's retained
`local_resources_factor = -0.5`, so this fix should cover that slice too.

### 3. CSO's new standing force exceeds its default-law manpower pool

`profiles.json:2200–2245` supplies three infantry formations, each with six
infantry battalions and engineers. The actual generated OOB and captured
primary unit contracts require **18,900 land personnel**. Its 24 fighters need
another **480**, for **19,380** total in every covered DLC route.

CSO has **1,000,000 core population**. Its history supplies no mobilization
override, starting conscription bonus or leader trait that changes the pool.
The default `volunteer_only` law in `_manpower.txt:51–76` has
`conscription = 0.015`, giving **15,000 nominal recruitable personnel**.
The source-calibrated opening shortfall is therefore **4,380**, before a
replacement margin. The exact native history-loading/mobilization outcome has
not been tested.

The current suite checks equipment replacement and records template manpower,
but it does not compare all actual land/air/naval personnel against eligible
population, opening law/spirit modifiers and a reserve. Reduce the newly
authored force or explicitly review a policy change. Do not create manpower,
change population or silently change an inherited law to hide the deficit.

The content owner has reported plans to reduce CSO to four battalions while
preserving its three formations, and to give MST/SLA more headroom. Those
changes are **not present or independently accepted at this fixed checkpoint**.

## Personnel cross-check

`stable-personnel.json` traverses actual selected histories and OOBs in all four
routes, adds land/air/naval personnel from captured technical contracts, and
parses the actual opening law/spirit modifiers. All referenced opening ideas
resolve. The stable checkpoint's recruited leaders have no country-leader
traits contributing an additional conscription modifier.

Non-core manpower is deliberately excluded from this table's conservative
core-only pool; the review does not assert it is zero in the engine. CSO is
entirely core, so that qualification does not alter its finding. Ten/twenty
percent reserves are displayed sensitivities, not newly approved policy gates.

| Country | Maximum covered personnel | Core-only nominal pool | Headroom | Headroom after 10% roster reserve |
|---|---:|---:|---:|---:|
| CSO | 19,380 | 15,000 | -4,380 | -6,318 |
| MST | 54,480 | 60,000 | 5,520 | 72 |
| SLA | 12,840 | 15,000 | 2,160 | 876 |
| ROH | 33,310 | 45,000 | 11,690 | 8,359 |
| CAL | 26,005 | 45,000 | 18,995 | 16,394.5 |
| FCU | 93,360 | 165,487.005 | 72,127.005 | 62,791.005 |

CSO is the only stable-profile deficit and the only stable profile below a
10% roster reserve. MST has almost no slack beyond that sensitivity. SLA would
miss a 20% reserve by 408 personnel. The remaining stable profiles have positive
core-only headroom. FRU correctly has limited conscription plus its retained
10% conscription factor; it was not compared using the default law.

`active-personnel.json` is a separate, explicitly **uncommitted, non-acceptance
observation** of the 50-profile working set at **2026-10-31 23:07:48 UTC**, before
the owner's reported calibration corrections. Its recorded inputs were stable
during that observation:

- Profile SHA256: `ce446771c05896ee8642cb5b48b5c5ce7edcb1de6ff570928b61be7491c4556b`.
- Foundation SHA256: `a48264b4b01b02d066c93421f3db9698d3a997a0cece5ebd25df07dd58a04778`.

Its additional retained UST force requires **48,600 personnel** against a
**17,617.1205** core-only nominal pool after the retained spirits' combined
`conscription_factor = -0.9`. This is an inherited manpower liability, not a
request to trim preserved units or mint manpower. The other six additional
retained-country observations have positive headroom. Their native behavior
and the changing active branch were not accepted by this review.

## Checks and non-blocking test gaps

The following checks passed read-only:

```text
python -B tools/world_starts/test_world_starts.py --reference <engine>  # 15/15
python -B tools/usea_expansion/build_leaders.py --check
python -B tools/world_foundation/build.py --check
python -B tools/anea/foundation.py --check
python -B docs/evidence/world-starts/independent/reproduce.py --label stable-7e01e9b --output docs/evidence/world-starts/independent/stable-personnel.json
```

The review also confirmed no WorldStarts land/air/naval OOB references in the
event, on-action, decision or scripted-effect owners. The new setup is
country-history-only; no late-save/startup regrant callback was found. Current
government, Anea and five-country generators reproduce without a foreign-owner
rewrite. Actual production roles all have matching roster designs; no current
production-only air/ship design without a created variant was found. Microstate
combat-air/naval absences are explicit reviewed dispositions, not silently
missing files.

Remaining non-blocking regression gaps:

- The variant-order test checks stocks and deployed equipment, but does not
  execute/validate production references inside each loaded OOB's
  `instant_effect` at the moment of loading. A future production-only designer
  role could therefore need an additional variant-order regression. No current
  profile exercises that failing shape.
- Slot checks enumerate civilian/military/dockyard/silo counts rather than all
  effective `shares_slots` building types. No omitted refinery/reactor/etc.
  exists in the currently reviewed states, so this is a future guard gap.
- New level-2 routes cross **14 unique inherited level-3/4 edges** across six
  stable countries. Original rows are preserved, but effective duplicate-edge
  precedence is not established by the tests. The JSON retains the edges.
  This is not a claim of observed native rail downgrade; either prove the
  effective-level contract or avoid depending on uncertain duplicate ordering.

No native parse, AI pacing, manpower mobilization, physical delivery, fuel,
convoy/rail throughput, save/reload or screenshot acceptance is claimed.

## Reproduction and evidence boundary

The review probe is read-only except for the explicitly requested JSON output.
It records relative input paths, hashes, times and whether inputs changed during
reading, and verifies stable profile/manifest digests. It imports no installed
media or complete engine scripts. The committed checkpoint remains unchanged;
only this independent-review directory was added in the detached worktree.

The content owner/root received each concrete finding while review continued.
Recheck the three accounting cases against a new coherent owner checkpoint
before marking them fixed; the current passing suite alone does not establish
that result.
