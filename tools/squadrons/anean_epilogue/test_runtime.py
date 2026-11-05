"""Offline regressions for the Anean continuations (ac_sqa), 2015-2016.

The compiled preview runs in the story interpreter (tools/squadrons/southern/
harness.py); the adapter supplies dates, identity, wars and the published
ac_eew flags, and plays the original story's recorded conclusion by setting
the exact flag its pinned compiler writes. Offline evidence, not a native run.
"""
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
STORY = HERE.parent
sys.path[:0] = [str(HERE), str(STORY / 'southern')]
from build import N, STEM, compile_rows, encode, mod_files, summary  # noqa: E402
from epilogue_contract import ADMITTED, KINDS, WINDOW, epilogues, source_story  # noqa: E402
from harness import StoryWorld, day  # noqa: E402

TAGS = ('EMM', 'EVA')
COUNTER = {'EMM': 'EVA', 'EVA': 'EMM'}
WAR = ('ac_eew_calendar_started', 'ac_eew_signature_seen', 'ac_eew_started')
SCENARIOS = {
    'quiet': dict(),
    'signature': dict(flags=('ac_eew_calendar_started', 'ac_eew_signature_seen')),
    'withheld': dict(flags=('ac_eew_calendar_started', 'ac_eew_declaration_withheld', 'ac_eew_closed')),
    'divergent': dict(flags=('ac_eew_route_divergent', 'ac_eew_closed')),
    'unreachable': dict(flags=('ac_eew_route_unreachable', 'ac_eew_closed')),
    'war': dict(war=True, flags=WAR),
    'war_no_air': dict(war=True, air=False, flags=WAR),
    'gracemeria': dict(war=True, flags=WAR + ('ac_eew_stage_gracemeria',)),
    'liberation': dict(war=True, flags=WAR + ('ac_eew_stage_gracemeria', 'ac_eew_stage_liberation')),
    'coup': dict(war=True, flags=WAR + ('ac_eew_stage_gracemeria', 'ac_eew_stage_liberation', 'ac_eew_stage_coup')),
    'ceasefire': dict(flags=WAR + ('ac_eew_stage_gracemeria', 'ac_eew_stage_liberation', 'ac_eew_stage_coup', 'ac_eew_ceasefire_signed',
                                   'ac_eew_outcome_ceasefire', 'ac_eew_ended')),
    'emmerian_victory': dict(flags=WAR + ('ac_eew_stage_gracemeria', 'ac_eew_stage_liberation', 'ac_eew_outcome_emmerian_victory', 'ac_eew_ended')),
    'estovakian_victory': dict(flags=WAR + ('ac_eew_stage_gracemeria', 'ac_eew_outcome_estovakian_victory', 'ac_eew_ended', 'ac_eew_emm_fallen')),
    'capitulated': dict(war=True, capitulated=True, flags=WAR + ('ac_eew_stage_gracemeria',)),
}


class AneanEpilogues(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {r['tag']: r for r in epilogues()}
        cls.preview = compile_rows(list(cls.rows.values()))
        cls.folder = tempfile.TemporaryDirectory()
        for relative, text in cls.preview.items():
            target = Path(cls.folder.name) / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encode(relative, text))

    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def world(self, enabled=True):
        return StoryWorld(self.folder.name, STEM, N, TAGS, enabled)

    def ident(self, tag, number):
        return N + '.' + str(self.rows[tag]['base'] + number)

    def concluded(self, kinds, when='2015.1.1', enabled=True):
        """The original story's recorded conclusion, as its pinned compiler writes it."""
        w = self.world(enabled).at(when)
        for tag, kind in kinds.items():
            if kind:
                w.countries[tag].flags['ac_sq_' + tag.lower() + '_ending_' + kind] = None
        return w

    def run_to(self, w, until, choose=0):
        while w.today < day(until):
            for tag, ident in w.week(TAGS):
                if choose is not None:
                    self.assertTrue(w.choose(ident, choose, tag), ident)
        return w

    def apply(self, w, tag, scenario):
        state = SCENARIOS[scenario]
        c = w.countries[tag]
        c.air = state.get('air', True)
        c.capitulated = state.get('capitulated', False)
        w.global_flags = set(state.get('flags', ()))
        w.wars = {frozenset(TAGS)} if state.get('war') else set()

    # ---------------------------------------------------------------------------------
    def test_source_preview_record_and_nothing_ships_before_admission(self):
        self.assertEqual(set(self.rows), set(TAGS))
        self.assertEqual(ADMITTED, ())
        self.assertEqual(mod_files(), [])
        record = json.loads((HERE / 'preview.json').read_text(encoding='utf-8'))
        self.assertEqual(record, json.loads(json.dumps(summary(list(self.rows.values()), self.preview))))

    def test_the_pinned_original_compiler_writes_the_conclusion_flags_read_here(self):
        events = (STORY.parents[1] / 'mod/2985041246/events/ac_squadrons.txt').read_text(encoding='utf-8-sig')
        for tag in TAGS:
            for kind in KINDS:
                self.assertIn('set_country_flag = ac_sq_' + tag.lower() + '_ending_' + kind, events)
            self.assertEqual(source_story(tag)['id'], self.rows[tag]['source_story'])

    def test_no_recorded_conclusion_no_epilogue(self):
        w = self.run_to(self.concluded({'EMM': None, 'EVA': None}), '2017.3.1')
        self.assertEqual(w.deliveries, [])
        off = self.run_to(self.concluded({'EMM': 'trusted', 'EVA': 'trusted'}, enabled=False), '2017.3.1')
        self.assertEqual(off.deliveries, [])

    def test_each_conclusion_reads_only_its_own_scenes_and_permitted_cast(self):
        for kind in KINDS:
            w = self.run_to(self.concluded({'EMM': kind, 'EVA': kind}), '2017.3.1')
            for tag, row in self.rows.items():
                seen = [(ident, descs) for t, ident, descs in w.deliveries if t == tag]
                self.assertEqual([i for i, _ in seen], [self.ident(tag, n) for n in range(1, 7)], (tag, kind))
                cast = source_story(tag)['cast']
                banned = [p['name'].split()[0] for p in cast if p['id'] not in row['cast_by_ending'][kind]]
                for ident, descs in seen:
                    self.assertEqual(len(descs), 1, ident)
                    self.assertIn('.d_' + kind + '_', descs[0])
                    text = w.loc[descs[0]]
                    for name in banned:
                        self.assertIsNone(re.search(r'\b' + name + r'\b', text), (ident, kind, name))
                flags = w.countries[tag].flags
                self.assertIn(N + '_' + tag.lower() + '_complete', flags)
                self.assertIn(N + '_' + tag.lower() + '_kind_' + kind, flags)

    def test_every_national_context_is_reached_by_an_actual_record_and_frozen(self):
        for tag, row in self.rows.items():
            for chapter in row['chapters']:
                expected = {c['id'] for c in chapter['contexts']} | {'default'}
                reached = set()
                for scenario in SCENARIOS:
                    w = self.concluded({tag: 'trusted'}, chapter['earliest'])
                    w.action('on_weekly', tag)
                    c = w.countries[tag]
                    c.variables[N + '_chapter'] = chapter['id'] - 1
                    c.variables[N + '_pending_chapter'] = 0
                    c.flags.pop(N + '_dispatch_pending', None)
                    w.queue = []
                    self.apply(w, tag, scenario)
                    w.execute([(N + '_' + tag.lower() + '_dispatch', '=', 'yes')], c)
                    w.today += 1
                    self.assertEqual(w.deliver_due(), [(tag, self.ident(tag, chapter['id']))], (tag, chapter['id'], scenario))
                    descs = w.deliveries[-1][2]
                    self.assertEqual(len(descs), 1)
                    reached.add(re.match(r'.*\.d_trusted_(.+?)(_callback)?$', descs[0])[1])
                    self.apply(w, tag, 'quiet' if scenario != 'quiet' else 'war')
                    self.assertEqual(w.descriptions(self.ident(tag, chapter['id']), c), descs)
                self.assertEqual(reached, expected, (tag, chapter['id']))

    def test_window_closes_late_saves_and_unanswered_scenes(self):
        late = self.run_to(self.concluded({'EMM': 'trusted', 'EVA': 'fractured'}, '2017.1.5'), '2017.6.1')
        self.assertEqual(late.deliveries, [])
        self.assertIn(N + '_late_archive', late.countries['EMM'].flags)
        idle = self.run_to(self.concluded({'EMM': 'compromised', 'EVA': 'compromised'}), '2017.3.1', choose=None)
        for tag in TAGS:
            flags = idle.countries[tag].flags
            self.assertIn(N + '_' + tag.lower() + '_missed_1', flags)
            self.assertIn(N + '_closed', flags)
            self.assertNotIn(N + '_' + tag.lower() + '_complete', flags)
            first = self.rows[tag]['chapters'][0]
            self.assertFalse(idle.choose(self.ident(tag, 1), 0, tag))
            self.assertNotIn(N + '_' + tag.lower() + '_' + first['options'][0]['flag'], flags)

    def test_callbacks_follow_the_earlier_choice(self):
        for tag, row in self.rows.items():
            for index in range(2):
                w = self.run_to(self.concluded({tag: 'trusted'}), '2017.3.1', choose=index)
                picked = {o['flag'] for c in row['chapters'] for o in c['options'][index:index + 1]}
                for t, ident, descs in w.deliveries:
                    if t != tag:
                        continue
                    chapter = row['chapters'][int(ident.split('.')[1]) - row['base'] - 1]
                    if chapter.get('callback'):
                        self.assertEqual(descs[0].endswith('_callback'), chapter['callback']['flag'] in picked, ident)

    def test_annexation_interrupts_and_choices_change_only_personal_state(self):
        w = self.run_to(self.concluded({'EMM': 'trusted', 'EVA': 'trusted'}), '2015.9.1')
        before = len([1 for t, _, _ in w.deliveries if t == 'EMM'])
        w.countries['EMM'].exists = False
        w.action('on_annex', 'EVA', other='EMM')
        self.assertIn(N + '_interrupted', w.countries['EMM'].flags)
        self.run_to(w, '2017.3.1')
        self.assertEqual(len([1 for t, _, _ in w.deliveries if t == 'EMM']), before)
        text = '\n'.join(v for k, v in self.preview.items() if not k.endswith('.yml'))
        for forbidden in ('declare_war_on', 'white_peace', 'set_global_flag', 'add_ideas', 'add_timed_idea', 'add_political_power',
                          'add_equipment', 'annex_country', 'add_manpower', 'cohesion', 'credibility'):
            self.assertNotIn(forbidden, text)


if __name__ == '__main__':
    unittest.main()
