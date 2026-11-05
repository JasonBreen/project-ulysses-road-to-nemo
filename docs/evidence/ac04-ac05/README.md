# AC04/AC5 source and offline validation

`validation.json` records 27 successful independent commands, including the 35
new actual-script campaign regressions, the existing campaign/partner/story
owners, original artwork and event-capture proofs, the complete PowerShell
static suite and a comparison with the immutable starting revision.

The source digest was unchanged before and after the complete pass. Each command
has its own exit code and raw-log SHA-256. Raw logs remain in the ignored local
`runtime-output/ac04-ac05` directory. The receipt hashes the `tools` and `mod`
script/data inputs; this receipt documentation is outside those inputs.

The reference validator reports the same 520 warnings as the starting revision,
with no added or removed warnings. The static suite also retains two inherited
map warnings and one technology warning. The map warnings cover one placeholder
owned state and 204 placeholder strategic-region files.

With Python 3.12, Pillow 11.3.0, numpy 2.2.6 and PowerShell 7:

```powershell
python -B tools/ac_campaigns/run_checks.py --powershell (Join-Path $PSHOME 'pwsh.exe')
```

Add `--reference-game-root` with an installed read-only HOI4 directory when
available. This work's static pass used the installed reference. The runner
never launches HOI4.

Native parsing, ordinary 1991 progression, AI pacing, balance, rendering and
save/reload remain unaccepted under issue #8. The five fixtures are opt-in
offline observations; no native save or normal installation was changed.
