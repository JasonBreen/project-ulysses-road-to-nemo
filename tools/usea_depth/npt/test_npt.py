"""Static checks for the North Point Usea Depth package (README test checklist).

Offline only: these read the shipped scripts and textures. They are not the HOI4
engine and say nothing about native parsing, AI behaviour or in-game layout.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from itertools import combinations
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE))
from usea_depth import seams  # noqa: E402
from usea_expansion.script import parse, get, walk  # noqa: E402
import content as c  # noqa: E402
import narrative as n  # noqa: E402

MOD = seams.MOD
OWN = {
    "focus": "common/national_focus/ac_ud_npt.txt",
    "events": "events/ac_ud_npt.txt",
    "ideas": "common/ideas/ac_ud_npt.txt",
    "effects": "common/scripted_effects/ac_ud_npt.txt",
    "characters": "common/characters/ac_ud_npt.txt",
    "gfx": "interface/ac_ud_npt.gfx",
}
LOC = MOD / "localisation/english/ac_ud_npt_l_english.yml"
KEY = re.compile(r'^\s*([\w.]+):\d*\s+"((?:\\.|[^"\\])*)"', re.M)
FISCAL = re.compile(r"\bac_econ_\w+\s*=\s*yes")
# Scripted effects defined outside the package that its scripts may call.
FOREIGN_EFFECTS = {"ac_ucw_bound", "ac_econ_refresh_budget", "ac_econ_pay_programme"}


def text(key):
    return (MOD / OWN[key]).read_text(encoding="utf-8-sig")


def own_text():
    return "\n".join(text(k) for k in OWN)


def mapping(nodes):
    return {k: v for k, _, v in nodes}


def shared_focuses():
    return {get(v, "id"): v for k, _, v in parse(text("focus")) if k == "shared_focus"}


def focus_refs(nodes, key):
    return [[ref for k, _, ref in group if k == "focus"] for k, _, group in nodes if k == key]


def localisation():
    return dict(KEY.findall(LOC.read_text(encoding="utf-8-sig")))


def all_localisation_keys():
    keys = set()
    for path in (MOD / "localisation").rglob("*.yml"):
        keys.update(k for k, _ in KEY.findall(path.read_text(encoding="utf-8-sig")))
    return keys


def strip_guarded_fiscal(source):
    """Remove every if-block whose limit is exactly the economy guard."""
    guard = re.compile(r"if\s*=\s*\{\s*limit\s*=\s*\{\s*ac_econ_ready\s*=\s*yes\s*\}")
    while True:
        match = guard.search(source)
        if not match:
            return source
        depth, cursor = 1, source.index("{", match.start()) + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(source[cursor], 0)
            cursor += 1
        source = source[:match.start()] + source[cursor:]


def ai_factor(node):
    ai = get(node, "ai_will_do", [])
    return float(get(ai, "factor", "1")), [v for k, _, v in ai if k == "modifier"]


class Budget(unittest.TestCase):
    def test_counts_equal_budget_and_release_plan(self):
        budget = json.loads((HERE / "budget.json").read_text(encoding="utf-8"))
        focuses = shared_focuses()
        events = [get(v, "id") for k, _, v in parse(text("events")) if k == "country_event"]
        self.assertEqual({"package": "npt", "marker": "USEA DEPTH NORTH POINT", "focuses": {"NPT": len(focuses)},
                          "trees": {"npt_pre_continental_war_focus": len(focuses)}, "events": len(events)}, budget)
        self.assertEqual(len(c.FOCUSES), len(focuses))
        self.assertGreaterEqual(len(focuses), 90)
        plan = json.loads((ROOT / "tools/overhaul/release_plan.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(["NPT"], plan["approved_expansions"]["usea_depth"]["packages"]["npt"]["tags"])
        self.assertTrue(all(i.startswith("NPT_ud_") for i in focuses))

    def test_every_id_is_imported_exactly_once_inside_the_marker(self):
        ids = list(shared_focuses())
        wrapper = (seams.FOCUS / "NPT.txt").read_text(encoding="utf-8-sig")
        blocks = {name: found for name, found, _ in seams.import_blocks(wrapper)}
        self.assertEqual(ids, blocks[c.MARKER])
        for path in seams.FOCUS.glob("*.txt"):
            source = path.read_text(encoding="utf-8-sig")
            imports = re.findall(r"shared_focus\s*=\s*(NPT_ud_\w+)", source)
            if path.name == "NPT.txt":
                self.assertEqual(Counter(ids), Counter(imports))
            else:
                self.assertEqual([], imports, path.name)
        # Shared-focus chaining must not pull the package into any other tree.
        for tree, positions in seams.tree_positions().items():
            found = {i for i in positions if i.startswith("NPT_ud_")}
            self.assertEqual(set(ids) if tree == c.TREE else set(), found, tree)

    def test_new_files_do_not_use_counted_prefixes(self):
        for relative in list(OWN.values()) + ["localisation/english/ac_ud_npt_l_english.yml"]:
            self.assertFalse(Path(relative).name.startswith(("ERU", "FCU", "NPT", "REC", "YUK", "ac_ucw")), relative)


class Layout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.positions = seams.tree_positions()[c.TREE]

    def test_nodes_sit_inside_the_band(self):
        self.assertEqual([], seams.band_violations(self.positions, list(shared_focuses()), *c.BAND))

    def test_titles_fit_and_no_captions_overlap(self):
        loc = localisation()
        for ident in shared_focuses():
            self.assertTrue(seams.title_fits(loc[ident]), ident)
        overlaps = [(a, b) for a, b in combinations(sorted(self.positions), 2)
                    if abs(self.positions[a][0] - self.positions[b][0]) * 96 < 147
                    and abs(self.positions[a][1] - self.positions[b][1]) * 160 < 54]
        self.assertEqual([], overlaps)

    def test_prerequisites_resolve_above_and_exclusions_are_mutual(self):
        own = shared_focuses()
        existing = set(seams.tree_positions()[c.TREE])
        for ident, node in own.items():
            for group in focus_refs(node, "prerequisite"):
                for ref in group:
                    self.assertIn(ref, existing, (ident, ref))
                    self.assertLess(self.positions[ref][1], self.positions[ident][1], (ident, ref))
            for group in focus_refs(node, "mutually_exclusive"):
                for ref in group:
                    self.assertIn(ident, sum(focus_refs(own[ref], "mutually_exclusive"), []), (ident, ref))

    def test_costs_and_era_gates(self):
        for ident, node in shared_focuses().items():
            self.assertIn(get(node, "cost"), ("5", "10"), ident)
        source = text("focus")
        for year in re.findall(r"\bdate\s*[<>]=?\s*(\d{4})\.", source):
            self.assertTrue(1991 <= int(year) <= 2005, year)
        gates = {c.ident(f.slug): f.available for f in c.FOCUSES}
        # Official anchors are date gates that open on the Chronicle day.
        self.assertIn("date > 1996.4.19", gates["NPT_ud_sky_announcement"])
        self.assertIn("date > 1997.5.29", gates["NPT_ud_coup_across_the_water"])
        self.assertIn("date > 1998.6.18", gates["NPT_ud_fragment_forecasts"])
        self.assertIn("date > 1999.7.7", gates["NPT_ud_after_the_fragments"])
        self.assertIn("date > 2000.4.20", gates["NPT_ud_boats_from_the_south"])
        # 1990s-only shelter work closes at the impact and before the calendar hand-off.
        for f in c.FOCUSES:
            if f.section == "shelters" and f.slug not in ("harbour_garrisons",):
                self.assertIn("date < 1999", f.available, f.slug)
            if f.section == "shelters" and f.slug not in ("sky_announcement", "harbour_garrisons"):
                self.assertIn("NOT = { has_global_flag = ac_ucw_calendar_started }", f.available, f.slug)


class ShelterReadiness(unittest.TestCase):
    """Evaluate only readiness effects, not the HOI4 runtime or other rewards."""

    def readiness(self, rewards, initial=0):
        effects = mapping(parse(text("effects")))
        value = initial

        def apply(nodes):
            nonlocal value
            for key, _, body in nodes:
                if key in effects:
                    apply(effects[key])
                elif key in ("set_variable", "add_to_variable"):
                    amount = get(body, "NPT_ud_shelter_readiness")
                    if amount is not None:
                        value = int(amount) if key == "set_variable" else value + int(amount)
                elif key == "clamp_variable" and get(body, "var") == "NPT_ud_shelter_readiness":
                    value = max(int(get(body, "min")), min(int(get(body, "max")), value))

        for reward in rewards:
            apply(reward)
        return value

    def test_both_completion_orders_preserve_readiness(self):
        focuses = shared_focuses()
        sky = get(focuses["NPT_ud_sky_announcement"], "completion_reward")
        council = get(focuses["NPT_ud_council_emergency_powers"], "completion_reward")
        for initial in (0, 3, 11, 12):
            for order in ((sky, council), (council, sky)):
                with self.subTest(initial=initial, order=order):
                    self.assertEqual(min(initial + 2, 12), self.readiness(order, initial))

    def test_detects_the_original_overwrite(self):
        council = get(shared_focuses()["NPT_ud_council_emergency_powers"], "completion_reward")
        broken_sky = parse("set_variable = { NPT_ud_shelter_readiness = 1 }")
        self.assertEqual(2, self.readiness((broken_sky, council)))
        self.assertNotEqual(2, self.readiness((council, broken_sky)))


class Localisation(unittest.TestCase):
    def test_complete_with_bom_and_no_duplicates(self):
        data = LOC.read_bytes()
        self.assertTrue(data.startswith(b"\xef\xbb\xbf"))
        keys = [k for k, _ in KEY.findall(data.decode("utf-8-sig"))]
        self.assertEqual(len(keys), len(set(keys)))
        others = set()
        for path in (MOD / "localisation").rglob("*.yml"):
            if path != LOC:
                others.update(k for k, _ in KEY.findall(path.read_text(encoding="utf-8-sig")))
        self.assertEqual(set(), set(keys) & others)
        loc = localisation()
        required = set()
        for ident in shared_focuses():
            required |= {ident, ident + "_desc"}
        for k, _, v in parse(text("events")):
            if k == "country_event":
                required |= {get(v, "title"), get(v, "desc")} | {get(o, "name") for kk, _, o in v if kk == "option"}
        for idea in c.IDEAS:
            required |= {idea.ident, idea.ident + "_desc"}
        for office in c.OFFICES:
            required |= {"NPT_ud_%s_office" % office.slug, "NPT_ud_%s_office_desc" % office.slug}
        self.assertEqual(set(), required - set(loc))

    def test_every_flag_and_variable_has_a_readable_label(self):
        keys = all_localisation_keys()
        source = own_text()
        flags = set(re.findall(r"\b(?:has|set|clr)_(?:country|global)_flag\s*=\s*(\w+)", source))
        variables = set(re.findall(r"\b(?:check_variable|set_variable|add_to_variable|has_variable)\s*=\s*\{?\s*(?:var\s*=\s*)?(\w+)", source))
        variables |= set(re.findall(r"has_variable\s*=\s*(\w+)", source))
        for name in flags | {v for v in variables if v.startswith("NPT_ud_")}:
            self.assertIn(name, keys, name)

    def test_text_is_plain_ascii_with_long_descriptions(self):
        loc = localisation()
        for key, value in loc.items():
            visible = re.sub("§.", "", value)
            self.assertTrue(all(ord(ch) < 128 for ch in visible), key)
            self.assertNotRegex(value, "[“”‘’]", key)
        for ident in shared_focuses():
            desc = loc[ident + "_desc"]
            self.assertGreaterEqual(len(desc.split()), 45, ident)
            self.assertRegex(desc, r"(Provisional gameplay|Mod provenance|Official)", ident)


class Events(unittest.TestCase):
    def test_long_form_text_and_layer_line(self):
        loc = localisation()
        events = [v for k, _, v in parse(text("events")) if k == "country_event"]
        self.assertEqual(len(n.EVENTS), len(events))
        self.assertGreaterEqual(len(events) * 5, len(c.FOCUSES) - 5, "about one event per five focuses")
        for event in events:
            body = loc[get(event, "desc")].replace("\\n", "\n").replace('\\"', '"')
            self.assertEqual([], seams.event_problems(body), get(event, "id"))
            self.assertTrue(get(event, "picture").startswith("GFX_ac_ud_npt_event_"))
            self.assertEqual("yes", get(event, "is_triggered_only"))
        # Branch openers, political turns and era transitions run well past the minimum.
        for number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 19, 23):
            self.assertGreaterEqual(len(" ".join(n.EVENTS[number].paragraphs).split()), 205, number)

    def test_each_event_is_fired_by_exactly_one_focus(self):
        fired = Counter(re.findall(r"country_event\s*=\s*\{\s*id\s*=\s*(ac_ud_npt\.\d+)", text("focus")))
        defined = {get(v, "id") for k, _, v in parse(text("events")) if k == "country_event"}
        self.assertEqual(defined, set(fired))
        self.assertEqual({1}, set(fired.values()))
        self.assertNotIn("ac_ud_npt.", text("effects"))

    def test_official_events_cite_the_chronicle(self):
        for number, date in ((12, "1996 / 04.20"), (13, "1997 / 05.30"), (14, "1998 / 06.19"), (16, "1999 / 07.08"), (17, "2000 / 04.21")):
            self.assertEqual("Official", n.EVENTS[number].layer)
            self.assertIn("ACES Chronicle, " + date, n.EVENTS[number].cite)


class Art(unittest.TestCase):
    def test_icons_and_shines_resolve_to_unique_mod_textures(self):
        sprites = dict(re.findall(r'name\s*=\s*"(GFX_\w+)"\s*texturefile\s*=\s*"([^"]+)"', text("gfx")))
        hashes = {}
        for ident, node in shared_focuses().items():
            icon = get(node, "icon")
            self.assertEqual("GFX_ac_ud_focus_" + ident, icon)
            self.assertEqual(sprites[icon], sprites[icon + "_shine"])
            path = MOD / sprites[icon]
            self.assertTrue(sprites[icon].startswith("gfx/AC_usea_depth/npt/focus/"), icon)
            with Image.open(path) as image:
                self.assertEqual((96, 96), image.size)
            hashes.setdefault(hashlib.sha256(path.read_bytes()).hexdigest(), []).append(ident)
        self.assertEqual([], [v for v in hashes.values() if len(v) > 1])
        self.assertNotIn("shine_overlay", text("gfx"))
        for name, texture in sprites.items():
            self.assertTrue(texture.startswith("gfx/AC_usea_depth/npt/"), name)
            self.assertTrue((MOD / texture).is_file(), texture)

    def test_ideas_portraits_and_event_pictures_use_package_sprites(self):
        sprites = dict(re.findall(r'name\s*=\s*"(GFX_\w+)"\s*texturefile\s*=\s*"([^"]+)"', text("gfx")))
        ideas = mapping(mapping(parse(text("ideas")))["ideas"])["country"]
        self.assertEqual({i.ident for i in c.IDEAS}, {k for k, _, _ in ideas})
        for name, _, body in ideas:
            self.assertIn("GFX_idea_" + get(body, "picture"), sprites, name)
        added = set(re.findall(r"\badd_ideas\s*=\s*(\w+)|add_idea\s*=\s*(\w+)", text("focus")))
        for pair in added:
            idea = next(x for x in pair if x)
            self.assertIn(idea, {i.ident for i in c.IDEAS}, idea)
        for _, _, body in parse(text("characters"))[0][2]:
            large = get(get(get(body, "portraits"), "civilian"), "large").strip('"')
            self.assertIn(large, sprites)
        for k, _, v in parse(text("events")):
            if k == "country_event":
                with Image.open(MOD / sprites[get(v, "picture")]) as image:
                    self.assertLessEqual(image.size, (215, 181))

    def test_manifest_matches_textures(self):
        rows = json.loads((HERE / "assets.json").read_text(encoding="utf-8"))["assets"]
        self.assertEqual(len(c.FOCUSES) + len(c.IDEAS) + len(c.OFFICES) + len(n.PICTURES), len(rows))
        for row in rows:
            path = ROOT / row["file"]
            self.assertEqual(row["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), row["file"])


class Politics(unittest.TestCase):
    def test_government_changes_only_in_regime_effects(self):
        for key in OWN:
            self.assertEqual([], seams.political_violations(text(key)), key)
        regimes = re.findall(r"^(ac_ud_npt_regime_\w+)\s*=", text("effects"), re.M)
        self.assertEqual(["ac_ud_npt_regime_parliament", "ac_ud_npt_regime_directorate"], regimes)
        for name in regimes:
            body = mapping(parse(text("effects")))[name]
            self.assertIn("promote_character", [k for k, _, _ in body])
        self.assertNotRegex(own_text(), r"\b(create_country_leader|kill_country_leader|retire_country_leader|add_country_leader_role)\b")

    def test_every_focus_or_option_reaching_a_regime_has_ai_zero(self):
        events = {get(v, "id"): v for k, _, v in parse(text("events")) if k == "country_event"}
        for k, _, event in parse(text("events")):
            for kk, _, option in event if k == "country_event" else []:
                if kk == "option" and "ac_ud_npt_regime_" in json.dumps(option):
                    self.assertEqual("0", get(get(option, "ai_chance"), "factor"))
        reaching = []
        for ident, node in shared_focuses().items():
            reward = json.dumps(get(node, "completion_reward"))
            fired = re.findall(r'"(ac_ud_npt\.\d+)"', reward)
            if "ac_ud_npt_regime_" in reward or any("ac_ud_npt_regime_" in json.dumps(events[e]) for e in fired):
                reaching.append(ident)
                self.assertEqual((0.0, []), ai_factor(node), ident)
        self.assertEqual(["NPT_ud_parliament_of_islands", "NPT_ud_readiness_directorate"], reaching)

    def test_the_ai_path_keeps_the_1991_government(self):
        # Walk the tree with only the focuses the AI can pick (factor above zero):
        # nothing it can reach changes the ruling party.
        own = shared_focuses()
        done = {"NPT_1991_elections", "NPT_old_guard_mandate", "NPT_drp_mandate", "NPT_reformist_mandate",
                "NPT_national_defense_review", "NPT_host_isaf"}
        changed = True
        while changed:
            changed = False
            for ident, node in own.items():
                factor, modifiers = ai_factor(node)
                if ident in done or factor <= 0:
                    continue
                if all(any(r in done for r in group) for group in focus_refs(node, "prerequisite")):
                    done.add(ident)
                    changed = True
        reached = done & set(own)
        self.assertIn("NPT_ud_council_long_watch", reached)
        self.assertFalse({i for i in reached if "ac_ud_npt_regime_" in json.dumps(get(own[i], "completion_reward"))})
        for opener in ("NPT_ud_parliament_petition", "NPT_ud_reformist_programme"):
            self.assertEqual(0.0, ai_factor(own[opener])[0])

    def test_unnamed_offices_only(self):
        characters = parse(text("characters"))[0][2]
        self.assertEqual({"NPT_ud_island_cabinet_office", "NPT_ud_readiness_directorate_office"}, {k for k, _, _ in characters})
        loc = localisation()
        for name, _, body in characters:
            self.assertEqual(name, get(body, "name"))
            self.assertIn("Unnamed office leader", loc[name + "_desc"])


class Guards(unittest.TestCase):
    def test_no_banned_effects_or_ucw_writes(self):
        source = own_text()
        self.assertEqual([], seams.banned_uses(source))
        self.assertNotRegex(source, r"\b(set|clr)_global_flag\b")
        self.assertNotRegex(source, r"ac_ucw_grievance|ac_ucw_country_start|ac_ucw_pressure|\bERU\b")
        self.assertNotRegex(source, r"\b(load_focus_tree|add_to_faction|white_peace|set_cosmetic_tag|add_state_claim)\b")
        # No place-to-state mapping: no numbered state scopes or state IDs.
        self.assertNotRegex(source, r"(?m)\b\d{2,4}\s*=\s*\{|\bstate\s*=\s*\d+")
        ucw_effects = set(re.findall(r"\b(ac_ucw_\w+)\s*=\s*yes", source))
        self.assertEqual({"ac_ucw_bound", "ac_ucw_active"}, ucw_effects)

    def test_every_fiscal_call_is_guarded(self):
        source = own_text()
        self.assertTrue(FISCAL.search(source))
        self.assertEqual([], FISCAL.findall(strip_guarded_fiscal(source).replace("ac_econ_ready = yes", "")))

    def test_called_effects_exist(self):
        defined = set(re.findall(r"^(\w+)\s*=\s*\{", text("effects"), re.M))
        called = set(re.findall(r"\b(ac_\w+)\s*=\s*yes", own_text())) - {"ac_econ_ready", "ac_ucw_active"}
        self.assertEqual(set(), called - defined - FOREIGN_EFFECTS)
        for name in FOREIGN_EFFECTS:
            self.assertTrue(any(re.search(r"(?m)^" + name + r"\s*=\s*\{", p.read_text(encoding="utf-8-sig"))
                                for p in (MOD / "common/scripted_effects").glob("*.txt")), name)

    def test_war_still_starts_by_default(self):
        # The package never touches the war files, so the Track A simulation is unchanged.
        spec = importlib.util.spec_from_file_location("ucw_for_npt", ROOT / "tools/Test-ContinentalWar.py")
        ucw = importlib.util.module_from_spec(spec)
        sys.modules["ucw_for_npt"] = ucw
        spec.loader.exec_module(ucw)
        world = ucw.at_war()
        self.assertIn("ac_ucw_war_started", world.globals)
        self.assertEqual(ucw.day("2003.6.22"), world.today)


class Generators(unittest.TestCase):
    def test_build_and_owner_generator_checks_pass(self):
        # leaders.py lists every authored country leader, so the office characters feed its record too.
        for args in (["tools/usea_depth/npt/build.py", "--check"], ["tools/usea_expansion/build_content.py", "--check"],
                     ["tools/release_foundations/leaders.py", "--check"]):
            result = subprocess.run([sys.executable, "-B"] + args, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
