"""Day-accurate accounting regressions; no native reachability claims."""
from collections import Counter
import json
import unittest

from coverage import BASE, HERE, MOD, ROOT, inventory, reclassify_baseline


class Coverage(unittest.TestCase):
    def row(self, condition):
        return inventory([('fixture.txt', 'focus_tree = { id = test focus = { id = SOA_test available = { '
                           + condition + ' } } }')])[0]

    def test_day_boundaries_and_comparators(self):
        for condition, year, era in [
            ('date > 2005.12.31', 2006, 'e2'),
            ('date >= 2005.12.31', 2005, 'e1'),
            ('date > 2020.12.31', 2021, 'e3'),
            ('date >= 2020.12.31', 2020, 'e2'),
            ('date = 2006.1.1', 2006, 'e2'),
            ('date != 1991.1.1', 1991, 'e1'),
            ('date <= 1990.12.31', None, None),
            ('date > 2040.12.31', 2041, None),
        ]:
            with self.subTest(condition=condition):
                row = self.row(condition)
                self.assertEqual((year, era), (row['earliest_literal_or_prerequisite_year'], row['era']))

    def test_wrappers_boolean_alternatives_and_negations(self):
        cases = [
            ('custom_trigger_tooltip = { tooltip = test NOT = { date < 2006.1.1 } }', 'e2'),
            ('hidden_trigger = { AND = { date > 2005.12.31 date < 2021.1.1 } }', 'e2'),
            ('OR = { date >= 2006.1.1 date >= 2021.1.1 }', 'e2'),
            ('OR = { date >= 2021.1.1 has_country_flag = alternate }', 'e1'),
            ('NOT = { AND = { date < 2006.1.1 has_country_flag = alternate } }', 'e1'),
            ('NOT = { date < 2006.1.1 has_country_flag = alternate }', 'e2'),
            ('NOT = { NOT = { date > 2020.12.31 } }', 'e3'),
            ('NOT = { OR = { date < 2006.1.1 date > 2020.12.31 } }', 'e2'),
            ('AND = { date > 2020.12.31 date < 2006.1.1 }', None),
            ('OR = { always = no date > 2005.12.31 }', 'e1'),
            ('NOT = { always = yes }', 'e1'),
            ('some_unknown_scope = { date > 2020.12.31 }', 'e1'),
        ]
        for condition, era in cases:
            with self.subTest(condition=condition):
                self.assertEqual(era, self.row(condition)['era'])

    def test_prerequisite_groups_and_inherited_windows(self):
        rows = inventory([('fixture.txt', '''focus_tree = { id = test
focus = { id = SOA_early available = { date > 2005.12.31 } }
focus = { id = SOA_late available = { date > 2020.12.31 } }
focus = { id = SOA_either prerequisite = { focus = SOA_early focus = SOA_late } }
focus = { id = SOA_both prerequisite = { focus = SOA_early } prerequisite = { focus = SOA_late } }
focus = { id = SOA_child prerequisite = { focus = SOA_either } }
focus = { id = SOA_closed prerequisite = { focus = SOA_late } available = { date < 2006.1.1 } }
focus = { id = SOA_impossible_child prerequisite = { focus = SOA_closed } }
focus = { id = SOA_surviving_alternative prerequisite = { focus = SOA_closed focus = SOA_early } }
focus = { id = SOA_gap prerequisite = { focus = SOA_early }
available = { OR = { date < 2000.1.1 date > 2020.12.31 } } }
}''')])
        eras = {r['id']: r['era'] for r in rows}
        self.assertEqual({'SOA_early':'e2', 'SOA_late':'e3', 'SOA_either':'e2',
                          'SOA_both':'e3', 'SOA_child':'e2', 'SOA_closed':None,
                          'SOA_impossible_child':None, 'SOA_surviving_alternative':'e2',
                          'SOA_gap':'e3'}, eras)

    def test_actual_fato_and_osean_continuation_dates(self):
        sources = [(p.relative_to(ROOT).as_posix(), p.read_text(encoding='utf-8-sig'))
                   for p in sorted((MOD / 'common/national_focus').glob('*.txt'))]
        rows = inventory(sources)
        by_id = {r['id']:r for r in rows}
        self.assertEqual('e2', by_id['FAT_nat_renewal_hearing']['era'])
        self.assertEqual(2006, by_id['FAT_nat_renewal_hearing']['earliest_literal_or_prerequisite_year'])
        ose = [r for r in rows if r['source'].endswith('/ac_snc_ose.txt')]
        self.assertEqual(44, len(ose))
        self.assertEqual({'e2':44}, dict(Counter(r['era'] for r in ose)))
        self.assertEqual(2006, by_id['OSE_snc_guarantor_limits_brief']['earliest_literal_or_prerequisite_year'])

    def test_baseline_reclassification_preserves_frozen_provenance(self):
        baseline = json.loads((HERE / 'baseline.json').read_text())
        # Simulate the faulty old allocation without changing the frozen ID set.
        historical = json.loads(json.dumps(baseline))
        for row in historical['focuses']:
            row['era'] = 'e1'
            row['earliest_literal_or_prerequisite_year'] = 1991
        corrected = reclassify_baseline(historical, baseline['focuses'])
        self.assertEqual(baseline, corrected)
        self.assertEqual(BASE, corrected['commit'])
        self.assertEqual(historical['reservations'], corrected['reservations'])
        with self.assertRaisesRegex(ValueError, 'Frozen baseline'):
            reclassify_baseline(historical, baseline['focuses'][:-1])
        changed_source = json.loads(json.dumps(baseline['focuses']))
        changed_source[0]['source'] = 'different.txt'
        with self.assertRaisesRegex(ValueError, 'Frozen baseline'):
            reclassify_baseline(historical, changed_source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
