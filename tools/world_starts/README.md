# Active-country physical foundations

This owner is being delivered in local slices. The current implemented slice is
FCU/YUK/NPT, the 25 previously industry-empty active starts, and fifteen
inherited-industry starts without a standing roster, and seven retained-army starts. The baseline inventory covers all 61 active histories, four BBA/MTG
routes and FATO's extra human-Belka context. The original 25-country proposal remains frozen; delivered profiles record reviewed
upward adjustments needed to replace actual combat and transport roles.
PLH/state 171 and seven landless emergent histories receive no blanket start grant.

All new budgets, force compositions, resource additions, numbered formations and
technical equipment recipes are provisional gameplay. They do not establish
official aircraft identities, mineral geography, economic output or a canonical
order of battle. Existing leaders, political setup, borders, cores, manpower,
province lists, mapped identities and individual buildings/resources are retained.

`inventory.py` reads actual history conditions and selected OOBs. Unknown history
conditions fail closed. `baseline_inventory.json` is a frozen intake at `60ec3a6`;
do not regenerate it from the changed candidate and call that a preserved baseline.

`profiles.json` owns the implemented budgets and programme recipes. `placement.py`
captures their original state histories and reproduces additive industrial and
logistics placement on exact owned-land adjacency. It retains the owned capital,
uses existing airports and authored naval spawn positions, and treats disconnected
components separately. `foundation.json` records all protected quantities,
placements, additions, exact routes and technical-source metadata.

`compile.py` owns only the profiles listed here. It gives each selected route one
land OOB and only the air/naval OOBs its role actually uses, after the necessary unlocks and variants. It supplies real
production lines and replacement/transport stocks, full opening fuel and scoped
AI roles/research. All setup is country-history-only; there is no startup,
weekly, event or save-load OOB callback. Fiscal eligibility and government-owner
markers are preserved. The physical setup works with macro/legacy/off fiscal rules.

The existing Anea and five-country World generators retain their own countries.
Shared map rows have explicit owners in `tools/logistics_owners.json`; no foreign
tail is accepted just because a hash was updated. BLK/OSE/SAP/FAT legacy history,
OOB and production repairs belong to the separate `tools/world_legacy` component.
This owner does not rewrite those histories or duplicate their armies.

Technical metadata contains only the selected IDs, unlock requirements, equipment
cost/resource/fuel numbers and subunit needs required to reproduce the package.
No installed textures, models or complete engine scripts are imported. A first
capture or changed profile needs an explicit read-only primary reference:

```powershell
python -B tools/world_starts/placement.py --reference '<read-only HOI4 root>'
python -B tools/world_starts/compile.py
python -B tools/world_starts/worksheet.py
python -B tools/world_foundation/registry.py --output tools/world_foundation/country_registry.json
python -B tools/overhaul/build_overview.py
```

Ordinary reproduction works without an installed game. It checks the captured
profile digest, geometry, actual output, production and equipment contracts:

```powershell
python -B tools/world_starts/placement.py --check
python -B tools/world_starts/compile.py --check
python -B tools/world_starts/worksheet.py --check
python -B tools/world_starts/test_world_starts.py
```

Pass `--reference '<read-only HOI4 root>'` to the tests to recompute the technical
contracts and compare every captured primary-source hash. Without it the installed
reference recapture is explicitly skipped; the actual-script and geometry tests
still run. CI exercises that offline route on Windows and Linux.

The sustainment worksheet checks actual template needs, production inputs and
replacement arithmetic. Air/naval fuel coefficients come from primary definitions.
Primary subunits can omit fuel while their equipment uses it, so army fuel is
reported as an explicitly unverified per-subunit equipment-stat proxy plus a
separate literal-equipment stress scenario. It is never silently treated as zero.
Native aggregation, mission tempo, loss rates and physical delivery remain pending.

FCU's retained mainland/capital component is landlocked, while its owned coast is
on detached islands. Its six new docks are placed on an owned coastal component;
no mainland coast, new faction or cross-water rail is invented. Existing coalition
membership and friendly transit are recorded, with native naval relay acceptance
explicitly pending. YUK's full high-tempo proxy exceeds domestic fuel income;
normal eligible oil imports or lower tempo remain necessary. Oil is not inflated
to promise unlimited all-force combat.

Native testing remains paused. Static checks do not establish game parsing,
fuel/convoy/supply throughput, AI growth, natural pacing or save/reload acceptance.

Retained-army mode composes original cumulative units blocks without loading a second army. NSB armor roles have explicit additional source cases and narrow history-only unlocks; see the calibration ledger for the unresolved native/extra-DLC boundaries.

`personnel.py --check` verifies the selected OOB report and exposes the preserved UST reinforcement debt. Universal sustainable-start acceptance remains false; see docs/WORLD_STARTS_ACCEPTANCE.md. `policies.py` captures actual starting laws/ideas and relevant technology effects; conservative core capacity and explicit import deficits replace raw-count/default-law assumptions.

The final-four physical adapter is `legacy_foundation.py`. It owns only state
history additions, exact owned-component routes, supply nodes and provisional
hub captions for BLK/OSE/SAP/FAT. Their armies, named hulls, aircraft, stocks,
production, research and AI belong to `tools/world_legacy`; this adapter cannot
write their histories or OOBs. `legacy_inputs.json` records the actual force
owner's manifest and every selected history/OOB receipt. A missing or changed
local component fails `--require-integrated-owner`; an external worktree capture
alone cannot satisfy that gate. The separate `legacy_sustainment.json` applies
their actual opening laws and inherited spirit costs to production inputs,
trade-CIV allowances, personnel and fuel sensitivity cases.

```powershell
python -B tools/world_starts/legacy_foundation.py --capture-source . --reference '<read-only HOI4 root>'
python -B tools/world_starts/legacy_worksheet.py
python -B tools/world_starts/test_legacy_logistics.py --require-integrated-owner
python -B tools/world_starts/legacy_foundation.py --check --require-integrated-owner
python -B tools/world_starts/coverage.py --check --require-integrated-owner
```

`coverage.json` partitions the 61 active starts among fifty profiles here, five
World Foundation profiles, two Anea profiles and four Legacy profiles. It reads
all 244 base BBA/MTG country-history branches and the separate FATO context.
NSB/La Resistance cases remain identified with their owners. This is source
coverage, with UST's established policy debt and extra DLC/native release gaps
preserved; it is not universal sustainable-start acceptance.
