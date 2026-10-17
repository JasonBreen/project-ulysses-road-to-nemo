# Economic foundation validation evidence

Local execution on 2026-10-17, from the isolated economy worktree based on `c72422d96f6bd9b33e61f725c2cdc8fe198a51d8`:

- Python 3.9.13: `python -m unittest discover -s tools -p test_economy.py -v` passed all 27 checks.
- The same checks passed through `tools/Test-UlyssesEconomy.ps1` with the already-installed Python executable supplied as `-PythonCommand`.
- `pwsh -NoProfile -File tools/Test-UlyssesStatic.ps1` passed. Map: zero structural errors, extra raster colors or out-of-bounds placements. Existing map warnings: one placeholder-owned state, 204 placeholder regions, and empty positions-file reference not supplied. Reference audit: 650 focus definitions, 599 event definitions, 3,180 inherited warnings; no blocking unresolved owned focus/event references.
- `git diff --cached --check` passed. Original history, events, national focuses, technologies and map files have no economy-branch changes.
- The inspected MD source paths were clean against pinned HEAD; the copied license's SHA-256 matched its source. No MD source file was written.

The actual-script harness produced these maxima over 3,914 weekly pulses, covering 1991 through end-2065 (rounded to 0.01 FU for display):

| Scenario | Maximum treasury | Maximum debt | Maximum unpaid bills |
| --- | ---: | ---: | ---: |
| Peace, high tax, basic services, capacity cap | 354,260.00 | 0.00 | 0.00 |
| Continuous war, low tax, expanded services, capacity cap | 2,000.00 | 3,900.00 | 439,763.38 |
| Same war, all industry lost after pulse 100 | 2,000.00 | 3,900.00 | 22,321.08 |

The stress test is reproducible as `test_1991_through_2065_stress_bounds` in `tools/test_economy.py`; all scenarios reconcile every weekly financial-position change and assert nonnegative balances below 1,000,000 FU and principal no greater than 6,500 FU. An intentionally excessive factory input exercises the provisional capacity cap. Continuous insolvency still creates substantial unpaid bills; numeric boundedness is not a balance or playability endorsement.

Deliberate-error coverage includes malformed syntax, unknown effects/variables, missing English localization, incorrect technology/equipment binding, absent procurement prerequisites, repeated transaction attempts, exhausted credit and partial repayments. These checks operate on the authored scripts, not a disconnected economic formula.

This evidence is static/offline only. Native HOI4 1.19 parsing, fixed-point precision/range, scheduling, category rendering, original-content parity, asset cleanup, native save/load, civil-war inheritance, AI balance, end-2065 gameplay and VS Code/Antigravity UI execution are not verified here. The separate port was still changing; no claim is made about its newer head. See [ECONOMY.md](ECONOMY.md) for the integration and runtime gates. Exact-head remote CI results are recorded in the tracking PR after publication.
