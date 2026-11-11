"""Static and offline checks for the Usea Depth partners package (README test checklist).

The AI simulation runs this package's real script inside the World harness from
tools/Test-ContinentalWar.py. It is an offline executor, not the HOI4 engine:
calls into other owners (the partner programme's bound/recalculate effects) are
recorded stubs, checked only for existence. Native acceptance remains under #8.
"""
from datetime import date
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / "tools"), str(ROOT / "tools/usea_expansion")]

from usea_depth import seams  # noqa: E402
from economy_script import parse, fields  # noqa: E402
import build  # noqa: E402
from content import BAND, BUDGET, BY_ID, COUNTRIES, FOCUSES, GATES, IDEAS, MARKER, PACKAGE, REGIMES  # noqa: E402
from narrative import all_events  # noqa: E402

MOD = ROOT / "mod/2985041246"
OWNED = {
    "focus": "common/national_focus/ac_ud_partners.txt",
    "events": "events/ac_ud_partners.txt",
    "ideas": "common/ideas/ac_ud_partners.txt",
    "effects": "common/scripted_effects/ac_ud_partners.txt",
    "triggers": "common/scripted_triggers/ac_ud_partners.txt",
    "characters": "common/characters/ac_ud_partners.txt",
    "gfx": "interface/ac_ud_partners.gfx",
    "loc": "localisation/english/ac_ud_partners_l_english.yml",
}
EXTERNAL_EFFECTS = {"ac_up_bound", "ac_up_recalculate"}
SCRIPT_KEYS = ("focus", "events", "ideas", "effects", "triggers", "characters")


def read(key):
    return (MOD / OWNED[key]).read_text(encoding="utf-8-sig")


def load(relative):
    return parse((MOD / relative).read_text(encoding="utf-8-sig"))


def mapping(nodes):
    return {key: value for key, _, value in nodes}


def localisation():
    keys = {}
    for path in sorted((MOD / "localisation/english").rglob("*.yml")):
        for key, value in re.findall(r'^\s*([\w.\-]+):\d*\s+"(.*)"\s*$', path.read_text(encoding="utf-8-sig"), re.M):
            keys[key] = value
    return keys


def ucw_module():
    spec = importlib.util.spec_from_file_location("ulysses_continental_war_harness", ROOT / "tools/Test-ContinentalWar.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CW = ucw_module()


class PartnersWorld(CW.World):
    """The Continental War harness with this package's focuses, events and effects applied."""

    def __init__(self, when="1991.1.1"):
        super().__init__(when)
        self.effects.update(mapping(load(OWNED["effects"])))
        self.triggers.update(mapping(load(OWNED["triggers"])))
        self.events.update({mapping(v)["id"]: (k, v) for k, _, v in load(OWNED["events"]) if k == "country_event"})
        self.shared = {mapping(v)["id"]: v for k, _, v in load(OWNED["focus"]) if k == "shared_focus"}
        self.characters, self.politics, self.global_writes, self.bonuses = set(), [], [], []
        self.current, self.bypassed = {}, {tag: set() for tag in COUNTRIES}
        for tag in COUNTRIES:
            # Stand-in for the partner owner's on_startup ac_up_initialize.
            self.countries[tag].flags["ac_up_initialized"] = None

    def trigger(self, nodes, country):
        rest, answers = [], []
        for node in nodes:
            key, _, value = node
            if key == "tag":
                answers.append(country.tag == value)
            elif key == "custom_trigger_tooltip":
                answers.append(self.trigger([n for n in value if n[0] != "tooltip"], country))
            elif key == "has_character":
                answers.append(value in self.characters)
            else:
                rest.append(node)
        return all(answers) and super().trigger(rest, country)

    def execute(self, nodes, country):
        run = []
        for node in nodes:
            key, _, value = node
            special = key in ("hidden_effect", "effect_tooltip", "add_tech_bonus", "set_politics", "set_popularities",
                              "recruit_character", "promote_character", "set_global_flag") or key in EXTERNAL_EFFECTS
            if not special:
                run.append(node)
                continue
            if run:
                super().execute(run, country)
                run = []
            if key == "hidden_effect":
                self.execute(value, country)
            elif key == "add_tech_bonus":
                self.bonuses.append((country.tag, fields(value)["category"]))
            elif key in ("set_politics", "set_popularities", "promote_character"):
                self.politics.append((country.tag, key, fields(value) if isinstance(value, list) else value))
            elif key == "recruit_character":
                self.characters.add(value)
            elif key == "set_global_flag":
                self.global_writes.append(value)
                super().execute([node], country)
        if run:
            super().execute(run, country)

    # A deterministic stand-in for AI focus choice: the highest ai_will_do factor wins.
    def done(self, tag):
        return self.countries[tag].focuses | self.bypassed[tag]

    def can_start(self, ident, tag):
        node, country = self.shared[ident], self.countries[tag]
        if country.capitulated and mapping(node).get("available_if_capitulated", "no") != "yes":
            return False
        finished = self.done(tag)
        for key, _, value in node:
            if key == "prerequisite" and not any(focus in finished for _, _, focus in value):
                return False
            if key == "mutually_exclusive" and any(focus in country.focuses for _, _, focus in value):
                return False
        return self.trigger(mapping(node)["available"], country)

    def ai_factor(self, ident):
        return float(fields(mapping(self.shared[ident])["ai_will_do"])["factor"])

    def finish(self, ident, tag):
        self.countries[tag].focuses.add(ident)
        self.execute(mapping(self.shared[ident])["completion_reward"], self.countries[tag])

    def focus_week(self):
        for tag in COUNTRIES:
            country = self.countries[tag]
            if tag in self.current:
                ident, due = self.current[tag]
                if self.today >= due:
                    del self.current[tag]
                    if self.can_start(ident, tag):
                        self.finish(ident, tag)
                continue
            for ident in (row.id for row in FOCUSES if row.tag == tag):
                node = mapping(self.shared[ident])
                if ident not in self.done(tag) and "bypass" in node and self.trigger(node["bypass"], country):
                    self.bypassed[tag].add(ident)
            options = [row.id for row in FOCUSES if row.tag == tag and row.id not in self.done(tag)
                       and self.ai_factor(row.id) > 0 and self.can_start(row.id, tag)]
            if options:
                ident = max(options, key=lambda i: (self.ai_factor(i), -BY_ID[i].order))
                self.current[tag] = (ident, self.today + 7 * int(mapping(self.shared[ident])["cost"]))

    def advance(self, until, partners=True):
        """Weekly ticks; returns the first day the war started, if it did."""
        started, lowest = None, None
        while self.today < CW.day(until):
            self.today += 7
            self.tick()
            if partners:
                self.focus_week()
            self.drain()
            eru = self.countries["ERU"].variables
            if "ac_ucw_calendar_started" in self.globals and "ac_ucw_grievance" in eru:
                lowest = eru["ac_ucw_grievance"] if lowest is None else min(lowest, eru["ac_ucw_grievance"])
            if started is None and "ac_ucw_war_started" in self.globals:
                started = self.today
        return started, lowest


class PartnersPackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loc = localisation()
        cls.own_loc = dict(re.findall(r'^\s*([\w.\-]+):\d*\s+"(.*)"\s*$', read("loc"), re.M))
        cls.texts = {key: read(key) for key in OWNED}
        cls.budget = json.loads((HERE / "budget.json").read_text(encoding="utf-8"))

    # Counts and imports --------------------------------------------------
    def test_counts_equal_budget_and_each_id_is_imported_once_in_its_own_marker(self):
        self.assertEqual(build.budget(), self.budget)
        self.assertEqual(BUDGET, self.budget["focuses"])
        self.assertEqual(sum(self.budget["focuses"].values()), sum(self.budget["trees"].values()))
        self.assertEqual(len(all_events()), self.budget["events"])
        defined = [mapping(v)["id"] for k, _, v in load(OWNED["focus"]) if k == "shared_focus"]
        self.assertEqual(sorted(BY_ID), sorted(defined))
        for tag in COUNTRIES:
            self.assertEqual(self.budget["focuses"][tag], sum(i.startswith(tag + "_ud_") for i in defined))
        imports = {}
        for path in sorted((MOD / "common/national_focus").glob("*.txt")):
            for ident in re.findall(r"(?m)^\s*shared_focus = (\w+)\s*$", path.read_text(encoding="utf-8-sig")):
                imports.setdefault(ident, []).append(path.name)
        for ident in BY_ID:
            self.assertEqual([BY_ID[ident].tag + ".txt"], imports.get(ident), ident)
        for tag in COUNTRIES:
            blocks = {name: ids for name, ids, _ in seams.import_blocks((MOD / "common/national_focus" / (tag + ".txt")).read_text(encoding="utf-8-sig"))}
            self.assertEqual(build.tree_ids(tag), blocks[MARKER])
            self.assertEqual([MARKER, seams.CAMPAIGNS], [n for n in blocks if n in (MARKER, seams.CAMPAIGNS)])
            tree = next(v for k, _, v in load("common/national_focus/%s.txt" % tag) if k == "focus_tree")
            self.assertEqual(COUNTRIES[tag]["tree"], mapping(tree)["id"])
            self.assertEqual(self.budget["trees"][COUNTRIES[tag]["tree"]], len(blocks[MARKER]))

    # Layout ----------------------------------------------------------------
    def test_nodes_sit_in_the_band_titles_fit_and_captions_never_overlap(self):
        positions = seams.tree_positions()
        gui = (MOD / "interface/nationalfocusview.gui").read_text(encoding="utf-8-sig")
        panel_w = int(re.search(r"continuous_focus_window.*?size = \{\s*width = (\d+)", gui, re.S)[1])
        for tag in COUNTRIES:
            tree = COUNTRIES[tag]["tree"]
            ids = build.tree_ids(tag)
            self.assertEqual([], seams.band_violations(positions[tree], ids, *BAND), tag)
            for a, b in combinations(sorted(positions[tree]), 2):
                (ax, ay), (bx, by) = positions[tree][a], positions[tree][b]
                self.assertFalse(abs(ax - bx) * 96 < 147 and abs(ay - by) * 160 < 54, (tree, a, b))
            source = (MOD / "common/national_focus" / (tag + ".txt")).read_text(encoding="utf-8-sig")
            panel_x = int(re.search(r"continuous_focus_position = \{ x = (\d+)", source)[1])
            self.assertGreater(min(positions[tree][i][0] for i in ids) * 96, panel_x + panel_w + 32, tag)
            outside = [i for i, (x, _) in positions[tree].items() if i not in ids and BAND[0] <= x <= BAND[1]]
            self.assertEqual([], outside, "Another owner's node sits inside the partners band")
        for row in FOCUSES:
            self.assertTrue(seams.title_fits(row.title), row.title)
            self.assertIn(row.cost, (5, 10), row.id)

    # Localisation ----------------------------------------------------------
    def test_localisation_is_complete_has_a_bom_and_labels_every_flag(self):
        self.assertTrue((MOD / OWNED["loc"]).read_bytes().startswith(b"\xef\xbb\xbfl_english:\n"))
        own = self.own_loc
        for row in FOCUSES:
            for key in (row.id, row.id + "_desc", row.id + "_done"):
                self.assertTrue(own.get(key), key)
        for ident in IDEAS:
            self.assertTrue(own.get(ident) and own.get(ident + "_desc"), ident)
        for event in all_events():
            ident = "ac_ud_up.%d" % event["n"]
            for suffix in [".t", ".d"] + ["." + "abc"[i] for i in range(len(event["options"]))]:
                self.assertTrue(own.get(ident + suffix), ident + suffix)
        for key in re.findall(r"\b(?:name|desc|title|tooltip)\s*=\s*([\w.]+)", "\n".join(self.texts[k] for k in SCRIPT_KEYS)):
            self.assertIn(key, self.loc, key)
        flags = set(re.findall(r"has_(?:country|global)_flag = (\w+)", "\n".join(self.texts[k] for k in SCRIPT_KEYS)))
        flags |= set(re.findall(r"set_country_flag = (\w+)", self.texts["focus"]))
        self.assertGreater(len(flags), 260)
        for flag in flags:
            self.assertTrue(self.loc.get(flag), "Unlabelled flag: " + flag)
        self.assertFalse(re.search(r"[“”‘’]", read("loc")))
        duplicates = [k for k in own if list(self.own_loc).count(k) > 1]
        self.assertEqual([], duplicates)

    # Art -------------------------------------------------------------------
    def test_icons_shines_portraits_and_pictures_resolve_to_mod_textures(self):
        sprites = dict(re.findall(r'name = "([^"]+)" texturefile = "([^"]+)"', self.texts["gfx"]))
        self.assertNotIn("shine_overlay", self.texts["gfx"])
        for row in FOCUSES:
            name = "GFX_ac_ud_focus_" + row.id
            self.assertEqual("gfx/AC_usea_depth/partners/focus/%s.dds" % row.id, sprites[name])
            self.assertEqual(sprites[name], sprites[name + "_shine"])
        for ident in IDEAS:
            self.assertIn("picture = ac_ud_" + ident, self.texts["ideas"])
            self.assertIn("GFX_idea_ac_ud_" + ident, sprites)
        for picture in re.findall(r"picture = (GFX_\w+)", self.texts["events"]):
            self.assertIn(picture, sprites)
        for portrait in re.findall(r'large = "(\w+)"', self.texts["characters"]):
            self.assertIn(portrait, sprites)
        for name, texture in sprites.items():
            self.assertTrue(name.startswith(("GFX_ac_ud_", "GFX_idea_ac_ud_")), name)
            self.assertTrue(texture.startswith("gfx/AC_usea_depth/partners/"), texture)
            self.assertTrue((MOD / texture).is_file(), texture)
        assets = json.loads((HERE / "assets.json").read_text(encoding="utf-8"))
        focus_hashes = [a["sha256"] for a in assets["assets"] if a["role"] == "original focus icon"]
        self.assertEqual(len(FOCUSES), len(set(focus_hashes)))
        self.assertEqual("Pillow 11.3.0", assets["renderer"])
        self.assertEqual(len(sprites) - len(FOCUSES), len(assets["assets"]))

    # Politics --------------------------------------------------------------
    def test_government_changes_only_in_regime_effects_with_ai_weight_zero(self):
        self.assertEqual([], seams.political_violations(self.texts["effects"]))
        for key in ("focus", "events", "ideas", "triggers", "characters"):
            self.assertIsNone(re.search(r"\bset_(politics|popularities)\b|add_popularity|set_party_name|create_country_leader", self.texts[key]), key)
        regime_names = re.findall(r"(?m)^(\w+) = \{", self.texts["effects"])
        self.assertEqual(sorted("ac_ud_partners_regime_" + slug for slug in REGIMES), sorted(regime_names))
        defined = re.findall(r"(?m)^(\w+_ud_\w+_office) = \{", self.texts["characters"])
        self.assertEqual(sorted(build.office(slug) for slug in REGIMES), sorted(defined))
        for slug, row in REGIMES.items():
            body = re.search(r"ac_ud_partners_regime_%s = \{(.*?)\n\}" % slug, self.texts["effects"], re.S)[1]
            self.assertIn("ruling_party = " + row["party"], body)
            self.assertIn("recruit_character = " + build.office(slug), body)
            self.assertIn("ideology = " + row["sub"], body)
            self.assertEqual(row["name"], self.own_loc[build.office(slug)])
            # An office, never a personal name.
            self.assertRegex(self.own_loc[build.office(slug)], r"\b(Council|Cabinet|Board|Directorate|Presidium|Committee)\b")
        for row in REGIMES.values():
            # The country keeps a name under every party a path can install.
            for suffix in ("", "_DEF"):
                self.assertTrue(self.loc.get("%s_%s%s" % (row["tag"], row["party"], suffix)), (row["tag"], row["party"], suffix))
        callers = [row for row in FOCUSES if any(t.startswith("regime:") for t in row.reward)]
        self.assertEqual(len(REGIMES), len(callers))
        for tag in COUNTRIES:
            self.assertIn(sum(row.tag == tag for row in callers), (2, 3), tag)
        for row in callers:
            self.assertEqual(0, row.ai, row.id)
            # The whole path that leads there is player-only.
            chain = [row]
            while chain[-1].prerequisites:
                chain.append(BY_ID[chain[-1].prerequisites[0][0]])
            for step in chain[:-1]:
                self.assertEqual(0, step.ai, step.id)
        shared = {mapping(v)["id"]: v for k, _, v in load(OWNED["focus"]) if k == "shared_focus"}
        for ident, node in shared.items():
            reward = repr(mapping(node)["completion_reward"])
            if "ac_ud_partners_regime_" in reward:
                self.assertEqual("0", fields(mapping(node)["ai_will_do"])["factor"], ident)
        for kind, _, event in load(OWNED["events"]):
            if kind != "country_event":
                continue
            for key, _, option in event:
                if key == "option":
                    self.assertNotIn("ac_ud_partners_regime_", repr(option), mapping(event)["id"])
        self.assertIsNone(re.search(r"has_popularity|party_popularity", "\n".join(self.texts[k] for k in SCRIPT_KEYS)))

    # The war still starts --------------------------------------------------
    def test_ai_default_path_keeps_the_war_in_summer_2003(self):
        baseline = CW.World("1991.1.1")
        base_started = None
        while baseline.today < CW.day("2003.10.1"):
            baseline.weeks(1)
            if base_started is None and "ac_ucw_war_started" in baseline.globals:
                base_started = baseline.today
        world = PartnersWorld("1991.1.1")
        world.advance("2003.6.1")
        # Before the war the AI has finished every pre-war focus it would take: nothing stalls it.
        for tag in COUNTRIES:
            waiting = [row.id for row in FOCUSES if row.tag == tag and row.ai > 0 and row.id not in world.done(tag)
                       and world.can_start(row.id, tag)]
            self.assertEqual([], waiting, tag)
        started, lowest = world.advance("2003.10.1")
        self.assertIsNotNone(started, "The Continental War did not start")
        self.assertEqual(base_started, started, "Partner content moved the AI war start")
        self.assertTrue(CW.day("2003.6.21") <= started <= CW.day("2003.9.22"), date.fromordinal(started))
        self.assertGreaterEqual(lowest, 25)
        self.assertEqual([], world.politics, "AI partners changed government")
        self.assertEqual([], [flag for flag in world.global_writes if flag.startswith("ac_ucw_") and flag not in baseline.globals])
        for tag in COUNTRIES:
            self.assertTrue(world.at_war("ERU", tag), tag)
            completed = world.countries[tag].focuses
            self.assertGreaterEqual(len(completed), 20, tag)
            self.assertFalse([i for i in completed if BY_ID[i].ai == 0], tag)
            self.assertTrue(any(BY_ID[i].slug.startswith(("keep_the", "keep_")) for i in completed), tag)
        self.assertIn("SNS_ud_invasion_summer", world.countries["SNS"].focuses | {world.current.get("SNS", ("",))[0]})
        self.assertTrue(world.bonuses)

    def test_player_paths_install_unnamed_offices_and_outcome_lanes_follow_the_war(self):
        world = PartnersWorld("1991.1.1")
        sns = world.countries["SNS"]
        sns.ai = False
        for slug in ("national_question", "charter_movement", "charter_drafting", "charter_assembly"):
            ident = "SNS_ud_" + slug
            self.assertTrue(world.can_start(ident, "SNS"), ident)
            world.finish(ident, "SNS")
        self.assertIn(("SNS", "set_politics", {"ruling_party": "democratic", "elections_allowed": "yes"}), world.politics)
        self.assertIn("SNS_ud_charter_presidium_office", world.characters)
        self.assertFalse(world.can_start("SNS_ud_keep_the_administration", "SNS"))
        world.drain()
        # Outcome lanes read the Continental War's flags and never write them.
        world.today = CW.day("2005.9.20")
        sns.focuses |= {"SNS_ud_keep_the_roads_open"}
        for flag, lane in (("ac_ucw_outcome_isaf_victory", "liberation_day"), ("ac_ucw_outcome_erusean_victory", "erusean_settlement"),
                           ("ac_ucw_outcome_stalemate", "armistice_watch")):
            world.globals.add(flag)
            self.assertTrue(world.can_start("SNS_ud_" + lane, "SNS"), lane)
            others = [o for o in ("liberation_day", "erusean_settlement", "armistice_watch") if o != lane]
            self.assertFalse(any(world.can_start("SNS_ud_" + o, "SNS") for o in others), lane)
            world.globals.discard(flag)
        world.globals.add("ac_ucw_war_started")
        sns.capitulated = True
        self.assertFalse(world.trigger([("custom_trigger_tooltip", "=", [("tooltip", "=", "x")] + parse(GATES["free"][0]))], sns))
        self.assertTrue(world.trigger(parse(GATES["occupied"][0]), sns))

    def assert_political_choices_exclusive(self, world, tag, openers):
        for chosen in openers:
            world.countries[tag].focuses.clear()
            for group in BY_ID[chosen].prerequisites:
                world.countries[tag].focuses.update(group)
            self.assertTrue(world.can_start(chosen, tag), chosen)
            world.finish(chosen, tag)
            for other in openers:
                if other != chosen:
                    self.assertFalse(world.can_start(other, tag), (chosen, other))

    def test_every_political_opener_excludes_every_other_choice(self):
        for tag in COUNTRIES:
            openers = [row.id for row in FOCUSES if row.tag == tag and row.y == 1 and row.x <= 40]
            self.assertEqual(4 if tag in ("SNS", "AMB") else 3, len(openers))
            self.assert_political_choices_exclusive(PartnersWorld(), tag, openers)
            # Deliberately remove reform-to-reform edges, reproducing the review defect.
            broken = PartnersWorld()
            reforms = set(openers[1:])
            for ident in reforms:
                broken.shared[ident] = [(k, op, [n for n in value if n[2] not in reforms]
                                         if k == "mutually_exclusive" else value)
                                        for k, op, value in broken.shared[ident]]
            with self.assertRaises(AssertionError):
                self.assert_political_choices_exclusive(broken, tag, openers)

    def occupation_world(self, prerequisite="coup_courts"):
        world = PartnersWorld("2004.1.1")
        world.countries["SNS"].capitulated = True
        world.countries["SNS"].focuses.add("SNS_ud_" + prerequisite)
        world.globals.add("ac_ucw_war_started")
        return world

    def assert_occupation_chain_reachable(self, world):
        for slug in ("invasion_summer", "quiet_ministries", "records_into_hiding", "exile_ledger"):
            ident = "SNS_ud_" + slug
            self.assertTrue(world.can_start(ident, "SNS"), ident)
            world.finish(ident, "SNS")
        self.assertFalse(world.can_start("SNS_ud_engineers_families", "SNS"))
        world.globals.add("ac_ucw_brief_engineers")
        self.assertTrue(world.can_start("SNS_ud_engineers_families", "SNS"))
        world.finish("SNS_ud_engineers_families", "SNS")

    def test_occupation_chain_after_capitulation_and_missing_setting_mutations(self):
        # Each pre-war route may be complete while the invasion focus is unfinished.
        for prerequisite in ("open_reception_centres", "transit_only", "coup_courts", "coup_cordon"):
            self.assert_occupation_chain_reachable(self.occupation_world(prerequisite))
        for slug in ("invasion_summer", "quiet_ministries", "records_into_hiding", "engineers_families", "exile_ledger"):
            broken = self.occupation_world()
            ident = "SNS_ud_" + slug
            broken.shared[ident] = [n for n in broken.shared[ident] if n[0] != "available_if_capitulated"]
            with self.assertRaises(AssertionError, msg=ident):
                self.assert_occupation_chain_reachable(broken)

    def test_capitulation_default_and_scripted_gates_still_apply(self):
        world = PartnersWorld("2004.1.1")
        ident = "SNS_ud_national_question"
        self.assertTrue(world.can_start(ident, "SNS"))
        world.countries["SNS"].capitulated = True
        self.assertFalse(world.can_start(ident, "SNS"))
        world.shared[ident].append(("available_if_capitulated", "=", "no"))
        self.assertFalse(world.can_start(ident, "SNS"))
        world.shared[ident][-1] = ("available_if_capitulated", "=", "yes")
        self.assertTrue(world.can_start(ident, "SNS"))
        self.assertFalse(world.can_start("SNS_ud_quiet_ministries", "SNS"), "Prerequisite still required")
        world.countries["SNS"].focuses.add("SNS_ud_invasion_summer")
        self.assertFalse(world.can_start("SNS_ud_quiet_ministries", "SNS"), "War gate still required")
        world.globals.add("ac_ucw_war_started")
        self.assertTrue(world.can_start("SNS_ud_quiet_ministries", "SNS"))
        self.assertFalse(world.can_start("SNS_ud_free_districts", "SNS"))
        world.countries["SNS"].capitulated = False
        self.assertFalse(world.can_start("SNS_ud_quiet_ministries", "SNS"), "Occupation gate still required")
        world.globals.add("ac_ucw_stonehenge_seized")
        self.assertTrue(world.can_start("SNS_ud_quiet_ministries", "SNS"))

    # Guards ----------------------------------------------------------------
    def test_fiscal_guards_banned_effects_and_continental_war_flags(self):
        everything = "\n".join(self.texts[k] for k in SCRIPT_KEYS)
        for key in SCRIPT_KEYS:
            self.assertEqual([], seams.banned_uses(self.texts[key]), key)
        self.assertIsNone(re.search(r"(set|clr)_(global|country)_flag = ac_ucw_", everything))
        self.assertNotIn("ac_ucw_grievance", everything)
        self.assertNotIn("ac_ucw_country_start", everything)
        self.assertNotIn("ac_ucw_pressure", everything)
        for match in re.finditer(r"\bac_econ_\w+", everything):
            preceding = everything[max(0, match.start() - 200):match.start()]
            self.assertIn("ac_econ_ready = yes", preceding, match[0])
        # No state is scoped or mapped: Stonehenge (state 310) is only read through the ac_ucw owner.
        self.assertIsNone(re.search(r"(?m)^\s*\d{1,4} = \{", everything))
        effects = r"\b(declare_war_on|add_to_faction|create_faction|puppet|annex_country|release|release_puppet|add_state_claim|set_capital|add_core_of|transfer_state|set_cosmetic_tag)\s*="
        self.assertIsNone(re.search(effects, everything))
        for effect in set(re.findall(r"\b(ac_up_\w+) = yes", everything)):
            self.assertIn(effect, EXTERNAL_EFFECTS)
        owner = (MOD / "common/scripted_effects/ac_usean_partners.txt").read_text(encoding="utf-8-sig")
        for effect in EXTERNAL_EFFECTS:
            self.assertRegex(owner, r"(?m)^%s = \{" % effect)

    def test_canon_gates_and_long_form_events(self):
        self.assertEqual({"skully": "date > 1995.12.30", "warn": "date > 1996.4.19", "coup": "date > 1997.5.29",
                          "henge": "date > 1998.6.18", "impact": "date > 1999.7.7", "refugee": "date > 2000.4.20"},
                         {k: GATES[k][0] for k in ("skully", "warn", "coup", "henge", "impact", "refugee")})
        anchored = {"SNS_ud_skully_islands_watch": "skully", "SNS_ud_read_the_warning": "warn", "SNS_ud_coup_night": "coup",
                    "SNS_ud_battery_completed": "henge", "SNS_ud_impact_night": "impact", "SNS_ud_refugee_question": "refugee",
                    "SNS_ud_invasion_summer": "war", "SNS_ud_liberation_day": "liberated"}
        for ident, gate in anchored.items():
            self.assertIn(gate, BY_ID[ident].gates, ident)
        events = all_events()
        self.assertEqual(list(range(1, 53)), [e["n"] for e in events])
        self.assertLessEqual(abs(len(events) - len(FOCUSES) / 5), 2)
        for event in events:
            text = self.own_loc["ac_ud_up.%d.d" % event["n"]].replace("\\n", "\n")
            self.assertEqual([], seams.event_problems(text), event["n"])
            self.assertGreaterEqual(len(text.rsplit("\n\n", 1)[0].split()), 200, event["n"])
            self.assertTrue(all(ord(c) < 127 for c in text), event["n"])
            self.assertGreaterEqual(len(event["options"]), 2)
            if event["layer"] == "Official":
                self.assertRegex(event["citation"], r"ACES Chronicle, (\d{4} / (\d\d\.\d\d|SUMMER))")
        prose = "\n".join(v for k, v in self.own_loc.items())
        # No Megalith or Stonehenge construction dates and no invented Stonehenge chronology.
        self.assertNotIn("Megalith", prose)
        for sentence in re.split(r"(?<=[.!?])\s", prose):
            if re.search(r"\b(construct|built|building began|groundbreaking)", sentence, re.I) and re.search(r"Stonehenge|battery|railgun", sentence, re.I):
                self.assertIsNone(re.search(r"\b(19|20)\d\d\b", sentence), sentence)
        # No invented impact geography: where fragments fell, what was spared, or compass bearings between countries.
        for phrase in ("fragment field", "fell where they fell", "spared", "fell far", "fell on", "struck the town", "lost its water works"):
            self.assertNotIn(phrase, prose.lower(), phrase)
        self.assertIsNone(re.search(r"\b(north|south|east|west)(ward|wards)?\b", prose, re.I))
        for year in re.findall(r"\b(199\d|200\d)\b", prose):
            self.assertIn(year, {"1991", "1995", "1996", "1997", "1998", "1999", "2000", "2003", "2004", "2005"}, year)

    def test_event_titles_fit_the_event_window(self):
        sys.path.insert(0, str(ROOT / "tools/event_style"))
        from event_style import review
        tree = review.load(MOD / "interface/eventwindow.gui")
        controls = review.named(tree)
        path = ("EventWindow", "top_Window", "Title")
        for event in all_events():
            key = "ac_ud_up.%d.t" % event["n"]
            metrics = review.metrics(event["title"], controls[path], review.horizontal_parents(controls, path))
            self.assertFalse(metrics["clipped"], key)
            self.assertFalse(metrics["missing_glyphs"], key)

    def test_generators_are_consistent(self):
        commands = [
            ([sys.executable, "-B", str(HERE / "build.py"), "--check"], ROOT),
            ([sys.executable, "-B", str(HERE / "build_art.py"), "--check"], ROOT),
            ([sys.executable, "-B", "build.py", "--check"], ROOT / "tools/usean_partners"),
        ]
        for command, cwd in commands:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
