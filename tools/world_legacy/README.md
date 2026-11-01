# Legacy military setup repairs

This component repairs the **BLK, OSE, SAP and FAT January 1991 military setup**
without changing their leaders, politics, existing land formations, borders,
province IDs or industrial budgets. It is based on `60ec3a6` and retains the
25 original input files under `baseline/`. Those files are **mod provenance**,
not evidence of official ACE COMBAT force inventories or ship identities.

The active designer navy is the named-hull reference for each country. A new
`<TAG>_navy_1991_legacy` projection supplies valid legacy equipment and inherited
class names when Man the Guns is unavailable. It preserves the active navy's
ship order, names and class definitions. The original legacy naval files remain
available; FATO's malformed quote is repaired in its retained legacy file.

| Country/context | Divisions | Original legacy/BBA aircraft | Repaired aircraft, either route | Original legacy/active MTG ships | Repaired ships, either route | MIL requests/core capacity | Yard requests/core capacity |
|---|---:|---:|---:|---:|---:|---:|---:|
| BLK | 57 | 1100 / 1130 | 1130 | 36 / 38 | 38 | 45 / 45 | 12 / 12 |
| OSE | 73 | 882 / 932 | 932 | 235 unused / 229 active | 229 | 46 / 50 | 23 / 23 |
| SAP | 18 | 220 / 220 | 220 | 30 / 31 | 31 | 8 / 8 | 2 / 8 |
| FAT, BLK controlled by AI | 28 | 195 / 195 | 195 | malformed / 16 | 16 | 12 / 12 | 1 / 6 |
| FAT, BLK controlled by player | 36 | 195 / 195 | 195 | malformed / 16 | 16 | 12 / 12 | 1 / 6 |

All four industrial budgets are entirely in owned core states at this component's
base. The audit derives capacities from actual state histories and excludes
non-core capacity rather than assuming compliance or rounding rules.

## Concrete repairs and calibration

- Osea's no-MTG branch previously selected `OSE_navy_dlc` and therefore requested
  designer equipment in the legacy route. It now selects the new projection.
- The unused `OSE_navy` contains **235** ships: ten light cruisers and 79
  submarines. The active MTG fleet contains **229** ships: twelve light cruisers
  and 71 submarines. It also differs in individual names. The original 235-hull
  definition is retained byte-for-byte apart from platform line endings; it is
  not silently substituted for the active force. The manifest retains both
  complete name lists and role counts. No active named hull is removed.
- Belka's fallback receives the two light cruisers present in its active MTG
  roster. Sapin's fallback receives the active roster's additional destroyer.
  These are compatibility projections of inherited content, not new historical
  claims or new formation names.
- Every inherited legacy aircraft wing remains unchanged. Belka's missing 30
  and Osea's missing 50 specialist scout aircraft use the BBA route's inherited
  locations, numbers and variant names in the legacy equipment route.
- Required equipment and module technologies are granted in branch-specific
  preludes **before** variants and OOBs. This also fixes Osea's late air-tech
  grant. Cruiser armor module1 has no effective research unlock in the mod's
  replacement naval technology file; affected designs use module2, which the
  mod's earliest cruiser armor technology actually enables. That small design
  adjustment is explicit provisional compatibility calibration.
- Osea's `P-3 Orion` variant now uses the exact maritime-patrol role equipment
  type referenced by its wing and stockpile. The inherited name and aircraft
  count are retained.
- Belka's 13 concurrent yard requests become twelve by combining two identical
  four-destroyer queues into one eight-destroyer queue. All **28 queued hulls**,
  equipment classes and matching initial progress are preserved; concurrency
  changes. FATO's two land contexts both requested sixteen MIL. Each now assigns
  four factories to its two tank lines, freeing capacity for a fighter line and
  retaining all standing formations. Sapin reallocates one tank factory to
  fighter replacement. The larger starts use spare MIL for supply replacements.
  Belka and Osea also receive a tracked-artillery replacement line matching the
  role already fielded by their divisions. Belka reallocates one of its fifteen
  tank factories; Osea uses one unassigned factory. Each fielded armor role has
  a starting replacement queue and reserve in both legacy and NSB routes.
- Inherited production efficiency values, including25 and50, are preserved.
  New lines use efficiency50 and progress0, following the installed1936 infantry
  OOB examples. The installed standalone ship-effect documentation instead uses
  efficiency0.1; these contexts disagree and native numeric interpretation is
  unverified. Only inherited progress above1 is provisionally interpreted as a
  percentage (progress2 becomes0.02); existing in-range progress is retained.
  This is explicit compatibility calibration, not proof of engine units.
- With No Step Back enabled, five land projections (including both FATO
  contexts) preserve every template, division, name, location and experience
  value. Eligible divisions explicitly select the reviewed Service Armour and
  Tracked Service Artillery variants through `force_equipment_variants`.
  Required hidden research is granted before variants, OOBs, stockpiles and
  production. The no-NSB route retains the legacy equipment. Each deployed
  armor role receives100 replacement vehicles in either route, an explicit
  provisional reserve rather than a historical inventory claim.
- Each country receives a bounded common supply reserve (3000 infantry,300
  support,100 artillery,100 AA,400 trucks,50 trains) and approximately ten
  percent aircraft spares by actual equipment/variant. Existing OOB reserves,
  such as Belka's trucks, remain included separately in the machine manifest.
  Convoy and fuel-ratio history settings are retained. Resource, refinery,
  storage and logistics additions belong to the separate world-start owner.
- An owned setup flag guards every OOB load and new stock grant. The work adds
  no startup, event, decision or monthly callback that grants forces to an old
  save. Native history loading and save behavior still require verification.

## Effective-primary technical contract

`primary_contract.json` captures **technical facts and hashes**, not installed
art or complete source files. Mod files override installed files by filename.
`Primary` resolves parent definitions, whole-block inheritance and named module
slot aliases in declaration order. Required slots and module categories are
checked on the actual selected designer variants. Explicit allowed modules and
turret-supplied slot-category overrides are included. Child slot lists replace
the parent list while literal whole-block inheritance preserves it; named slot
aliases copy the earlier resolved slot. Legacy upgrade variants are not
incorrectly subjected to designer-slot requirements.

The read-only installed reference supplied for this task is
`G:/steamlbirary/steamapps/common/Hearts of Iron IV`. Important primary routes:

| Contract | Exact primary source/identifier | Use |
|---|---|---|
| Transport baseline | Installed `common/technologies/air_techs.txt`, `early_transport_plane` | Enables `transport_plane_equipment_1`; omitted by the effective mod replacement file |
| Transport compatibility owner | `common/technologies/ac_world_legacy_support.txt`, `ac_wl_transport_support` | Unresearchable, no-folder history-only bridge preserving Belka's ten transports |
| Legacy scouting | Effective mod `common/technologies/air_techs.txt`, `scout_plane1` | Has `allow_branch = { has_dlc = "La Resistance" }` |
| Designer camera | Effective equipment/module catalog, `recon_camera` and captured camera technology | Module/tech existence is distinct from DLC mission availability |
| Cruiser armor | Effective mod `common/technologies/MTG_naval.txt`, `basic_cruiser_armor_scheme` | Enables `ship_armor_cruiser_2`, not module1 |
| Queue syntax | Installed `documentation/effects_documentation.md`, `add_equipment_production` | Equipment, creator, variant, amount, progress and efficiency fields |
| History queue convention | Installed `history/units/USA_1936.txt` and `GER_1936.txt` | Infantry history examples use efficiency50; the standalone ship-effect example uses0.1; both contexts are hash-captured and native units remain unverified |
| NSB service-role owner | `tools/world_starts/armor.py` and `common/technologies/ac_ws_armour_support.txt`, reviewed dependency `c87312f5bb6cb2bfeebcaadedb5753c87463a221` | History-only chassis, module and subunit unlocks; no research-tree restoration |
| Deployed variant selection | Installed `history/units/AFG_1936_nsb.txt`, division `force_equipment_variants` | Owner, creator and version-name bindings select the authored designer equipment |
| Aircraft stock variant | Installed `common/scripted_effects/00_scripted_effects.txt`, historical stock grants | Uses `variant_name` for named equipment reserves |
| Legacy scout upgrade | Installed `common/units/equipment/upgrades/air_upgrades.txt`, `plane_range_upgrade` | Valid inherited legacy upgrade field |

The hidden transport bridge has its English name/description in
`ac_world_legacy_l_english.yml`. It adds no visible research panel, aircraft,
leader, national history or canonical claim.

## DLC and acceptance limits

The actual-source audit evaluates **40 core profiles**: eight BBA/MTG/NSB
combinations for each country, with both FATO opponent contexts. It records another **40
La Résistance-disabled profiles** as an explicit release gap. Specialist
airframes remain present, but force-granted technology and equipment existence
do **not** establish reconnaissance-mission availability without that DLC. This
component does not claim universal DLC acceptance.

The No Step Back-specific armor bridge is the reviewed world-start dependency
merged into this candidate. The actual-source audit checks its chassis/module
unlocks, required slots, turret category overrides, exact deployed variants,
replacement queues and stock bindings. Native designer initialization and
replacement operation remain untested. Numeric combat statistics, range and resource
costs differ between designer and legacy equipment abstractions. Named hull and
class preservation, specialist counts and valid source bindings establish
bounded capability coverage, not numerical combat equivalence.

All results here are **static/offline**. Native HOI4 loading, DLC mission
operation, carrier assignment, physical production, supply, fuel throughput,
natural AI priorities, pacing and native save/reload remain untested. No game,
desktop, normal installation, user profile or save was touched.

## Reproduction

From the repository root:

```powershell
python -B tools/world_legacy/build.py
python -B tools/world_legacy/audit.py
python -B tools/world_legacy/test_legacy.py
python -B tools/world_legacy/build.py --check
python -B tools/world_legacy/audit.py --check
```

Refreshing primary facts is a deliberate source update requiring the read-only
reference. It must be reviewed together with its generated output:

```powershell
python -B tools/world_legacy/build.py --reference 'G:/steamlbirary/steamapps/common/Hearts of Iron IV'
python -B tools/world_legacy/audit.py
```

Ordinary checks consume the committed technical facts and do not require an
installed game. `manifest.json` retains actual per-profile templates, deployed
formations, wings, named ships, equipment, variants/modules, selected research,
stocks, production requests, capacities, inputs and failures. Its source hashes
normalize CRLF to LF. `compiled_cases.json` records the compiler's branch plans.
Unit and ship declarations outside edited top-level production/wing blocks
retain their original formatting and comments. The regressions compare actual
land formations and politics structurally, preserve original wings, preserve
active named hulls and queued Belkan hulls, test loaded setup guards, check
primary ordering/slots and require generated-output consistency.
