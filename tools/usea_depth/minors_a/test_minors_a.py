"""Static checks for the Usea Depth minor states A package (README "Every package test checks").

Offline only: no HOI4 launch, parser, save/load or AI run. Each check reads the
committed outputs, not the authoring modules alone, so a stale build fails here.
"""
import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import content as C  # noqa: E402
from usea_depth import seams  # noqa: E402
from usea_expansion.script import parse, get  # noqa: E402

MOD = C.MOD
OWN_FILES = [build.focus_file(t) for t in C.TAGS] + list(build.FILES.values())
LOC_PATH = MOD / build.OWN_LOC


def text(relative):
    return (MOD / relative).read_text(encoding="utf-8-sig")


def localisation():
    keys = {}
    for path in sorted((MOD / "localisation/english").rglob("*.yml")):
        for match in re.finditer(r'^\s*([\w.\-]+):\d*\s+"(.*)"\s*$', path.read_text(encoding="utf-8-sig", errors="replace"), re.M):
            keys.setdefault(match[1], match[2])
    return keys


def own_localisation():
    return {m[1]: m[2] for m in re.finditer(r'^\s*([\w.\-]+):0 "(.*)"$', LOC_PATH.read_text(encoding="utf-8-sig"), re.M)}


def tree_nodes(tag):
    tree = get(parse(text(build.focus_file(tag))), "focus_tree")
    return tree, [node for kind, _, node in tree if kind == "focus"]


def blocks_named(source, key):
    """Bodies of every `key = { ... }` block, brace-balanced."""
    out = []
    for match in re.finditer(r"\b%s\s*=\s*\{" % re.escape(key), source):
        depth, cursor = 1, match.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(source[cursor], 0)
            cursor += 1
        out.append(source[match.end():cursor - 1])
    return out


class MinorsA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.states = C.load_states()
        cls.budget = json.loads((HERE / "budget.json").read_text(encoding="utf-8"))
        cls.loc = localisation()
        cls.own_loc = own_localisation()

    # Counts and imports -------------------------------------------------
    def test_generators_reproduce_every_output(self):
        for script in ("build.py", "build_art.py"):
            result = subprocess.run([sys.executable, "-B", str(HERE / script), "--check"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_counts_equal_budget_and_each_id_is_defined_once_in_its_own_tree(self):
        self.assertEqual("minors_a", self.budget["package"])
        self.assertEqual(set(C.TAGS), set(self.budget["focuses"]))
        seen = Counter()
        for path in (MOD / "common/national_focus").glob("*.txt"):
            source = path.read_text(encoding="utf-8-sig")
            for ident in re.findall(r"\bid\s*=\s*((?:%s)_ud_\w+)" % "|".join(C.TAGS), source):
                seen[(ident, path.name)] += 1
            for ident in re.findall(r"shared_focus\s*=\s*((?:%s)_ud_\w+)" % "|".join(C.TAGS), source):
                self.fail("minor focus %s imported as a shared focus in %s" % (ident, path.name))
        events = 0
        for tag in C.TAGS:
            _, nodes = tree_nodes(tag)
            ids = [get(n, "id") for n in nodes]
            self.assertEqual(self.budget["focuses"][tag], len(ids), tag)
            self.assertEqual(self.budget["trees"][C.tree_id(tag)], len(ids), tag)
            self.assertGreaterEqual(len(ids), 55, tag)
            for ident in ids:
                self.assertEqual({(ident, "ac_ud_minor_%s.txt" % tag.lower()): 1}, {k: v for k, v in seen.items() if k[0] == ident})
        events = len(re.findall(r"^country_event = \{", text(build.FILES["events"]), re.M))
        self.assertEqual(self.budget["events"], events)
        self.assertEqual(sum(self.budget["focuses"].values()), sum(self.budget["trees"].values()))
        self.assertGreaterEqual(events, sum(self.budget["focuses"].values()) // 5)

    def test_tree_weight_outranks_regional_tree_and_panel_position(self):
        regional = text("common/national_focus/ac_regional_foundation.txt")
        self.assertIn("modifier = { add = 5 ac_pol_uses_regional_tree = yes }", regional)
        for tag in C.TAGS:
            tree, nodes = tree_nodes(tag)
            self.assertEqual(C.tree_id(tag), get(tree, "id"))
            self.assertIn("country = { factor = 0 modifier = { add = 45 tag = %s original_tag = %s } }" % (tag, tag), text(build.focus_file(tag)))
            self.assertEqual("no", get(tree, "default"))
            max_x = max(int(get(n, "x")) for n in nodes)
            position = get(tree, "continuous_focus_position")
            self.assertEqual((max_x + 4) * 96, int(get(position, "x")), tag)

    # Layout -----------------------------------------------------------------
    def test_nodes_sit_in_band_titles_fit_and_captions_never_overlap(self):
        positions = seams.tree_positions()
        for tag in C.TAGS:
            tree = C.tree_id(tag)
            self.assertIn(tree, positions)
            ids = [get(n, "id") for n in tree_nodes(tag)[1]]
            self.assertEqual([], seams.band_violations(positions[tree], ids, 0, C.MAX_X), tag)
            placed = positions[tree]
            for a in ids:
                self.assertTrue(seams.title_fits(self.own_loc[a]), a)
                for b in ids:
                    if a < b:
                        (ax, ay), (bx, by) = placed[a], placed[b]
                        self.assertFalse(abs(ax - bx) * 96 < 147 and abs(ay - by) * 160 < 54, (a, b))

    def test_prerequisites_exclusions_and_costs_are_consistent(self):
        for tag in C.TAGS:
            _, nodes = tree_nodes(tag)
            ids = {get(n, "id"): n for n in nodes}
            for ident, node in ids.items():
                self.assertIn(get(node, "cost"), ("5", "10"), ident)
                for kind, _, body in node:
                    if kind in ("prerequisite", "mutually_exclusive"):
                        for _, _, ref in body:
                            self.assertIn(ref, ids, ident)
                    if kind == "mutually_exclusive":
                        for _, _, ref in body:
                            other = [r for k, _, b in ids[ref] if k == "mutually_exclusive" for _, _, r in b]
                            self.assertIn(ident, other, "exclusion is not mirrored: %s / %s" % (ident, ref))

    # Localisation -------------------------------------------------------------
    def test_localisation_is_complete_with_bom_and_no_curly_quotes(self):
        raw = LOC_PATH.read_bytes()
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
        decoded = raw.decode("utf-8-sig")
        self.assertTrue(decoded.startswith("l_english:\n"))
        self.assertFalse(any(c in decoded for c in "“”‘’"))
        self.assertTrue(decoded.isascii())
        needed = []
        for tag in C.TAGS:
            for node in tree_nodes(tag)[1]:
                needed += [get(node, "id"), get(node, "id") + "_desc"]
            needed += [C.tree_id(tag), C.tree_id(tag) + "_desc"]
        for source in (text(build.FILES["ideas"]),):
            for ident in re.findall(r"^\t\t(\w+_spirit) = \{", source, re.M):
                needed += [ident, ident + "_desc"]
        for ident in re.findall(r"^(\w+_office) = \{", text(build.FILES["characters"]), re.M):
            needed += [ident, ident + "_desc"]
        events = text(build.FILES["events"])
        needed += re.findall(r"(?:title|desc|name) = (ac_ud_mina\.[\w.]+)", events)
        needed += re.findall(r"custom_effect_tooltip = (\w+)", "\n".join(text(build.focus_file(t)) for t in C.TAGS))
        for ident in re.findall(r"^\t(ac_ud_minors_a_adopt_\w+_decision) = \{", text(build.FILES["decisions"]), re.M):
            needed += [ident, ident + "_desc"]
        missing = [key for key in needed if key not in self.loc]
        self.assertEqual([], missing)
        # Our keys never duplicate another file's keys.
        others = {}
        for path in sorted((MOD / "localisation").rglob("*.yml")):
            if path == LOC_PATH:
                continue
            for match in re.finditer(r'^\s*([\w.\-]+):\d*\s+"', path.read_text(encoding="utf-8-sig", errors="replace"), re.M):
                others[match[1]] = path.name
        self.assertEqual({}, {k: others[k] for k in self.own_loc if k in others})

    def test_every_flag_read_or_set_has_a_readable_label(self):
        source = "\n".join(text(f) for f in OWN_FILES)
        flags = set(re.findall(r"\b(?:has|set|clr)_(?:country|global)_flag = (\w+)", source))
        self.assertTrue(flags)
        for flag in sorted(flags):
            self.assertIn(flag, self.loc, flag)
            self.assertNotEqual(flag, self.loc[flag])
        self.assertNotRegex(source, r"\b(?:set|clr)_global_flag\b")

    # Art -----------------------------------------------------------------------
    def test_icons_shines_portraits_and_pictures_resolve_to_mod_textures(self):
        sprites = {}
        for path in (MOD / "interface").glob("*.gfx"):
            for name, texture in re.findall(r'name\s*=\s*"(GFX_\w+)"\s+texturefile\s*=\s*"([^"]+)"', path.read_text(encoding="utf-8-sig", errors="replace")):
                sprites.setdefault(name, texture)
        own = text("interface/ac_ud_minors_a.gfx")
        for tag in C.TAGS:
            for node in tree_nodes(tag)[1]:
                ident = get(node, "id")
                self.assertEqual("GFX_ac_ud_focus_" + ident, get(node, "icon"))
                for line in seams.focus_sprites(C.PACKAGE, ident):
                    self.assertIn(line, own)
                for name in ("GFX_ac_ud_focus_" + ident, "GFX_ac_ud_focus_" + ident + "_shine"):
                    self.assertTrue((MOD / sprites[name]).is_file(), name)
                    self.assertTrue(sprites[name].startswith("gfx/AC_usea_depth/minors_a/"), name)
        ideas = text(build.FILES["ideas"])
        for picture in re.findall(r"picture = (\w+)", ideas):
            self.assertTrue((MOD / sprites["GFX_idea_" + picture]).is_file(), picture)
        for portrait in re.findall(r'large = "(GFX_\w+)"', text(build.FILES["characters"])):
            self.assertTrue((MOD / sprites[portrait]).is_file(), portrait)
        from event_picture_fit import audit
        report = audit.audit([build.FILES["events"]])
        self.assertEqual(len(re.findall(r"^country_event = \{", text(build.FILES["events"]), re.M)), report["explicit_consumers"])
        assets = json.loads((HERE / "assets.json").read_text(encoding="utf-8"))
        focus_rows = [r for r in assets if r["role"] == "original focus composition"]
        self.assertEqual(sum(self.budget["focuses"].values()), len(focus_rows))
        self.assertEqual(len(focus_rows), len({r["sha256"] for r in focus_rows}))
        self.assertTrue(all(r["file"].startswith("gfx/AC_usea_depth/minors_a/") for r in assets))
        self.assertNotIn("shine_overlay", own)

    # Politics -----------------------------------------------------------------
    def test_governments_change_only_in_regime_effects_with_ai_weight_zero(self):
        for relative in OWN_FILES:
            self.assertEqual([], seams.political_violations(text(relative)), relative)
        effects = text(build.FILES["effects"])
        regimes = re.findall(r"^(ac_ud_minors_a_regime_\w+) = \{", effects, re.M)
        self.assertEqual(sum(len(s.governments) for s in self.states), len(regimes))
        for state in self.states:
            self.assertIn(len(state.governments), (2, 3), state.tag)
        calls = Counter()
        for tag in C.TAGS:
            for node in tree_nodes(tag)[1]:
                body = json.dumps(node)
                used = re.findall(r"ac_ud_minors_a_regime_\w+", body)
                if used:
                    calls.update(used)
                    self.assertEqual("{ factor = 0 }", re.search(r"ai_will_do = (\{[^}]*\})", text(build.focus_file(tag)).split("id = " + get(node, "id") + "\n", 1)[1])[1])
        self.assertEqual({name: 1 for name in regimes}, dict(calls))
        events = text(build.FILES["events"])
        self.assertNotIn("regime", events)
        self.assertNotRegex(events, r"set_politics|set_popularities|recruit_character|promote_character")
        characters = text(build.FILES["characters"])
        self.assertEqual(sorted(re.findall(r"^(\w+) = \{", characters, re.M)[1:]),
                         sorted(C.office_id(s.tag, g.slug) for s in self.states for g in s.governments))
        # Popularities are seeded only by the effects; histories are untouched.
        for path in (MOD / "history/countries").glob("*.txt"):
            if path.name[:3] in C.TAGS:
                self.assertNotIn("ac_ud", path.read_text(encoding="utf-8-sig", errors="replace"))

    def test_ai_never_reaches_a_government_change(self):
        for state in self.states:
            by_slug = {f.slug: f for f in state.focuses}
            reachable = {state.root}
            changed = True
            while changed:
                changed = False
                for focus in state.focuses:
                    if focus.slug in reachable or focus.regime:
                        continue
                    if all(any(ref in reachable for ref in group) for group in C.requirement_groups(focus)):
                        reachable.add(focus.slug)
                        changed = True
            self.assertFalse([s for s in reachable if by_slug[s].regime], state.tag)
            self.assertGreaterEqual(len(reachable), 30, "%s leaves the AI too little to do" % state.tag)

    # War, fiscal and banned effects ---------------------------------------------
    def test_no_banned_effects_no_ucw_writes_and_owned_states_only(self):
        for relative in OWN_FILES:
            source = text(relative)
            self.assertEqual([], seams.banned_uses(source), relative)
            self.assertNotIn("ac_ucw_country_start", source)
            self.assertNotRegex(source, r"\b(?:set|add_to|subtract_from|multiply|clamp)_variable\s*=\s*\{\s*(?:var\s*=\s*)?ac_ucw_")
            self.assertNotRegex(source, r"\bac_ucw_grievance\b")
            self.assertNotRegex(source, r"add_claim_by|remove_claim_by|set_capital|create_faction|puppet|release")
        for state in self.states:
            source = text(build.focus_file(state.tag))
            for state_id in re.findall(r"\b(\d{1,3}) = \{", source):
                self.assertIn(int(state_id), state.owned_states, state.tag)
            self.assertNotRegex(source, r"\b310\s*=\s*\{|\bstate\s*=\s*310\b", "Stonehenge's state is never scoped")
            for state_id in re.findall(r"\bstate\s*=\s*(\d+)", source):
                self.assertIn(int(state_id), state.owned_states, state.tag)

    def test_every_fiscal_call_is_guarded(self):
        for relative in OWN_FILES:
            for line in text(relative).splitlines():
                for call in re.findall(r"\b(ac_(?:econ|macro)_\w+) = yes", line):
                    if call in ("ac_econ_ready", "ac_macro_ready", "ac_econ_enabled"):
                        continue
                    self.assertRegex(line, r"if = \{ limit = \{ ac_econ_ready = yes \} %s = yes \}" % call, relative)

    def test_ai_war_start_harness_still_passes(self):
        code = ("import importlib.util, sys, unittest\n"
                "spec = importlib.util.spec_from_file_location('cw', 'tools/Test-ContinentalWar.py')\n"
                "cw = importlib.util.module_from_spec(spec); spec.loader.exec_module(cw)\n"
                "suite = unittest.TestSuite()\n"
                "for case in [c for c in vars(cw).values() if isinstance(c, type) and issubclass(c, unittest.TestCase)]:\n"
                "    for name in ('test_ai_starts_war_in_summer_2003_window_and_faction_defends', 'test_low_grievance_keeps_the_ai_from_war'):\n"
                "        if hasattr(case, name): suite.addTest(case(name))\n"
                "result = unittest.TextTestRunner(verbosity=0).run(suite)\n"
                "sys.exit(0 if result.wasSuccessful() and result.testsRun == 2 else 1)\n")
        env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "tools"), str(ROOT / "tools/usea_expansion")]))
        result = subprocess.run([sys.executable, "-B", "-c", code], cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    # Era gates and events ---------------------------------------------------------
    def test_era_gates_follow_the_chronicle_anchors(self):
        expected = {era: gate for era, gate in C.ERAS.items() if gate}
        for state in self.states:
            source = text(build.focus_file(state.tag))
            for focus in state.focuses:
                if focus.era == "early":
                    continue
                body = source.split("id = %s\n" % C.fid(state.tag, focus.slug), 1)[1].split("\n\t}\n", 1)[0]
                self.assertIn(expected[focus.era], body, focus.slug)
            eras = {f.era for f in state.focuses}
            for needed in ("ulysses", "impact", "war"):
                self.assertIn(needed, eras, state.tag)
        self.assertEqual("date > 1996.4.19", C.ERAS["ulysses"])
        self.assertEqual("date > 1999.7.7", C.ERAS["impact"])

    def test_events_are_long_form_with_a_source_line(self):
        events = text(build.FILES["events"])
        keys = re.findall(r"desc = (ac_ud_mina\.\d+\.d)", events)
        self.assertGreaterEqual(len(keys), 80)
        for key in keys:
            body = self.own_loc[key].replace("\\n", "\n").replace('\\"', '"')
            self.assertEqual([], seams.event_problems(body), key)
            self.assertTrue(body.rsplit("\n\n", 1)[-1].startswith("Provisional gameplay"), key)
        for picture in re.findall(r"picture = (\w+)", events):
            self.assertTrue(picture.startswith("GFX_ac_ud_event_"), picture)

    def test_no_new_named_people_and_no_place_mapping(self):
        own = LOC_PATH.read_text(encoding="utf-8-sig")
        for name in C.CHRONICLE_PLACES + C.PLACEHOLDER_NAMES:
            self.assertNotRegex(own, r"\b%s\b" % re.escape(name), name)
        office_words = ("Council", "Office", "Presidium", "Assembly", "Directorate", "Board", "Cabinet", "Senate", "Committee",
                        "Regency", "Executive", "Commission", "Union", "Federation", "Commonwealth", "Congress", "Secretariat", "Chancery")
        for state in self.states:
            for gov in state.governments:
                self.assertTrue(any(word in gov.title for word in office_words), gov.title)

    def test_adoption_decision_lets_old_saves_switch(self):
        source = text(build.FILES["decisions"])
        self.assertTrue(source.split("\n", 1)[1].startswith("ac_pol_institutions = {"))
        for tag in C.TAGS:
            body = blocks_named(source, "ac_ud_minors_a_adopt_%s_decision" % tag.lower())[0]
            self.assertIn("ac_pol_previous_tree_idle = yes", blocks_named(body, "available")[0])
            self.assertIn("load_focus_tree = { tree = %s keep_completed = yes }" % C.tree_id(tag), body)
            self.assertIn("NOT = { has_focus_tree = %s }" % C.tree_id(tag), body)

    def test_ledger_and_backlog_rows(self):
        ledger = (ROOT / "docs/usea_depth/MINORS_A.md").read_text(encoding="utf-8")
        for state in self.states:
            self.assertIn(C.tree_id(state.tag), ledger)
            for gov in state.governments:
                self.assertIn(C.regime_name(state.tag, gov.slug), ledger)
        backlog = (ROOT / "docs/LORE_EVENT_COVERAGE_BACKLOG.md").read_text(encoding="utf-8")
        self.assertIn("docs/usea_depth/MINORS_A.md", backlog)
        for name in ("CHO", "PLA", "FRU", "ALR", "DOR", "SCA", "BLD"):
            self.assertIn(name, backlog.split("docs/usea_depth/MINORS_A.md", 1)[0].rsplit("\n", 2)[-1] + backlog.split("docs/usea_depth/MINORS_A.md", 1)[1].split("\n", 1)[0])

    def test_new_files_avoid_reserved_prefixes(self):
        for relative in OWN_FILES + [build.OWN_LOC, "interface/ac_ud_minors_a.gfx"]:
            name = Path(relative).name
            self.assertFalse(name.startswith(("ERU", "FCU", "NPT", "REC", "YUK", "ac_ucw")), name)
            self.assertTrue((MOD / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main(verbosity=2)
