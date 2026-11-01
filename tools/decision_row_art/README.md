# Bounded decision-row presentation repair

This standalone source/offline repair is based on `78e573625ec2ad9265b6aca348966866a857693e`. It retains country content, gameplay conditions, category illustrations, national spirits, project artwork and existing sprite IDs.

The previous row aliases pointed to100×100 Anea/institution category icons or60×60 strategic-project idea icons. The standard row's centered icon at(30,19) exceeded the row top/left and entered the title column beginning atx62. Expanding all three Belkan garrison decisions' repeated conditional `icon={key=...}` blocks also exposed four40×40 icons, whose standard centered placement crossed the row top by one pixel. Their fallback icon must be inspected too.

The repair authors **13 separate26×29 RGBA row compositions**:

| Owner | Compact subjects | Stable row bindings | Large art |
|---|---|---|---|
| Anea |Recovery, relief |`GFX_decision_ac_anea_recovery`, `GFX_decision_ac_anea_relief` |100×100 category art and category/full aliases retained |
| Institutions |Assembly |`GFX_decision_ac_pol_institutions` |100×100 category icon and all mandate/idea art retained |
| Strategic projects |Excalibur, V2, Stonehenge, Arkbird, Megalith, Rhongomyniad |Existing six `GFX_decision_ac_sp_*` IDs |Original project/reward/idea/category bindings retained |
| Belkan garrisons |None/low/mid/big control |Existing four `GFX_decision_BLK_garrison_control_*` IDs |Old40×40 textures retained; new compositions stamp the existing BLK flag |

The editable master is `geometry.py`, drawn specifically for row resolution rather than reducing complex category art. The original navy/cyan/light palette, deliberate transparency and no baked lettering remain consistent. Garrison stamps use the established `gfx/flags/BLK.tga`; the new manifest records its exact source hash. No installed or external image pixels are imported. The two original Anea compositions are owned by `tools/anea/build_art.py`, the institutional row by `tools/institutions/build_art.py`, and the six project/four garrison rows by this directory's `build.py`.

Each delivered DDS has26×29pixels, one26pixel-wide frame, and alpha extrema0–255. The manifests record exact dimensions, alpha, frame counts, sprite bindings, SHA256 and source/provenance. `source/preserved_assets.json` protects all263 previously shipped Anea/institution textures. `source/before_bindings.json` pins the former13row-source textures as well. Original illustrations, office cards and flag assets are unchanged. The captured project/garrison GFX sources allow the compiler to reproduce narrow row-path changes while retaining every unrelated sprite definition.

The three previously untranslated garrison actions now have English titles/descriptions using their inherited Hugelse, Hoffnung and Friede names. Descriptions reflect the actual existing25political-power cost,14-day period and control increase of one level up to three. The two directly referenced raw-key tooltips are translated too. These additions are **mod-provenance presentation**, not new canonical history or a political rewrite.

## Consumer-bound verification

`bounds.py` enumerates actual authored decision definitions through the existing effective dependency reader. It expands every repeated conditional key and conservative default; it loads each selected GFX definition and real DDS rather than trusting asset-manifest dimensions. Frame width comes from the actual DDS width divided by the actual GFX frame count. The actual GUI `scale` and `centerposition` are applied independently for all three shipped templates:

| Template | Icon position | Anchor |26×29source rectangle |
|---|---|---|---|
| `decision_item` |(30,19) |Centered |(17,4.5,26,29) |
| `targeted_decision_item` |(15,0) |Top-left |(15,0,26,29) |
| `timed_decision_item` |(32,20) |Centered |(19,5.5,26,29) |

All rectangles remain inside the104pixel row height and before the title column atx62. The conservative common size limit from these controls is47×38. The repair uses26×29 to retain margins. No GUI geometry, font, flag control, button, timer, row template or interaction binding is changed.

The full current scan covers **549active authored icon variants**, including conditional alternatives and runtime defaults. **67active variants** previously violated at least one source bound, and none do after the repair. The initial simple inventory counted61oversized scalar row references; six Anea entries in that count are statically retired, while full expansion adds12Belkan conditional variants. Those six retired entries still share the repaired Anea bindings. Category-header defaults are classified by their actual `common/decisions/categories/` source path and are not mistaken for row icons.

`Test-DecisionUI.py` includes actual-source positive tests and negative fixtures. A real100×100 DDS must fail all three real row layouts. A104×29strip with four frames passes because each frame is26×29; changing the actual standard GUI scale to2 makes it fail. An oversized conditional alternative cannot evade the check even when its sample trigger is false. The three garrison title/description/tooltip keys, BOM, source cost/duration and actual font-wrapped title bounds are tested explicitly.

## Reproduction and evidence

Use Python3.12 with `Pillow==11.3.0`, matching CI:

```powershell
python -B tools/anea/build_art.py
python -B tools/institutions/build_art.py
python -B tools/decision_row_art/build.py
python -B tools/decision_row_art/render_review.py
python -B tools/decision_row_art/run_checks.py --engine 'G:/steamlbirary/steamapps/common/Hearts of Iron IV'
```

Every art/review generator supports `--check`. The checks read the installed reference only for effective dependencies/static contracts; they never launch HOI4. The evidence runner executes at most two source checks concurrently. Results and logs are retained in `docs/evidence/decision-rows`.

The [offline gallery](../../docs/evidence/decision-rows/index.html) reconstructs before/after bindings using actual row backgrounds, frame metadata, GUI positions, current font atlases and localized titles. Its before garrison samples retain their captured missing English key behavior; after samples show the restored titles. Bounding lines and labels are review annotations, never delivered asset markings. Half-pixel positioning is a source calculation, not a claim about native rasterization. This gallery is not a native screenshot or a new product UI.

## Remaining acceptance and inherited behavior

Native testing remains paused. Verify the actual standard, targeted, timed and map-only displays, conditional control levels, hover states, flag substitutions, category/idea/project screens and scrolling at3440×1440/1.0,1920×1080/1.0 and2560×1440/1.25 when testing is separately resumed. Source bounds, asset checks and an effective dependency gate cannot establish native visibility, input or scaling.

The existing garrison actions retain their inherited `SPR_*` visibility/cooldown flags, map-only mode and existing legacy variable syntax. These are explicitly recorded gameplay/integration gaps outside this row-art repair; translating their presentation does not certify that their political path is reachable or correct. The normal installation, saves and other worktrees remain untouched.
