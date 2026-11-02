# Aviation implementation ledger

The conventional aviation packet is **provisional gameplay**, implemented in the `ac_air_` namespace. Its exact specifications and dates are authored balance values, not official ACES chronology or real aircraft data. Source base: composed review parent `549cad986c630334d398beb2e11c8e23939f3990`; reviewed font API: `5b4a25d243bfbf9012869d4a6da1874317c64fe4`.

| Claim or contract | Source layer and exact reference | Affected implementation | Status and limit |
|---|---|---|---|
| Six research families dated 2006/2010/2015/2020 | Provisional gameplay; `tools/air_program/air_content.py` | `ac_air_{systems,fighter,strike,maritime,transport,surveillance}_<year>` | Implemented source; natural progression untested |
| Complete aircraft and designer defaults | Provisional gameplay statistics; effective installed 1.19.4.1 inheritance captured in `primary_contract.json` | `zz_ac_air_equipment.txt`, `zz_ac_air_modules.txt` | 20 complete models, 16 frames, 32 modules; required slots, repeated limits, thrust, materials and costs checked |
| Existing air foundations and 1991 rosters | Mod provenance; original 1,107 hashes retained in `preserved_sources.json` | Existing country histories, OOBs, technologies, equipment and strategic owners | All technical/history sources unchanged; two separately reviewed financial-owner exceptions documented below; no early/late grants |
| Engine equipment/mission/designer grammar | Installed primary reference, exact per-file SHA-256 in `primary_contract.json.source_sha256`; `plane_airframes.txt`, `x_plane_airframes.txt`, `quad_engine_airframe.txt`, `00_plane_modules.txt`, `plane_blueprints_generic.gui` | Ordered effective replay in `air_primary.py` | Loose-file source evidence; no native designer/mission acceptance |
| AI design and paid production grammar | Same primary capture; `common/ai_equipment/_documentation.md`, `generic_planes.txt`, `common/ai_strategy/default.txt`, `documentation/dynamic_variables_documentation.md` | `ac_air_designs`, replacements and research plan | Dated researched gates; native selection/XP/queue behavior untested |
| La Résistance reconnaissance and transport boundaries | Captured predecessor technologies/archetypes and native mission declarations | Surveillance gates; one complete transport route | Disabled-recon gap explicit; no invented AEW/AAR/ASW behavior or per-wing telemetry |
| Maritime mine capability difference | Captured legacy predecessor mission list versus actual three-component BBA default | `capabilities.json.default_physical_parity` | Legacy mining declarations retained; default modular recipe does not claim equivalent mine capability |
| Fiscal observation ownership | Existing `tools/economy_v2` generated owner and real-owner fixtures | Native air archetype/type inheritance | Existing base plus one maximum role pool; no additional coefficient or custom fiscal writer |
| Reviewed release-account composition | Release component `578db157`; exact two-file/version and function proofs in `reviewed_owner_updates.json` | Existing compatibility/macro initializers and two public adapters | Other 1,105 captured files and 53 unchanged functions remain pinned; canonical generator and release-finance checks pass |
| Original technical art | Original procedural authoring; `build_art.py`, 56 editable SVGs and `assets.json` | 94 DDS, 146 sprite bindings, 16 actual 508×248 blueprint consumers | Offline art reviewed; native rendering remains untested |
| Common research UI and fonts | Captured original whole-AST contract plus reviewed font migration | AIR/LAND pure extension and strict normalization | Both generator orders checked; no original capture refresh or unbound search control |
| Older air surfaces | Mod provenance; exact 38 legacy and 41 BBA definitions inventoried in `capabilities.json` | Existing tabs, IDs, equipment unlocks and labels | Retained; old hardware, labels, models and attachments remain a separate conversion backlog |

The editable source, reproduction commands, physical-stat table, route differences and native acceptance matrix are in [the packet README](../tools/air_program/README.md). Retained checks and explicitly labelled reconstructions are in [the evidence directory](evidence/air-program/README.md). No official portrait, flag, aircraft programme biography or post-2020 war is created by this packet.

The current review stack's exact-source phases and original component results
are distinguished in [the integration record](evidence/air-program/integration/README.md).
