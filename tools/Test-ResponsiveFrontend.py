"""Screenshot-driven geometry and eligibility regressions; no native claims."""
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/frontend_briefing'))
from responsive import CONTRACT, MOD, VIEWPORTS, build, named, parse, get, validate


class ResponsiveFrontend(unittest.TestCase):
    def setUp(self):
        self.gui = (MOD / 'interface/frontendgamesetupview.gui').read_text()

    def test_actual_windows_fit_all_eight_supported_viewports_and_scale_pairs(self):
        self.assertEqual(8, len(VIEWPORTS))
        self.assertEqual([], validate(self.gui))
        self.assertEqual(self.gui, build(self.gui))

    def test_oversized_bookmarks_missing_controls_scroll_and_frame_changes_fail(self):
        for old, new in [('width = 250', 'width = 2000%%'),
                         ('height = 620', 'height = 1200'),
                         ('name = "country_name"', 'name = "lost_country_name"'),
                         ('scale = 0.45', 'scale = 1.0'),
                         ('scrollbarType = "ac_exp_standardtext_slider"', ''),
                         ('"GFX_ac_overhaul_world_overview"', '"GFX_missing"')]:
            altered = self.gui.replace(old, new, 1)
            self.assertTrue(altered != self.gui, old)
            try:
                result = validate(altered)
            except ValueError:
                result = ['missing binding']
            self.assertTrue(result, old)

    def test_background_uses_installed_engine_percentage_and_cover_constraints(self):
        node = named(parse((MOD / 'interface/frontendmainview.gui').read_text()), 'frontend_background')
        box = get(node, 'size')
        self.assertEqual('100%', get(get(box, 'min'), 'width'))
        self.assertEqual('100%', get(get(box, 'min'), 'height'))
        self.assertEqual('100%', get(get(box, 'max'), 'width'))
        self.assertEqual('yes', get(box, 'preserve_aspect_ratio'))
        for w, h, scale in VIEWPORTS:
            cover = max(w / scale / 1920, h / scale / 1080)
            self.assertGreaterEqual(1920 * cover + 1e-6, w / scale)
            self.assertGreaterEqual(1080 * cover + 1e-6, h / scale)

    def test_profile_tooltip_has_identical_truth_for_all_tags_and_an_unsupported_tag(self):
        spec = importlib.util.spec_from_file_location('responsive_institutions', ROOT / 'tools/Test-Institutions.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        world = module.World().init()
        tags = {r['tag'] for r in json.loads((ROOT / 'tools/institutions/profiles.json').read_text())}
        trigger = world.triggers['ac_pol_profiled']
        self.assertEqual(['custom_trigger_tooltip'], [k for k, _, _ in trigger])
        self.assertEqual('ac_pol_profiled_tt', get(trigger[0][2], 'tooltip'))
        for country in world.countries.values():
            self.assertEqual(country.original_tag in tags, world.trigger(trigger, country))
        country = next(iter(world.countries.values()))
        country.original_tag = 'ZZZ'
        self.assertFalse(world.trigger(trigger, country))


if __name__ == '__main__':
    unittest.main(verbosity=2)
