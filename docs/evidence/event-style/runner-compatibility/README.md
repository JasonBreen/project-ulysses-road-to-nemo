# Live Event-Fit runner after style composition

The separate14-group full run remains pinned to source`01cb3118` in
[`../source-checks/results.json`](../source-checks/results.json). It was not
rewritten after this runner-only follow-up.

The live runner now defaults to the explicit reviewed `event-style` contract. It
requires the registered23-field GUI restoration and actual style metadata, then
zero eventwindow/decision ownership failures under an explicit base-only profile.
Historical `original-fit` mode requires the original unstyled GUI and exact15
fallbacks. There is no automatic missing-owner or arbitrary-failure acceptance.
Ordinary new results go to `event-picture-fit/composed-source-checks`, preserving
the old historical receipts.

At clean source **`1b8028936bedd96e3bf79f57f81443e2f2325cf7`**, all five runner
regressions passed, including missing screens, unexpected fallbacks, wrong exit
codes, unspecified/DLC-enabled profiles, wrong source mode and exact historical
failure-set negatives. The live affected contract also passed:

```powershell
python -B tools/event_picture_fit/run_checks.py --engine $env:ULYSSES_GAME_ROOT --event-screen-contract event-style --screen-contract-only --output docs/evidence/event-style/runner-compatibility
```

[`results.json`](results.json) records identical before/after receipts for8,766
tracked non-evidence inputs with raw hash
`82de7d0ac1943b68173b98bd5655f63925c968d69d05983b5847462a012fd9a0`.
The actual dependency report has zero failures on both requested screens.
Wider unresolved pools and inherited reference parse failures remain recorded;
this is not a global presentation or native acceptance gate.

This follow-up changes only the runner, its focused test, documentation and CI
invocation. No mod, GUI, texture, font, source master, original fit capture,
historical15-backlog receipt or completed14-group receipt changes.
