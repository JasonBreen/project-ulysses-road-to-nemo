# National depth: delivery ledger

This is the programme that gives every country at least 150 focuses, each one
visible. It was approved on 6 November 2026; the plan and its waves are in the
session plan, and the build is described in `tools/national_depth/README.md`.
`tools/Test-FocusVisibility.py` checks visibility.

On 11 November 2026 you directed that new content follow main's national
campaign era targets (`docs/WORLD_CAMPAIGNS_2040.md`; 1991–2005, 2006–2020,
2021–2040), written with this compiler and its lints. `tools/world_campaigns/
coverage.py` credits compiled trees by era. Mass production is still waiting on
your review of the Perbla pilot.

## Source layers

Every focus, idea, event, office, building and flag in a bespoke tree is
**provisional gameplay**, unless a row in that country's spec `SOURCES` names
something else:
- an exact official ACES Chronicle row, used only as a date anchor or pressure,
  never as an asserted national outcome;
- or **mod provenance**: an inherited state, idea or event the tree builds on.

No tree names a new person. Governments change only through a regime effect
attached to an unnamed office, and the AI never takes those focuses. No tree
moves a border, a core or a faction, or declares war. Buildings go only into the
country's own 1991 states.

## Delivered

| Wave | Country | Spec | Own + shared focuses | Events | Review |
| --- | --- | --- | ---: | ---: | --- |
| W0c pilot | Perbla (PBL) | `tools/world_depth/pbl/content.py` | 143 + 36 = 179 | 13 | [image](evidence/national-depth/pbl.png) |

The content page for all delivered trees is
[evidence/national-depth/index.html](evidence/national-depth/index.html).

**Chopinburg pilot retired (11 November 2026).** Merging main brought in Usea
Depth minors A (PR #77). That package owns `ac_ud_minor_cho.txt` and the
`CHO_ud_*` ids, so the 161-focus pilot spec, its compiled files and its art were
removed in favour of main's tree. Chopinburg's remaining era targets are now
tracked by `tools/world_campaigns/manifest.json`.

**Pilot notes:**
- **Perbla:**
  - The inherited Perbla intervention events stay their own owner; the tree
    neither fires nor duplicates them.
  - The archive's `perblan_totalitarianism` sub-ideology is used for one of
    four political paths.
  - Belkan War rows are cited as date anchors only.
  - Dakrain's claims on Terentio states are acknowledged with no border effect.

**Not verified natively:** parsing, the rendered focus screen, AI pacing and
balance (#8).
