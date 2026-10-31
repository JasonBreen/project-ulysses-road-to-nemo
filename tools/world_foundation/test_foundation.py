"""Actual-source foundation regressions; no HOI4 runtime or save emulation."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from placements import ROOT, MOD, derive, topology
from build import outputs, country_output
from registry import inspect, input_path_order
from script import parse, get, walk
from shared_logistics import compose, manifest_rows

parser = argparse.ArgumentParser()
parser.add_argument("--reference", default=os.environ.get("ULYSSES_GAME_ROOT"))
args, remaining = parser.parse_known_args()
REF = Path(args.reference) if args.reference else None
MANIFEST = json.loads((HERE / "foundation.json").read_text())
PROFILES = json.loads((HERE / "profiles.json").read_text())["countries"]


def read(relative):
    return parse((MOD / relative).read_text(encoding="utf-8-sig"))


def condition(body, dlcs):
    result = []
    for key, _, value in body:
        if key == "has_dlc":
            result.append(value.strip('"') in dlcs)
        elif key.upper() == "NOT":
            result.append(not condition(value, dlcs))
        else:
            raise AssertionError("Unhandled history condition: " + key)
    return all(result)


def selected(tree, dlcs):
    for key, op, value in tree:
        if key == "if":
            body = [n for n in value if n[0] not in ("limit", "else")] if condition(get(value, "limit"), dlcs) else get(value, "else", [])
            yield from selected(body, dlcs)
        else:
            yield key, op, value


class WorldFoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definitions, cls.graph, cls.centroids, cls.pixels, cls.size = topology()

    def test_registry_digest_order_is_platform_independent(self):
        names = ['history/units/BLK_land.txt', 'history/units/ac_shared.txt',
                 'common/characters/ac_governments.txt', 'common/characters/DEL.txt']
        order = []
        for kind, base in [(PurePosixPath, '/repo/mod'), (PureWindowsPath, 'G:/repo/mod')]:
            root = kind(base)
            paths = [root / name for name in reversed(names)]
            ordered = sorted(paths, key=lambda path: input_path_order(path, root))
            order.append([path.relative_to(root).as_posix() for path in ordered])
        self.assertEqual(order[0], order[1])
        self.assertEqual(sorted(names, key=lambda name: (name.casefold(), name)), order[0])

    def test_registry_contains_all_69_without_claiming_universal_playability(self):
        expected = inspect()
        self.assertEqual(expected, json.loads((HERE / "country_registry.json").read_text()))
        self.assertEqual(len(expected["countries"]), 69)
        self.assertEqual(len({r["tag"] for r in expected["countries"]}), 69)
        self.assertGreater(expected["summary"]["landowning_without_industry"], 0)
        self.assertEqual(expected["summary"]["landowning_with_foreign_capital"], 0)
        for tag in PROFILES:
            row = next(r for r in expected["countries"] if r["tag"] == tag)
            self.assertTrue(all(row["source_checks"].values()), row)
            self.assertEqual(row["support_status"], "authored_foundation_native_acceptance_pending")
        self.assertEqual(next(r for r in expected["countries"] if r["tag"] == "PLH")["support_status"], "unresolved_placeholder_do_not_infer")

    def test_generated_output_and_placements_are_reproducible(self):
        self.assertEqual(derive(), MANIFEST)
        for relative, text in outputs().items():
            self.assertEqual((MOD / relative).read_text(encoding="utf-8"), text, relative)

    def test_geometry_identity_and_owned_capital_supply_origins(self):
        self.assertEqual(hashlib.sha256((MOD / "map/provinces.bmp").read_bytes()).hexdigest(), MANIFEST["raster_sha256"])
        self.assertEqual(hashlib.sha256((MOD / "map/definition.csv").read_bytes()).hexdigest(), MANIFEST["definition_sha256"])
        for tag, row in MANIFEST["countries"].items():
            self.assertIn(row["capital"], row["states"])
            cap = get(read(row["baseline"][str(row["capital"])]["path"]), "state")
            points = {int(v[0][0]): int(v[1][0]) for k, _, v in get(cap, "history") if k == "victory_points"}
            self.assertEqual(max(points, key=points.get), row["capital_province"])
            for ident, baseline in row["baseline"].items():
                state = get(read(baseline["path"]), "state"); hist = get(state, "history")
                self.assertEqual(get(hist, "owner"), baseline["owner"])
                self.assertEqual([v for k, _, v in hist if k == "add_core_of"], baseline["cores"])
                self.assertEqual(int(get(state, "manpower")), baseline["manpower"])
                self.assertEqual([int(k) for k, _, _ in get(state, "provinces")], baseline["provinces"])
                self.assertNotEqual(int(ident), 171)

    def test_industry_and_supply_budgets_and_owned_adjacent_routes(self):
        for tag, row in MANIFEST["countries"].items():
            totals = {"civilian": 0, "military": 0, "dockyard": 0}
            owned = set(row["provinces"]); reached = {row["capital_province"]}
            for ident in row["states"]:
                state = get(read(row["baseline"][str(ident)]["path"]), "state"); buildings = get(get(state, "history"), "buildings")
                for key, field in [("civilian", "industrial_complex"), ("military", "arms_factory"), ("dockyard", "dockyard")]:
                    totals[key] += int(get(buildings, field, "0"))
                slots = sum(int(get(buildings, k, "0")) for k in ("industrial_complex", "arms_factory", "dockyard"))
                self.assertLessEqual(slots, {"town": 4, "city": 6, "large_city": 8}[get(state, "state_category")])
                self.assertEqual(int(get(buildings, "infrastructure")), 2)
            self.assertEqual(totals, {key: PROFILES[tag][key] for key in totals})
            for route in row["routes"]:
                self.assertEqual(route[0], row["capital_province"])
                self.assertTrue(set(route) <= owned)
                for a, b in zip(route, route[1:]):
                    self.assertIn(b, self.graph[a])
                reached.update(route)
            self.assertTrue(set(row["supply_hubs"]) <= reached)
            self.assertTrue(set(row["airports"].values()) <= reached)
            for port in row["ports"]:
                self.assertIn(port["province"], reached)
                self.assertTrue(self.definitions[port["province"]]["coastal"])
                self.assertTrue(any(self.definitions[n]["kind"] == "sea" for n in self.graph[port["province"]]))

    def test_four_dlc_branches_load_once_and_production_fits_actual_factories(self):
        for tag, row in MANIFEST["countries"].items():
            results = []
            for bba, mtg in [(False, False), (True, False), (False, True), (True, True)]:
                dlcs = ({"By Blood Alone"} if bba else set()) | ({"Man the Guns"} if mtg else set())
                history = list(selected(read(row["country_history"]), dlcs))
                rosters = [v.strip('"') for k, _, v in history if k in ("set_oob", "set_air_oob", "set_naval_oob")]
                self.assertEqual(len(rosters), 3)
                self.assertEqual(len(set(rosters)), 3)
                factories = {"military": 0, "dockyard": 0}; divisions = planes = ships = 0
                for roster in rosters:
                    tree = read("history/units/" + roster + ".txt")
                    for key, values in walk(tree):
                        if key == "division":
                            divisions += 1
                            self.assertIn(int(get(values, "location")), row["supply_hubs"])
                            self.assertEqual(get(values, "start_equipment_factor"), "1.0")
                        elif key == "ship":
                            ships += 1
                        elif key == "add_equipment_production":
                            kind = get(get(values, "equipment"), "type")
                            factories["dockyard" if kind == "convoy_1" else "military"] += int(get(values, "requested_factories"))
                            self.assertEqual(get(get(values, "equipment"), "creator"), tag)
                    for state, _, wings in get(tree, "air_wings", []):
                        count = sum(int(get(v, "amount")) for _, _, v in wings)
                        planes += count
                        self.assertLessEqual(count, row["placements"][state]["air_base"] * 200)
                        for _, _, details in wings:
                            self.assertEqual(get(details, "creator"), tag)
                            self.assertEqual(get(details, "owner"), tag)
                results.append((divisions, planes, ships))
                self.assertEqual(factories, {k: PROFILES[tag][k] for k in factories})
                reserves = {get(v, "type"): int(get(v, "amount")) for k, _, v in history if k == "add_equipment_to_stockpile"}
                self.assertEqual(reserves["motorized_equipment_1"], PROFILES[tag]["trucks"])
                self.assertEqual(reserves["train_equipment_1"], PROFILES[tag]["trains"])
                self.assertEqual(get(history, "set_convoys"), str(PROFILES[tag]["convoys"]))
                self.assertEqual(get(history, "set_fuel_ratio"), "1.0")
            self.assertEqual(len(set(results)), 1)
            p = PROFILES[tag]
            self.assertEqual(results[0], (p["divisions"], p["fighters"] + p["cas"], p["destroyers"] + p["submarines"]))

    def test_existing_leaders_policies_membership_and_new_game_only_history(self):
        for tag, row in MANIFEST["countries"].items():
            before = parse(row["country_history_source"]); after = read(row["country_history"])
            for key in ("recruit_character", "set_party_name", "set_popularities", "add_ideas", "set_stability", "set_war_support"):
                self.assertEqual([v for k, _, v in before if k == key], [v for k, _, v in after if k == key], (tag, key))
            self.assertIsNone(get(get(after, "set_politics"), "last_election"))
        for path in (MOD / "common/on_actions").glob("*.txt"):
            self.assertNotIn("_wf_land", path.read_text(encoding="utf-8-sig"))
        faction = (MOD / "history/countries/FCU - Central Usea.txt").read_text()
        for tag in PROFILES:
            self.assertIn("add_to_faction = " + tag, faction)

    def test_ai_targets_are_scoped_affordable_and_do_not_create_wars(self):
        for tag, profile in PROFILES.items():
            tree = read(f"common/ai_templates/{tag}_world_foundation.txt")
            body = tree[0][2]
            self.assertEqual([k for k, _, _ in get(body, "available_for")], [tag])
            self.assertEqual(get(body, "role"), "ac_wf_territorial")
            target = get(get(body, tag + "_wf_territorial_target"), "target_template")
            self.assertEqual(get(get(target, "regiments"), "infantry"), "6")
            self.assertEqual(get(get(target, "support"), "artillery") is not None, bool(profile["reserve_artillery"]))
            strategies = read(f"common/ai_strategy/{tag}_world_foundation.txt")
            for _, _, policy in strategies:
                self.assertEqual(get(get(policy, "allowed"), "original_tag"), tag)
                self.assertEqual(get(get(policy, "allowed"), "tag"), tag,
                                 "A dynamic civil-war clone must not cancel its generic AI role without this national template")
            text = (MOD / f"common/ai_strategy/{tag}_world_foundation.txt").read_text()
            self.assertNotIn("declare_war_on", text)
            self.assertNotIn("type = conquer", text)
            self.assertIn("type = ai_wanted_divisions_factor", text)

    def test_declared_foreign_history_marker_preserved_and_extra_effect_rejected(self):
        import build
        begin = "# BEGIN ECONOMY V2 NEW CAMPAIGN\n# New histories only; old saves are never reseeded.\nset_country_flag = ac_macro_history_eligible\n# END ECONOMY V2 NEW CAMPAIGN\n"
        with tempfile.TemporaryDirectory() as temp:
            for tag in ("SNS", "DEL"):
                row = MANIFEST["countries"][tag]; path = Path(temp) / row["country_history"]; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(begin + (MOD / row["country_history"]).read_text())
                with patch.object(build, "MOD", Path(temp)):
                    output = country_output(tag, row, PROFILES[tag])
                    self.assertEqual(output.count("# BEGIN ECONOMY V2 NEW CAMPAIGN"), 1)
                    self.assertIn("set_country_flag = ac_macro_history_eligible", output)
                    path.write_text(begin.replace("set_country_flag", "add_political_power = 100\nset_country_flag") + row["country_history_source"])
                    with self.assertRaisesRegex(ValueError, "Unexpected economic"):
                        country_output(tag, row, PROFILES[tag])

    def test_shared_generators_compose_both_orders_and_reject_mutated_foreign_tail(self):
        spec = importlib.util.spec_from_file_location("anea_foundation_generator", ROOT / "tools/anea/foundation.py")
        anea = importlib.util.module_from_spec(spec); spec.loader.exec_module(anea)
        a, w = anea.outputs(), outputs()
        for relative in ("map/railways.txt", "map/supply_nodes.txt"):
            self.assertEqual(a[relative], w[relative])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); mod = root / "mod/2985041246"
            for relative in ["tools/logistics_owners.json", "tools/anea/foundation.json", "tools/world_foundation/foundation.json"]:
                target = root / relative; target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / relative, target)
            for path in (MOD / "history/states").glob("*.txt"):
                target = mod / "history/states" / path.name; target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, target)
            for relative in ("map/railways.txt", "map/supply_nodes.txt"):
                target = mod / relative; target.parent.mkdir(parents=True, exist_ok=True); target.write_text((MOD / relative).read_text())
            for first, second in [("anea", "world_foundation"), ("world_foundation", "anea")]:
                for owner in (first, second, first):
                    for relative, text in compose(root, mod, owner=owner).items():
                        (mod / relative).write_text(text)
                self.assertEqual(compose(root, mod), {p: a[p] for p in ("map/railways.txt", "map/supply_nodes.txt")})
            path = mod / "map/supply_nodes.txt"; original = path.read_text()
            point = MANIFEST["countries"]["SNS"]["supply_hubs"][0]
            path.write_text(original.replace(f"1 {point}\n", f"2 {point}\n", 1))
            with self.assertRaisesRegex(ValueError, "mutated foreign"):
                compose(root, mod, owner="anea")
            path.write_text(original.replace(f"1 {point}\n", "", 1))
            with self.assertRaisesRegex(ValueError, "mutated foreign"):
                compose(root, mod, owner="anea")
            path.write_text(original + "1 999999\n")
            with self.assertRaisesRegex(ValueError, "Undeclared/foreign"):
                compose(root, mod, owner="anea")

    @unittest.skipUnless(REF and REF.exists(), "No installed read-only reference supplied")
    def test_effective_tech_equipment_modules_and_variant_order(self):
        files = {p.name: p for p in (REF / "common/technologies").glob("*.txt")}
        files.update({p.name: p for p in (MOD / "common/technologies").glob("*.txt")})
        definitions = {}
        for path in files.values():
            try:
                tree = parse(path.read_text(encoding="utf-8-sig"))
            except (ValueError, IndexError):
                continue
            definitions.update({k: v for k, _, v in get(tree, "technologies", [])})
        for tag, row in MANIFEST["countries"].items():
            for bba, mtg in [(False, False), (True, False), (False, True), (True, True)]:
                dlcs = ({"By Blood Alone"} if bba else set()) | ({"Man the Guns"} if mtg else set())
                enabled = {"convoy_1"}; modules = set(); variants = set()
                for key, _, value in selected(read(row["country_history"]), dlcs):
                    if key == "set_technology":
                        for tech, _, _ in value:
                            self.assertIn(tech, definitions)
                            # Paradox definitions may repeat an enable block;
                            # union every occurrence rather than its first one.
                            for section, _, entries in definitions[tech]:
                                if section == "enable_equipments":
                                    enabled.update(k for k, _, _ in entries)
                                elif section == "enable_equipment_modules":
                                    modules.update(k for k, _, _ in entries)
                    elif key == "create_equipment_variant":
                        self.assertIn(get(value, "type"), enabled)
                        for _, _, module in get(value, "modules", []):
                            self.assertIn(module, modules)
                        variants.add(get(value, "name"))
                    elif key == "add_equipment_to_stockpile":
                        self.assertIn(get(value, "type"), enabled)
                        if get(value, "variant_name"):
                            self.assertIn(get(value, "variant_name"), variants)
                    elif key in ("set_oob", "set_air_oob", "set_naval_oob"):
                        roster = read("history/units/" + value.strip('"') + ".txt")
                        for _, _, wings in get(roster, "air_wings", []):
                            for equipment, _, details in wings:
                                self.assertIn(equipment, enabled)
                                if get(details, "version_name"):
                                    self.assertIn(get(details, "version_name"), variants)
                        for node, body in walk(roster):
                            if node == "equipment":
                                if get(body, "type"):
                                    self.assertIn(get(body, "type"), enabled)
                                else:
                                    for equipment, _, details in body:
                                        self.assertIn(equipment, enabled)
                                        if get(details, "version_name"):
                                            self.assertIn(get(details, "version_name"), variants)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + remaining, verbosity=2)
