"""Generate new-campaign foundations only; --check never writes.

No startup/on-action grants, focus additions, border edits or forced wars.
"""
import argparse
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "mod/2985041246"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
sys.path.insert(0, str(ROOT / "tools"))
from script import parse, get, setv, render
from shared_logistics import compose

NOTE = "# World foundation: provisional gameplay; tools/world_foundation/foundation.json and profiles.json.\n"
MARKER = "# BEGIN WORLD FOUNDATION"


def block(key, body):
    return key + " = {\n" + "\n".join("\t" + line for line in body.splitlines()) + "\n}\n"


def variant(name, equipment, modules):
    return block("create_equipment_variant", f'name = "{name}"\ntype = {equipment}\n' +
                 block("modules", "\n".join(f"{k} = {v}" for k, v in modules.items())))


def production(equipment, amount, tag, version=None):
    details = f"type = {equipment}\ncreator = {tag}"
    if version:
        details += f'\nversion_name = "{version}"'
    return block("add_equipment_production", block("equipment", details) +
                 f"requested_factories = {amount}\nprogress = 0.25\nefficiency = 50")


def state_output(row, ident, cfg):
    path = MOD / row["baseline"][ident]["path"]
    tree = parse(path.read_text(encoding="utf-8-sig")); state = get(tree, "state")
    hist = get(state, "history"); base = row["baseline"][ident]
    actual = {"owner": get(hist, "owner"), "cores": [v for k, _, v in hist if k == "add_core_of"],
              "manpower": int(get(state, "manpower")), "provinces": [int(k) for k, _, _ in get(state, "provinces")]}
    if any(actual[k] != base[k] for k in actual):
        raise ValueError("Protected state identity changed: " + ident)
    buildings = get(hist, "buildings")
    for key, value in [("infrastructure", cfg["infrastructure"]), ("industrial_complex", cfg["civilian"]),
                       ("arms_factory", cfg["military"]), ("dockyard", cfg["dockyard"]),
                       ("air_base", cfg["air_base"]), ("fuel_silo", cfg["fuel_silo"])]:
        setv(buildings, key, str(value))
    for p, level in cfg["naval_bases"].items():
        province = get(buildings, p, []); setv(province, "naval_base", str(level)); setv(buildings, p, province)
    owned = set(base["provinces"])
    for p in row["supply_hubs"]:
        if p not in owned:
            continue
        province = get(buildings, str(p), []); setv(province, "supply_node", "1"); setv(buildings, str(p), province)
        if row.get("preserve_inherited_economy"):
            # The inherited capital100 and port30 remain the supply/VP
            # hierarchy. Only previously unnamed new hubs receive a small VP.
            if p in row["new_victory_points"]:
                hist[:] = [n for n in hist if n[0] != "victory_points" or int(n[2][0][0]) != p]
                hist.append(["victory_points", "=", [[str(p), None, None], ["5", None, None]]])
        else:
            hist[:] = [n for n in hist if n[0] != "victory_points" or int(n[2][0][0]) != p]
            hist.append(["victory_points", "=", [[str(p), None, None], ["20" if p == row["capital_province"] else "5", None, None]]])
    resources = get(state, "resources", [])
    for key, value in cfg["resources"].items():
        setv(resources, key, str(value))
    slots = cfg["civilian"] + cfg["military"] + cfg["dockyard"] + (cfg["fuel_silo"] if row.get("preserve_inherited_economy") else 0)
    if row.get("preserve_inherited_economy"):
        capacities = {"town": 4, "city": 6, "large_city": 8, "metropolis": 10}
        original = row["baseline"][ident]["economy"]["state_category"]
        category = original
        if slots > capacities[original]:
            category = next(k for k, v in capacities.items() if v >= slots)
        setv(state, "state_category", category)
    elif slots > 6:
        setv(state, "state_category", "large_city")
    elif slots > 4:
        setv(state, "state_category", "city")
    return NOTE + render(tree) + "\n"


def country_output(tag, row, profile):
    # Preserve all inherited parties, popularity, ideas and recruited leaders.
    # Remove the copied 1930 election date rather than invent a 1991 office term.
    source = re.sub(r'^\s*last_election\s*=\s*"1930\.11\.9"\s*\n', "", row["country_history_source"], flags=re.M)
    # The economic owner may add its new-campaign eligibility marker in a
    # separate package. Preserve that declared block, but reject extra effects
    # disguised as its marker instead of silently authorizing foreign setup.
    current = (MOD / row["country_history"]).read_text(encoding="utf-8-sig")
    begin, end = "# BEGIN ECONOMY V2 NEW CAMPAIGN", "# END ECONOMY V2 NEW CAMPAIGN"
    if begin in current:
        if current.count(begin) != 1 or current.count(end) != 1:
            raise ValueError("Invalid economic eligibility section: " + tag)
        foreign = current[current.index(begin):current.index(end) + len(end)]
        if parse(foreign) != [["set_country_flag", "=", "ac_macro_history_eligible"]]:
            raise ValueError("Unexpected economic eligibility commands: " + tag)
        if begin not in source:
            leader_marker = "# BEGIN EXPANSION START LEADER"
            if leader_marker in source:
                source = source.replace(leader_marker, foreign + "\n\n" + leader_marker, 1)
            else:
                source = source.rstrip() + "\n\n" + foreign + "\n"
    text = source.rstrip() + "\n\n" + MARKER + "\n" + NOTE
    text += f'set_convoys = {profile["convoys"]}\nstarting_train_buffer = 1\nset_fuel_ratio = 1.0\n'
    common = ["infantry_weapons", "infantry_weapons1", "tech_support", "tech_engineers", "tech_recon",
              "gw_artillery", "basic_train", "motorised_infantry", "basic_machine_tools", "construction1",
              "electronic_mechanical_engineering", "fuel_silos", "fuel_refining"]
    text += block("set_technology", "\n".join(key + " = 1" for key in common))
    text += "set_grand_doctrine = new_superior_firepower\nset_grand_doctrine = new_fleet_in_being\nset_grand_doctrine = new_operational_integrity\n"
    bba = block("set_technology", "aa_lmg = 1\nearly_bombs = 1\naircraft_construction = 1\nengines_1 = 1\nengines_2 = 1\niw_small_airframe = 1\nbasic_small_airframe = 1")
    bba += variant(tag + " Service Fighter", "small_plane_airframe_1", {"fixed_main_weapon_slot": "light_mg_4x", "engine_type_slot": "engine_2_1x"})
    if profile["cas"]:
        bba += variant(tag + " Service Support", "small_plane_cas_airframe_1", {"fixed_main_weapon_slot": "bomb_locks", "engine_type_slot": "engine_2_1x"})
    reserve_fighters = profile.get("reserve_fighters", 12 if profile["fighters"] > 24 else 8)
    reserve_cas = profile.get("reserve_cas", 6 if profile["cas"] else 0)
    for kind, version, count in [("small_plane_airframe_1", "Service Fighter", reserve_fighters),
                                 ("small_plane_cas_airframe_1", "Service Support", reserve_cas)]:
        if count:
            bba += block("add_equipment_to_stockpile", f'type = {kind}\namount = {count}\nproducer = {tag}\nvariant_name = "{tag} {version}"')
    bba += f'set_air_oob = "{tag}_wf_air_bba"\n'
    legacy = block("set_technology", "early_fighter = 1\nfighter1 = 1\nCAS1 = 1")
    legacy += block("add_equipment_to_stockpile", f'type = fighter_equipment_1\namount = {reserve_fighters}\nproducer = {tag}')
    if profile["cas"]:
        legacy += block("add_equipment_to_stockpile", f"type = CAS_equipment_1\namount = {reserve_cas}\nproducer = {tag}")
    legacy += f'set_air_oob = "{tag}_wf_air"\n'
    text += block("if", 'limit = { has_dlc = "By Blood Alone" }\n' + bba + block("else", legacy))
    mtg = block("set_technology", "early_ship_hull_light = 1\nbasic_ship_hull_light = 1\nearly_ship_hull_submarine = 1\nbasic_ship_hull_submarine = 1\nbasic_battery = 1\nbasic_torpedo = 1\nbasic_depth_charges = 1\nmtg_transport = 1")
    mtg += variant(tag + " Coastal Escort", "ship_hull_light_2", {"fixed_ship_battery_slot": "ship_light_battery_1", "fixed_ship_anti_air_slot": "ship_anti_air_1", "fixed_ship_fire_control_system_slot": "ship_fire_control_system_0", "fixed_ship_engine_slot": "light_ship_engine_2", "fixed_ship_torpedo_slot": "ship_torpedo_1", "rear_1_custom_slot": "ship_depth_charge_1"})
    if profile["submarines"]:
        mtg += variant(tag + " Coastal Submarine", "ship_hull_submarine_2", {"fixed_ship_torpedo_slot": "ship_torpedo_sub_1", "fixed_ship_engine_slot": "sub_ship_engine_2"})
    mtg += f'set_naval_oob = "{tag}_wf_navy_mtg"\n'
    legacy_navy = block("set_technology", "early_destroyer = 1\nbasic_destroyer = 1\nearly_submarine = 1\nbasic_submarine = 1\ntransport = 1")
    legacy_navy += f'set_naval_oob = "{tag}_wf_navy"\n'
    text += block("if", 'limit = { has_dlc = "Man the Guns" }\n' + mtg + block("else", legacy_navy))
    text += f'set_oob = "{tag}_wf_land"\n'
    for equipment, amount in [("infantry_equipment_1", profile["reserve_infantry"]), ("support_equipment_1", profile["reserve_support"]),
                              ("artillery_equipment_1", profile["reserve_artillery"]), ("motorized_equipment_1", profile["trucks"]),
                              ("train_equipment_1", profile["trains"])]:
        if amount:
            text += block("add_equipment_to_stockpile", f"type = {equipment}\namount = {amount}\nproducer = {tag}")
    return text + "# END WORLD FOUNDATION\n"


def land_output(tag, row, profile):
    support = "engineer = { x = 0 y = 0 }"
    if profile["reserve_artillery"]:
        support += "\nartillery = { x = 0 y = 1 }"
    regiments = "\n".join(f"infantry = {{ x = {x} y = {y} }}" for x in range(2) for y in range(3))
    template = block("division_template", f'name = "{tag} Territorial Infantry"\ndivision_names_group = {tag}_WF_INF\n' + block("regiments", regiments) + block("support", support))
    divisions = ""
    for n in range(profile["divisions"]):
        location = row["land_deployments"][n] if "land_deployments" in row else row["supply_hubs"][n % len(row["supply_hubs"])]
        divisions += block("division", f'name = "{tag} Territorial Division {n + 1}"\nlocation = {location}\ndivision_template = "{tag} Territorial Infantry"\nstart_experience_factor = 0.2\nstart_equipment_factor = 1.0')
    lines = "".join(production(e, amount, tag) for e, amount in profile["production"].items() if e not in ("fighter", "cas"))
    return NOTE + template + block("units", divisions) + block("instant_effect", lines)


def air_output(tag, row, profile, dlc):
    if "air_deployments" in row:
        wings = ""
        for deployment in row["air_deployments"]:
            planes = ""
            for role, modern, legacy, version in [("fighters", "small_plane_airframe_1", "fighter_equipment_1", "Service Fighter"),
                                                   ("cas", "small_plane_cas_airframe_1", "CAS_equipment_1", "Service Support")]:
                amount = deployment[role]
                if amount:
                    details = f"owner = {tag}\ncreator = {tag}\namount = {amount}"
                    if dlc:
                        details += f'\nversion_name = "{tag} {version}"'
                    planes += block(modern if dlc else legacy, details)
            wings += block(str(deployment["state"]), planes)
        lines = production("small_plane_airframe_1" if dlc else "fighter_equipment_1", profile["production"]["fighter"], tag, tag + " Service Fighter" if dlc else None)
        if profile["production"].get("cas"):
            lines += production("small_plane_cas_airframe_1" if dlc else "CAS_equipment_1", profile["production"]["cas"], tag, tag + " Service Support" if dlc else None)
        return NOTE + block("air_wings", wings) + block("instant_effect", lines)
    aircraft = [("small_plane_airframe_1" if dlc else "fighter_equipment_1", profile["fighters"], "Service Fighter")]
    if profile["cas"]:
        aircraft.append(("small_plane_cas_airframe_1" if dlc else "CAS_equipment_1", profile["cas"], "Service Support"))
    wings = ""
    for kind, amount, version in aircraft:
        details = f"owner = {tag}\ncreator = {tag}\namount = {amount}"
        if dlc:
            details += f'\nversion_name = "{tag} {version}"'
        wings += block(kind, details)
    fighter = "small_plane_airframe_1" if dlc else "fighter_equipment_1"
    return NOTE + block("air_wings", block(str(row["capital"]), wings)) + block("instant_effect", production(fighter, profile["production"]["fighter"], tag, tag + " Service Fighter" if dlc else None))


def navy_output(tag, row, profile, dlc):
    ships = ""; groups = {}
    for kind, amount, modern, legacy, version in [("destroyer", profile["destroyers"], "ship_hull_light_2", "destroyer_2", "Coastal Escort"), ("submarine", profile["submarines"], "ship_hull_submarine_2", "submarine_2", "Coastal Submarine")]:
        groups[kind] = ""
        for n in range(amount):
            details = f"amount = 1\nowner = {tag}" + (f'\nversion_name = "{tag} {version}"' if dlc else "")
            ship = block("ship", f'name = "{tag} {version} {n + 1}"\ndefinition = {kind}\n' + block("equipment", block(modern if dlc else legacy, details)))
            ships += ship; groups[kind] += ship
    p = row.get("naval_base", row["ports"][0]["province"])
    fleet = block("fleet", f'name = "{tag} Coastal Service"\nnaval_base = {p}\n' + block("task_force", f'name = "{tag} Coastal Patrol"\nlocation = {p}\n' + ships))
    if "naval_production" in profile:
        tasks = "".join(block("task_force", f'name = "{tag} Coastal {role}"\nlocation = {p}\n' + body)
                        for role, body in groups.items() if body)
        fleet = block("fleet", f'name = "{tag} Coastal Service"\nnaval_base = {p}\n' + tasks)
    lines = production("convoy_1", profile["dockyard"], tag)
    if "naval_production" in profile:
        lines = ""
        for role, modern, legacy, version in [("convoy", "convoy_1", "convoy_1", None),
                                              ("destroyer", "ship_hull_light_2", "destroyer_2", "Coastal Escort"),
                                              ("submarine", "ship_hull_submarine_2", "submarine_2", "Coastal Submarine")]:
            lines += production(modern if dlc else legacy, profile["naval_production"][role], tag, tag + " " + version if dlc and version else None)
    return NOTE + block("units", fleet) + block("instant_effect", lines)


def ai_output(tag):
    base = f"allowed = {{ tag = {tag} original_tag = {tag} }}\nenable = {{ has_capitulated = no }}\nabort_when_not_enabled = yes\n"
    # Roles add to engine defaults; cancel the generic infantry/armor/mountain
    # ratios while selecting one country-specific affordable territorial role.
    for typ, ident, amount in [("role_ratio", "infantry", -80), ("role_ratio", "armor", -2), ("role_ratio", "mountaineers", -4), ("role_ratio", "ac_wf_territorial", 100), ("unit_ratio", "fighter", 15), ("unit_ratio", "convoy", 15), ("unit_ratio", "capital_ship", -10), ("equipment_production_factor", "infantry", 20), ("equipment_production_factor", "support", 15)]:
        base += block("ai_strategy", f"type = {typ}\nid = {ident}\nvalue = {amount}")
    peace = f"allowed = {{ tag = {tag} original_tag = {tag} }}\nenable = {{ has_war = no }}\nabort_when_not_enabled = yes\n"
    peace += block("ai_strategy", "type = ai_wanted_divisions_factor\nvalue = -60")
    peace += block("ai_strategy", "type = build_building\nid = industrial_complex\nvalue = 30")
    war = f"allowed = {{ tag = {tag} original_tag = {tag} }}\nenable = {{ has_war = yes }}\nabort_when_not_enabled = yes\n"
    war += block("ai_strategy", "type = ai_wanted_divisions_factor\nvalue = -25")
    war += block("ai_strategy", "type = equipment_production_factor\nid = infantry\nvalue = 20")
    if tag == "ERU":
        # Territorial infantry keeps the initial twelve formations affordable;
        # replacement production supports existing wings and coastal escorts.
        for typ, ident, value in [("unit_ratio", "cas", 5), ("unit_ratio", "screen_ship", 15),
                                  ("equipment_production_factor", "motorized", 10),
                                  ("build_building", "air_base", 5), ("build_building", "infrastructure", 10)]:
            base += block("ai_strategy", f"type = {typ}\nid = {ident}\nvalue = {value}")
    return NOTE + block(tag + "_wf_sustainment", base) + block(tag + "_wf_civilian", peace) + block(tag + "_wf_defense", war)


def outputs():
    manifest = json.loads((HERE / "foundation.json").read_text()); profiles = json.loads((HERE / "profiles.json").read_text())["countries"]
    output = {}; region_loc = []; loc = []
    for tag, row in manifest["countries"].items():
        profile = profiles[tag]
        for ident, cfg in row["placements"].items():
            output[row["baseline"][ident]["path"]] = state_output(row, ident, cfg)
            if not cfg.get("preserve_names"):
                region_loc.append(f' STATE_{ident}:0 "{cfg["name"]}"')
        for p in row["supply_hubs"]:
            if row.get("preserve_inherited_economy") and p not in row["new_victory_points"]:
                continue
            label = profile["name"] + (" Capital Centre" if p == row["capital_province"] else f" Logistics Centre {p}")
            region_loc.append(f' VICTORY_POINTS_{p}:0 "{label}"')
        output[row["country_history"]] = country_output(tag, row, profile)
        output[f"history/units/{tag}_wf_land.txt"] = land_output(tag, row, profile)
        for dlc in (False, True):
            output[f'history/units/{tag}_wf_air' + ("_bba" if dlc else "") + ".txt"] = air_output(tag, row, profile, dlc)
            output[f'history/units/{tag}_wf_navy' + ("_mtg" if dlc else "") + ".txt"] = navy_output(tag, row, profile, dlc)
        output[f"common/units/names_divisions/{tag}_world_foundation.txt"] = NOTE + block(tag + "_WF_INF", f'name = "Territorial Infantry Division"\nfor_countries = {{ {tag} }}\ncan_use = {{ always = yes }}\ndivision_types = {{ "infantry" }}\nfallback_name = "%d Territorial Infantry Division"')
        output[f"common/ai_strategy/{tag}_world_foundation.txt"] = ai_output(tag)
        support = "engineer = 1" + ("\nartillery = 1" if profile["reserve_artillery"] else "")
        target = block(tag + "_wf_territorial_target", "upgrade_prio = { factor = 1 }\n" + block("target_template", block("support", support) + block("regiments", "infantry = 6")))
        output[f"common/ai_templates/{tag}_world_foundation.txt"] = NOTE + block(tag + "_wf_territorial", f"available_for = {{ {tag} }}\nrole = ac_wf_territorial\nupgrade_prio = {{ factor = 5 }}\n" + target)
        research = f"name = {tag}_wf_research_name\ndesc = {tag}_wf_research_desc\nallowed = {{ tag = {tag} original_tag = {tag} }}\nenable = {{ always = yes }}\nabort_when_not_enabled = yes\n"
        research += block("research", "industry = 15\ninfantry_tech = 15\nsupport_tech = 12\nlight_fighter = 10\nelectronics = 5\ndd_tech = 2") + "weight = { factor = 1 }\n"
        output[f"common/ai_strategy_plans/{tag}_world_foundation.txt"] = NOTE + block(tag + "_wf_research", research)
        loc.append(f' {tag}_wf_research_name:0 "{profile["name"]}: Defensive Sustainment"')
        loc.append(f' {tag}_wf_research_desc:0 "Maintain civilian industry, affordable territorial formations, replacement aircraft and coastal logistics. These priorities are provisional gameplay calibration."')
    output.update(compose(ROOT, MOD, owner="world_foundation"))
    output["localisation/english/replace/ac_world_foundation_regions_l_english.yml"] = "\ufeffl_english:\n" + "\n".join(region_loc) + "\n"
    output["localisation/english/ac_world_foundation_l_english.yml"] = "\ufeffl_english:\n" + "\n".join(loc) + "\n"
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    failures = []
    for relative, expected in outputs().items():
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(expected, encoding="utf-8", newline="\n")
    if failures:
        raise SystemExit("World foundation generated output differs: " + ", ".join(failures))
    manifest = json.loads((HERE / "foundation.json").read_text())
    countries = manifest["countries"]
    print(f"World foundation: {sum(len(r['states']) for r in countries.values())} states, {len(countries)} histories, {len(countries) * 5} DLC-aware OOBs; " + ("consistent" if args.check else "generated"))


if __name__ == "__main__":
    main()
