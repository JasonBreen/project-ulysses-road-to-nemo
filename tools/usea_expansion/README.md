# Usean expansion authoring sources

This directory owns the 1991–2005 expansion, original briefing artwork and
packaging of the separately credited official AC8 promotional assets.

The implementation base is `8f503d1de6b434031fcb110a6dd1dd7f26622a78`, verified
against remote `main` on 30 October 2026. Development uses the separate
`codex/usea-art-expansion` worktree. The installed mod and ordinary user profile
are not build outputs.

## Rebuild

Use Python 3.12 and Pillow 11.3.0. The bundled DINish font and its OFL license
are in `tools/frontend_typography/source`. Run from the repository root:

```powershell
python -B tools/build_continental_war.py
python -B tools/usea_expansion/build_content.py
python -B tools/usea_expansion/build_ui.py
python -B tools/usea_expansion/build_fonts.py
python -B tools/usea_expansion/build_art.py
python -B tools/usea_expansion/package_media.py
python -B tools/usea_expansion/build_gallery.py
python -B tools/Test-UseaExpansion.py
python -B tools/audit_visual_dependencies.py --strict-all
```

`repair_frontend.py` applies the full-viewport canvas and background-picker
repair idempotently. `repair_research.py` is a migration driven by an engine
dependency report, not a normal rebuild step. The committed GUI is its output.
`capture_art_contract.py GAME_ROOT` is an explicit developer metadata import;
normal artwork rebuilds do not read installed-game pixels or files.

`build_continental_war.py --check`, `build_content.py --check`, and
`build_ui.py --check` compare generated output without modifying it. The
Continental War generator remains the owner of its established trees/effects.

## Artwork records

| Record | Purpose |
| --- | --- |
| `original_art.json` | Ten original illustration prompts, provenance and corrections |
| `sources/original_events/` | Editable lossless PNG masters, including the correction removing the yellow mark |
| `official_art.json` | Official Bandai Namco source URLs, retrieval date, credit and source hashes |
| `sources/official_ac8/` | Unmodified promotional downloads and named character art |
| `media_assets.json` | Packaged event, loading, thumbnail and portrait dimensions, bindings and hashes |
| `focus_art.json` | All 192 focus IDs, titles, semantic motifs, bindings and texture paths |
| `focus_compositions.py` | Subject selection and distinct arrangements; no baked focus-title captions |
| `ui_assets.json` | Recorded sprite formats, frame counts, source reference paths and format corrections |
| `assets.json` | Every generated UI/focus/policy/continuous texture, dimensions, frames and hash |
| `fonts.json` | Briefing font format, glyph counts and source hash |
| `focus_contract.json`, `scrollbar_contract.json` | Engine control identities and compatible geometry; no game pixels |
| `continuous_contract.json` | Inherited 1.19.4 continuous-focus behavior; only the artwork binding changes |

DDS output is uncompressed RGBA to preserve deliberate apertures and avoid
introducing compressor-dependent artifacts. Sprite strips are horizontal; width
must divide exactly by frame count. Panels are opaque, overlays and icon
apertures transparent. Original file dimensions that were not integral frame
widths are retained as `source_width`, with the correction in `format_repair`.

The source PNGs are the reproducible inputs for the generated illustrations:
rerunning an image model is not claimed to produce identical pixels. The DDS
packaging and procedural line artwork are reproducible from committed inputs.
There are no added image watermarks or invented human leader portraits. The
AC8 portrait collection does not assign those characters to governments;
Sinclair and the office leaders are implemented separately as described below.

## Official promotional artwork

The AC8 source layer is **official promotional artwork**, credited to
**ACE COMBAT 8: WINGS OF THEVE / Bandai Namco Entertainment**. It is separate
from the original provisional illustrations. Source pages:

- https://en.bandainamcoent.eu/ace-combat/ace-combat-8-wings-of-theve
- https://en.bandainamcoent.eu/ace-combat/ace-combat-8-wings-of-theve/characters
- https://en.bandainamcoent.eu/ace-combat/ace-combat-8-wings-of-theve/press

The press material supplies editorial assets and credit instructions; this
record does not assert ownership, a commercial license, or general permission
to redistribute the publisher's assets. Publication remains a separate action.
The original downloads and credits are preserved. The AC8 characters belong to
its later setting and are delivered as a named portrait collection, without
inserting them into the 1991–2005 governments.

## Native isolation and evidence

`prepare_native.py` creates a physical engine copy and an isolated profile,
sets that copy's `userdir.txt`, copies the exact candidate mod payload, and
records hashes. It refuses to overwrite an existing session. Use
`--sync-payload` only while the test game is closed; it checks for stale files
instead of silently deleting them. `--verify-normal` compares the normal
profile's configuration, saves and logs against the preservation manifest.

`audit_screens.py GAME_ROOT --output REPORT.json` resolves the effective
engine/mod GFX files and scrollbar templates used by the repaired focus and
research screens, including runtime-selected focus-state sprites. It reports
engine imagery, missing assets, conflicting effective definitions and retained
shader/flag dependencies separately. Native screenshots and the coverage
ledger remain the visual acceptance evidence; neither audit substitutes for it.

## Screenshot and starting-government repairs

Run `build_dashboard.py`, `build_events_ui.py`, `build_leaders.py`, and `build_retired_mechanics.py` to rebuild their committed output. Each accepts `--check`. Dashboard and event contracts retain engine control metadata; leader and retired-event manifests preserve identities and provenance. `Test-InterfaceRepairs.py` checks visibility, geometry, bindings, leader coverage, removal boundaries and source consistency.

`run_checks.py --engine GAME_ROOT` runs the static/offline acceptance suite and records commands, exit status and logs. It never launches the game. Native coverage is reported separately.
