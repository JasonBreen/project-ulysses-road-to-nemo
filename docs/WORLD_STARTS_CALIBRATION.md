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
