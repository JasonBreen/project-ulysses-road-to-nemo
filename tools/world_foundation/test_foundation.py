"""Actual-source foundation regressions; no HOI4 runtime or save emulation."""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
import os
import re
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
from script import parse, get, walk, setv
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

    def test_registry_classifies_placeholder_emergent_and_leader_representation(self):
        rows = inspect()['countries']
        classes = {kind: sum(row['start_classification'] == kind for row in rows)
                   for kind in ('active', 'emergent', 'placeholder')}
        self.assertEqual({'active': 61, 'emergent': 7, 'placeholder': 1}, classes)
        self.assertEqual('placeholder', next(row for row in rows if row['tag'] == 'PLH')['start_classification'])
        fcu = next(row for row in rows if row['tag'] == 'FCU')
        self.assertIn('provisional', fcu['leader_representation']['term_source'])
        self.assertEqual(14, sum(row['tag'] not in ('EVA',) and row['capital_source_layer'] == 'approved provisional capital district' for row in rows))
        for row in rows:
            if row['leader_representation']['kind'] == 'government office':
                self.assertTrue(all(name.endswith('_ac_government_office') for name in row['recruited_active_party_leaders']))

    def test_integrated_fiscal_and_institution_profiles_cover_every_history(self):
        if not (ROOT / 'tools/economy_v2/profiles.json').exists() or not (ROOT / 'tools/institutions/profiles.json').exists():
            self.skipTest('Shared owners are not integrated into this foundation-only candidate')
        report = inspect()
        self.assertEqual(2, report['schema'])
        self.assertIn('CRLF normalized', report['support_profile_hash_normalization'])
        for row in report['countries']:
            self.assertGreater(row['fiscal_profile']['gdp_billion'], 0, row['tag'])
            self.assertIn('not canon', row['fiscal_profile']['source_layer'])
            self.assertTrue(row['political_institution']['institution'])
            self.assertIn('provisional', row['political_institution']['source_layer'])
            self.assertIsInstance(row['regional_contracts'], list)
            self.assertIn('native', row['scope_note'])
    def test_prerequisite_repair_workflow_gates_remain_separate(self):
        workflow = (ROOT / '.github/workflows/static-validation.yml').read_text()
        commands = re.findall(r'^\s+run:\s*([^\n]+)', workflow, re.M)
        for script in ('tools/world_foundation/test_foundation.py', 'tools/overhaul/check_release_plan.py',
                       'tools/Test-OverhaulRepairs.py', 'tools/Test-DecisionUI.py', 'tools/Test-FocusScreenRepairs.py'):
            matching = [line for line in commands if script in line]
            self.assertEqual(matching, ['python -B ' + script], script)

    def test_prerequisite_regional_overlay_reuses_world_owned_names(self):
        def labels(name):
            return dict(re.findall(r'^\s*(\w+):\d+\s+"([^\n]*)"',
                (MOD / 'localisation/english/replace' / name).read_text(encoding='utf-8-sig'), re.M))
        repair = labels('ac_overhaul_regions_l_english.yml')
        world = labels('ac_world_foundation_regions_l_english.yml')
        shared = set(repair) & set(world)
        self.assertEqual(len(shared), 8)
        manifest = json.loads((ROOT / 'tools/overhaul/regional_labels.json').read_text())
        changes = {r['key']: r for r in manifest['changes']}
        for key in shared:
            self.assertEqual(repair[key], world[key], key)
            self.assertEqual(changes[key]['name_owner'], 'world_foundation')
        self.assertEqual(repair['STATE_268'], 'Delarus Capital District')
        self.assertEqual(repair['VICTORY_POINTS_7895'], 'San Salvacion Logistics Centre 7895')

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
            owned = set(row["provinces"]); roots = {c["root"] for c in row.get("components", [])} or {row["capital_province"]}
            reached = set(roots)
            for ident in row["states"]:
                state = get(read(row["baseline"][str(ident)]["path"]), "state"); buildings = get(get(state, "history"), "buildings")
                for key, field in [("civilian", "industrial_complex"), ("military", "arms_factory"), ("dockyard", "dockyard")]:
                    totals[key] += int(get(buildings, field, "0"))
                slots = sum(int(get(buildings, k, "0")) for k in ("industrial_complex", "arms_factory", "dockyard"))
                if row.get("preserve_inherited_economy"):
                    slots += int(get(buildings, "fuel_silo", "0"))
                self.assertLessEqual(slots, {"town": 4, "city": 6, "large_city": 8, "metropolis": 10}[get(state, "state_category")])
                self.assertEqual(int(get(buildings, "infrastructure")), row["placements"][str(ident)]["infrastructure"])
            self.assertEqual(totals, {key: PROFILES[tag][key] for key in totals})
            for route in row["routes"]:
                self.assertIn(route[0], roots)
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
                assignments = Counter(); wing_counts = Counter()
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
                            naval = kind == "convoy_1" or kind.startswith("ship_hull_") or kind in ("destroyer_2", "submarine_2")
                            factories["dockyard" if naval else "military"] += int(get(values, "requested_factories"))
                            assignments[kind] += int(get(values, "requested_factories"))
                            self.assertEqual(get(get(values, "equipment"), "creator"), tag)
                    for state, _, wings in get(tree, "air_wings", []):
                        count = sum(int(get(v, "amount")) for _, _, v in wings)
                        planes += count
                        self.assertLessEqual(count, row["placements"][state]["air_base"] * 200)
                        for _, _, details in wings:
                            self.assertEqual(get(details, "creator"), tag)
                            self.assertEqual(get(details, "owner"), tag)
                        wing_counts.update({kind: int(get(details, "amount")) for kind, _, details in wings})
                results.append((divisions, planes, ships))
                self.assertEqual(factories, {k: PROFILES[tag][k] for k in factories})
                expected = {kind: amount for kind, amount in PROFILES[tag]["production"].items() if kind not in ("fighter", "cas")}
                fighter = "small_plane_airframe_1" if bba else "fighter_equipment_1"
                cas = "small_plane_cas_airframe_1" if bba else "CAS_equipment_1"
                expected[fighter] = PROFILES[tag]["production"]["fighter"]
                if PROFILES[tag]["production"].get("cas"):
                    expected[cas] = PROFILES[tag]["production"]["cas"]
                naval_plan = PROFILES[tag].get("naval_production", {"convoy": PROFILES[tag]["dockyard"]})
                for role, kind in [("convoy", "convoy_1"), ("destroyer", "ship_hull_light_2" if mtg else "destroyer_2"),
                                   ("submarine", "ship_hull_submarine_2" if mtg else "submarine_2")]:
                    if naval_plan.get(role):
                        expected[kind] = naval_plan[role]
                self.assertEqual(dict(assignments), expected, (tag, bba, mtg))
                self.assertEqual(wing_counts[fighter], PROFILES[tag]["fighters"])
                self.assertEqual(wing_counts[cas], PROFILES[tag]["cas"])
                reserves = {get(v, "type"): int(get(v, "amount")) for k, _, v in history if k == "add_equipment_to_stockpile"}
                self.assertEqual(reserves["motorized_equipment_1"], PROFILES[tag]["trucks"])
                self.assertEqual(reserves["train_equipment_1"], PROFILES[tag]["trains"])
                self.assertEqual(reserves[fighter], PROFILES[tag].get("reserve_fighters", 12 if PROFILES[tag]["fighters"] > 24 else 8))
                if PROFILES[tag]["cas"]:
                    self.assertEqual(reserves[cas], PROFILES[tag].get("reserve_cas", 6))
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
        for tag in ("SNS", "AMB", "UGE", "DEL"):
            self.assertIn("add_to_faction = " + tag, faction)
        self.assertNotIn("add_to_faction = ERU", faction)
        self.assertNotIn("create_faction", (MOD / MANIFEST["countries"]["ERU"]["country_history"]).read_text())

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
            for tag in ("SNS", "DEL", "ERU"):
                row = MANIFEST["countries"][tag]; path = Path(temp) / row["country_history"]; path.parent.mkdir(parents=True, exist_ok=True)
                current = re.sub(r'# BEGIN ECONOMY V2 NEW CAMPAIGN\n.*?# END ECONOMY V2 NEW CAMPAIGN\n?', '',
                                 (MOD / row["country_history"]).read_text(), flags=re.S)
                path.write_text(begin + current)
                with patch.object(build, "MOD", Path(temp)):
                    output = country_output(tag, row, PROFILES[tag])
                    self.assertEqual(output.count("# BEGIN ECONOMY V2 NEW CAMPAIGN"), 1)
                    self.assertIn("set_country_flag = ac_macro_history_eligible", output)
                    path.write_text(begin + begin + current)
                    with self.assertRaisesRegex(ValueError, 'Invalid economic eligibility'):
                        country_output(tag, row, PROFILES[tag])
                    path.write_text(begin.replace("set_country_flag", "add_political_power = 100\nset_country_flag") + row["country_history_source"])
                    with self.assertRaisesRegex(ValueError, "Unexpected economic"):
                        country_output(tag, row, PROFILES[tag])

    def test_erusea_retains_every_factory_resource_floor_port_and_victory_point(self):
        row = MANIFEST["countries"]["ERU"]; profile = PROFILES["ERU"]
        self.assertEqual(row["capital_province"], 644)
        self.assertEqual(row["airports"]["349"], 1118)
        for ident, baseline in row["baseline"].items():
            state = get(read(baseline["path"]), "state"); hist = get(state, "history"); buildings = get(hist, "buildings")
            original = baseline["economy"]
            for key, field in [("civilian", "industrial_complex"), ("military", "arms_factory"), ("dockyard", "dockyard")]:
                self.assertEqual(int(get(buildings, field, "0")), original[key], (ident, key))
            resources = {k: float(v) for k, _, v in get(state, "resources")}
            additions = profile["resource_additions"].get(ident, {})
            self.assertEqual(resources, {k: float(v) + additions.get(k, 0) for k, v in original["resources"].items()})
            self.assertGreaterEqual(int(get(buildings, "infrastructure")), original["infrastructure"])
            for p, level in original["naval_bases"].items():
                self.assertEqual(int(get(get(buildings, p), "naval_base")), level)
            actual_vps = [v for k, _, v in hist if k == "victory_points"]
            for vp in original["victory_points"]:
                self.assertIn(vp, actual_vps, ident)
        self.assertEqual(sum(len(b["economy"]["naval_bases"]) for b in row["baseline"].values()), 16)
        self.assertEqual(sum(p["inherited"] for p in row["ports"]), 16)
        # Existing state/VP identities are not relabeled by this foundation.
        loc = (MOD / "localisation/english/replace/ac_world_foundation_regions_l_english.yml").read_text(encoding="utf-8-sig")
        for ident in row["baseline"]:
            self.assertNotIn(f" STATE_{ident}:", loc)
        self.assertNotIn(" VICTORY_POINTS_644:", loc)
        self.assertNotIn(" VICTORY_POINTS_4600:", loc)

    def test_erusea_component_ports_routes_and_detached_deployments(self):
        row = MANIFEST["countries"]["ERU"]
        groups = row["components"]
        self.assertEqual(len(groups), 30)
        self.assertEqual(sum(len(c["provinces"]) for c in groups), len(row["provinces"]))
        self.assertEqual(set().union(*(set(c["provinces"]) for c in groups)), set(row["provinces"]))
        self.assertEqual(len(row["ports"]), 45)
        self.assertEqual(row["routes"], [r for c in groups for r in c["routes"]])
        self.assertEqual(row["supply_hubs"], [p for c in groups for p in c["supply_hubs"]])
        for component in groups:
            owned = set(component["provinces"]); reached = {component["root"]}
            self.assertTrue(component["ports"])
            self.assertTrue(set(component["ports"]) <= owned)
            if component["index"]:
                self.assertIn(component["root"], component["ports"])
                self.assertNotIn(644, owned)
            for route in component["routes"]:
                self.assertEqual(route[0], component["root"])
                self.assertTrue(set(route) <= owned, "A rail must never jump water to another owned island")
                for a, b in zip(route, route[1:]):
                    self.assertIn(b, self.graph[a])
                reached.update(route)
            self.assertTrue(set(component["terminals"]) <= reached)
            deployments = [p for p in row["land_deployments"] if p in owned]
            self.assertEqual(len(deployments), 8 if not component["index"] else 1 if component["deployment"] else 0)
        airports = {int(k): int(v[0][0]) for k, _, v in read("map/airports.txt") if k.isdigit() and v}
        buildings = [line.split(";") for line in (MOD / "map/buildings.txt").read_text().splitlines() if ";" in line]
        naval_spawns = {(int(r[0]), int(r[6])) for r in buildings if r[1] == "naval_base_spawn"}
        airfield_positions = {int(r[0]) for r in buildings if r[1] == "air_base"}
        for port in row["ports"]:
            self.assertTrue(any((port["state"], p) in naval_spawns for p in self.graph[port["province"]]),
                            "A coastal receiving port also needs a same-state adjacent-sea spawn position")
        for state, p in row["airports"].items():
            self.assertEqual(airports[int(state)], p)
            self.assertIn(int(state), airfield_positions)
        self.assertEqual(sum(d["fighters"] for d in row["air_deployments"]), 96)
        self.assertEqual(sum(d["cas"] for d in row["air_deployments"]), 24)

    def test_original_four_country_outputs_and_placements_remain_exact(self):
        baseline = json.loads((HERE / "original_four.json").read_text())
        for tag, digest in baseline["profiles_sha256"].items():
            self.assertEqual(hashlib.sha256(json.dumps(PROFILES[tag], sort_keys=True).encode()).hexdigest(), digest)
        for tag, digest in baseline["country_rows_sha256"].items():
            self.assertEqual(hashlib.sha256(json.dumps(MANIFEST["countries"][tag], sort_keys=True).encode()).hexdigest(), digest)
        for relative, digest in baseline["generated_files_sha256"].items():
            self.assertEqual(hashlib.sha256((MOD / relative).read_text(encoding="utf-8").encode()).hexdigest(), digest, relative)
        for relative, digest in baseline["history_ast_sha256_except_declared_macro_eligibility"].items():
            tree = [n for n in read(relative) if n != ["set_country_flag", "=", "ac_macro_history_eligible"]]
            self.assertEqual(hashlib.sha256(json.dumps(tree, sort_keys=True).encode()).hexdigest(), digest, relative)

    def test_erusea_calibration_worksheet_and_bounded_resource_additions(self):
        report = json.loads((HERE / "erusea_budget.json").read_text())
        self.assertEqual(report["profile_sha256"], hashlib.sha256(json.dumps(PROFILES["ERU"], sort_keys=True).encode()).hexdigest())
        self.assertEqual(report["placements_sha256"], hashlib.sha256(json.dumps(MANIFEST["countries"]["ERU"]["placements"], sort_keys=True).encode()).hexdigest())
        for relative, digest in report["source_files_sha256"].items():
            if relative.startswith("mod/"):
                self.assertEqual(hashlib.sha256((MOD / relative[4:]).read_bytes()).hexdigest(), digest, relative)
        if REF:
            from budget import worksheet
            self.assertEqual(report, worksheet(REF))
        self.assertEqual(len(report["branches"]), 4)
        for branch in report["branches"]:
            self.assertTrue(all(v >= 0 for v in branch["domestic_margin"].values()))
            self.assertGreater(report["daily_fuel_gain_lower_worksheet"], branch["daily_combined_reference_fuel"])
            self.assertEqual(set(branch["30_day_replacements_no_output_bonus_at_50_percent_mil_efficiency"]), set(PROFILES["ERU"]["production"]) | set(PROFILES["ERU"]["naval_production"]))
            self.assertGreater(branch["daily_with_whole_navy_in_combat_reference_fuel"], branch["daily_combined_reference_fuel"])
        self.assertEqual(report["initial_land_equipment_need"], {"infantry_equipment": 7320, "support_equipment": 360, "artillery_equipment": 144})
        self.assertEqual(report["infantry_per_formation"]["daily_supply"], 0.54)
        self.assertLess(0.54, report["defines"]["NBuildings.SUPPLY_PORT_LEVEL_THROUGHPUT"])

    def test_erusea_placement_rejects_changed_factories_and_lost_states(self):
        from erusea import derive_erusea
        row = MANIFEST["countries"]["ERU"]
        states = {}
        for ident, baseline in row["baseline"].items():
            state = get(read(baseline["path"]), "state")
            states[int(ident)] = {k: copy.deepcopy(baseline[k]) for k in ("path", "owner", "cores", "manpower", "provinces")}
            states[int(ident)]["body"] = state
        airports = {int(k): int(v[0][0]) for k, _, v in read("map/airports.txt") if k.isdigit() and v}
        def run(source, profile=None, prior=None):
            return derive_erusea(source, row["country_history"], row["country_history_source"], prior or row,
                                 self.definitions, self.graph, airports, profile or PROFILES["ERU"])
        self.assertEqual(run(states), row)
        changed = copy.deepcopy(states)
        setv(get(get(changed[349]["body"], "history"), "buildings"), "arms_factory", "5")
        with self.assertRaisesRegex(ValueError, "factory placement changed"):
            run(changed)
        changed = copy.deepcopy(states); changed[276]["owner"] = "SNS"
        with self.assertRaisesRegex(ValueError, "Protected state identity"):
            run(changed)
        profile = copy.deepcopy(PROFILES["ERU"]); profile["resource_additions"]["349"]["steel"] = -1
        with self.assertRaisesRegex(ValueError, "must be additive"):
            run(states, profile=profile)
        prior = copy.deepcopy(row); prior["baseline"]["349"]["economy"]["resources"]["steel"] = "0.5"
        self.assertEqual(run(states, prior=prior)["placements"]["349"]["resources"]["steel"], "32.5")

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
