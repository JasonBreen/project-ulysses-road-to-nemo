# National depth: delivery ledger

This is the programme that gives every country at least 150 focuses, each one
visible. It was approved on 6 November 2026; the plan and its waves are in the
session plan, and the build is described in `tools/national_depth/README.md`.
`tools/Test-FocusVisibility.py` checks visibility.

On 11 November 2026 you directed that new content follow main's national
campaign era targets (`docs/WORLD_CAMPAIGNS_2040.md`; 1991–2005, 2006–2020,
2021–2040), written with this compiler and its lints. `tools/world_campaigns/
coverage.py` credits compiled trees by era. You approved the Perbla pilot as the
template on 11 November 2026, and wave E1a (era 1 for the 29 countries that had
no tree) was delivered on 15 November 2026.

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

### Wave E1a: era 1 (1991–2005) for the 29 countries with no tree (15 November 2026)

Each country below started on the generic or a regional tree. Each now has its
own schema-2 spec for era 1, at or above its target (80 for other active and
emergent countries), compiled with the 36 shared institutional focuses.
`tools/world_campaigns/coverage.py` reports that no country still starts on the
generic or a regional tree.

| Country | Spec | Own + shared focuses | Branches | Events | Decisions | Offices | Review |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Aemurraq (AEM) | `tools/world_depth/aem/content.py` | 99 + 36 = 135 | 9 | 10 | 6 | 4 | [image](evidence/national-depth/aem.png) |
| Aquitoria (AQU) | `tools/world_depth/aqu/content.py` | 101 + 36 = 137 | 10 | 12 | 6 | 4 | [image](evidence/national-depth/aqu.png) |
| Arklith (ARK) | `tools/world_depth/ark/content.py` | 140 + 36 = 176 | 14 | 15 | 7 | 4 | [image](evidence/national-depth/ark.png) |
| Azbekerania (AZB) | `tools/world_depth/azb/content.py` | 113 + 36 = 149 | 10 | 12 | 6 | 3 | [image](evidence/national-depth/azb.png) |
| Baltica (BAL) | `tools/world_depth/bal/content.py` | 107 + 36 = 143 | 11 | 12 | 6 | 3 | [image](evidence/national-depth/bal.png) |
| Dakrain (DAK) | `tools/world_depth/dak/content.py` | 98 + 36 = 134 | 9 | 12 | 6 | 4 | [image](evidence/national-depth/dak.png) |
| Echea (EHE) | `tools/world_depth/ehe/content.py` | 98 + 36 = 134 | 9 | 11 | 6 | 3 | [image](evidence/national-depth/ehe.png) |
| Echinata (ECH) | `tools/world_depth/ech/content.py` | 97 + 36 = 133 | 10 | 12 | 6 | 3 | [image](evidence/national-depth/ech.png) |
| Gibraltar (GIB) | `tools/world_depth/gib/content.py` | 103 + 36 = 139 | 10 | 14 | 6 | 4 | [image](evidence/national-depth/gib.png) |
| Glaceland (GLA) | `tools/world_depth/gla/content.py` | 98 + 36 = 134 | 10 | 13 | 6 | 3 | [image](evidence/national-depth/gla.png) |
| Kaluga (KLG) | `tools/world_depth/klg/content.py` | 101 + 36 = 137 | 9 | 11 | 6 | 3 | [image](evidence/national-depth/klg.png) |
| Luremia (LUR) | `tools/world_depth/lur/content.py` | 89 + 36 = 125 | 10 | 13 | 6 | 3 | [image](evidence/national-depth/lur.png) |
| Malynea (MAY) | `tools/world_depth/may/content.py` | 94 + 36 = 130 | 9 | 12 | 7 | 3 | [image](evidence/national-depth/may.png) |
| Monstrua (MST) | `tools/world_depth/mst/content.py` | 99 + 36 = 135 | 10 | 12 | 6 | 3 | [image](evidence/national-depth/mst.png) |
| Nihon (NIH) | `tools/world_depth/nih/content.py` | 103 + 36 = 139 | 10 | 12 | 6 | 3 | [image](evidence/national-depth/nih.png) |
| Nordlands (NRL) | `tools/world_depth/nrl/content.py` | 149 + 36 = 185 | 13 | 15 | 7 | 4 | [image](evidence/national-depth/nrl.png) |
| Ratio (RAT) | `tools/world_depth/rat/content.py` | 97 + 36 = 133 | 9 | 9 | 6 | 3 | [image](evidence/national-depth/rat.png) |
| Relentio (REL) | `tools/world_depth/rel/content.py` | 99 + 36 = 135 | 9 | 11 | 7 | 3 | [image](evidence/national-depth/rel.png) |
| Romny (RMN) | `tools/world_depth/rmn/content.py` | 90 + 36 = 126 | 9 | 11 | 6 | 3 | [image](evidence/national-depth/rmn.png) |
| Serenava (SER) | `tools/world_depth/ser/content.py` | 94 + 36 = 130 | 10 | 16 | 6 | 3 | [image](evidence/national-depth/ser.png) |
| Seterano (SET) | `tools/world_depth/set/content.py` | 101 + 36 = 137 | 11 | 12 | 6 | 3 | [image](evidence/national-depth/set.png) |
| Sfaenland (SFA) | `tools/world_depth/sfa/content.py` | 110 + 36 = 146 | 10 | 14 | 6 | 3 | [image](evidence/national-depth/sfa.png) |
| Silvonia (ESN) | `tools/world_depth/esn/content.py` | 103 + 36 = 139 | 10 | 12 | 6 | 4 | [image](evidence/national-depth/esn.png) |
| Slavia (SLA) | `tools/world_depth/sla/content.py` | 103 + 36 = 139 | 10 | 12 | 6 | 4 | [image](evidence/national-depth/sla.png) |
| Terentio (TER) | `tools/world_depth/ter/content.py` | 95 + 36 = 131 | 10 | 13 | 6 | 3 | [image](evidence/national-depth/ter.png) |
| Valka (VLK) | `tools/world_depth/vlk/content.py` | 99 + 36 = 135 | 9 | 10 | 6 | 3 | [image](evidence/national-depth/vlk.png) |
| Verusa (VER) | `tools/world_depth/ver/content.py` | 101 + 36 = 137 | 10 | 13 | 6 | 3 | [image](evidence/national-depth/ver.png) |
| Wellow (WEL) | `tools/world_depth/wel/content.py` | 129 + 36 = 165 | 12 | 16 | 6 | 4 | [image](evidence/national-depth/wel.png) |
| Wielvakia (WIE) | `tools/world_depth/wie/content.py` | 99 + 36 = 135 | 9 | 11 | 6 | 3 | [image](evidence/national-depth/wie.png) |

**Totals:**
- 3,009 own focuses: 89 to 149 per country, against a combined era-1 target of
  2,440.
- 358 events, 178 decisions and 96 unnamed offices.

**Coverage after E1a:**
- 39 of the 68 countries meet their era-1 target.
- The other 29 already had a tree (Usea Depth minors, principals and regional
  owners). They need attach mode before the era-1 top-ups, E1b and E1c.
- All eras together: 7,203 of 22,920 focuses delivered.

**How it was checked:**
- **Each spec** passes the schema-2 lint against the mod and every other spec:
  titles, descriptions, five-word overlap, flags, reachability, building slots
  and the era targets.
- **Across specs,** `crosslint` also compares event text: no two countries'
  events share a five-word run above 0.3.
- **Neighbours** are written only from their own side. No tree assumes a
  neighbour's choice, moves a claim, a core or a border, or declares war.

**Notes:**
- **Releases.** Relentio, Serenava and Terentio are written for the released
  country only. They agree with Perbla's crown-lands branch and with each other,
  and none narrates when or how the release happens.
- **Serenava's capital.** Its history file (archive) puts the capital in state
  236, which is a Relentio core; Relentio's file puts its capital in 581,
  Serenava's own state. The release foundation's owned-capital selection
  (`ac_release_<TAG>_select_owned_capital`) already corrects this on release.
  Serenava's tree therefore adds no capital builds. The history files are
  unchanged.
- **Ratio's western neighbour** was first written as "Wiesmont", a name the mod
  never uses. It was corrected to the mod name, Wielvakia, on 15 November 2026.
- **Captions.** Where a state still carries an Earth-template or placeholder
  caption, the trees use a description ("the marsh district") or an existing
  victory-point name. They never use the caption itself.

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

## Compiler aligned with the national-campaign targets (11 November 2026)

- **Schema 2 specs** (`SCHEMA = 2`, `ERAS`) are linted against
  `tools/world_campaigns/manifest.json`. Each claimed era must meet its target,
  less what other owners delivered.
  - `test_compiled_eras_match_national_campaign_credit` runs main's
    `coverage.inventory` on the compiled fixture and confirms each branch is
    credited to the intended era.
- **Decisions.** `DecisionDef` gives one category per country, with 4–8
  decisions per era. Decisions cannot change the government, and repeatable
  decisions cannot build.
- **Event chains.** At least one per schema-2 spec. Every event must be
  reachable; this rule applies to every spec.
- **Campaign hooks.** `HasGlobal` and `NotGlobal` accept only global flags that
  some mod script sets, so a new tree cannot add a read-but-never-set flag.
- **Buildings.**
  - `dockyard` is allowed in coastal states only.
  - A shared-slot check uses the base-game state categories (native check #8)
    and the per-state caps.
  - Mutually exclusive alternatives, including those exclusive through a parent
    or a flag only one focus sets, count once.
  - The check confirmed that Perbla's builds fit.
- **Ownership guard.** `package.py` refuses to overwrite a file another
  generator owns. World Depth names (`_wd_`) are reserved for this compiler.
  Every other file must be listed in a package budget's `files` list.
- **Not yet built: attach mode**, for countries that already have a tree
  (Usea Depth minors, principals, regional owners). It is needed before the
  era-1 top-up waves (E1b, E1c), and its first step is checking that each owner
  generator keeps foreign marker blocks.
- **Perbla approved (11 November 2026), as is**, as the template. Wave E1a was
  delivered on 15 November 2026 (see *Delivered*).
- **Next: attach mode (C1b).** The era-1 top-ups for the 29 countries that
  already have a tree (E1b, E1c) need it.

