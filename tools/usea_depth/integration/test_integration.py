"""Cross-package checks for Usea Depth, once all six packages are merged.

Each package test checks its own files. This one checks what only shows up
when the packages sit together in one mod:
- definitions, events, sprites and localisation keys stay unique across the mod;
- flags and scripted calls resolve;
- every new focus is imported once;
- the totals in release_plan.json match the packages' own budgets.

Static and offline: no HOI4 launch, parser, save/load or AI run.
"""
import json
import re
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from usea_depth import seams  # noqa: E402

MOD = ROOT / "mod/2985041246"
DEPTH = json.loads((ROOT / "tools/overhaul/release_plan.json").read_text(encoding="utf-8"))["approved_expansions"]["usea_depth"]
PACKAGES = DEPTH["packages"]
NAMESPACES = {"eru": "ac_ud_eru", "fcu": "ac_ud_fcu", "npt": "ac_ud_npt", "partners": "ac_ud_up",
              "minors_a": "ac_ud_mina", "minors_b": "ac_ud_minb"}
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[^\s{}=]+|=')
FOCUS_ID = re.compile(r"\b[A-Z][A-Z0-9]{2}_ud_\w+")


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace")


def code(path):
    return re.sub(r"#[^\n]*", "", read(path))


def owner(path):
    """The Usea Depth package that owns a file, or None for the rest of the mod."""
    stem = path.stem.replace("_l_english", "")
    if not stem.startswith("ac_ud_"):
        return None
    if stem.startswith("ac_ud_minor_"):
        tag = stem[len("ac_ud_minor_"):].upper()
        return next(name for name, row in PACKAGES.items() if tag in row["tags"])
    return stem[len("ac_ud_"):]


def openings(text, depth):
    """Names of `name = {` blocks that open at the given brace depth."""
    names, level, previous = [], 0, []
    for token in TOKEN.findall(text):
        if token.startswith("#"):
            continue
        if token == "{":
            if level == depth and len(previous) == 2 and previous[1] == "=":
                names.append(previous[0])
            level += 1
        elif token == "}":
            level -= 1
        previous = (previous + [token])[-2:]
    return names


def definitions(folder, depth, pattern="*.txt"):
    found = defaultdict(list)
    for path in sorted((MOD / folder).glob(pattern)):
        for name in openings(code(path), depth):
            found[name].append(path)
    return found


def ud_files(*folders, pattern="ac_ud_*"):
    return [p for folder in folders for p in sorted((MOD / folder).glob(pattern)) if p.is_file()]


class Totals(unittest.TestCase):
    def test_every_approved_package_is_merged_with_a_budget(self):
        budgets = {p.parent.name: json.loads(p.read_text(encoding="utf-8")) for p in ROOT.glob(DEPTH["addenda_glob"])}
        self.assertEqual(set(PACKAGES), set(budgets))
        delivered = DEPTH.get("delivered")
        self.assertIsNotNone(delivered, "record the merged totals under approved_expansions.usea_depth.delivered")
        self.assertEqual(sum(sum(b["focuses"].values()) for b in budgets.values()), delivered["focuses"])
        self.assertEqual(sum(b["events"] for b in budgets.values()), delivered["events"])
        self.assertEqual({k: sum(b["focuses"].values()) for k, b in budgets.items()}, delivered["focuses_by_package"])


class Uniqueness(unittest.TestCase):
    def assert_unique(self, found):
        clashes = {name: sorted({p.name for p in paths}) for name, paths in found.items()
                   if len(paths) > 1 and any(owner(p) for p in paths)}
        self.assertEqual({}, clashes)

    def test_scripted_effects_and_triggers(self):
        self.assert_unique(definitions("common/scripted_effects", 0))
        self.assert_unique(definitions("common/scripted_triggers", 0))

    def test_ideas_characters_and_decisions(self):
        self.assert_unique(definitions("common/ideas", 2))
        self.assert_unique(definitions("common/characters", 1))
        self.assert_unique(definitions("common/decisions", 1))
        self.assert_unique(definitions("common/decisions/categories", 0))

    def test_focus_ids_are_defined_once_and_imported_once(self):
        defined, imported = Counter(), Counter()
        for path in sorted((MOD / "common/national_focus").glob("*.txt")):
            text = code(path)
            defined.update(FOCUS_ID.findall(" ".join(re.findall(r"\bid\s*=\s*(\w+)", text))))
            imported.update(re.findall(r"(?m)^\s*shared_focus\s*=\s*([A-Z][A-Z0-9]{2}_ud_\w+)\s*$", text))
        self.assertEqual([], sorted(i for i, n in defined.items() if n > 1))
        self.assertEqual([], sorted(i for i, n in imported.items() if n > 1))
        self.assertEqual([], sorted(set(imported) - set(defined)))

    def test_events_use_their_own_namespace_once(self):
        ids, spaces = Counter(), defaultdict(list)
        for path in sorted((MOD / "events").glob("*.txt")):
            text = code(path)
            ids.update(re.findall(r"\bid\s*=\s*(ac_ud_\w+\.\d+)", text))
            for space in re.findall(r"(?m)^\s*add_namespace\s*=\s*(\w+)", text):
                spaces[space].append(path.name)
        self.assertEqual([], sorted(i for i, n in ids.items() if n > 1))
        for package, space in NAMESPACES.items():
            with self.subTest(package=package):
                self.assertEqual(["ac_ud_%s.txt" % package], spaces.get(space))
                self.assertTrue(all(i.split(".")[0] in NAMESPACES.values() for i in ids))

    def test_sprites_are_defined_once_and_every_used_sprite_exists(self):
        names = Counter()
        for path in sorted((MOD / "interface").glob("*.gfx")):
            names.update(re.findall(r'name\s*=\s*"?(GFX_ac_ud_\w+)', code(path)))
        self.assertEqual([], sorted(n for n, c in names.items() if c > 1))
        used = set()
        for path in ud_files("common/national_focus", "common/ideas", "common/decisions", "events", pattern="ac_ud_*.txt"):
            used.update(re.findall(r"\b(GFX_ac_ud_\w+)", code(path)))
        self.assertEqual([], sorted(u for u in used if u not in names and u + "_shine" not in names))

    def test_localisation_keys_are_defined_in_one_file(self):
        keys = defaultdict(list)
        for path in sorted((MOD / "localisation/english").rglob("*.yml")):
            for key in re.findall(r'(?m)^\s*([\w.\-]+):\d*\s+"', read(path)):
                keys[key].append(path)
        clashes = {k: sorted(p.name for p in v) for k, v in keys.items() if len(v) > 1 and any(owner(p) for p in v)}
        self.assertEqual({}, clashes)


class References(unittest.TestCase):
    def setUp(self):
        self.mod_text = "\n".join(code(p) for p in sorted(MOD.rglob("*.txt")))

    def test_ud_flags_that_are_checked_are_set_somewhere(self):
        checked = set()
        for path in ud_files("common/national_focus", "common/ideas", "common/decisions", "common/scripted_effects",
                             "common/scripted_triggers", "common/on_actions", "events", pattern="ac_ud_*.txt"):
            text = code(path)
            checked.update(re.findall(r"has_(?:country|global|state)_flag\s*=\s*(\w*_ud_\w*)", text))
            checked.update(re.findall(r"has_(?:country|global|state)_flag\s*=\s*\{[^}]*?\bflag\s*=\s*(\w*_ud_\w*)", text))
        set_flags = set(re.findall(r"set_(?:country|global|state)_flag\s*=\s*(\w+)", self.mod_text))
        set_flags.update(re.findall(r"set_(?:country|global|state)_flag\s*=\s*\{[^}]*?\bflag\s*=\s*(\w+)", self.mod_text))
        self.assertEqual([], sorted(checked - set_flags))

    def test_scripted_calls_resolve(self):
        known = set(definitions("common/scripted_effects", 0)) | set(definitions("common/scripted_triggers", 0))
        calls = set()
        for path in ud_files("common/national_focus", "common/ideas", "common/decisions", "common/scripted_effects",
                             "common/scripted_triggers", "common/on_actions", "events", pattern="ac_ud_*.txt"):
            calls.update(re.findall(r"\b(ac_\w+)\s*=\s*(?:yes|no)\b", code(path)))
        self.assertEqual([], sorted(calls - known))


class Wrappers(unittest.TestCase):
    def test_every_marker_block_survives_in_every_wrapper(self):
        for package, (name, files) in seams.MARKERS.items():
            for file in files:
                with self.subTest(package=package, file=file):
                    blocks = [n for n, _, _ in seams.import_blocks(read(seams.FOCUS / file))]
                    self.assertEqual(1, blocks.count(name))


if __name__ == "__main__":
    unittest.main()
