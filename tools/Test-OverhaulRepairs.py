"""Regression checks for the screenshot repairs, separate from native acceptance."""
import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
sys.path.insert(0, str(ROOT / 'tools/anea'))
sys.path.insert(0, str(ROOT / 'tools/overhaul'))
from script import get, parse
from build_briefs_ui import country_window, normalize_for_fingerprint, remove_overview
from build_overview import strip_inline_maps


class OverhaulRepairs(unittest.TestCase):
    def setUp(self):
        self.gui = (MOD / 'interface/frontendgamesetupview.gui').read_text(encoding='utf-8-sig')

    def test_map_is_a_separate_bounded_noninteractive_layer_behind_country_controls(self):
        _, controls = country_window(self.gui)
        node = controls['ac_overhaul_world_overview']
        self.assertEqual('yes', get(node, 'alwaystransparent'))
        self.assertEqual('"GFX_ac_overhaul_world_overview"', get(node, 'spriteType'))
        x, y = (int(get(get(node, 'position'), k)) for k in ('x', 'y'))
        manifest = json.loads((ROOT / 'tools/overhaul/overview_assets.json').read_text())
        self.assertGreaterEqual(x, 0)
        self.assertGreaterEqual(y, -316)
        self.assertLessEqual(x + manifest['width'], 1225)
        self.assertLess(y + manifest['height'], int(get(get(controls['countries_mini'], 'position'), 'y')))
        self.assertLess(self.gui.index('name = "ac_overhaul_world_overview"'),
                        self.gui.index('name ="countries"', self.gui.index('gamesetup_interesting_countries_window')))
        self.assertNotIn('name = "ac_briefing_map_statistics"', self.gui)

    def test_overview_controls_are_not_a_broad_fingerprint_exemption(self):
        for old, new in [('x = 14 y = -304', 'x = 14 y = -305'),
                         ('"GFX_ac_overhaul_world_overview"', '"GFX_missing"'),
                         ('"ac_overhaul_overview_note"', '"missing_note"')]:
            with self.subTest(change=old):
                changed = self.gui.replace(old, new, 1)
                self.assertNotEqual(changed, self.gui)
                with self.assertRaises(ValueError):
                    normalize_for_fingerprint(changed)
        self.assertNotIn('ac_overhaul_world_overview', remove_overview(self.gui, required=True))

    def test_legacy_map_removal_preserves_every_narrative_character(self):
        sample = '\ufeffl_english:\n BLK_GATHERING_STORM_DESC:0 "£GFX_map_belka_map\\nFull narrative, £GFX_other and \\"quotation\\"."\n'
        expected = sample.replace('£GFX_map_belka_map\\n', '')
        self.assertEqual(expected, strip_inline_maps(sample))
        self.assertEqual(expected, strip_inline_maps(expected))
        text = (MOD / 'localisation/english/bookmarks_l_english.yml').read_text(encoding='utf-8-sig')
        self.assertNotRegex(text, r'£GFX_map_\w+_map')

    def test_overview_is_packaged_and_records_only_mod_geography_sources(self):
        manifest = json.loads((ROOT / 'tools/overhaul/overview_assets.json').read_text())
        texture = MOD / manifest['file']
        with Image.open(texture) as image:
            self.assertEqual((1197, 594), image.size)
        self.assertEqual(manifest['sha256'], hashlib.sha256(texture.read_bytes()).hexdigest())
        self.assertEqual('mod provenance', manifest['source_layer'])
        self.assertGreater(len(manifest['sources']), 600)
        for row in manifest['sources']:
            self.assertTrue(row['file'].startswith('mod/2985041246/'))
            self.assertEqual(row['sha256'], hashlib.sha256((ROOT / row['file']).read_bytes()).hexdigest())
        prose = MOD / 'localisation/english/ac_overhaul_frontend_l_english.yml'
        self.assertTrue(prose.read_bytes().startswith(b'\xef\xbb\xbf'))
        for key in ('AC_OVERHAUL_OVERVIEW_TITLE', 'AC_OVERHAUL_OVERVIEW_NOTE'):
            self.assertIn(key + ':0', prose.read_text(encoding='utf-8-sig'))

    def test_overview_generation_is_reproducible(self):
        result = subprocess.run([sys.executable, '-B', 'tools/overhaul/build_overview.py', '--check'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_regional_labels_resolve_screenshot_placeholders_without_geography_changes(self):
        manifest = json.loads((ROOT / 'tools/overhaul/regional_labels.json').read_text())
        changes = {row['key']: row for row in manifest['changes']}
        self.assertEqual('Amber Capital District', changes['STATE_501']['value'])
        for province in (6090, 8727, 4655, 8579, 8569, 2371, 9069, 3274, 8782):
            row = changes['VICTORY_POINTS_' + str(province)]
            self.assertNotRegex(row['value'], r'^\d+$|TEMP')
            self.assertEqual('provisional gameplay', row['source_layer'])
            self.assertIsNotNone(row['state'])
            self.assertNotEqual(171, row['state'])
        self.assertNotIn('STATE_171', changes)
        for row in manifest['changes']:
            self.assertFalse(row['key'].startswith('STRATEGICREGION'))
        # The effective replacement layer takes precedence over inherited text.
        path = MOD / 'localisation/english/replace/ac_overhaul_regions_l_english.yml'
        effective = dict(re.findall(r'^\s*(\w+):\d+\s+"([^\n]*)"', path.read_text(encoding='utf-8-sig'), re.M))
        self.assertEqual({key: row['value'] for key, row in changes.items()}, effective)
        result = subprocess.run([sys.executable, '-B', 'tools/overhaul/build_regional_labels.py', '--check'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_fiscal_pages_have_disjoint_direct_control_visibility(self):
        from script import walk
        gui = parse((MOD / 'interface/ac_economy_gui.gui').read_text())
        windows = {get(n, 'name', '').strip('"'): n for _, n in walk(gui)}
        logic = get(get(parse((MOD / 'common/scripted_guis/ac_economy.txt').read_text()),
                        'scripted_gui'), 'project_ulysses_economy_screen')
        triggers = get(logic, 'triggers')
        for key, _, trigger in triggers:
            if not key.endswith('_visible') or not get(trigger, 'check_variable'):
                continue
            name = key.removesuffix('_visible')
            self.assertIn(name, windows)
            self.assertEqual('yes', get(trigger, 'ac_econ_ready'))
            condition = get(trigger, 'check_variable')
            self.assertEqual(1, len(condition))
            self.assertEqual('ac_econ_ui_tab', condition[0][0])
            self.assertIn(condition[0][2], ('0', '1', '2'))
        window = windows['project_ulysses_economy_screen']
        self.assertFalse(any(k == 'containerWindowType' and get(n, 'name', '').strip('"') in
                             ('overview_panel', 'budget_panel', 'contracts_panel')
                             for k, _, n in window if isinstance(n, list)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
