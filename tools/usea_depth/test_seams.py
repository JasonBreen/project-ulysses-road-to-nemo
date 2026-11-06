"""Static checks that every owner generator keeps a foreign Usea Depth import block.

Each owner runs in its own interpreter, because several packages use a module
named content. Nothing on disk is changed: the foreign block is supplied by
patching the seams lookups or a temporary copy of the wrapper.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from usea_depth import seams  # noqa: E402

TREE = "focus_tree = {\n\tid = demo\n\tfocus = {\n\t\tid = demo_a\n\t}\n\tshared_focus = demo_b\n}\n"
CAMPAIGN = "\t# BEGIN AC CAMPAIGNS IMPORTS\n\tshared_focus = demo_camp\n\t# END AC CAMPAIGNS IMPORTS\n"


def run(code, cwd=ROOT):
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "tools"), str(ROOT / "tools/usea_expansion")]))
    result = subprocess.run([sys.executable, "-B", "-c", code], cwd=cwd, env=env, capture_output=True, text=True)
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return json.loads(result.stdout.strip().splitlines()[-1])


class Seams(unittest.TestCase):
    def test_attach_adds_before_the_closing_brace_and_replaces_in_place(self):
        once = seams.attach(TREE, "USEA DEPTH ERUSEA", ["ERU_ud_a", "ERU_ud_b"])
        self.assertTrue(once.endswith("\tshared_focus = demo_b\n\t# BEGIN USEA DEPTH ERUSEA IMPORTS\n\tshared_focus = ERU_ud_a\n\tshared_focus = ERU_ud_b\n\t# END USEA DEPTH ERUSEA IMPORTS\n}\n"))
        twice = seams.attach(once, "USEA DEPTH ERUSEA", ["ERU_ud_c"])
        self.assertEqual(1, twice.count("# BEGIN USEA DEPTH ERUSEA IMPORTS"))
        self.assertIn("shared_focus = ERU_ud_c", twice)
        self.assertNotIn("ERU_ud_a", twice)
        self.assertEqual(twice, seams.attach(twice, "USEA DEPTH ERUSEA", ["ERU_ud_c"]))

    def test_attach_goes_before_campaign_imports(self):
        tree = TREE[:-2] + CAMPAIGN + "}\n"
        text = seams.attach(tree, "USEA DEPTH PARTNERS", ["SNS_ud_a"])
        self.assertLess(text.index("USEA DEPTH PARTNERS"), text.index("AC CAMPAIGNS"))
        self.assertEqual(["USEA DEPTH PARTNERS", "AC CAMPAIGNS"], [n for n, _, _ in seams.import_blocks(text)])

    def test_malformed_or_reserved_blocks_are_rejected(self):
        with self.assertRaises(ValueError):
            seams.import_blocks(TREE.replace("}\n", "\t# BEGIN BROKEN IMPORTS\n\tshared_focus = x\n}\n"))
        with self.assertRaises(ValueError):
            seams.attach(TREE, "AC CAMPAIGNS", ["x"])
        with self.assertRaises(ValueError):
            seams.attach(TREE, "lower case", ["x"])
        with self.assertRaises(ValueError):
            seams.attach(TREE, "USEA DEPTH ERUSEA", ["x", "x"])

    def test_attach_file_keeps_bom_and_line_endings(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "TREE.txt"
            path.write_bytes(b"\xef\xbb\xbf" + TREE.replace("\n", "\r\n").encode())
            self.assertFalse(seams.attach_file(path, "USEA DEPTH NORTH POINT", ["NPT_ud_a"], check=True))
            self.assertEqual(b"\xef\xbb\xbf" + TREE.replace("\n", "\r\n").encode(), path.read_bytes())
            self.assertFalse(seams.attach_file(path, "USEA DEPTH NORTH POINT", ["NPT_ud_a"]))
            data = path.read_bytes()
            self.assertTrue(data.startswith(b"\xef\xbb\xbf"))
            self.assertNotIn(b"\n", data.replace(b"\r\n", b""))
            self.assertTrue(seams.attach_file(path, "USEA DEPTH NORTH POINT", ["NPT_ud_a"], check=True))

    def test_long_event_and_politics_rules(self):
        short = seams.event_text(["One paragraph."], "Provisional gameplay")
        self.assertIn("fewer than 3 paragraphs", seams.event_problems(short))
        long = seams.event_text([" ".join(["word"] * 70)] * 3, "Official", "ACES Chronicle 1996 / 04.20")
        self.assertEqual([], seams.event_problems(long))
        name, effect = seams.regime_effect("eru", "constitution", "democratic", "ERU_ud_cabinet_office", "conservatism", True)
        self.assertEqual("ac_ud_eru_regime_constitution", name)
        self.assertEqual([], seams.political_violations(effect))
        self.assertEqual(["ac_ud_eru_reward"], seams.political_violations("ac_ud_eru_reward = {\n\tset_politics = { ruling_party = fascism }\n}\n"))
        self.assertEqual(["set_global_flag = ac_ucw_"], seams.banned_uses("set_global_flag = ac_ucw_war_started"))

    def test_opening_trees_keep_foreign_blocks(self):
        # build_content.py writes ERU_opening.txt and FCU_opening.txt in full.
        code = r'''
import json, sys
sys.path.insert(0, "tools/usea_expansion"); sys.path.insert(0, "tools")
import build_content as b
block = "\t# BEGIN USEA DEPTH TEST IMPORTS\n\tshared_focus = TEST_ud_node\n\t# END USEA DEPTH TEST IMPORTS\n"
b.foreign_import_blocks = lambda path: [block] if path.name.endswith("_opening.txt") else []
b.shared_nodes = lambda ids: {"TEST_ud_node": [("id", "=", "TEST_ud_node"), ("x", "=", "23"), ("y", "=", "9")]}
b.build_trees()
out = {k: v for k, v in b.OUT.items() if k.endswith("_opening.txt")}
print(json.dumps({k: [v.count(block), v.rstrip().endswith(block + "}"), "x = 2592" in v] for k, v in out.items()}))
'''
        result = run(code)
        self.assertEqual({"common/national_focus/ERU_opening.txt": [1, True, True],
                          "common/national_focus/FCU_opening.txt": [1, True, True]}, result)

    def test_opening_tree_panel_bound_is_enforced(self):
        code = r'''
import json, sys
sys.path.insert(0, "tools/usea_expansion"); sys.path.insert(0, "tools")
import build_content as b
block = "\t# BEGIN USEA DEPTH TEST IMPORTS\n\tshared_focus = TEST_ud_node\n\t# END USEA DEPTH TEST IMPORTS\n"
b.foreign_import_blocks = lambda path: [block]
b.shared_nodes = lambda ids: {"TEST_ud_node": [("id", "=", "TEST_ud_node"), ("x", "=", "24"), ("y", "=", "9")]}
try:
    b.build_trees(); print(json.dumps("built"))
except SystemExit as error:
    print(json.dumps(str(error)))
'''
        self.assertIn("keep x <= 23", run(code))

    def test_partner_trees_keep_foreign_blocks_before_campaigns(self):
        code = r'''
import json, sys
sys.path.insert(0, "tools")
from usea_depth import seams
block = "\t# BEGIN USEA DEPTH TEST IMPORTS\n\tshared_focus = TEST_ud_node\n\t# END USEA DEPTH TEST IMPORTS\n"
seams.foreign_import_blocks = lambda path, own=(): [block]
import build
out = build.outputs()
trees = {k: v for k, v in out.items() if k.startswith("common/national_focus/")}
print(json.dumps({k: [v.count(block), v.index(block) < v.index("# BEGIN AC CAMPAIGNS IMPORTS")] for k, v in trees.items()}))
'''
        result = run(code, cwd=ROOT / "tools/usean_partners")
        self.assertEqual({"common/national_focus/%s.txt" % t: [1, True] for t in ("SNS", "AMB", "UGE", "DEL")}, result)

    def test_war_trees_keep_foreign_blocks(self):
        # build_continental_war.py preserves every marker block in ERU.txt and FCU.txt.
        code = r'''
import importlib.util, json, pathlib, shutil, sys, tempfile
spec = importlib.util.spec_from_file_location("cw", "tools/build_continental_war.py")
cw = importlib.util.module_from_spec(spec); spec.loader.exec_module(cw)
sys.path.insert(0, "tools")
from usea_depth import seams
folder = pathlib.Path(tempfile.mkdtemp())
(folder / "common/national_focus").mkdir(parents=True)
result = {}
for tag in ("ERU", "FCU"):
    source = (cw.MOD / ("common/national_focus/%s.txt" % tag)).read_text(encoding="utf-8")
    (folder / ("common/national_focus/%s.txt" % tag)).write_text(seams.attach(source, "USEA DEPTH TEST", ["TEST_ud_node"]), encoding="utf-8")
cw.MOD = folder
for tag in ("ERU", "FCU"):
    kept = cw.preserved_imports(tag)
    result[tag] = ["USEA DEPTH TEST" in kept, kept.index("USEA DEPTH TEST") < kept.index("AC CAMPAIGNS")]
shutil.rmtree(folder)
print(json.dumps(result))
'''
        self.assertEqual({"ERU": [True, True], "FCU": [True, True]}, run(code))

    def test_campaign_attach_and_north_point_support_keep_foreign_blocks(self):
        code = r'''
import json, sys
sys.path.insert(0, "tools/usea_expansion"); sys.path.insert(0, "tools")
from ac_campaigns.imports import attach
from usea_depth import seams
import build_content as b
tree = "focus_tree = {\n\tid = demo\n\tshared_focus = demo_b\n}\n"
tree = seams.attach(tree, "USEA DEPTH TEST", ["TEST_ud_node"])
campaign = attach(tree, ["demo_camp"])
npt = (b.MOD / "common/national_focus/NPT.txt").read_text(encoding="utf-8-sig")
npt = seams.attach(npt, "USEA DEPTH TEST", ["TEST_ud_node"])
support = b.remove_owned_support(npt, [r for r in b.FOCUSES if r.tag == "NPT" and r.phase == "support"])
print(json.dumps(["USEA DEPTH TEST" in campaign, campaign.index("USEA DEPTH TEST") < campaign.index("AC CAMPAIGNS"), support.count("# BEGIN USEA DEPTH TEST IMPORTS")]))
'''
        self.assertEqual([True, True, 1], run(code))

    def test_markers_name_existing_wrappers(self):
        for package, (name, files) in seams.MARKERS.items():
            with self.subTest(package=package):
                self.assertRegex(name, r"^USEA DEPTH [A-Z ]+$")
                for file in files:
                    path = seams.FOCUS / file
                    self.assertTrue(path.exists(), file)
                    seams.import_blocks(path.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
