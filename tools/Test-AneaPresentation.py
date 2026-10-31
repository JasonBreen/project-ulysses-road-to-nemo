"""Validate live bookmark and office presentation bindings without desktop use."""
import hashlib
import copy
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import get, parse, walk


def read(relative):
    return parse((MOD / relative).read_text(encoding='utf-8-sig'))


class AneaPresentation(unittest.TestCase):
    def test_only_two_existing_offices_select_the_anea_presentations(self):
        manifest = json.loads((ROOT / 'tools/usea_expansion/leaders.json').read_text())
        self.assertEqual(69, len(manifest))
        self.assertEqual(51, sum(row['missing'] for row in manifest))
        selected = [row for row in manifest if row.get('presentation_source')]
        self.assertEqual({'EMM', 'EVA'}, {row['tag'] for row in selected})
        for row in selected:
            self.assertEqual('gfx/AC_anea/cards/' + row['tag'] + '_office.dds', row['presentation_source'])
            self.assertEqual('democratic', row['party'])
            self.assertTrue(row['missing'])

    def test_recruited_characters_retain_names_and_existing_sprite_bindings(self):
        characters = get(read('common/characters/ac_starting_governments.txt'), 'characters')
        gfx = (MOD / 'interface/ac_starting_governments.gfx').read_text()
        for tag, name in (('EMM', 'Emmeria'), ('EVA', 'Estovakia')):
            character = get(characters, tag + '_ac_government_office')
            self.assertEqual(tag + '_ac_government_office', get(character, 'name'))
            portraits = get(get(get(character, 'portraits'), 'civilian'), 'large')
            self.assertEqual('"GFX_ac_exp_government_' + tag + '"', portraits)
            self.assertIn('name = "GFX_ac_exp_government_' + tag + '"', gfx)
            history = read('history/countries/' + tag + ' - ' + name + '.txt')
            self.assertEqual(1, sum(k == 'recruit_character' and v == tag + '_ac_government_office'
                                    for k, _, v in history))
            self.assertFalse(any(k in ('create_country_leader', 'set_country_leader') for k, _, v in history))

    def test_live_portrait_bytes_and_flag_provenance_match_the_authored_cards(self):
        assets = json.loads((ROOT / 'tools/usea_expansion/leader_assets.json').read_text())
        self.assertEqual(51, len(assets))
        for tag in ('EMM', 'EVA'):
            path = 'gfx/leaders/AC_start_governments/' + tag + '.dds'
            row = next(row for row in assets if row['file'] == path)
            presentation = MOD / row['presentation_source']
            self.assertEqual(presentation.read_bytes(), (MOD / path).read_bytes())
            self.assertEqual(row['presentation_source_sha256'], hashlib.sha256(presentation.read_bytes()).hexdigest())
            self.assertEqual(row['sha256'], row['presentation_source_sha256'])
            self.assertEqual('gfx/flags/' + tag + '.tga', row['source'])
            self.assertEqual(row['source_sha256'], hashlib.sha256((MOD / row['source']).read_bytes()).hexdigest())

    def test_both_1991_bookmarks_offer_each_country_as_a_minor(self):
        for file in ('blitzkrieg.txt', 'the_gathering_storm.txt'):
            bookmark = get(get(read('common/bookmarks/' + file), 'bookmarks'), 'bookmark')
            self.assertEqual('1991.1.1.12', get(bookmark, 'date'))
            self.assertEqual('"BLK"', get(bookmark, 'default_country'))
            self.assertEqual('"GFX_select_date_1936"', get(bookmark, 'picture'))
            for tag in ('EMM', 'EVA'):
                country = get(bookmark, '"' + tag + '"')
                self.assertIsNotNone(country, (file, tag))
                self.assertEqual('yes', get(country, 'minor'))
                self.assertEqual('democratic', get(country, 'ideology'))
                self.assertEqual('"' + tag + '_ANEA_1991_DESC"', get(country, 'history'))
                self.assertIsNone(get(country, 'effect'))
                self.assertIsNone(get(country, 'picture'))

    def test_bookmark_focus_previews_reference_real_foundation_content(self):
        focus_nodes = {}
        for tag in ('EMM', 'EVA'):
            for kind, node in walk(read('common/national_focus/' + tag + '.txt')):
                if kind == 'focus':
                    focus_nodes[get(node, 'id')] = node
        for file in ('blitzkrieg.txt', 'the_gathering_storm.txt'):
            bookmark = get(get(read('common/bookmarks/' + file), 'bookmarks'), 'bookmark')
            for tag in ('EMM', 'EVA'):
                country = get(bookmark, '"' + tag + '"')
                focuses = [key for key, _, _ in get(country, 'focuses')]
                self.assertEqual(3, len(focuses))
                for ident in focuses:
                    self.assertIn(ident, focus_nodes)
                    self.assertTrue(ident.startswith(tag + '_an_'))
                    self.assertIn('GFX_ac_anea_focus_' + ident, str(focus_nodes[ident]))

    def test_country_briefs_are_complete_1991_text_without_disaster_foreknowledge(self):
        path = MOD / 'localisation/english/ac_anea_bookmarks_l_english.yml'
        self.assertTrue(path.read_bytes().startswith(b'\xef\xbb\xbf'))
        text = path.read_text(encoding='utf-8-sig')
        self.assertTrue(text.startswith('l_english:'))
        for tag in ('EMM', 'EVA'):
            match = re.search(r'^ ' + tag + r'_ANEA_1991_DESC:0 "(.*)"$', text, re.M)
            self.assertIsNotNone(match)
            brief = match[1]
            self.assertGreater(len(brief.split()), 130)
            self.assertIn('provisional campaign design', brief)
            self.assertNotRegex(brief.lower(), r'ulysses|asteroid|sanctions|1998|1999|2000|2015')
        gui = (MOD / 'interface/frontendgamesetupview.gui').read_text()
        self.assertIn('name = "minor_country_leader"', gui)
        self.assertIn('name ="countries_mini"', gui)

    def test_starting_government_packaging_is_reproducible(self):
        result = subprocess.run([sys.executable, '-B', 'tools/usea_expansion/build_leaders.py', '--check'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_country_history_has_separate_scrolling_bounds_and_keeps_controls(self):
        sys.path.insert(0, str(ROOT / 'tools/anea'))
        from build_briefs_ui import validate_bounds, repaired_node
        contract = json.loads((ROOT / 'tools/anea/briefing_control.json').read_text())
        text = (MOD / 'interface/frontendgamesetupview.gui').read_text(encoding='utf-8-sig')
        start, end = validate_bounds(text, contract)
        actual = parse(text[start:end])[0]
        self.assertEqual(repaired_node(contract), actual)
        original = copy.deepcopy(contract['original_node'][2])
        changed = copy.deepcopy(actual[2])
        original = [row for row in original if row[0] not in ('position', 'maxHeight', 'font')]
        changed = [row for row in changed if row[0] not in ('position', 'maxHeight', 'scrollbarType', 'font')]
        self.assertEqual(original, changed)
        self.assertEqual('"history"', get(actual[2], 'name'))
        self.assertEqual('"Aces16"', get(actual[2], 'font'))
        self.assertEqual('380', get(actual[2], 'maxWidth'))
        self.assertEqual('145', get(actual[2], 'maxHeight'))
        self.assertEqual('"ac_exp_standardtext_slider"', get(actual[2], 'scrollbarType'))
        self.assertEqual(dict(heading_bottom=480, narrative_top=485,
                              narrative_bottom=630, navigation_top=665), contract['bounds'])

    def test_history_exception_preserves_the_original_whole_layout_fingerprint(self):
        sys.path.insert(0, str(ROOT / 'tools/anea'))
        from build_briefs_ui import normalize_for_fingerprint
        spec = importlib.util.spec_from_file_location('anea_frontend_validation', ROOT / 'tools/frontend_briefing/validate.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        text = (MOD / 'interface/frontendgamesetupview.gui').read_text(encoding='utf-8-sig')
        expected = (ROOT / 'tools/frontend_briefing/layout.sha256').read_text().strip()
        self.assertEqual(expected, module.layout(normalize_for_fingerprint(text)))
        # The exception must not conceal unrelated geometry changes.
        altered = text.replace('size = { width=1225 height=717 }',
                               'size = { width=1226 height=717 }', 1)
        self.assertNotEqual(text, altered)
        self.assertNotEqual(expected, module.layout(normalize_for_fingerprint(altered)))

    def test_history_contract_rejects_missing_scroll_and_changed_engine_controls(self):
        sys.path.insert(0, str(ROOT / 'tools/anea'))
        from build_briefs_ui import normalize_for_fingerprint
        text = (MOD / 'interface/frontendgamesetupview.gui').read_text(encoding='utf-8-sig')
        cases = [
            text.replace('scrollbarType = "ac_exp_standardtext_slider"', '', 1),
            text.replace('name = "history"', 'name = "history_missing"', 1),
            text.replace('name = "minor_country_leader"', 'name = "missing_portrait"', 1),
        ]
        for altered in cases:
            with self.subTest(change=altered != text):
                self.assertNotEqual(text, altered)
                with self.assertRaises(ValueError):
                    normalize_for_fingerprint(altered)

    def test_country_brief_ui_generation_is_reproducible(self):
        result = subprocess.run([sys.executable, '-B', 'tools/anea/build_briefs_ui.py', '--check'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
