# Scoped event-window defaults

This owner replaces exactly 17 sprite-reference fields and six font fields in
`interface/eventwindow.gui`. It contains no event content, leader definitions,
agency definitions, government changes, gameplay effects or layout changes.

`SOURCE_eventwindow.gui` is a normalized copy of the original GUI. Its hash must
match the **unchanged** historical `event_picture_fit/contract.json`. Generation
substitutes only the 23 registered scalar values at explicit named-control paths.
Independent lexical and ordered-AST restoration require the entire original
source and ordered tree to match. Reverted bindings, extra/missing controls,
unknown values, changed actions/conditions/geometry and unrelated edits fail.
The fit owner admits only this restoration API; its original capture, pictures,
548 protected originals, 108 Anea focus DDS and military captures stay intact.

## Reproduction

Use Python 3.12 with Pillow **11.3.0**, the CI packaging version. There is no game,
desktop, network, downloaded asset or external editor dependency.

```powershell
python -B tools/event_style/build.py
python -B tools/event_style/build.py --check
python -B tools/event_style/validate.py
python -B tools/event_style/review.py
python -B tools/event_style/review.py --check
python -B tools/Test-EventStyle.py
python -B tools/Test-EventPictures.py
```

For read-only installed-reference verification:

```powershell
python -B tools/event_style/primary.py --engine $env:ULYSSES_GAME_ROOT --check
python -B tools/overhaul/audit_consumers.py $env:ULYSSES_GAME_ROOT --profile docs/evidence/effective-dependencies/profiles/base-only.json --gate-screen eventwindow.gui --gate-decisions --summary-only --output docs/evidence/event-style/effective-eventwindow-base-only.json
```

`primary.json` records the installed **1.19.4.1** launcher `rawVersion`, definition
and texture hashes, DDS header dimensions, sprite types and original metadata.
Only definitions/headers are captured; no installed image pixels are imported.
PE ProductVersion `1.0` is not used as a game-version identifier.

## Original asset package

The editable generator `build_art.py` records the same geometric primitives as
12 SVG masters and produces uncompressed RGBA DDS textures. `assets.json` records
all dimensions, frame counts, alpha counts, source/runtime hashes, 13 sprite
bindings and unchanged font raw hashes. Every texture has an actual GUI consumer.
Midsection and bottom use distinct sprite aliases over one shared seamless tile.
The geometry is authored for this project and asserts no real agency identity.

The two `ACEvent16`/`ACEvent20` aliases use the existing ACBriefing16/20 bitmap
atlases and metrics byte for byte. Global engine font/leader/agency aliases are
not overridden. Unknown faces use a neutral office document/building mark;
dynamic character and agency control bindings remain unchanged.

The actual native sprite types are preserved: ordinary `spriteType`,
`corneredTileSpriteType`, and `frameAnimatedSpriteType`. The operative strip has
24 distinct 528×596 states, 80fps, no looping, no play-on-show and unchanged pause
metadata. The transparent 95×95 image retains its native 3×3 quad, 1px border,
non-tiled center and existing effect. Mid/bottom tile dimensions are 580×66 with
290×16 borders. Actual scaled portrait bounds have a fully clear integer alpha
aperture (9,10)–(166,221) inside the 172×232 frame.

The inherited agency texture was **233×119 with two frames**, a nominal 116.5px
per-frame width. The approved authored strip is **234×119 with two complete
117×119 frames**: an explicit nominal **+0.5px per frame** correction. Its actual
GUI bounds end at x478/y154, inside the 528px operative body and above the title
at y170. Native slicing and animation behavior remain unaccepted.

## Evidence limits

Review PNGs use actual delivered textures and shipped bitmap glyph/kerning/alpha
metrics. Only PNG compression may differ: checks require equal dimensions and
every decoded RGBA pixel. All DDS/SVG/GFX/manifest bytes remain exact.

The four source-coordinate diagrams deliberately do not invent engine reflow.
The original zero-height leader roots, child anchors and section sizes remain
unchanged. Source anchors can overlap when drawn without native section sizing;
these diagrams are not accepted native event layouts. The source contains no
authored leader/operative events, so those two template illustrations use a
labelled long-text stress sample from actual country text. Their unscrollable
stress overflow is recorded; no real current event is claimed to fit there.

Only well-formed English quoted localization lines are measured. Missing keys,
malformed inherited lines and runtime substitutions are retained as explicit
measurement exclusions, not silently fitted or rewritten. Existing country/news
scrollbars remain the mechanism for long descriptions. Native wrap, input,
scrolling, portrait substitutions, reflow, frame slicing and display scales need
separate acceptance.

The effective eventwindow ownership gate is bounded to that screen. Wider
portrait pools, agencies, event pictures, models, MIOs, audio and DLC/runtime
fallbacks remain their own open audit families.
