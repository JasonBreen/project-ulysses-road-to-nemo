# Active-world foundation calibration

All numbers below are provisional gameplay, not canonical national output, population, order of battle or resource geography. Existing individual buildings, forces, capitals and identities are retained. Additions are explicitly bounded. Native acceptance remains paused.

The integrated source baseline is `60ec3a6` (P1 `8a96ff0` plus ERU `13c8e48`). The branch-sensitive intake covers 61 active histories and four BBA/MTG projections; PLH/state 171 and seven emergent histories are excluded from new-start grants.

## First three priority starts

| Country | Retained CIV/MIL/docks | Target total | New force calibration | Source comparison |
|---|---:|---:|---|---|
|FCU|2/1/0|24/14/6|12 formations, 160 fighters, 48 support aircraft, 8 escorts/3 submarines|Federation core; approved role calibration at existing Emmerian industrial order|
|YUK|7/7/0|80/45/18|60 formations, 600 fighters/144 support/96 tactical aircraft;70 conventional ships|OSE retains 73 formations, 882 legacy/932 BBA planes and 229 active designer ships; new YUK replaces missing foundations without changing Osea|
|NPT|17/11/15|17/11/15|8 infantry formations, 72 fighters/12 support, 6 escorts/2 submarines|Retained industry; bounded island defense and merchant logistics|

The first three rows are implemented and pass actual four-DLC source, equipment, production, topology and preservation checks. Their detailed technical contract and primary worksheet are in `tools/world_starts/foundation.json` and `sustainment.json`. Native acceptance is still pending; the 25-country table below is now implemented as a second source slice, with explicit replacement-backed adjustments. Other incomplete active starts remain pending. Existing OSE/BLK/SAP army and industry budgets remain preserved. Known intake defects include Osea selecting its designer navy in the non-MTG branch, FATO's malformed legacy naval quote, FATO AI-line requests above its military capacity and Belkan naval-line requests above its yard capacity. Repairs will retain the active force and supply a valid comparable missing route, with explicit before/after counts.

## Twenty-five industry-empty active countries

These implemented totals are not blanket national-strength rankings. Roles describe the authored gameplay package on inherited geography. All need real per-role equipment/replacement and resource/fuel worksheets. Civil-defense starts intentionally have no invented standing combat aviation or combat navy; port access and merchant supply are separate capabilities.

| Country | CIV/MIL/docks | Formations | Fighters/CAS | Escorts/submarines | Gameplay role |
|---|---:|---:|---:|---:|---|
|NEC — Nordennavic|20/10/6|14|144/24|8/3|regional maritime reserve|
|WEL — Wellow|16/8/6|10|120/24|8/2|dispersed maritime trade|
|SOA — Sotoa|14/7/3|10|96/12|4/2|regional combined services|
|AZB — Azbekerania|12/6/2|8|72/12|2/0|continental reserve|
|ESN — Silvonia|10/6/2|7|48/12|2/0|territorial air defense|
|GLA — Glaceland|12/6/4|8|72/12|5/2|dispersed coastal support|
|NIH — Nihon|10/6/4|6|72/12|5/2|island service network|
|LEA — Leasath|12/7/3|10|96/24|4/2|regional readiness|
|VER — Verusa|10/6/3|7|60/12|3/1|land and coastal reserve|
|PLA — Platania|10/6/3|6|60/12|3/1|regional transport and defense|
|ECH — Echinata|9/6/2|5|48/12|3/0|coastal service capacity|
|SCA — Scandia|8/5/3|5|48/0|4/1|dispersed air and sea defense|
|SFA — Sfaenland|8/6/3|6|36/12|2/1|territorial readiness|
|CHO — Chopinburg|8/5/3|6|48/0|3/1|coastal dispersal|
|ROH — Rohden|8/6/3|5|36/12|2/1|limited combined defense|
|AEM — Aemurraq|7/5/2|4|36/0|2/0|merchant route security|
|KLG — Kaluga|6/5/2|4|24/0|1/0|limited coastal defense|
|EHE — Echea|6/5/2|4|24/0|2/0|small coastal service|
|CAL — Calladen|6/5/2|4|24/0|1/0|territorial guard|
|RJR — Roca Roja|5/5/2|3|24/0|1/0|local route security|
|SET — Seterano|5/5/2|3|12/0|1/0|small service budget|
|RMN — Romny|5/5/0|4|12/0|0/0|limited air and territorial guard|
|CRS — Corscae|4/3/0|3|0/0|0/0|civil defense; no invented combat air/navy|
|MAY — Malynea|3/3/1|2|0/0|0/0|island civil defense and merchant receiving|
|VLK — Valka|4/3/0|2|0/0|0/0|small civil-defense service|

Industry is added only to reviewed owned industrial/port terminals; island receiving facilities do not imply free new island industry. No cross-water railway, faction grant, forced war, leader change or old-save grant is introduced. The existing seven authored foundations remain under their owning generators. Other inherited starts receive missing capabilities rather than duplicate armies.

The frozen `empty_calibration_draft.json` records the intake proposal. The delivered profile records each upward MIL/yard adjustment in `calibration_review`: an aircraft start has rifle, engineer-support, truck, train and each aircraft-role line; a standing combat navy has a convoy line plus each hull class. The three civil-defense roles instead have three military lines (rifle/truck/train), four-battalion infantry, no unsupported support companies and no combat aviation or navy. Malynea alone has a merchant convoy yard. Convoy-only OOBs contain production without an empty fleet; aircraft-free countries have no air OOB at all.

The registry retains raw false capability observations and separately records the explicit reviewed role dispositions. Removing a disposition makes the source gap visible again. It does not claim every country has aircraft or ships. All resource additions are bounded gameplay allocations for actual line inputs after conservative default exports; full-tempo fuel arithmetic remains a sensitivity rather than a promise of unlimited operations. The 25-country component receives no free imported army, fictitious procurement contract or automated old-save grant.

## Fifteen inherited-industry starts without a standing roster

These countries keep every inherited civilian factory and yard at its original state. Missing military lines are additive; their sizes follow actual replacement roles rather than an equal allocation. DOR/MST retain zero yards and receive no invented combat navy. AQU/BAL/GIB/LUR have infantry and transport lines without unsupported combat aviation or engineer companies. Their source role dispositions remain explicit in the registry.

| Country | Inherited CIV/MIL/yards | Target CIV/MIL/yards | Formations | Fighters/CAS | Escorts/submarines |
|---|---:|---:|---:|---:|---:|
|ALR — Albard|14/6/9|14/8/9|8|72/12|6/2|
|AQU — Aquitoria|3/2/0|3/3/0|2|0/0|0/0|
|ARK — Arklith|15/3/20|15/8/20|8|96/24|8/4|
|AUR — Aurelia|25/5/9|25/10/9|14|120/24|8/3|
|BAL — Baltica|2/2/0|2/3/0|2|0/0|0/0|
|BLD — Bulgurdarest|11/5/3|11/6/3|8|60/12|3/1|
|CSO — Central Sotoa|4/4/0|4/5/0|3|24/0|0/0|
|DAK — Dakrain|4/4/2|4/5/2|4|24/0|1/0|
|DOR — Dorondo|10/10/0|10/13/0|8|72/12|0/0|
|FRU — Ferustia|5/4/0|5/5/0|6|36/0|0/0|
|GIB — Gibraltar|2/0/0|2/3/0|2|0/0|0/0|
|LUR — Luremia|5/1/0|5/3/0|3|0/0|0/0|
|MST — Monstrua|10/10/0|10/10/0|8|72/12|0/0|
|SLA — Slavia|2/5/0|2/5/0|2|12/0|0/0|
|VOS — Voslage|5/3/2|5/5/2|6|36/0|1/0|

All additions are provisional gameplay. Actual deployment, required equipment and module unlocks, simultaneous line allocations, stocks, full opening fuel, scoped AI, retained identity and owned-component routes are tested. The four BBA/MTG projections establish source coverage only. No armored units are introduced by this fifteen-country slice. The following sections document retained-army compatibility and integrated legacy-owner support, including explicit NSB/LaR boundaries. Native acceptance remains pending.

## Seven retained-army starts

The original land files remain untouched as provenance and saved reference targets. New country histories select one composed land roster, containing every inherited formation and cumulative units block, instead of loading the original and an additional army. Formation name/order metadata, deployment provinces, experience and equipment factors are preserved. Supply routes reach the retained deployment locations. Original politics, leaders, ideas, relationships and fiscal eligibility markers stay under their existing owners.

| Country | Retained CIV/MIL/yards | Target CIV/MIL/yards | Preserved formations | Starting service aircraft | Combat ships |
|---|---:|---:|---:|---:|---:|
|GEB|10/5/0|10/6/0|10|1 retained bomber|0|
|UST|8/4/0|8/7/0|9|50 fighters,15 support|0|
|NRL|18/3/11|18/10/11|15|72 fighters,12 support|8|
|PBL|24/16/6|24/24/6|29|96 fighters,24 support|7|
|RAT|11/6/4|11/10/4|12|48 fighters,12 support|4|
|SYC|3/1/4|3/8/4|7|24 fighters,12 support|3|
|WIE|8/5/3|8/11/3|14|48 fighters,12 support|3|

GEB's single training bomber remains a single aircraft; its existing air-force-development content remains relevant. PBL's original sixteen assigned military lines retain their allocations; eight added lines cover previously unsupported support/carrier/SPG/rocket and aviation roles. No formations are removed. Two undefined PBL `medium_sp_artillery` support entries (Heavy Infantry and Mechanized Brigade) become valid `medium_sp_artillery_brigade` regiments in free slot2,0. Undefined `xxx` and foreign `GER_Arm_01` naming groups become numbered template-matching groups while preserving formation order metadata. These are bounded validity repairs to inherited mod content, not new official military history.

## Armor compatibility and extra DLC boundaries

The core matrix is four BBA/MTG combinations. YUK/NRL/PBL/RAT/SYC/WIE also have four additional NSB-enabled source cases, bringing this owner's fifty profiles to224cases. The mod's inherited `common/technologies/NSB_armor.txt` is entirely commented; designer chassis/module presence in the installed catalog alone does not establish an unlock. Three narrow history-only, unresearchable/no-folder `ac_ws_nsb_*_support` technologies therefore unlock only the actual chassis, required modules and subunit for a fielded service role. No general armor technology tree or visible research screen is restored. NSB-off retains the existing technical legacy types; NSB-on creates matching owned variants before stocks and land production load.

`armor.py` maps provisional service recipes to installed1.19.4.1 `common/units/equipment/tank_chassis.txt`, `x_tank_chassis.txt`, `common/units/equipment/modules/00_tank_modules.txt` and the relevant subset of `common/technologies/NSB_armor.txt`. The metadata records exact effective source hashes, required slot/category contracts, costs, resources (including module build-cost resources), fuel coefficients, equipment archetypes and unlock order. Parent-slot `inherit`, whole-slot-map inheritance and same-hull slot aliases are resolved; wrong slot categories fail. Counts and broad roles are comparable; raw designer/legacy statistics are reported separately rather than asserted equal. Native designer behavior is not established by these source cases.

PBL's retained IMV role uses the existing mod `imv1` compatibility technology and base technical armored-car equipment. Its La Resistance enabled/disabled source boundary remains an explicit release gate; hard-coded DLC availability is not inferred merely from an authored technology definition. Legacy-owner BLK/OSE/SAP/FAT repairs and all four countries' logistics/resource worksheets are now integrated through exact local source receipts. All 61 active countries having industry does not mean all 61 starts have completed every DLC/native acceptance gate.

## Reviewed capacity and personnel constraints

The implementation now allocates NEW industry/resources only on owned-core states. YUK's two inherited KLG-core states keep their identities and receive no new industrial/resource allocations. DOR retains its 3 non-core MIL in 487, excludes them from usable startup capacity, and adds 3 core MIL:13 physical / 10 conservative usable core MIL. Known non-core-controller slot/factory/resource modifiers are source-recorded; the worksheets do not assume compliance rounding. Rail output retains all inherited edges and levels and emits only new edges, preserving higher-level infrastructure without relying on duplicate-row precedence.

`policies.py` captures literal actual opening laws, ideas and relevant technology effects. FRU's 75% exports and 50% resource penalty remain; Al 4 / steel 6 industrial imports require 2 CIV under the read-only primary resource terms, matching the conservative allowance after rounded consumer goods. No free trade deal, new faction or actual delivered supply is assumed. UST's resource/consumer-goods/manpower penalties remain; its small remaining steel shortfall gets bounded core allocation because its conservative trade-CIV allowance is zero. Fuel income and replacement production now use these actual policies; full-activity import pressure and conservative reserve scenarios are reported separately.

`personnel.py` reads actual selected OOBs, primary subunit/equipment personnel, retained core populations and opening laws/ideas. New starts must fit a 10% deployed-personnel replacement reserve. CSO uses3 four-battalion formations (13,380 total deployed including aircraft; 1,338 reserve against 15,000 pool), MST five-battalion formations and SLA four-battalion formations. No population or conscription-law grant is used. UST retains its 9 authored formations and 65 aircraft but fails this source budget because of its inherited combined negative conscription factors. That liability is explicitly exposed in the 69-country registry and [release checklist](WORLD_STARTS_ACCEPTANCE.md); it is not reduced to a native-pending note or a universal green claim. Existing conditional reform-route source bindings are checked, while natural access/pacing remains pending.

The offline policy parser lists three unrelated installed country files using unsupported preprocessing syntax. None supplies an active/default idea in these fifty histories; any unresolved required policy fails closed. Relevant effective mod inputs are hash-checked offline, changed history policies require explicit recapture, and primary-reference runs recompute the actual policy/technical data.

## Retained large-force starts: physical support and bounded inputs

BLK/OSE/SAP/FAT keep every individual inherited factory, resource floor, core,
population, capital and force identity. `tools/world_legacy` owns their actual
history/OOB, designer/legacy and replacement repairs. The separate
`tools/world_starts/legacy_foundation.py` adapter writes only state/logistics
outputs, and requires exact local receipts for that force component. Its
per-case technical data are recomputed from the effective read-only 1.19.4.1
primary definitions; no installed art/model/script package is copied.

| Country | Retained CIV/MIL/yards | Added base resources | Industrial import CIV margin, worst source case |
|---|---:|---|---:|
| BLK | 43/45/12 | oil 64, tungsten 11, chromium 54 | 0 |
| OSE | 117/50/23 | none | 7 |
| SAP | 18/8/8 | oil 24, aluminium 10, rubber 4, chromium 10 | 0 |
| FAT | 13/12/6 | oil 16 | 3 |

These resource additions are provisional production calibration, not official
mineral geography. Existing Osean resources remain sufficient for its bounded
industrial import allowance; no oil is added there. All four retain their real
opening economic/trade/conscription laws and spirits. Industrial imports use
the primary resource-specific `cic` terms and conservative core CIV after
rounded consumer goods. No trade contract or delivered resource is granted.
Fuel imports and reduced operational tempo remain separate continuing costs.
The worksheet's simultaneous full-establishment army proxy, whole-air-force and
whole-navy reference can require 73–93 oil imports for BLK, 123–168 for OSE,
93–113 for SAP, and 18–33 for FAT across the recorded DLC cases. Those stress
cases can exceed available trade CIV. They are not a promise of continuous
all-force combat. The guaranteed base storage alone covers roughly 9.02, 4.97,
13.84 and 31.85 days respectively in the worst net stress case, excluding
positive silo storage and bonuses; the actual opening grant fills fuel to the
country's storage capacity under the force owner. Native consumption,
aggregation, delivered oil and shipping throughput remain unobserved.

Source production output is reported at an explicit half-MIL-efficiency
reference scenario, independent of the authored queue's numeric efficiency.
Installed primary GER/USA OOBs use 50 and inherited mod queues use 25/50, while
effects documentation contains a fractional example. Preserve inherited convention and
record the discrepancy; neither an observed native unit nor a 100-fold output
change is asserted. Progress values above one receive the force owner's
documented provisional normalization, with native acceptance still open.

Every selected land deployment, actual fleet home port, state airfield and
inherited industrial district receives an owned-land route to its component's
capital/receiving terminal. Existing airport coordinates serve as declared
industrial logistics anchors; they are not moved. Disconnected components use
existing valid sea-spawn geometry rather than cross-water rails. Higher-level
inherited rail rows remain immutable. This also extends the fifty-profile
adapter to connect every original industrial district, without changing its
factory placement.

BLK retains one narrowly identified sealed component: provinces 1939, 5906,
7545, 7569, 7570, 7595 and 7603 in state 309 are isolated by inherited impassable
adjacencies, with no sea coast/spawn. The whole state's 101,046 population,
BLK/UST cores, original industry/resources and geography remain untouched. None
of those seven provinces hosts an actual required starting formation, airfield,
port, hub, industrial or resource target. The entire state is excluded from new
allocations to avoid a shared-state assumption. This is an inherited sealed-area
limitation with no required starting dependency, not a claim that it is empty or
that every geographic component is universally connected.

The integrated release report must bind the force component's 80 source cases:
40 BBA/MTG/NSB/FATO-context cases with La Resistance present, plus 40 explicitly
open La Resistance-disabled reconnaissance cases. Source NSB recipes and
replacement unlocks do not certify native initialization or mission behavior.
PBL's retained armored-car availability remains a separate recorded extra-DLC
boundary. `coverage.json` preserves all these limits together with UST's source
reinforcement debt; no universal sustainable-start pass is claimed.
