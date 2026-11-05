"""Decision-category descriptions: measured length, hard failures and the
chosen-policies-only template. Offline measurement, not native rendering."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tools/decision_text'), str(ROOT / 'tools/usea_expansion')]
import measure  # noqa: E402
from script import parse, get, walk  # noqa: E402
from event_style.review import locs  # noqa: E402


class DecisionText(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = measure.measurement()
        cls.strings = locs()

    def test_real_mod_has_no_hard_failure_and_only_reasoned_overruns(self):
        self.assertEqual((470, 'ACBriefing16'), (self.data['control']['width'], self.data['control']['font']))
        self.assertEqual([], self.data['hard_failures'])
        self.assertEqual([], self.data['over_budget_not_allowlisted'])
        self.assertEqual([], self.data['stale_allowlist'])
        self.assertGreaterEqual(self.data['categories'], 60)
        contract = measure.contract()
        for ident, reason in contract['allowlist'].items():
            self.assertGreater(len(reason), 40, ident)
        # The register repair: the two superpower registers were 48 and 47 lines.
        rows = {row['category']: row for row in self.data['rows']}
        for ident in ('ac_snp_ose_programmes', 'ac_snp_yuk_programmes'):
            self.assertLessEqual(rows[ident]['longest']['lines'], 24)
            self.assertLessEqual(rows[ident]['shortest']['lines'], contract['line_budget'])

    def test_no_category_declares_custom_icons(self):
        # The custom_icons strip sits at y 75; nothing uses it, so nothing can overlap it.
        for path in (MOD / 'common/decisions').rglob('*.txt'):
            self.assertNotIn('custom_icon', path.read_text(encoding='utf-8-sig', errors='replace'), path.name)

    def test_service_categories_print_chosen_policies_only(self):
        defined = measure.defined_texts()
        lines = {name: keys for name, keys in defined.items() if name.endswith('_policy_line')}
        self.assertGreater(len(lines), 50)
        for name, keys in lines.items():
            with self.subTest(name=name):
                self.assertEqual('', self.strings[keys[-1]])  # unchosen: nothing printed
                for key in keys[:-1]:
                    self.assertTrue(self.strings[key].startswith('Standing policy: '))
                    self.assertTrue(self.strings[key].endswith('\n'))
        services = [row['category'] for row in self.data['rows'] if re.fullmatch(r'ac_\w+_services', row['category'])]
        self.assertGreaterEqual(len(services), 12)
        for key, value in ((ident + '_desc', self.strings[ident + '_desc']) for ident in services):
                with self.subTest(key=key):
                    self.assertNotIn('Authorization commits', value)
                    self.assertNotIn('_policy_text]', value)
                    self.assertIn('_policy_line]', value)

    def test_every_generated_custom_cost_has_a_hover_tooltip(self):
        keys = set()
        for path in (MOD / 'common/decisions').glob('ac_*.txt'):
            keys.update(re.findall(r'custom_cost_text\s*=\s*(\w+)', path.read_text(encoding='utf-8-sig')))
        generated = {k for k in keys if re.fullmatch(r'ac_\w+_funded_cost|ac_snp_cost_(?:ose_civil|ose_protected|yuk)', k)}
        self.assertGreaterEqual(len(generated), 9)
        for key in sorted(generated):
            with self.subTest(key=key):
                self.assertIn(key + '_tooltip', self.strings)
                self.assertIn('institutional-capacity', self.strings[key + '_tooltip'])

    def test_fixture_reports_cycles_unresolved_slots_glyphs_words_and_budget(self):
        with tempfile.TemporaryDirectory() as folder:
            mod = Path(folder)
            for relative in ('interface/countrydecisionview.gui',):
                (mod / relative).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(MOD / relative, mod / relative)
            (mod / 'common/decisions/categories').mkdir(parents=True)
            (mod / 'common/scripted_localisation').mkdir(parents=True)
            (mod / 'localisation').mkdir()
            (mod / 'common/decisions/categories/x.txt').write_text(
                'fx_cycle = { }\nfx_missing = { }\nfx_glyph = { }\nfx_word = { }\nfx_long = { }\nfx_ok = { }\n', encoding='utf-8')
            (mod / 'common/scripted_localisation/x.txt').write_text(
                'defined_text = { name = fx_a text = { localization_key = fx_a_key } }\n'
                'defined_text = { name = fx_pick text = { trigger = { always = no } localization_key = fx_short } text = { localization_key = fx_wide } }\n',
                encoding='utf-8')
            strings = {'fx_cycle_desc': '[fx_a]', 'fx_a_key': 'loop [fx_a]', 'fx_missing_desc': 'Value [fx_nowhere]',
                       'fx_glyph_desc': 'Snowman ☃', 'fx_word_desc': 'W' * 60, 'fx_long_desc': '\\n'.join(['line'] * 20),
                       'fx_ok_desc': 'Status [?fx_var|0] for [ROOT.GetName]: [fx_pick]', 'fx_short': 'a', 'fx_wide': 'a much wider alternative'}
            (mod / 'localisation/x_l_english.yml').write_text('l_english:\n' + ''.join(' %s:0 "%s"\n' % kv for kv in strings.items()), encoding='utf-8-sig')
            data = measure.measurement(mod)
            rows = {row['category']: row for row in data['rows']}
            self.assertEqual({'fx_cycle', 'fx_missing', 'fx_glyph', 'fx_word'}, set(data['hard_failures']))
            self.assertIn('cycle:fx_a', rows['fx_cycle']['longest']['problems'])
            self.assertIn('unresolved_slot:fx_nowhere', rows['fx_missing']['longest']['problems'])
            self.assertEqual(['☃'], rows['fx_glyph']['longest']['missing_glyphs'])
            self.assertEqual(['W' * 60], rows['fx_word']['longest']['unbreakable_words'])
            self.assertEqual(['fx_long'], data['over_budget_not_allowlisted'])
            ok = rows['fx_ok']
            self.assertEqual(1, ok['longest']['lines'])
            self.assertIn('9999', ok['text_longest']);self.assertIn(measure.SCOPE_NAME, ok['text_longest'])
            self.assertIn('a much wider alternative', ok['text_longest'])

    def test_review_reproduces(self):
        result = subprocess.run([sys.executable, '-B', 'tools/decision_text/measure.py', '--check'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
