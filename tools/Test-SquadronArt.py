"""Original squadron source, texture, crop and consumer checks.

This verifies packaged assets and their actual script consumers. Individual
source reviews and contact sheets are retained separately. Pixel and reference
checks cannot establish native GUI rendering or the absence of every visual
artifact in generated artwork.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/squadrons'))
sys.path.insert(0, str(ROOT / 'tools'))
from schema import campaigns
from economy_script import parse, fields


def walk(nodes):
    for key, _, value in nodes:
        if isinstance(value, list):
            yield key, value
            yield from walk(value)


class SquadronArt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / 'tools/squadrons/assets.json').read_text())
        cls.assets = cls.manifest['assets']
        cls.sprites = {}
        for key, body in walk(parse((MOD / 'interface/ac_squadrons.gfx').read_text())):
            if key == 'spriteType':
                row = fields(body)
                name = row['name'].strip('"')
                if name in cls.sprites:
                    raise ValueError('Conflicting owned sprite: ' + name)
                cls.sprites[name] = row

    def test_all_78_retained_original_masters_have_individual_provenance(self):
        expected = {p['id'] for r in campaigns() for p in r['cast']}
        plan = json.loads((ROOT / 'tools/squadrons/art_plan.json').read_text())
        expected |= {r['id'] for r in plan['scenes'] + plan['loading']}
        self.assertEqual(78, len(expected))
        actual = {}
        for path in (ROOT / 'tools/squadrons/sources').rglob('*.png'):
            record = json.loads(path.with_suffix('.json').read_text())
            self.assertEqual(record['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual('built-in image_gen', record['generator'])
            self.assertTrue(record['prompt']); self.assertTrue(record['review'])
            self.assertNotIn('pending', record['review'].lower())
            self.assertEqual(path.name, record['file'])
            with Image.open(path) as image:
                self.assertEqual((record['width'], record['height']), image.size)
                self.assertGreater(image.width, 800)
            actual[record['id']] = record['sha256']
        self.assertEqual(expected, set(actual))
        self.assertEqual(78, len(set(actual.values())))

    def test_all_textures_have_deliberate_dimensions_frames_and_alpha(self):
        self.assertEqual(115, len(self.assets))
        self.assertEqual(109, len(self.sprites))
        self.assertEqual(115, len({r['file'] for r in self.assets}))
        for row in self.assets:
            path = MOD / row['file']
            self.assertEqual(row['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(1, row['frames'])
            self.assertEqual((row['width'], row['height']), (row['frame_width'], row['frame_height']))
            with Image.open(path) as image:
                self.assertEqual((row['width'], row['height']), image.size)
                self.assertEqual('RGBA', image.mode)
                extrema = image.getchannel('A').getextrema()
                self.assertEqual((row['alpha_min'], row['alpha_max']), extrema)
                if '/categories/' in row['file'] or '/ideas/' in row['file']:
                    self.assertEqual((0, 255), extrema)
                    for x, y in ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1)):
                        self.assertEqual(0, image.getpixel((x, y))[3])
                else:
                    self.assertEqual((255, 255), extrema)
            if row.get('source'):
                self.assertEqual(row['source_sha256'], hashlib.sha256((ROOT / row['source']).read_bytes()).hexdigest())
                self.assertTrue((ROOT / row['provenance']).exists())

    def test_story_consumers_resolve_to_owned_textures_without_fallbacks(self):
        used = set()
        for relative in ('events/ac_squadrons.txt', 'common/decisions/categories/ac_squadrons.txt'):
            for key, body in walk(parse((MOD / relative).read_text(encoding='utf-8-sig'))):
                for prop, _, value in body:
                    if prop in ('picture', 'icon') and isinstance(value, str) and value.startswith('GFX_ac_sq_'):
                        used.add(value)
        self.assertGreaterEqual(len(used), 78)
        self.assertFalse(used - self.sprites.keys())
        for name in used:
            texture = self.sprites[name]['texturefile'].strip('"')
            self.assertTrue(texture.startswith('gfx/AC_squadrons/'))
            self.assertTrue((MOD / texture).exists())
        ideas = (MOD / 'common/ideas/ac_squadrons.txt').read_text()
        self.assertIn('picture = ac_sq_professional_debrief', ideas)
        self.assertIn('GFX_idea_ac_sq_professional_debrief', self.sprites)

    def test_every_chapter_has_an_explicit_deliberately_shared_scene(self):
        mapping = {(r['tag'], r['chapter']): r for r in self.manifest['chapter_mapping']}
        self.assertEqual(120, len(mapping))
        sources = set()
        for row in campaigns():
            events = parse((MOD / 'events/ac_squadrons.txt').read_text(encoding='utf-8-sig'))
            pictures = {fields([row for row in body if row[0] in ('id', 'picture')])['id']:
                        fields([row for row in body if row[0] in ('id', 'picture')])['picture']
                        for key, _, body in events if key == 'country_event'}
            for chapter in row['chapters']:
                entry = mapping[row['tag'], chapter['id']]
                sprite = 'GFX_ac_sq_' + entry['source']
                self.assertIn(sprite, self.sprites)
                self.assertEqual(sprite, pictures['ac_sq.' + str(row['base'] + chapter['id'])])
                self.assertTrue(entry['reason'])
                sources.add(entry['source'])
        self.assertEqual(48, len(sources))
        self.assertIn('without depicting a specific victory or loss', self.manifest['ending_mapping'])

    def test_loading_screens_are_independent_masters_and_valid_picker_bindings(self):
        rows = [r for r in self.assets if r['role'] == 'original independent loading-screen composition']
        self.assertEqual(6, len(rows))
        scene_hashes = {r['source_sha256'] for r in self.assets if r['role'] == 'original deliberately shared narrative scene'}
        definitions = parse((MOD / 'common/frontend/backgrounds/ac_sq_backgrounds.txt').read_text())
        self.assertEqual({'ac_sq_' + r['tag'].lower() for r in campaigns()}, {key for key, _, _ in definitions})
        for row in rows:
            self.assertEqual((1920, 1080), (row['width'], row['height']))
            self.assertNotIn(row['source_sha256'], scene_hashes)
            ident = Path(row['file']).stem
            self.assertIn('GFX_' + ident + '_small', self.sprites)
            self.assertIn('native crop acceptance pending', row['safe_area'].lower())

    def test_narrative_cast_never_binds_to_national_officeholders(self):
        for path in (MOD / 'common/characters').glob('*.txt'):
            text = path.read_text(encoding='utf-8-sig')
            self.assertNotRegex(text, r'GFX_ac_sq_(?:portrait|cast)_')
        portraits = [r for r in self.assets if r['role'].startswith('original narrative cast portrait;')]
        self.assertEqual(24, len(portraits))
        self.assertTrue(all((r['width'], r['height']) == (156, 210) for r in portraits))

    def test_no_other_sprite_family_conflicts_with_story_names(self):
        owners = {}
        pattern = re.compile(r'\bname\s*=\s*"(GFX_ac_sq_[A-Za-z0-9_]+|GFX_idea_ac_sq_[A-Za-z0-9_]+)"')
        for path in (MOD / 'interface').glob('*.gfx'):
            for name in pattern.findall(path.read_text(encoding='utf-8-sig')):
                self.assertNotIn(name, owners, (name, path, owners.get(name)))
                owners[name] = path
        self.assertEqual(set(self.sprites), set(owners))

    def test_packaged_bytes_and_galleries_reproduce(self):
        result = subprocess.run([sys.executable, '-B', 'tools/squadrons/build_art.py', '--check'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        gallery = ROOT / 'docs/evidence/squadrons/artwork-gallery.html'
        self.assertEqual(78, gallery.read_text().count('<figure '))
        self.assertNotIn('Source production incomplete', gallery.read_text())


if __name__ == '__main__':
    unittest.main(verbosity=2)
