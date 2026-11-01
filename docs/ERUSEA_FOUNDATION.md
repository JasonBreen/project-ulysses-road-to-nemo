# Erusea — additive 1991 force and logistics foundation

This source package fills Erusea's missing starting forces and sustainment. It
extends the world-foundation owner after `fb3e8c3`; it does not add a focus tree,
war, campaign outcome, leader, operational squadron story, border or country tag.
All added forces, equipment configurations, ports, airfields, supply hubs,
resource values and unit names are **provisional gameplay calibration**. They
are not an official order of battle, mineral map or claim about named 1991
aircraft. The existing Erusean character definitions and recruits are retained.

## Preserved baseline and additive facilities

The 20 inherited owned states retain every individual factory placement:
**28 civilian factories, 23 military factories and 11 dockyards**. Ownership,
cores, manpower, province lists, state 171/`XXX`, the province raster, adjacency,
airport coordinates and all other map coordinates are unchanged. No inherited
resource value falls. The originally zero resource rows receive only the
explicit additions below. All 16 inherited naval bases retain their provinces
and levels. Existing state and victory-point names are retained.

Capital state 349 retains province 644 at 100 VP and port 4600 at 30 VP. Supply
origin 644 is connected to the inherited airport coordinate 1118 and mainland
industrial, deployment and port terminals. The topology inspector finds
**30 separate owned-land components**: the 345-province mainland and 29 detached
components. Every detached component receives a minimum level 1 valid coastal
port if it has none. The choice is its existing operational airport when
coastal, otherwise its lowest valid coastal province ID. This is reproducible
gameplay placement with no sourced city claim.

The result has 45 ports, eight authored supply hubs and 31 railway paths. Every
railway remains inside one owned-land component. Detached components use sea
receiving ports; no railway joins islands across water. Four operational island
components in states 240, 262, 350 and 467 receive one infantry formation each,
level 1 airfields and minimum level 1 infrastructure. The other 25 detached
components receive no troops, airfields or industry. A port-fed component can
still be blockaded; valid geometry does not prove native sea-route throughput.

Mainland airfields in 349 and 298 receive level 2. One fuel silo is placed in 349.
Only overcapacity inherited categories are raised: 298 and 349 to `metropolis`,
333/432/457 to `city`. The ten-slot capital includes its retained nine factories
and the new silo. No factory is created or moved by this capacity repair.

Exact component membership, province choices, deployment locations and captured
factory/resource/VP/port baselines are in
[`foundation.json`](../tools/world_foundation/foundation.json). Derivation is in
[`erusea.py`](../tools/world_foundation/erusea.py); no geography is inferred from
official artwork or a fan map.

## Starting roster and replacement plan

| Item | New-campaign setup | Continuing production |
|---|---|---|
| Land |12 formations, each six infantry battalions, engineers and support artillery; eight mainland, four operational islands |6 MIL rifles, 2 support equipment, 3 artillery |
| Air |96 fighters split 48/48 between 349/298; 24 support aircraft in 349 |7 MIL fighters, 2 MIL support aircraft |
| Logistics |120 convoys, 60 trains, 1,200 trucks; transport stocks do not create motorized battalions |2 MIL trucks, 1 MIL trains; 3 dockyards convoys |
| Navy |8 numbered escorts and 3 numbered submarines, separate task forces, retained capital port 644 |6 dockyards escorts, 2 dockyards submarines |
| Replacement stocks |2,400 rifles, 360 support equipment, 288 artillery, 24 fighters, 12 support aircraft |All 23 MIL and 11 dockyards are assigned once |

The infantry requires 7,320 rifles, 360 support equipment and 144 artillery for
its initial fully equipped formations; separate replacement stock is additional.
It uses 79,200 initial land manpower without changing any state's manpower. The
primary unit-definition worksheet gives 0.54 supply per formation versus the
reference level 1 port coefficient 3; this is a static capacity comparison,
not a tested delivery rate.

BBA/legacy aircraft and MTG/legacy naval routes have the same roster counts,
transport stocks, replacement planes and factory budgets. The modern branch
creates the tagged variants after their technology/module unlocks and before
loading the corresponding OOB. Names such as `ERU Service Fighter` and numbered
coastal vessels identify technical gameplay designs, not canonical service
aircraft or ship names. The inherited engine's older technical hull/airframe
IDs remain an explicit technology-foundation limitation. No story plane is
invented to fill that gap.

The setup is country-history-only. It has no startup, event, decision or
save-load grant and no callback that loads an OOB again. Old saves retain their
armies and stockpiles. Existing Usean calendar, pressure, war/faction/project
owners are untouched; Erusea is not added to Central Usea's starting faction.
Country AI/research requires both current and original ERU tags, so a civil-war
clone cannot cancel its generic role priorities for an unavailable national
template. It favors affordable infantry, replacement aviation and escorts,
civilian construction, infrastructure and relevant research; it creates no war
goal. Native AI choices and growth still require acceptance testing.

## Explicit resource and fuel calibration

| State | Base additions | Retained inherited infrastructure |
|---|---|---:|
|349|32 steel, 20 aluminium, 14 rubber, 16 oil|5|
|333|32 steel, 4 tungsten|4|
|298|20 aluminium|2|

These are fictional balance allocations, not claims of deposits or a real
national economy. Erusea keeps the default civilian economy and export-focused
trade law. No fabricated import agreement, free resource transfer or hidden
production modifier is added. The worksheet reads the installed primary
definitions, the mod's technology/law definitions and its overriding factory
speed defines. At undamaged inherited infrastructure, default 50% exports,
and conservative per-state integer floors, the additions retain 53 steel,
30 aluminium, 12 rubber, 3 tungsten and 14 oil. The worst of the four DLC
combinations needs 50 steel, 29 aluminium, 11 rubber and 3 tungsten. This leaves
small input margins and preserves trade pressure after damage, territorial loss,
export changes or force expansion. The positive supply-route extraction bonus
and resource technologies are excluded from that margin.

At 50% military efficiency, no positive output bonuses and 30 days, the reference
arithmetic yields 1,080 rifles, 45 support equipment, 77.14 artillery, 72 trucks,
1.29 trains, 26.25–29.72 fighters and 8.18–9 support aircraft. Dockyard arithmetic
yields 3.21 convoys, 0.43–0.90 escorts and 0.31–0.60 submarines. Fractional figures
are progress estimates, not guaranteed completed equipment. The same force
counts have different native design costs and therefore different replacement
speeds across DLC routes; parity here means comparable role/capability, not
identical combat statistics.

The fuel worksheet's deliberately conservative daily income is 540 after the
default civilian penalty and the two starting fuel technologies, excluding
positive state fuel bonuses. Reference full-roster air-superiority/CAS plus
whole-navy patrol arithmetic ranges 353.28–440.16 per day. The silo and civilian
capacity penalty give a 112,500 starting full-stock worksheet, about 255.59 days
at the worst patrol arithmetic with **zero income**. Whole-navy combat instead
of patrol raises the sensitivity to 494.88–658.56 daily, so prolonged combat can
require oil imports or reduced tempo. Terrain, damaged facilities, blockades,
actual mission cycles, MIOs and later modifiers are not simulated. These
figures establish a bounded source calibration; they do not certify native
fuel distribution, losses or campaign balance.

Reproduce the primary-definition worksheet with:

```powershell
python -B tools/world_foundation/budget.py --reference '<read-only HOI4 root>' --check
```

[`erusea_budget.json`](../tools/world_foundation/erusea_budget.json) records all
used primary-file hashes, effective coefficients, equations' inputs, costs,
resource margins and four DLC results. No installed asset or script is copied
into the mod.

## Provenance and verification boundaries

| Content/IDs | Layer and exact evidence | Status |
|---|---|---|
|ERU history, 20 state identities, all individual 28/23/11 factories, 16 ports, 644/4600 VP hierarchy, existing recruits|Mod provenance: captured ERU baseline in `foundation.json`, source base `fb3e8c3`, inherited country/state histories|Preserved, source-checked |
|New `ERU_wf_*` OOBs, `ERU_WF_INF`, `ERU_wf_*` AI, receiving ports, rail/hub/airfield additions, resource additions and numbered names|Provisional gameplay: approved ERU foundation task; `profiles.json`, `erusea.py`, `build.py`|Implemented; source checks, native pending |
|Unlocks, equipment/modules, replacement costs, supply/fuel coefficients|Read-only engine technical evidence: exact paths and SHA256 values in `erusea_budget.json`; not Strangereal canon|Static primary-definition comparison |
|Named operational 1991 aircraft, official ship names, mineral geography or new chronology|No new official claim authored|Out of scope; existing research gaps retained |

The compatibility snapshot in `original_four.json` keeps the four delivered
partner country rows and individual generated files exact. Shared logistics and
localization aggregates extend additively. Economic new-campaign eligibility
markers survive country-history regeneration; unexpected commands inside that
foreign marker are rejected. Anea/world logistics regeneration works in either
order and rejects stale or mutated foreign records. The 69-country registry is
refreshed honestly; its other foundation gaps are not declared fixed by this
Erusean slice.

See the [retained source acceptance record](evidence/erusea-foundation/ACCEPTANCE.md)
for exact checks and limitations. **Native testing remains paused.** Engine
parsing, four DLC new starts, old-save isolation, sea supply, fuel throughput,
AI deployment/production, transitions, save/reload and natural pacing remain
unobserved. Normal installation, profiles and saves were not altered. No push,
PR, remote merge, release or installation synchronization is part of this
component handoff.
