# Event-window defaults and style repair

This component follows the independent event-picture fit packet at `93db0e2b`.
It replaces the 15 effective eventwindow engine fallbacks with original scoped
briefing defaults, frames, neutral office/agency marks and existing-atlas font
aliases. It now changes exactly **17 sprite-reference fields, six font fields and
two explicitly provisional horizontal description insets**. All other layout,
controls, identities, events, leaders, agencies, policies and gameplay remain
unchanged. Native border/clipping semantics are unaccepted.

The source owner and reproduction commands are in
[`tools/event_style/README.md`](../tools/event_style/README.md). The offline
[gallery](evidence/event-style/gallery.html),
[complete text/aperture/restoration measurements](evidence/event-style/measurements.json),
[explicit base-only effective dependency report](evidence/event-style/effective-eventwindow-base-only.json)
and [exact-source checks](evidence/event-style/source-checks/results.json) retain
their separate coverage boundaries.

## Preservation

The original Event-Fit capture is unchanged. Both source-text restoration and an
independent ordered-AST traversal undo only the 25 explicitly registered values
and require the entire original GUI to match. Negative fixtures reject each
reverted/wrong/missing field, extra/duplicated controls and changed geometry,
actions, conditions or ordering. The fit owner calls only this strict restoration
when its original GUI hash differs; no broad exception or original recapture is
introduced. All 548 protected originals, 108 Anea focus DDS, three military
captures and every existing event's gameplay/text/options remain unchanged.

The original fit inventory is regenerated only for its two deliberately changed
default sprite names. Its 425 actual explicit picture consumers and native
210×176 /397×153 fit apertures remain unchanged.

## Artwork and primary contracts

Twelve original editable geometric SVG textures serve 13 new event-scoped sprite
aliases. All are navy/cyan/light, with no text, watermark, human face, claimed
agency identity or guessed flag. No installed pixels are copied. The office
placeholder is a neutral civic office mark. Mid/bottom aliases deliberately share
one tile. Every actual sprite's original type and metadata are checked against
read-only installed **HOI4 1.19.4.1**, identified by launcher `rawVersion`.

The operative strip retains all **24 distinct 528×596 frames**, **80fps**, no loop,
no play-on-show and original pause metadata. The transparent source is95×95 but
retains the actual3×3 quad/1px border. Existing580×66 tile/290×16 borders remain.
The neutral agency strip is deliberately normalized from233×119/two fractional
116.5px frames to234×119/two117px frames. This explicit nominal+0.5px/frame change
fits the source slot; native agency slicing is not accepted.

Both `ACEvent16`/`ACEvent20` aliases reuse the existing ACBriefing atlases and
metrics byte for byte. They are direct children of the native `bitmapfonts`
registration block. Root-only or arbitrarily nested declarations fail both the
direct validator and the effective font collector. Global engine aliases remain
untouched.

## Text, bounds and acceptance limits

The corrected PR #55 audit measures **1,892** well-formed authored fields:
**1,803 country and 89 news**, including every repeated title/description and its
conditional variants. There are **zero static current title clips** and **zero
missing glyphs**. Before padding, **16 description instances had one-pixel
horizontal ink overflow**, retained as failed findings in the committed
pre-padding receipts and raw measurement copy. A vertical scrollbar only
counts **properly wrapped bottom overflow** as accessible: it cannot repair left,
right, top or unbreakable-word overflow. **256** long bodies satisfy that limited
scroll-accessibility condition before padding. **130** dynamic fields and **90** inherited
missing/malformed localization references remain separately listed; none is
represented as accepted runtime text. No localization is rewritten here.

The 16 findings are repeated variants in `ac_sq.217`/`ac_sq.10217`,
`ac_sq.301`/`ac_sq.10301`, `ac_sq.316`/`ac_sq.10316`,
`ac_sq.414`/`ac_sq.10414`, plus `gebet.3` and `sapin_politics.6`.
Exact localization keys, field occurrences, conditional paths, ink rectangles
and overflow directions are retained in `pr55-review/raw-metrics-before-padding.json`. The
earlier 1,624-field/zero-body-clip results remain historical receipts; they are
superseded by this stricter measurement, not silently reinterpreted as passing.

## Separate provisional description-inset repair

Only the existing `EventWindow/midsection/Description/borderSize.x` and
`EventWindow_News/midsection/Description/borderSize.x` values change **0 → 1**.
The original immutable GUI capture remains unchanged; these numeric fields are
registered explicitly as substitutions24/25, with independent lexical and ordered
AST restoration. Font/atlas/metric and narrative bytes remain unchanged.

Installed1.19.4.1 text-box examples establish that nonzero `borderSize` is authored
on native controls. They do not establish the exact maxWidth formula. Therefore
the source analysis records **both provisional interpretations**, never treating
either as verified engine behavior:

| Description | maxWidth includes borders: origin / wrap / outer / right clearance | maxWidth excludes borders: origin / wrap / outer / right clearance |
|---|---|---|
| Country | +1 /510 /512 /37 | +1 /512 /514 /35 |
| News | +1 /458 /460 /29 | +1 /460 /462 /27 |

Every field is tested under both interpretations using actual unchanged bitmap
glyph ink. Any unbreakable-word, horizontal or top overflow remains a failure;
vertical scrolling only handles properly wrapped bottom overflow. Finite ancestor
widths are checked separately, and either unbounded or negative clearance fails.
Both modeled interpretations now have **zero static title overflow, zero
unscrollable static body overflow and zero parent-clearance findings** across the
1,892 measured fields. **269** long bodies are scroll-accessible under this modeled
contract. This is **modeled inset coverage**, not accepted native rendering or a
waiver of the original16 findings.

There are no authored leader/operative events in this payload. Their two template
reviews therefore use explicit actual-country-text stress proxies. Those long
proxies overflow the existing unscrollable description fields and the narrow
operative title; the report retains that limitation instead of changing layout.
The actual portrait-frame aperture is transparent over the full scaled office
image; the two117×119 agency states end at(478,154), inside the528px body and above
the title at y170. Aperture tests follow the actual GUI sprite through the
supplied GFX definitions and selected frame to its bound texture. A same-sized
opaque texture rebinding fails even when the original authored frame remains
present and transparent on disk.

The four offline drawings retain literal source anchors. Native automatic section
sizing, zero-height leader roots, dynamic options/reflow, portrait rotation and
text wrap are not simulated. Raw anchors may visibly intersect in this drawing;
that is not a claim about successful or failed engine reflow. Gallery labels make
this distinction explicit. Native animation, input, scrolling, dynamic identities,
DLC activation and display-scale acceptance remain paused.

The effective base-only dependency gate passes with **zero eventwindow failures**
and **zero decision-screen failures**. The wider report still contains inherited
portrait/agency/event-picture/MIO/model/audio/runtime gaps and12 reference parse
failures. A bounded ownership pass is not whole-presentation or native acceptance.
