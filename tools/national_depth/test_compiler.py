"""Compiler regressions for tools/national_depth (offline; Pillow 11.3.0).

    python -B tools/national_depth/test_compiler.py                  # run
    python -B tools/national_depth/test_compiler.py --record-golden  # after a reviewed compiler change
"""
import dataclasses
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import types
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / 'tools/usea_depth'), str(ROOT / 'tools/usea_expansion')]
import art  # noqa: E402
from compile import compile_country, institutional_block  # noqa: E402
import focus_layout  # noqa: E402
import lint  # noqa: E402
import seams  # noqa: E402
import spec as S  # noqa: E402
from PIL import Image  # noqa: E402

GOLDEN = HERE / 'golden.json'


def fixture():
    loader = importlib.util.spec_from_file_location('national_depth_fixture', HERE / 'fixtures/fixture_spec.py')
    module = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(module)
    return module


def variant(**changes):
    base = fixture()
    module = types.SimpleNamespace(**{k: getattr(base, k) for k in ('COUNTRY', 'SOURCES', 'IDEAS', 'EVENTS', 'OFFICES', 'BRANCHES')})
    for key, value in changes.items():
        setattr(module, key, value)
    return module


def digest(relative, data):
    if relative.endswith('.dds'):
        with Image.open(io.BytesIO(data)) as image:
            return 'rgba:' + hashlib.sha256(image.convert('RGBA').tobytes()).hexdigest()
    return hashlib.sha256(data).hexdigest()


def golden_record():
    outputs, *_ = compile_country(fixture())
    return {relative: digest(relative, data) for relative, data in sorted(outputs.items())}


class Compiler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        art.require_pinned_pillow()
        cls.outputs, cls.budget, cls.assets, cls.positions = compile_country(fixture())

    def test_fixture_matches_the_golden_output(self):
        self.assertEqual(json.loads(GOLDEN.read_text(encoding='utf-8')), golden_record())

    def test_layout_is_compact_on_screen_and_clear_of_the_panel(self):
        country = fixture().COUNTRY
        rows = {}
        for key, (x, y) in self.positions.items():
            self.assertTrue(0 <= x <= country.max_columns and y >= 12, key)
            rows.setdefault(y, []).append(x)
        for xs in rows.values():
            xs.sort()
            self.assertTrue(all(b - a >= 2 for a, b in zip(xs, xs[1:])))
        ids, block = institutional_block()
        nodes = dict(block)
        nodes.update({'DOR_ud_' + k: v for k, v in self.positions.items()})
        geometry = focus_layout.gui_geometry()
        panel = tuple(self.budget['panel'])
        self.assertEqual([], focus_layout.overlaps(nodes, panel, geometry))
        self.assertEqual(focus_layout.panel_position(nodes, geometry), panel)
        self.assertEqual(36, len(ids))

    def test_tree_imports_the_institutional_block_and_assigns_the_country(self):
        tree = self.outputs['common/national_focus/ac_ud_minor_dor.txt'].decode()
        self.assertIn('modifier = { add = 50 tag = DOR original_tag = DOR }', tree)
        for ident in institutional_block()[0]:
            self.assertIn('shared_focus = %s\n' % ident, tree)
        self.assertIn('mutually_exclusive = {\n\t\t\tfocus = DOR_ud_rail_spurs', tree)
        self.assertIn('mutually_exclusive = {\n\t\t\tfocus = DOR_ud_rail_gauge', tree)

    def test_politics_only_through_regime_effects_with_ai_zero(self):
        effects = self.outputs['common/scripted_effects/ac_ud_dor.txt'].decode()
        self.assertEqual([], seams.political_violations(effects))
        tree = self.outputs['common/national_focus/ac_ud_minor_dor.txt'].decode()
        council = tree[tree.index('id = DOR_ud_works_council'):]
        council = council[:council.index('completion_reward')]
        self.assertIn('factor = 0', council)
        for relative, data in self.outputs.items():
            if relative.endswith('.txt'):
                self.assertEqual([], seams.banned_uses(data.decode()), relative)
                if 'scripted_effects' not in relative:
                    self.assertNotIn('set_politics', data.decode(), relative)

    def test_every_key_is_localised_with_a_bom(self):
        yml = self.outputs['localisation/english/ac_ud_dor_l_english.yml']
        self.assertTrue(yml.startswith(b'\xef\xbb\xbf'))
        keys = set(re.findall(r'^ ([^:\s]+):0 ', yml.decode('utf-8-sig'), re.M))
        text = ''.join(d.decode() for r, d in self.outputs.items() if r.endswith('.txt'))
        wanted = set(re.findall(r'\bid = (DOR_ud_\w+)', text)) | set(re.findall(r'\b(DOR_ud_\w+_office)\b', text))
        wanted |= {w + '_desc' for w in wanted if not w.endswith('_tt_1')}
        wanted |= set(re.findall(r'(?:title|desc|name) = (ac_ud_dor\.\d+\.[a-z])\b', text))
        wanted |= set(re.findall(r'custom_effect_tooltip = (\S+)', text))
        wanted |= set(re.findall(r'set_country_flag = (DOR_ud_\w+)', text))
        self.assertEqual(set(), wanted - keys)
        self.assertIn('ac_ud_dor_tree', keys)

    def test_every_sprite_has_a_texture_and_icons_are_unique(self):
        gfx = self.outputs['interface/ac_ud_dor.gfx'].decode()
        for name, texture in re.findall(r'name = "(GFX_\w+)" texturefile = "([^"]+)"', gfx):
            self.assertIn(texture, self.outputs, name)
        icons = [digest(r, d) for r, d in self.outputs.items() if '/focus/' in r]
        self.assertEqual(len(icons), len(set(icons)))
        self.assertEqual(8, len(icons))

    def test_validation_rejects_effects_outside_the_catalogue(self):
        base = fixture()
        first = base.BRANCHES[0]

        def with_focus(**changes):
            focus = dataclasses.replace(first.focuses[0], **changes)
            return variant(BRANCHES=(dataclasses.replace(first, focuses=(focus,) + first.focuses[1:]),) + base.BRANCHES[1:])
        cases = [
            (with_focus(icon=('dragon', 'document')), 'unknown icon subject'),
            (with_focus(cost=7), 'cost must be 5 or 10'),
            (with_focus(reward=(S.Build('infrastructure', state=1),)), 'outside the 1991 states'),
            (with_focus(reward=(S.Build('nuclear_reactor'),)), 'bad building'),
            (with_focus(reward=(S.Research('magic'),)), 'bad research'),
            (with_focus(reward=(S.Regime('junta'),)), 'unknown office'),
            (with_focus(reward=(S.Idea('missing'),)), 'unknown idea'),
            (with_focus(after=('nowhere',)), 'unknown focus reference'),
            (with_focus(title='A "quoted" title'), 'ASCII text without double quotes'),
            (variant(IDEAS=(S.IdeaDef('rail_board', 'Rail Board', 'x', {'max_planning': 0.1}),) + base.IDEAS[1:]), 'unknown modifier'),
            (variant(IDEAS=(S.IdeaDef('rail_board', 'Rail Board', 'x', {'stability_factor': 0.5}),) + base.IDEAS[1:]), 'beyond'),
            (variant(EVENTS=(dataclasses.replace(base.EVENTS[0], paragraphs=('Too short.',)),)), 'fewer than'),
            (variant(OFFICES=(dataclasses.replace(base.OFFICES[0], ideology='despotism'),)), 'unknown party or sub-ideology'),
        ]
        for module, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, re.escape(message)):
                    compile_country(module)

    def test_lint_catches_filler_and_borrowed_text(self):
        base = fixture()
        words = ('The river towns agreed to measure every bridge on the line and publish the measurements with their cost so that '
                 'the next council can see what was bought and why it was needed and who signed the order for it in the hall')
        long = lambda n: words + ' ' + ' '.join('detail%d' % i for i in range(n))  # noqa: E731
        focuses = [S.Focus('item_%d' % i, 'Item %d' % i, long(i), ('rail', 'document'), reward=(S.PP(10),)) for i in range(6)]
        module = variant(BRANCHES=(S.Branch('only', 'Only', 1991, 'FOCUS_FILTER_POLITICAL', tuple(focuses)),))
        problems = '\n'.join(lint.lint(module))
        for expected in ('own focuses; at least 120', 'branches; at least 10', 'mutually exclusive', 'bare currency',
                         'reward signature appears 6 times', 'too similar'):
            self.assertIn(expected, problems)
        flagged = variant(BRANCHES=(dataclasses.replace(base.BRANCHES[0], focuses=base.BRANCHES[0].focuses[:2]),) + base.BRANCHES[1:])
        self.assertIn('flags set but never read: gauge_agreed', '\n'.join(lint.lint(flagged, strict=False)))
        borrowed = lint.lint(base, others=[('Survey the River Line', 'unrelated')], strict=False)
        self.assertIn('titles already used elsewhere: Survey the River Line', '\n'.join(borrowed))


if __name__ == '__main__':
    if '--record-golden' in sys.argv:
        art.require_pinned_pillow()
        GOLDEN.write_text(json.dumps(golden_record(), indent=1) + '\n', encoding='utf-8', newline='\n')
        print('Golden output recorded')
    else:
        unittest.main()
