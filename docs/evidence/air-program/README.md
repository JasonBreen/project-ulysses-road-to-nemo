# Aviation source and offline review evidence

All artifacts here are source checks or offline reconstructions. HOI4 was not launched. Native designer, mission, production, natural AI and save/reload behavior remain untested.

- Open `art-index.html` for the original equipment, component/research and 508×248 blueprint galleries. All 20 aircraft, 24 research compositions, 32 module subjects and 16 blueprint crops were reviewed offline for legibility, repeated generic compositions, clipping and unwanted yellow marks.
- `research-page.png` reconstructs the shipped Aviation Systems page using actual GUI coordinates, DDS, English localization and authored ACBriefing BMFont glyph metrics. `research-page.json` records all 24 card rectangles, 16 actual blueprint bindings and three display geometries, with zero text/bounds findings.
- `research-consumers.json` is the installed-reference effective dependency audit for the requested common research screen, new card templates and blueprint controls. Its requested-screen result must be read separately from wider inherited parse/presentation backlog.
- `results.json` and named text logs retain 17 passing source-check groups. The focused AIR suite has 31 tests; LAND has 22, research fonts 10, the actual fiscal owner 27 and force upkeep 9. Current-start coverage verifies 50 World Starts, five World Foundation, two Anea and four Legacy owners: 61 countries and 244 selected base cases. The capability worksheet lives in `tools/air_program/capabilities.json`; primary captures are loose-file contracts, not native mission evidence.

The requested research/card/blueprint ownership gates have zero failures. The wider dependency inventory still records 12 unrelated installed-reference parse failures and other inherited presentation dependencies; this packet does not claim the whole-surface presentation gate. Full static validation exits successfully with its two geography placeholder warnings, reference warnings and one technology warning retained in `static.txt`. Existing `XXX` geography and state 171 are unchanged.

The composed font measurement records 301 protected inherited font assignments and 329 total current assignments. Source ink/bounds findings are zero. The two existing ACBriefing FNT files must have their exact committed LF bytes under the reviewed `.gitattributes`; DDS hashes remain raw. Neither glyph metrics nor pixels are changed by this AIR packet.

Reproduce from the repository root using Python 3.12 and `Pillow==11.3.0`:

```powershell
python -B tools/air_program/build_art.py --check
python -B tools/air_program/build_ui.py --check
python -B tools/air_program/render_review.py --check
python -B tools/air_program/test_air.py
python -B tools/air_program/run_checks.py --engine 'G:/steamlbirary/steamapps/common/Hearts of Iron IV' --core
```

The full contract, provenance and remaining native matrix are in `tools/air_program/README.md`. Editable original sources and manifest hashes are retained alongside the delivered DDS package. No normal installation or user save is changed by these commands.
