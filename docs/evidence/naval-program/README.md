# Naval source and offline evidence

No native game, designer, mission, AI progression or save/reload was exercised. The installed 1.19.4.1 game was used only as a read-only technical reference.

- `art-index.html` presents the original equipment, research/component, bare blueprint and cropped normal/highlight-layer galleries. Editable SVGs and packaging provenance are under `tools/naval_program`.
- `research-page.png/json` reconstructs all 24 actual new research cards with shipped geometry, localization, DDS and briefing font metrics. Three display cases and 20 actual designer consumers are recorded separately.
- `designer-defaults.png` composites all 20 bare top views and their actual selected category layers at the actual shipped control coordinates. It is labelled offline and is not a native screenshot.
- `research-consumers.json` retains requested common research/AIR/NAVAL template and blueprint dependency closure. Its requested-screen gates are distinct from the wider inherited presentation inventory and installed-reference parse backlog.
- `results.json` and named logs retain the bounded source gates. The owning `capabilities.json` records 12 date/MTG cases, 16 independent DLC profiles, physical/stat/material/classification parity, reference detection margins and retained older surfaces.
- `source-receipt.json`, when present, identifies the exact tested commit/source fingerprint. An evidence-only follow-up commit does not change that tested payload.

Reproduce with Python 3.12 and `Pillow==11.3.0`, from the repository root:

```powershell
python -B tools/naval_program/build.py --check
python -B tools/naval_program/build_art.py --check
python -B tools/naval_program/build_ui.py --check
python -B tools/naval_program/audit.py --check
python -B tools/naval_program/render_review.py --check
python -B tools/naval_program/test_naval.py
python -B tools/naval_program/run_checks.py --engine 'G:/steamlbirary/steamapps/common/Hearts of Iron IV' --core
```

The two existing briefing FNT files must match their committed LF bytes under `.gitattributes`; no glyph/pixel normalization is performed. PNG checks require identical dimensions/decoded RGBA, while DDS and authored sources retain exact-byte checks. Native testing, normal-install synchronization and release acceptance remain separate.
