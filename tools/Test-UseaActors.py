"""Static contract checks for the North Point, Recta and Yuktobania trees.

These read the shipped scripts offline; they are not the HOI4 engine. They cover
structure, references, localisation and the shared flag contract, not native
parsing, AI focus selection, rendered layout or in-game reachability.
"""
import argparse
from pathlib import Path
import re
import sys
import unittest

from economy_script import parse

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod/2985041246"

# tag -> (tree file, focus file, tree id, idea file)
TREES = {
    "NPT": ("NPT.txt", "NPT_pre_continental_war.txt", "npt_pre_continental_war_focus", "north point.txt"),
    "REC": ("REC.txt", "REC.txt", "rec_postwar_consolidation_focus", "recta.txt"),
    "YUK": ("YUK.txt", "YUK.txt", "yuk_reform_focus", "yuktobania.txt"),
}
OWN_SHARED_FLAGS = {"ac_npt_hosts_isaf", "ac_yuk_arkbird_partner"}
# Flags owned by PR A (the ac_ucw war arc) and PR C (special projects).
FOREIGN_FLAG = re.compile(r"^(ac_ucw_\w+|ac_sp_\w+_complete)$")
SET_FLAG = re.compile(r"\b(?:set|clr)_(?:global|country)_flag\s*=\s*(?:\{\s*flag\s*=\s*)?(\w+)")
READ_FLAG = re.compile(r"\bhas_(?:global|country)_flag\s*=\s*(\w+)")
FORBIDDEN = ("transfer_state", "annex_country", "declare_war_on", "add_wargoal",
             "set_politics", "create_country_leader", "kill_country_leader",
             "retire_country_leader", "add_country_leader_role", "load_focus_tree")
LOC_KEY = re.compile(r'^\s*([A-Za-z0-9_.]+):\d*\s+"', re.M)


def load(relative):
    return parse((MOD / relative).read_text(encoding="utf-8-sig"))


def text(relative):
    return (MOD / relative).read_text(encoding="utf-8-sig")


def mapping(nodes):
    return {key: value for key, _, value in nodes}


def focus_ids(nodes, key):
    return [ident for block in (v for k, _, v in nodes if k == key)
            for k, _, ident in block if k == "focus"]


def owned_files(tag):
    tree_file, focus_file, _, idea_file = TREES[tag]
    files = {"common/national_focus/" + tree_file, "common/national_focus/" + focus_file,
             "common/ideas/" + idea_file, "common/ai_strategy/" + tag + ".txt"}
    return sorted(files)


def tree(tag):
    tree_file, focus_file, tree_id, _ = TREES[tag]
    trees = [v for k, _, v in load("common/national_focus/" + tree_file) if k == "focus_tree"]
    matches = [v for v in trees if mapping(v)["id"] == tree_id]
    assert len(matches) == 1, (tag, tree_id)
    focuses = {mapping(v)["id"]: v for k, _, v in load("common/national_focus/" + focus_file)
               if k == "shared_focus"}
    return matches[0], focuses


def localisation(tag):
    path = MOD / "localisation/english/country_{}_l_english.yml".format(tag)
    return path, LOC_KEY.findall(path.read_text(encoding="utf-8-sig"))


def mentions_foreign_flag(nodes):
    found = set()
    for key, _, value in nodes:
        if isinstance(value, list):
            found |= mentions_foreign_flag(value)
        elif key in ("has_global_flag", "has_country_flag") and FOREIGN_FLAG.match(value):
            found.add(value)
    return found


class UseaActorContracts(unittest.TestCase):
    def test_tree_container_follows_country_weight_pattern(self):
        for tag in TREES:
            container, _ = tree(tag)
            data = mapping(container)
            self.assertEqual("no", data["default"], tag)
            modifier = mapping(data["country"])
            self.assertEqual("0", modifier["factor"])
            self.assertEqual(tag, mapping(modifier["modifier"])["original_tag"])

    def test_tree_imports_every_focus_and_prerequisites_resolve(self):
        for tag in TREES:
            container, focuses = tree(tag)
            imports = [v for k, _, v in container if k == "shared_focus"]
            self.assertEqual(len(imports), len(set(imports)), tag)
            self.assertEqual(set(focuses), set(imports), tag)
            self.assertGreaterEqual(len(focuses), 12, tag)
            for ident, nodes in focuses.items():
                self.assertTrue(ident.startswith(tag + "_"), ident)
                for ref in focus_ids(nodes, "prerequisite") + focus_ids(nodes, "mutually_exclusive"):
                    self.assertIn(ref, focuses, (ident, ref))
                for ref in focus_ids(nodes, "mutually_exclusive"):
                    self.assertIn(ident, focus_ids(focuses[ref], "mutually_exclusive"), (ident, ref))

    def test_coordinates_are_unique_and_roots_sit_on_top(self):
        for tag in TREES:
            _, focuses = tree(tag)
            seen = {}
            for ident, nodes in focuses.items():
                data = mapping(nodes)
                self.assertNotIn("relative_position_id", data, ident)
                coordinate = (int(data["x"]), int(data["y"]))
                self.assertNotIn(coordinate, seen, (ident, seen.get(coordinate)))
                seen[coordinate] = ident
                for ref in focus_ids(nodes, "prerequisite"):
                    self.assertLess(int(mapping(focuses[ref])["y"]), coordinate[1], (ident, ref))

    def test_every_focus_idea_and_tooltip_is_localised_with_bom(self):
        for tag in TREES:
            path, keys = localisation(tag)
            self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"), path)
            self.assertEqual(len(keys), len(set(keys)), path)
            _, focuses = tree(tag)
            for ident in focuses:
                self.assertIn(ident, keys)
                self.assertIn(ident + "_desc", keys)
            source = "\n".join(text(f) for f in owned_files(tag))
            for tooltip in re.findall(r"\btooltip\s*=\s*(\w+)", source):
                self.assertIn(tooltip, keys)
            focus_source = "\n".join(text(f) for f in owned_files(tag) if f.startswith("common/national_focus/"))
            for idea in re.findall(r"\badd_ideas\s*=\s*(\w+)", focus_source):
                self.assertIn(idea, keys)
                self.assertIn(idea + "_desc", keys)

    def test_added_ideas_are_defined_with_mod_pictures(self):
        sprites = set(re.findall(r'name\s*=\s*"(GFX_idea_[A-Za-z0-9_]+)"', text("interface/ac_ideas.gfx")))
        for tag in TREES:
            _, focuses = tree(tag)
            idea_file = "common/ideas/" + TREES[tag][3]
            ideas = {}
            for _, _, group in load(idea_file):
                for category, _, entries in group:
                    if category == "country":
                        ideas.update(mapping(entries))
            for ident, nodes in focuses.items():
                reward = mapping(nodes).get("completion_reward", [])
                for key, _, value in reward:
                    if key == "add_ideas":
                        self.assertIn(value, ideas, (ident, value))
                        picture = mapping(ideas[value])["picture"]
                        self.assertIn("GFX_idea_" + picture, sprites, (value, picture))

    def test_focus_icons_resolve_to_briefing_sprites_with_shine(self):
        gfx = text("interface/ac_frontend_briefing.gfx")
        sprites = {}
        for name, texture in re.findall(r'name\s*=\s*"([^"]+)"\s*texturefile\s*=\s*"([^"]+)"', gfx):
            sprites[name] = texture
        for tag in TREES:
            _, focuses = tree(tag)
            for ident, nodes in focuses.items():
                icon = mapping(nodes)["icon"]
                self.assertTrue(icon.startswith("GFX_ac_briefing_"), (ident, icon))
                self.assertIn(icon, sprites, ident)
                self.assertIn(icon + "_shine", sprites, ident)
                self.assertTrue((MOD / sprites[icon]).is_file(), (ident, sprites[icon]))

    def test_no_border_changes_leader_changes_or_late_dates(self):
        for tag in TREES:
            source = "\n".join(text(f) for f in owned_files(tag))
            for forbidden in FORBIDDEN:
                self.assertNotRegex(source, r"\b" + forbidden + r"\s*=", (tag, forbidden))
            for year in re.findall(r"\bdate\s*[<>]=?\s*(\d{4})\.", source):
                self.assertLessEqual(int(year), 2005, tag)

    def test_shared_flags_from_other_tracks_are_only_read(self):
        sources = [f for tag in TREES for f in owned_files(tag)] + ["events/Yuktobania.txt"]
        written = set()
        for relative in sources:
            for flag in SET_FLAG.findall(text(relative)):
                self.assertIsNone(FOREIGN_FLAG.match(flag), (relative, flag))
                written.add(flag)
        shared = {flag for flag in written if flag.startswith("ac_")}
        self.assertEqual(OWN_SHARED_FLAGS, shared)
        self.assertIn("set_country_flag = ac_npt_hosts_isaf", text("common/national_focus/NPT_pre_continental_war.txt"))
        self.assertIn("set_country_flag = ac_yuk_arkbird_partner", text("common/national_focus/YUK.txt"))

    def test_host_isaf_is_gated_on_isaf_formation_and_cites_the_chronicle(self):
        _, focuses = tree("NPT")
        self.assertEqual({"ac_ucw_isaf_formed"}, mentions_foreign_flag(mapping(focuses["NPT_host_isaf"])["available"]))
        _, keys = localisation("NPT")
        loc = text("localisation/english/country_NPT_l_english.yml")
        self.assertIn("2004 / 09.16", loc)
        _, yuk_focuses = tree("YUK")
        self.assertIn("1999 / 10.08", text("localisation/english/country_YUK_l_english.yml"))
        self.assertEqual("1999.10.7", mapping(mapping(yuk_focuses["YUK_arkbird_debris_talks"])["available"])["date"])

    def test_trees_stay_playable_when_other_tracks_never_set_their_flags(self):
        for tag in TREES:
            _, focuses = tree(tag)
            gated = {ident for ident, nodes in focuses.items()
                     if mentions_foreign_flag([n for n in nodes if n[0] in ("available", "bypass", "prerequisite")])}
            blocked = set(gated)
            changed = True
            while changed:
                changed = False
                for ident, nodes in focuses.items():
                    groups = [v for k, _, v in nodes if k == "prerequisite"]
                    if ident not in blocked and any(all(ref in blocked for _, _, ref in group) for group in groups):
                        blocked.add(ident)
                        changed = True
            # Gated content may only be a leaf branch; the rest of the tree,
            # including every root, must stay reachable without the flags.
            self.assertLessEqual(len(blocked), 3, (tag, sorted(blocked)))
            for ident, nodes in focuses.items():
                if not [k for k, _, _ in nodes if k == "prerequisite"]:
                    self.assertNotIn(ident, blocked, ident)

    def test_recta_links_the_postwar_local_recovery_flow(self):
        _, focuses = tree("REC")
        source = text("common/national_focus/REC.txt")
        self.assertIn("has_country_flag = ac_postwar_settlement_pending", source)
        # A Recta released before the war must not finish recovery before the
        # postwar handoff and the ac_pwi.76 briefing choice.
        available = mapping(focuses["REC_local_recovery_programme"])["available"]
        gates = [mapping(value) for key, _, value in available if key == "custom_trigger_tooltip"]
        self.assertIn("ac_postwar_contract_started", [gate.get("has_global_flag") for gate in gates])
        choices = [gate["OR"] for gate in gates if "OR" in gate]
        self.assertEqual(1, len(choices))
        self.assertEqual({"ac_pwi_choice_76_0", "ac_pwi_choice_76_1"}, {value for _, _, value in choices[0]})
        self.assertIn("ac_postwar_local_recovery", text("common/decisions/ac_continuation_decisions.txt"))
        self.assertIn("id = ac_pwi.76", text("events/ac_pwi.txt"))

    def test_yuktobania_branches_follow_the_intervention_choice(self):
        event = text("events/Yuktobania.txt")
        self.assertIn("set_country_flag = YUK_fp_intervened", event)
        self.assertIn("set_country_flag = YUK_fp_stood_aside", event)
        _, focuses = tree("YUK")
        self.assertEqual(["YUK_army_reform_commission"], focus_ids(focuses["YUK_lessons_of_the_intervention"], "mutually_exclusive"))
        for ident in ("YUK_expeditionary_command", "YUK_reformed_field_command"):
            self.assertIn("remove_ideas = yuk_top_heavy_command_structure",
                          re.search(r"id = " + ident + r"\b.*?search_filters", text("common/national_focus/YUK.txt"), re.S).group())

    def test_fiscal_effects_are_guarded(self):
        for tag in TREES:
            source = "\n".join(text(f) for f in owned_files(tag))
            calls = re.findall(r"\bac_econ_(?!ready\b)\w+\s*=\s*yes", source)
            guarded = re.findall(r"limit\s*=\s*\{\s*ac_econ_ready\s*=\s*yes\s*\}\s*ac_econ_\w+\s*=\s*yes", source)
            self.assertEqual(len(calls), len(guarded), tag)
            self.assertNotRegex(source, r"\b(?:add_to|set|subtract_from)_variable\s*=\s*\{\s*ac_econ_")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=MOD)
    args, remaining = parser.parse_known_args()
    MOD = args.mod_root.resolve()
    unittest.main(argv=[sys.argv[0]] + remaining)
