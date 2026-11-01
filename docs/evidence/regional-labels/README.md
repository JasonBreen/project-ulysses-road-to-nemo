# Regional caption source acceptance

The final candidate at `31c8756a3dcf4132d33d7fa081fa8cb10359d6f3` passes all
eight commands in `final/results.json`, with payload digest
`d1f92a00f5d65ce462dea8c223286d05d61b3b498b07ea0f99d9d59455de2d86`.
It includes the current PR43/base-branch update and main `25ab6721`.

The explicit manifest repairs 206 state captions (204 Earth-template matches
and two empty entries), 37 already existing locality captions (13 template
matches and 24 absent entries), and four inherited school titles. Every new
name is provisional presentation; the technical IDs, point values and full
school descriptions are preserved. No physical geography file is written.

`missing-caption-findings.json` preserves the independent audit that exposed
the two empty state and 24 absent locality captions after the first template
pass. The final independent audit has zero unprotected caption problems. The
inherited `XXX` state607 and PLH/state171 remain under their existing source
requirements; complete map-label and global-conversion acceptance remain false.
This is a narrow source gate, not a wildcard exception for map presentation.

Focused coverage is eight tests with the installed primary reference, including
negative ownership/source/protected-scope mutations, both packaging commands,
actual point placements and raw primary-file/loose-English checks. Seven source
tests execute in CI, with one explicit installed-reference skip. The remaining
commands cover actual focus/decision typography, screenshot/privacy regressions,
registry, strict authored assets and complete static/reference validation with
the verified immutable baseline payload.

`caption-review.html` is a searchable before/after source table, not an engine
map or screenshot. Native text substitution, map placement/zoom, three display
configurations and save/reload remain untested. Normal installation, desktop,
playsets and saves were untouched.
