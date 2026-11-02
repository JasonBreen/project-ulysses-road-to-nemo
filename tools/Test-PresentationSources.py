"""Negative authored-source fixtures retain the required group/audio bindings."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_presentation_sources import inspect


class PresentationSources(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.mod = Path(self.temporary.name)
        names = ("GFX_group_infantry_icon", "GFX_group_mobile_icon", "GFX_group_armor_icon")
        self.put("interface/subuniticons.gfx", "spriteTypes={" + "".join('spriteType={name="'+name+'"}' for name in names) + "}")
        self.put("sound/superevents_category.asset", 'category={name="SuperEvents" soundeffects={fixture_effect}}')
        self.put("sound/effects.asset", 'soundeffect={name="fixture_effect" sounds={}}')
        self.assertTrue(inspect(self.mod)["passed"])

    def put(self, name, text):
        path = self.mod / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def test_lone_block_stray_assignment_brace_and_unterminated_quote_fail(self):
        cases = ("{", "spriteTypes={} unexpected=}", 'guiTypes={containerWindowType={name="window}}')
        for source in cases:
            with self.subTest(source=source):
                self.put("interface/invalid.gui", source)
                report = inspect(self.mod)
                self.assertFalse(report["passed"])
                self.assertTrue(any(row["path"] == "interface/invalid.gui" for row in report["failures"]))
                self.assertEqual(3, report["counter_sprite_definitions"])
                self.assertEqual(["fixture_effect"], report["superevent_category_members"])

    def test_escaped_quotes_comments_and_literal_braces_remain_valid(self):
        self.put("interface/literal.gui", r'guiTypes={containerWindowType={name="literal } \"quote\" # text"}} # { " ignored')
        self.assertTrue(inspect(self.mod)["passed"])

    def test_cli_returns_failure_even_when_all_required_bindings_survive(self):
        self.put("interface/invalid.gfx", "{")
        output = self.mod / "report.json"
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/check_presentation_sources.py"),
                                 "--mod-root", str(self.mod), "--output", str(output)], capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(json.loads(output.read_text())["passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
