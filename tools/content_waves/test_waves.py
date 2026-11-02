"""Source, artwork and actual-script offline regressions for content waves A and D.

The runtime half executes the generated scripted effects with the real P1
political and fiscal owners (tools/Test-SharedSystems.py). The adapter only
supplies dates, focus completion, scope switching and engine observations.
Decimal execution and deepcopy reloads are offline evidence, not native saves.
"""
import copy
from datetime import date
from decimal import Decimal as D
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / "mod/2985041246"
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools/usea_expansion")]
spec = importlib.util.spec_from_file_location("content_waves_shared", ROOT / "tools/Test-SharedSystems.py")
shared = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = shared
spec.loader.exec_module(shared)
parse, fields = shared.parse, shared.fields

from content_waves.framework import focus_id, branch_id, service_id  # noqa: E402
from content_waves import free_erusea, nordennavic  # noqa: E402
from event_picture_fit import audit as picture_audit  # noqa: E402

FE, NC = free_erusea.WAVE, nordennavic.WAVE
NAMES = {"ac_fe": "free_erusea", "ac_nec": "nordennavic"}
WAVES = ((FE, "free_erusea"), (NC, "nordennavic"))
OWNED_FILES = [f"{folder}/ac_{name}.txt" for name in NAMES.values() for folder in (
    "common/national_focus", "common/scripted_effects", "common/scripted_triggers", "common/ideas",
    "common/decisions", "common/decisions/categories", "common/on_actions", "common/custom_localization", "events")]


def text(relative):
    return (MOD / relative).read_text(encoding="utf-8-sig")


def localization():
    keys = {}
    for path in (MOD / "localisation/english").glob("*.yml"):
        for match in re.finditer(r'^ ([^\s:#]+):\d* "(.*)"$', path.read_text(encoding="utf-8-sig"), re.M):
            keys.setdefault(match[1], []).append(path.name)
    return keys


class Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loc = localization()
        cls.manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
        cls.assets = {row["sprite"]: row for row in json.loads((HERE / "assets.json").read_text(encoding="utf-8"))["assets"]}

    def test_generators_and_continental_war_import_block_are_consistent(self):
        for script in ("build.py", "build_art.py"):
            result = subprocess.run([sys.executable, "-B", str(HERE / script), "--check"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        cw = importlib.util.spec_from_file_location("cw_preserve", ROOT / "tools/build_continental_war.py")
        module = importlib.util.module_from_spec(cw)
        cw.loader.exec_module(module)
        for tag in ("ERU", "FCU"):
            preserved = module.preserved_imports(tag)
            ids = [focus_id(FE, b, i) for b in FE.branches if b.tag == tag for i in range(6)]
            self.assertEqual("# BEGIN OVERSIGHT YEARS IMPORTS\n" + "".join(f"shared_focus = {i}\n" for i in ids) + "# END OVERSIGHT YEARS IMPORTS\n", preserved)

    def test_approved_budgets_and_globally_unique_ids(self):
        self.assertEqual({"ERU": 36, "FCU": 24, "NEC": 42}, self.manifest["counts"])
        self.assertEqual(102, self.manifest["total"])
        defined = []
        for path in (MOD / "common/national_focus").glob("*.txt"):
            defined += re.findall(r"^\s*id\s*=\s*(\w+)", path.read_text(encoding="utf-8-sig"), re.M)
        ours = {row["id"] for row in self.manifest["focuses"]}
        for ident in ours:
            self.assertEqual(1, defined.count(ident), ident)
        tree = parse(text("common/national_focus/NEC.txt"))
        imports = [v for k, _, v in fields(tree)["focus_tree"] if k == "shared_focus"]
        self.assertEqual(sorted(r["id"] for r in self.manifest["focuses"] if r["tag"] == "NEC"), sorted(imports))

    def test_every_focus_is_localized_iconed_and_has_a_real_consumer(self):
        for row in self.manifest["focuses"]:
            ident = row["id"]
            with self.subTest(focus=ident):
                self.assertIn(ident, self.loc)
                self.assertGreaterEqual(len(self.loc.get(ident + "_desc", [""])), 1)
                sprite = self.assets["GFX_" + ("ac_fe" if row["wave"] == "A" else "ac_nec") + "_focus_" + ident]
                self.assertEqual((96, 96), (sprite["width"], sprite["height"]))
        for wave, name in WAVES:
            effects = text(f"common/scripted_effects/ac_{name}.txt")
            for b in wave.branches:
                for i in (1, 2):
                    self.assertIn(f"add_ideas = {focus_id(wave, b, i)}_spirit", effects)
                stem = focus_id(wave, b, 0)[:-len("_register")]
                self.assertIn(f"has_country_flag = {stem}_service_completed", text(f"common/national_focus/ac_{name}.txt"))

    def test_exclusive_policies_are_symmetric(self):
        for wave, name in WAVES:
            focuses = {fields(v)["id"]: v for k, _, v in parse(text(f"common/national_focus/ac_{name}.txt")) if k == "shared_focus"}
            for b in wave.branches:
                a, c = focus_id(wave, b, 1), focus_id(wave, b, 2)
                self.assertEqual(c, fields(fields(focuses[a])["mutually_exclusive"])["focus"])
                self.assertEqual(a, fields(fields(focuses[c])["mutually_exclusive"])["focus"])

    def test_localization_keys_resolve_once_and_files_have_bom(self):
        for name in NAMES.values():
            raw = (MOD / f"localisation/english/ac_{name}_l_english.yml").read_bytes()
            self.assertTrue(raw.startswith(b"\xef\xbb\xbfl_english:\n"))
        duplicates = {k: v for k, v in self.loc.items() if len(v) > 1 and any(n.startswith("ac_free_erusea") or n.startswith("ac_nordennavic") for n in v)}
        self.assertEqual({}, duplicates)
        for relative in OWNED_FILES:
            if "custom_localization" in relative:
                continue
            source = text(relative)
            for key in re.findall(r"\b(?:title|desc|name)\s*=\s*([\w.]+)", source):
                if key.startswith(("ac_fe", "ac_nec")):
                    self.assertTrue(key in self.loc, relative + ": " + key)

    def test_every_called_owned_effect_and_trigger_is_defined(self):
        defined = set()
        for folder in ("scripted_effects", "scripted_triggers"):
            for path in (MOD / "common" / folder).glob("*.txt"):
                defined |= set(re.findall(r"^(\w+)\s*=\s*\{", path.read_text(encoding="utf-8-sig"), re.M))
        for relative in OWNED_FILES:
            for call in re.findall(r"\b((?:ac_fe|ac_nec|ERU_fe|FCU_fe|NEC_nc)_\w+|ac_econ_\w+|ac_macro_\w+|ac_pol_\w+) = yes", text(relative)):
                self.assertTrue(call in defined, relative + ": " + call)

    def test_artwork_bindings_exist_and_event_pictures_fit_native_apertures(self):
        gfx = (MOD / "interface/ac_content_waves.gfx").read_text(encoding="utf-8")
        sprites = dict(re.findall(r'name = "(\w+)" texturefile = "([^"]+)"', gfx))
        for relative in OWNED_FILES:
            source = text(relative)
            for sprite in re.findall(r"\b(GFX_(?:ac_fe|ac_nec)_\w+)", source):
                self.assertIn(sprite, sprites, sprite)
            for ident in re.findall(r"^\t\t(\w+) = \{\n\t\t\tpicture = (\w+)", source, re.M):
                self.assertIn("GFX_idea_" + ident[1], sprites)
            for icon in re.findall(r"\bicon = ((?:ac_fe|ac_nec)_\w+)", source):
                self.assertIn("GFX_decision_" + icon, sprites)
        for sprite, relative in sprites.items():
            if sprite.endswith("_shine"):
                continue
            with Image.open(MOD / relative) as image:
                row = self.assets[sprite]
                self.assertEqual((row["width"], row["height"]), image.size)
                if row["role"] == "decision row":
                    self.assertEqual((26, 29), image.size)
        report = picture_audit.audit(["events/ac_free_erusea.txt", "events/ac_nordennavic.txt"])
        # Wave A: 2 openings, 10 scenes, 10 finals, 2 national finals and owner events .2/.4.
        # Wave D: 1 opening, 7 scenes, 7 finals and 1 national final. Two owner news events.
        self.assertEqual({"country_event": 26 + 16, "news_event": 2}, report["counts"])
        for row in report["consumers"]:
            self.assertLessEqual(row["bounds"][2], 215 if row["event_type"] == "country_event" else 456)
            self.assertLessEqual(row["bounds"][3], 181 if row["event_type"] == "country_event" else 244)

    def test_no_forbidden_world_changes_and_honest_chronology(self):
        combined = "\n".join(text(r) for r in OWNED_FILES)
        for forbidden in ("transfer_state", "add_state_core", "remove_state_core", "start_civil_war", "create_country", "annex_country",
                          "set_cosmetic_tag", "add_to_faction", "create_faction", "declare_war_on", "white_peace", "create_wargoal",
                          "add_manpower", "create_unit", "add_equipment_to_stockpile", "set_politics", "create_country_leader"):
            self.assertNotIn(forbidden, combined, forbidden)
        effects = text("common/scripted_effects/ac_free_erusea.txt")
        self.assertIn("date > 2006.9.25", effects)
        self.assertIn("date < 2007.9.26", effects)
        self.assertIn("ac_fe_late_start_skipped", effects)
        loc = (MOD / "localisation/english/ac_free_erusea_l_english.yml").read_text(encoding="utf-8-sig")
        self.assertIn("ACES Chronicle (2006 / 09.26)", loc)
        self.assertIn("no end date is claimed", loc)


class World(shared.World):
    PREFIXES = ("ac_fe_", "ac_nec_", "ERU_fe_", "FCU_fe_", "NEC_nc_")

    def __init__(self, mode="full"):
        super().__init__(mode)
        self.wave_actions = {}
        self.focuses = {}
        self.messages = {}
        for name in NAMES.values():
            for folder, library in (("scripted_effects", self.effects), ("scripted_triggers", self.triggers)):
                for key, _, value in parse(text(f"common/{folder}/ac_{name}.txt")):
                    if key in library:
                        raise ValueError("Conflicting owner " + key)
                    library[key] = value
            self.wave_actions[name] = fields(parse(text(f"common/on_actions/ac_{name}.txt")))["on_actions"]
            self.focuses.update({fields(v)["id"]: v for k, _, v in parse(text(f"common/national_focus/ac_{name}.txt")) if k == "shared_focus"})
            self.messages.update({next(x for key, _, x in v if key == "id"): v for k, _, v in parse(text(f"events/ac_{name}.txt")) if k in ("country_event", "news_event")})
        for c in self.countries.values():
            c.completed = set()
            c.timed_ideas = {}
            c.stability = D("0.6")
            c.trees = set()

    def number(self, value, context, temp, root, previous):
        if value.startswith(self.PREFIXES):
            return temp.get(value, context.variables.get(value, D(0)))
        return super().number(value, context, temp, root, previous)

    def trigger(self, nodes, context, temp=None, root=None, previous=None):
        results = []
        for key, op, value in nodes:
            if key == "has_completed_focus":
                answer = value in context.completed
            elif key == "country_exists":
                answer = value in self.countries and any(s.owner == value for s in self.states.values())
            elif key == "has_stability":
                answer = {"<": context.stability < D(value), ">": context.stability > D(value)}[op]
            elif key == "has_war_with":
                answer = False
            elif key == "has_focus_tree":
                answer = value in context.trees
            elif key in self.countries:
                answer = self.trigger(value, self.countries[key], temp, root, context)
            else:
                answer = super().trigger([(key, op, value)], context, temp, root, previous)
            results.append(answer)
        return all(results)

    def execute(self, nodes, context, temp=None, root=None, previous=None):
        temp = {} if temp is None else temp
        root = context if root is None else root
        branch = None
        for key, op, value in nodes:
            if key in ("if", "else_if", "else"):
                if key == "if":
                    branch = False
                elif branch is None:
                    raise ValueError("Orphan branch")
                condition = key == "else" or self.trigger(next(v for k, _, v in value if k == "limit"), context, temp, root, previous)
                if not branch and condition:
                    self.execute([r for r in value if r[0] != "limit"], context, temp, root, previous)
                    branch = True
                continue
            branch = None
            name = value[0][0] if isinstance(value, list) and value and isinstance(value[0], tuple) else None
            if key in ("set_variable", "add_to_variable", "subtract_from_variable", "set_temp_variable", "add_to_temp_variable",
                       "subtract_from_temp_variable") and name and name.startswith(self.PREFIXES):
                _, _, operand = value[0]
                amount = self.number(operand, context, temp, root, previous)
                target = temp if "temp_variable" in key else context.variables
                before = target.get(name, D(0))
                target[name] = amount if key.startswith("set_") else before + amount if key.startswith("add_") else before - amount
            elif key == "add_timed_idea":
                data = fields(value)
                context.ideas.add(data["idea"])
                context.timed_ideas[data["idea"]] = self.today + int(data["days"])
            elif key == "remove_ideas":
                context.ideas.discard(value)
                context.timed_ideas.pop(value, None)
            elif key in ("country_event", "news_event"):
                data = fields(value)
                self.events.append((context.tag, data["id"], self.today + int(data.get("days", 0))))
            elif key == "load_focus_tree":
                context.trees.add(fields(value)["tree"])
            elif key in self.countries or key in ("FROM", "ROOT"):
                target = previous if key == "FROM" else root if key == "ROOT" else self.countries[key]
                self.execute(value, target, temp, root, context)
            else:
                super().execute([(key, op, value)], context, temp, root, previous)

    def advance(self, days):
        self.today += days
        for c in self.countries.values():
            for ident, expiry in list(c.timed_ideas.items()):
                if expiry <= self.today:
                    c.ideas.discard(ident)
                    c.timed_ideas.pop(ident)

    def wave_action(self, name, action, tag=None, other=None):
        node = fields(fields(self.wave_actions[name])[action])["effect"]
        self.execute(node, self.countries.get(tag), root=self.countries.get(tag), previous=self.countries.get(other))

    def complete(self, ident, tag):
        c = self.countries[tag]
        node = self.focuses[ident]
        if not self.trigger(fields(node)["available"], c):
            raise AssertionError("Unavailable focus " + ident)
        self.execute(fields(node)["completion_reward"], c)
        c.completed.add(ident)

    def available(self, ident, tag):
        return self.trigger(fields(self.focuses[ident])["available"], self.countries[tag])

    def option(self, event, letter, tag):
        node = self.messages[event]
        option = next(v for k, _, v in node if k == "option" and next(x for key, _, x in v if key == "name") == f"{event}.{letter}")
        self.execute([r for r in option if r[0] not in ("name", "ai_chance")], self.countries[tag])


def world(mode="full", today=date(2006, 10, 1)):
    w = World(mode).initialize_both()
    w.today = today.toordinal()
    for name in NAMES.values():
        w.wave_action(name, "on_startup")
    for tag in ("ERU", "FCU", "NEC"):
        c = w.countries[tag]
        c.variables["ac_pol_capacity"] = D(40)
        if mode == "experimental":
            c.flags["ac_econ_initialized"] = None
            c.variables.update(ac_econ_treasury=D(100), ac_econ_arrears=D(0))
    return w


class Runtime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baselines = {mode: world(mode) for mode in ("full", "experimental", "disabled")}

    def fresh(self, mode="full"):
        return copy.deepcopy(self.baselines[mode])

    def test_every_service_pays_real_owners_once_and_completes_after_ninety_days(self):
        for wave in (FE, NC):
            for b in wave.branches:
                for n in range(2):
                    for mode in ("full", "experimental", "disabled"):
                        with self.subTest(branch=branch_id(b), service=n, mode=mode):
                            w = self.fresh(mode)
                            c = w.countries[b.tag]
                            c.completed.add(focus_id(wave, b, 0 if n == 0 else 3))
                            ident = service_id(wave, b, n)
                            before = copy.deepcopy(c)
                            w.run(ident + "_start", b.tag)
                            self.assertEqual(before.pp - 35, c.pp)
                            self.assertEqual(36, c.variables["ac_pol_capacity"])
                            if mode == "full":
                                self.assertEqual(before.variables["ac_macro_cash"] - D(".002"), c.variables["ac_macro_cash"])
                            elif mode == "experimental":
                                self.assertEqual(before.variables["ac_econ_treasury"] - 2, c.variables["ac_econ_treasury"])
                            self.assertIn(ident + "_spirit", c.ideas)
                            snapshot = copy.deepcopy(c)
                            w.run(ident + "_start", b.tag)
                            self.assertEqual(snapshot, c)
                            w.advance(89)
                            w.run(ident + "_finish", b.tag)
                            self.assertNotIn(ident + "_completed", c.flags)
                            w.advance(1)
                            w.run(ident + "_finish", b.tag)
                            self.assertIn(ident + "_completed", c.flags)
                            self.assertIn(focus_id(wave, b, 0)[:-len("_register")] + "_service_completed", c.flags)
                            self.assertNotIn(ident + "_spirit", c.ideas)

    def test_shortfalls_never_authorize_a_service(self):
        b = NC.branches[0]
        for reason in ("pp", "capacity", "war", "not_unlocked"):
            w = self.fresh()
            c = w.countries["NEC"]
            c.completed.add(focus_id(NC, b, 0))
            if reason == "pp":
                c.pp = D(34)
            elif reason == "capacity":
                c.variables["ac_pol_capacity"] = D(3)
            elif reason == "war":
                c.war = True
            else:
                c.completed.clear()
            before = copy.deepcopy(c)
            w.run(service_id(NC, b, 0) + "_start", "NEC")
            self.assertEqual(before, c, reason)

    def prepare(self, wave, b):
        w = self.fresh()
        w.globals |= set(re.findall(r"(?<!NOT = \{ )has_global_flag = (\w+)", b.gate))
        if b.gate.startswith("has_global_flag = ac_ucw_outcome_isaf_victory has_global_flag = ac_fe_insurrection_started"):
            w.globals.add("ac_fe_insurrection_started")
        if "2013.12.31" in b.gate:
            w.today = date(2014, 6, 1).toordinal()
        w.countries[b.tag].completed |= set(b.entry)
        return w

    def test_branch_policies_exclude_review_needs_service_and_settlement_improves(self):
        for wave in (FE, NC):
            for b in wave.branches:
                for choice in (1, 2):
                    with self.subTest(branch=branch_id(b), choice=choice):
                        w = self.prepare(wave, b)
                        c = w.countries[b.tag]
                        w.complete(focus_id(wave, b, 0), b.tag)
                        w.complete(focus_id(wave, b, choice), b.tag)
                        self.assertFalse(w.available(focus_id(wave, b, 3 - choice), b.tag))
                        w.complete(focus_id(wave, b, 3), b.tag)
                        self.assertFalse(w.available(focus_id(wave, b, 4), b.tag))
                        ident = service_id(wave, b, 1)
                        w.run(ident + "_start", b.tag)
                        w.advance(90)
                        w.run(ident + "_finish", b.tag)
                        w.complete(focus_id(wave, b, 4), b.tag)
                        w.complete(focus_id(wave, b, 5), b.tag)
                        policy = focus_id(wave, b, choice) + "_spirit"
                        self.assertNotIn(policy, c.ideas)
                        self.assertIn(policy + "_settled", c.ideas)
                        snapshot = copy.deepcopy(c)
                        w.run(focus_id(wave, b, 5) + "_apply", b.tag)
                        self.assertEqual(snapshot, c)

    def test_nordennavic_stages_wait_for_dates_and_earlier_settlements(self):
        late = {k: focus_id(NC, next(b for b in NC.branches if b.key == k), 0) for k in nordennavic.STAGE_2 + nordennavic.STAGE_3}
        w = self.fresh()
        w.today = date(2005, 6, 1).toordinal()
        c = w.countries["NEC"]
        c.completed.add("NEC_nc_harbours_settlement")
        self.assertFalse(w.available(late["technical_reserve"], "NEC"))
        w.today = date(2006, 1, 1).toordinal()
        self.assertTrue(w.available(late["technical_reserve"], "NEC"))
        self.assertFalse(w.available(late["neutral_waters"], "NEC"))
        c.completed.add("NEC_nc_northern_routes_settlement")
        self.assertFalse(w.available(late["neutral_waters"], "NEC"))
        w.today = date(2014, 1, 1).toordinal()
        self.assertTrue(w.available(late["neutral_waters"], "NEC"))

    def test_erusea_routes_follow_the_actual_continental_war_outcome(self):
        routes = {"ac_ucw_outcome_isaf_victory": {"oversight", "return"}, "ac_ucw_outcome_erusean_victory": {"victor", "return"},
                  "ac_ucw_outcome_stalemate": {"armistice", "return"}, "ac_ucw_war_averted": {"ordinary", "return"}}
        for flag, expected in routes.items():
            with self.subTest(route=flag):
                w = self.fresh()
                w.globals.add(flag)
                c = w.countries["ERU"]
                c.completed |= {b.entry[0] for b in FE.branches if b.tag == "ERU"}
                open_ = {b.key for b in FE.branches if b.tag == "ERU" and w.available(focus_id(FE, b, 0), "ERU")}
                self.assertEqual(expected, open_)
                f = w.countries["FCU"]
                f.completed.add("FCU_ucw_exp_settlement_assessment")
                open_fcu = {b.key for b in FE.branches if b.tag == "FCU" and w.available(focus_id(FE, b, 0), "FCU")}
                self.assertEqual({"oversight", "partners"} if "isaf" in flag else {"drawdown", "partners"}, open_fcu)

    def test_openings_describe_the_actual_route_not_an_assumed_victory(self):
        custom = parse(text("common/custom_localization/ac_free_erusea.txt"))
        loc = dict(re.findall(r'^ ([^\s:#]+):0 "(.*)"$', (MOD / "localisation/english/ac_free_erusea_l_english.yml").read_text(encoding="utf-8-sig"), re.M))
        for tag in ("ERU", "FCU"):
            node = next(v for k, _, v in custom if k == "defined_text" and next(x for key, _, x in v if key == "name") == f"{tag}_fe_route_context")
            for flag in ("ac_ucw_outcome_isaf_victory", "ac_ucw_outcome_erusean_victory", "ac_ucw_outcome_stalemate", "ac_ucw_war_averted", None):
                with self.subTest(tag=tag, route=flag):
                    w = self.fresh()
                    if flag:
                        w.globals.add(flag)
                    chosen = next(fields(v)["localization_key"] for k, _, v in node
                                  if k == "text" and w.trigger(fields(v).get("trigger", []), w.countries[tag]))
                    value = loc[chosen]
                    self.assertEqual(flag == "ac_ucw_outcome_isaf_victory", "oversight" in value, value)
            opening = loc[f"ac_fe.{10 + list(FE.countries).index(tag)}.d"]
            self.assertIn(f"[{tag}_fe_route_context]", opening)
            self.assertNotIn("surrender", opening)

    def owner(self, today=date(2006, 9, 26)):
        w = self.fresh()
        w.globals.add("ac_ucw_outcome_isaf_victory")
        w.today = today.toordinal()
        return w, w.countries["ERU"]

    def test_insurrection_starts_on_the_anchor_only_after_an_isaf_victory(self):
        w, c = self.owner(date(2006, 9, 25))
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w.globals)
        w.today = date(2006, 9, 26).toordinal()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertIn("ac_fe_insurrection_started", w.globals)
        self.assertEqual(D(55) + D("0.4"), c.variables["ac_fe_pressure"])
        self.assertIn("ac_fe_pressure_active", c.ideas)
        self.assertIn(("ERU", "ac_fe.1", w.today + 1), w.events)
        w2 = self.fresh()
        w2.today = date(2006, 10, 1).toordinal()
        w2.globals.add("ac_ucw_outcome_stalemate")
        w2.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w2.globals)

    def test_late_first_observation_never_replays_the_outbreak(self):
        w, c = self.owner(date(2008, 3, 1))
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w.globals)
        self.assertIn("ac_fe_insurrection_closed", w.globals)
        self.assertIn("ac_fe_late_start_skipped", w.globals)
        self.assertNotIn("ac_fe_pressure", c.variables)

    def test_policies_and_services_contain_the_insurrection_state_based(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        start = c.variables["ac_fe_pressure"]
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(start + D("0.4"), c.variables["ac_fe_pressure"])
        c.ideas.add("ERU_fe_insurrection_policy_b_spirit")
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(start + D("0.4") - D("0.5"), c.variables["ac_fe_pressure"])
        f = w.countries["FCU"]
        f.completed.add("FCU_fe_security_operations")
        ident = service_id(FE, next(b for b in FE.branches if b.tag == "FCU" and b.key == "security"), 1)
        w.run(ident + "_start", "FCU")
        w.advance(90)
        before = c.variables["ac_fe_pressure"]
        w.run(ident + "_finish", "FCU")
        self.assertEqual(before - 6, c.variables["ac_fe_pressure"])
        c.variables["ac_fe_pressure"] = D("5.3")
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertIn("ac_fe_insurrection_contained", w.globals)
        self.assertFalse(any(i.startswith("ac_fe_pressure_") for i in c.ideas))
        frozen = c.variables["ac_fe_pressure"]
        w.run("ac_fe_relief_major", "ERU")
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(frozen, c.variables["ac_fe_pressure"])

    def test_crisis_review_fires_once_per_year_and_options_have_bounded_effects(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        c.variables["ac_fe_pressure"] = D(90)
        c.stability = D("0.2")
        w.events.clear()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(["ac_fe.2"], [e for _, e, _ in w.events])
        self.assertIn("ac_fe_pressure_severe", c.ideas)
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(["ac_fe.2"], [e for _, e, _ in w.events])
        w.option("ac_fe.2", "a", "ERU")
        self.assertIn(("FCU", "ac_fe.4"), [(t, e) for t, e, _ in w.events])
        f = w.countries["FCU"]
        pp = f.pp
        before = c.variables["ac_fe_pressure"]
        w.option("ac_fe.4", "a", "FCU")
        self.assertEqual(pp - 40, f.pp)
        self.assertIn("ac_fe_partner_assistance", c.ideas)
        self.assertEqual(before - 6, c.variables["ac_fe_pressure"])

    def test_annexation_closes_the_owner_without_touching_other_state(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        w.wave_action("free_erusea", "on_annex", "FCU", "ERU")
        self.assertIn("ac_fe_insurrection_closed", w.globals)
        self.assertFalse(any(i.startswith("ac_fe_pressure_") for i in c.ideas))

    def test_nordennavic_adoption_and_anean_callback_read_only(self):
        w = self.fresh()
        c = w.countries["NEC"]
        decision = fields(fields(parse(text("common/decisions/ac_nordennavic.txt")))["ac_nec_nec_services"])["NEC_nc_adopt_campaign"]
        w.execute(fields(decision)["complete_effect"], c)
        self.assertIn(nordennavic.TREE_ID, c.trees)
        custom = parse(text("common/custom_localization/ac_nordennavic.txt"))
        node = next(v for k, _, v in custom if k == "defined_text" and next(x for key, _, x in v if key == "name") == "NEC_nc_anean_record")
        def pick():
            for key, _, value in node:
                if key == "text" and w.trigger(fields(value).get("trigger", []), c):
                    return fields(value)["localization_key"]
        self.assertEqual("NEC_nc_anean_none", pick())
        w.globals.add("ac_anea_nec_participates")
        self.assertEqual("NEC_nc_anean_participates", pick())


if __name__ == "__main__":
    unittest.main(verbosity=2)
