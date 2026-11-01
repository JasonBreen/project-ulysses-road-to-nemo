# Authored counter and audio-category delimiter repair

The stronger dependency inventory exposed two inherited authored files that its
strict source reader rejected with `Unexpected }`: the final line of
`interface/subuniticons.gfx` and the final line of
`sound/superevents_category.asset`. This repair removes one unmatched closing
brace from each file. The 561 counter sprite definitions, two sound-effect
members, category compressor settings, textures and audio files are preserved.
No media, leader, country setup, gameplay reward or historical outcome is added.

`before-after.json` runs the current source gate against the actual pre-repair
text from its recorded base commit in a disposable text-only fixture. Each
original file fails; the repaired set passes. This is **source parsing**, not an
in-game before/after screenshot or audio-playback result.

The new `tools/check_presentation_sources.py` gate strictly parses authored
`.gui`, `.gfx` and `.asset` files under interface, gfx, sound and music. It also
checks the three engine-bound unit group sprite names and the SuperEvents
category's named sound-effect bindings. CI runs this independently of texture
existence and effective-provider checks. Its current result is 81 parsed files,
561 counter sprite definitions and both named sound-effect bindings, zero
authored-source failures. It uses the audit reader, so unsupported engine syntax
and native acceptance remain separate concerns.

Reproduction from the repository root:

```powershell
python -B tools/check_presentation_sources.py --output docs/evidence/presentation-delimiters/source-gate.json
python -B tools/audit_visual_dependencies.py --strict-all
pwsh -NoProfile -ExecutionPolicy Bypass -File tools/Test-UlyssesStatic.ps1 -ModRoot mod/2985041246 -ReferenceGameRoot <installed-engine-reference>
python -B tools/overhaul/audit_consumers.py <installed-engine-reference> --gate-decisions --gate-screen ac_macro_economy.gui --summary-only --output docs/evidence/presentation-delimiters/ownership.json
```

The strict authored-asset check passes with 6,552 sprite definitions, 1,204 focus
icons and zero authored-GFX missing references. Full static/reference validation
passes with the inherited map2/reference2006/technology1 warnings retained.
Decision and macroeconomy requested-screen ownership each have zero failures.
The loose-reference source-reader failures fall from fourteen to twelve; the
remaining twelve belong to engine files and remain explicitly uninspected by
this reader. These narrow checks do not certify complete presentation closure.

Evidence is tied to exact source hashes in `source-gate.json`; the delivered
mod payload hash and validation context are in `validation.json`. Native testing
remains paused: no game launch, rendered counter inspection, audio playback,
save/reload, profile/settings change or normal installation synchronization was
performed. PR #29/#30 native acceptance checklists remain open.
