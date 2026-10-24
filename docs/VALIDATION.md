# Static validation

## Aftermath transition checks

`Test-UlyssesStatic.ps1` also runs `tools/Test-PeaceWeInherit.py`, including the
read-only authoring/output parity check. Python 3.9+ is required; Windows prefers
the existing `py` launcher, with `python` as the fallback. Static CI declares its
Python runtime explicitly. The offline harness executes the shipped aftermath
script subset and rejects unknown syntax; it does not emulate the HOI4 engine.
See [the expansion checklist](PEACE_WE_INHERIT.md#acceptance-checklist).

The before/after reference inventory for this expansion is 666→724 focuses,
620→662 events, and **2,011→2,011 warnings**. Existing map and technology warnings
remain design inventory. Native acceptance remains unrun.

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

`tools\Test-UlyssesStatic.ps1` launches its child validators with the same PowerShell edition used to launch the wrapper, so the documented `powershell.exe` command does not require a separate PowerShell 7 installation. It also fails on invalid building province associations, duplicate event definitions, malformed event targets, and a missing BOM on the added Belkan continuation localization.

`tools\Validate-UlyssesReferences.ps1` separately audits focus prerequisites/position references, owned event references, country-history localization coverage, and event/focus localization keys. The optimized full audit completes in about 13.4 seconds on the current checkout, with 0 structural errors, 0 missing focus references, and 0 missing owned event references. Its 2,011 warnings are inherited archive localization inventory (1,581 missing and 60 empty event-key references, 283 missing and 67 empty focus keys, and 20 country-history tags without localization), not newly introduced campaign-reference failures. The localization index accepts both versioned `key:0 "text"` and versionless `key: "text"` entries; event localization auditing also includes underscore-only IDs used by `custom_effect_tooltip`, preventing missing keys such as `BLK_unlock_focus_tt` from being silently skipped. The campaign contract separately requires and passes all new campaign localization.

`tools\Validate-UlyssesTechnologies.ps1` validates technology date literals and `start_year` values against the documented 1900–2065 audit horizon. It is a syntax/horizon guard, not evidence that authored gameplay or canon-backed content exists for every year. Technology names that resolve from the base game are intentionally not treated as missing mod localization by this validator; their provenance and any Strangereal-specific replacements are tracked in the canon/content roadmap.

`tools\Test-CampaignReviewRegressions.py` covers the inherited defeat-tree handoff, chronology gate, mutually exclusive opening decisions, AI fallback timing, postwar idea cleanup, decision categories, neutral penalty removal, focus AI syntax, and continuation localization. `tools\Test-RunUlyssesCampaignChecks.ps1` is a negative test that injects a failing child command and verifies the aggregate PowerShell wrapper returns nonzero.

`tools\Validate-NoVanillaAssets.ps1` performs two independent asset checks. The path-relative check compares normalized text or raw binary SHA-256 hashes at matching paths and uses the immutable April extraction to classify inherited versus newly introduced installed-reference matches. The path-independent check covers visible/audio asset extensions, uses file size only to prefilter installed-reference candidates, and then compares full SHA-256 hashes regardless of filename or directory. It therefore catches renamed copied assets without treating different files as matches. On the current repair head, the authorized HOI4 reference comparison reports 13 inherited text/config matches (all also present in the immutable baseline), zero new path matches, zero path-independent asset matches, and zero warnings. A dedicated regression fixture covers CRLF/LF-only differences.

The static wrapper also asserts `NDefines.NGame.END_DATE = "2066.1.1.1"`. HOI4 end-date semantics are intended here as a next-day boundary so the inclusive project cutoff includes 2065-12-31; only a runtime date-advance test can confirm the engine behavior for the selected 1.19 build.
