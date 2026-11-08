# Usea Depth

Usea Depth is a large focus expansion for every Usean country, 1991–2005. It is approved in `tools/overhaul/release_plan.json` under `approved_expansions.usea_depth`, alongside the original 1,028-focus budget. Erusea's remaining 54 focuses stay earmarked for the Lighthouse-era wave F1.

Six content packages are built in parallel, one PR each, on the seams added with this document. Native status for every package: not tested in HOI4. Native acceptance remains under #8.

## Why

Measured on `main` at 82c8edab:

- **Erusea and Central Usea:** their opening trees (18 and 24 focuses) run out around 1993, and nothing follows until the December 1999 tree switch.
- **North Point:** about three years of 1991 content.
- **14 minor states:** only the shared 36-focus regional tree.

## Packages

| Package | Folder | Tags | Planned new focuses | Marker | Wrapper files | Placement band |
| --- | --- | --- | --- | --- | --- | --- |
| Erusea | `eru` | ERU | ~300 | `USEA DEPTH ERUSEA` | `ERU_opening.txt`, `ERU.txt` | opening: x ≤ 23, y ≥ 6. War: x 42–94 |
| Central Usea | `fcu` | FCU | ~300 | `USEA DEPTH CENTRAL USEA` | `FCU_opening.txt`, `FCU.txt` | opening: x ≤ 23, y ≥ 6. War: x 42–94 |
| North Point | `npt` | NPT | ~100 | `USEA DEPTH NORTH POINT` | `NPT.txt` | x 44–94 |
| Partners | `partners` | SNS, AMB, UGE, DEL | ~260 | `USEA DEPTH PARTNERS` | `SNS.txt`, `AMB.txt`, `UGE.txt`, `DEL.txt` | x 28–94 |
| Minors A | `minors_a` | CHO, PLA, FRU, ALR, DOR, SCA, BLD | ~420 | none | new `ac_ud_minor_<tag>.txt` trees | x ≤ 23 |
| Minors B | `minors_b` | SYC, CAL, RJR, ROH, VOS, CRS, SHI | ~390 | none | new `ac_ud_minor_<tag>.txt` trees | x ≤ 23 |

Planned counts are approximate. Each package records its real counts in its own `tools/usea_depth/<pkg>/budget.json`, and `tools/overhaul/check_release_plan.py` validates every one:

```json
{"package": "eru", "marker": "USEA DEPTH ERUSEA", "focuses": {"ERU": 300},
 "trees": {"ac_exp_eru_opening": 190, "ac_ucw_eru_tree": 110}, "events": 60}
```

The `trees` totals must equal the `focuses` totals, because every new focus is imported by exactly one tree.

## Delivered

All six packages are merged (#77–#82): 1,814 new focuses and 370 long-form events. Nothing has been tested natively in HOI4; native acceptance remains under #8.

| Package | PR | Focuses | Events | Ledger |
| --- | --- | --- | --- | --- |
| Erusea | #82 | 322 (200 opening, 122 war) | 60 | [ERU.md](ERU.md) |
| Central Usea | #81 | 294 | 60 | [FCU.md](FCU.md) |
| North Point | #79 | 107 | 23 | [NPT.md](NPT.md) |
| Partners | #78 | 260 (SNS 80, AMB 60, UGE 60, DEL 60) | 52 | [PARTNERS.md](PARTNERS.md) |
| Minors A | #77 | 437 (about 62 per state) | 94 | [MINORS_A.md](MINORS_A.md) |
| Minors B | #80 | 394 (about 61 per state, Shilage 30) | 81 | [MINORS_B.md](MINORS_B.md) |

The merged totals are recorded under `approved_expansions.usea_depth.delivered` in `tools/overhaul/release_plan.json`. `tools/usea_depth/integration/test_integration.py` runs from `run_checks.py` and checks what only shows up once the packages are together:

- those totals match the packages' own budgets;
- scripted effects, triggers, ideas, characters, decisions, events, sprites and localisation keys are defined once across the whole mod;
- every flag a package checks is set somewhere, and every scripted call resolves;
- each new focus is imported exactly once;
- every marker block survives in every wrapper.

## Ownership

**Files a package owns.** Each package creates only new files:

- `tools/usea_depth/<pkg>/`: `content.py`, `narrative.py`, `build.py` (with `--check`), `build_art.py`, `test_<pkg>.py`, `budget.json`, `assets.json`
- `mod/2985041246/common/<folder>/ac_ud_<pkg>.txt`, for each of the folders `national_focus`, `events`, `ideas`, `scripted_effects`, `scripted_triggers`, `decisions`, `decisions/categories`, `characters` and `on_actions`
- `localisation/english/ac_ud_<pkg>_l_english.yml` (UTF-8 with BOM)
- `interface/ac_ud_<pkg>.gfx`
- `gfx/AC_usea_depth/<pkg>/**`
- `docs/usea_depth/<PKG>.md`: the package ledger, with a source layer and an exact citation for every lore row

No new file may start with `ERU`, `FCU`, `NPT`, `REC`, `YUK` or `ac_ucw`. Those names are counted by `tools/Test-UseaExpansion.py` and `tools/Test-ContinentalWar.py`.

**Shared files a package may touch:**

- Its marker block in its wrapper files, written only through `seams.attach_file()`. After attaching, re-run the wrapper's owner generator:

  | Wrapper | Owner generator |
  | --- | --- |
  | `ERU_opening.txt`, `FCU_opening.txt` | `python -B tools/usea_expansion/build_content.py` |
  | `ERU.txt`, `FCU.txt` | `python -B tools/build_continental_war.py` |
  | partner trees | `cd tools/usean_partners && python -B build.py` |
  | `NPT.txt` | `python -B tools/usea_expansion/build_content.py` |

- Never hand-edit `continuous_focus_position`.
- One row in `docs/LORE_EVENT_COVERAGE_BACKLOG.md`.
- These generated records: `tools/world_foundation/country_registry.json`, `docs/evidence/event-style/*` and `docs/evidence/decision-rows/*`. Never hand-merge them. Take `origin/main`'s copy and re-run `python -B tools/content_waves/refresh_records.py`.

**IDs:**

| Item | Pattern |
| --- | --- |
| Focuses | `<TAG>_ud_<slug>` |
| Ideas and flags | `<TAG>_ud_*` |
| Effects and triggers | `ac_ud_<pkg>_*` |
| Minor trees | `ac_ud_<tag>_tree` |
| Office leaders | `<TAG>_ud_<slug>_office` |
| Sprites | `GFX_ac_ud_*` |

**Event namespaces:** `ac_ud_eru`, `ac_ud_fcu`, `ac_ud_npt`, `ac_ud_up`, `ac_ud_mina`, `ac_ud_minb`.

## Content rules

**Sources.** Read `docs/CANON_POLICY.md`, `.agents/skills/canon-lore-research/SKILL.md` and the Chronicle rows in [USEAN_CONTINENTAL_WAR.md](../USEAN_CONTINENTAL_WAR.md). The only official Usea anchors are:

- 1995 / 12.31: the Skully Islands rebels
- 1996 / 04.20: the Ulysses announcement
- 1997 / 05.30: the Usea-wide coup
- 1998 / 06.19: Stonehenge completed
- 1999 / 07.08: the impact
- 2000 / 04.21: the refugee closure
- the 2003–2005 war rows

Everything else is provisional gameplay or mod provenance, and is labelled as such. There are no Usea sources for 1991–1994 or 2001–2002, and none at all for Amber, Ugellas, Delarus or the minors.

**Never invent:**

- New named people. New governments get unnamed office leaders, such as a "Crown Council" or an "Emergency Directorate", with portraits the package generates.
- Chronicle place names mapped to states. Stonehenge's state 310 remains the only mapping.
- `transfer_state`, cores, borders, `declare_war_on`, `annex_country`, or faction changes.
- A Shilage annexation inside 1991–2005.
- Megalith or Stonehenge construction dates.

**Politics.**

- Government changes happen only inside scripted effects named `ac_ud_<pkg>_regime_*`, built with `seams.regime_effect()`. Each one recruits and promotes a matching office leader.
- Every focus or event option that reaches one has an AI weight of 0, so the AI keeps its 1991 governments.
- Central Usea regime changes before the 22 August 2003 founding of ISAF are player-only alternate history.
- Erusea's postwar "never a forced government swap" rule is unchanged.
- Partner and minor popularities are placeholders. Seed them through effects, never in history files (`tools/world_foundation/original_four.json` freezes the partner histories). Never build mechanics on popularity thresholds.

**The Chronicle war still happens by default.** New content must not set or clear any `ac_ucw_*` global flag, push AI Erusea's grievance below 25, or edit `ac_ucw_country_start`. The Erusea, Central Usea and partner tests simulate the AI default path with the World harness in `tools/Test-ContinentalWar.py`, and assert the war still starts in summer 2003.

**Era gates in the opening trees.**

- Every opening-tree focus has `available = { date < 1999.12.1 NOT = { has_global_flag = ac_ucw_calendar_started } }`.
- Content is banded across the decade:
  - 1991–1995: rebuilding and early politics
  - from 1996.4.20: preparing for Ulysses
  - from 1997.5.30: the coup and its aftermath
  - from 1998.6.19: Stonehenge
  - from 1999.7.8: impact relief
- Anything that must survive the December 1999 tree switch goes through the package's own once-only effect, run after `ac_ucw_calendar_started`.

**Size and time.**

- One playthrough completes about 71 opening-tree focuses in 1991–1999 and about 60 in 2000–2005.
- Larger trees come from mutually exclusive branches: political paths, doctrine and economic choices, and lanes specific to each outcome.
- Focus cost is 5, or 10 for a major commitment.
- No interchangeable factory or political-power filler.

**Events.**

- Branch openers, political turns and era transitions fire long-form events.
- Each one has at least three paragraphs and 180 words, ends with a source-layer line, and uses no curly quotes. Build them with `seams.event_text()` and check them with `seams.event_problems()`.

**Other rules.**

- Fiscal calls sit inside `limit = { ac_econ_ready = yes }`.
- Art is mod-only, with one unique generated icon per focus. Its shine reuses the same texture (`seams.focus_sprites()`), never the vanilla `shine_overlay.dds`.
- Draw with `seams.glyph_library()` and Pillow 11.3.0. Never call the library's `save()`, `build_focuses()` or `main()`.

## Seams API (`tools/usea_depth/seams.py`)

| Helper | Use |
| --- | --- |
| `MARKERS` | Marker name and wrapper files for each package |
| `attach_file(path, name, ids, check=False)` | Add or replace a package's import block, keeping the file's BOM and line endings |
| `attach`, `import_blocks`, `foreign_import_blocks`, `reinsert` | The text-level primitives, which the owner generators also use |
| `shared_nodes(ids)` | Resolve shared focus definitions across all trees |
| `tree_positions()`, `band_violations(...)`, `title_fits(text)` | Layout, using the font metrics and position resolver from `Test-FocusScreenRepairs.py` |
| `glyph_library()`, `SUBJECTS`, `encoded(image)`, `focus_sprites(pkg, id)` | Art |
| `event_text(...)`, `event_problems(text)` | Long-form events |
| `office_character(...)`, `regime_effect(...)` | Unnamed leaders and the only allowed form of government change |
| `banned_uses(text)`, `political_violations(effects_text)` | Content guards for package tests |

## Every package test checks

- Counts equal `budget.json`. Each ID is imported exactly once, inside the package's own marker or tree.
- Nodes sit inside the package's band. Titles fit, and no captions overlap (`python -B tools/Test-FocusScreenRepairs.py`).
- Localisation is complete and has a BOM. Every `has_*_flag` has a readable label.
- Icons and shines resolve to mod textures.
- Government changes appear only in `ac_ud_<pkg>_regime_*` effects, with an AI weight of 0.
- The AI war-start simulation passes (Erusea, Central Usea and partners).
- Every fiscal call has its guard. No banned effects or `ac_ucw_*` flag writes.
- `build.py --check` and each touched owner generator's `--check` pass.

`python -B tools/usea_depth/run_checks.py` runs the seams test and every package test. It runs from `tools/Test-UlyssesStatic.ps1` and from `.github/workflows/usea-depth.yml`.

## Merging

- This seams PR merges first.
- The content PRs then merge one at a time. Each one is brought up to date with `main` just before it merges, after re-running the owner generators and `refresh_records.py`.
- When another package's block sits at the same insertion point, keep both blocks and re-run the owner generators' `--check`.
