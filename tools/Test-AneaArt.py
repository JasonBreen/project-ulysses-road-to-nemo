"""Offline Anea artwork contracts; no engine or desktop interaction."""
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
HERE = ROOT / 'tools/anea'


class AneaArt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assets = json.loads((HERE / 'assets.json').read_text())
        cls.focuses = json.loads((HERE / 'focus_art.json').read_text())
        cls.sources = json.loads((HERE / 'original_art.json').read_text())
        cls.gfx = (MOD / 'interface/ac_anea_art.gfx').read_text()

    def test_every_texture_has_verified_format_dimensions_frames_and_hash(self):
        self.assertEqual(165, len(self.assets))
        self.assertEqual(len(self.assets), len({row['file'] for row in self.assets}))
        for row in self.assets:
            with self.subTest(texture=row['file']):
                path = MOD / row['file']
                data = path.read_bytes()
                self.assertEqual(b'DDS ', data[:4])
                self.assertEqual(row['sha256'], hashlib.sha256(data).hexdigest())
                with Image.open(path) as image:
                    self.assertEqual((row['width'], row['height']), image.size)
                    self.assertEqual((row['alpha_min'], row['alpha_max']),
                                     image.convert('RGBA').getchannel('A').getextrema())
                self.assertGreater(row['frames'], 0)
                self.assertEqual(0, row['width'] % row['frames'])
                self.assertEqual(row['frame_width'], row['width'] // row['frames'])

    def test_focus_coverage_compositions_and_transparent_apertures(self):
        sys.path.insert(0, str(HERE))
        from content import FOCUSES
        self.assertEqual({row.id for row in FOCUSES}, {row['id'] for row in self.focuses})
        self.assertEqual(108, len(self.focuses))
        self.assertEqual(108, len({row['sha256'] for row in self.focuses}))
        for row in self.focuses:
            with self.subTest(focus=row['id']):
                with Image.open(MOD / row['asset']) as image:
                    self.assertEqual((96, 96), image.size)
                    alpha = image.convert('RGBA').getchannel('A')
                    for corner in ((0, 0), (95, 0), (0, 95), (95, 95)):
                        self.assertEqual(0, alpha.getpixel(corner))
                    bounds = alpha.getbbox()
                    self.assertGreater(bounds[0], 0)
                    self.assertGreater(bounds[1], 0)
                    self.assertLess(bounds[2], 96)
                    self.assertLess(bounds[3], 96)
                self.assertIn('name = "' + row['sprite'] + '"', self.gfx)
                self.assertIn('name = "' + row['sprite'] + '_shine"', self.gfx)

    def test_original_masters_are_complete_and_separate_from_loading_scenes(self):
        self.assertEqual(10, len(self.sources))
        self.assertEqual(10, len({row['source_sha256'] for row in self.sources}))
        self.assertEqual(8, sum(not row['id'].startswith('loading_') for row in self.sources))
        self.assertEqual(2, sum(row['id'].startswith('loading_') for row in self.sources))
        for row in self.sources:
            path = HERE / row['file']
            self.assertEqual(row['source_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertIn('Original', row['provenance'])
            self.assertEqual('Built-in image_gen', row['generator'])
            self.assertRegex(row['prompt'], r'No (words|text)')
            self.assertNotIn('C:\\', json.dumps(row))
            with Image.open(path) as image:
                self.assertEqual((row['width'], row['height']), image.size)

    def test_event_pictures_fit_the_repaired_country_event_column(self):
        rows = [row for row in self.assets if row['role'] == 'original narrative illustration']
        self.assertEqual(8, len(rows))
        for row in rows:
            self.assertEqual((200, 160), (row['width'], row['height']))
            self.assertEqual(255, row['alpha_min'])
            self.assertIn('texturefile = "' + row['file'] + '"', self.gfx)

    def test_all_new_spirit_and_category_tokens_resolve(self):
        sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
        from script import get, parse
        sprite_names = re.findall(r'name\s*=\s*"([^"]+)"', self.gfx)
        self.assertEqual(len(sprite_names), len(set(sprite_names)))
        for name in ('ac_anea', 'ac_anea_policies'):
            path = MOD / 'common/ideas' / (name + '.txt')
            if not path.exists():
                self.fail('Missing integrated idea definitions: ' + str(path))
            country_ideas = get(get(parse(path.read_text(encoding='utf-8-sig')), 'ideas'), 'country')
            for ident, _, body in country_ideas:
                picture = get(body, 'picture')
                if picture:
                    self.assertIn('GFX_idea_' + picture.strip('"'), sprite_names, ident)
        for suffix in ('recovery', 'relief'):
            for prefix in ('GFX_ac_anea_category_', 'GFX_decision_category_ac_anea_', 'GFX_decision_ac_anea_'):
                self.assertIn(prefix + suffix, sprite_names)

    def test_loading_rotation_has_both_required_texture_sizes(self):
        background = (MOD / 'common/frontend/backgrounds/ac_anea_backgrounds.txt').read_text()
        for tag in ('emm', 'eva'):
            name = 'ac_anea_' + tag
            self.assertIn(name + ' = {}', background)
            for suffix, size in (('', (1920, 1080)), ('_small', (192, 144))):
                with Image.open(MOD / 'gfx/loadingscreens' / (name + suffix + '.dds')) as image:
                    self.assertEqual(size, image.size)

    def test_established_flags_are_preserved_in_office_presentations(self):
        for tag in ('EMM', 'EVA'):
            row = next(row for row in self.assets if row.get('sprite') == 'GFX_ac_anea_office_' + tag.lower())
            self.assertEqual((156, 210), (row['width'], row['height']))
            self.assertEqual('mod/2985041246/gfx/flags/' + tag + '.tga', row['source'])
            self.assertEqual(row['source_sha256'], hashlib.sha256((ROOT / row['source']).read_bytes()).hexdigest())
            # The established recruited identities retain their generator-owned cards.
            characters = (MOD / 'common/characters/ac_starting_governments.txt').read_text()
            self.assertIn('GFX_ac_exp_government_' + tag, characters)

    def test_packaging_is_reproducible(self):
        result = subprocess.run([sys.executable, '-B', str(HERE / 'build_art.py'), '--check'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
