# Linux artwork-gallery correction

The first Linux `conventional-land` job on PR #46 failed at review commit
`4e6fc846f267585799c81873070c96c8f9622e4b` in
`test_generators_and_visual_artifacts_are_byte_reproducible`:

```
Stale land art: docs/evidence/land-program/asset-gallery.png
```

Run: <https://github.com/JasonBreen/project-ulysses-road-to-nemo/actions/runs/41271178065>.
The preceding 106 delivered DDS comparisons passed. The gallery used
`ImageFont.truetype`, whose rasterization depends on the platform FreeType
build. It now composes its captions from the delivered `ACBriefing16` glyph
atlas, matching the research-page reconstruction. Review PNG consistency checks
compare exact dimensions and decoded RGBA pixels; DDS, SVG, GFX and manifest
outputs retain exact-byte checks. Different PNG compression cannot hide a
different pixel or dimension.

Repackaging changed only the two offline gallery PNGs and the generator-source
hash in the asset manifest. All delivered mod files remain identical to the
ten-gate source payload documented in `caption-parent/results.json`. All 22
focused LAND tests passed again with the read-only installed primary after the
correction. Exact-head Linux and Windows CI must still be checked after pushing
the correction; the original failed run remains visible as evidence.

This fixes review-artifact reproducibility. It supplies no native rendering,
designer, AI, save/reload or release acceptance.
