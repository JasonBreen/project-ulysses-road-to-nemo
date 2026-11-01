# Offline fiscal interface review

Open [ui-review.html](ui-review.html) for all five page reconstructions and the
bounds findings. These are offline review artifacts, not HOI4 screenshots or a
replacement interface. Native rendering, scaling, interaction, tooltips and
save serialization remain untested.

From the repository root, using the project Python environment with Pillow:

```powershell
python -B tools/economy_v2/render_review.py
python -B tools/economy_v2/render_review.py --check
```

The first command writes the five labelled PNGs, gallery and audit record. The
second reproduces them in memory and compares the PNG pixels and text records
without rewriting anything. Either command exits nonzero on missing glyphs,
unresolved variables, invalid sprite frames, out-of-window controls or detected
text overflow. `--check` also fails on stale evidence. Input hashes normalize
CRLF to LF for text files; binary DDS hashes retain their exact bytes.

The renderer reads the delivered GUI positions and control sizes, sprite
bindings and frame counts, ACBriefing bitmap-font definitions and atlas,
English localization, scripted visibility/enablement conditions and graph
frame properties. It does not move controls, shrink text or invent a selected
tab appearance to make the reconstruction fit. Four-frame buttons use the
normal first frame or disabled fourth frame; engine state mapping still needs
native verification. Word wrapping follows delivered glyph advances and is an
offline approximation of engine line breaking.

The illustrative Emmerian sample supplies explicit factory/force observations
to the actual-script `World` interpreter. Financial formulas remain in the
shipped effects. It runs twelve scheduled settlements from February 1991 to
January 1992, retains their variables, performs a copied-state startup after the
sixth settlement, then authorizes replacement funding through the public
effect. The copied state is not a native save file. All observations, actions,
monthly values, final variables, visible controls, substituted text, selected
graph frames, bounds findings and source fingerprints are retained in
[ui-review-report.json](ui-review-report.json). The sample is fictional gameplay
calibration and does not establish natural campaign balance or a starting OOB.
