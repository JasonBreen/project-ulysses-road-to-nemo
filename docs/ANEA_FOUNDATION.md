# Anea starting-country foundation

Implemented source and offline validation; **native acceptance remains open**.
The implementation base is `cf8fec41abe5080b1af66eb86189b35c7af522f6`.
No installed mod, normal profile, user save or display configuration is changed.

## Provenance and boundaries

| Subject | Source layer | Exact reference | Disposition |
| --- | --- | --- | --- |
| EMM/EVA tags, owned provinces, borders, cores and manpower | Mod provenance | Base commit's `history/countries/EMM - Emmeria.txt`, `EVA - Estovakia.txt`, their 76 owned state histories and `map/provinces.bmp` | Preserved; the inherited million-person-per-state scaffold is not canonical demographic evidence. |
| Capital, industry, ports, supply hubs, railways, resources and regional labels | Provisional gameplay | User-approved Anea foundation plan, 30 October 2026; `tools/anea/foundation.json` | Authored within existing territory. No claim that the provisional capital districts or numbered regional/transport labels map canonical cities. |
| Starting forces, equipment, technologies, political support and economic laws | Provisional gameplay | User-approved playable-country requirement; existing mod/native equipment contracts | Authored for a sustainable mid-power opening. No claim of a historical national order of battle. |
| Existing office characters | User-approved office representation | `tools/usea_expansion/leaders.json`, `common/characters/ac_starting_governments.txt` | Retained. No named 1991 officeholder, election date, term or biography is invented. |
| Technology/module/OOB syntax | Technical compatibility | Existing FATO/Ustio patterns and read-only HOI4 1.19.4.1 effective definitions | Referenced IDs and syntax; no native art, executable or gameplay files copied. |

Nothing edits country ownership, cores, province lists, inherited manpower,
raster data, province definitions, state 171 or unrelated placeholder regions.
The inherited Earth state names are superseded through an English replacement
localization file. A state's numbered provisional label is a presentation aid,
not an assertion of official administrative geography.

## Exact opening calibration

| Item | Emmeria | Estovakia |
| --- | ---: | ---: |
| Owned states / land provinces | 41 / 978 | 35 / 409 |
| Capital state / province | 154 / 3678 | 124 / 6470 |
| Civilian factories | 24 | 20 |
| Military factories | 14 | 16 |
| Dockyards | 6 | 4 |
| Supplied mainland hubs | 6 | 6 |
| Reachable airbase states, level 2 each | 154, 159, 24 | 124, 204, 192 |
| Infantry / mobile / mechanized divisions | 8 / 2 / 2 | 10 / 2 / 2 |
| Fighters / strike aircraft | 160 / 60 | 180 / 60 |
| Patrol cruisers / escorts / coastal submarines | 1 / 6 / 2 | 1 / 4 / 3 |
| Convoys / trains in reserve | 120 / 120 | 120 / 120 |
| Capital fuel silos | 1 | 1 |

Every deployed division starts at an owned supply hub with its own template and
full starting equipment. Six-battalion templates limit the initial force's
manpower, replacement and supply burden. Support engineers, artillery and
logistics are supplied; mobile formations also have motorized reconnaissance.
Stockpiles include 5,000 infantry equipment, 1,000 support equipment, 600
artillery, 1,500 trucks, 600 mechanized vehicles and 30 reserve aircraft per
role. All equipment and corresponding unlocks exist in the selected DLC branch.

Land production requests thirteen Emmerian and fourteen Estovakian military
factories. The selected air roster requests the remaining one or two factories.
The selected naval roster assigns the existing dockyard budget to convoy
replacement. BBA/legacy and MTG/legacy branches provide the same deployed role
counts and never load both rosters. Variants are created before their rosters.

Both countries receive a full initial fuel ratio, one capital fuel silo, basic
refining/storage technology and an abstract 12-unit domestic oil allocation. This permits normal
fuel replenishment; sustained exercises and naval/air deployment can still
require trade or further investment. Steel (24/20), aluminium (12) and tungsten
(4) are deliberately limited balance allocations supporting basic replacement
production. They are not claims of mines, deposits, historical output or a
restored Estovakian offshore facility. Rubber and chromium remain zero. Actual
fuel endurance, trade choices and replacement throughput require native testing.

The inherited ruling democratic group and office character remain. The copied
1930 election fields are removed; elections remain disabled. Starting popularity
(EMM 60 democratic/25 neutral/10 fascist/5 communist; EVA 40/45/10/5), stability,
war support and civilian laws are openly provisional game calibration.

## Geometry, logistics and repeatability

`foundation_map.py` derives land adjacency from shared horizontal/vertical pixel
edges in the inherited province raster, then removes explicit impassable links.
It excludes sea, lake and foreign provinces from every route.

For Estovakia, the largest owned land component is selected by raster area. Its
area-weighted geometric centre determines the nearest state centroid, with state
ID breaking ties: state **124**. Emmeria retains state **154**. A 20-point
provisional capital location and supply hub share the selected capital province;
this gives the state capital an unambiguous supply origin. Other hubs receive
five-point, neutrally numbered logistics-centre labels.

Ports are actual coastal owned-land provinces adjacent to water:

| Country | Port province | State | Starting naval-base level |
| --- | ---: | ---: | ---: |
| EMM | 4666 | 157 | 3 |
| EMM | 294 | 159 | 3 |
| EVA | 1600 | 141 | 3 |
| EVA | 6912 | 204 | 3 |

Level-two railway paths connect each capital to supply hubs, ports and the eight
selected mainland industrial areas. All starting airfields use the inherited
airport placements and are connected by the same network. Detached components
receive basic infrastructure but no artificial foreign-land railway shortcut.
No starting formation is deployed there.

Numeric-only railway/supply-node formats retain a hash-verified inherited prefix;
the appended rows' ownership and adjacency are validated. State building slots
are enlarged only from town to city/large city where the allocated industry
requires it. The generated state/category totals fit the installed reference's
base slot capacities.

The committed manifest records province/state placements, borders/manpower/core
invariants, raster/definition hashes, connected components, all routes and the
inherited logistics-prefix hashes. Regeneration uses Python 3.12+, Pillow and
NumPy (validated locally with Pillow 11.0.0 / NumPy 2.2.6):

```powershell
python -B tools/anea/foundation_map.py
python -B tools/anea/foundation.py
python -B tools/anea/foundation.py --check
python -B tools/anea/test_foundation.py --reference $env:ULYSSES_GAME_ROOT
```

The first command updates the authored placement manifest; use it only when
deliberately reviewing placement changes. `foundation.py --check` and the tests
do not write tracked files. Removing the `--reference` option runs all portable
geometry/setup tests while marking the effective engine unlock test skipped.

## AI and save continuity

EMM/EVA receive separate peacetime, wartime and post-crisis replacement priorities,
plus research plans favouring industry, infantry, support, defensive aviation and
logistics. Priorities are explicitly additive to the inherited generic AI.
The post-crisis posture reads the shared owner's `ac_anea_crisis` flag; it does
not initialize or rewrite regional campaign state. No new diplomatic aggression
or scripted war is introduced.

Country-history forces, production, technology, resources and building histories
are new-campaign setup. No startup/weekly effect loads these rosters into an
existing save. Existing offices remain recruited through the prior generator's
stable marker, and `build_leaders.py --check` remains valid. Any old-save capital
repair belongs to the shared owner's guarded current-eligibility handling;
country-history initialization itself is not replayed.

## Validation and remaining acceptance

Eleven focused offline regressions pass, including the four BBA/MTG combinations
for both countries and installed-reference technology/module unlock checks.
They cover generated bytes, reproducible capital/geometry rules, unchanged
ownership/cores/provinces/manpower, exact industry, slot capacity, true coastal
ports, air capacity, owned-land railway connectivity, supplied land deployment,
comparable DLC rosters, factory conservation, office identity and new-game-only
setup.

Native acceptance is still required for parser execution, actual aircraft/ship
capability, model placements, supply distribution, fuel endurance, reinforcement,
AI deployment/research/construction, trade, saving and loading. The offline tests
are not evidence that these countries have been played in HOI4.
