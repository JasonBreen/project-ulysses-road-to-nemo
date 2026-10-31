# World foundation registry and selected Usean starts

This Package 1 source slice is based on main
`3810d1a`, preserving the approval baseline `1f04456`. It implements a reproducible
69-country source registry and the initial military/industrial/logistics
foundations for **SNS, AMB, UGE and DEL**, plus all fourteen reviewed foreign-capital
repairs described in [the capital ledger](WORLD_CAPITAL_REPAIRS.md). It adds no focuses, war outcomes,
country tags, borders, cores, leader identities or event grants.
Native testing is paused; source checks do not establish playable balance,
AI behavior or final game acceptance.

This review slice is stacked on prerequisite [PR32](https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/32),
the repair/privacy package. Its source is merged into the World branch without
merging main. The [combined acceptance record](evidence/world-foundation/repair-stack/README.md)
records the refreshed overview/registry, independent CI steps and shared regional
label ownership. World foundation labels take precedence by agreement between
the two authored files, rather than by relying on localization load order.

The subsequent [Erusean foundation](ERUSEA_FOUNDATION.md) preserves the four
starts below and extends the same owner with an additive ERU roster and
component-based logistics. It retains ERU's individual 28 CIV/23 MIL/11 dockyard
placements and all 16 inherited ports. Its new forces, bounded resource
additions and minimum island receiving facilities are documented gameplay
calibration. The four-country budgets and placements below remain unchanged.

## What the registry establishes

[country_registry.json](../tools/world_foundation/country_registry.json) is
generated from actual country/state histories, leader definitions, direct OOB
references, production assignments, focus definitions and logistics records.
Every country has a support status and explicit failed source checks. Existing
event-driven forces and native parser/supply/AI behavior are outside that
registry's direct-history boundary.

After this slice, 69 histories include 62 currently landowning countries.
**26 landowners still have no industry and 28 no infrastructure; 51 histories
have no direct OOB reference after the ERU addition. All 62 landowning countries
now have owned capitals.** These are
documented inherited gaps, not claims that every affected country is absent or
unplayable. Dormant/emergent countries are separate from active ones, and PLH /
state 171 remains explicitly unresolved. The inspector records an inherited
offline parsing error in `FAT_navy.txt`; that is not a new native test result.

## New-campaign budget and provenance

| Country | CIV | MIL | Docks | Territorial divisions | Fighters / CAS | Escorts / submarines | Reserve trains / trucks / convoys |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| San Salvacion | 8 | 5 | 2 | 6 | 48 / 12 | 3 / 1 | 24 / 400 / 40 |
| Amber | 7 | 4 | 2 | 5 | 36 / 12 | 2 / 1 | 20 / 300 / 40 |
| Ugellas | 5 | 3 | 1 | 3 | 24 / 0 | 2 / 0 | 12 / 200 / 30 |
| Delarus | 5 | 3 | 1 | 3 | 24 / 0 | 2 / 0 | 12 / 200 / 30 |

These figures, the reserve equipment, resource calibration and force composition
are **provisional gameplay**, not official economic, mineral or military facts.
[profiles.json](../tools/world_foundation/profiles.json) is their authoring source.
The modest territorial formations use six infantry battalions and engineers;
SNS/AMB also have support artillery and its production/reserve supply. Every
military factory is assigned to actual infantry, support, artillery or fighter
production; every dockyard starts convoy production. Replacement aircraft,
equipment, trucks, trains and full initial fuel are present in country history.
Normal trade and physical sustainment remain necessary.

All four retain their owned starting capitals, parties, popularities, national
ideas, existing faction membership and leaders. Remove only the copied 1930
election date rather than inventing an office term. SNS/AMB/UGE keep their
approved office leaders; DEL retains its inherited named leader. No startup,
weekly or event effect reseeds forces, factories or stocks into existing saves.

Each country gets one land roster, mutually exclusive BBA/legacy air rosters and
MTG/legacy naval rosters. Variants and their modules are unlocked and created
before the selected roster loads exactly once. The branches have equal plane,
ship and division counts, with their creator/owner consistent. Coastal vessel
names are numbered service descriptions, not invented canon ship identities.

Country-scoped research, civilian construction, replacement production and
affordable territorial deployment policies are authored. A separate territorial
AI role avoids making its target compete with a second generic infantry target;
the matching generic role weights are canceled for these countries. The initial
templates do not require tanks, mechanized fleets or unaffordable large armies.
Actual AI growth and supply use remain native acceptance items.

National role overrides require both the current tag and original tag. A dynamic
civil-war clone therefore retains its own generic AI behavior rather than having
it canceled in favor of a template available only to the original country.

## Placements and composability

[foundation.json](../tools/world_foundation/foundation.json) records every
placement, route and protected original state identity. Ports are true owned
coastal provinces adjacent to sea. The existing capital airport provides an
unambiguous capital VP/supply origin, and railways follow actual owned land
pixel-edge adjacency with impassable links excluded. Hubs, airfields, ports and
starting deployments have capital-connected routes. Province rasters,
definitions, ownership, cores, inherited manpower, state 171 and strategic-region
geography remain unchanged.

Preserve the inherited mod's mapped San Salvacion, Meriton, East Meriton, Gnome
Ravine, Hatties Ravine and Ugellas labels as **mod provenance**. Replace the
selected countries' Earth/placeholder labels with neutral numbered districts as
**provisional gameplay**. These are not new official provincial mappings. No
unresolved strategic-region XXX is renamed.

Shared railway/node files now have explicit manifest owners in
`tools/logistics_owners.json`. Their immutable original prefix remains checked;
present foreign rows must match declared manifest records and country ownership.
An owner can regenerate its records without truncating another foundation.
Unknown, stale, duplicate or mutated foreign rows are rejected. This is not an
opaque hash exemption for arbitrary appended content. Anea and world foundation
generation work in either order.

Starting-government regeneration now replaces only its own marked section,
preserving later country foundation blocks. The world generator also preserves
the economic owner's declared new-campaign eligibility marker, if installed,
while rejecting additional effects disguised inside that marker. This slice
does not itself implement or enable the separate macroeconomic package.

## Reproduction and verification

From the repository root, using the existing Pillow/numpy validation dependencies:

```powershell
python -B tools/world_foundation/placements.py --check
python -B tools/world_foundation/build.py --check
python -B tools/world_foundation/registry.py --check
python -B tools/world_foundation/test_foundation.py
python -B tools/anea/test_foundation.py
python -B tools/usea_expansion/build_leaders.py --check
```

To author reviewed changes, regenerate placements with `placements.py`, outputs
with `build.py`, and the report with
`registry.py --output tools/world_foundation/country_registry.json`, then rerun
the checks. Review registry differences before accepting a new snapshot. These
commands do not touch a normal installation or user saves.

Pass `--reference $env:ULYSSES_GAME_ROOT` to the foundation test suites for
read-only effective technology/equipment/module validation against the installed
game. Without that reference their engine-definition test is explicitly skipped;
geometry, protection, roster parity and generation tests still run. CI runs the
world suite before the existing Anea gates. Full static checks, existing Usean
campaign/actor tests and strict authored assets remain required; shortcut and
natural native acceptance must be reported separately when testing resumes.
