# Conventional Naval Systems, 2006–2020

This additive source packet supplies **24 dated research commitments, 20 complete ships, 20 MTG hulls and 64 components**. It composes the reviewed LAND/font parent `f07a105e`, original aviation `caa26730`, and portable review/font/source-identity follow-ups through `4aae7af3`, starting from verified remote main `25ab6721`. Existing country histories, fleets, variants, queues, old technical IDs, maps, war/faction/project owners and post-2020 contracts are preserved.

All new names, dates, specifications and costs are **provisional gameplay**, not claims about official ACES procurement, real naval hardware or subsequent wars. The programme models conventional gun/torpedo ships and manufactured service fittings. It does not implement guided missiles, nuclear propulsion, submarine-versus-submarine combat or a new carrier air group.

## Reproduction

Use Python 3.12 and CI-pinned `Pillow==11.3.0` and `numpy==2.2.6`. Text generation and captured-primary replay do not require the installed game. Packaging and offline review use Pillow and the shipped original briefing font atlas; the integrated start/map checks require NumPy. No commercial editor, desktop interaction or game launch is required.

```powershell
python -B tools/naval_program/build.py
python -B tools/naval_program/build_art.py
python -B tools/naval_program/build_ui.py
python -B tools/naval_program/audit.py
python -B tools/naval_program/render_review.py
python -B tools/research_fonts/measure.py
python -B tools/naval_program/test_naval.py
```

The authoring scripts accept `--check`. The three research UI generators derive a single canonical screen through explicit registered owners; all six LAND/AIR/NAVAL generation orders must produce identical output. The immutable pre-NAVAL capture and the original LAND/AIR captures are not refreshed to accept unrelated edits. The existing strict font migration/restoration API and exact raw FNT provenance remain authoritative.

```powershell
# Explicit primary recapture only after reviewing the installed source changes:
python -B tools/naval_program/capture.py 'G:/steamlbirary/steamapps/common/Hearts of Iron IV'
python -B tools/naval_program/audit.py --check --reference 'G:/steamlbirary/steamapps/common/Hearts of Iron IV'
python -B tools/naval_program/run_checks.py --engine 'G:/steamlbirary/steamapps/common/Hearts of Iron IV' --core
```

The installed reference was **1.19.4.1**. Captures contain declarations, identifiers, numerical dimensions and hashes; they contain no copied engine pixels. The runner uses at most two workers, retains logs under `docs/evidence/naval-program`, and never launches HOI4. `--only` reruns selected changed gates while keeping previous results.

For final receipts, commit the complete source and use `run_checks.py --exact-source --core --engine <reference>`. It uses the shared `tools/source_snapshot.py` owner to require clean source, pin the exact commit and all tracked raw input bytes outside `docs/evidence`, then verify the same inputs after every selected check finishes. Exact mode rejects `--only`: old retained results cannot be relabelled for a new source commit. The receipt identifies the tested code commit even if a later evidence-only commit records its outputs.

For an explicitly bounded follow-up phase, use `--pin-source --only <comma-separated-checks> --output <new-phase-directory>`. It uses the same source fence and includes only that invocation's rows; no earlier results are retained or relabelled. This supplements the separately recorded complete run. Only the unpinned legacy convenience mode can retain older rows, and its report identifies that limitation.

## Research and manufacturing

All six families have nodes in **2006, 2010, 2015 and 2020**. Each node has a paid research cost and hard date gate. Later role tiers require their preceding tier and same-year Naval Systems. The first role commitment checks the correct existing legacy or MTG foundation. Systems begins with radio, basic machine tools and electronic/mechanical engineering. No prerequisite, aircraft, hull, national variant, crew, dockyard or equipment stock is granted on initialization, research or late loading.

| Family | Physical use | First legacy / MTG foundation |
|---|---|---|
| Naval Systems | Four propulsion families, sensors, fire direction, local air defense and protection | Existing engineering/electronics foundations |
| Escort Ships | Conventional guns, torpedoes, sonar and depth-charge fittings | `advanced_destroyer` / `advanced_ship_hull_light` |
| Patrol Cruisers | Light cruiser endurance, surface armament and defense | `advanced_light_cruiser` / `advanced_ship_hull_cruiser` |
| Fleet Combatants | Capital-role conventional cruiser | `advanced_heavy_cruiser` / `advanced_ship_hull_cruiser` |
| Patrol Submarines | Conventional torpedo patrol and surface interdiction | `advanced_submarine` / `advanced_ship_hull_submarine` |
| Carrier Platforms | Ship, propulsion, deck capacity and local defense | `advanced_carrier` / `advanced_ship_hull_carrier` |

There is exactly one eligible paid ship route per family/tier: complete model without MTG, researched designer hull with MTG. The same research unlocks the actual components needed by its default fit. Independent BBA/NSB/La Résistance switches do not create duplicate or missing naval routes. Source fixtures cover 12 date/MTG cases and all 16 independent four-DLC combinations. Immediate research closure is a source-eligibility fixture, not natural research time or AI pacing.

### Defaults, classification and costs

Native complete ships already use `default_modules`. Several inherited complete models have zero bare weapon statistics. This packet therefore authors the **same bare hull and complete explicit default recipe on both routes**, rather than baking module contributions into a complete ship and then inheriting them again.

Every resolved default slot is declared, including deliberate `empty` optional slots. Complete models use the modern counterpart's explicit native slot definitions because their old complete parents sometimes expose fewer slots. MTG hulls retain the valid native slot inheritance. Both routes validate required engines, batteries/decks, categories, every repeated module-count restriction and default coverage. The reader preserves same-hull slot aliases, rather than dropping scalar slot declarations.

Native deck manpower appears outside `add_stats`; it is counted separately exactly once. The first carrier's base crew of 1,800 plus its 600-person deck fit yields 2,400. The default escort has light-gun attack 5, IC cost 2,460 and fuel coefficient 9. New torpedo outfits retain the native `naval_torpedo_hit_chance_factor` capability as a module coefficient; its effect is not a certified hit probability. First-tier torpedo attack/accuracy, heavy-battery piercing and dual-purpose air defense are compared with captured actual predecessors. Negative fixtures bake the gun contribution into the bare hull, omit a required engine, assign a wrong module category, violate an earlier count limit, lower inherited priority, remove default-slot coverage, or introduce negative costs/materials; these must fail.

Heavy cruiser batteries add the native capital classification. A new MTG fleet-combatant hull begins as a native screening cruiser; its selected heavy battery promotes the default to capital role. Swapping to an eligible light battery returns the source-derived screening classification. A carrier retains carrier identity while deck/air-defense components add their normal tags. Native classification and optional designer operation still require runtime acceptance.

| Default ship | 2006 / 2020 IC | 2006 / 2020 fuel coefficient | 2006 / 2020 crew | Continuing production-line materials |
|---|---:|---:|---:|---|
| Escort | 2,460 / 3,462 | 9 / 10.5 | 240 / 240 | Steel 5, aluminium 3, chromium 1 |
| Patrol cruiser | 4,370 / 6,056 | 18 / 21 | 850 / 850 | Steel 5, chromium 3, tungsten 1, aluminium 3 |
| Fleet combatant | 5,320 / 7,354 | 18 / 21 | 1,100 / 1,100 | Steel 5, chromium 3, tungsten 1, aluminium 3 |
| Patrol submarine | 1,700 / 2,357 | 4 / 4.75 | 100 / 100 | Steel 3, chromium 1 |
| Carrier | 9,920 / 13,460 | 26 / 29 | 2,400 / 2,550 | Steel 6, chromium 3, aluminium 3 |

These are native equipment coefficients and continuing line-resource requirements, not instantaneous treasury bills. Output, national modifiers, trade, fuel tempo, repair and real construction time remain separate. No industry or resources are added to fund future ships. New priorities increase above each captured effective parent, including submarine priority 2,500. Default physical cost/material/crew/stat parity is independently replayed from actual equipment/modules; it is not a promise about every optional loadout.

## Mission and detection boundaries

Sonar supplies `sub_detection`; depth charges supply `sub_attack`. The primary defines contain reference sub-hunter thresholds of 15 attack and 2 detection, plus a reworked detection/visibility formula whose older predecessors are marked deprecated. The worksheet reports statistics and numerical reference margins. It does not certify native sub-hunter selection, spotting, reveal probability, escort effectiveness or delivered damage.

Patrol submarines have torpedo attack for the supported surface-interdiction role, with zero underwater `sub_attack`; no submarine-versus-submarine warfare is claimed. Carrier deck capacity uses the captured native increment of ten aircraft per `carrier_size` point: the defaults provide coefficients 6–9, corresponding to 60–90 source capacity. No wings are supplied. Carrier aircraft must still be researched and manufactured through the existing eligible routes; the aviation packet did not add a modern carrier air group.

Inherited mining and other optional modules remain available under their existing research and DLC contracts. A bare new default fit does not establish equal mining missions with MTG disabled. Mixed optional averaged batteries are rejected by the bounded arithmetic instead of being silently summed; native aggregation and those loadouts require acceptance. No guided-missile, nuclear, strategic-weapon, replenishment-at-sea or per-hull maintenance mechanic is introduced.

## AI and fiscal ownership

Research/design priorities activate after 2005, and each new design requires the appropriate dated role and Systems research plus MTG. Their eligible design-group base of 6,000 exceeds the captured generic base priorities, including destroyer 2,500 and escort 1,000; zero-priority guards remain active before eligibility. This is an authored preference, not proof against every conditional national modifier or native selection. Actual native naval role IDs direct escort, light-cruiser, heavy-cruiser, submarine and carrier weighting. Replacement role weighting requires more than two existing dockyards, or more than nine for carriers. It is a weighting, not a reserved production line or capacity grant. Natural research, XP/design creation, queue selection, refitting and replacement behavior remain untested.

The existing fiscal owner remains unchanged. `num_ships` supplies one commissioned-ship base; carrier and submarine queries supply their existing premiums. Actual-owner fixtures bill every native class and its source crew, preserve the intended base-plus-premium behavior and show that AA/capital/screen tags do not create extra invoices. Disabled fiscal mode remains inert. No stockpiled hulls, synthetic per-hull telemetry, new archetype, additional fiscal coefficient or independent account writer is added.

## Original artwork and actual controls

The original procedural master and **250 editable SVGs** package **273 RGBA8 DDS textures and 333 sprite bindings**. These include 24 distinct research compositions, 20 ship views, 64 component icons, 20 bare top views, 142 cropped normal/highlight category layers, a four-frame tab, a navy background and an explicitly transparent technical background. Complete and designer defaults intentionally share their physical ship illustrations. Icons are fitted to their own subject bounds for readability; full designer images retain their native coordinate space.

Ship blueprint containers are **512×260** and their top-view image is **508×248** at `(0,0)`. They retain `equipment_image`, `module_slots`, the actual slot/category subcontrols and normal/`@highlight` bindings. Cropped category layers retain their own primary dimensions; they are not stretched full-size overlays. The consumer validator restores only the declared new names/sprite substitutions, then compares the complete original blueprint AST, including geometry. It checks actual DDS frames, scale and alpha apertures against actual controls, and verifies that each selected default category has both normal and highlight imagery. A few literal native `@highlight` alternatives are retained exactly rather than renamed.

All imagery is original navy/cyan/light geometric artwork, with no engine pixels, national portraits, watermarks or yellow artifacts. `assets.json` records provenance, dimensions, frame widths, alpha extrema/apertures, source SVGs, SHA-256 and every binding. DDS/SVG/GFX/manifests remain exact-byte reproducible. PNG review artifacts compare dimensions and decoded RGBA pixels, allowing compression differences without accepting changed art.

The new page preserves real native drag, wheel and horizontal/vertical scrollbar bindings. No captured native research-search binding exists, so no decorative search field is added. All three required display geometries are checked offline. The common GUI uses the existing authored ACBriefing/ACResearch resources: 301 protected inherited font assignments and 342 total composed assignments. Raw FNT bytes remain their exact committed LF representation; DDS hashes remain raw.

## Retained surfaces and acceptance

The package preserves and inventories **32 legacy naval, 40 MTG hull and 47 MTG support technology definitions**. Their old IDs, labels, unlocks and 1922–1999/2000 dates remain. Battleship/battlecruiser modernization, older imagery, native 3D ships and attachments, naval doctrines, MIO identities, convoys/support vessels and specialized advanced systems remain separate work. This additive page is not completion of the whole anti-vanilla military conversion.

The 1,110-source preservation manifest pins existing histories, equipment, technologies, defines, on-actions and authoritative owner scripts. A legitimate upstream owner change requires an enumerated reviewed exception and its generator proof; never repin the whole manifest merely to make a check pass.

The composed review branch retains that original manifest. It accepts only the two already-reviewed release-account updates recorded in `tools/air_program/reviewed_owner_updates.json`: `ac_economy_compat.txt` and `ac_macro_effects.txt`. Each must match its exact original and replacement hash. The AIR composition test also checks all 53 unchanged functions, the four specifically added/changed functions, no removed functions and canonical generator output. All other 1,108 captured sources remain exact. This admits the release account's zero-seed adoption and guarded payment contract; it does not authorize a new naval financial writer or a general source exception.

The evidence directory contains original-art galleries, actual default-category composites and a reconstruction of the shipped research page using real coordinates, sprites, localization and BMFont metrics. These are **offline artifacts**, not native screenshots. Native testing remains paused.

| Required native area | Still-open acceptance |
|---|---|
| Displays | 3440×1440/1.0, 1920×1080/1.0 and 2560×1440/1.25; tab discovery, 24 nodes, detail scrolling, tooltips, keyboard controls, drag and both scrollbars |
| DLC | MTG on/off and independent BBA/NSB/La Résistance combinations; actual activated packs rather than source switches |
| Construction/designer | All complete ships and default designs, researched components, XP, required slots, count limits, categories, classification, ordinary upgrades and paid refits |
| Presentation | All 20 top views, default and optional category states/highlights, cropped alpha apertures, interface pictures and inherited 3D fallback disposition |
| Operations | Screening/escort, surface combat, torpedo interdiction, patrol, spotting/reveals and depth-charge damage; explicit mining and subcombat gaps |
| Carrier | Actual 60–90 default capacity, existing eligible air groups, deck operation, crews, losses and repair; no modern air-group equivalence assumed |
| Industry and AI | Real material/fuel/crew demands, funded queue retention, research/XP/design choice, line allocation and natural replacement pacing |
| Fiscal | Native commissioned-ship/type/crew query semantics, base plus intended premiums, no duplicate classifications, disabled economy and no stockpile bill |
| Starts and saves | All 61 current starts; old fleets/queues/variants retained, no late grants, ongoing designs/research, save/reload and natural 2006/2010/2015/2020 checkpoints |

Publication, merging, normal-install synchronization and release acceptance are separate actions.
