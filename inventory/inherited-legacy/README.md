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
