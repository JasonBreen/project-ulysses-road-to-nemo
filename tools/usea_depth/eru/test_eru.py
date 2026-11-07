"""Static and offline checks for the Usea Depth Erusea package (README test checklist).

Runs from tools/usea_depth/run_checks.py. Nothing here launches HOI4; the war-start
simulation uses the World harness of tools/Test-ContinentalWar.py, which executes
the shipped script subset offline and is not the engine.
"""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / "tools"), str(HERE)]
from usea_depth import seams  # noqa: E402
import content as C  # noqa: E402
import narrative as N  # noqa: E402

MOD = ROOT / "mod/2985041246"
MARKER, WRAPPERS = seams.MARKERS["eru"]
FILES = {
    "focus": MOD / "common/national_focus/ac_ud_eru.txt",
    "events": MOD / "events/ac_ud_eru.txt",
    "ideas": MOD / "common/ideas/ac_ud_eru.txt",
    "effects": MOD / "common/scripted_effects/ac_ud_eru.txt",
    "triggers": MOD / "common/scripted_triggers/ac_ud_eru.txt",
    "characters": MOD / "common/characters/ac_ud_eru.txt",
    "on_actions": MOD / "common/on_actions/ac_ud_eru.txt",
}
LOC = MOD / "localisation/english/ac_ud_eru_l_english.yml"
GFX = MOD / "interface/ac_ud_eru.gfx"
REFERENCE = Path(r"G:/steamlbirary/steamapps/common/Hearts of Iron IV/documentation/modifiers_documentation.md")


def text(path):
    return path.read_text(encoding="utf-8-sig")


def script():
    return "\n".join(text(path) for path in FILES.values())


def all_loc_keys():
    keys = set()
    for path in (MOD / "localisation").rglob("*.yml"):
        keys.update(re.findall(r'^\s*([^\s:#]+):\d*\s+"', path.read_text(encoding="utf-8-sig", errors="replace"), re.M))
    return keys


def package_loc():
    return dict(re.findall(r'^ ([^\s:]+):0 "((?:\\.|[^"\\])*)"$', text(LOC), re.M))


def load_ucw():
    spec = importlib.util.spec_from_file_location("ulysses_ucw_harness", ROOT / "tools/Test-ContinentalWar.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


UCW = load_ucw()
mapping, load, day = UCW.mapping, UCW.load, UCW.day
REGIME_KEYS = ("set_politics", "set_popularities", "recruit_character", "promote_character")
# Existing low-weight de-escalation focuses belong to the Continental War owner, which tests them itself.
OWNER_DEESCALATION = {"ERU_ucw_refugee_quotas", "ERU_ucw_continental_dialogue"}


class Sim(UCW.World):
    """The Continental War World with this package (and the opening tree) applied."""

    def __init__(self, when="1991.1.1", fiscal=False, own_weekly_first=False):
        super().__init__(when, fiscal=fiscal)
        self.effects.update(mapping(load("common/scripted_effects/ac_ud_eru.txt")))
        self.triggers.update(mapping(load("common/scripted_triggers/ac_ud_eru.txt")))
        self.triggers.update(mapping(load("common/scripted_triggers/ac_expansion.txt")))
        self.events.update({mapping(v)["id"]: (k, v) for k, _, v in load("events/ac_ud_eru.txt") if k == "country_event"})
        on_actions = mapping(mapping(load("common/on_actions/ac_ud_eru.txt"))["on_actions"])
        self.own_weekly = mapping(on_actions["on_weekly_ERU"])["effect"]
        self.own_weekly_first = own_weekly_first
        opening = load("common/national_focus/ERU_opening.txt")[0][2]
        war = load("common/national_focus/ERU.txt")[0][2]
        shared = {mapping(v)["id"]: v for k, _, v in load("common/national_focus/ac_ud_eru.txt") if k == "shared_focus"}
        self.focuses.update({mapping(v)["id"]: v for k, _, v in opening if k == "focus"})
        self.focuses.update(shared)
        imported = lambda tree: [v for k, _, v in tree if k == "shared_focus" and isinstance(v, str) and v in shared]
        self.trees = {
            C.OPENING_TREE: [mapping(v)["id"] for k, _, v in opening if k == "focus"] + imported(opening),
            C.WAR_TREE: [mapping(v)["id"] for k, _, v in war if k == "focus"] + imported(war),
        }
        self.regime_calls = []
        self.fiscal_calls = []
        self.popularity = Counter()
        self.grievance_log = []
        self.progress = None

    def trigger(self, nodes, country):
        answers = []
        rest = []
        for node in nodes:
            key, _, value = node
            if key == "has_completed_focus":
                answers.append(value in country.focuses)
            elif key == "has_character":
                answers.append(False)
            else:
                rest.append(node)
        return all(answers) and (super().trigger(rest, country) if rest else True)

    def execute(self, nodes, country):
        rest = []
        for node in nodes:
            key, _, value = node
            if key in REGIME_KEYS:
                self.regime_calls.append((self.today, key))
            elif key == "add_popularity":
                data = UCW.fields(value)
                self.popularity[data["ideology"]] += float(data["popularity"])
            elif key == "add_tech_bonus":
                data = UCW.fields(value)
                assert int(data["uses"]) == 1 and 0 < float(data["bonus"]) <= 1, data
                country.bonuses.append(data)
            elif key.startswith("ac_econ_") and key != "ac_econ_ready":
                assert self.fiscal, "Unguarded fiscal call: " + key
                self.fiscal_calls.append(key)
            else:
                rest.append(node)
        # Keep if/else_if chains intact by executing the non-intercepted nodes in order.
        if rest:
            super().execute(rest, country)

    def tick(self, tags=UCW.TAGS):
        eru = self.countries["ERU"]
        if self.own_weekly_first:
            self.execute(self.own_weekly, eru)
        super().tick(tags)
        if not self.own_weekly_first:
            self.execute(self.own_weekly, eru)

    def tree(self):
        eru = self.countries["ERU"]
        return eru.tree or C.OPENING_TREE

    def weight(self, ident):
        return float(UCW.fields(mapping(self.focuses[ident])["ai_will_do"])["factor"])

    def ai_focus(self, rng=None):
        eru = self.countries["ERU"]
        if self.progress:
            ident, tree, finish = self.progress
            if tree != self.tree() or not self.focus_available(ident, "ERU"):
                self.progress = None          # cancel_if_invalid / tree switch
            elif self.today >= finish:
                self.progress = None
                self.complete(ident, "ERU")
                return ident
            else:
                return None
        candidates = [i for i in self.trees[self.tree()] if i not in eru.focuses and i not in OWNER_DEESCALATION
                      and self.weight(i) > 0 and self.focus_available(i, "ERU")]
        if not candidates:
            return None
        if rng is None:
            best = max(self.weight(i) for i in candidates)
            ident = next(i for i in candidates if self.weight(i) == best)
        else:
            ident = rng.choices(candidates, [self.weight(i) for i in candidates])[0]
        cost = int(mapping(self.focuses[ident])["cost"])
        self.progress = (ident, self.tree(), self.today + cost * 7)
        return None

    def run_until(self, when, rng=None):
        end = day(when) if isinstance(when, str) else when
        while self.today < end:
            self.today += 7
            self.ai_focus(rng)
            self.tick()
            self.drain()
            eru = self.countries["ERU"]
            if "ac_ucw_grievance" in eru.variables:
                self.grievance_log.append((self.today, eru.variables["ac_ucw_grievance"]))
        return self


def run_ai(seed=None, own_weekly_first=False):
    world = Sim("1991.1.1", own_weekly_first=own_weekly_first)
    return world.run_until("2003.9.30", random.Random(seed) if seed is not None else None)


class Package(unittest.TestCase):
    def assertNoMatch(self, pattern):
        found = re.search(pattern, self.script)
        self.assertIsNone(found, found and found.group(0))

    @classmethod
    def setUpClass(cls):
        cls.budget = json.loads((HERE / "budget.json").read_text(encoding="utf-8"))
        cls.script = script()
        cls.loc = package_loc()
        cls.positions = seams.tree_positions()

    # -- counts and imports ------------------------------------------------------------
    def test_counts_equal_budget_and_each_id_is_imported_once_in_its_own_block(self):
        opening = [f.id for f in C.FOCUSES if f.tree == "opening"]
        war = [f.id for f in C.FOCUSES if f.tree == "war"]
        self.assertEqual({"package": "eru", "marker": MARKER, "focuses": {"ERU": len(C.FOCUSES)},
                          "trees": {C.OPENING_TREE: len(opening), C.WAR_TREE: len(war)}, "events": len(N.EVENTS)}, self.budget)
        defined = re.findall(r"(?m)^\tid = (\w+)$", text(FILES["focus"]))
        self.assertEqual(opening + war, defined)
        self.assertEqual(len(defined), len(set(defined)))
        for wrapper, ids in (("ERU_opening.txt", opening), ("ERU.txt", war)):
            blocks = {name: found for name, found, _ in seams.import_blocks(text(seams.FOCUS / wrapper))}
            self.assertEqual(ids, blocks[MARKER], wrapper)
        imports = Counter()
        for path in seams.FOCUS.glob("*.txt"):
            imports.update(i for i in re.findall(r"(?m)^\s*shared_focus = (ERU_ud_\w+)\s*$", text(path)))
        self.assertEqual({i: 1 for i in defined}, dict(imports))
        self.assertTrue(all(i.startswith("ERU_ud_") for i in defined))
        self.assertEqual(set(C.IDEAS), set(re.findall(r"(?m)^\t\t(ERU_ud_\w+) = \{$", text(FILES["ideas"]))))
        for path in list(FILES.values()) + [LOC, GFX]:
            self.assertFalse(path.name.startswith(("ERU", "FCU", "NPT", "REC", "YUK", "ac_ucw")), path)

    def test_nodes_sit_in_the_band_titles_fit_and_captions_never_overlap(self):
        opening = [f.id for f in C.FOCUSES if f.tree == "opening"]
        war = [f.id for f in C.FOCUSES if f.tree == "war"]
        self.assertEqual([], seams.band_violations(self.positions[C.OPENING_TREE], opening, 0, 23, 6))
        self.assertEqual([], seams.band_violations(self.positions[C.WAR_TREE], war, 42, 94, 0))
        for tree in (C.OPENING_TREE, C.WAR_TREE):
            nodes = sorted(self.positions[tree].items())
            overlaps = [(a, b) for n, (a, pa) in enumerate(nodes) for b, pb in nodes[n + 1:]
                        if abs(pa[0] - pb[0]) * 96 < 147 and abs(pa[1] - pb[1]) * 160 < 54]
            self.assertEqual([], overlaps, tree)
        for row in C.FOCUSES:
            self.assertTrue(seams.title_fits(row.title), row.id)
        for row in C.FOCUSES:
            for group in row.pre:
                for parent in group.split("|"):
                    ident = parent if parent.startswith("ERU_") else "ERU_ud_" + parent
                    position = self.positions[C.OPENING_TREE if row.tree == "opening" else C.WAR_TREE]
                    self.assertLess(position[ident][1], row.y, (row.id, ident))
            if row.tree == "war":
                self.assertFalse(any(p.startswith(("ERU_ucw_", "ERU_fe_", "ERU_camp_")) for g in row.pre for p in g.split("|")), row.id)

    # -- gates ---------------------------------------------------------------------------
    def test_every_opening_focus_carries_the_era_gate_and_its_band(self):
        nodes = {mapping(v)["id"]: v for k, _, v in load("common/national_focus/ac_ud_eru.txt")}
        source = text(FILES["focus"])
        for row in C.FOCUSES:
            body = source[source.index("id = %s\n" % row.id):]
            body = body[:body.index("\n}\n")]
            available = re.search(r"available = \{ (.*) \}\n", body)[1]
            if row.tree == "opening":
                self.assertIn("date < 1999.12.1 NOT = { has_global_flag = ac_ucw_calendar_started }", available, row.id)
                if row.band:
                    self.assertIn(C.BANDS[row.band][0], available, row.id)
            else:
                self.assertIn("ac_ucw_active = yes", available, row.id)
            self.assertIn(row.id, nodes)
            self.assertIn(row.cost, (5, 10), row.id)

    # -- localisation --------------------------------------------------------------------
    def test_localisation_is_complete_ascii_with_bom_and_every_flag_has_a_label(self):
        self.assertTrue(LOC.read_bytes().startswith(b"\xef\xbb\xbf"))
        keys = all_loc_keys()
        for row in C.FOCUSES:
            self.assertIn(row.id, self.loc)
            self.assertGreaterEqual(len(self.loc[row.id + "_desc"].split()), 15, row.id)
        for ident in C.IDEAS:
            self.assertIn(ident, self.loc)
            self.assertIn(ident + "_desc", self.loc)
        for number, event in N.EVENTS.items():
            base = "%s.%d" % (C.NAMESPACE, number)
            for suffix in [".t", ".d"] + [".%s" % "abcdefgh"[i] for i in range(len(event["options"]))]:
                self.assertIn(base + suffix, self.loc)
        for name in re.findall(r"\bname = ([\w.]+)", self.script):
            self.assertIn(name, keys, name)
        for flag in set(re.findall(r"\bhas_(?:country|global)_flag\s*=\s*(\w+)", self.script)) | set(re.findall(r"\bset_country_flag\s*=\s*(\w+)", self.script)):
            self.assertIn(flag, keys, "Flag without a readable label: " + flag)
        for value in self.loc.values():
            self.assertFalse([c for c in value if ord(c) > 126], value[:60])
        all_ids = Counter(list(self.loc))
        self.assertEqual([], [k for k, n in all_ids.items() if n > 1])

    # -- long-form events ----------------------------------------------------------------
    def test_events_are_long_form_short_titled_and_all_reachable(self):
        self.assertGreaterEqual(len(N.EVENTS), len(C.FOCUSES) // 6)
        for number, event in N.EVENTS.items():
            body = seams.event_text(event["paragraphs"], event["layer"], event["citation"])
            self.assertEqual([], seams.event_problems(body), number)
            self.assertEqual(body.replace("\n", "\\n"), self.loc["%s.%d.d" % (C.NAMESPACE, number)].replace('\\"', '"'))
            self.assertLessEqual(len(event["title"]), 30, number)
            self.assertGreaterEqual(len(event["options"]), 2, number)
        fired = set(int(n) for n in re.findall(r"country_event = \{ id = ac_ud_eru\.(\d+)", self.script))
        self.assertEqual(set(N.EVENTS), fired)
        sprites = set(re.findall(r'name = "(\w+)"', text(GFX)))
        for picture in re.findall(r"picture = (GFX_\w+)", text(FILES["events"])):
            self.assertIn(picture, sprites)

    # -- art -----------------------------------------------------------------------------
    def test_icons_shines_spirits_pictures_and_portraits_resolve_to_mod_textures(self):
        from PIL import Image
        sprites = dict(re.findall(r'name = "(\w+)" texturefile = "([^"]+)"', text(GFX)))
        manifest = json.loads((HERE / "assets.json").read_text(encoding="utf-8"))
        self.assertEqual("Pillow 11.3.0", manifest["renderer"])
        hashes = {row["file"]: row["sha256"] for row in manifest["assets"]}
        self.assertEqual(len(C.FOCUSES), manifest["focus_compositions"])
        self.assertEqual(len(hashes), len(set(hashes.values())))
        for row in C.FOCUSES:
            icon = "GFX_ac_ud_focus_" + row.id
            self.assertEqual(sprites[icon], sprites[icon + "_shine"])
            self.assertEqual("gfx/AC_usea_depth/eru/focus/%s.dds" % row.id, sprites[icon])
        for ident in C.IDEAS:
            self.assertIn("GFX_idea_" + ident, sprites)
        for name, texture in sprites.items():
            self.assertTrue(texture.startswith("gfx/AC_usea_depth/eru/"), name)
            path = MOD / texture
            self.assertTrue(path.is_file(), texture)
            import hashlib
            self.assertEqual(hashes[texture], hashlib.sha256(path.read_bytes()).hexdigest(), texture)
            with Image.open(path) as image:
                self.assertEqual("DDS", image.format)
                expected = (96, 96) if "/focus/" in texture else (75, 75) if "/ideas/" in texture else (210, 176) if "/events/" in texture else (156, 210)
                self.assertEqual(expected, image.size, texture)
        self.assertNotIn("shine_overlay", text(GFX))
        self.assertEqual({"GFX_ac_ud_portrait_ERU_ud_%s_office" % s for s in C.OFFICES},
                         set(re.findall(r'large = "(\w+)"', text(FILES["characters"]))))

    # -- politics ------------------------------------------------------------------------
    def test_government_changes_only_in_regime_effects_reached_with_ai_weight_zero(self):
        self.assertEqual([], seams.political_violations(text(FILES["effects"])))
        for name in ("focus", "events", "ideas", "triggers", "characters", "on_actions"):
            self.assertNotRegex(text(FILES[name]), r"\bset_(politics|popularities)\b", name)
        regimes = set(re.findall(r"(?m)^(ac_ud_eru_regime_\w+) = \{", text(FILES["effects"])))
        self.assertEqual({"ac_ud_eru_regime_" + s for s in C.REGIMES}, regimes)
        reached = [row for row in C.FOCUSES if "ac_ud_eru_regime_" in row.reward]
        self.assertEqual(len(C.REGIMES), len(reached))
        for row in reached:
            self.assertEqual(0, row.ai, row.id)
        for event in N.EVENTS.values():
            for _, effect, _ in event["options"]:
                self.assertNotIn("ac_ud_eru_regime_", effect)
        weekly = text(FILES["effects"]).split("# Government changes")[0]
        self.assertNotIn("ac_ud_eru_regime_", weekly)
        openers = {row.id: row.ai for row in C.FOCUSES if row.slug.startswith("path_")}
        self.assertEqual({"ERU_ud_path_prerogative": 60, "ERU_ud_path_constitution": 0, "ERU_ud_path_regency": 0}, openers)
        for row in C.FOCUSES:
            if row.lane in ("constitution", "regency", "assembly_war", "regency_war"):
                self.assertEqual(0, row.ai, row.id)
        characters = text(FILES["characters"])
        self.assertEqual(sorted("ERU_ud_%s_office" % s for s in C.OFFICES),
                         sorted(re.findall(r"(?m)^\t(ERU_ud_\w+_office) = \{$", characters)))
        for slug, (title, _, _) in C.OFFICES.items():
            self.assertTrue(title.startswith("The "), "Office leaders stay unnamed: " + title)

    def test_grievance_cuts_are_never_taken_by_the_ai(self):
        def cuts(effect):
            return bool(re.search(r"ac_ucw_grievance = -\d", effect))
        for row in C.FOCUSES:
            if cuts(row.reward):
                self.assertEqual(0, row.ai, row.id)
        for number, event in N.EVENTS.items():
            for label, effect, factor in event["options"]:
                if cuts(effect):
                    self.assertEqual(0, factor, (number, label))
        # The carry-over lowers the grievance only behind flags that AI-weighted content never sets.
        def cut(key, value):
            return key == "add_to_variable" and value[0][0] == "ac_ucw_grievance" and float(value[0][2]) < 0

        def lowering(nodes, guards=()):
            found = set()
            for key, _, value in nodes:
                if key in ("if", "else_if", "else") and isinstance(value, list):
                    limit = mapping(value).get("limit", [])
                    flags = tuple(v for k, _, v in limit if k == "has_country_flag")
                    found |= lowering([n for n in value if n[0] != "limit"], guards + flags)
                elif cut(key, value):
                    self.assertTrue(guards, "Unguarded grievance cut in a package effect")
                    found.add(guards[-1])
            return found

        effects = mapping(load("common/scripted_effects/ac_ud_eru.txt"))
        flags = lowering(effects["ac_ud_eru_carry_over"])
        self.assertEqual(set(), lowering(effects["ac_ud_eru_weekly"]))
        self.assertEqual({"ERU_ud_stonehenge_accepted", "ERU_ud_refugees_received", "ERU_ud_first_assembly_elections_done"}, flags)
        for flag in flags:
            setters = [row for row in C.FOCUSES if "set_country_flag = " + flag in row.reward or flag == row.id + "_done"]
            self.assertTrue(setters, flag)
            self.assertEqual([0] * len(setters), [row.ai for row in setters], flag)
            for event in N.EVENTS.values():
                for _, effect, factor in event["options"]:
                    if "set_country_flag = " + flag in effect:
                        self.assertEqual(0, factor, flag)

    # -- guards and banned effects -------------------------------------------------------
    def test_fiscal_calls_are_guarded_and_no_banned_effect_or_ucw_flag_write_appears(self):
        calls = re.findall(r"\bac_econ_(?!ready\b)\w+ = yes", self.script)
        guarded = re.findall(r"if = \{ limit = \{ ac_econ_ready = yes \} ac_econ_\w+ = yes \}", self.script)
        self.assertTrue(calls)
        self.assertEqual(len(calls), len(guarded))
        self.assertEqual([], seams.banned_uses(self.script))
        self.assertNoMatch(r"\b(set|clr)_(global|country)_flag\s*=\s*ac_ucw_")
        self.assertNoMatch(r"\b(set|clr)_(global|country)_flag\s*=\s*ac_fe_")
        self.assertNoMatch(r"\bac_ucw_country_start\s*=")
        self.assertNoMatch(r"\b\d{2,3}\s*=\s*\{")
        self.assertNoMatch(r"\b310\b")
        for forbidden in ("every_country", "every_state", "capital_scope", r"random_owned_\w+", "add_state_core", "load_focus_tree",
                          "create_country_leader", "kill_country_leader", "set_cosmetic_tag", "set_party_name"):
            self.assertNoMatch(r"\b%s\b" % forbidden)

    def test_tech_categories_and_modifiers_are_engine_keys(self):
        tags = "\n".join(text(p) for p in (MOD / "common/technology_tags").glob("*.txt"))
        for category in set(re.findall(r"category = (\w+)", self.script)):
            self.assertRegex(tags, r"(?m)^\s*%s\s*$" % category, category)
        modifiers = {key for _, _, values, _ in C.IDEAS.values() for key in values}
        # A modifier is accepted when the mod's other ideas already use it (this covers dynamic keys such as
        # <ideology>_drift that the documentation does not list by name), or when it is in this reviewed set,
        # which the read-only game documentation must list whenever it is available.
        other = "\n".join(text(p) for p in (MOD / "common/ideas").glob("*.txt") if p.name != "ac_ud_eru.txt")
        used = set(re.findall(r"(?m)^\s*(\w+) = -?[0-9.]+\s*$", other))
        reviewed = {"air_training_xp_gain_factor", "special_project_speed_factor", "compliance_growth_on_our_occupied_states",
                    "resistance_growth_on_our_occupied_states", "required_garrison_factor", "navy_submarine_detection_factor",
                    "convoy_escort_efficiency", "naval_damage_factor", "navy_org_factor", "industry_repair_factor",
                    "air_cas_efficiency"}
        if REFERENCE.exists():
            listed = set(re.findall(r"(?m)^## (\w+)\s*$", REFERENCE.read_text(encoding="utf-8", errors="replace")))
            self.assertEqual(set(), reviewed - listed)
        self.assertEqual(set(), modifiers - reviewed - used)

    # -- the AI default path -------------------------------------------------------------
    def test_ai_default_path_keeps_the_monarchy_and_starts_the_war_in_summer_2003(self):
        for first in (False, True):
            world = run_ai(own_weekly_first=first)
            eru = world.countries["ERU"]
            self.assertEqual([], world.regime_calls)
            self.assertTrue(world.flag(eru, "ERU_ud_course_crown"))
            self.assertFalse(world.flag(eru, "ERU_ud_course_constitution") or world.flag(eru, "ERU_ud_course_regency"))
            self.assertTrue(world.flag(eru, "ERU_ud_carried_over") and world.flag(eru, "ERU_ud_war_crown"))
            for era in ("skully", "ulysses", "coup", "stonehenge", "impact"):
                self.assertTrue(world.flag(eru, "ERU_ud_era_" + era), era)
            self.assertIn("ac_ucw_war_started", world.globals)
            self.assertTrue(world.grievance_log)
            self.assertGreaterEqual(min(value for _, value in world.grievance_log), 25)
            done = [f for f in eru.focuses if f.startswith("ERU_ud_")]
            self.assertGreater(len([f for f in done if f in world.trees[C.OPENING_TREE]]), 40)
            self.assertGreater(len([f for f in done if f in world.trees[C.WAR_TREE]]), 8)

    def test_war_starts_inside_the_provisional_summer_window(self):
        world = Sim("1991.1.1")
        world.run_until("2003.6.14")
        self.assertNotIn("ac_ucw_war_started", world.globals)
        start = None
        while world.today < day("2003.9.22"):
            world.run_until(world.today + 7)
            if "ac_ucw_war_started" in world.globals:
                start = world.today
                break
        self.assertIsNotNone(start)
        self.assertGreaterEqual(start, day("2003.6.21"))
        self.assertLess(start, day("2003.9.22"))
        self.assertGreaterEqual(min(v for _, v in world.grievance_log), 25)

    def test_weighted_random_ai_never_cuts_the_grievance_below_25(self):
        for seed in range(6):
            world = run_ai(seed)
            self.assertEqual([], world.regime_calls, seed)
            self.assertIn("ac_ucw_war_started", world.globals, seed)
            self.assertGreaterEqual(min(v for _, v in world.grievance_log), 25, seed)

    def test_player_paths_change_government_only_through_their_regime_effects(self):
        world = Sim("1993.6.1")
        eru = world.countries["ERU"]
        eru.ai = False
        for ident in world.trees[C.OPENING_TREE]:
            if ident.startswith("ERU_exp_"):
                eru.focuses.add(ident)
        for slug in ("crown_and_court", "palace_chancery", "privy_council_minutes", "succession_statute", "royal_progress",
                     "crowns_question", "path_constitution", "drafting_commission", "publish_the_minutes", "legalize_the_parties",
                     "free_press_law", "charter_written", "first_assembly_elections"):
            world.complete("ERU_ud_" + slug, "ERU")
        self.assertEqual(sorted(["set_politics", "set_popularities", "recruit_character", "promote_character"]),
                         sorted(k for _, k in world.regime_calls))
        self.assertFalse(world.focus_available("ERU_ud_path_regency", "ERU"))
        world.today = day("1999.12.8")
        world.tick()
        world.drain()
        world.tick()
        world.drain()
        self.assertTrue(world.flag(eru, "ERU_ud_war_assembly"))
        self.assertEqual(37, eru.variables["ac_ucw_grievance"])

    def test_regency_hands_the_new_decade_to_whoever_holds_the_seals(self):
        for returned, expected in ((False, "ERU_ud_war_regency"), (True, "ERU_ud_war_crown")):
            world = Sim("1999.12.8")
            eru = world.countries["ERU"]
            eru.ai = False
            eru.flags["ERU_ud_course_regency"] = None
            eru.flags["ERU_ud_regency_ordinance_done"] = None
            if returned:
                eru.flags["ERU_ud_return_the_seals_done"] = None
            world.tick()
            world.drain()
            self.assertTrue(world.flag(eru, expected), expected)
            self.assertEqual(45 if returned else 50, eru.variables["ac_ucw_grievance"])

    def test_unfinished_government_paths_fall_back_to_crown(self):
        for path in ("constitution", "regency"):
            for own_weekly_first in (False, True):
                with self.subTest(path=path, own_weekly_first=own_weekly_first):
                    world = Sim("1999.12.8", own_weekly_first=own_weekly_first)
                    eru = world.countries["ERU"]
                    eru.ai = False
                    eru.flags["ERU_ud_course_" + path] = None
                    world.tick()
                    world.tick()
                    self.assertTrue(world.flag(eru, "ERU_ud_war_crown"))
                    self.assertFalse(world.flag(eru, "ERU_ud_war_assembly"))
                    self.assertFalse(world.flag(eru, "ERU_ud_war_regency"))
                    self.assertEqual(45, eru.variables["ac_ucw_grievance"])
                    self.assertEqual([], world.regime_calls)

    def test_battery_umbrella_requires_live_control_and_ends_when_lost(self):
        ident = "ERU_ud_battery_umbrella_doctrine"
        spirit = "ERU_ud_battery_umbrella"
        ideas = mapping(mapping(load("common/ideas/ac_ud_eru.txt"))["ideas"])
        cancel = mapping(mapping(ideas["country"])[spirit])["cancel"]
        for state in ("pre_seizure", "not_operational", "live", "lost", "destroyed"):
            with self.subTest(state=state):
                world = Sim("2000.1.8")
                eru = world.countries["ERU"]
                world.tick()
                eru.flags["ERU_ucw_air_arm_done"] = None
                eru.focuses.add("ERU_ud_air_doctrine_board")
                world.controllers[310] = "ERU"
                world.globals.update(("ac_ucw_stonehenge_seized", "ac_ucw_stonehenge_operational"))
                if state == "pre_seizure":
                    world.globals.remove("ac_ucw_stonehenge_seized")
                elif state == "not_operational":
                    world.globals.remove("ac_ucw_stonehenge_operational")
                elif state == "lost":
                    world.controllers[310] = "SNS"
                elif state == "destroyed":
                    world.execute(world.effects["ac_ucw_destroy_stonehenge"], eru)
                self.assertEqual(state == "live", world.focus_available(ident, "ERU"))
                # Direct reward execution also tests conditions changing during completion.
                world.execute(mapping(world.focuses[ident])["completion_reward"], eru)
                self.assertEqual(state == "live", spirit in eru.ideas)
                self.assertEqual(state != "live", world.trigger(cancel, eru))
                # Old saves or already-completed focuses must lose an invalid bonus.
                eru.ideas[spirit] = None
                world.execute(world.own_weekly, eru)
                self.assertEqual(state == "live", spirit in eru.ideas)

    def test_earned_battery_umbrella_is_removed_on_recapture_or_destruction(self):
        for loss in ("recapture", "destruction", "inoperative"):
            with self.subTest(loss=loss):
                world = Sim("2000.1.8")
                eru = world.countries["ERU"]
                world.tick()
                eru.flags["ERU_ucw_air_arm_done"] = None
                eru.focuses.add("ERU_ud_air_doctrine_board")
                world.controllers[310] = "ERU"
                world.execute(world.effects["ac_ucw_seize_stonehenge"], eru)
                world.complete("ERU_ud_battery_umbrella_doctrine", "ERU")
                self.assertIn("ERU_ud_battery_umbrella", eru.ideas)
                if loss == "recapture":
                    world.controllers[310] = "SNS"
                elif loss == "destruction":
                    world.execute(world.effects["ac_ucw_destroy_stonehenge"], eru)
                else:
                    world.globals.remove("ac_ucw_stonehenge_operational")
                world.execute(world.own_weekly, eru)
                self.assertNotIn("ERU_ud_battery_umbrella", eru.ideas)

    def test_fiscal_prototype_runs_every_guarded_call(self):
        world = Sim("1993.6.1", fiscal=True)
        eru = world.countries["ERU"]
        world.execute([("if", "=", [("limit", "=", [("ac_econ_ready", "=", "yes")]), ("ac_econ_set_reconstruction", "=", "yes")])], eru)
        self.assertEqual(["ac_econ_set_reconstruction"], world.fiscal_calls)

    # -- generators ----------------------------------------------------------------------
    def test_build_and_owner_generators_check(self):
        for command in (["tools/usea_depth/eru/build.py", "--check"], ["tools/usea_expansion/build_content.py", "--check"],
                        ["tools/build_continental_war.py", "--check"]):
            result = subprocess.run([sys.executable, "-B"] + command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, " ".join(command) + "\n" + result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
