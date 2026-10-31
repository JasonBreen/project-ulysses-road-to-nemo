# Anea original artwork and reproducible packaging

The Anea package extends the established navy-and-cyan briefing presentation with
**108 distinct focus compositions, eight original narrative illustrations and two
independent loading scenes**. There are 162 delivered DDS textures and 272 sprite
bindings, including national and shared policy art, decision-category/decision
aliases, loading thumbnails and reusable country/office cards.

Open [the portable artwork gallery](evidence/anea/artwork-gallery.html) or
[the focus contact sheet](evidence/anea/focus-contact-sheet.png) for review. The
contact sheet has captions for reviewers; game focus images contain no baked
captions or focus numbers.

## Sources and provenance

- `tools/anea/original_art.json` records the exact prompt, generated output name,
  committed source, source hash, dimensions, source layer and visual-review note
  for every raster master. All ten were created with the built-in `image_gen`
  tool on 30 October 2026. There is no CLI/API fallback dependency.
- Eight complete PNG masters are under `tools/anea/sources/events`; two separate
  PNG loading masters are under `tools/anea/sources/loading`. The loading scenes
  are independent compositions, rather than event crops.
- `tools/anea/build_art.py` and `focus_art.json` are the editable code-native
  sources and art direction for focus, policy and category imagery. They extend
  the repository's original geometry vocabulary and use the bundled DINish font
  under its existing OFL licence. They do not read installed-game textures.
- Office and country cards reuse the existing EMM/EVA flags unchanged. Their
  source hashes are recorded. No named leader, human portrait or new emblem is
  invented. The existing recruited office character IDs and portrait sprite
  names remain unchanged. The two existing
  portrait texture paths now select these Anea office cards through an explicit
  `presentation_source` in the starting-government manifest.

All generated scenes are **provisional gameplay illustrations**. They express
Emmerian civic capacity, shelter preparations, assistance and cooperation, and
Estovakian industrial strain, unfinished engineering, disrupted transport and
distribution reform. They do not establish a canonical city plan, capital
location, order of battle, individual or official historical image. The
unfinished engineering scene is deliberately incomplete and non-operational.

The ten masters were inspected for artificial yellow marks, logos, readable
captions, named portraits and UI overlays. No such overlays were retained. Natural
scene lights and practical safety rails are part of the depicted environment.

## Packaging and bindings

Run from the repository root with Python and Pillow installed:

```powershell
python -B tools/anea/build_art.py
python -B tools/anea/build_art.py --check
python -B tools/Test-AneaArt.py
python -B tools/usea_expansion/build_leaders.py --check
python -B tools/anea/build_briefs_ui.py --check
python -B tools/Test-AneaPresentation.py
```

The generator is independent of Dino's Mod Builder and all desktop software.
`--check` reconstructs outputs in memory and compares delivered DDS, manifests,
bindings and HTML bytes, without writing tracked files. Review contact-sheet PNGs
are compared as exact RGBA pixels because Pillow/zlib versions can encode the
same pixels with different compression streams. Regenerating does not contact an
image-generation service; all selected masters are committed.

`tools/anea/assets.json` records each texture's dimensions, frame count, frame
width, RGBA alpha extrema, SHA-256, role, sprite and source hashes. Delivered DDS
files use deterministic uncompressed RGBA8 encoding. All are single-frame
textures. Normal/shine focus sprite aliases deliberately share each focus's art;
the existing engine-bound briefing UI owns state/selection frames.

| Family | Delivered size | Binding contract |
| --- | --- | --- |
| Focuses | 96×96, transparent outer aperture | `GFX_ac_anea_focus_<focus ID>` and `_shine` |
| National spirits | 75×75 | `GFX_idea_ac_anea_idea_<policy ID>` |
| Shared spirits | 75×75 | `GFX_idea_ac_anea_<shared policy>` |
| Decision categories | 100×100 | `GFX_decision_category_ac_anea_recovery/relief` |
| Decision aliases | 100×100 | `GFX_decision_ac_anea_recovery/relief` |
| Country events | 200×160, opaque navy letterbox | `GFX_ac_anea_event_emm_1..4` / `eva_1..4` |
| Loading scenes | 1920×1080 | `ac_anea_emm` / `ac_anea_eva` background entries |
| Loading thumbnails | 192×144 | `GFX_ac_anea_emm_small` / `eva_small` |
| Reusable office cards | 156×210 | `GFX_ac_anea_office_emm/eva` |
| Reusable country cards | 200×160 | `GFX_ac_anea_country_emm/eva` |

Event and loading masters are contained, centred and resampled with Lanczos onto
opaque navy canvases. The original field of view is preserved, rather than
stretching or making country-event pictures overlap the repaired option column.
Related country narrative events may share one of their country's four scenes.

The standalone background-definition file adds only the two new scenes. It
preserves the existing loading rotation and the separately sourced AC8 collection.
Both 1991 bookmarks list Emmeria and Estovakia as minor countries, with three
actual foundation focus previews and full original country briefs. Their live
office portraits select the new authored office-card bytes while preserving the
existing character IDs, sprites and flag identity. `tools/Test-AneaPresentation.py`
checks these bindings and the absence of disaster foreknowledge in the 1991
briefs. The 200×160 country scene cards remain reusable presentation assets; no
unsupported per-country bookmark picture field is introduced.

## Country-selection narrative bounds

The engine-bound `history` text control now occupies **x35, y485, width380,
height145**, below the heading ending at y480 and above the navigation beginning
at y665. It uses the existing authored `ac_exp_standardtext_slider`, so long
country briefs remain accessible within that bounded area. The engine control
name, Aces12 font, text alignment, width, heading, portraits, country lists,
navigation and Return/Escape controls are preserved.

`tools/anea/briefing_control.json` records the original complete control from
`cf8fec41abe5080b1af66eb86189b35c7af522f6`. `build_briefs_ui.py` applies only the
explicit y-position, height and scrollbar changes and rejects unrecognised
control edits. Its ordinary build and `--check` need no installed game.

The historical frontend layout hash was **not refreshed**. The briefing
validator first requires the exact repaired node, its non-overlapping bounds and
required engine controls, then restores only that captured control for the
original whole-layout fingerprint. Regression tests prove that removing the
scrollbar, losing required controls or changing unrelated geometry fails.

This is a static bounds/control repair. Country-brief scrolling and complete
native display at the three target resolutions remain on the acceptance list.

## Verification and limits

The focused offline suite checks complete focus coverage, unique compositions,
transparent apertures, DDS headers/dimensions/frame contracts, source/output
hashes, idea and category token resolution, loading rotation dependencies,
established flag identity and packaging reproducibility. The full authored asset
audit and engine dependency audit remain integration gates.

Packaging was additionally checked with Pillow **11.3.0** installed into an
isolated ignored dependency directory, matching CI's pinned version. All
delivered textures, manifests and bindings were identical to those produced with
the local Pillow **11.0.0**. The contact-sheet PNG's compression stream differed,
while its RGBA pixels were identical; the review-art check therefore compares
pixels. The isolated install did not change system Python packages.

No native HOI4 rendering is claimed. Final scale, interaction and screenshot
acceptance must be recorded separately at the three planned display settings.
