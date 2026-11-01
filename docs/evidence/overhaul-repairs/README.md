# Overhaul Package 0 evidence

This directory records the privacy and screenshot-repair package based on main
`3810d1a`, retaining the approval baseline `1f04456`. It does not establish native acceptance.

## Before evidence

The three October 31 images are user-provided Steam captures:

- `before/20261031091134_1.jpg`: blank country-selection map after the earlier
  scrolling-history repair clipped the oversized inline image.
- `before/20261031091236_1.jpg`: FCU caption/exclusion collisions, uneven link
  tiles and an initially clipped continuous-focus panel.
- `before/20261031091241_1.jpg`: inherited decisions chrome and template labels.

The screenshot archive and normal game profile were read only. No game process,
desktop input, display setting, playset, save or installed mod was changed.

## Source previews

`overview.png` is a **static generated texture preview**, not an in-game after
capture. Its geometry and starting state ownership come from the editable mod.
The GUI supplies localized title/note controls and renders this layer behind
country controls. Selected-country information remains engine-owned. There are
no fabricated dynamic statistics.

The old five country map PNGs remain preserved as inherited assets. The five
oversized inline prefixes were removed without shortening narrative prose.

## Verification boundary

The retained `validation/static-results.json` records **30 passing check groups**
with their commands and logs. The focused suites include seven overview/fiscal/
label regressions, sixteen decision/dependency tests and nine focus-screen tests.
The focus geometry check resolves 25 trees and 950 focus instances, with zero
caption intersections after seven inherited placement repairs. All 883 currently
localized focus IDs fit the measured three-line caption contract.

The strict authored-asset gate reports zero missing assets. The separate
no-imported-vanilla check reports zero new and zero path-independent vanilla
matches, retaining four inherited technical map-file matches. The effective
decision screen resolves its direct and runtime-selected graphic dependencies;
the broader consumer backlog and uninspected DLC archives remain explicit in
`tools/overhaul/consumer_audit.json`.

The candidate payload is recorded by hash in `validation/candidate-payload.json`.
It is a source candidate, not a copy installed or tested in HOI4.

## PR32 review corrections

The review payload distinguishes filled and remaining decision-progress artwork,
inventories every repeated conditional icon key and the unproven runtime default,
runs the four repair checks as independent CI steps, and expands decision rows
to 104 pixels with 356×54 title bounds. Costs/timers sit beneath the title and
progress beneath both. The regression measures all known decision names,
literal country/state-name variations and year substitutions from 1991 through
2065 with the actual shipped font advances. These corrections preserve the
engine-bound controls and scrolling protocol.

The refreshed effective decision gate resolves twelve conditional icon branches
and three conservative conditional defaults to mod assets. The broader artwork,
model, portrait and audio backlog remains separately reported, including all
uninspected DLC archive limits. No in-game after screenshot is claimed.

See also [the focus repair ledger](../../FOCUS_SCREEN_REPAIRS_20261031.md) and
[the offline focus geometry/seam projection](../package0-focus/focus-geometry-and-seams.png).

The full existing offline suite, focused repair regressions and effective
installed-engine dependency checks are recorded separately from native status.
The effective-consumer audit reports broader unresolved vanilla dependencies;
passing a repaired-screen gate does not mean the whole conversion is complete.

Native testing remains paused at the user's request. Before release acceptance,
recreate these three cases on the exact candidate at 3440x1440/1.0,
1920x1080/1.0 and 2560x1440/1.25. Check selected-country updates, long prose,
focus states/links/titles, zoom, search, scrolling and continuous-focus entry
navigation. Exercise populated and valid-empty decisions, economy tabs and long
country/news events. Retain actual after captures here when authorized.

Keep the separate remaining PR #29 and PR #30 native checklists open; this
package does not retroactively change their coverage.
