# First-wave squadron artwork: source and offline review

The source set is complete: **24 recurring-character portrait masters, 48 narrative
illustrations and six independently composed loading screens**. All 78 selected
masters have distinct hashes and individual production/review records. The
original casts are supporting fiction and do not replace national leaders.

The source gallery is [artwork-gallery.html](artwork-gallery.html). Reproduce the
selected masters' packaging with Python 3.12 and Pillow 11.3.0:

```powershell
python -B tools/squadrons/build_art.py
python -B tools/squadrons/build_art.py --check
python -B tools/Test-SquadronArt.py
python -B tools/audit_visual_dependencies.py --strict-all
```

## Delivered textures and bindings

| Family | Masters | Delivered textures | Dimensions |
|---|---:|---:|---|
| Recurring cast | 24 | 24 portraits and 24 event cards | 156×210 and 200×160 |
| Narrative scenes | 48 | 48 event cards | 200×160 |
| Independent loading compositions | 6 | Six full screens and six picker images | 1920×1080 and 192×144 |
| Story categories | Procedural sources using established flags | 6 | 100×100 |
| Professional debrief spirit | Original procedural source | 1 | 75×75 |
| **Total** | **78 image masters** | **115 DDS textures / 109 sprite definitions** | One frame each |

The asset manifest records frame sizes, alpha extrema, source hash, provenance,
sprite binding and all 120 chapter-to-scene assignments. All full illustrations
and portrait cards use opaque navy containment to preserve the entire source.
Category and spirit silhouettes have intentional transparent outer corners.
Related scenes deliberately share a documented composition; opposing personal
conclusions use the quiet airfield composition without depicting a national
victory, defeat or destroyed strategic project.

## Visual review and correction

The retained source and packaged-texture contact sheets were inspected for
unreadable detail, accidental lettering, insignia, yellow overlay marks,
repeated generic compositions, portrait clipping and misleading outcomes.
Thirteen initial masters received narrow cleanup edits. Prompts and selected
outputs remain in their per-image records.

An additional exact 3440:1440 center-cover review identified a few clipped pixels
at the top of the Emmerian cargo tail. A built-in image-generation edit reframed
the aircraft smaller and lower within natural sky and terrain. The superseded
master/record remain under `tools/squadrons/revisions/`; the replacement is
selected in `sources/loading/emm_loading.png`. The complete cargo tail and
fighter now survive the offline crop. The review image is
[dds-review-emm-reframed-3440-ratio.png](dds-review-emm-reframed-3440-ratio.png).
Earlier `dds-review-*` contact sheets preserve the pre-correction inspection;
the selected-source gallery and packaged DDS files contain the corrected image.
Natural sunlight is part of the painted scenery; no artificial yellow watermark
or annotation is added.

## Checks and limits

The full package rebuilt successfully after the framing correction. All eight
artwork checks passed: all 78 provenance records, all 115 texture hashes and
frame/alpha bounds, all story consumers, chapter mapping, independent loading
bindings, exclusion from national leader bindings, sprite uniqueness and
byte-reproducible packaging/galleries. The separate runtime runner passed all
24 authored-script tests and generated-narrative consistency.

These are **source checks and offline image inspection**. The crop image is not
a screenshot from HOI4, and the artwork tests do not establish native font,
event-window, loading rotation, animation, UI-scale or GPU behavior. Native
testing remains paused. The three required display configurations, real game
loading/screens, story reading and save/reload remain acceptance gates. This
record makes no normal-installation or release-acceptance claim.
