# Inherited legacy unit definitions

The files under `common/units/` and `common/unit_tags/00_categories.txt` were
inherited from the April 5, 2024 Project Ulysses archive. They are preserved
here as inactive provenance while
the active 1.19 continuation uses the installed game's current unit schema.

Native HOI4 startup on Operation Postern v1.19.3 rejected the active copies
with obsolete equipment tokens and sub-unit categories. They must not be
reintroduced into the active mod payload without a dedicated 1.19 migration
and native validation pass. The six `*.equipment_variants.txt` files preserve
the 91 country-history aircraft-variant blocks removed from active setup after
native startup reported invalid 1.14-era modules and name groups.

`common/units/names_divisions/OSE_names_divisions.txt` was returned to the
active payload: active Osea OOBs use its `OSE_Inf_01`, `OSE_Arm_01`, and
`OSE_MOT_01` groups, vanilla 1.19 has no Osea definitions, and every
`division_types` entry in it is a native 1.19 sub-unit. GER groups resolve from
the installed game's own `GER_names_divisions.txt`.

The BLK and OSE unit/ship name lists are active again under
`common/units/names/`, because BLK and OSE are mod-only tags with no vanilla
naming pools. `00_OSE_names.txt` uses only 1.19 keys and was moved back as-is.
The archive `00_BLK_names.txt` stays here unchanged; its active copy renames
nine pre-By Blood Alone aircraft archetype blocks (`fighter_equipment`,
`CAS_equipment`, `nav_bomber_equipment`, the three `cv_*` variants,
`heavy_fighter_equipment`, `tac_bomber_equipment`, `strat_bomber_equipment`)
to the 1.19 airframe keys Osea's file already uses. The `FLEET_NAME_*` and
`AIR_WING_NAME_BLK_*` templates both files reference still have no localization.

The following additional exact files are preserved here after the compatibility
pass:

- `common/ai_templates/generic.txt` and `common/ai_equipment/generic_tank.txt`:
  obsolete AI schema overrides.
- `common/technologies/armor.txt`, `artillery.txt`, and `infantry.txt`:
  1.14-era technology overrides whose custom subunits/equipment are absent from
  the active 1.19 schema.
- `common/on_actions/05_lar_on_actions.txt`: an old pony/DLC override with
  unavailable culture and operative schema.
- `events/crowbuildingdebugevents.txt`: developer-only test events referencing
  unavailable province/building data.
