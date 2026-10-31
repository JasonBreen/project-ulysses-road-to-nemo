# October 31 focus-screen repairs

The retained FCU screenshot `20261031091236_1.jpg` shows a three-line caption
spilling from its title area, exclusion markers crossing captions, visibly wavy
route tiles and a continuous-focus panel initially below the viewport. These
repairs address the authored geometry and initial placement. Native acceptance
remains separate.

The source is `tools/usea_expansion/build_ui.py`, `build_art.py` and the explicit
texture format metadata in `ui_assets.json`. The captured engine GUI contract is
preserved. Caption state textures record their original dimensions alongside the
deliberate 64px authored height; every joint/country variant uses that same height.

## Geometry and artwork

- The shipped ACBriefing16 font has an 18px line height. Node captions now reserve
  **54px**, with matching 64px state backgrounds. Local y44–98 text fits inside
  the y40–104 title frame. The normal 96px symbol ends at y40; node row pitch is
  **160px**, with 16px more initial grid padding to keep the first icon visible.
- Both exclusion offsets move to y−28. Together with the preserved 28px item
  offset, the 32px marker ends at y32, above the caption beginning at y44.
- Opposite-direction even-width Pillow lines produced a one-pixel thickness
  shift at each 16px tile centre. Cardinal arms now use aligned rectangles. Tests
  check edge ports, straight horizontal/vertical coverage and equal frame masks.
  Gold remains an authored state colour; its presence was not a vanilla fallback.
- Continuous-focus symbols use positive offsets, separate 64px caption frames and
  172px grid rows. The 770×456 panel contains a 352px clipped scrolling entries area.
  Its title, description, progress and rows have separate bounded regions.
- ERU and FCU opening trees put the panels at **(2016,16)** and **(2592,16)** respectively, clear of their rightmost
  focus. It fits the primary 3440×1440 view. Existing outer pan/scroll controls
  remain available at smaller views; native scrolling is still unverified.
- An inherited duplicated `GEB_north_gebadia_factories` localization key had
  replaced its short title with a paragraph. The second key is corrected to
  `_desc`; the original narrative is preserved.
- A second audit resolves explicit tree nodes, imported shared roots, shared
  descendants and relative-position anchors before comparing caption rectangles.
  It found seven inherited intersections. Belka's industrial preparation moves
  from resolved column 9 to 10. Its unclassified settlement moves from column 0
  to 4, carrying its relative legacy node with it. Sapin's six-focus recovery
  branch moves from column 60 to 70, beyond the inherited army branches. These
  are coordinate changes only; IDs, prerequisites, rewards and availability are
  preserved. All **25 trees / 950 resolved instances** now have zero intersecting
  caption rectangles, with no availability-based exceptions.

[Offline geometry/seam projection](evidence/package0-focus/focus-geometry-and-seams.png)
uses delivered textures and the actual bitmap-font glyphs. It is a review aid,
not an engine screenshot or evidence of runtime interaction.

## Reproduction and validation

```powershell
python -B tools/usea_expansion/build_ui.py
python -B tools/usea_expansion/build_art.py --focus-ui-only
python -B tools/usea_expansion/build_content.py
python -B tools/build_peace_we_inherit.py
python -B tools/usea_expansion/preview_focus_repairs.py
python -B tools/Test-FocusScreenRepairs.py
python -B tools/Test-UseaExpansion.py
```

The scoped artwork command preserves non-focus artwork and the complete asset
manifest. Add `--check` to its invocation to compare focus textures/metadata
without writing; the UI and content generators also support `--check`.

The focused suite measures **883 currently authored localized focus IDs**,
including both scripted Belkan title variants, using the shipped font advances.
All measured labels fit three lines at 147px. Missing/unresolved art or
localization consumers remain part of the broader Package 0 dependency inventory;
this is not a claim that every inherited focus binding or every screen is fixed.

Native verification must still check full focus states, selected/search results,
zoom, drag/pan, continuous-focus inner/outer scrolling, keyboard controls and the
longest captions at 3440×1440/1.0, 1920×1080/1.0 and 2560×1440/1.25. No desktop/game
launch, installation synchronization or save modification was performed here.
