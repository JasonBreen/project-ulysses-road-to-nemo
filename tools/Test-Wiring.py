"""Wiring ratchet: no new defect or warning, and fixed ones leave the baseline.

    python -B tools/Test-Wiring.py            # unit tests on a synthetic mod, then the ratchet
    python -B tools/Test-Wiring.py --record   # after fixes: rewrite the baseline (refuses new findings)

The baseline (docs/evidence/wiring/baseline.json) lists every active defect and
warning by check and name. A finding not in it fails; a baseline entry that no
longer occurs also fails until --record removes it, so the list only shrinks.
Allowlist entries that match nothing fail too. Static source evidence only.
"""
import json
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/wiring'))
import audit  # noqa: E402
from index import Index, parse  # noqa: E402

BASELINE = ROOT / 'docs/evidence/wiring/baseline.json'


def write(root, files):
    for rel, text in files.items():
        path = Path(root) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text), encoding='utf-8')


MINI = {
    'common/country_tags/tags.txt': 'AAA = "countries/A.txt"\nBBB = "countries/B.txt"\n',
    'history/states/1-One.txt': 'state = { id = 1 provinces = { 10 } }\n',
    'map/definition.csv': '0;0;0;0;land;false;unknown;0\n10;1;1;1;land;false;plains;1\n',
    'localisation/english/a_l_english.yml': '﻿l_english:\n a.1.t:0 "T"\n a.1.d:0 "D"\n a.1.a:0 "A"\n AAA_root:0 "R"\n AAA_root_desc:0 "R"\n',
    'events/a.txt': '''
        add_namespace = a
        country_event = { id = a.1 title = a.1.t desc = a.1.d is_triggered_only = yes
            option = { name = a.1.a country_event = a.9 set_country_flag = AAA_done } }
        country_event = { id = a.2 title = a.2.t desc = a.2.d is_triggered_only = yes option = { name = a.2.a } }
        country_event = { id = a.3 hidden = yes is_triggered_only = yes immediate = { if = { limit = { always = yes } } else = { } } }
        country_event = { id = a.4 hidden = yes is_triggered_only = yes immediate = { if = { limit = { always = no } } else = { add_political_power = 1 } } }
        country_event = { id = a.5 hidden = yes mean_time_to_happen = { days = 10 } }
    ''',
    'common/on_actions/a.txt': 'on_actions = { on_startup = { effect = { country_event = a.1 } } on_daily = { events = { a.3 } random_events = { 50 = a.4 50 = 0 } } }\n',
    'common/scripted_effects/a.txt': '''
        ac_used_effect = { set_global_flag = ac_$what$_set }
        ac_unused_effect = { add_political_power = 1 }
    ''',
    'common/scripted_triggers/a.txt': 'ac_used_trigger = { has_global_flag = ac_alpha_set }\n',
    'common/ideas/a.txt': 'ideas = { country = { AAA_spirit = { } AAA_lonely = { } } economy = { law = yes AAA_law = { } } }\n',
    'common/characters/a.txt': 'characters = { AAA_leader = { advisor = { slot = air_chief idea_token = AAA_air_token } } }\n',
    'common/decisions/categories/a.txt': 'ac_cat = { }\n',
    'common/decisions/a.txt': '''
        ac_cat = { ac_dec = { complete_effect = {
            ac_used_effect = { what = alpha } ac_used_effect = yes ac_missing_effect = yes
            add_ideas = { AAA_spirit AAA_ghost CHI_vanilla } activate_advisor = AAA_air_token
            recruit_character = AAA_leader recruit_character = AAA_nobody activate_decision = ac_gone
            load_focus_tree = { tree = ac_loaded keep_completed = yes } load_focus_tree = ac_missing_tree
            transfer_state = 1 transfer_state = 99 controls_province = 10 controls_province = 77
            set_variable = { ac_var = 1 } if = { limit = { check_variable = { ac_var > 0 } check_variable = { ac_ghost > 0 } } }
            if = { limit = { has_country_flag = AAA_done has_global_flag = ac_never has_global_flag = ac_beta_set } }
            country_event = a.404 country_event = news.1
        } } }
        ac_lost_category = { ac_orphan = { } }
    ''',
    'common/national_focus/a.txt': '''
        focus_tree = { id = ac_assigned country = { factor = 0 modifier = { add = 10 tag = AAA } } shared_focus = AAA_root shared_focus = AAA_absent
            focus = { id = AAA_own } }
        focus_tree = { id = ac_loaded country = { factor = 0 } }
        focus_tree = { id = ac_stranded country = { factor = 0 } }
        shared_focus = { id = AAA_root }
        shared_focus = { id = AAA_child prerequisite = { focus = AAA_root } }
        shared_focus = { id = AAA_island }
    ''',
}


class Synthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        write(cls.tmp.name, MINI)
        cls.index = Index(cls.tmp.name)
        findings, cls.externals = audit.audit(cls.index)
        cls.names = {}
        for f in findings:
            cls.names.setdefault(f['check'], set()).add(f['name'])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def has(self, check, name):
        self.assertIn(name, self.names.get(check, set()), '%s %s not reported; got %s' % (check, name, self.names.get(check)))

    def lacks(self, check, name):
        self.assertNotIn(name, self.names.get(check, set()))

    def test_parser_keeps_lines_and_survives_bad_braces(self):
        nodes, problems = parse('a = {\n b = 1 # c = 2\n}\n}\nd = {')
        self.assertEqual(nodes[0].value[0].line, 2)
        self.assertEqual(len(nodes[0].value), 1)
        self.assertEqual(len(problems), 2)

    def test_flags(self):
        self.has('flag-read-never-set', 'global:ac_never')
        self.lacks('flag-read-never-set', 'global:ac_beta_set')          # matches the ac_$what$_set pattern
        self.lacks('flag-read-never-set', 'country:AAA_done')
        self.lacks('flag-set-never-read', 'global:ac_$what$_set')          # read as ac_alpha_set and ac_beta_set

    def test_events(self):
        self.has('event-undefined', 'a.404')
        self.lacks('event-undefined', 'news.1')                            # vanilla namespace: external
        self.has('event-no-caller', 'a.2')
        for live in ('a.1', 'a.3', 'a.4', 'a.5'):
            self.lacks('event-no-caller', live)
        self.assertEqual(self.externals['event'], 1)

    def test_scripted(self):
        self.has('scripted-undefined', 'ac_missing_effect')
        self.has('scripted-param-missing', 'ac_used_effect(what)')
        self.has('scripted-unused', 'ac_unused_effect')
        self.lacks('scripted-unused', 'ac_used_effect')
        self.has('scripted-unused', 'ac_used_trigger')                     # defined, never called in the mini mod

    def test_ideas_characters_decisions(self):
        self.has('idea-undefined', 'AAA_ghost')
        self.lacks('idea-undefined', 'CHI_vanilla')
        self.lacks('idea-undefined', 'AAA_air_token')
        self.has('idea-unreferenced', 'AAA_lonely')
        self.lacks('idea-unreferenced', 'AAA_law')
        self.has('character-undefined', 'AAA_nobody')
        self.has('decision-undefined', 'ac_gone')
        self.has('category-undefined', 'ac_lost_category')

    def test_trees(self):
        self.has('tree-unassignable', 'ac_stranded')
        self.lacks('tree-unassignable', 'ac_loaded')
        self.lacks('tree-unassignable', 'ac_assigned')
        self.has('tree-load-undefined', 'ac_missing_tree')
        self.has('shared-focus-undefined', 'AAA_absent')
        self.has('shared-focus-unimported', 'AAA_island')
        self.lacks('shared-focus-unimported', 'AAA_child')

    def test_variables_map_and_empty_blocks(self):
        self.has('variable-read-never-set', 'ac_ghost')
        self.lacks('variable-read-never-set', 'ac_var')
        self.has('state-undefined', '99')
        self.lacks('state-undefined', '1')
        self.has('province-undefined', '77')
        self.has('empty-guarded-block', 'common/decisions/a.txt:ac_cat/if#1')
        self.has('empty-guarded-block', 'common/decisions/a.txt:ac_cat/if#2')
        self.assertEqual(1, len([n for n in self.names.get('empty-else', ()) if n.startswith('events/a.txt')]))
        self.assertFalse([n for n in self.names.get('empty-guarded-block', ()) if n.startswith('events/')])

    def test_localisation(self):
        self.has('loc-missing', 'a.2.t')
        self.lacks('loc-missing', 'a.1.t')
        self.has('loc-missing', 'AAA_own')
        self.lacks('loc-missing', 'AAA_root_desc')

    def test_allowlist_and_ratchet_keys(self):
        findings = [audit.finding('flag-read-never-set', 'global:ac_never'), audit.finding('event-undefined', 'a.404')]
        entries = [{'check': 'flag-read-never-set', 'name': 'global:ac_*', 'class': 'intentional', 'reason': 'x', 'layer': 'y'},
                   {'check': 'loc-missing', 'name': 'nothing', 'class': 'intentional', 'reason': 'x', 'layer': 'y'}]
        active, allowed, stale = audit.apply_allowlist(findings, entries)
        self.assertEqual(['event-undefined|a.404'], [audit.key(f) for f in active])
        self.assertEqual(1, len(allowed))
        self.assertEqual('nothing', stale[0]['name'])

    def test_reference_root_resolves_vanilla_names(self):
        with tempfile.TemporaryDirectory() as game:
            write(game, {'common/ideas/v.txt': 'ideas = { country = { CHI_vanilla = { } } }\n',
                         'events/news.txt': 'add_namespace = news\nnews_event = { id = news.1 is_triggered_only = yes }\n',
                         'common/decisions/v.txt': 'v_cat = { AAA_ghost_decision = { } }\n'})
            write(self.tmp.name, {'descriptor.mod': 'replace_path="common/decisions"\n'})
            index = Index(self.tmp.name, game)
            names = {(f['check'], f['name']) for f in audit.audit(index)[0]}
            self.assertNotIn(('idea-undefined', 'CHI_vanilla'), names)
            self.assertNotIn(('event-undefined', 'news.1'), names)
            self.assertNotIn('AAA_ghost_decision', index.decisions)       # replace_path hides vanilla decisions


def current():
    index, active, allowed, stale, externals = audit.run()
    gated = sorted({audit.key(f) for f in active if f['severity'] in audit.GATED})
    return index, active, allowed, stale, externals, gated


def ratchet(record=False):
    index, active, allowed, stale, externals, gated = current()
    print(audit.summary(active, allowed, externals, index))
    problems = []
    if stale:
        problems.append('allowlist entries that match nothing (remove them): ' + '; '.join(
            '%s %s' % (e['check'], e['name']) for e in stale))
    if index.problems:
        problems.append('parse problems: ' + '; '.join(index.problems[:10]))
    old = json.loads(BASELINE.read_text(encoding='utf-8'))['findings'] if BASELINE.exists() else None
    new = [k for k in gated if old is not None and k not in old]
    if new:
        problems.append('new wiring findings (fix them, or allowlist with a reason):\n  ' + '\n  '.join(new))
    if record:
        if new:
            raise SystemExit('Refusing to record: ' + '\n'.join(problems))
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps({'schema': 1, 'generator': 'tools/Test-Wiring.py --record',
                                        'about': 'Active wiring defects and warnings still to fix; may only shrink.',
                                        'counts': {s: sum(1 for k in gated if audit.SEVERITY[k.split('|')[0]] == s) for s in audit.GATED},
                                        'findings': gated}, indent=1) + '\n', encoding='utf-8', newline='\n')
        print('Wiring baseline recorded: %d findings' % len(gated))
        return
    if old is None:
        problems.append('no baseline; run --record')
    else:
        fixed = [k for k in old if k not in gated]
        if fixed:
            problems.append('fixed findings still in the baseline (run --record to lower it):\n  ' + '\n  '.join(fixed))
    if problems:
        raise SystemExit('Wiring ratchet failed:\n' + '\n'.join(problems))
    print('Wiring ratchet: %d open findings, none new' % len(gated))


def main():
    record = '--record' in sys.argv
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Synthetic)
    if not unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful():
        raise SystemExit(1)
    ratchet(record)


if __name__ == '__main__':
    main()
