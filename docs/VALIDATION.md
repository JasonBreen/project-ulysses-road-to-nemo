# Static validation

The repository includes `tools/Validate-UlyssesMap.ps1`. It reads the mod as text and binary metadata only; it does not load, launch, or execute HOI4 or mod code.

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-UlyssesMap.ps1 -ModRoot .\mod\2985041246
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Test-UlyssesStatic.ps1 -ModRoot .\mod\2985041246 -ReferenceGameRoot 'G:\steamlbirary\steamapps\common\Hearts of Iron IV'
```

With `-ReferenceGameRoot`, the validator compares optional format-sensitive files against the installed game. In this archive and installed build, both `map\positions.txt` files are empty, so that is recorded as a matching-format note rather than a defect. The validator also checks province RGB coverage, building/unit-stack coordinate bounds, railway province counts, and supply-node references.

The validator fails for structural errors such as duplicate IDs, unknown province references, repeated state/strategic-region assignments, invalid adjacency endpoints, invalid raster colors, out-of-bounds placement coordinates, or non-lake land provinces missing from states. It reports the following as warnings requiring design or runtime follow-up:

- placeholder-owned states;
- `XXX`/placeholder strategic regions;
- empty `map\positions.txt` when no installed reference is supplied;
- incomplete building placement keys;
- unexpected province-raster dimensions.

The static regression script treats structural errors, non-lake land omissions, extra raster colors, and out-of-bounds placement coordinates as failures. It also asserts that the preserved demo-end event exposes the `ac_continuation_active` handoff flag. The validator is not a substitute for the HOI4 parser, a launcher test, a save/load test, or a long-run AI campaign.
