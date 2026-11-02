# Pacific story original artwork

This component retains **26 new original selected masters** for the approved
Osean and Yuktobanian supporting stories: eight cast portraits, sixteen narrative
scenes and two independently composed loading screens. It preserves the existing
78 original masters and their 78 metadata files. The selected PNGs are exact
built-in `image_gen` outputs; none were painted over with Python or substituted
with contact sheets. Five superseded originals are retained under
`tools/squadrons/revisions`, outside the selected-source tree.

These people are original supporting fiction, **not national leaders** or
official Ace Combat characters. No national leader identity, flag, border,
military roster, chapter script or outcome owner is changed here. The separate
official AC8 collection is unaffected. Scenery is illustrative fiction, not
canonical mapped geography. Ages describe the initial story act; ending scenes
use experienced, back-facing adult silhouettes suitable for later conclusions.

The locked writer brief is [brief.md](brief.md). [plan.json](plan.json) contains
the exact selected prompts, stable file IDs, chapter/ending mappings and edit
references. Each PNG has a matching JSON recording its exact raw SHA-256,
dimensions, source output filename, generator, transparency/frame count,
individual visual review and packaging contract. Built-in generation is not
bit-for-bit reproducible; the retained original is the reproducible packaging
input. Prompt history and service-output receipts are preserved. One harmless
maintenance-scene request was rejected at output safety review and delivered no
image; the selected civilian component-inspection revision is explicitly recorded.

## Cast and scene coverage

| Host | Four original portrait references | Scene subjects |
| --- | --- | --- |
| OSE | Rhea Calder, Malik Renn, June Carver, Sana Ivers | Receiving shift; second frequency; returned component; chair kept free; account carried home; shared debrief; protected version; different departures |
| YUK | Irina Sokol, Anton Rask, Daria Vesnin, Lev Miren | Names on board; answer heard; work before return; duty not taken; practice handed on; next learner; signed silence; board left behind |

For each host, core slots 1–5 cover exactly the twenty approved chapters.
Slots **6 / 7 / 8 are exclusively trusted / compromised / fractured personal
endings**. They are distinct scenes and imply no national victory, peace,
defeat, occupation, death or compulsory historical result. The trusted
Yuktobanian scene contains the four cast-linked experienced adults and one
anonymous younger learner. Fractured scenes show two visibly separate routes.

## Packaging contracts and review

- **Portraits:** original 1122×1402 PNGs; use full-height contain at 156×210.
  Rhea's upper hair margin is tight, so do not trim additional source height.
- **Narrative:** original 1672×941 PNGs, except OSE 3 at 1672×940. Use full-source
  contain at 200×160, retaining every required person and action. The offline
  gallery also exposes conservative center-cover alternatives. OSE 6 and YUK 8
  must keep the full fit: a center crop discards an outer cast member or a
  separate departure and can change the personal meaning.
- **Loading:** the service returned two independent 1932×814 panoramas despite
  the requested 16:9 master framing. Retain those originals. Use the reviewed
  **center-cover** treatment for 1920×1080 and 3440:1440, rather than a generic
  contain path that adds large navy bars. Both ratios retain the principal
  workers, Osean vertical tail/service vehicle and Yuktobanian receiving approach.
  The partly framed parked machinery is background, not a specified live unit.
- All selected originals are one-frame, opaque, full-bleed artwork. Natural
  sunrise/workshop warmth and incidental safety paint are scenery; there are no
  yellow graphic watermarks or overlays. The targeted edits remove unintended
  emblems/pseudo-writing and correct the approved personal actions.

The [offline gallery](../../../docs/evidence/pacific-story-art/gallery.html)
links every original and crop preview. It uses the actual shipped ACBriefing16
bitmap atlas for labels; no operating-system font rasterization is involved.
PNG review reproduction compares dimensions and decoded RGBA pixels, while
selected originals and references retain exact raw binary hashes.

This is **source and offline crop evidence only**. The scripting/packaging owner
still has to bind these selected sources to the new campaigns, produce DDS
assets and review actual packaged cards. Native rendering, loading scaling,
display configurations and save/campaign acceptance remain untested while
desktop/game testing is paused. Existing national office leaders remain intact.

## Reproduce the source checks

Use Python 3.12 with Pillow **11.3.0**, matching CI. On this machine the pinned
interpreter is `G:\Project-Ulysses-Overhaul\.venv-ci\Scripts\python.exe`.
From the repository root:

```powershell
python -B tools/squadrons/pacific_art/audit.py
python -B tools/squadrons/pacific_art/test_art.py
python -B tools/squadrons/pacific_art/review.py
python -B tools/squadrons/pacific_art/review.py --check
# After committing the selected sources, verify raw Git blobs too:
python -B tools/squadrons/pacific_art/audit.py --git-blobs
```

The eleven focused tests include real selected-source validation, negative
hash/dimension/alpha/signature mutations, exact scene/ending coverage, retained
edit provenance, all 31 PNGs' effective Git binary attributes, inherited-source
preservation and compression-independent review checks. No test calls image
generation or opens a desktop application. The authoring/intake helpers are an
audit trail, not prerequisites for reproducing the delivered source checks.

Do not introduce a broad `tools/** text eol=lf` rule after image binary rules.
Such a filter can damage the PNG signature at Git commit time. This component
uses the existing `.py`, `.json`, `.md` text rules and `.png` binary rule, and
verifies committed PNG bytes against the selected files before handoff.
