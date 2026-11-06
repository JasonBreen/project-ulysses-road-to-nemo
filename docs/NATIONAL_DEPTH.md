# National depth: delivery ledger

This is the programme that gives every country at least 150 focuses, each one
visible. It was approved on 6 November 2026; the plan and its waves are in the
session plan, and the build is described in `tools/national_depth/README.md`.
`tools/Test-FocusVisibility.py` is the definition of done.

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
| W0c pilot | Chopinburg (CHO), Usean minor | `tools/usea_depth/minors_a/countries/CHO.py` | 161 + 36 = 197 | 13 | [image](evidence/national-depth/cho.png) |
| W0c pilot | Perbla (PBL) | `tools/world_depth/pbl/content.py` | 143 + 36 = 179 | 13 | [image](evidence/national-depth/pbl.png) |

The content page for all delivered trees is
[evidence/national-depth/index.html](evidence/national-depth/index.html).

**Pilot notes:**
- **Chopinburg:**
  - The 2019 Chronicle row about Chopinburg airspace is deliberately not used:
    the ledger gives it no political status.
  - Usean anchors (1996.4.20, 1997.5.30, 1998.6.19, 1999.7.8, 2003) gate eras
    only.
  - The three 1991 paths, the 1997 coup aftermath and the 2006 recovery change
    government only through offices.
- **Perbla:**
  - The inherited Perbla intervention events stay their own owner; the tree
    neither fires nor duplicates them.
  - The archive's `perblan_totalitarianism` sub-ideology is used for one of
    four political paths.
  - Belkan War rows are cited as date anchors only.
  - Dakrain's claims on Terentio states are acknowledged with no border effect.

**Not verified natively:** parsing, the rendered focus screen, AI pacing and
balance (#8).
