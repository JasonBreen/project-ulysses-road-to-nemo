# Country-selection briefing repair — 24 October 2026

The country-selection screen inherited parchment panels, metal framing, brass
statistics badges and WWII focus/idea illustrations. The repair replaces the
screen's chrome with original navy panels, cyan rules, flat controls and light
ACES text. It also styles the adjacent scenario selector. Implementation base:
verified remote main `1c36a33`.

## Delivered artwork and provenance

| Family | Implementation | Source layer |
| --- | --- | --- |
| Country-selection background | Same 1225×1033 extent and existing panel/control positions; new navy history, information and focus panels | Original authored UI artwork |
| Scenario selector and bookmark frame | New panel and light text, preserving the existing bookmark layout | Original authored UI artwork |
| Buttons, portrait overlay and flag frames | Flat outlines; transparent flag apertures preserve visibility | Original authored UI artwork |
| Bookmark national spirits and focuses | 15 idea bindings and 15 focus bindings across BLK, OSE, UST, SAP and GEB; purpose-drawn pictograms | Original authored UI artwork, existing gameplay meanings |
| Engine-selected ideology badges | Six exact VFS path overrides; same dimensions as the corresponding engine sprites | Original authored UI artwork; reference dimensions only |
| Map statistics frame | Noninteractive overlay covers the baked metal/brass frame and badges; six transparent value apertures retain the original figures | Original authored UI artwork over inherited mod maps |
| Maps, flags, portraits, country-specific party insignia | Existing archive artwork retained | Inherited mod content; no new canon claim |

No installed-game image pixels or fonts are build inputs. No new lore, biographies,
statistics, borders or campaign effects are introduced. The five map PNGs remain
byte-identical: `tools/frontend_briefing/maps.json` records their hashes. Their
embedded statistics are still static bookmark illustrations, not live force counts.

The map overlay deliberately does **not** repaint or regenerate geography. The
old statistics art remains inside the inherited PNGs underneath the overlay; the
original numeric areas, including their existing backdrops, remain visible.

`tools/frontend_briefing/build.py` reproducibly creates 44 legacy 32-bit BGRA DDS
textures with alpha using Pillow. `assets.json` records dimensions and frame counts.
`interface/ac_frontend_briefing.gfx` defines 59 sprites. The common idea/focus
changes replace only artwork bindings; costs, prerequisites, identifiers and
effects are unchanged. These particular bindings also affect their normal in-game
idea/focus appearances.

The existing 1.19 GUI restoration tool now reapplies the styling through
`tools/frontend_briefing/style_gui.py`. Styling is idempotent. All original control
names, geometry, orientations and compatibility stubs are preserved; the sole
additional control is the noninteractive map-statistics overlay.

## Static evidence

Run from the repository root:

```powershell
python tools/frontend_briefing/validate.py
./tools/Test-UlyssesStatic.ps1 -ModRoot "$PWD/mod/2985041246" -ReferenceGameRoot $env:ULYSSES_GAME_ROOT -BaselineRoot $env:ULYSSES_BASELINE_ROOT
./tools/Test-UlyssesEconomy.ps1
```

| Check | Result |
| --- | --- |
| Briefing contract | 44 BGRA textures, 59 sprites, 30 bookmark bindings pass; original layout fingerprint preserved |
| Regression guards | Flag/value apertures remain transparent; dark-panel fonts are light; map hashes unchanged; engine-selected badge paths are supplied |
| GUI restoration | Applying styling twice is identical; styling the pre-repair GUI reproduces the checked-in control tree |
| Map/campaign suite | Pass, zero errors; two inherited map warnings (placeholder ownership and strategic regions) |
| Reference audit | 2,011 warnings before and after; warning lists identical after normalizing checkout paths; zero missing focus references, duplicate events, malformed events or missing owned events |
| Technology audit | One inherited warning; unchanged campaign horizon |
| Delivered-asset audit | 2,876 mod files; zero new or path-independent vanilla matches; four inherited empty/config map matches |
| Economy | All 27 tests pass |
| Source/payload parity | All 2,876 payload files match source SHA-256; no missing or extra files |

CI runs the dependency-free briefing validator alongside existing static checks.
Pillow is needed only to rebuild artwork, not to play or validate the delivered DDSs.

## Native evidence and limits

Native testing was separately authorized by the user. The final visible test used
HOI4 Operation Postern 1.19.3.0.c01a, checksum `cba9`, DirectX 11, 3440×1440 and GUI
scale 1.0. Runtime logs identify one active mod, Project Ulysses: Continuation.

| Screen/action | Native observation |
| --- | --- |
| Scenario selector | Navy panel, readable light text, preserved bookmark image and working selection |
| Belka | Parchment and ornate framing removed from the displayed panel; flat ideology glyph, new idea/focus icons and all six original statistics visible |
| Osea, Ustio, Sapin, Gebet | Each flag selects the correct country, map highlight, history, leader, government, idea/focus glyphs and statistics |
| Flag frames | Corrected after first-run inspection; all five flags visible on the final build |
| Map overlay | Brass badges covered on all five maps without hiding the figures or intercepting clicks |
| Navigation | Country-selection Back returns to scenario selection; Select Country reaches the Belkan map lobby; lobby Back returns to main menu |
| Shutdown | Quit closes the copied engine; no game process remains |

The native screenshot and full local logs are retained in the disposable visual
test evidence folder; proprietary engine files, normal saves and user configuration
backups are not committed. Native observations cover this screen repair, not the
aftermath campaign acceptance matrix.

**Remaining visual coverage:** other resolutions/UI scales, multiplayer, load/save
dialogs and full in-game screens were not accepted in this pass. The lobby still
has legacy top/bottom bars, difficulty controls, pie-chart decoration and Start
ornamentation. A pre-existing raw `COUNTRY_SELECTION_CHARACTER_DESC_NAME` hover key
also remains. Country-specific archive insignia are retained. This change is not
a claim of zero reachable vanilla imagery throughout the game; the broader issue
#4/#8 visual/runtime work remains open.

## Isolation and preservation

The test used a separate profile/payload on G: and the existing physical copied
engine from the earlier isolated playtest. The normal launcher/playset was never
selected or edited, and no normal save was loaded. Autosave and cloud saving were
disabled in the disposable profile. The copied engine's previous profile routing
was backed up and restored afterward; the earlier aftermath worktree and payload
were preserved.

An initial hidden diagnostic launch with a command-line userdir override wrote
startup logs to the normal directory. It was stopped before gameplay. Unlike the
earlier campaign session, all original normal logs had been backed up: diagnostic
logs were retained separately and the 20 originals were restored byte-for-byte.
The final visible launch omitted the command-line override and used the copied
engine's `userdir.txt` plus copied launcher data path, with runtime logs under the
disposable profile.

Final SHA-256 verification covers **81 normal saves, eight configuration/launcher
files and 20 restored log files**. There are no added/removed normal saves and no
installed-engine `userdir.txt`. The local preservation manifest records each file;
it is not published because it contains user save names and system paths.
