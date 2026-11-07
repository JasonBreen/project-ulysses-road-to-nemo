"""Static checks for the Usea Depth minors B package (the README's test checklist).

Reads the generated mod files, not the authoring modules, wherever the engine would.
Static and offline only; nothing here was observed in HOI4.
"""
import hashlib
import json
import re
import subprocess
import sys
import unittest
from itertools import combinations
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MOD = ROOT / "mod/2985041246"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
from usea_depth import seams  # noqa: E402
from script import parse, get, walk  # noqa: E402
import build  # noqa: E402

# Every authored state module (states/<tag>.py) in package order.
TAGS = tuple(s.TAG for s in build.all_states())
FILES = {
    "effects": "common/scripted_effects/ac_ud_minors_b.txt",
    "triggers": "common/scripted_triggers/ac_ud_minors_b.txt",
    "ideas": "common/ideas/ac_ud_minors_b.txt",
    "characters": "common/characters/ac_ud_minors_b.txt",
    "events": "events/ac_ud_minors_b.txt",
    "decisions": "common/decisions/ac_ud_minors_b.txt",
    "categories": "common/decisions/categories/ac_ud_minors_b.txt",
}
TREES = {tag: "common/national_focus/ac_ud_minor_%s.txt" % tag.lower() for tag in TAGS}
LOCFILE = MOD / "localisation/english/ac_ud_minors_b_l_english.yml"
GFX = MOD / "interface/ac_ud_minors_b.gfx"


def text(relative):
    return (MOD / relative).read_text(encoding="utf-8-sig")


def nodes(relative):
    return parse(text(relative))


def all_script():
    return {name: text(path) for name, path in list(FILES.items()) + [(t, p) for t, p in TREES.items()]}


def localisation(path=None):
    keys = {}
    paths = [path] if path else sorted((MOD / "localisation").rglob("*.yml"))
    for p in paths:
        for m in re.finditer(r'^\s*([^\s:#]+):\d*\s+"((?:\\.|[^"\\\r\n])*)"', p.read_text(encoding="utf-8-sig", errors="replace"), re.M):
            keys[m[1]] = m[2]
    return keys


def focus_nodes(tag):
    tree = get(nodes(TREES[tag]), "focus_tree")
    return tree, [n for k, _, n in tree if k == "focus"]


def flat(block):
    """Every key = scalar pair inside a block, in order."""
    out = []
    for k, op, v in block:
        if isinstance(v, list):
            out.append((k, None))
            out.extend(flat(v))
        else:
            out.append((k, v))
    return out


def sprites():
    found = {}
    for path in sorted((MOD / "interface").glob("*.gfx")):
        for m in re.finditer(r'name\s*=\s*"([^"]+)"\s+texturefile\s*=\s*"([^"]+)"', path.read_text(encoding="utf-8-sig", errors="replace")):
            found.setdefault(m[1], []).append(m[2])
    return found


class ReviewRegressions(unittest.TestCase):
    """Small offline models of the generated guards and political idea rewards."""

    @staticmethod
    def capacity_available(available, capacity):
        # Other prerequisites are assumed satisfied; inspect the generated AND guard.
        checks = [body for key, _, body in available if key == "check_variable"]
        for check in checks:
            for variable, op, value in check:
                if variable != "ac_pol_capacity" or op != ">=":
                    raise AssertionError("Unexpected capacity condition")
                if capacity < float(value):
                    return False
        return True

    def test_every_programme_requires_full_capacity_cost(self):
        decisions = get(nodes(FILES["decisions"]), "ac_ud_minors_b_programmes")
        programmes = [(ident, body) for ident, _, body in decisions
                      if get(get(body, "complete_effect", []), "ac_ud_minors_b_pay_programme") == "yes"]
        self.assertEqual(sum(len(state.DECISIONS) for state in build.all_states()), len(programmes))
        self.assertGreater(len(programmes), 0)
        pay = get(nodes(FILES["effects"]), "ac_ud_minors_b_pay_programme")
        self.assertEqual("-2", get(get(pay, "set_temp_variable"), "ac_pol_capacity_delta"))
        for ident, body in programmes:
            available = get(body, "available")
            for capacity in (0, 1, 1.99, 2, 3):
                with self.subTest(decision=ident, capacity=capacity):
                    self.assertEqual(capacity >= 2, self.capacity_available(available, capacity))
            # Removing the affordability check recreates the reviewed exploit.
            broken = [node for node in available if node[0] != "check_variable"]
            self.assertTrue(self.capacity_available(broken, 0))

    @staticmethod
    def political_ideas(rewards, order):
        ideas = {"CRS_ud_strait_divide_spirit"}
        completed = set()

        def matches(limit):
            results = []
            for key, _, value in limit:
                if key == "NOT":
                    results.append(not matches(value))
                elif key == "has_completed_focus":
                    results.append(value in completed)
                elif key == "has_idea":
                    results.append(value in ideas)
                else:
                    raise AssertionError("Unexpected idea condition: " + key)
            return all(results)

        def apply(effect):
            for key, _, value in effect:
                if key == "if":
                    if matches(get(value, "limit")):
                        apply([node for node in value if node[0] != "limit"])
                elif key == "add_ideas":
                    ideas.add(value)
                elif key == "remove_ideas":
                    ideas.discard(value)
                # Regime calls and scheduled narrative events do not change these ideas.
                elif key != "country_event" and not key.startswith("ac_ud_minors_b_regime_"):
                    raise AssertionError("Unexpected political effect: " + key)

        for focus in order:
            apply(rewards[focus])
            completed.add(focus)
        return ideas

    def test_conference_does_not_restore_replaced_spirit(self):
        _, focuses = focus_nodes("CRS")
        rewards = {get(focus, "id"): get(focus, "completion_reward") for focus in focuses}
        conference = "CRS_ud_inter_island_conference"
        accord = "CRS_ud_strait_accord_spirit"
        self.assertEqual({accord}, self.political_ideas(rewards, (conference,)))
        for path, spirit in (("western_executive", "western_order"), ("harbour_commons", "harbour_commons")):
            political = "CRS_ud_" + path
            expected = {"CRS_ud_" + spirit + "_spirit"}
            for order in ((conference, political), (political, conference)):
                with self.subTest(order=order):
                    self.assertEqual(expected, self.political_ideas(rewards, order))
            broken = dict(rewards, **{conference: parse("remove_ideas = CRS_ud_strait_divide_spirit add_ideas = " + accord)})
            self.assertNotEqual(expected, self.political_ideas(broken, (political, conference)))
        self.assertEqual({"CRS_ud_federal_compact_spirit"},
                         self.political_ideas(rewards, (conference, "CRS_ud_two_island_compact")))


class Package(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.budget = json.loads((HERE / "budget.json").read_text(encoding="utf-8"))
        cls.loc = localisation(LOCFILE)
        cls.trees = {tag: focus_nodes(tag) for tag in TAGS}
        cls.events = [n for k, _, n in nodes(FILES["events"]) if k == "country_event"]
        cls.effects = {k: v for k, _, v in nodes(FILES["effects"])}

    # Counts and import ownership ---------------------------------------------------------
    def test_counts_equal_budget_and_every_focus_is_defined_once_in_its_own_tree(self):
        counts = {tag: len(focuses) for tag, (_, focuses) in self.trees.items()}
        self.assertEqual("minors_b", self.budget["package"])
        self.assertEqual(counts, self.budget["focuses"])
        self.assertEqual({build.tree_id(t): n for t, n in counts.items()}, self.budget["trees"])
        self.assertEqual(len(self.events), self.budget["events"])
        self.assertEqual(sum(self.budget["focuses"].values()), sum(self.budget["trees"].values()))
        for tag in TAGS:
            planned = build.PLANNED[tag]
            self.assertLessEqual(abs(counts[tag] - planned), 6, tag)
        defined = {}
        for path in sorted((MOD / "common/national_focus").glob("*.txt")):
            body = path.read_text(encoding="utf-8-sig", errors="replace")
            for ident in re.findall(r"\bid\s*=\s*([A-Z]{3}_ud_\w+)", body):
                if ident[:3] in TAGS:
                    defined.setdefault(ident, []).append(path.name)
            for ident in re.findall(r"shared_focus\s*=\s*([A-Z]{3}_ud_\w+)", body):
                self.assertNotIn(ident[:3], TAGS, "minor trees are owned outright, not imported: " + ident)
        for tag, (tree, focuses) in self.trees.items():
            self.assertEqual(build.tree_id(tag), get(tree, "id"))
            for focus in focuses:
                ident = get(focus, "id")
                self.assertTrue(ident.startswith(tag + "_ud_"), ident)
                self.assertEqual([Path(TREES[tag]).name], defined[ident], ident)
        self.assertEqual(sum(counts.values()), len(defined))

    def test_no_new_file_uses_a_reserved_prefix(self):
        for path in list(FILES.values()) + list(TREES.values()) + [LOCFILE.relative_to(MOD).as_posix(), GFX.relative_to(MOD).as_posix()]:
            self.assertFalse(Path(path).name.startswith(("ERU", "FCU", "NPT", "REC", "YUK", "ac_ucw")), path)

    # Placement and captions ---------------------------------------------------------------
    def test_nodes_sit_in_the_band_and_the_continuous_panel_clears_the_tree(self):
        positions = seams.tree_positions()
        for tag, (tree, focuses) in self.trees.items():
            ids = [get(f, "id") for f in focuses]
            tree_positions = positions[build.tree_id(tag)]
            self.assertEqual([], seams.band_violations(tree_positions, ids, 0, 23), tag)
            max_x = max(int(get(f, "x")) for f in focuses)
            panel = get(tree, "continuous_focus_position")
            self.assertEqual(str((max_x + 4) * 96), get(panel, "x"), tag)
            self.assertEqual(set(ids), set(tree_positions), tag)

    def test_titles_fit_and_no_captions_overlap(self):
        positions = seams.tree_positions()
        for tag, (_, focuses) in self.trees.items():
            for focus in focuses:
                self.assertTrue(seams.title_fits(self.loc[get(focus, "id")]), get(focus, "id"))
            tree = positions[build.tree_id(tag)]
            for a, b in combinations(sorted(tree), 2):
                (ax, ay), (bx, by) = tree[a], tree[b]
                self.assertFalse(abs(ax - bx) * 96 < 147 and abs(ay - by) * 160 < 54, (a, b))

    def test_prerequisites_and_exclusions_resolve_without_cycles(self):
        for tag, (_, focuses) in self.trees.items():
            ids = {get(f, "id"): f for f in focuses}
            for ident, focus in ids.items():
                for kind, _, block in focus:
                    if kind in ("prerequisite", "mutually_exclusive"):
                        for _, _, ref in block:
                            self.assertIn(ref, ids, (ident, ref))
                            if kind == "prerequisite":
                                self.assertLess(int(get(ids[ref], "y")), int(get(focus, "y")), (ident, ref))
                            else:
                                self.assertIn(ident, [r for k, _, b in ids[ref] if k == "mutually_exclusive" for _, _, r in b], (ident, ref))
                self.assertIn(get(focus, "cost"), ("5", "10"), ident)

    # Weights and old saves ----------------------------------------------------------------
    def test_trees_outrank_the_regional_tree_only_for_their_own_tag(self):
        regional = get(nodes("common/national_focus/ac_regional_foundation.txt"), "focus_tree")
        self.assertIn("add = 5", re.sub(r"\s+", " ", text("common/national_focus/ac_regional_foundation.txt")))
        self.assertEqual("ac_regional_foundation", get(regional, "id"))
        for tag, (tree, _) in self.trees.items():
            rule = get(tree, "country")
            self.assertEqual("0", get(rule, "factor"))
            modifiers = [m for k, _, m in rule if k == "modifier"]
            self.assertEqual(1, len(modifiers))
            self.assertEqual({"add": "45", "tag": tag, "original_tag": tag}, {k: v for k, _, v in modifiers[0]})
            self.assertEqual("no", get(tree, "default"))

    def test_adopt_decisions_switch_old_saves_through_the_idle_seam(self):
        category = get(nodes(FILES["decisions"]), "ac_ud_minors_b_programmes")
        categories = nodes(FILES["categories"])
        self.assertIsNotNone(get(categories, "ac_ud_minors_b_programmes"))
        for tag in TAGS:
            decision = get(category, tag + "_ud_adopt_programme")
            self.assertIsNotNone(decision, tag)
            available = flat(get(decision, "available"))
            self.assertIn(("ac_pol_previous_tree_idle", "yes"), available)
            effect = get(decision, "complete_effect")
            guarded = get(effect, "if")
            self.assertIn(("ac_pol_previous_tree_idle", "yes"), flat(get(guarded, "limit")))
            load = get(guarded, "load_focus_tree")
            self.assertEqual({"tree": build.tree_id(tag), "keep_completed": "yes"}, {k: v for k, _, v in load})

    # Localisation --------------------------------------------------------------------------
    def test_localisation_is_complete_with_a_bom(self):
        self.assertTrue(LOCFILE.read_bytes().startswith(b"\xef\xbb\xbfl_english:"))
        self.assertNotIn(b"\r\n", LOCFILE.read_bytes())
        needed = set()
        for tag, (tree, focuses) in self.trees.items():
            needed |= {build.tree_id(tag), build.tree_id(tag) + "_desc"}
            for focus in focuses:
                needed |= {get(focus, "id"), get(focus, "id") + "_desc"}
        for k, _, v in get(nodes(FILES["ideas"]), "ideas")[0][2]:
            needed |= {k, k + "_desc"}
        for k, _, v in get(nodes(FILES["decisions"]), "ac_ud_minors_b_programmes"):
            needed |= {k, k + "_desc"}
        for k, _, v in get(nodes(FILES["characters"]), "characters"):
            needed |= {k, k + "_desc"}
        for event in self.events:
            needed |= {get(event, "title"), get(event, "desc")}
            needed |= {get(o, "name") for k, _, o in event if k == "option"}
        self.assertEqual(set(), needed - set(self.loc))
        for key, value in self.loc.items():
            self.assertNotRegex(value, "[“”‘’]", key)

    def test_every_flag_read_or_set_has_a_readable_label(self):
        everything = localisation()
        for name, body in all_script().items():
            for flag in re.findall(r"has_(?:country|global|state)_flag\s*=\s*(\w+)", body):
                self.assertIn(flag, everything, (name, flag))
            for flag in re.findall(r"set_country_flag\s*=\s*(\w+)", body):
                self.assertIn(flag, everything, (name, flag))
            for flag in re.findall(r"set_country_flag\s*=\s*\{\s*flag\s*=\s*(\w+)", body):
                self.assertIn(flag, everything, (name, flag))

    # Art ------------------------------------------------------------------------------------
    def test_icons_and_shines_resolve_to_unique_mod_textures(self):
        found = sprites()
        textures = []
        for tag, (_, focuses) in self.trees.items():
            for focus in focuses:
                ident = get(focus, "id")
                icon = get(focus, "icon")
                self.assertEqual("GFX_ac_ud_focus_" + ident, icon)
                expected = "gfx/AC_usea_depth/minors_b/focus/%s.dds" % ident
                self.assertEqual([expected], found.get(icon), icon)
                self.assertEqual([expected], found.get(icon + "_shine"), icon)
                path = MOD / expected
                with Image.open(path) as image:
                    self.assertEqual((96, 96), image.size)
                textures.append(hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(len(textures), len(set(textures)), "every focus icon is a distinct composition")
        self.assertNotIn("shine_overlay", GFX.read_text(encoding="utf-8"))
        for k, _, idea in get(nodes(FILES["ideas"]), "ideas")[0][2]:
            self.assertIn("GFX_idea_" + get(idea, "picture"), found)
        for tag in TAGS:
            with Image.open(MOD / found["GFX_decision_ac_ud_minb_" + tag.lower()][0]) as image:
                self.assertEqual((32, 32), image.size)
        for k, _, character in get(nodes(FILES["characters"]), "characters"):
            sprite = re.search(r'large\s*=\s*"([^"]+)"', text(FILES["characters"]).split(k + " = {", 1)[1])[1]
            with Image.open(MOD / found[sprite][0]) as image:
                self.assertEqual((156, 210), image.size)
        manifest = json.loads((HERE / "assets.json").read_text(encoding="utf-8"))
        for row in manifest["assets"]:
            self.assertEqual(row["sha256"], hashlib.sha256((MOD / row["file"]).read_bytes()).hexdigest(), row["file"])
            self.assertTrue(row["file"].startswith("gfx/AC_usea_depth/minors_b/"), row["file"])
        for name, files in found.items():
            if name.startswith(("GFX_ac_ud_focus_", "GFX_ac_ud_minb_", "GFX_decision_ac_ud_minb_", "GFX_decision_category_ac_ud_minors_b")) or "_ud_" in name and name.startswith("GFX_idea_"):
                if any(f.startswith("gfx/AC_usea_depth/minors_b/") for f in files):
                    self.assertEqual(1, len(files), name)

    def test_event_pictures_are_existing_mod_art(self):
        found = sprites()
        for event in self.events:
            picture = get(event, "picture")
            self.assertTrue(picture.startswith("GFX_ac_camp_event_"), picture)
            self.assertTrue((MOD / found[picture][0]).exists(), picture)

    # Politics ---------------------------------------------------------------------------------
    def test_government_changes_only_in_regime_effects_with_zero_ai_weight(self):
        for name, body in all_script().items():
            if name != "effects":
                self.assertNotRegex(body, r"\bset_(politics|popularities)\b", name)
                self.assertNotRegex(body, r"\b(recruit|promote|retire)_character\b", name)
        self.assertEqual([], seams.political_violations(text(FILES["effects"])))
        regimes = [k for k in self.effects if k.startswith("ac_ud_minors_b_regime_")]
        self.assertEqual(set(regimes), {k for k in self.effects if "set_politics" in json.dumps(self.effects[k])})
        per_tag = {}
        for name in regimes:
            per_tag.setdefault(name.split("_")[5].upper(), []).append(name)
            body = self.effects[name]
            office = get(body, "promote_character")
            self.assertRegex(get(office, "character"), r"^[A-Z]{3}_ud_\w+_office$")
        self.assertEqual({t: True for t in TAGS}, {t: 2 <= len(per_tag.get(t, [])) <= 3 for t in TAGS})
        reached = set()
        for tag, (_, focuses) in self.trees.items():
            for focus in focuses:
                calls = [k for k, _ in flat(get(focus, "completion_reward")) if k.startswith("ac_ud_minors_b_regime_")]
                if calls:
                    reached.update(calls)
                    self.assertEqual("0", get(get(focus, "ai_will_do"), "factor"), get(focus, "id"))
        for event in self.events:
            for k, _, option in event:
                if k == "option" and any(key.startswith("ac_ud_minors_b_regime_") for key, _ in flat(option)):
                    self.assertEqual("0", get(get(option, "ai_chance"), "factor"), get(event, "id"))
        self.assertEqual(set(regimes), reached)

    def test_office_leaders_are_unnamed_generated_cards(self):
        characters = get(nodes(FILES["characters"]), "characters")
        effects = text(FILES["effects"])
        for ident, _, body in characters:
            self.assertRegex(ident, r"^(%s)_ud_[a-z0-9_]+_office$" % "|".join(TAGS))
            self.assertEqual(ident, get(body, "name"))
            self.assertIn("recruit_character = " + ident, effects)
            self.assertIn("unnamed office", self.loc[ident + "_desc"].lower())

    def test_no_popularity_thresholds_and_no_history_seeding(self):
        for name, body in all_script().items():
            self.assertNotRegex(body, r"\bhas_popularity\b|\bparty_popularity\b|\bpopularity\s*[<>]", name)
        histories = "".join(p.read_text(encoding="utf-8-sig", errors="replace") for p in (MOD / "history/countries").glob("*.txt"))
        self.assertNotIn("_ud_", histories)

    # Guards -------------------------------------------------------------------------------------
    def test_no_banned_effects_war_flags_or_grievance_writes(self):
        for name, body in all_script().items():
            self.assertEqual([], seams.banned_uses(body), name)
            self.assertNotRegex(body, r"(set|clr)_global_flag", name)
            self.assertNotRegex(body, r"ac_ucw_(grievance|country_start|pressure)|_variable\s*=\s*\{\s*ac_ucw_", name)
            self.assertNotRegex(body, r"\b(give_guarantee|give_military_access|release|release_puppet|set_autonomy|puppet|add_opinion_modifier|create_faction)\s*=", name)
            self.assertNotRegex(body, r"\bset_variable\s*=\s*\{\s*ac_pol_capacity\b|add_to_variable\s*=\s*\{\s*ac_pol_capacity\s*=", name)
        # The Continental War owner is untouched: no package file hooks its on-actions or start effect.
        self.assertFalse((MOD / "common/on_actions/ac_ud_minors_b.txt").exists())
        # Other Usea Depth packages may own hooks there (North Point's hosting); minors B owns none.
        for owner in ("common/on_actions/ac_ucw.txt", "common/scripted_effects/ac_ucw.txt"):
            self.assertNotRegex(text(owner), r"ac_ud_minors_b|ac_ud_minb|\b(%s)_ud_" % "|".join(TAGS), owner)

    def test_institution_gains_go_through_the_capacity_effect(self):
        for name, body in all_script().items():
            deltas = len(re.findall(r"ac_pol_capacity_delta\s*=", body))
            calls = len(re.findall(r"ac_pol_change_capacity\s*=\s*yes", body))
            self.assertEqual(deltas, calls, name)
        for tag in TAGS:
            self.assertGreaterEqual(len(re.findall(r"ac_pol_change_capacity", text(TREES[tag]))), 5, tag)

    def test_every_fiscal_call_is_guarded(self):
        body = text(FILES["effects"])
        tree = parse(body)

        def visit(block, guarded):
            for k, _, v in block:
                if k.startswith(("ac_econ_", "ac_macro_")) and not k.endswith("_ready") and k != "ac_econ_ready":
                    self.assertTrue(guarded, k)
                if isinstance(v, list):
                    inner = guarded or (k == "if" and ("ac_econ_ready", "yes") in flat(get(v, "limit") or []))
                    visit([n for n in v if n[0] != "limit"], inner)
        visit(tree, False)
        for name, script in all_script().items():
            if name != "effects":
                self.assertNotRegex(script, r"\bac_(econ|macro)_(?!ready)\w+\s*=\s*yes", name)

    def test_research_categories_buildings_and_modifiers_are_valid(self):
        categories = set()
        for path in (MOD / "common/technology_tags").glob("*.txt"):
            body = path.read_text(encoding="utf-8-sig", errors="replace")
            for block in re.findall(r"technology_categories\s*=\s*\{(.*?)\}", body, re.S):
                categories.update(re.findall(r"^\s*(\w+)", block, re.M))
        used = set(re.findall(r"category\s*=\s*(\w+)", "".join(all_script().values())))
        self.assertTrue(used <= categories, used - categories)
        known = set()
        for path in (MOD / "common/ideas").glob("*.txt"):
            if path.name == "ac_ud_minors_b.txt":
                continue
            for block in re.findall(r"modifier\s*=\s*\{([^{}]*)\}", path.read_text(encoding="utf-8-sig", errors="replace")):
                known.update(re.findall(r"(\w+)\s*=\s*-?[\d.]+", block))
        for k, _, idea in get(nodes(FILES["ideas"]), "ideas")[0][2]:
            self.assertTrue({m for m, _, _ in get(idea, "modifier")} <= known, k)

    # Events --------------------------------------------------------------------------------------
    def test_events_are_long_form_and_every_one_is_reachable(self):
        ids = [get(e, "id") for e in self.events]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(text(FILES["events"]).count("add_namespace = ac_ud_minb") == 1)
        fired = set(re.findall(r"country_event\s*=\s*\{\s*id\s*=\s*(ac_ud_minb\.\d+)", "".join(all_script().values())))
        self.assertEqual(set(ids), fired)
        for event in self.events:
            self.assertEqual("yes", get(event, "is_triggered_only"))
            body = self.loc[get(event, "desc")].replace("\\n", "\n")
            self.assertEqual([], seams.event_problems(body), get(event, "id"))
            self.assertLessEqual(len(body), 3000, get(event, "id"))
        per_tag = {}
        for ident in ids:
            per_tag.setdefault(int(ident.split(".")[1]) // 100, []).append(ident)
        for tag, (_, focuses) in self.trees.items():
            self.assertGreaterEqual(len(per_tag[build.EVENT_BASE[tag] // 100]) * 6, len(focuses), tag)

    def test_trees_are_distinct_not_one_template(self):
        titles = [self.loc[get(f, "id")] for _, focuses in self.trees.values() for f in focuses]
        self.assertEqual(len(titles), len(set(titles)), "focus titles repeat across the package")
        layouts = {tag: frozenset((get(f, "x"), get(f, "y")) for f in focuses) for tag, (_, focuses) in self.trees.items()}
        for a, b in combinations(TAGS, 2):
            overlap = len(layouts[a] & layouts[b]) / min(len(layouts[a]), len(layouts[b]))
            self.assertLess(overlap, 0.6, (a, b))

    def test_shilage_tree_is_dormant_and_never_releases_or_annexes(self):
        if "SHI" not in TAGS:
            self.skipTest("Shilage module not authored yet")
        tree, focuses = self.trees["SHI"]
        self.assertEqual({"add": "45", "tag": "SHI", "original_tag": "SHI"}, {k: v for k, _, v in get(get(tree, "country"), "modifier")})
        body = text(TREES["SHI"])
        for token in ("annex", "release", "transfer_state", "add_state_core", "add_core_of", "set_owner"):
            self.assertNotIn(token, body)
        # Shilage may hold any subset of its cores, so it never scopes a state by ID
        # (607 is an unresolved XXX placeholder): only the capital, behind a control guard.
        self.assertNotRegex(body, r"(?m)^\s*\d+\s*=\s*\{")
        self.assertIn("capital_scope", body)
        shilage_events = [e for e in self.events if get(e, "id").startswith("ac_ud_minb.7")]
        self.assertEqual(["SHI"], sorted({get(get(e, "trigger"), "original_tag") for e in shilage_events}))
        self.assertNotIn("SHI", "".join(text(TREES[t]) for t in TAGS if t != "SHI"))

    # Generators ----------------------------------------------------------------------------------
    def test_generators_reproduce_the_committed_outputs(self):
        for script in ("build.py", "build_art.py"):
            result = subprocess.run([sys.executable, "-B", str(HERE / script), "--check"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
