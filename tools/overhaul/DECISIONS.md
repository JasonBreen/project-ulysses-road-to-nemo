# Decision presentation and effective-consumer audit

This Package 0 source repair replaces the inherited decision screen with navy
panels, cyan structure, light text and restrained gold selection accents. It
does not establish native rendering, input or campaign acceptance.

The captured `decisions_contract.json` contains engine control/geometry and
texture-format metadata from the installed 1.19.4.1 reference. No engine image,
font, shader source or audio bytes are imported. Original artwork is reproducible
geometry in `build_decisions_ui.py`; `decisions_assets.json` records each DDS,
dimensions, frame count, alpha range, hash and sprite binding. Existing authored
ACBriefing fonts retain their own provenance and packaging sources.

## Reproduce and check

From the repository root, with Python 3 and Pillow:

```powershell
python -B tools/overhaul/build_decisions_ui.py
python -B tools/overhaul/build_decisions_ui.py --check
python -B tools/Test-DecisionUI.py
python -B tools/audit_visual_dependencies.py --strict-all
```

Ordinary generation and all twelve focused tests need no installed game. The
explicit developer-only `--capture-contract <engine>` command refreshes format
metadata; it is not part of a normal reproducible build. Capture normalizes old
`.lua` effect aliases to existing `.shader` services without copying their code.

All required decision, targeted/timed decision, report, category, collapse,
tracking, popup-preference, custom-icon and map-locator control names remain.
Escape and the engine's viewport-sized scrolling protocol remain. Decision rows
reserve separate bounds for two-line titles, cost, timer, tracking and action;
progress bars sit below the text. The missing inherited category separator is
explicitly supplied. Fractional inherited strip widths are rounded up to complete
integer frames in the authored sheets.

`countrydecisionview.gfx` owns the chrome. The generated `decisions.gfx` shadows
the engine's runtime icon family so engine-selected defaults cannot fall back
to WWII artwork. It also binds inherited unresolved XXX/placeholder/mission
tokens. These are original semantic briefing glyphs and compatibility defaults,
not a claim that every old decision now has a unique finished illustration.

## Installed-reference dependency inventory

```powershell
python -B tools/overhaul/audit_consumers.py <engine> --gate-decisions --output tools/overhaul/consumer_audit.json
```

The audit applies same-path overrides, case-insensitive resource paths and
descriptor `replace_path` isolation. It follows effective scrollbar templates,
bitmap-font files, direct GUI sprites, actual authored decision/category icons,
model clone/mesh/attachment/animation dependencies, MIO parents/icons, agency
logos, portraits and audio consumers. It also inventories authored focus/event/
idea/technology image consumers and scripted-GUI window/click/list bindings.
Cross-file conflicting definitions and parse failures remain visible. Statically
retired decisions are listed with their exclusion reason.

The decision exit gate covers loose installed-engine plus mod graphics, fonts
and templates only. It does not certify sound replacement, native flag binding,
visibility, input, z-order or the rest of the conversion. `--screen <filename>`
adds an inventory; `--gate-screen <filename>` additionally gates that complete
screen. Runtime image defaults and engine-generated culture/entity conventions
that cannot be fully expanded are labeled uninspected.

Installed DLC ZIP paths and sizes are inventoried, but their contents are
**uninspected**. Installation does not prove ownership, activation or runtime
reachability. A clean loose-file screen gate cannot certify full DLC closure.

`mod_resolved` means a dependency resolves to mod-local files. It does not prove
that those files are original, licensed, visually appropriate or engine-tested.
Asset hash/provenance checks and approved native testing remain separate gates.
The whole-mod backlog, including inherited engine portraits, agency/MIO art,
models, sound and unresolved references, is reported honestly and does not
silently become a passing full-conversion certificate.
