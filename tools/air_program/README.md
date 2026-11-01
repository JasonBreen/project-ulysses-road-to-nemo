# Conventional Aviation Systems, 2006–2020

This additive source packet starts from composed review parent `549cad986c630334d398beb2e11c8e23939f3990`, with the separately reviewed research-font migration from `5b4a25d243bfbf9012869d4a6da1874317c64fe4`. It adds 24 dated research commitments, 20 complete aircraft models, 16 modular airframes, 32 components and a real Aviation Systems research page.

Every new name, date, specification, research cost and industrial allocation is **provisional gameplay**. The work makes no claim about official ACES aircraft programmes, real hardware specifications or subsequent wars. Existing technical IDs, 1991 histories, formations, variants, project owners and the post-2020 campaign contract remain intact.

## Reproduction and file ownership

Run from the repository root with Python 3.12 and `Pillow==11.3.0`. Generated text and the capability worksheet use the standard library; original texture packaging and the offline page reconstruction use Pillow. The installed game is optional for ordinary reproduction. The committed primary capture supports independent replay of the effective equipment subset.

```powershell
python -B tools/air_program/build.py
python -B tools/air_program/build_art.py
python -B tools/air_program/build_ui.py
python -B tools/air_program/audit.py
python -B tools/air_program/render_review.py
python -B tools/air_program/test_air.py
```

Each authoring command supports `--check`. The UI is composable: running either `tools/land_program/build_ui.py` or `tools/air_program/build_ui.py` first produces exactly the same common research screen. AIR owns two named controls, its card templates and 16 native blueprint containers. LAND remains the canonical common-screen generator; its normalizer removes only registered additions and the reviewed scrollbar properties, then calls the strict font-restoration helper before comparing the original whole AST. Neither original GUI capture is refreshed to accept unrelated changes.

```powershell
python -B tools/air_program/audit.py --reference 'G:/steamlbirary/steamapps/common/Hearts of Iron IV'
python -B tools/air_program/run_checks.py --engine 'G:/steamlbirary/steamapps/common/Hearts of Iron IV' --core
```

The first command is an explicit primary recapture, appropriate only after reviewing source changes. The second reads the installed loose files without launching the engine and retains bounded logs under `docs/evidence/air-program`. At most two checks run concurrently. `--only` reruns specified changed gates while retaining previous results. `--check --reference` verifies the captured contracts without rewriting them.

| Source | Responsibility |
|---|---|
| `air_content.py` | Six families, four tiers, prerequisites, role presentation and default recipes |
| `build.py` | Technology, complete equipment, frames, components, AI and English localization |
| `air_primary.py` | Ordered effective equipment reader; inherited slots, duplicate roles, repeated module limits, mission declarations and bounded stat arithmetic |
| `audit.py` | Current-definition replay against captured primary facts, paid route eligibility and explicit capability differences |
| `air_ui.py`, `build_ui.py` | Pure common-screen extension, engine-bound card templates and actual designer blueprint controls |
| `build_art.py`, `source/art/*.svg` | Original geometric masters, DDS packaging, sprite aliases, dimensions, alpha and hashes |
| `presentation.py`, `render_review.py` | Actual blueprint consumer bounds and page reconstruction from shipped controls, localization, DDS and BMFont glyph metrics |
| `preserved_sources.json` | 1,107 inherited technical/history sources pinned to the reviewed parent; no wholesale recapture on mismatch |

## Dated research and paid manufacture

Every family has nodes in 2006, 2010, 2015 and 2020. Research has a positive cost, a hard date gate and real unlocks. Later role tiers require their preceding tier and the same-year Systems node. Systems begins with radio, basic machine tools and electronic/mechanical engineering. The first combat/surveillance commitment also checks the correct existing legacy or designer foundation inside its actual `allow` guard. No old-save initialization, free design, equipment stock or late research grant is added.

| Family | Manufactured capability | First inherited foundation |
|---|---|---|
| Air Systems | Propulsion, flight controls and maritime electronics | Radio, basic machine tools and electronic/mechanical engineering |
| Air Superiority | Conventional fighter | `jet_fighter2`, or BBA modern small airframe |
| Tactical Strike | Conventional battlefield attack | `CAS3`, or BBA modern small airframe |
| Maritime Strike | Conventional ship/port attack | `naval_bomber3`, or BBA modern small airframe |
| Air Transport | One complete native transport-aircraft route | Current Systems; no history-only Belkan bridge dependency |
| Air Surveillance | Optional reconnaissance aircraft | La Résistance plus `scout_plane2`, or BBA modern medium airframe and `photo_reconnaisance` |

The legacy-format model is producible only with BBA disabled; the corresponding modular frame is eligible only with BBA enabled. Transport deliberately has one complete-aircraft route in both cases. Surveillance additionally requires La Résistance in research and production. There are 20 eligible models at 2020 with La Résistance, and 16 without it, in each of the independent MTG/NSB switch combinations. Research closure fixtures assume immediate completion solely to inspect eligibility; they do not measure natural research time or AI progression.

All 16 default modular recipes validate native inherited required slots, categories, every repeated count limit, module-defined roles, positive thrust sufficient for weight, physical materials and costs. They match their complete counterparts in source statistics, resources, crew and fuel. Creating a researched modular design still requires native XP/design actions and paid production. Optional loadouts can differ. Mixed contributors to averaged weapon statistics are rejected by the offline arithmetic rather than silently treated as a sum.

| Aircraft family | 2006 / 2020 IC | 2006 / 2020 fuel coefficient | Crew | Continuing line materials |
|---|---:|---:|---:|---|
| Fighter | 54 / 78 | 0.27 / 0.33 | 20 | Aluminium 4, rubber 1, steel 1, tungsten 1, chromium 1 |
| Strike | 54 / 78 | 0.27 / 0.33 | 20 | Aluminium 4, rubber 1, steel 1, chromium 1 |
| Maritime strike | 56 / 80 | 0.27 / 0.33 | 20 | Aluminium 4, rubber 1, steel 1, chromium 1 |
| Transport | 70 / 100 | 0.80 / 0.95 | 80 | Aluminium 5, rubber 2, chromium 1 |
| Surveillance | 76 / 103 | 0.55 / 0.67 | 40 | Aluminium 6, rubber 2, chromium 1 |

Materials are native continuing production-line coefficients, not an item charged once per aircraft. Fuel is an equipment coefficient; actual mission consumption, national modifiers, imports, crew aggregation and production throughput require native checks. No starting industry or resources are increased to pay for future research. Complete priorities are 200/210/220/230, above the captured effective parents; frames use 2100/2110/2120/2130. Ordering is an authored contract, not proof of AI replacement behavior.

## Source-supported missions and limits

The installed 1.19.4.1 primary vocabulary uses `attack_logistics`. It does not establish that a declared mission is active under every DLC combination. The source explicitly preserves each predecessor's mission declarations and duplicate-role overrides, including native `for_each` changes and camera classification exclusions.

Legacy maritime aircraft retain mine-planting/sweeping declarations. A bare BBA maritime attack recipe supplies ship/port attack and patrol declarations but does not include equivalent mine equipment. The worksheet lists that difference rather than deleting inherited missions or claiming universal parity. Additional mining configuration and its DLC/mission behavior remain separate work.

La Résistance-disabled reconnaissance is a visible release gap, including inherited specialist wings. This packet neither force-grants technology to imply mission equivalence nor invents a substitute intelligence mechanic. Surveillance has optical reconnaissance and passive naval-detection source statistics, zero naval attack and zero air superiority. It is not an ASW attack platform, airborne early-warning system or operational jamming implementation. Native transport declarations cover `paradrop` and `air_supply`; actual mission/DLC permissions and troops' training still require acceptance.

## AI, operating costs and continuity

Research and production priorities activate after 2005 and require relevant researched nodes. BBA design groups remain zero-priority before 2006 or their first role research, and each design requires its dated role and Systems technology plus applicable DLC. Their allowed component set is the actual researched default recipe. Native design creation, XP use and production remain untested.

Fighter, strike, maritime and surveillance replacement weights use existing verified native role IDs. Transport uses a separate archetype strategy: at most one requested MIL when the country has more than 20 MIL, has researched transport 2006 and holds fewer than 21 transport aircraft. This competes for existing capacity. It is not free equipment or an assertion that every small country should operate a transport fleet.

All new aircraft inherit established native air archetypes, types and interface categories. The existing fiscal owner therefore observes the deployed-aircraft base and its one maximum role-premium pool. Actual-owner fixtures demonstrate each supported role incurs cost, multirole observations do not add several premiums, and disabled fiscal mode remains inert. No custom archetype, extra fiscal coefficient, stockpile bill, per-wing telemetry or guessed operational measurement is introduced.

## Original artwork and retained surfaces

The editable procedural master and 56 exported SVGs produce 94 RGBA8 DDS textures and 146 sprite bindings. Research uses 24 distinct 112×40 compositions; complete equipment uses 20 distinct 192×96 views; modules use 32 distinct 64×64 subjects; 16 designer overlays are 508×248; the tab has four 89×30 frames. A separate 96×96 technical sheet is retained. Related complete/designer defaults intentionally share the same physical aircraft art through explicit aliases. `assets.json` records every texture's dimensions, frame width, alpha extrema, SHA-256, provenance and source binding. The original illustrations contain no imported engine pixels, national portraits, watermarks or yellow artifacts.

The actual `equipment_designer_<frameID>` controls retain the required `equipment_image_overlay` name and consume the correct full-size texture. Regression fixtures substitute an existing 64×64 module DDS into that real control, alter geometry and change bindings; each must fail. All artwork is original authored geometry, rather than renamed native imagery.

This additive page does **not** retire the old air tabs. `capabilities.json` inventories all 38 legacy and 41 BBA technology definitions, their exact dates, folders and hashes. The legacy tab retains carrier, heavy-fighter, tactical-bomber, strategic-bomber and suicide-aircraft contracts. The old BBA tabs retain small/medium/large frames and native-style bombs, guns, engines, cameras and associated labels, including 1977/1981 dates. Relabelled dates do not complete their equipment or presentation conversion. They remain reachable subject to existing DLC/technology gates.

Existing 3D plane entities and attachments, ordinary air map-role presentation outside the new sprites, MIO identities and old equipment art are presentation backlog. Carrier conversion, heavy/tactical/strategic bomber families, helicopters, drones, missiles, stealth, AEW, aerial refueling and ASW attacks are outside this conventional slice. Existing strategic-project owners remain authoritative. The new screen uses actual drag, wheel and native horizontal/vertical scrollbars; neither captured GUI provides a research-search binding, so no unbound search field is added.

## Review and native acceptance

`docs/evidence/air-program` contains the three original-art galleries, a research-page reconstruction, actual consumer-bound reports and retained source-check results. Page geometry and text checks cover 3440×1440 at 1.0, 1920×1080 at 1.0 and 2560×1440 at 1.25. The image is explicitly an **offline reconstruction**, with illustrative research states, rather than a screenshot of the engine.

Native testing is paused and is still required for release acceptance:

| Area | Native coverage still required |
|---|---|
| Displays and controls | All three display configurations; tab discovery, all 24 nodes, states, tooltips, keyboard behavior, drag, both scrollbars and long detail descriptions |
| DLC routes | BBA×La Résistance four core combinations, with independent MTG/NSB enabled/disabled; actual activated packs rather than inferred source switches |
| Designer | All 16 default recipes, paid XP/design creation, inherited optional slots and exclusions, count limits, blueprint placement, optional mixed averaged armament and saved variants |
| Missions | Fighter/interception, CAS/logistics/ship/port attack as eligible, patrol, La Résistance recon, transport supply/paradrop and the explicit mining/disabled-recon differences |
| Industry and AI | Real queue/resource/crew/fuel costs, delivered replacement aircraft, inherited lines retained, natural research/XP/design decisions and bounded transport allocation |
| Fiscal observations | Native deployed-role and multirole query semantics; enabled/disabled economy modes, no duplicate role bill and no stockpile charge |
| Starts and saves | All 61 current start contracts remain source-compatible; new 1991 games, old saves before/after 2006, incomplete foundations, ongoing research/designs and save/reload around dated unlocks |
| Progression | Natural 2006/2010/2015/2020 checkpoints alongside separately labelled shortcut coverage |

No merge, publication, normal-install synchronization or native acceptance is implied by a source pass.
