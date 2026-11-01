# Naval source and offline evidence

No native game, designer, mission, AI progression or save/reload was exercised. The installed 1.19.4.1 game was used only as a read-only technical reference.

The final exact-source run passed **all 19 groups** against code commit `38dc1f8fc5bdca55d75bc869ab37f174a0aff492`. Before and after the run, the shared source owner measured **7,883 tracked inputs** outside review evidence with identical SHA-256 `196c8fb3621b70c69f8063cf0296484d4e1685324cd461d21100b53c13e8e751`. The focused naval suite passed 27 tests; AIR passed 31, LAND 23, research fonts 10, the fiscal owner 27, force upkeep 9 and source-identity fixtures 4. All 61 current starts and 244 selected base cases passed their integrated coverage gate.

The authored asset `--strict-all` gate checked 7,447 sprite definitions with zero missing references. Requested common research, AIR/NAVAL templates and aircraft/ship blueprint screens have zero ownership/dependency failures. The wider inventory retains 12 unrelated installed-reference parse failures and other inherited presentation backlog. Full static validation exits successfully with its existing two geography warnings, reference warnings and one technology warning; it is not a warning-free or whole-surface native acceptance claim.

All 24 research compositions, 20 ship views, 64 component icons, 20 bare top views, 142 normal/highlight layers and 20 actual default-category composites were inspected offline. The research reconstruction has zero bounds/text findings at all three required display geometries. The original navy/cyan/light masters contain no yellow pixels or watermarks. Their native state selection, interpolation, designer operation and rendering remain untested.

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
