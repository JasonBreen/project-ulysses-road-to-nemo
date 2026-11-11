# Country selection and ultrawide repair

Private source reference: user screenshots `20261106031141_1.jpg` and
`20261106031335_1.jpg`, both 3440×1440, supplied 6 November 2026. Their observed
defects are scenario-card/history overlap, a bounded central background rather
than a viewport cover, and institutional tooltips enumerating all country tags.

The scenario panel is now 780×620 with two finite 250×211 bookmark slots, a
separate scrolling description and a footer. The country picker is 1200×660:
the static inherited-geography overview and scrolling country lists occupy the
upper region; scrolling history, government information and national spirits
have separate lower regions. Original engine control names and both bookmark
definitions remain. Country-detail spirits no longer extend past the panel.

The background uses the installed 1.19 interface's percentage/minimum/maximum
aspect-ratio mechanism. The original texture is preserved and the horizontal
maximum follows the viewport. No display or game-profile settings are changed.

The `ac_pol_profiled` trigger retains its complete tag OR inside one
`custom_trigger_tooltip`. It displays one institutional-profile requirement.
Power, capacity, cooldown, ownership and initialization checks remain visible
through the surrounding availability trigger. Offline tests compare all 69
profiles and a non-profiled identity; costs and institutional effects are unchanged.

`tools/frontend_briefing/responsive_original.json` records the original managed
blocks. It is provenance, not a replacement golden hash. Validation checks safe
rectangles, list clipping/scrolling, button extents, exact control bindings and
the reviewed properties; unrelated controls retain the historical fingerprint.
Generation is repeatable through `responsive.py`; the existing Anea briefing
owner recognizes the new layout instead of restoring the earlier geometry.

Validation matrix: 3440×1440 at 1.0/1.25/1.5, 2560×1440 and 1920×1080 at
1.0/1.25, and 1280×720 at 1.0. These are **static geometry projections**.
Commands: `python -B tools/Test-ResponsiveFrontend.py`, existing frontend,
institution, interface, Anea presentation and overhaul-repair checks, and the
PowerShell static suite. Native rendering, mouse input and engine scrolling
remain untested under #8; no HOI4 launch is part of this change.
