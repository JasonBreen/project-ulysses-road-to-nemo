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

## Continuous-focus panel on every tree (5 November 2026)

A re-measurement after Wave F1 found the panel overlapping real nodes on four
trees whose generators still used fixed positions, and one tree with no panel
declared. `tools/usea_expansion/focus_layout.py` now owns the geometry: the panel
is 770×456 (`continuous_focus_window`), the pitch 96×160 (`focus_spacing`) and the
node footprint the union of the centred icon, caption frame, glows, historical
marker and viewing-flag frame, **x −12 to 177, y −56 to 104** from the node origin.
The placement rule puts the panel top-aligned at y 16 and
`(rightmost x of the nodes whose footprint meets the band y 16–472 + 3) × 96`
across, so rows appended later below never move it.

| Tree | File | Before | Overlapping nodes before | After | Clearance |
| --- | --- | --- | ---: | --- | ---: |
| `ac_ucw_eru_tree` | `ERU.txt` | 1200, 1700 | 3 | 2592, 16 | 111 px |
| `ac_ucw_fcu_tree` | `FCU.txt` | 1300, 1700 | 3 | 2592, 16 | 111 px |
| `ac_anea_emm_tree` | `EMM.txt` | 50, 2100 | 6 | 2592, 16 | 111 px |
| `ac_anea_eva_tree` | `EVA.txt` | 50, 2100 | 6 | 2592, 16 | 111 px |
| `generic_focus` | `generic.txt` | none declared | — | 2400, 16 | 111 px |

`tools/build_continental_war.py` and `tools/anea/build_campaign.py` call the rule;
`generic.txt` (hand maintained) carries the position with a comment naming the
rule. The other 29 trees already cleared every node and keep their generators'
own rules. `test_every_tree_declares_a_panel_that_clears_every_node` checks all
34 trees: a declared panel, no intersection with any resolved node footprint, at
least 32 px from the nearest node in its band, and the five trees above equal to
the rule. EMM and EVA, like the two opening trees, fit the 3440-px primary view
(50 + 2592 + 770 = 3412).

[Layout review](evidence/package0-focus/index.html) (`layout.json`, five
quarter-scale images; nodes overlapped before in red, the old panel outlined in
red, the new one in cyan) is written by
`python -B tools/usea_expansion/preview_focus_repairs.py --layouts` and checked
with `--check` (JSON and HTML byte for byte, PNGs by size and RGBA). Offline
geometry only; native placement is still to be confirmed (#8).

[Offline geometry/seam projection](evidence/package0-focus/focus-geometry-and-seams.png)
uses delivered textures and the actual bitmap-font glyphs. It is a review aid,
not an engine screenshot or evidence of runtime interaction.

## Every focus visible; the 150-focus floor (6 November 2026)

`tools/Test-FocusVisibility.py` is the definition of done for the programme that
gives every country at least 150 focuses (the national-depth programme; its
compiler, `tools/national_depth/`, is the next step).
It runs in CI after the layout review. For every tree it requires:

- every resolved node at x, y >= 0;
- no two captions closer than two columns on a row;
- a localised title and description for every focus outside the base game's generic tree;
- an icon sprite defined in the mod with an existing texture;
- no `allow_branch` other than tag-only gates on shared imports and three reviewed
  Belkan chain gates (`BLK_party_disagreements`, `BLK_nationalism_unleashed`,
  `BLK_taking_off_the_kid_gloves`);
- `initial_show_position` naming a focus in its tree.

Size is a ratchet. For 68 countries (61 that own land on 1 January 1991 except
`PLH`, plus the release tags REC, SBK, AWW, SHI, REL, SER, TER), the test
evaluates each tree's `country` weights on the start date and counts every tree
the country can be on, with imports.
[`baseline.json`](evidence/focus-visibility/baseline.json) records each tree's
floor. A floor never falls (`--record` refuses), waves raise it, and the target
is 150 (`--report` prints progress).

**Repairs made with the test:**

| Defect | Repair (mod provenance) |
| --- | --- |
| 18 nodes of `ustio_democracy` and 10 of `ustio_non_ali` resolved left of x = 0 | The four absolute Ustio roots in `UST_shared.txt` moved 8 columns right (`UST_start`, `UST_deal`, `UST_army_debate`, `UST_no_step_on_our_land`, whose relative anchor is commented out). Relative coordinates are unchanged, so the repaired `x = -1` pin in `Test-UstioContinuity.py` still holds |
| 4 nodes of `ac_belkan_postwar` left of x = 0 | `ac_postwar_reconstruction` moved 4 columns right; the unclassified-outcome pins became (8,3) and (8,4) |
| `BLK_party_disagreements` named an undefined sprite (`...won_elections-convene_the_parliament`) | Points to the defined `GFX_goal_BLK_dlp_won_elections` |
| 15 inherited AWW focuses had no title or description | `ac_focus_text_repairs_l_english.yml` states what each focus does, read from its script; no history added |

The baseline recorded at this point (`--report`): 68 countries and 35 trees,
2 of them at 150. That leaves 2,802 focuses to add to existing trees, and 46
countries still start on the generic or regional tree.

## Reproduction and validation

```powershell
python -B tools/usea_expansion/build_ui.py
python -B tools/usea_expansion/build_art.py --focus-ui-only
python -B tools/usea_expansion/build_content.py
python -B tools/build_peace_we_inherit.py
python -B tools/usea_expansion/preview_focus_repairs.py
python -B tools/usea_expansion/preview_focus_repairs.py --check
python -B tools/Test-FocusScreenRepairs.py
python -B tools/Test-FocusVisibility.py
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
