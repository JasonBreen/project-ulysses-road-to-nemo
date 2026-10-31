"""Reproduce ERU's static input/replacement/fuel worksheet from primary files.

This deliberately excludes native trade decisions, losses, damage, mission
tempo, MIOs and later policy changes. It is a calibration worksheet, not a
simulation or an assertion of observed native throughput.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / "mod/2985041246"
sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
from script import get, parse


def worksheet(reference):
    used = {}
    version = json.loads((reference / "launcher-settings.json").read_text(encoding="utf-8-sig"))["rawVersion"]

    def load(path):
        layer = "mod" if path.is_relative_to(MOD) else "reference"
        base = MOD if layer == "mod" else reference
        used[layer + "/" + path.relative_to(base).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        return parse(path.read_text(encoding="utf-8-sig"))

    def catalog(relative, section):
        paths = {p.name: p for p in (reference / relative).glob("*.txt")}
        paths.update({p.name: p for p in (MOD / relative).glob("*.txt")})
        result = {}; owners = {}
        for path in sorted(paths.values(), key=lambda p: p.name):
            # Parse broadly, but record only files actually used below.
            tree = parse(path.read_text(encoding="utf-8-sig"))
            entries = get(tree, section, [])
            if section == "equipments":
                entries = entries + get(tree, "duplicate_archetypes", [])
            for key, _, body in entries:
                result[key] = body; owners[key] = path
        return result, owners

    equipment, equipment_files = catalog("common/units/equipment", "equipments")
    modules, module_files = catalog("common/units/equipment/modules", "equipment_modules")
    units, unit_files = catalog("common/units", "sub_units")

    def resolve(ident, definitions, files, chain=()):
        if ident in chain:
            raise ValueError("Cyclic technical definition: " + ident)
        body = definitions[ident]; load(files[ident])
        parent = get(body, "parent", get(body, "archetype"))
        result = resolve(parent, definitions, files, chain + (ident,)) if parent else {}
        result.update({key: value for key, _, value in body})
        return result

    def stats(ident, fitted=()):
        body = resolve(ident, equipment, equipment_files)
        values = {key: float(body.get(key, 0)) for key in ("build_cost_ic", "fuel_consumption")}
        resources = {key: float(value) for key, _, value in body.get("resources", [])}
        multipliers = Counter()
        for module in fitted:
            m = resolve(module, modules, module_files)
            for key, _, value in m.get("add_stats", []):
                if key in values:
                    values[key] += float(value)
            for key, _, value in m.get("multiply_stats", []):
                if key in values:
                    multipliers[key] += float(value)
            for key, _, value in m.get("add_resources", []):
                resources[key] = resources.get(key, 0) + float(value)
        for key in values:
            values[key] *= 1 + multipliers[key]
        return {**values, "resources_per_factory": resources, "equipment": ident, "modules": list(fitted)}

    raw = (reference / "common/defines/00_defines.lua").read_text(encoding="utf-8-sig")
    path = reference / "common/defines/00_defines.lua"
    used["reference/common/defines/00_defines.lua"] = hashlib.sha256(path.read_bytes()).hexdigest()
    defines = {}
    for section, keys in {
        "NCountry": ["BASE_FUEL_GAIN_PER_OIL", "BASE_FUEL_GAIN", "BASE_FUEL_CAPACITY"],
        "NProduction": ["BASE_FACTORY_SPEED_MIL", "BASE_FACTORY_SPEED_NAV"],
        "NBuildings": ["INFRASTRUCTURE_RESOURCE_BONUS", "SUPPLY_PORT_LEVEL_THROUGHPUT"],
        "NAir": ["FUEL_COST_MULT"], "NNavy": ["FUEL_COST_MULT", "IN_COMBAT_FUEL_COST"],
    }.items():
        region = raw.split(section + " = {", 1)[1].split("\n}", 1)[0]
        for key in keys:
            value = float(re.search(r"^\s*" + key + r"\s*=\s*([\d.]+)", region, re.M).group(1))
            defines[section + "." + key] = value
    for path in sorted((MOD / "common/defines").glob("*.lua")):
        text = path.read_text(encoding="utf-8-sig")
        used["mod/" + path.relative_to(MOD).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        for key in defines:
            matches = re.findall(r"NDefines\." + re.escape(key) + r"\s*=\s*([\d.]+)", text)
            if matches:
                defines[key] = float(matches[-1])
    laws = get(load(MOD / "common/ideas/_economic.txt"), "ideas")
    export = float(get(get(get(get(laws, "trade_laws"), "export_focus"), "modifier"), "min_export"))
    civilian = get(get(get(laws, "economy"), "civilian_economy"), "modifier")
    fuel_gain_modifier = float(get(civilian, "fuel_gain_factor", "0"))
    techs = get(load(MOD / "common/technologies/industry.txt"), "technologies")
    fuel_gain_modifier += sum(float(get(get(techs, ident), "fuel_gain_factor", "0")) for ident in ("fuel_silos", "fuel_refining"))
    buildings = get(load(reference / "common/buildings/00_buildings.txt"), "buildings")
    silo_capacity = float(get(get(get(get(buildings, "fuel_silo"), "country_modifiers"), "modifiers"), "max_fuel_building")) * 1000
    profile = json.loads((HERE / "profiles.json").read_text())["countries"]["ERU"]
    row = json.loads((HERE / "foundation.json").read_text())["countries"]["ERU"]
    domestic = Counter(); gross = Counter()
    for cfg in row["placements"].values():
        for key, value in cfg["resources"].items():
            gross[key] += float(value)
            # Floor both stages as a deliberately conservative worksheet bound;
            # no claim about the engine's hidden rounding implementation.
            domestic[key] += math.floor(math.floor(float(value) * (1 + cfg["infrastructure"] * defines["NBuildings.INFRASTRUCTURE_RESOURCE_BONUS"])) * (1 - export))
    common = {kind: stats(kind) for kind in profile["production"] if kind not in ("fighter", "cas")}
    branches = []
    for bba, mtg in [(False, False), (True, False), (False, True), (True, True)]:
        fighter = stats("small_plane_airframe_1", ["light_mg_4x", "engine_2_1x"]) if bba else stats("fighter_equipment_1")
        support = stats("small_plane_airframe_1", ["bomb_locks", "engine_2_1x"]) if bba else stats("CAS_equipment_1")
        escort = stats("ship_hull_light_2", ["ship_light_battery_1", "ship_anti_air_1", "ship_fire_control_system_0", "light_ship_engine_2", "ship_torpedo_1", "ship_depth_charge_1"]) if mtg else stats("destroyer_2")
        submarine = stats("ship_hull_submarine_2", ["ship_torpedo_sub_1", "sub_ship_engine_2"]) if mtg else stats("submarine_2")
        lines = {**common, "fighter": fighter, "cas": support}
        naval = {"convoy": stats("convoy_1"), "destroyer": escort, "submarine": submarine}
        inputs = Counter(); replacements = {}
        for items, assignments, speed, efficiency in [(lines, profile["production"], defines["NProduction.BASE_FACTORY_SPEED_MIL"], 0.5),
                                                       (naval, profile["naval_production"], defines["NProduction.BASE_FACTORY_SPEED_NAV"], 1)]:
            for kind, s in items.items():
                count = assignments[kind]
                inputs.update({key: value * count for key, value in s["resources_per_factory"].items()})
                replacements[kind] = round(30 * speed * efficiency * count / s["build_cost_ic"], 4)
        air_burn = 24 * defines["NAir.FUEL_COST_MULT"] * (profile["fighters"] * fighter["fuel_consumption"] + profile["cas"] * support["fuel_consumption"])
        naval_burn = 24 * defines["NNavy.FUEL_COST_MULT"] * (profile["destroyers"] * escort["fuel_consumption"] + profile["submarines"] * submarine["fuel_consumption"])
        branches.append({"bba": bba, "mtg": mtg, "technical_stats": {**lines, **naval},
            "resource_inputs": dict(sorted(inputs.items())), "domestic_margin": {k: domestic[k] - v for k, v in sorted(inputs.items())},
            "30_day_replacements_no_output_bonus_at_50_percent_mil_efficiency": replacements,
            "daily_air_superiority_and_CAS_reference_fuel": round(air_burn, 4),
            "daily_whole_navy_patrol_reference_fuel": round(naval_burn, 4),
            "daily_combined_reference_fuel": round(air_burn + naval_burn, 4),
            "daily_with_whole_navy_in_combat_reference_fuel": round(air_burn + naval_burn * defines["NNavy.IN_COMBAT_FUEL_COST"], 4)})
    fuel_gain = 24 * (defines["NCountry.BASE_FUEL_GAIN"] + domestic["oil"] * defines["NCountry.BASE_FUEL_GAIN_PER_OIL"]) * (1 + fuel_gain_modifier)
    capacity = (defines["NCountry.BASE_FUEL_CAPACITY"] + sum(c["fuel_silo"] for c in row["placements"].values()) * silo_capacity) * (1 + float(get(civilian, "max_fuel_factor", "0")))
    per_division = Counter(); manpower = supply = 0
    for kind, count in [("infantry", 6), ("engineer", 1), ("artillery", 1)]:
        u = resolve(kind, units, unit_files)
        per_division.update({key: int(value) * count for key, _, value in u.get("need", [])})
        manpower += int(u["manpower"]) * count; supply += float(u.get("supply_consumption", 0)) * count
    return {"schema": 1, "evidence": "static primary-definition calibration worksheet; no native throughput or balance acceptance",
        "country": "ERU", "reference_version_target": "HOI4 1.19.4.1", "source_files_sha256": dict(sorted(used.items())),
        "reference_version_observed": {"source": "launcher-settings.json:rawVersion", "value": version},
        "profile_sha256": hashlib.sha256(json.dumps(profile, sort_keys=True).encode()).hexdigest(),
        "placements_sha256": hashlib.sha256(json.dumps(row["placements"], sort_keys=True).encode()).hexdigest(),
        "assumptions": ["Retain default civilian_economy and export_focus; no invented trade agreements or law change.",
            "Infrastructure is undamaged; separately floor extraction and retained share as conservative bound; ignore positive resource technologies and supply-route resource bonuses.",
            "Military replacement arithmetic uses50% efficiency and no factory/output bonus; dockyards use no efficiency multiplier.",
            "Initial infantry has no fuel-using battalion/support company; reserve trucks are not an operating motorized army.",
            "Air superiority/CAS and naval patrol multipliers are1 in installed definitions. Naval combat is a separate2x sensitivity.",
            "Fuel worksheet excludes positive fuel_gain_factor_from_states, terrain, doctrine, mission scheduling, MIO, losses and damage.",
            "Domestic surplus is not an infinite guarantee: loss of control, export-law changes, expanded forces or damaged infrastructure require trade, repairs or rationing."],
        "defines": defines, "gross_base_resources": dict(sorted(gross.items())), "default_export_fraction": export,
        "conservatively_retained_resources": dict(sorted(domestic.items())),
        "infantry_per_formation": {"equipment": dict(per_division), "manpower": manpower, "daily_supply": round(supply, 4)},
        "initial_land_equipment_need": {k: v * profile["divisions"] for k, v in per_division.items()},
        "daily_fuel_gain_lower_worksheet": round(fuel_gain, 4), "starting_full_fuel_capacity_worksheet": capacity,
        "worst_roster_patrol_zero_income_stock_days_worksheet": round(capacity / max(b["daily_combined_reference_fuel"] for b in branches), 2),
        "branches": branches}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "erusea_budget.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(); report = worksheet(args.reference); text = json.dumps(report, indent=2) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("ERU calibration worksheet differs from primary definitions")
    else:
        args.output.write_text(text, encoding="utf-8", newline="\n")
    print("ERU primary-definition worksheet: " + ("consistent" if args.check else "generated"))
