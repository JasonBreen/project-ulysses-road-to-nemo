# Land Systems review evidence

**Source/offline status:** all14 retained check groups pass for the working-tree candidate based on `224c9ccb23f7745d1829b334c5f901c897e83c72`. **Native acceptance:** untested and paused. No game, desktop, normal installation or user saves were used.

The authoring, reproduction commands, gameplay contract, retained older surfaces and native acceptance matrix are in [the implementation ledger](../../../tools/land_program/README.md). The primary capture reports installed loose-file version1.19.4.1; that is a definition/provenance observation, not a live engine acceptance result.

Review these artifacts:

- [Actual-coordinate research-page reconstruction](research-page.png) and [geometry findings](research-page.json):32nodes, zero text/bounds findings, three specified logical viewport configurations. Explicitly offline and illustrative research states.
- [Original research/module/counter gallery](asset-gallery.png), [complete-equipment gallery](equipment-gallery.png) and [asset index](asset-gallery.html). All authored technical compositions were visually reviewed; scripted checks inspect dimensions, frame differences, alpha, palette, source hashes and sprite consumers. No yellow watermark or label is baked into delivered DDS.
- [Retained check results](results.json), with per-group logs below. These are not native screenshots, natural progression, save serialization or observed designer operation.
- [Capability worksheet](../../../tools/land_program/capabilities.json):12date/NSB profiles,16independent DLC-switch profiles, eight default physical-recipe parity comparisons, eight optional optics/radio recipes and eight supplied-company packages. These are explicit source calculations and unlock checks.
- [Primary definition contract](../../../tools/land_program/primary_contract.json), [asset manifest](../../../tools/land_program/assets.json), [old-source contract](../../../tools/land_program/preserved_sources.json) and [GUI exception contract](../../../tools/land_program/ui_contract.json).

| Check group | Evidence |
|---|---|
| LAND22: actual definitions, routes, company costs, AI gates, full target stock/technology requirements, effective parent priorities, old-source preservation, fonts, controls, art and regeneration |[land.txt](land.txt)|
| Existing macroeconomy owner and lifecycle |[macro.txt](macro.txt)|
| Upkeep9, including read-only installed contract; LAND separately executes distinct specialist and overlap fixtures |[upkeep.txt](upkeep.txt)|
| World50 primary24, including installed recapture and hash-seed stability |[world-50.txt](world-50.txt)|
| Anea11 foundations with read-only primary definitions |[anea-2.txt](anea-2.txt)|
| Five-country foundation20; its optional reference recapture is skipped in this runner, while50/Anea/land primary gates run with a reference |[world-5.txt](world-5.txt)|
| Legacy16:80NSB/BBA/MTG/LaR-status source profiles and retained source identities |[legacy-4.txt](legacy-4.txt)|
| Six-owner funded replacements14 |[replacements.txt](replacements.txt)|
| All61active country histories /244selected BBA/MTG source cases, exact owner receipts |[all-61-selected-starts.txt](all-61-selected-starts.txt)|
| Existing interface regressions |[interfaces.txt](interfaces.txt)|
| Authored asset audit `--strict-all` |[assets.txt](assets.txt)|
| Composed macro generated output |[generated-macro.txt](generated-macro.txt)|
| Captured effective LAND worksheet consistency |[capability-contract.txt](capability-contract.txt)|
| Full static/source/map/reference validation |[static.txt](static.txt)|

## Claim and provenance ledger

| Claim / IDs | Source layer and exact reference | Disposition / conflict boundary |
|---|---|---|
| Eight families, dated2006/2010/2015/2020, all `ac_land_*` model/module names and balance values |Provisional gameplay; approved modern-land programme; editable values in `tools/land_program/land_content.py` and `build.py` |Implemented in source. No claim of canonical procurement, named national hardware or official technical performance |
| Native technology `allow`, dependencies, equipment/module/subunit unlocks, inherited equipment and default slots |Read-only installed1.19.4.1 `common/technologies/infantry.txt`, `support.txt`, `common/units/equipment/{tank_chassis,x_tank_chassis,infantry,support,motorized,mechanized}.txt`, `modules/00_tank_modules.txt`; normalized hashes and effective definitions in the primary contract |Adapted with additive IDs and authored values. Source-valid default recipes; native design creation and production remain untested |
| AI native design roles, archetype buffer allocation and supplied-template grammar |Installed `common/ai_equipment/{_documentation.md,generic_tank.txt}`, `common/ai_templates/_documentation.md`, and `common/ai_strategy/default.txt` (`default_produce_some_trucks_for_buffer`); exact hashes in the contract |Adapted, with no free stock, industry or early variants. Natural selection, XP spending, queue retention and deployment are untested |
| Starting equipment, World hidden armor bridge, all old rosters/history files |Mod provenance at224c9; `preserved_sources.json`, actual61-start/244case checks and retained owner fixtures |Preserved. Separate legitimate-release history changes must be reviewed and composed explicitly rather than hidden by a blanket hash refresh |
| Specialist upkeep |Existing provisional macro cost owner; `tools/economy_v2/{forces.py,force_observables.json}` and generated `ac_macro_effects.txt` |Exactly two distinct archetypes added to the support pool at its existing coefficient. Actual-owner fixtures pass; native observation semantics remain unverified |
| 106technical DDS /158sprite bindings /68editable SVGs |Original code-native geometry in `build_art.py`; `assets.json` hashes every delivered DDS and editable export |Implemented and reviewed offline. No installed/external pixels; inherited3D entities and older presentation remain backlog |
| New folder and detail scrolling |Mod provenance captured in `source/research_base.gui`; narrow GUI AST exception contract |Implemented with actual engine control names; no invented search binding. Native tab discovery, scaling and scrolling are untested |

There is no merged-country, faction, border, strategic weapon or new leader contract in this packet. The inherited Infantry/Support/Armor/Artillery/Electronics tabs remain reachable. Their exact old IDs and dates are inventoried rather than described as converted.
