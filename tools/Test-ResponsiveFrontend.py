"""Screenshot-driven geometry and eligibility regressions; no native claims."""
import copy
import importlib.util
import json
import re
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/frontend_briefing'))
from responsive import CONTRACT, MOD, VIEWPORTS, build, named, parse, get, validate, span, walk


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

    def assert_focus_previews_fit(self, gui):
        tree = parse(gui)
        entry = named(tree, 'focus_entry')
        icon = named(entry, 'icon')
        self.assertEqual('"CENTER"', get(icon, 'orientation'))
        self.assertEqual('yes', get(icon, 'centerPosition'))
        scale = float(get(icon, 'scale', '1'))
        self.assertGreater(scale, 0)
        panel = named(named(tree, 'gamesetup_interesting_countries_window'), 'focus')
        grid = named(panel, 'focus_grid')
        entry_w, entry_h = [float(get(get(entry, 'size'), k)) for k in ('width', 'height')]
        slot_w, slot_h = [float(get(get(grid, 'slotsize'), k)) for k in ('width', 'height')]
        panel_w, panel_h = [float(get(get(panel, 'size'), k)) for k in ('width', 'height')]
        capacity = int(get(get(grid, 'max_slots'), 'x'))
        self.assertLessEqual(capacity * slot_w, panel_w)
        self.assertLessEqual(slot_h, panel_h)
        self.assertLessEqual(entry_w, slot_w)
        self.assertLessEqual(entry_h, slot_h)
        previews = []
        for path in sorted((MOD / 'common/bookmarks').glob('*.txt')):
            for key, node in walk(parse(path.read_text(encoding='utf-8-sig'))):
                focuses = get(node, 'focuses')
                if focuses:
                    ids = [k for k, _, _ in focuses]
                    self.assertLessEqual(len(ids), capacity, (path.name, key))
                    previews.extend(ids)
        self.assertIn('BLK_dlp_victory', previews)
        self.assertIn('EMM_an_national_account', previews)
        wanted = set(previews)
        icons = {}
        for path in (MOD / 'common/national_focus').glob('*.txt'):
            text = path.read_text(encoding='utf-8-sig')
            if not wanted.intersection(re.findall(r'\bid\s*=\s*(\w+)', text)):
                continue
            for _, node in walk(parse(text)):
                focus_id = get(node, 'id')
                if focus_id in wanted:
                    self.assertNotIn(focus_id, icons)
                    icons[focus_id] = get(node, 'icon').strip('"')
        self.assertEqual(wanted, set(icons))
        sprites = {}
        for path in (MOD / 'interface').glob('*.gfx'):
            text = path.read_text(encoding='utf-8-sig')
            if not any(sprite in text for sprite in icons.values()):
                continue
            for kind, node in walk(parse(text)):
                sprite = get(node, 'name', '').strip('"')
                if kind.lower() == 'spritetype' and sprite in icons.values():
                    self.assertNotIn(sprite, sprites)
                    sprites[sprite] = node
        self.assertEqual(set(icons.values()), set(sprites))
        for focus_id, sprite in icons.items():
            node = sprites[sprite]
            data = (MOD / get(node, 'texturefile').strip('"')).read_bytes()
            self.assertEqual(b'DDS ', data[:4])
            h, w = struct.unpack_from('<II', data, 12)
            frames = int(get(node, 'noOfFrames', '1'))
            self.assertEqual(0, w % frames)
            self.assertLessEqual(w / frames * scale, min(entry_w, slot_w), focus_id)
            self.assertLessEqual(h * scale, min(entry_h, slot_h), focus_id)

    def test_actual_bookmark_focus_textures_fit_entries_slots_and_panel(self):
        self.assert_focus_previews_fit(self.gui)

    def test_unscaled_preview_mutations_fail_geometry_and_binding_contract(self):
        start, end = span(self.gui, 'focus_entry')
        for replacement in ('scale = 1.0', ''):
            with self.subTest(replacement=replacement):
                changed = self.gui[:start] + self.gui[start:end].replace('scale = 0.60', replacement) + self.gui[end:]
                self.assertNotEqual(self.gui, changed)
                self.assertTrue(validate(changed))
                with self.assertRaises(AssertionError):
                    self.assert_focus_previews_fit(changed)

    def assert_portrait_clear_of_selectors_and_ideas(self, gui):
        country = named(parse(gui), 'gamesetup_interesting_countries_window')
        mini = named(country, 'countries_mini')
        def position(node):
            return [float(get(get(node, 'position'), axis, '0')) for axis in ('x', 'y')]
        def dimensions(node):
            return [float(get(get(node, 'size'), axis)) for axis in ('width', 'height')]
        mini_x, mini_y = position(mini)
        mini_w, mini_h = dimensions(mini)
        # Exercise the second row, not only the first visible country selectors.
        mini_grid = named(mini, 'countries_grid')
        self.assertEqual(2 * float(get(get(mini_grid, 'slotsize'), 'height')), mini_h)
        spirit = named(country, 'spirit')
        ideas = named(spirit, 'ideas')
        spirit_x, spirit_y = position(spirit)
        ideas_x, ideas_y = position(ideas)
        ideas_w, ideas_h = dimensions(ideas)
        ideas_box = (spirit_x + ideas_x, spirit_y + ideas_y,
                     spirit_x + ideas_x + ideas_w, spirit_y + ideas_y + ideas_h)
        boxes = {}
        for control, gfx_file in [('minor_portrait_overlay', 'ac_frontend_briefing.gfx'),
                                  ('minor_country_leader', 'zz_ac_visual_scrub.gfx')]:
            node = named(country, control)
            sprite = get(node, 'spriteType', get(node, 'quadTextureSprite')).strip('"')
            binding = named(parse((MOD / 'interface' / gfx_file).read_text()), sprite)
            data = (MOD / get(binding, 'texturefile').strip('"')).read_bytes()
            self.assertEqual(b'DDS ', data[:4])
            h, w = struct.unpack_from('<II', data, 12)
            scale = float(get(node, 'scale', '1'))
            x, y = position(node)
            self.assertEqual(0, float(get(node, 'rotation', '0')))
            box = (x, y, x + w * scale, y + h * scale)
            self.assertGreaterEqual(box[1], mini_y + mini_h, control)
            self.assertTrue(box[2] <= ideas_box[0] or box[0] >= ideas_box[2] or
                            box[3] <= ideas_box[1] or box[1] >= ideas_box[3], control)
            country_w, country_h = dimensions(country)
            self.assertGreaterEqual(box[0], 0)
            self.assertLessEqual(box[2], country_w)
            self.assertLessEqual(box[3], country_h)
            boxes[control] = box
        frame, leader = boxes['minor_portrait_overlay'], boxes['minor_country_leader']
        self.assertTrue(frame[0] <= leader[0] < leader[2] <= frame[2])
        self.assertTrue(frame[1] <= leader[1] < leader[3] <= frame[3])

    def test_portrait_fits_between_two_row_selector_and_idea_strip(self):
        self.assert_portrait_clear_of_selectors_and_ideas(self.gui)

    def test_portrait_old_position_or_unscaled_downshift_fails_geometry(self):
        for replacements in [(('y = 364', 'y = 345'), ('y = 369', 'y = 350')),
                             (('scale = 0.44', 'scale = 0.50'),)]:
            with self.subTest(replacements=replacements):
                changed = self.gui
                for old, new in replacements:
                    changed = changed.replace(old, new, 1)
                self.assertNotEqual(self.gui, changed)
                self.assertTrue(validate(changed))
                with self.assertRaises(AssertionError):
                    self.assert_portrait_clear_of_selectors_and_ideas(changed)

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
