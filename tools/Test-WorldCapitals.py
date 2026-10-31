"""Actual capital mapping and protected-geometry checks; no native claims."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/world_capitals'))
from build import INVALID, CAPITAL, derive, outputs, repair, select
from script import parse, get


class WorldCapitals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / 'tools/world_capitals/placements.json').read_text())

    def test_all_69_histories_have_explicit_disposition(self):
        m = self.manifest
        groups = [set(m['countries']), set(m['preserved_owned_capitals']), set(m['dormant_histories_preserved'])]
        self.assertEqual([14, 48, 7], [len(group) for group in groups])
        self.assertEqual(69, len(set.union(*groups)))
        self.assertEqual({p.name[:3] for p in (MOD / 'history/countries').glob('*.txt')}, set.union(*groups))
        for i, group in enumerate(groups):
            for other in groups[i + 1:]:
                self.assertFalse(group & other)
        self.assertIn('PLH', groups[1])

    def test_all_landowning_capitals_are_owned_after_repairs(self):
        owners = {}
        for path in (MOD / 'history/states').glob('*.txt'):
            state = get(parse(path.read_text(encoding='utf-8-sig')), 'state')
            owners[int(get(state, 'id'))] = get(get(state, 'history'), 'owner')
        active = set(owners.values())
        for path in (MOD / 'history/countries').glob('*.txt'):
            tag = path.name[:3]
            if tag in active:
                capital = int(get(parse(path.read_text(encoding='utf-8-sig')), 'capital'))
                self.assertEqual(tag, owners[capital], tag)

    def test_mappings_reproduce_from_raster_without_changes(self):
        self.assertEqual(self.manifest, derive())
        for relative, expected in self.manifest['geography_hashes'].items():
            self.assertEqual(expected, hashlib.sha256((MOD / relative).read_bytes()).hexdigest())
        for tag, row in self.manifest['countries'].items():
            self.assertIn(row['capital'], row['owned_states'])
            self.assertNotEqual(row['old_capital'], row['capital'])
            self.assertIn(row['representative_province'], row['mainland_provinces'])
            self.assertNotIn(171, row['owned_states'])
            distances = {int(i): n for i, n in row['candidate_squared_distances'].items()}
            self.assertEqual(row['capital'], min(distances, key=lambda i: (distances[i], i)))

    def test_largest_landmass_uses_area_not_province_count(self):
        states = {10: {'land': [1]}, 20: {'land': [2, 3]}}
        graph = defaultdict(set, {1: set(), 2: {3}, 3: {2}})
        result = select(states, graph, {1: (5, 5), 2: (20, 0), 3: (22, 0)}, {1: 100, 2: 3, 3: 3})
        self.assertEqual(10, result['capital'])
        self.assertEqual([1], result['mainland_provinces'])

    def test_nearest_state_centre_and_lowest_state_id_tie(self):
        graph = defaultdict(set, {1: {2}, 2: {1, 3}, 3: {2}})
        positions = {1: (0, 0), 2: (10, 0), 3: (20, 0)}
        result = select({30: {'land': [1]}, 40: {'land': [2]}, 50: {'land': [3]}}, graph, positions, {1: 1, 2: 1, 3: 1})
        self.assertEqual(40, result['capital'])
        result = select({30: {'land': [1]}, 20: {'land': [2]}}, graph, positions, {1: 1, 2: 1})
        self.assertEqual(20, result['capital'])

    def test_repair_preserves_foreign_setup_and_comments(self):
        source = '# country\ncapital = 1 # inherited district\nrecruit_character = office\n# BEGIN WORLD FOUNDATION\nset_oob = "fleet"\n# END WORLD FOUNDATION\n# BEGIN ECONOMY V2 NEW CAMPAIGN\nset_country_flag = ac_macro_history_eligible\n# END ECONOMY V2 NEW CAMPAIGN\n'
        expected = source.replace('capital = 1 #', 'capital = 42 #')
        self.assertEqual(expected, repair(source, 42))
        self.assertEqual(expected, repair(expected, 42))
        for bad in ('', 'capital = 1\ncapital = 2\n'):
            with self.assertRaises(ValueError):
                repair(bad, 42)

    def test_only_reviewed_capital_fields_are_generated(self):
        generated = outputs(self.manifest)
        paths = {MOD / row['history'] for row in self.manifest['countries'].values()}
        self.assertEqual(15, len(generated))
        for path in paths:
            source = path.read_text(encoding='utf-8-sig')
            result = generated[path].decode('utf-8')
            self.assertEqual(CAPITAL.sub('CAPITAL', source), CAPITAL.sub('CAPITAL', result))
        self.assertEqual(set(INVALID), set(self.manifest['countries']))

    def test_check_mode_is_current(self):
        subprocess.run([sys.executable, '-B', str(ROOT / 'tools/world_capitals/build.py'), '--check'], check=True, capture_output=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
