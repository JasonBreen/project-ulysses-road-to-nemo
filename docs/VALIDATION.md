# Static validation

The repository includes `tools/Validate-UlyssesMap.ps1`. It reads the mod as text and binary metadata only; it does not load, launch, or execute HOI4 or mod code.

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Validate-UlyssesMap.ps1 -ModRoot .\mod\2985041246
```

The validator fails for structural errors such as duplicate IDs, unknown province references, repeated state/strategic-region assignments, invalid adjacency endpoints, or non-lake land provinces missing from states. It reports the following as warnings requiring design or runtime follow-up:

- placeholder-owned states;
- `XXX`/placeholder strategic regions;
- empty `map\positions.txt`;
- incomplete building placement keys;
- unexpected province-raster dimensions.

The validator is not a substitute for the HOI4 parser, a launcher test, a save/load test, or a long-run AI campaign.
