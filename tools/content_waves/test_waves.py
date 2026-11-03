"""Source, artwork and actual-script offline regressions for every content wave.

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
from content_waves import aurelia, circum_pacific, estovakia, free_erusea, nordennavic  # noqa: E402
from content_waves.registry import MODULES  # noqa: E402
from event_picture_fit import audit as picture_audit  # noqa: E402

FE, NC, EB, AU, CP = free_erusea.WAVE, nordennavic.WAVE, estovakia.WAVE, aurelia.WAVE, circum_pacific.WAVE
NAMES = {m.WAVE.prefix: m.NAME for m in MODULES}
WAVES = tuple((m.WAVE, m.NAME) for m in MODULES)
PREFIX_BY_KEY = {m.KEY: m.WAVE.prefix for m in MODULES}
STEMS = tuple(f"{tag}_{m.WAVE.infix}" for m in MODULES for tag in (*m.WAVE.countries, *m.WAVE.extra_tags))
OWNED_RE = "|".join(sorted(NAMES) + sorted(STEMS))
OWNED_FILES = [f"{folder}/ac_{name}.txt" for name in NAMES.values() for folder in (
    "common/national_focus", "common/scripted_effects", "common/scripted_triggers", "common/ideas", "common/ai_strategy",
    "common/decisions", "common/decisions/categories", "common/on_actions", "common/custom_localization", "events")
    if (MOD / f"{folder}/ac_{name}.txt").exists()]
EXPECTED = {"ERU": 36, "FCU": 24, "NEC": 42, "EVA": 30, "EMM": 18, "AUR": 54}
STORY_FLAGS = ("ac_cpw_started", "ac_cpw_tainted", "ac_cpw_prevented", "ac_cpw_declaration_withheld")


def text(relative):
    return (MOD / relative).read_text(encoding="utf-8-sig")


def localization():
    keys = {}
    for path in (MOD / "localisation/english").glob("*.yml"):
        for match in re.finditer(r'^ ([^\s:#]+):\d* "(.*)"$', path.read_text(encoding="utf-8-sig"), re.M):
            keys.setdefault(match[1], []).append(path.name)
    return keys


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loc = localization()
        cls.manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
        cls.assets = {row["sprite"]: row for row in json.loads((HERE / "assets.json").read_text(encoding="utf-8"))["assets"]}

    def test_generators_and_foreign_tree_import_blocks_are_consistent(self):
        for script in ("build.py", "build_art.py"):
            result = subprocess.run([sys.executable, "-B", str(HERE / script), "--check"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        sys.path.insert(0, str(ROOT / "tools/anea"))
        owners = {"ERU": load_module("cw_preserve", ROOT / "tools/build_continental_war.py"),
                  "EVA": load_module("anea_preserve", ROOT / "tools/anea/build_campaign.py")}
        owners["FCU"], owners["EMM"] = owners["ERU"], owners["EVA"]
        for module in MODULES:
            for tag, name in getattr(module, "IMPORTS", {}).items():
                with self.subTest(tag=tag):
                    ids = [focus_id(module.WAVE, b, i) for b in module.WAVE.branches if b.tag == tag for i in range(6)]
                    expected = f"# BEGIN {name} IMPORTS\n" + "".join(f"shared_focus = {i}\n" for i in ids) + f"# END {name} IMPORTS\n"
                    self.assertEqual(expected, owners[tag].preserved_imports(tag))

    def test_approved_budgets_and_globally_unique_ids(self):
        self.assertEqual(EXPECTED, self.manifest["counts"])
        self.assertEqual(sum(EXPECTED.values()), self.manifest["total"])
        defined = []
        for path in (MOD / "common/national_focus").glob("*.txt"):
            defined += re.findall(r"^\s*id\s*=\s*(\w+)", path.read_text(encoding="utf-8-sig"), re.M)
        for ident in {row["id"] for row in self.manifest["focuses"]}:
            self.assertEqual(1, defined.count(ident), ident)
        for tag in ("NEC", "AUR"):
            tree = parse(text(f"common/national_focus/{tag}.txt"))
            imports = [v for k, _, v in fields(tree)["focus_tree"] if k == "shared_focus"]
            self.assertEqual(sorted(r["id"] for r in self.manifest["focuses"] if r["tag"] == tag), sorted(imports))

    def test_every_focus_is_localized_iconed_and_has_a_real_consumer(self):
        for row in self.manifest["focuses"]:
            ident = row["id"]
            with self.subTest(focus=ident):
                self.assertIn(ident, self.loc)
                self.assertIn(ident + "_desc", self.loc)
                sprite = self.assets["GFX_" + PREFIX_BY_KEY[row["wave"]] + "_focus_" + ident]
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
            if not wave.branches:
                self.assertFalse((MOD / f"common/national_focus/ac_{name}.txt").exists(), name)
                continue
            focuses = {fields(v)["id"]: v for k, _, v in parse(text(f"common/national_focus/ac_{name}.txt")) if k == "shared_focus"}
            for b in wave.branches:
                a, c = focus_id(wave, b, 1), focus_id(wave, b, 2)
                self.assertEqual(c, fields(fields(focuses[a])["mutually_exclusive"])["focus"])
                self.assertEqual(a, fields(fields(focuses[c])["mutually_exclusive"])["focus"])

    def test_localization_keys_resolve_once_and_files_have_bom(self):
        ours = tuple(f"ac_{name}" for name in NAMES.values())
        for name in NAMES.values():
            raw = (MOD / f"localisation/english/ac_{name}_l_english.yml").read_bytes()
            self.assertTrue(raw.startswith(b"\xef\xbb\xbfl_english:\n"))
        duplicates = {k: v for k, v in self.loc.items() if len(v) > 1 and any(n.startswith(ours) for n in v)}
        self.assertEqual({}, duplicates)
        for relative in OWNED_FILES:
            if "custom_localization" in relative:
                continue
            for key in re.findall(r"\b(?:title|desc|name)\s*=\s*([\w.]+)", text(relative)):
                if key.startswith(tuple(NAMES)):
                    self.assertTrue(key in self.loc, relative + ": " + key)

    def test_every_called_owned_effect_and_trigger_is_defined(self):
        defined = set()
        for folder in ("scripted_effects", "scripted_triggers"):
            for path in (MOD / "common" / folder).glob("*.txt"):
                defined |= set(re.findall(r"^(\w+)\s*=\s*\{", path.read_text(encoding="utf-8-sig"), re.M))
        pattern = re.compile(r"\b((?:" + OWNED_RE + r")_\w+|ac_econ_\w+|ac_macro_\w+|ac_pol_\w+) = yes")
        for relative in OWNED_FILES:
            for call in pattern.findall(text(relative)):
                self.assertTrue(call in defined, relative + ": " + call)

    def test_artwork_bindings_exist_and_event_pictures_fit_native_apertures(self):
        gfx = (MOD / "interface/ac_content_waves.gfx").read_text(encoding="utf-8")
        sprites = dict(re.findall(r'name = "(\w+)" texturefile = "([^"]+)"', gfx))
        prefixes = "|".join(sorted(NAMES))
        for relative in OWNED_FILES:
            source = text(relative)
            for sprite in re.findall(r"\b(GFX_(?:" + prefixes + r")_\w+)", source):
                self.assertIn(sprite, sprites, sprite)
            for ident in re.findall(r"^\t\t(\w+) = \{\n\t\t\tpicture = (\w+)", source, re.M):
                self.assertIn("GFX_idea_" + ident[1], sprites)
            for icon in re.findall(r"\bicon = ((?:" + prefixes + r")_\w+)", source):
                self.assertIn("GFX_decision_" + icon, sprites)
        for sprite, relative in sprites.items():
            if sprite.endswith("_shine"):
                continue
            with Image.open(MOD / relative) as image:
                row = self.assets[sprite]
                self.assertEqual((row["width"], row["height"]), image.size)
                if row["role"] == "decision row":
                    self.assertEqual((26, 29), image.size)
        report = picture_audit.audit([f"events/ac_{name}.txt" for name in NAMES.values()])
        # A: 24 narrative + owner .2/.4/.5; D: 16 narrative; B: 20 narrative + Emmerian aid events .5/.6;
        # Aurelia: 20 narrative; C: the Yuktobanian declaration .5 and the Osean Arkbird decision .6.
        # News: A .1/.3/.6; B .1-.4, .7-.14; C .1-.4, .7-.15 and the sixteen stages .20-.35.
        self.assertEqual({"country_event": 27 + 16 + 22 + 20 + 2, "news_event": 3 + 12 + 29}, report["counts"])
        for row in report["consumers"]:
            self.assertLessEqual(row["bounds"][2], 215 if row["event_type"] == "country_event" else 456)
            self.assertLessEqual(row["bounds"][3], 181 if row["event_type"] == "country_event" else 244)

    def test_no_forbidden_world_changes_and_honest_chronology(self):
        combined = "\n".join(text(r) for r in OWNED_FILES)
        for forbidden in ("transfer_state", "add_state_core", "remove_state_core", "start_civil_war", "create_country", "annex_country",
                          "set_cosmetic_tag", "add_to_faction", "create_faction", "white_peace", "create_wargoal", "add_wargoal",
                          "add_manpower", "create_unit", "add_equipment_to_stockpile", "set_politics", "create_country_leader",
                          "recruit_character", "add_country_leader_role", "launch_nuke", "set_owner", "set_state_controller"):
            self.assertNotIn(forbidden, combined, forbidden)
        # Only the Circum-Pacific War owner declares a war, and only the sourced one.
        self.assertNotIn("declare_war_on", "\n".join(text(r) for r in OWNED_FILES if "circum_pacific" not in r))
        self.assertEqual(["declare_war_on = { target = OSE type = topple_government }"],
                         re.findall(r"declare_war_on = \{[^}]*\}", text("common/scripted_effects/ac_circum_pacific.txt")))
        effects = text("common/scripted_effects/ac_free_erusea.txt")
        self.assertIn("date > 2006.9.25", effects)
        self.assertIn("date < 2007.9.26", effects)
        self.assertIn("ac_fe_late_start_skipped", effects)
        loc = (MOD / "localisation/english/ac_free_erusea_l_english.yml").read_text(encoding="utf-8-sig")
        self.assertIn("ACES Chronicle records that Mobius 1 defeated the insurrection on 26 September 2006 (2006 / 09.26)", loc)
        self.assertIn("defeat by Mobius 1 on 26 September 2006 (2006 / 09.26)", loc)
        self.assertIn("is provisional gameplay", loc)
        self.assertNotIn("no end date is claimed", loc)
        ecw = text("common/scripted_effects/ac_estovakia.txt")
        for anchor in ("date > 2007.4.2", "date > 2007.6.29", "date > 2008.7.14", "date > 2008.10.22", "date > 2010.2.18",
                       "date > 2011.5.8", "date > 2013.1.14", "date > 2013.10.28", "date < 2008.4.3"):
            self.assertIn(anchor, ecw)
        ecw_loc = (MOD / "localisation/english/ac_estovakia_l_english.yml").read_text(encoding="utf-8-sig")
        for citation in ("2007 / 04.03", "2007 / 06.30", "2008 / 07.15", "2008 / 10.23", "2010 / 02.19", "2011 / 05.09",
                         "2013 / 01.15", "2013 / 10.29", "2013 / 11.25", "2014 / 02.03", "2014 / 02.04"):
            self.assertIn(citation, ecw_loc)
        self.assertNotRegex(ecw, r"\b(?:set|clr)_(?:global|country)_flag = ac_anea_")
        aurelian = "\n".join(text(r) for r in OWNED_FILES if "ac_aurelia" in r) + (MOD / "localisation/english/ac_aurelia_l_english.yml").read_text(encoding="utf-8-sig")
        for name in ("Navarro", "Gleipnir", "Gandr", "Aubrey", "Archelon", "Nevera", "Griswall", "Gryphus", "exploitation"):
            self.assertNotIn(name, aurelian, name)

    def test_circum_pacific_owner_honours_the_published_consumer_contract(self):
        effects = text("common/scripted_effects/ac_circum_pacific.txt")
        triggers = text("common/scripted_triggers/ac_circum_pacific.txt")
        loc = (MOD / "localisation/english/ac_circum_pacific_l_english.yml").read_text(encoding="utf-8-sig")
        # The four flags the Pacific squadron stories already read are the only route observations.
        for flag in STORY_FLAGS:
            self.assertIn("set_global_flag = " + flag, effects, flag)
        for relative in ("tools/squadrons/chapters/OSE.json", "tools/squadrons/chapters/YUK.json"):
            story = (ROOT / relative).read_text(encoding="utf-8")
            for flag in set(re.findall(r"has_global_flag = (ac_cpw_\w+)", story)):
                self.assertIn(flag, STORY_FLAGS, relative + ": " + flag)
        # Its own calendar: the opening, the anchor, the late-save limit and every sourced stage.
        for anchor in ("date > 2010.9.21", "date > 2010.9.26", "date < 2011.9.27", "date > 2008.8.20", "date > 2010.9.22", "date > 2010.9.23",
                       "date > 2010.9.29", "date > 2010.10.3", "date > 2010.10.21", "date > 2010.10.24", "date > 2010.10.31", "date > 2010.11.1",
                       "date > 2010.11.3", "date > 2010.11.13", "date > 2010.11.28", "date > 2010.12.5", "date > 2010.12.8", "date > 2010.12.18",
                       "date > 2010.12.22", "date > 2010.12.28", "date > 2010.12.29", "date > 2010.12.30", "ac_cpw_late_start_skipped"):
            self.assertIn(anchor, effects, anchor)
        for citation in ("2008 / 08.21", "2010 / 09.23", "2010 / 09.24", "2010 / 09.27", "2010 / 09.30", "2010 / 10.04", "2010 / 10.22", "2010 / 10.25",
                         "2010 / 11.01", "2010 / 11.02", "2010 / 11.04", "2010 / 11.14", "2010 / 11.29", "2010 / 12.06", "2010 / 12.09", "2010 / 12.19",
                         "2010 / 12.23", "2010 / 12.29", "2010 / 12.30", "2010 / 12.31", "Super Weapons, Scinfaxi & Hrimfaxi", "provisional gameplay"):
            self.assertIn(citation, loc, citation)
        # No scripted peace, no assumed end date, no faction veto, pre-existing wars inspected, third parties observed.
        self.assertNotIn("white_peace", effects)
        self.assertNotIn("date > 2010.12.31", effects)
        self.assertNotIn("is_in_faction", effects + triggers)
        self.assertNotIn("has_guaranteed", effects + triggers)
        self.assertIn("ac_cpw_third_party_present", triggers)
        self.assertIn("OR = { has_war = yes OSE = { has_war = yes } }", effects)
        # Foreign owners are read, never written: the only project state touched is the sourced loss of the Arkbird.
        self.assertNotRegex(effects, r"\b(?:set|clr)_(?:global|country)_flag = ac_(?:snc|snp|sp|anea|ucw|yuk)_")
        self.assertNotRegex(effects, r"\b(?:set|add_to|subtract_from)_variable = \{ ac_(?:snc|snp|sp)_")
        self.assertEqual({"ac_sp_arkbird_joint_operations", "ac_sp_arkbird_debris_clearing"}, set(re.findall(r"remove_ideas = (ac_sp_\w+)", effects)))
        self.assertNotRegex(effects, r"add_ideas = ac_sp_")
        self.assertNotIn("ac_sp_arkbird_complete_effect", effects)
        # Named canon appears only in event text; nothing becomes a character, unit or leader.
        self.assertNotRegex("\n".join(text(r) for r in OWNED_FILES if "circum_pacific" in r), r"Harling|Nikanor|Razgriz|Wardog|Snow|Genette|Beagle")
        for name in ("Snow", "Genette", "Beagle", "Talisman"):
            self.assertNotIn(name, loc, name)


class World(shared.World):
    # Owned variables, the existing Anea recovery variable that Wave B reads and the
    # Pacific national-continuation records that the Circum-Pacific War owner reads.
    PREFIXES = tuple(p + "_" for p in NAMES) + tuple(s + "_" for s in STEMS) + ("ac_anea_", "ac_snc_", "ac_snp_")

    def __init__(self, mode="full"):
        super().__init__(mode)
        self.wave_actions = {}
        self.focuses = {}
        self.messages = {}
        self.wars = set()
        for name in NAMES.values():
            for folder, library in (("scripted_effects", self.effects), ("scripted_triggers", self.triggers)):
                for key, _, value in parse(text(f"common/{folder}/ac_{name}.txt")):
                    if key in library:
                        raise ValueError("Conflicting owner " + key)
                    library[key] = value
            self.wave_actions[name] = fields(parse(text(f"common/on_actions/ac_{name}.txt")))["on_actions"]
            if (MOD / f"common/national_focus/ac_{name}.txt").exists():
                self.focuses.update({fields(v)["id"]: v for k, _, v in parse(text(f"common/national_focus/ac_{name}.txt")) if k == "shared_focus"})
            self.messages.update({next(x for key, _, x in v if key == "id"): v for k, _, v in parse(text(f"events/ac_{name}.txt")) if k in ("country_event", "news_event")})
        # The real Osean and Yuktobanian continuation records; their programme owner is observed as active.
        for name in ("ac_snc_ose", "ac_snc_yuk"):
            for key, _, value in parse(text(f"common/scripted_triggers/{name}.txt")):
                self.triggers.setdefault(key, value)
        self.triggers.setdefault("ac_snp_active", [("always", "=", "yes")])
        for c in self.countries.values():
            c.completed = set()
            c.timed_ideas = {}
            c.stability = D("0.6")
            c.trees = set()
            c.subject = False

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
                answer = frozenset((context.tag, value)) in self.wars
            elif key == "has_war":
                answer = (context.war or any(context.tag in pair for pair in self.wars)) == (value == "yes")
            elif key == "is_subject":
                answer = context.subject == (value == "yes")
            elif key == "any_country":
                answer = any(self.trigger(value, c, temp, root, context) for c in self.countries.values()
                             if any(s.owner == c.tag for s in self.states.values()))
            elif key == "any_controlled_state":
                answer = any(self.trigger(value, s, temp, root, context) for s in self.states.values() if s.controller == context.tag)
            elif key == "is_core_of":
                answer = value in getattr(context, "cores", ()) or context.owner == value
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
            elif key == "declare_war_on":
                self.wars.add(frozenset((context.tag, fields(value)["target"])))
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
        self.execute([r for r in option if r[0] not in ("name", "ai_chance", "trigger")], self.countries[tag])


def world(mode="full", today=date(2006, 10, 1)):
    w = World(mode).initialize_both()
    w.today = today.toordinal()
    for name in NAMES.values():
        w.wave_action(name, "on_startup")
    for tag in EXPECTED:
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

    def ready(self, wave=None, mode="full"):
        """A world in which the wave's countries are eligible and initialized."""
        w = self.fresh(mode)
        if wave is EB:
            w.today = date(2008, 1, 1).toordinal()
            for tag in EB.countries:
                w.run("ac_ecw_initialize", tag)
        return w

    def test_every_service_pays_real_owners_once_and_completes_after_ninety_days(self):
        for wave in (FE, NC, EB, AU):
            for b in wave.branches:
                for n in range(2):
                    for mode in ("full", "experimental", "disabled"):
                        with self.subTest(branch=branch_id(b), service=n, mode=mode):
                            w = self.ready(wave, mode)
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
        w = self.ready(wave)
        w.globals |= set(re.findall(r"(?<!NOT = \{ )has_global_flag = (\w+)", b.gate))
        if b.gate.startswith("has_global_flag = ac_ucw_outcome_isaf_victory has_global_flag = ac_fe_insurrection_started"):
            w.globals.add("ac_fe_insurrection_started")
        if "2013.12.31" in b.gate:
            w.today = date(2014, 6, 1).toordinal()
        elif "2009.12.31" in b.gate:
            w.today = date(2010, 6, 1).toordinal()
        w.countries[b.tag].completed |= set(b.entry)
        return w

    def test_branch_policies_exclude_review_needs_service_and_settlement_improves(self):
        for wave in (FE, NC, EB, AU):
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

    def test_aurelia_stages_wait_for_dates_and_earlier_settlements(self):
        first = {k: focus_id(AU, next(b for b in AU.branches if b.key == k), 0) for k in aurelia.STAGE_2 + aurelia.STAGE_3}
        w = self.fresh()
        w.today = date(2005, 6, 1).toordinal()
        c = w.countries["AUR"]
        self.assertFalse(w.available(first["finance"], "AUR"))
        c.completed.add("AUR_au_trade_settlement")
        self.assertFalse(w.available(first["finance"], "AUR"))
        w.today = date(2006, 1, 1).toordinal()
        self.assertTrue(w.available(first["finance"], "AUR"))
        self.assertFalse(w.available(first["leasath_war"], "AUR"))
        w.today = date(2010, 1, 1).toordinal()
        self.assertTrue(w.available(first["leasath_war"], "AUR"))
        self.assertFalse(w.available(first["relations"], "AUR"))
        c.completed.add("AUR_au_exports_settlement")
        self.assertFalse(w.available(first["relations"], "AUR"))
        w.today = date(2014, 1, 1).toordinal()
        self.assertTrue(w.available(first["relations"], "AUR"))

    def test_aurelia_adoption_and_hand_off_flags(self):
        w = self.prepare(AU, next(b for b in AU.branches if b.key == "relations"))
        c = w.countries["AUR"]
        decision = fields(fields(parse(text("common/decisions/ac_aurelia.txt")))["ac_aur_aur_services"])["AUR_au_adopt_campaign"]
        w.execute(fields(decision)["complete_effect"], c)
        self.assertIn(aurelia.TREE_ID, c.trees)
        w.complete("AUR_au_relations_register", "AUR")
        w.complete("AUR_au_relations_policy_a", "AUR")
        self.assertIn("AUR_au_relations_policy_a_done", c.flags)
        self.assertFalse(w.available("AUR_au_relations_policy_b", "AUR"))

    def ecw(self, today=date(2007, 4, 3)):
        w = self.ready(EB)
        w.today = today.toordinal()
        return w, w.countries["EVA"]

    def weekly_at(self, w, day):
        w.today = day.toordinal()
        w.wave_action("estovakia", "on_weekly_EVA", "EVA")

    def news(self, w):
        return [e for _, e, _ in w.events if e.startswith("ac_ecw.")]

    def test_civil_war_starts_on_the_anchor_and_late_saves_never_replay_it(self):
        w, c = self.ecw(date(2007, 4, 2))
        w.wave_action("estovakia", "on_weekly_EVA", "EVA")
        self.assertNotIn("ac_ecw_capital_seized", w.globals)
        self.weekly_at(w, date(2007, 4, 3))
        self.assertIn("ac_ecw_capital_seized", w.globals)
        self.assertEqual(D(75), c.variables["ac_ecw_luf_authority"])
        self.assertEqual(D(20), c.variables["ac_ecw_eastern_strength"])
        self.assertIn("ac_ecw_luf_holds_capital", c.ideas)
        self.assertEqual(["ac_ecw.1"], self.news(w))
        late, lc = self.ecw(date(2008, 5, 1))
        late.wave_action("estovakia", "on_weekly_EVA", "EVA")
        self.assertIn("ac_ecw_late_start_skipped", late.globals)
        self.assertNotIn("ac_ecw_capital_seized", late.globals)
        self.assertNotIn("ac_ecw_luf_authority", lc.variables)

    def test_historical_chain_fires_each_anchor_once_and_ends_in_2013(self):
        w, c = self.ecw()
        w.globals.add("ac_anea_bureau")
        anea_before = {g for g in w.globals if g.startswith("ac_anea_")}
        eva_anea_before = {k: v for k, v in c.flags.items() if k.startswith(("ac_anea_", "EVA_an_"))}
        self.weekly_at(w, date(2007, 4, 3))
        self.weekly_at(w, date(2007, 6, 30))
        self.assertIn("ac_ecw_war_running", w.globals)
        self.assertEqual(D(70), c.variables["ac_ecw_luf_authority"])
        self.weekly_at(w, date(2008, 7, 15))
        self.assertEqual((D(65), D(35)), (c.variables["ac_ecw_luf_authority"], c.variables["ac_ecw_eastern_strength"]))
        self.weekly_at(w, date(2008, 10, 23))
        self.assertIn("ac_ecw_anea_initiative_on_hold", w.globals)
        self.weekly_at(w, date(2010, 2, 19))
        self.assertIn(("EMM", "ac_ecw.5"), [(t, e) for t, e, _ in w.events])
        w.option("ac_ecw.5", "a", "EMM")
        self.assertIn("ac_ecw_emm_aid_ended_luf", w.globals)
        self.assertEqual(D(60), c.variables["ac_ecw_luf_authority"])
        self.weekly_at(w, date(2011, 5, 9))
        w.option("ac_ecw.6", "a", "EMM")
        self.assertIn("ac_ecw_emm_aid_ended_all", w.globals)
        self.weekly_at(w, date(2013, 1, 15))
        self.assertEqual(D(20), c.variables["ac_ecw_luf_authority"])
        self.assertIn("ac_ecw_luf_in_retreat", c.ideas)
        self.weekly_at(w, date(2013, 10, 29))
        self.assertTrue({"ac_ecw_ended", "ac_ecw_eastern_victory", "ac_ecw_historical_end"} <= w.globals)
        self.assertFalse(any(i in c.ideas for i in ("ac_ecw_luf_holds_capital", "ac_ecw_divided_country", "ac_ecw_luf_in_retreat")))
        self.assertIn("ac_ecw_civil_war_ended", c.ideas)
        for day in (date(2013, 11, 25), date(2014, 2, 3), date(2014, 2, 4), date(2014, 3, 1)):
            self.weekly_at(w, day)
        self.assertEqual(["ac_ecw.1", "ac_ecw.2", "ac_ecw.3", "ac_ecw.4", "ac_ecw.5", "ac_ecw.6", "ac_ecw.7", "ac_ecw.9",
                          "ac_ecw.10", "ac_ecw.11", "ac_ecw.12"], self.news(w))
        self.assertEqual(anea_before, {g for g in w.globals if g.startswith("ac_anea_")})
        self.assertEqual(eva_anea_before, {k: v for k, v in c.flags.items() if k.startswith(("ac_anea_", "EVA_an_"))})

    def test_emmerian_alternatives_need_the_conditional_aid_policy_and_ai_follows_history(self):
        w, c = self.ecw()
        self.weekly_at(w, date(2007, 4, 3))
        options = {next(x for k, _, x in v if k == "name"): v for k, _, v in w.messages["ac_ecw.5"] if k == "option"}
        condition = fields(options["ac_ecw.5.b"])["trigger"]
        self.assertFalse(w.trigger(condition, w.countries["EMM"]))
        w.countries["EMM"].flags["EMM_ecw_aid_policy_a_done"] = None
        self.assertTrue(w.trigger(condition, w.countries["EMM"]))
        self.assertEqual("100", fields(fields(options["ac_ecw.5.a"])["ai_chance"])["factor"])
        self.assertEqual("0", fields(fields(options["ac_ecw.5.b"])["ai_chance"])["factor"])
        pp = w.countries["EMM"].pp
        w.option("ac_ecw.5", "b", "EMM")
        self.assertIn("ac_ecw_emm_aid_conditional", w.globals)
        self.assertEqual(pp - 25, w.countries["EMM"].pp)

    def test_negotiated_settlement_is_earned_not_free(self):
        w, c = self.ecw()
        self.weekly_at(w, date(2007, 4, 3))
        self.weekly_at(w, date(2007, 6, 30))
        decision = fields(fields(parse(text("common/decisions/ac_estovakia.txt")))["ac_ecw_eva_services"])["EVA_ecw_negotiate"]
        self.assertFalse(w.trigger(fields(decision)["available"], c))
        c.flags.update({"EVA_ecw_talks_policy_a_done": None, "EVA_ecw_capital_policy_a_done": None})
        self.assertFalse(w.trigger(fields(decision)["available"], c))
        w.globals.add("ac_ecw_emm_aid_conditional")
        self.assertTrue(w.trigger(fields(decision)["available"], c))
        pp = c.pp
        w.execute(fields(decision)["complete_effect"], c)
        self.assertTrue({"ac_ecw_ended", "ac_ecw_negotiated"} <= w.globals)
        self.assertNotIn("ac_ecw_historical_end", w.globals)
        self.assertEqual(pp - 50, c.pp)
        self.assertIn("ac_ecw_negotiated_peace", c.ideas)
        self.assertEqual("ac_ecw.14", self.news(w)[-1])
        self.weekly_at(w, date(2013, 1, 15))
        self.weekly_at(w, date(2013, 10, 29))
        self.assertNotIn("ac_ecw.9", self.news(w))

    def test_weak_eastern_faction_gives_the_provisional_prolonged_war(self):
        w, c = self.ecw()
        self.weekly_at(w, date(2007, 4, 3))
        self.weekly_at(w, date(2007, 6, 30))
        c.flags["EVA_ecw_oil_policy_b_done"] = None
        self.weekly_at(w, date(2008, 7, 15))
        self.assertEqual(D(25), c.variables["ac_ecw_eastern_strength"])
        self.weekly_at(w, date(2013, 1, 15))
        self.assertIn("ac_ecw_prolonged", w.globals)
        self.assertIn("ac_ecw.8", self.news(w))
        before = c.variables["ac_ecw_luf_authority"]
        self.weekly_at(w, date(2013, 10, 29))
        self.assertNotIn("ac_ecw_ended", w.globals)
        self.assertLess(c.variables["ac_ecw_luf_authority"], before)
        c.variables["ac_ecw_luf_authority"] = D("20.05")
        self.weekly_at(w, date(2015, 3, 1))
        self.assertTrue({"ac_ecw_ended", "ac_ecw_eastern_victory"} <= w.globals)
        self.assertNotIn("ac_ecw_historical_end", w.globals)
        self.assertEqual("ac_ecw.13", self.news(w)[-1])
        self.assertFalse({"ac_ecw.10", "ac_ecw.11", "ac_ecw.12"} & set(self.news(w)))

    def test_policies_shift_the_balance_and_annexation_closes_the_owner(self):
        w, c = self.ecw()
        self.weekly_at(w, date(2007, 4, 3))
        w.complete("EVA_ecw_capital_register", "EVA")
        w.complete("EVA_ecw_capital_policy_b", "EVA")
        self.assertEqual((D(83), D(25)), (c.variables["ac_ecw_luf_authority"], c.variables["ac_ecw_eastern_strength"]))
        w.wave_action("estovakia", "on_annex", "EMM", "EVA")
        self.assertIn("ac_ecw_closed", w.globals)
        self.assertFalse(any(i.startswith("ac_ecw_luf") or i == "ac_ecw_divided_country" for i in c.ideas))

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

    # Wave C: the Circum-Pacific War owner ------------------------------------------
    def cpw(self, today=date(2010, 9, 22)):
        w = self.fresh()
        w.today = today.toordinal()
        return w, w.countries["YUK"], w.countries["OSE"]

    def tick(self, w, day, tag="YUK"):
        w.today = day.toordinal()
        w.wave_action("circum_pacific", f"on_weekly_{tag}", tag)

    def cpw_news(self, w):
        return [e for _, e, _ in w.events if e.startswith("ac_cpw.") and e not in ("ac_cpw.5", "ac_cpw.6")]

    def earn(self, w, tag, record):
        """Satisfy the real ac_snc_* trigger for one record, as the national package defines it."""
        c = w.countries[tag]
        c.flags[f"ac_snc_{tag.lower()}_initialized"] = None
        c.variables[f"ac_snc_{tag.lower()}_identity"] = D(c.identity)
        if (tag, record) == ("YUK", "verification"):
            c.flags.update({"YUK_snc_field_answers_settlement_done": None, "YUK_snc_field_answers_civil_done": None, "ac_snc_yuk_message_10_public": None})
            c.ideas.add("yuk_reformed_field_command")
            c.completed.add("YUK_army_reform_complete")
            c.variables["ac_snp_yuk_civil"] = D(60)
        elif (tag, record) == ("YUK", "channel"):
            c.flags["YUK_snc_scientific_custody_settlement_done"] = None
        elif (tag, record) == ("OSE", "verification"):
            c.flags.update({"OSE_snc_contact_verification_settlement_done": None, "OSE_snc_contact_verification_civil_done": None, "ac_snc_ose_message_11_public": None})
        else:
            c.flags["OSE_snc_pacific_channel_settlement_done"] = None

    def declare(self, w):
        self.tick(w, date(2010, 9, 27))
        w.option("ac_cpw.5", "a", "YUK")
        self.assertIn("ac_cpw_started", w.globals)
        return w

    def test_arkbird_summit_needs_the_completed_project_and_fires_once(self):
        w, y, o = self.cpw(date(2008, 8, 21))
        self.tick(w, date(2008, 8, 21))
        self.assertEqual([], self.cpw_news(w))
        self.assertFalse({"ac_cpw_summit_held", "ac_cpw_summit_skipped"} & w.globals)
        w.globals.add("ac_sp_arkbird_complete")
        self.tick(w, date(2008, 8, 28))
        self.tick(w, date(2008, 9, 4))
        self.assertEqual(["ac_cpw.14"], self.cpw_news(w))
        self.assertIn("ac_cpw_summit_held", w.globals)
        late, _, _ = self.cpw(date(2009, 9, 1))
        late.globals.add("ac_sp_arkbird_complete")
        self.tick(late, date(2009, 9, 1))
        self.assertIn("ac_cpw_summit_skipped", late.globals)
        self.assertEqual([], self.cpw_news(late))

    def test_prelude_and_declaration_follow_the_anchor_and_late_saves_never_replay(self):
        w, y, o = self.cpw()
        self.tick(w, date(2010, 9, 22))
        self.assertIn("ac_cpw_calendar_started", w.globals)
        self.assertEqual([], self.cpw_news(w))
        self.tick(w, date(2010, 9, 23))
        self.tick(w, date(2010, 9, 24))
        self.tick(w, date(2010, 9, 26))
        self.assertEqual(["ac_cpw.1", "ac_cpw.2"], self.cpw_news(w))
        self.assertNotIn("ac_cpw_started", w.globals)
        self.tick(w, date(2010, 9, 27))
        self.assertIn(("YUK", "ac_cpw.5", w.today + 1), w.events)
        self.assertTrue({"ac_cpw_declaration_asked", "ac_cpw_declaration_pending", "ac_cpw_declaration_window"} <= set(y.flags))
        self.assertEqual(set(), w.wars)
        options = {next(x for k, _, x in v if k == "name"): v for k, _, v in w.messages["ac_cpw.5"] if k == "option"}
        self.assertEqual("100", fields(fields(options["ac_cpw.5.a"])["ai_chance"])["factor"])
        self.assertEqual("0", fields(fields(options["ac_cpw.5.b"])["ai_chance"])["factor"])
        self.assertEqual("ac_cpw_mandate_earned = yes", " ".join(f"{k} = {v}" for k, _, v in fields(options["ac_cpw.5.b"])["trigger"]))
        w.option("ac_cpw.5", "a", "YUK")
        self.assertEqual({frozenset(("YUK", "OSE"))}, w.wars)
        self.assertIn("ac_cpw_started", w.globals)
        self.assertFalse({"ac_cpw_tainted", "ac_cpw_pre_existing_war"} & w.globals)
        self.assertTrue({"ac_cpw_yuk_war_footing", "ac_cpw_yuk_submarine_carriers"} <= y.ideas)
        self.assertIn("ac_cpw_ose_war_footing", o.ideas)
        self.assertNotIn("ac_cpw_declaration_pending", y.flags)
        self.assertEqual(["ac_cpw.1", "ac_cpw.2", "ac_cpw.3"], self.cpw_news(w))
        # The tick never asks twice and never declares twice.
        self.tick(w, date(2010, 9, 28))
        self.assertEqual(["ac_cpw.1", "ac_cpw.2", "ac_cpw.3"], self.cpw_news(w))
        late, _, _ = self.cpw(date(2011, 10, 1))
        self.tick(late, date(2011, 10, 1))
        self.assertTrue({"ac_cpw_closed", "ac_cpw_late_start_skipped"} <= late.globals)
        self.assertNotIn("ac_cpw_calendar_started", late.globals)
        self.assertEqual([], self.cpw_news(late))
        gone, _, _ = self.cpw()
        for state in gone.states.values():
            if state.owner == "OSE":
                state.owner = state.controller = "BLK"
        self.tick(gone, date(2010, 9, 22))
        self.assertTrue({"ac_cpw_closed", "ac_cpw_principal_missing"} <= gone.globals)

    def test_declaration_window_falls_back_to_history_and_withholding_needs_the_mandate(self):
        w, y, o = self.cpw()
        self.tick(w, date(2010, 9, 27))
        self.tick(w, date(2010, 10, 4))
        self.assertNotIn("ac_cpw_started", w.globals)
        self.tick(w, date(2010, 10, 12))
        self.assertIn("ac_cpw_started", w.globals)
        self.assertEqual({frozenset(("YUK", "OSE"))}, w.wars)
        w2, y2, o2 = self.cpw()
        self.tick(w2, date(2010, 9, 27))
        w2.option("ac_cpw.5", "b", "YUK")
        self.assertNotIn("ac_cpw_declaration_withheld", w2.globals)
        self.assertIn("ac_cpw_declaration_pending", y2.flags)
        self.earn(w2, "YUK", "verification")
        w2.option("ac_cpw.5", "b", "YUK")
        self.assertIn("ac_cpw_declaration_withheld", w2.globals)
        self.assertIn("ac_cpw_yuk_mandate_kept", y2.ideas)
        self.assertNotIn("ac_cpw_declaration_pending", y2.flags)
        self.assertEqual(set(), w2.wars)
        for day in (date(2010, 9, 30), date(2010, 10, 25), date(2010, 12, 31), date(2011, 3, 1)):
            self.tick(w2, day)
        self.assertEqual(["ac_cpw.5", "ac_cpw.7"], [e for _, e, _ in w2.events if e.startswith("ac_cpw.") and e not in ("ac_cpw.1", "ac_cpw.2")])
        self.assertFalse({"ac_cpw_started", "ac_cpw_closed"} & w2.globals)

    def test_reciprocal_exchange_prevents_the_declaration_and_is_earned(self):
        w, y, o = self.cpw()
        for tag, record in (("OSE", "verification"), ("OSE", "channel"), ("YUK", "verification"), ("YUK", "channel")):
            self.earn(w, tag, record)
        self.tick(w, date(2010, 9, 27))
        self.assertIn("ac_cpw_prevented", w.globals)
        self.assertNotIn("ac_cpw_started", w.globals)
        self.assertNotIn(("YUK", "ac_cpw.5", w.today + 1), w.events)
        self.assertEqual(set(), w.wars)
        self.assertIn("ac_cpw_yuk_exchange_standing", y.ideas)
        self.assertIn("ac_cpw_ose_exchange_standing", o.ideas)
        self.assertEqual(["ac_cpw.4"], [e for _, e, _ in w.events if e.startswith("ac_cpw.") and e not in ("ac_cpw.1", "ac_cpw.2")])
        partial, _, _ = self.cpw()
        for tag, record in (("OSE", "verification"), ("OSE", "channel"), ("YUK", "channel")):
            self.earn(partial, tag, record)
        self.tick(partial, date(2010, 9, 27))
        self.assertNotIn("ac_cpw_prevented", partial.globals)
        self.assertIn(("YUK", "ac_cpw.5", partial.today + 1), partial.events)

    def test_historical_course_fires_each_stage_once_and_ends_on_observed_cessation(self):
        w, y, o = self.cpw()
        w.globals.add("ac_sp_arkbird_complete")
        o.ideas |= {"ac_sp_arkbird_debris_clearing", "ac_sp_arkbird_joint_operations"}
        y.ideas.add("ac_sp_arkbird_joint_operations")
        self.declare(w)
        self.tick(w, date(2010, 9, 30))
        self.assertIn("ac_cpw_stage_eaglin", w.globals)
        self.assertIn("ac_cpw_ose_carrier_losses", o.ideas)
        self.assertIn(("OSE", "ac_cpw.6", w.today + 1), w.events)
        w.option("ac_cpw.6", "a", "OSE")
        self.assertIn("ac_cpw_arkbird_committed", w.globals)
        self.assertIn("ac_cpw_ose_arkbird_at_the_front", o.ideas)
        self.tick(w, date(2010, 10, 4))
        self.assertNotIn("ac_cpw_yuk_submarine_carriers", y.ideas)
        self.assertIn("ac_cpw_yuk_submarine_carrier", y.ideas)
        self.tick(w, date(2010, 10, 22))
        self.tick(w, date(2010, 10, 25))
        self.assertIn("ac_cpw_arkbird_sabotaged", w.globals)
        self.assertIn("ac_cpw_ose_arkbird_grounded", o.ideas)
        self.tick(w, date(2010, 11, 1))
        self.assertNotIn("ac_cpw_stage_bastok", w.globals)
        foothold = next(s for s in w.states.values() if s.owner == "YUK")
        foothold.controller = "OSE"
        self.tick(w, date(2010, 11, 1))
        self.assertIn("ac_cpw_stage_bastok", w.globals)
        self.assertIn("ac_cpw_ose_expeditionary_strain", o.ideas)
        self.tick(w, date(2010, 11, 2))
        self.assertIn("ac_cpw_ose_dresdene_inquiry", o.ideas)
        self.tick(w, date(2010, 11, 4))
        self.assertIn("ac_cpw_ose_home_front_alert", o.ideas)
        self.tick(w, date(2010, 11, 14))
        self.assertFalse({"ac_cpw_yuk_submarine_carriers", "ac_cpw_yuk_submarine_carrier"} & y.ideas)
        self.tick(w, date(2010, 11, 29))
        self.tick(w, date(2010, 12, 6))
        self.assertIn("ac_cpw_yuk_stronghold_lost", y.ideas)
        self.tick(w, date(2010, 12, 9))
        self.assertIn("ac_cpw_ose_president_returns", o.ideas)
        self.tick(w, date(2010, 12, 19))
        self.assertIn("ac_cpw_arkbird_lost", w.globals)
        self.assertFalse({"ac_sp_arkbird_debris_clearing", "ac_sp_arkbird_joint_operations"} & (o.ideas | y.ideas))
        self.assertFalse({"ac_cpw_ose_arkbird_at_the_front", "ac_cpw_ose_arkbird_grounded"} & o.ideas)
        self.assertIn("ac_sp_arkbird_complete", w.globals)
        self.tick(w, date(2010, 12, 23))
        self.assertIn("ac_cpw_yuk_leadership_question", y.ideas)
        self.tick(w, date(2010, 12, 29))
        self.tick(w, date(2010, 12, 30))
        self.assertIn("ac_cpw_disarmament_appeal", w.globals)
        self.assertTrue("ac_cpw_disarmament_appeal" in y.ideas and "ac_cpw_disarmament_appeal" in o.ideas)
        self.tick(w, date(2010, 12, 31))
        self.assertNotIn("ac_cpw_ended", w.globals)
        self.tick(w, date(2011, 1, 7))
        self.assertNotIn("ac_cpw_ended", w.globals)
        w.wars.clear()
        self.tick(w, date(2011, 1, 14))
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation", "ac_cpw_historical_course"} <= w.globals)
        self.assertFalse(any(i.startswith("ac_cpw_") and i.endswith(("_war_footing", "_carriers", "_carrier", "_appeal")) for i in y.ideas | o.ideas))
        self.tick(w, date(2011, 1, 21))
        self.assertEqual(["ac_cpw.1", "ac_cpw.2", "ac_cpw.3", "ac_cpw.20", "ac_cpw.15", "ac_cpw.21", "ac_cpw.22", "ac_cpw.23", "ac_cpw.24", "ac_cpw.25",
                          "ac_cpw.26", "ac_cpw.27", "ac_cpw.28", "ac_cpw.29", "ac_cpw.30", "ac_cpw.31", "ac_cpw.32", "ac_cpw.33", "ac_cpw.34", "ac_cpw.35",
                          "ac_cpw.10"], self.cpw_news(w))
        self.assertFalse({g for g in w.globals if g.startswith(("ac_snc_", "ac_snp_"))})

    def test_arkbird_stages_need_the_completed_project_and_the_commitment(self):
        w, y, o = self.cpw()
        self.declare(w)
        for day in (date(2010, 9, 30), date(2010, 10, 25), date(2010, 12, 19)):
            self.tick(w, day)
        self.assertNotIn(("OSE", "ac_cpw.6"), [(t, e) for t, e, _ in w.events])
        self.assertFalse({"ac_cpw_stage_arkbird_sabotage", "ac_cpw_stage_arkbird_lost"} & w.globals)
        self.assertIn("ac_cpw_stage_eaglin", w.globals)
        held, y2, o2 = self.cpw()
        held.globals.add("ac_sp_arkbird_complete")
        self.declare(held)
        self.tick(held, date(2010, 9, 30))
        held.option("ac_cpw.6", "b", "OSE")
        self.assertIn("ac_cpw_arkbird_held_back", held.globals)
        for day in (date(2010, 10, 7), date(2010, 10, 25), date(2010, 12, 19)):
            self.tick(held, day)
        self.assertEqual(1, [e for _, e, _ in held.events].count("ac_cpw.6"))
        self.assertFalse({"ac_cpw_arkbird_committed", "ac_cpw_stage_arkbird_sabotage", "ac_cpw_stage_arkbird_lost"} & held.globals)

    def test_pre_existing_or_third_party_wars_move_the_crisis_to_external_observation(self):
        w, y, o = self.cpw()
        w.wars.add(frozenset(("OSE", "BLK")))
        self.declare(w)
        self.assertTrue({"ac_cpw_tainted", "ac_cpw_pre_existing_war"} <= w.globals)
        self.tick(w, date(2010, 9, 30))
        self.assertNotIn("ac_cpw_stage_eaglin", w.globals)
        w.wars.discard(frozenset(("YUK", "OSE")))
        self.tick(w, date(2010, 10, 7))
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_cessation"} <= w.globals)
        self.assertNotIn("ac_cpw_historical_course", w.globals)
        self.assertEqual(["ac_cpw.3", "ac_cpw.9", "ac_cpw.13"], [e for _, e, _ in w.events if e.startswith("ac_cpw.") and e not in ("ac_cpw.1", "ac_cpw.2", "ac_cpw.5")])
        later, y2, o2 = self.cpw()
        self.declare(later)
        self.tick(later, date(2010, 9, 30))
        self.assertIn("ac_cpw_stage_eaglin", later.globals)
        later.wars.add(frozenset(("YUK", "BLK")))
        self.tick(later, date(2010, 10, 4))
        self.assertIn("ac_cpw_tainted", later.globals)
        self.assertNotIn("ac_cpw_stage_sand_island", later.globals)
        self.assertIn("ac_cpw.9", [e for _, e, _ in later.events])
        self.assertIn("ac_cpw_yuk_war_footing", y2.ideas)
        existing, y3, o3 = self.cpw()
        existing.wars.add(frozenset(("OSE", "YUK")))
        self.tick(existing, date(2010, 9, 27))
        self.assertTrue({"ac_cpw_started", "ac_cpw_tainted", "ac_cpw_existing_war_observed"} <= existing.globals)
        self.assertNotIn(("YUK", "ac_cpw.5", existing.today + 1), existing.events)
        self.assertNotIn("ac_cpw_yuk_war_footing", y3.ideas)
        self.assertIn("ac_cpw.8", [e for _, e, _ in existing.events])

    def test_capitulation_and_annexation_record_the_actual_outcome(self):
        w, y, o = self.cpw()
        w.globals.add("ac_sp_arkbird_complete")
        self.declare(w)
        self.tick(w, date(2010, 9, 30))
        w.option("ac_cpw.6", "a", "OSE")
        self.assertIn("ac_cpw_ose_arkbird_at_the_front", o.ideas)
        y.capitulated = True
        w.wave_action("circum_pacific", "on_capitulation_immediate", "YUK")
        self.assertTrue({"ac_cpw_yuk_fallen", "ac_cpw_ended", "ac_cpw_outcome_osean_victory"} <= w.globals)
        self.assertIn("ac_cpw.11", [e for _, e, _ in w.events])
        # Every untimed owner idea leaves with the war, including the Arkbird deployment.
        self.assertFalse({i for i in o.ideas | y.ideas if i.startswith("ac_cpw_") and i not in ("ac_cpw_ose_carrier_losses",)})
        w2, y2, o2 = self.cpw()
        self.declare(w2)
        w2.wave_action("circum_pacific", "on_annex", "YUK", "OSE")
        self.assertTrue({"ac_cpw_ose_fallen", "ac_cpw_ended", "ac_cpw_outcome_yuktobanian_victory"} <= w2.globals)
        self.assertIn("ac_cpw.12", [e for _, e, _ in w2.events])
        w3, y3, o3 = self.cpw()
        self.declare(w3)
        for state in w3.states.values():
            if state.owner == "YUK":
                state.owner = state.controller = "OSE"
        self.tick(w3, date(2010, 10, 4), "OSE")
        self.assertTrue({"ac_cpw_ended", "ac_cpw_outcome_osean_victory"} <= w3.globals)

    def test_crisis_decisions_cost_once_and_follow_the_phase(self):
        rows = {k: v for category in parse(text("common/decisions/ac_circum_pacific.txt")) for k, _, v in category[2]}
        for tag in ("OSE", "YUK"):
            with self.subTest(tag=tag):
                w, y, o = self.cpw()
                c = w.countries[tag]
                home, record = rows[f"{tag}_cpw_home_front"], rows[f"{tag}_cpw_war_record"]
                self.assertFalse(w.trigger(fields(home)["available"], c))
                self.declare(w)
                self.assertTrue(w.trigger(fields(home)["available"], c))
                self.assertFalse(w.trigger(fields(record)["available"], c))
                # The engine charges `cost` once; the effects must not charge it again.
                self.assertEqual(("50", "25"), (fields(home)["cost"], fields(record)["cost"]))
                self.assertEqual(("yes", "yes"), (fields(home)["fire_only_once"], fields(record)["fire_only_once"]))
                pp = c.pp
                w.execute(fields(home)["complete_effect"], c)
                self.assertEqual(pp, c.pp)
                self.assertIn(f"ac_cpw_{tag.lower()}_home_front", c.ideas)
                self.assertFalse(w.trigger(fields(home)["available"], c))
                snapshot = copy.deepcopy(c)
                w.execute(fields(home)["complete_effect"], c)
                self.assertEqual(snapshot, c)
                w.wars.clear()
                self.tick(w, date(2010, 10, 4))
                self.assertTrue(w.trigger(fields(record)["available"], c))
                w.execute(fields(record)["complete_effect"], c)
                self.assertEqual(pp, c.pp)
                self.assertIn(f"ac_cpw_{tag.lower()}_war_record", c.ideas)
        self.assertNotIn("add_political_power", text("common/scripted_effects/ac_circum_pacific.txt"))

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
        self.assertIn(("FCU", "ac_fe.5", w.today + 1), w.events)
        self.assertIn("ac_fe_response_window", c.flags)
        self.assertNotIn("ac_fe_prolonged", w.globals)
        w2 = self.fresh()
        w2.today = date(2006, 10, 1).toordinal()
        w2.globals.add("ac_ucw_outcome_stalemate")
        w2.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w2.globals)
        # A capitulated Erusea that still owns land cannot start the insurrection.
        w3, c3 = self.owner()
        c3.capitulated = True
        w3.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertNotIn("ac_fe_insurrection_started", w3.globals)
        self.assertNotIn("ac_fe_pressure", c3.variables)
        self.assertEqual([], [e for _, e, _ in w3.events if e.startswith("ac_fe.")])

    def test_historical_route_records_the_defeat_by_mobius_1(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        option = {next(x for k, _, x in v if k == "name"): v for k, _, v in w.messages["ac_fe.5"] if k == "option"}
        self.assertEqual("100", fields(fields(option["ac_fe.5.a"])["ai_chance"])["factor"])
        self.assertEqual("0", fields(fields(option["ac_fe.5.b"])["ai_chance"])["factor"])
        w.events.clear()
        w.option("ac_fe.5", "a", "FCU")
        self.assertIn("ac_fe_insurrection_defeated", w.globals)
        self.assertNotIn("ac_fe_prolonged", w.globals)
        self.assertEqual(["ac_fe.6"], [e for _, e, _ in w.events])
        self.assertFalse(any(i.startswith("ac_fe_pressure_") for i in c.ideas))
        frozen = c.variables["ac_fe_pressure"]
        for _ in range(8):
            w.advance(7)
            w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        w.run("ac_fe_relief_major", "ERU")
        self.assertEqual(frozen, c.variables["ac_fe_pressure"])
        self.assertEqual(["ac_fe.6"], [e for _, e, _ in w.events])
        self.assertNotIn("ac_fe_prolonged", w.globals)
        # The aftermath branches stay open after the historical defeat.
        c.completed.add("ERU_ucw_exp_settlement_assessment")
        self.assertTrue(w.available("ERU_fe_insurrection_register", "ERU"))

    def test_prolonged_route_is_provisional_and_needs_no_central_usean_answer(self):
        w, c = self.owner()
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        w.option("ac_fe.5", "b", "FCU")
        self.assertIn("ac_fe_prolonged", w.globals)
        before = c.variables["ac_fe_pressure"]
        w.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertEqual(before + D("0.4"), c.variables["ac_fe_pressure"])
        w.run("ac_fe_defeat", "FCU")
        self.assertNotIn("ac_fe_insurrection_defeated", w.globals)
        # Central Usea cannot answer: the prolonged route starts at once.
        w2, c2 = self.owner()
        for state in w2.states.values():
            if state.owner == "FCU":
                state.owner = state.controller = "ERU"
        w2.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertIn("ac_fe_prolonged", w2.globals)
        self.assertNotIn("ac_fe.5", [e for _, e, _ in w2.events])
        # An unanswered response window falls back to the prolonged route.
        w3, c3 = self.owner()
        w3.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        w3.advance(31)
        w3.wave_action("free_erusea", "on_weekly_ERU", "ERU")
        self.assertIn("ac_fe_prolonged", w3.globals)

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
