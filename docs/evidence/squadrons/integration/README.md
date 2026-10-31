# Squadron package on the reviewed prerequisite stack

This candidate composes repair/privacy PR #32, World Foundation PR #33, the
shared economy/institutions PR #34 and partner-programme PR #35 with the six
original squadron campaigns and complete artwork. The story component is
`ee8104e8027908b81aed54343ccf8fdd090650a1`; its integrated runtime payload was
tested at `83edac9`. The later prerequisite merge adds review documentation,
offline economy reconstructions and CI checks without changing delivered mod
bytes. The retained [results.json](results.json) identifies the tested payload
with its sorted-path/raw-byte SHA-256.

Reproduce from the repository root with Python 3.12, Pillow 11.3.0, numpy 2.2.6
and PowerShell 7:

```powershell
python -B tools/squadrons/run_integration.py --engine <read-only-game-reference>
```

The optional `--engine` argument supplies installed scripts to the full static
reference audit. It does not launch the game or write to the reference directory.
Without it, the source suite retains its explicitly reported reference skips.

All twelve recorded checks passed: narrative consistency, 24 story runtime
cases, eight artwork cases, real partner/fiscal/institution integration,
World foundations/registry, focus geometry, decision bounds, screenshot repair
regressions, roadmap counts, strict authored assets and the full static suite.
The registry was refreshed for the story host declarations. CI retains each
story gate as a separate failing step and preserves all prerequisite checks.

The strict authored audit reports 6528 sprite definitions, 1204 checked focus
icons and zero missing authored texture references or cleaned-family regressions.
The full static/reference wrapper reports map errors 0, retained placeholder
map warnings 2, reference warnings 2006 and technology warning 1. These counts
do not claim completed worldwide support or a closed engine/DLC dependency graph.
The changed-story-script scanner separately found zero errors and warnings.

**Native testing remains paused.** These are source, bounded offline interpreter
and image-review results. Shortcut fixtures and copied state are not native
natural progression or save serialization. PR #29/#30 acceptance lists remain
pending. No game launch, desktop input, normal installation, profile, display
setting or user save was touched.
