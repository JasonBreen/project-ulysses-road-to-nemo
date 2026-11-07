"""Static and offline checks for the Central Usea (FCU) Usea Depth package.

Covers the README test checklist: counts against budget.json, single imports inside
the package marker, bands, titles and captions, localisation and labels, art,
government changes, fiscal guards, banned effects, the AI war-start simulation on the
World harness from tools/Test-ContinentalWar.py, and every --check. None of this is
native HOI4 evidence.
"""
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / "tools")]
from usea_depth import seams  # noqa: E402
import content as C  # noqa: E402
import narrative as N  # noqa: E402

MOD = ROOT / "mod/2985041246"
spec = importlib.util.spec_from_file_location("ucw", ROOT / "tools/Test-ContinentalWar.py")
ucw = importlib.util.module_from_spec(spec)
sys.modules["ucw"] = ucw
spec.loader.exec_module(ucw)
from economy_script import fields  # noqa: E402

FILES = {
    "focus": "common/national_focus/ac_ud_fcu.txt", "ideas": "common/ideas/ac_ud_fcu.txt", "events": "events/ac_ud_fcu.txt",
    "effects": "common/scripted_effects/ac_ud_fcu.txt", "characters": "common/characters/ac_ud_fcu.txt",
    "on_actions": "common/on_actions/ac_ud_fcu.txt", "gfx": "interface/ac_ud_fcu.gfx",
}
LOC = MOD / "localisation/english/ac_ud_fcu_l_english.yml"
MARKER = seams.MARKERS["fcu"][0]
BUDGET = json.loads((HERE / "budget.json").read_text(encoding="utf-8"))


def read(key):
    return (MOD / FILES[key]).read_text(encoding="utf-8-sig")


def script_text():
    return "\n".join(read(k) for k in FILES if k != "gfx")


def loc_keys(path):
    return dict(re.findall(r'(?m)^\s*([\w.]+):\d*\s+"(.*)"\s*$', path.read_text(encoding="utf-8-sig")))


def all_loc():
    keys = {}
    for path in (MOD / "localisation/english").rglob("*.yml"):
        keys.update(loc_keys(path))
    return keys


class DepthWorld(ucw.World):
    """The Continental War harness with this package's focuses, events, effects and weekly hook."""

    def __init__(self, when="1991.1.1", **kwargs):
        super().__init__(when, **kwargs)
        self.effects.update(ucw.mapping(ucw.load(FILES["effects"])))
        self.events.update({ucw.mapping(v)["id"]: (k, v) for k, _, v in ucw.load(FILES["events"]) if k == "country_event"})
        self.focuses.update({ucw.mapping(v)["id"]: v for k, _, v in ucw.load(FILES["focus"]) if k == "shared_focus"})
        self.mine = [ucw.mapping(v)["id"] for k, _, v in ucw.load(FILES["focus"]) if k == "shared_focus"]
        self.politics = []
        self.characters = {"FCU": {"FCU_robert_sinclair"}}

    def trigger(self, nodes, country):
        rest, answers = [], []
        for key, operator, value in nodes:
            if key == "has_character":
                answers.append(value in self.characters.setdefault(country.tag, set()))
            elif key in ("NOT", "OR", "AND") and any(k == "has_character" for k, _, _ in value):
                parts = [self.trigger([part], country) for part in value]
                answers.append(any(parts) if key == "OR" else (not all(parts) if key == "NOT" else all(parts)))
            else:
                rest.append((key, operator, value))
        return all(answers) and super().trigger(rest, country)

    def execute(self, nodes, country):
        branch = None
        for key, operator, value in nodes:
            if key in ("if", "else_if", "else"):
                if key == "if":
                    branch = False
                elif branch is None:
                    raise AssertionError("Orphaned " + key)
                condition = key == "else" or self.trigger(ucw.mapping(value)["limit"], country)
                if not branch and condition:
                    self.execute([node for node in value if node[0] != "limit"], country)
                    branch = True
                continue
            branch = None
            if key == "add_tech_bonus":
                data = fields(value)
                assert int(data["uses"]) == 1 and 0 < float(data["bonus"]) <= 1, data
                country.bonuses.append(data)
            elif key.startswith("ac_econ_") and key not in self.effects:
                assert self.fiscal, "Unguarded fiscal call: " + key
            elif key in ("set_politics", "set_popularities"):
                self.politics.append((country.tag, key, fields(value)))
            elif key == "recruit_character":
                self.characters.setdefault(country.tag, set()).add(value)
            elif key == "promote_character":
                data = fields(value)
                assert data["character"] in self.characters.get(country.tag, set()), data
                self.politics.append((country.tag, key, data))
            else:
                super().execute([(key, operator, value)], country)

    def weight(self, ident):
        return float(fields(ucw.mapping(self.focuses[ident])["ai_will_do"])["factor"])

    def chronicle(self, country):
        """Flags the ac_ur on_actions set on FCU (Chronicle, 1995 / 12.31 and 1997 / 05.30), with ac_ur.3's AI option."""
        if self.today >= ucw.day("1995.12.31"):
            country.flags.setdefault("ac_ur_skully_recorded", None)
        if self.today >= ucw.day("1997.5.30"):
            country.flags.setdefault("ac_ur_coup_started", None)
        if self.today >= ucw.day("1997.6.6"):
            country.flags.setdefault("ac_ur_coup_defeated", None)
        if self.today >= ucw.day("1997.11.1"):
            country.focuses.add("FCU_ur_assessment")

    def ai_path(self, until):
        """Weekly AI play for FCU on this package's focuses: highest weight first, cancelled if invalid on completion."""
        fcu = self.countries["FCU"]
        current, left, started = None, 0, None
        while self.today < ucw.day(until):
            self.today += 7
            self.chronicle(fcu)
            self.tick()
            self.execute([("ac_ud_fcu_weekly", "=", "yes")], fcu)
            if current:
                left -= 7
                if left <= 0:
                    if self.focus_available(current, "FCU"):
                        self.complete(current, "FCU")
                    current = None
            if not current:
                options = [i for i in self.mine if i not in fcu.focuses and self.weight(i) > 0 and self.focus_available(i, "FCU")]
                if options:
                    current = max(options, key=lambda i: (self.weight(i), -self.mine.index(i)))
                    left = 7 * int(ucw.mapping(self.focuses[current])["cost"])
            self.drain()
            if started is None and "ac_ucw_war_started" in self.globals:
                started = self.today
        return started


class CentralUsea(unittest.TestCase):
    def test_counts_match_budget_and_each_id_is_imported_once_inside_the_marker(self):
        trees = {}
        for f in C.FOCUSES:
            trees[f.tree] = trees.get(f.tree, 0) + 1
        self.assertEqual({"package": "fcu", "marker": MARKER, "focuses": {"FCU": len(C.FOCUSES)}, "trees": trees,
                          "events": len(N.EVENTS)}, BUDGET)
        self.assertEqual(sum(BUDGET["trees"].values()), BUDGET["focuses"]["FCU"])
        defined = re.findall(r"(?m)^\tid = (FCU_ud_\w+)$", read("focus"))
        self.assertEqual([f.id for f in C.FOCUSES], defined)
        self.assertEqual(BUDGET["events"], len(re.findall(r"(?m)^\tid = ac_ud_fcu\.\d+$", read("events"))))
        imports = {}
        for path in seams.FOCUS.glob("*.txt"):
            for ident in re.findall(r"(?m)^\s*shared_focus = (FCU_ud_\w+)\s*$", path.read_text(encoding="utf-8-sig")):
                imports.setdefault(ident, []).append(path.name)
        self.assertEqual({f.id: ["FCU_opening.txt" if f.tree == C.OPENING else "FCU.txt"] for f in C.FOCUSES}, imports)
        for name, tree in (("FCU_opening.txt", C.OPENING), ("FCU.txt", C.WAR)):
            blocks = {n: ids for n, ids, _ in seams.import_blocks((seams.FOCUS / name).read_text(encoding="utf-8-sig"))}
            self.assertEqual([f.id for f in C.FOCUSES if f.tree == tree], blocks[MARKER], name)

    def test_bands_titles_and_captions(self):
        positions = seams.tree_positions()
        opening = [f.id for f in C.FOCUSES if f.tree == C.OPENING]
        war = [f.id for f in C.FOCUSES if f.tree == C.WAR]
        self.assertEqual([], seams.band_violations(positions[C.OPENING], opening, 0, 23, 6))
        self.assertEqual([], seams.band_violations(positions[C.WAR], war, 42, 94))
        for tree in (C.OPENING, C.WAR):
            nodes = positions[tree]
            for ident in (opening if tree == C.OPENING else war):
                x, y = nodes[ident]
                for other, (ox, oy) in nodes.items():
                    if other != ident:
                        self.assertFalse(abs(x - ox) * 96 < 147 and abs(y - oy) * 160 < 54, (ident, other))
        for f in C.FOCUSES:
            self.assertTrue(seams.title_fits(f.title), f.id)
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/Test-FocusScreenRepairs.py")], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout[-3000:] + result.stderr[-3000:])

    def test_opening_era_gates_and_war_gates(self):
        for f in C.FOCUSES:
            available = ucw.mapping(DepthWorld().focuses[f.id])["available"]
            text = " ".join(str(node) for node in available)
            if f.tree == C.OPENING:
                self.assertIn(C.OPENING_GUARD, read("focus").split("id = " + f.id + "\n", 1)[1].split("cancel_if_invalid")[0], f.id)
            else:
                self.assertIn("ac_ucw_active", text, f.id)
        stamps = {"date > 1996.4.19": ("evacuation", "stonehenge"), "has_country_flag = ac_ur_coup_started": ("coup",)}
        for gate, sections in stamps.items():
            for f in C.FOCUSES:
                if f.section in sections and f.id not in ("FCU_ud_interception_drills", "FCU_ud_neutral_custody_protocol",
                                                           "FCU_ud_federal_battery_custody"):
                    self.assertTrue(gate in f.gate or "date > 199" in f.gate or "ac_ur_coup" in f.gate
                                    or "ac_sp_stonehenge_complete" in f.gate, f.id)
        for f in C.FOCUSES:
            if f.section == "impact" and f.id != "FCU_ud_relief_planning_cell":
                self.assertTrue("date > 1999.7.7" in f.gate or "date > 1998.12.31" in f.gate, f.id)

    def test_localisation_is_complete_with_bom_and_flag_labels(self):
        self.assertTrue(LOC.read_bytes().startswith(b"\xef\xbb\xbf"))
        own = loc_keys(LOC)
        raw = re.findall(r'(?m)^\s*([\w.]+):\d*\s', LOC.read_text(encoding="utf-8-sig"))
        self.assertEqual(len(raw), len(set(raw)))
        everywhere = all_loc()
        needed = [f.id for f in C.FOCUSES] + [f.id + "_desc" for f in C.FOCUSES]
        needed += [i[0] for i in C.IDEAS] + [i[0] + "_desc" for i in C.IDEAS]
        needed += ["FCU_ud_%s_office" % s for s in ("directorate", "unity")] + ["FCU_ud_%s_office_desc" % s for s in ("directorate", "unity")]
        needed += list(C.TOOLTIPS) + list(C.VARIABLE_LABELS)
        for number, e in N.EVENTS.items():
            needed.append(e["id"] + ".t")
            needed += ["%s.d.%s" % (e["id"], "abc"[i]) for i in range(len(e["variants"]))] or [e["id"] + ".d"]
            needed += ["%s.%s" % (e["id"], o[0]) for o in e["options"]]
        for key in needed:
            self.assertIn(key, own, key)
        text = script_text()
        for flag in set(re.findall(r"has_(?:country|global)_flag = (\w+)", text)) | set(re.findall(r"set_country_flag = (\w+)", text)):
            self.assertIn(flag, everywhere, "Unlabelled flag " + flag)
        for key in re.findall(r"custom_effect_tooltip = (\w+)", text):
            self.assertIn(key, own)
        for value in own.values():
            self.assertFalse(set(value) & set("“”‘’"), value[:60])

    def test_events_are_long_form_with_source_lines(self):
        own = loc_keys(LOC)
        for number, e in N.EVENTS.items():
            keys = ["%s.d.%s" % (e["id"], "abc"[i]) for i in range(len(e["variants"]))] or [e["id"] + ".d"]
            for key in keys:
                body = own[key].replace("\\n", "\n").replace('\\"', '"')
                self.assertEqual([], seams.event_problems(body), key)
                self.assertTrue(body.rsplit("\n\n", 1)[-1].startswith(seams.LAYERS), key)
        self.assertGreaterEqual(len(N.EVENTS) * 5, len(C.FOCUSES) - 10, "About one event per five focuses")

    def test_icons_shines_and_textures_are_mod_art(self):
        gfx = read("gfx")
        sprites = dict(re.findall(r'name = "(\w+)" texturefile = "([^"]+)"', gfx))
        for f in C.FOCUSES:
            self.assertIn("icon = GFX_ac_ud_focus_" + f.id, read("focus"))
            for line in seams.focus_sprites("fcu", f.id):
                self.assertIn(line, gfx)
        for name, texture in sprites.items():
            self.assertTrue(texture.startswith("gfx/AC_usea_depth/fcu/"), name)
            self.assertTrue((MOD / texture).is_file(), texture)
            self.assertNotIn("shine_overlay", texture)
        for ident, *_ in C.IDEAS:
            picture = re.search(r"\t\t%s = \{\n\t\t\tpicture = (\w+)" % ident, read("ideas"))[1]
            self.assertIn("GFX_idea_" + picture, sprites)
        for picture in set(re.findall(r"picture = (GFX_\w+)", read("events"))):
            self.assertIn(picture, sprites)
        for portrait in re.findall(r'large = "(\w+)"', read("characters")):
            self.assertIn(portrait, sprites)
        assets = json.loads((HERE / "assets.json").read_text(encoding="utf-8"))
        self.assertEqual(len({row["pixels_sha256"] for row in assets["textures"]}), len(assets["textures"]))
        self.assertEqual({"gfx/AC_usea_depth/fcu/focus/%s.dds" % f.id for f in C.FOCUSES},
                         {row["file"] for row in assets["textures"] if "/focus/" in row["file"]})

    def test_government_changes_only_in_regime_effects_with_ai_weight_zero(self):
        text = script_text()
        self.assertEqual([], seams.political_violations(text))
        effects = ucw.mapping(ucw.load(FILES["effects"]))
        regimes = sorted(k for k in effects if k.startswith("ac_ud_fcu_regime_"))
        self.assertEqual(["ac_ud_fcu_regime_directorate", "ac_ud_fcu_regime_restoration", "ac_ud_fcu_regime_unity"], regimes)
        world = DepthWorld()
        reaching = [i for i in world.mine if "ac_ud_fcu_regime_" in str(world.focuses[i])]
        self.assertEqual(sorted(f.id for f in C.FOCUSES if f.regime), sorted(reaching))
        for ident in reaching:
            self.assertEqual(0, world.weight(ident), ident)
        for number, (_, nodes) in world.events.items():
            if number.startswith("ac_ud_fcu."):
                for kind, _, option in nodes:
                    if kind == "option":
                        self.assertNotIn("ac_ud_fcu_regime_", str(option), number)
        characters = read("characters")
        self.assertEqual(["FCU_ud_directorate_office", "FCU_ud_unity_office"],
                         re.findall(r"(?m)^\t(\w+) = \{", characters))
        self.assertIn("FCU_robert_sinclair = {", (MOD / "common/characters/ac_starting_governments.txt").read_text(encoding="utf-8-sig"))

    def test_fiscal_guards_banned_effects_and_canon_limits(self):
        nodes = ucw.load(FILES["focus"]) + ucw.load(FILES["effects"]) + ucw.load(FILES["events"])

        def walk(items, guarded):
            for key, _, value in items:
                if key.startswith("ac_econ_") and key != "ac_econ_ready":
                    self.assertTrue(guarded, key)
                if isinstance(value, list):
                    inner = guarded
                    if key == "if":
                        limit = ucw.mapping(value).get("limit", [])
                        inner = guarded or any(k == "ac_econ_ready" and v == "yes" for k, _, v in limit)
                    walk(value, inner)
        walk(nodes, False)
        text = script_text()
        self.assertEqual([], seams.banned_uses(text))
        self.assertNotRegex(text, r"set_global_flag\s*=")
        self.assertNotRegex(text, r"ac_ucw_grievance|ac_ucw_country_start")
        self.assertNotRegex(text, r"(?m)^\s*\d{1,4}\s*=\s*\{|\bstate\s*=\s*\d")
        self.assertNotRegex(text, r"every_country|random_country|add_core|set_capital|create_country_leader")
        own = loc_keys(LOC)
        for key, value in own.items():
            for sentence in re.split(r"(?<=[.;])\s+", value.replace("\\n", " ")):
                for weapon, allowed in (("Stonehenge", {"1998", "2003", "2005"}), ("Megalith", {"2005"})):
                    if weapon in sentence:
                        years = set(re.findall(r"\b(19\d\d|20\d\d)\b", sentence)) - {"1996", "1999", "1997", "1995"}
                        self.assertLessEqual(years, allowed, (key, sentence))

    def test_ai_default_path_still_starts_the_war_in_summer_2003(self):
        world = DepthWorld("1991.1.1")
        started = world.ai_path("2003.7.31")
        fcu = world.countries["FCU"]
        self.assertIsNotNone(started, "The AI default path must still start the Continental War")
        self.assertGreaterEqual(started, ucw.day("2003.6.21"))
        self.assertLess(started, ucw.day("2003.7.1"))
        self.assertEqual([], world.politics, "The AI never changes Central Usea's government")
        baseline = ucw.started()
        baseline.today = ucw.day("1999.12.8")
        baseline.weeks((world.today - baseline.today) // 7)
        self.assertIn("ac_ucw_war_started", baseline.globals)
        self.assertEqual(baseline.countries["ERU"].variables["ac_ucw_grievance"], world.countries["ERU"].variables["ac_ucw_grievance"],
                         "This package must not move Erusea's grievance")
        self.assertGreater(world.countries["ERU"].variables["ac_ucw_grievance"], 24)
        self.assertIn("FCU_ud_hold_course", fcu.focuses)
        self.assertIn("FCU_ud_carryover_done", fcu.flags)
        self.assertTrue({"FCU_ud_impact_prepared", "FCU_ud_impact_strained", "FCU_ud_impact_overwhelmed"} & set(fcu.flags))
        self.assertEqual(set(), {f for f in fcu.focuses if f.startswith("FCU_ud_") and world.weight(f) == 0})
        self.assertGreater(len([f for f in fcu.focuses if f in world.mine and world.focuses[f] and f in
                                {x.id for x in C.FOCUSES if x.tree == C.OPENING}]), 40)
        for flag in ucw.CONTRACT_SET:
            if flag not in ("ac_ucw_calendar_started", "ac_ucw_war_started"):
                self.assertNotIn(flag, world.globals, flag)

    def test_player_regime_paths_change_government_once_and_restore(self):
        world = DepthWorld("1996.5.1")
        fcu = world.countries["FCU"]
        fcu.ai = False
        for step in ("federal_question", "emergency_powers", "emergency_statute", "command_liaison", "civil_military_board",
                     "emergency_threshold", "proclaim_directorate"):
            world.complete("FCU_ud_" + step, "FCU")
        self.assertEqual("neutrality", world.politics[0][2]["ruling_party"])
        self.assertIn("FCU_ud_directorate_office", world.characters["FCU"])
        self.assertFalse(world.focus_available("FCU_ud_unity_talks", "FCU"))
        world.today = ucw.day("1998.7.1")
        fcu.flags["ac_ur_coup_started"] = None
        for step in ("civil_compact", "emergency_information_board", "district_councils", "directorate_amnesty",
                     "directorate_review", "return_authority"):
            world.complete("FCU_ud_" + step, "FCU")
        self.assertEqual("democratic", [p for p in world.politics if p[1] == "set_politics"][-1][2]["ruling_party"])
        self.assertNotIn("FCU_ud_gov_directorate", fcu.flags)
        self.assertFalse(world.focus_available("FCU_ud_extend_directorate", "FCU"))
        world = DepthWorld("1992.1.1")
        for step in ("federal_question", "unity_talks", "cross_bench_compact", "coalition_arithmetic", "regional_ministers",
                     "form_unity_government"):
            world.complete("FCU_ud_" + step, "FCU")
        self.assertEqual(1, sum(p[1] == "set_politics" for p in world.politics))
        self.assertIn("FCU_ud_unity_office", world.characters["FCU"])
        self.assertFalse(world.focus_available("FCU_ud_emergency_threshold", "FCU"))

    def test_impact_tally_and_carryover_run_once(self):
        for readiness, flag in ((70, "FCU_ud_impact_prepared"), (40, "FCU_ud_impact_strained"), (5, "FCU_ud_impact_overwhelmed")):
            world = DepthWorld("1999.7.10")
            fcu = world.countries["FCU"]
            fcu.variables["FCU_ud_readiness"] = readiness
            world.execute([("ac_ud_fcu_weekly", "=", "yes")], fcu)
            world.execute([("ac_ud_fcu_weekly", "=", "yes")], fcu)
            self.assertIn(flag, fcu.flags)
            self.assertEqual(1, [i[2] for i in world.queue].count("ac_ud_fcu.26"))
        late = DepthWorld("2001.3.1")
        late.globals.add("ac_ucw_calendar_started")
        late.execute([("ac_ud_fcu_weekly", "=", "yes")], late.countries["FCU"])
        self.assertIn("FCU_ud_impact_tallied", late.countries["FCU"].flags)
        self.assertNotIn("ac_ud_fcu.26", [i[2] for i in late.queue])
        world = ucw.started()
        depth = DepthWorld("1999.12.8")
        depth.globals, depth.countries = world.globals, world.countries
        fcu = depth.countries["FCU"]
        fcu.flags["FCU_ud_relief_lane_corps"] = None
        fcu.ideas["FCU_ud_relief_corps_idea"] = None
        fcu.variables["FCU_ud_readiness"] = 80
        recovery = fcu.variables["ac_ucw_recovery"]
        for _ in range(2):
            depth.execute([("ac_ud_fcu_weekly", "=", "yes")], fcu)
        self.assertEqual(recovery + 3, fcu.variables["ac_ucw_recovery"])
        self.assertIn("FCU_ud_relief_work_continues_idea", fcu.ideas)
        self.assertNotIn("FCU_ud_relief_corps_idea", fcu.ideas)
        self.assertEqual(1, [i[2] for i in depth.queue].count("ac_ud_fcu.30"))

    def test_generators_check_cleanly(self):
        commands = [
            [sys.executable, "-B", str(HERE / "build.py"), "--check"],
            [sys.executable, "-B", str(HERE / "build_art.py"), "--check"],
            [sys.executable, "-B", str(ROOT / "tools/usea_expansion/build_content.py"), "--check"],
            [sys.executable, "-B", str(ROOT / "tools/build_continental_war.py"), "--check"],
        ]
        for command in commands:
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, " ".join(command[-2:]) + "\n" + result.stdout[-2000:] + result.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
