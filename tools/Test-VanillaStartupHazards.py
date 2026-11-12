"""Static checks for vanilla scripts that would address Earth map objects.

The mod keeps loading every vanilla ``common/on_actions`` file it does not
override. A vanilla file that adds province modifiers or names province IDs
beyond the Strangereal map runs against the wrong provinces, or against
provinces that do not exist. The 1.19.4 ``14_sea_on_actions.txt`` did this in
``on_startup``, and a new 1991 game crashed on its first daily tick.

N006 reproduced another first-day crash when automatic vanilla events queried
Earth-only states (including SEA_japan_news_events.03's state995). The authored
event collection must replace the vanilla directory, rather than merge with it.

The mod-side check always runs. The scan of the installed game's files runs
only with ``--reference-game-root`` (or ``ULYSSES_GAME_ROOT``) and reads that
folder without changing it. These are offline checks, not the HOI4 engine.
"""
import argparse
import os
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod/2985041246"
GAME = None

# Vanilla on_actions the mod blanks because they are Earth-only and touch provinces.
BLANKED = ("14_sea_on_actions.txt",)
PROVINCE_CONTEXT = re.compile(
    r"province\s*=\s*\{[^}]*\}|province\s*=\s*\d+|provinces\s*=\s*\{[^}]*\}|(?:prioritize_)?location\s*=\s*\d+"
)


def uncommented(path):
    return re.sub(r"#[^\n]*", "", path.read_text(encoding="utf-8-sig", errors="replace"))


def highest_province(mod):
    ids = []
    for line in (mod / "map/definition.csv").read_text(encoding="utf-8-sig", errors="replace").splitlines():
        field = line.split(";", 1)[0].strip()
        if field.isdigit():
            ids.append(int(field))
    return max(ids)


def hazards(path, limit):
    """Province modifiers and province IDs beyond the mod map in one vanilla file."""
    text = uncommented(path)
    beyond = sorted({int(n) for m in PROVINCE_CONTEXT.finditer(text) for n in re.findall(r"\d+", m[0]) if int(n) > limit})
    found = []
    if "add_province_modifier" in text:
        found.append("add_province_modifier")
    if beyond:
        found.append("province IDs beyond %d: %s" % (limit, ", ".join(map(str, beyond[:8]))))
    return found


class ModOverrides(unittest.TestCase):
    def test_authored_events_replace_earth_event_directory_in_every_descriptor(self):
        for path in (MOD / 'descriptor.mod', MOD / 'ProjectUlysses.mod',
                     MOD.parent / (MOD.name + '.mod')):
            with self.subTest(descriptor=path.name):
                self.assertRegex(uncommented(path), r'(?m)^replace_path\s*=\s*"events"\s*$')

    def test_mod_event_calls_do_not_depend_on_removed_vanilla_definitions(self):
        # Consume quoted strings/comments before looking for syntax. Descriptions
        # and comments containing event-shaped examples are not event consumers.
        token = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[A-Za-z_][A-Za-z0-9_.]*|[={}0-9]+')
        def code(path):
            return ' '.join(m[0] for m in token.finditer(path.read_text(encoding='utf-8-sig'))
                            if not m[0].startswith(('"', '#')))
        declarations = '\n'.join(code(p) for p in (MOD / 'events').glob('*.txt'))
        definitions = set(re.findall(r'\bid\s*=\s*([A-Za-z0-9_]+\.\d+)\b', declarations))
        self.assertTrue(definitions)
        unresolved = []
        for folder in ('common', 'events', 'history'):
            for path in (MOD / folder).rglob('*.txt'):
                for ident in re.findall(r'\b(?:country_event|news_event)\s*=\s*(?:\{\s*(?:id\s*=\s*)?)?([A-Za-z0-9_]+\.\d+)\b', code(path)):
                    if ident not in definitions:
                        unresolved.append((path.relative_to(MOD).as_posix(), ident))
        self.assertEqual([], unresolved)

    def test_earth_only_startup_files_are_blank(self):
        for name in BLANKED:
            with self.subTest(name=name):
                path = MOD / "common/on_actions" / name
                self.assertTrue(path.exists(), name + " must override the vanilla file")
                self.assertEqual("on_actions={}", re.sub(r"\s+", "", uncommented(path)))

    def test_province_limit_is_read_from_the_mod_map(self):
        self.assertEqual(11351, highest_province(MOD))


class InstalledGame(unittest.TestCase):
    def setUp(self):
        root = GAME or os.environ.get("ULYSSES_GAME_ROOT")
        if not root:
            self.skipTest("needs --reference-game-root or ULYSSES_GAME_ROOT")
        self.game = Path(root)
        self.folder = self.game / "common/on_actions"
        self.assertTrue(self.folder.is_dir(), "not a HOI4 install: %s" % self.game)
        self.limit = highest_province(MOD)

    def test_loaded_vanilla_on_actions_stay_off_earth_provinces(self):
        problems = {}
        for path in sorted(self.folder.glob("*.txt")):
            if (MOD / "common/on_actions" / path.name).exists():
                continue
            found = hazards(path, self.limit)
            if found:
                problems[path.name] = found
        self.assertEqual({}, problems, "override these vanilla files in mod/2985041246/common/on_actions")

    def test_blanked_files_still_exist_in_the_game(self):
        # A blank override for a file the game no longer ships is dead weight.
        for name in BLANKED:
            self.assertTrue((self.folder / name).exists(), name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=MOD)
    parser.add_argument("--reference-game-root", type=Path)
    args, remaining = parser.parse_known_args()
    MOD = args.mod_root.resolve()
    GAME = args.reference_game_root
    unittest.main(argv=[sys.argv[0]] + remaining)
