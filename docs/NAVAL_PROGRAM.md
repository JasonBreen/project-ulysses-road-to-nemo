# Conventional naval implementation ledger

This is a **provisional gameplay** hardware/research packet, not official chronology or a declaration of native acceptance. New identifiers use `ac_naval_`; no country identities, leaders, borders, histories, factions or strategic-project owners are introduced.

| Claim or contract | Source layer and exact reference | Implementation | Disposition |
|---|---|---|---|
| Six dated families through 2020 | Provisional gameplay; `tools/naval_program/naval_content.py` | 24 techs, 20 complete ships, 20 hulls, 64 modules | Authored source; natural progression untested |
| Native slots, repeated limits and aliases | Installed 1.19.4.1 primary; `common/units/equipment/ship_hull_{light,cruiser,submarine,carrier}.txt`, exact hashes and ordered ASTs in `primary_contract.json` | `naval_primary.py`, explicit selected defaults | Required/category/count/default tests; no old definitions overwritten |
| Native defaults contribute once | Same primary complete models and explicit `default_modules`; deck manpower in `00_ship_modules.txt:2622` | Same bare hull plus explicit recipe in both routes | Independent source parity and double-contribution negative fixture |
| Cruiser role promotion | `00_ship_modules.txt`, medium-battery `add_equipment_type = capital_ship`, exact captured bodies/hashes | Native screening hull plus selected heavy battery | Default and optional source classification checked; native operation untested |
| Detection and depth-charge distinction | `00_ship_modules.txt`, sonar/depth-charge definitions; `00_defines.lua:2125–2126,2185–2188` | Detection and attack statistics; numerical reference margins | No spotting, reveal or subcombat equivalence claim |
| Carrier capacity and crew | `00_defines.lua:1338`; `ship_deck_space` manpower outside `add_stats` | Researched deck capacity 6–9; manufactured ship and separate existing air group | 60–90 source capacity; no aircraft grants or modern air-group claim |
| Native AI roles and design grammar | `common/ai_equipment/_documentation.md`, `generic_naval.txt`, `common/ai_strategy/default.txt`, captured exact hashes | Dated researched designs and existing-yard role weighting | No free ship/line; native XP/selection/refit untested |
| Ship fiscal observations | `documentation/dynamic_variables_documentation.md:677–681`; existing `tools/economy_v2/forces.py` and actual owner fixtures | Commissioned base plus existing carrier/submarine premiums and crew | No new fiscal writer, coefficient or per-hull simulation |
| Original technical art | Original procedural source, 250 SVGs, `assets.json` | 273 DDS / 333 bindings, including native-shaped normal/highlight patches | No engine/external pixels; offline reviewed |
| Designer controls | `interface/equipmentdesigner/ships/ship_hull_*.gui`, original structure captured with dimensions/hashes | 512×260 controls, 508×248 top views and cropped category layers | Actual consumer/frame/scale/aperture/selected-binding validation |
| Research composition/fonts | Immutable LAND/AIR captures and pre-NAVAL capture, strict reviewed font migration | All six generator orders, original whole-AST restoration | No capture refresh, new alias or fake search |
| Existing starts and old surfaces | Mod provenance; original 1,110-source preservation manifest; 32/40/47 older naval definitions inventoried | Existing fleets, queues, variants, technologies and owners | 1,108 exact sources plus two individually hashed, generator-checked release-account updates; older imagery, models, doctrines and specialized families remain backlog |

The [packet README](../tools/naval_program/README.md) contains reproduction, physical values, DLC limits and the native acceptance matrix. The [evidence directory](evidence/naval-program/README.md) distinguishes source checks, loose-file contracts and offline reconstructions. Source green does not establish native naval or campaign acceptance.
