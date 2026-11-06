# National depth: bespoke 150-focus trees for every country

This is the compiler for the programme that gives every country at least 150
focuses, each one visible (plan approved 6 November 2026). The definition of
done is `tools/Test-FocusVisibility.py`, with its ratchet in
`docs/evidence/focus-visibility/baseline.json`.

| File | Role |
| --- | --- |
| `spec.py` | The spec constructors a writer uses: country, branches, focuses, rewards, requirements, ideas, events and offices |
| `catalogue.py` | The vetted vocabulary: modifiers with maximum magnitudes, buildings, technology categories, search filters, the mod's parties and sub-ideologies, and each country's own 1991 states |
| `layout.py` | Compact placement: one lane per branch, tiers two columns apart, bands below the shared institutional block (rows 0-10), at most 23 columns for Usean minors and 35 for other countries |
| `art.py` | One unique procedural icon per focus from the shared glyph library, idea icons, three national event pictures and office cards; uncompressed RGBA DDS; Pillow 11.3.0 |
| `compile.py` | Spec in, mod files out (see below), with validation that raises on the first problem |
| `lint.py` | The bespoke and anti-filler gate (see `BRIEF.md`) |
| `package.py` | Builds or checks every spec in both roots, and writes each package's `budget.json` and `assets.json` |
| `test_compiler.py` | Golden output, layout, validation and lint regressions on `fixtures/fixture_spec.py` |
| `BRIEF.md` | The writer brief for one country |

**What `compile.py` writes:**
- the tree, which imports the 36 shared institutional focuses
  (`tools/institutions`);
- ideas, events, office characters and regime effects (the only government
  change, at AI weight 0);
- localisation with a BOM, and readable labels for every flag;
- sprites.

**Roots:**
- **Usean countries:** `tools/usea_depth/<package>/countries/<TAG>.py`. IDs are
  `<TAG>_ud_*`, trees `ac_ud_<tag>_tree` in `ac_ud_minor_<tag>.txt`, and art
  goes in `gfx/AC_usea_depth/<package>/`.
- **Everyone else:** `tools/world_depth/<tag>/content.py`. IDs are
  `<TAG>_wd_*`, trees `ac_wd_<tag>_tree` in `ac_wd_<tag>.txt`, and art goes in
  `gfx/AC_world_depth/<tag>/`.
- **Budgets:** each package's `budget.json` feeds
  `tools/overhaul/check_release_plan.py`, under
  `approved_expansions.usea_depth` and `world_depth`.

```text
python -B tools/national_depth/test_compiler.py           # Pillow 11.3.0
python -B tools/national_depth/package.py --check
python -B tools/Test-FocusVisibility.py
python -B tools/overhaul/check_release_plan.py
```

All of this is static and offline evidence. Native parsing, the rendered focus
screen and balance are untested (#8).
