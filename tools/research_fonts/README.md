# Research font ownership repair

This bounded English typography repair replaces 301 inherited assignments using
twelve engine font aliases on `countrytechtreeview.gui`. Twelve new `ACResearch*`
bindings reuse the existing original `ACBriefing16` and `ACBriefing20` atlases.
There are no new glyph pixels, engine font images, global engine-alias overrides,
control moves or source-GUI recaptures.

`primary_contract.json` records the installed 1.19.4.1 default English alias names,
font metrics, base colors, inline color-code values and source hashes. Complete
engine font files and pixels are not copied. Japanese/Russian/Polish fallback
overrides are not imported or claimed as language coverage.

The new aliases retain original inline G/R/Y/H/T and applicable O/g state colors.
Former black-on-paper stat labels become secondary light text on the already
authored navy panels; amounts remain brighter. Headings/subtitles retain a muted
role with a readable cyan shade. Names and category labels use the eighteen-pixel
briefing line inside their existing twenty-pixel rectangles. Other headings use
the twenty-two-pixel briefing line, fitting even the inherited thirty-two-pixel
header rectangles. Every inherited declared text height and every literal year
caption is checked against the actual shipped font metrics. Dynamic names still
use their inherited rectangles and engine-bound tooltip/detail controls.

The two reused FNT files are explicitly LF in `.gitattributes`, matching their
already committed blobs. Their content and all DDS pixels remain unchanged. The
font manifest records normalized text hashes and raw DDS hashes; the explicit
base-only audit profile pins exactly four authored resources without family
wildcard exceptions. This profile does not imply enabled DLC or native activation.

`measure.py` checks the actual DDS alpha, not only the FNT line-height fields.
Across all 361 shipped glyphs, the sixteen-point atlas has ink from y=1 to y=19;
the twenty-point atlas has ink from y=2 to y=25 (exclusive bottom coordinates).
These fit the original minimum twenty- and thirty-pixel rectangles used by their
respective replacement roles. The report checks all 292 inherited declared text
rectangles, all 148 literal year captions, and ten illustrative role/name samples,
including accented capitals and an accented name. It preserves the distinction
between a previous line-height budget overrun and proven native clipping.

A seemingly convenient compact-metrics adapter was rejected after measuring its
alpha: moving the baselines up three/four pixels to match inherited compact font
metadata cuts accented capitals off above y=0. A negative regression demonstrates
this failure. Existing authored side bearings also remain visible in the report:
some letters extend one pixel left of their advance origin, and the fraction
slash extends three. The passing source checks cover vertical envelopes, literal
years and measured examples; they do not certify arbitrary dynamic-name width,
native left-edge clipping, parent-row clipping or line spacing at every UI scale.
The original dense stat-row geometry stays unchanged and requires native review.

## Pure composition API

```python
from research_fonts.migration import migrate, restore

value = migrate(source)                  # Before adding LAND/AIR pages.
original_tree = restore(cleaned, source) # After removing registered additions.
```

Both functions are pure. `migrate` changes actual `font`/`buttonFont` scalar
assignments, preserving comments, display strings and every other byte. It is
idempotent and leaves new AIR/LAND `ACBriefing16/20` controls alone. `restore`
returns a deep copy and requires the exact reviewed new value at each original
font field. A reverted engine alias, another authored alias or an unregistered
structural edit fails; normalization cannot hide it. All other fields remain
visible to the unchanged whole-AST comparison with the original captured SOURCE.

LAND calls this API in `build_ui.py`. The AIR owner can remove only its registered
folder/tab alongside LAND's before calling `restore`. The original
`tools/land_program/source/research_base.gui` and all 1,050 protected input hashes
remain unchanged. No whole captured GUI or protected manifest is overwritten.

## Reproduce

```powershell
python -B tools/research_fonts/build.py
python -B tools/land_program/build_ui.py
python -B tools/research_fonts/test_fonts.py
python -B tools/research_fonts/measure.py
python -B tools/research_fonts/measure.py --check
python -B tools/land_program/test_land.py
python -B tools/research_fonts/capture_reference.py --engine <HOI4-directory>
```

Both generators support `--check`. `build.py --capture-reference <HOI4-directory>`
refreshes only this package's separate primary metadata. Source checks and offline
measurements do not establish native rasterization, dynamic string coverage,
input, language fallback or the requested three display configurations. Native
testing remains paused; installation and user data are untouched.

`capture_reference.py` verifies the separately captured primary metadata without
rewriting it, then calls the effective dependency auditor with the exact four-file
font provenance profile. It records every actual font assignment grouped under
the fourteen resolved aliases (twelve migrated roles plus the two authored LAND
fonts). Research and decision screen ownership are independent of the completed
global presentation gate, which this focused capture does not request or claim.
After another owner adds registered research pages, regenerate `measure.py`'s
artifact before `--check`; the 301 original migrations remain fixed while the
canonical generated screen's additional authored assignments may increase.
