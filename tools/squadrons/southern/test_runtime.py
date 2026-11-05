"""Offline regressions for the Aurelian and Leasathian stories (ac_sqs).

The compiled preview is executed by the story interpreter in harness.py: the
actual dispatch, delivery, choice, expiry, interrupt and ending scripts run as
text; the adapter supplies dates, identity, wars, capitulation, aircraft and
the published ac_alc/ac_lcw flags. Offline evidence, not a native run.
"""
import itertools
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build import NAMESPACE, STEM, compile_rows, encode, mod_files, summary  # noqa: E402
from harness import StoryWorld, day  # noqa: E402
from story_contract import ADMITTED, published_flags, stories  # noqa: E402

TAGS = ('AUR', 'LEA')
COUNTER = {'AUR': 'LEA', 'LEA': 'AUR'}
# Observable states a story may read; every conditional scene must be reached by one.
SCENARIOS = {
    'peace': dict(),
    'no_air': dict(air=False),
    'civil_war': dict(flags=('ac_lcw_started',)),
    'civil_negotiated': dict(flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_lcw_negotiated')),
    'civil_historical': dict(flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_lcw_historical_end')),
    'civil_prolonged': dict(flags=('ac_lcw_started', 'ac_lcw_prolonged', 'ac_alc_route_unreachable', 'ac_alc_closed')),
    'withheld': dict(flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_declaration_withheld', 'ac_alc_closed')),
    'war': dict(war=True, flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started')),
    'war_no_air': dict(war=True, air=False, flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started')),
    'overrun': dict(war=True, flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started', 'ac_alc_stage_overrun')),
    'retaken': dict(war=True, flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started', 'ac_alc_stage_overrun', 'ac_alc_stage_griswall')),
    'removal': dict(war=True, flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started', 'ac_alc_stage_removal')),
    'ceasefire': dict(flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started', 'ac_alc_stage_removal', 'ac_alc_ceasefire_signed',
                             'ac_alc_outcome_ceasefire', 'ac_alc_ended')),
    'aurelian_victory': dict(flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started', 'ac_alc_stage_overrun', 'ac_alc_stage_griswall',
                                    'ac_alc_outcome_aurelian_victory', 'ac_alc_ended')),
    'leasathian_victory': dict(flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started', 'ac_alc_stage_overrun',
                                      'ac_alc_outcome_leasathian_victory', 'ac_alc_ended')),
    'capitulated': dict(war=True, capitulated=True, flags=('ac_lcw_started', 'ac_lcw_ended', 'ac_alc_started', 'ac_alc_stage_overrun')),
}


def ending_kind(cohesion, credibility):
    return 'trusted' if cohesion >= 65 and credibility >= 65 else 'fractured' if cohesion < 45 else 'compromised'


def simulate(row, picks):
    cohesion = credibility = 50
    for chapter, index in zip(row['chapters'], picks):
        option = chapter['options'][index]
        cohesion = min(100, max(0, cohesion + option['cohesion']))
        credibility = min(100, max(0, credibility + option['credibility']))
    return ending_kind(cohesion, credibility)


def path_to(row, kind):
    """A deterministic choice path that reaches the requested conclusion."""
    keys = {'trusted': lambda o: o['cohesion'] + o['credibility'], 'fractured': lambda o: -o['cohesion'],
            'compromised': lambda o: o['cohesion'] - o['credibility']}
    picks = [max(range(len(c['options'])), key=lambda i: keys[kind](c['options'][i])) for c in row['chapters']]
    if simulate(row, picks) == kind:
        return picks
    for flip in itertools.product(*[range(len(c['options'])) for c in row['chapters'][:6]]):
        trial = list(flip) + picks[6:]
        if simulate(row, trial) == kind:
            return trial
    raise AssertionError('No path to ' + kind + ' for ' + row['tag'])


class SouthernStories(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {r['tag']: r for r in stories()}
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
        return StoryWorld(self.folder.name, STEM, NAMESPACE, TAGS, enabled)

    def ident(self, tag, number):
        return NAMESPACE + '.' + str(self.rows[tag]['base'] + number)

    def run_to(self, w, until, choose=None):
        while w.today < day(until):
            for tag, ident in w.week(TAGS):
                if choose is not None:
                    index = choose(tag, ident)
                    if index is not None:
                        self.assertTrue(w.choose(ident, index, tag), ident)
        return w

    def apply(self, w, tag, scenario):
        state = SCENARIOS[scenario]
        c = w.countries[tag]
        c.air = state.get('air', True)
        c.capitulated = state.get('capitulated', False)
        w.global_flags = set(state.get('flags', ()))
        w.wars = {frozenset((tag, COUNTER[tag]))} if state.get('war') else set()

    def open_scene(self, w, tag, number):
        """Reserve and deliver one chapter through the real dispatch effect."""
        c = w.countries[tag]
        chapter = self.rows[tag]['chapters'][number - 1]
        for name in list(c.flags):
            if name in (NAMESPACE + '_dispatch_pending', NAMESPACE + '_cooldown') or name.startswith(NAMESPACE + '_' + tag.lower() + '_view_'):
                c.flags.pop(name)
        c.flags.pop(NAMESPACE + '_' + tag.lower() + '_delivered_' + str(number), None)
        c.variables[NAMESPACE + '_pending_chapter'] = 0
        c.variables[NAMESPACE + '_chapter'] = number - 1
        w.queue = []
        w.at(chapter['earliest'])
        w.execute([(NAMESPACE + '_' + tag.lower() + '_dispatch', '=', 'yes')], c)
        w.today += 1
        delivered = w.deliver_due()
        self.assertEqual(delivered, [(tag, self.ident(tag, number))])
        return w.deliveries[-1][2]

    def started(self, when='1991.1.1', enabled=True):
        w = self.world(enabled).at(when)
        w.action('on_startup')
        return w

    # ---------------------------------------------------------------------------------
    def test_source_preview_record_and_nothing_ships_before_admission(self):
        self.assertEqual(set(self.rows), set(TAGS))
        self.assertEqual(ADMITTED, ())
        self.assertEqual(mod_files(), [], 'No southern story file may ship before its art is reviewed')
        record = json.loads((HERE / 'preview.json').read_text(encoding='utf-8'))
        self.assertEqual(record, json.loads(json.dumps(summary(list(self.rows.values()), self.preview))))
        self.assertFalse(record['native_acceptance'])

    def test_every_event_key_is_localised_and_scenes_equal_the_authored_text(self):
        w = self.world()
        for ident, node in w.events.items():
            keys = [v for k, _, v in node if k == 'title']
            keys += [v if isinstance(v, str) else dict((a, b) for a, _, b in v)['text'] for k, _, v in node if k == 'desc']
            for k, _, v in node:
                if k == 'option':
                    name = dict((a, b) for a, _, b in v if not isinstance(b, list))['name']
                    keys.append(name)
                    keys += [b for a, _, b in v if a == 'custom_effect_tooltip']
            for key in keys:
                self.assertIn(key, w.loc, ident)
        for tag, row in self.rows.items():
            for chapter in row['chapters']:
                base = w.loc[self.ident(tag, chapter['id']) + '.d_base']
                self.assertEqual(base, chapter['text'])
                if chapter.get('callback'):
                    self.assertEqual(w.loc[self.ident(tag, chapter['id']) + '.d_base_callback'], chapter['text'] + '\n\n' + chapter['callback']['text'])
                for variant in chapter.get('condition_variants', []):
                    self.assertEqual(w.loc[self.ident(tag, chapter['id']) + '.d_' + variant['id']], variant['text'])
        flags = published_flags()
        self.assertTrue({'ac_alc_started', 'ac_alc_stage_overrun', 'ac_lcw_started', 'ac_lcw_prolonged'} <= flags)

    def test_full_path_delivers_twenty_chapters_then_one_conclusion_per_story(self):
        w = self.run_to(self.started(), '2021.6.1', choose=lambda tag, ident: 0)
        for tag, row in self.rows.items():
            seen = [ident for t, ident, descs in w.deliveries if t == tag]
            self.assertEqual(seen[:20], [self.ident(tag, n) for n in range(1, 21)])
            kind = simulate(row, [0] * 20)
            self.assertEqual(seen[20:], [self.ident(tag, 90 + ['trusted', 'compromised', 'fractured'].index(kind))])
            self.assertIn(NAMESPACE + '_' + tag.lower() + '_ending_' + kind, w.countries[tag].flags)
            for _, ident, descs in w.deliveries:
                self.assertEqual(len(descs), 1, ident)

    def test_all_three_conclusions_are_reachable_with_the_actual_script(self):
        for tag, row in self.rows.items():
            for kind in ('trusted', 'compromised', 'fractured'):
                picks = path_to(row, kind)
                w = self.run_to(self.started(), '2021.6.1',
                                choose=lambda t, ident: picks[int(ident.split('.')[1]) - row['base'] - 1]
                                if t == tag and int(ident.split('.')[1]) - row['base'] <= 20 else 0)
                self.assertIn(NAMESPACE + '_' + tag.lower() + '_ending_' + kind, w.countries[tag].flags, (tag, kind))
                idea = NAMESPACE + '_professional_debrief'
                self.assertEqual(idea in w.countries[tag].ideas, kind == 'trusted')
            self.assertGreaterEqual(len({p for p in path_to(row, 'trusted')}), 2, 'The trusted path should use more than one button')

    def test_every_conditional_scene_is_reached_by_an_actual_record_and_frozen(self):
        for tag, row in self.rows.items():
            for chapter in row['chapters']:
                expected = {v['id'] for v in chapter.get('condition_variants', [])} | {'base'} | ({'cap'} if 'capitulated_text' in chapter else set())
                reached = {}
                for scenario in SCENARIOS:
                    w = self.started()
                    self.apply(w, tag, scenario)
                    descs = self.open_scene(w, tag, chapter['id'])
                    self.assertEqual(len(descs), 1, (tag, chapter['id'], scenario))
                    context = re.match(r'.*\.d_(.+?)(_callback)?$', descs[0])[1]
                    reached.setdefault(context, scenario)
                    # The record changes afterwards; the delivered context is frozen.
                    self.apply(w, tag, 'peace' if scenario != 'peace' else 'war')
                    self.assertEqual(w.descriptions(self.ident(tag, chapter['id']), w.countries[tag]), descs)
                self.assertEqual(set(reached), expected, (tag, chapter['id'], reached))

    def test_callbacks_follow_the_earlier_choice_only(self):
        for tag, row in self.rows.items():
            for chapter in row['chapters']:
                if not chapter.get('callback'):
                    continue
                w = self.started()
                descs = self.open_scene(w, tag, chapter['id'])
                self.assertFalse(descs[0].endswith('_callback'))
                w = self.started()
                w.countries[tag].flags[NAMESPACE + '_' + tag.lower() + '_' + chapter['callback']['flag']] = None
                descs = self.open_scene(w, tag, chapter['id'])
                self.assertTrue(descs[0].endswith('_callback'), (tag, chapter['id']))

    def test_late_admission_files_earlier_acts_without_their_choices(self):
        w = self.run_to(self.started('2012.3.1'), '2021.6.1', choose=lambda tag, ident: 0)
        for tag, row in self.rows.items():
            numbers = [int(ident.split('.')[1]) - row['base'] for t, ident, _ in w.deliveries if t == tag]
            self.assertGreaterEqual(numbers[0], 11, tag)
            flags = w.countries[tag].flags
            for chapter in row['chapters'][:10]:
                self.assertIn(NAMESPACE + '_' + tag.lower() + '_missed_' + str(chapter['id']), flags)
                for option in chapter['options']:
                    self.assertNotIn(NAMESPACE + '_' + tag.lower() + '_' + option['flag'], flags)
        late = self.run_to(self.started('2021.2.1'), '2021.6.1')
        self.assertEqual(late.deliveries, [])

    def test_unanswered_scene_expires_once_and_a_stale_answer_does_nothing(self):
        w = self.run_to(self.started(), '1991.1.20')
        ident = self.ident('AUR', 1)
        self.assertIn(('AUR', ident), [(t, i) for t, i, _ in w.deliveries])
        self.run_to(w, '1991.3.1')
        aur = w.countries['AUR']
        self.assertIn(NAMESPACE + '_aur_missed_1', aur.flags)
        self.assertFalse(w.choose(ident, 0, 'AUR'))
        self.assertEqual(aur.variables[NAMESPACE + '_cohesion'], 50)
        self.assertEqual([i for t, i, _ in w.deliveries if t == 'AUR'].count(ident), 1)

    def test_annexation_interrupts_and_the_rule_disables_everything(self):
        w = self.run_to(self.started(), '1995.1.1', choose=lambda tag, ident: 0)
        before = len([1 for t, _, _ in w.deliveries if t == 'LEA'])
        w.countries['LEA'].exists = False
        w.action('on_annex', 'AUR', other='LEA')
        self.assertIn(NAMESPACE + '_interrupted', w.countries['LEA'].flags)
        self.run_to(w, '2000.1.1', choose=lambda tag, ident: 0)
        self.assertEqual(len([1 for t, _, _ in w.deliveries if t == 'LEA']), before)
        off = self.run_to(self.started(enabled=False), '1995.1.1')
        self.assertEqual(off.deliveries, [])
        self.assertTrue(all(not c.flags for c in off.countries.values()))

    def test_the_interpreter_runs_the_shipped_pacific_stories_end_to_end(self):
        w = StoryWorld(HERE.parents[2] / 'mod/2985041246', 'ac_squadrons_pacific', 'ac_sqp', ('OSE', 'YUK')).at('1991.1.1')
        w.action('on_startup')
        while w.today < day('2021.6.1'):
            for tag, ident in w.week(('OSE', 'YUK')):
                self.assertTrue(w.choose(ident, 0, tag), ident)
        for tag, base in (('OSE', 700), ('YUK', 800)):
            seen = [ident for t, ident, _ in w.deliveries if t == tag]
            self.assertEqual(seen[:20], ['ac_sqp.' + str(base + n) for n in range(1, 21)])
            self.assertEqual(len(seen), 21)
        self.assertTrue(all(len(descs) == 1 for _, _, descs in w.deliveries))

    def test_choices_change_only_personal_story_state(self):
        allowed = {'set_country_flag', 'set_variable', 'add_to_variable', 'clamp_variable', 'clr_country_flag', 'if',
                   'custom_effect_tooltip', 'add_timed_idea'}
        w = self.world()
        for ident, node in w.events.items():
            for key, _, option in node:
                if key != 'option':
                    continue
                for k, _, v in option:
                    if k == 'if':
                        self.assertTrue({a for a, _, _ in v if a != 'limit'} <= allowed, ident)
                    elif k not in ('name', 'trigger', 'ai_chance'):
                        self.assertIn(k, allowed, ident)
        effects = '\n'.join(self.preview.values())
        for forbidden in ('declare_war_on', 'white_peace', 'annex_country', 'transfer_state', 'add_political_power', 'add_equipment',
                          'set_politics', 'create_country_leader', 'set_global_flag', 'add_manpower', 'add_ideas'):
            self.assertNotIn(forbidden, effects)


if __name__ == '__main__':
    unittest.main()
