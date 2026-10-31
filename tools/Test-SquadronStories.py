"""Execute the shipped squadron scripts with the Continental War interpreter.

Unknown effects/triggers fail closed. The model includes original versus current
tags, real reservation dates, event delivery/immediate effects, and read-only
archives. Deepcopy reloads are explicitly offline persistence checks, not native
HOI4 parsing, save serialization, aircraft observations, AI pacing or visual QA.
"""
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools/squadrons'))
from economy_script import parse, fields
from schema import campaigns, validate

spec = importlib.util.spec_from_file_location('squadron_ucw', ROOT / 'tools/Test-ContinentalWar.py')
ucw = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ucw
spec.loader.exec_module(ucw)
STORIES = campaigns()
BY_TAG = {row['tag']: row for row in STORIES}


def load(relative):
    return parse((MOD / relative).read_text(encoding='utf-8-sig'))


def mapping(nodes):
    return {key: value for key, _, value in nodes}


def walk(nodes):
    for key, _, value in nodes:
        if isinstance(value, list):
            yield key, value
            yield from walk(value)


def story_flag(row, short):
    return 'ac_sq_' + row['tag'].lower() + '_' + short


def core_id(row, number):
    return 'ac_sq.' + str(row['base'] + number)


def ending_kind(cohesion, credibility):
    return 'trusted' if cohesion >= 65 and credibility >= 65 else 'fractured' if cohesion < 45 else 'compromised'


class World(ucw.World):
    """Reuse the fail-closed executor; load only this owner's actual libraries."""
    library = None

    def __init__(self, when='1991.1.1', enabled=True):
        if World.library is None:
            raw_events = load('events/ac_squadrons.txt')
            events = {}
            for kind, _, node in raw_events:
                if kind != 'country_event':
                    continue
                ident = mapping(node)['id']
                if ident in events:
                    raise AssertionError('Duplicate squadron event: ' + ident)
                events[ident] = (kind, node)
            categories = mapping(load('common/decisions/categories/ac_squadrons.txt'))
            decisions = {}
            for category, _, rows in load('common/decisions/ac_squadrons.txt'):
                for ident, _, node in rows:
                    if ident in decisions:
                        raise AssertionError('Duplicate squadron decision: ' + ident)
                    decisions[ident] = (category, node)
            World.library = (
                mapping(load('common/scripted_effects/ac_squadrons.txt')),
                mapping(load('common/scripted_triggers/ac_squadrons.txt')),
                events, categories, decisions,
                mapping(mapping(load('common/on_actions/ac_squadrons.txt'))['on_actions']))
        self.effects, self.triggers, self.events, self.categories, self.decision_rows, self.actions = World.library
        self.decisions = {ident: row for ident, (_, row) in self.decision_rows.items()}
        self.today = ucw.day(when)
        self.enabled = enabled
        self.globals = {'ac_ucw_calendar_started', 'ac_anea_accord'}
        self.countries = {tag: ucw.Country(tag) for tag in (*BY_TAG, 'FCU', 'NPT', 'OSE', 'YUK', 'ZZZ')}
        for country in self.countries.values():
            country.original_tag = country.tag
            country.air_manpower = 1
            country.political_power = 300
            country.equipment = {'infantry_equipment': 19}
            country.variables.update(ac_macro_cash=123, ac_anea_recovery=37, ac_ucw_pressure=11, ac_pwi_recovery=9)
        self.faction = {}
        self.wars = set()
        self.controllers = {310: 'SNS', 224: 'BLK', 335: 'UST'}
        self.rule = False
        self.fiscal = False
        self.queue = []
        self.news = []
        self.deliveries = []

    def number(self, value, country):
        if value == 'deployed_airforce_manpower_k':
            return country.air_manpower
        # HOI4 unset variables evaluate to zero. Unknown foreign observables
        # still fail closed through the existing interpreter.
        if value.startswith('ac_sq_'):
            return country.variables.get(value, 0)
        return super().number(value, country)

    def trigger(self, nodes, country):
        answers = []
        for key, operator, value in nodes:
            if key == 'tag':
                answers.append(country.tag == value)
            elif key == 'original_tag':
                answers.append(country.original_tag == value)
            elif key == 'has_game_rule':
                assert fields(value) == {'rule': 'ac_sq_stories', 'option': 'enabled'}
                answers.append(self.enabled)
            else:
                answers.append(super().trigger([(key, operator, value)], country))
        return all(answers)

    def execute(self, nodes, country):
        branch = None
        for key, operator, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    branch = False
                elif branch is None:
                    raise AssertionError('Orphaned ' + key)
                condition = key == 'else' or self.trigger(mapping(value)['limit'], country)
                if not branch and condition:
                    self.execute([n for n in value if n[0] != 'limit'], country)
                    branch = True
                continue
            branch = None
            if key == 'every_country':
                for target in self.countries.values():
                    if target.exists and self.trigger(mapping(value).get('limit', []), target):
                        self.execute([n for n in value if n[0] != 'limit'], target)
            elif key == 'add_timed_idea':
                data = fields(value)
                assert data['idea'] == 'ac_sq_professional_debrief'
                country.ideas[data['idea']] = self.today + int(data['days'])
            else:
                super().execute([(key, operator, value)], country)

    def action(self, name):
        body = mapping(self.actions[name])['effect']
        if name == 'on_startup':
            self.execute(body, None)
        else:
            for country in self.countries.values():
                if country.exists:
                    self.execute(body, country)

    def init(self):
        for tag in BY_TAG:
            self.run('ac_sq_initialize', tag)
        return self

    def advance(self, days):
        self.today += days
        for country in self.countries.values():
            country.ideas = {key: end for key, end in country.ideas.items() if end is None or end > self.today}

    def descriptions(self, ident, tag):
        country = self.countries[tag]
        keys = []
        for key, _, value in self.events[ident][1]:
            if key == 'desc':
                if isinstance(value, str):
                    keys.append(value)
                elif self.trigger(mapping(value).get('trigger', []), country):
                    keys.append(mapping(value)['text'])
        return keys

    def deliver(self, ident, tag):
        country = self.countries[tag]
        node = mapping(self.events[ident][1])
        if not country.exists or not self.trigger(node.get('trigger', []), country):
            return False
        self.execute(node.get('immediate', []), country)
        self.deliveries.append((tag, ident, self.descriptions(ident, tag)))
        return True

    def preferred(self, ident, tag='ERU'):
        options = self.options(ident)
        eligible = [(float(fields(mapping(o).get('ai_chance', [('factor', '=', '0')]))['factor']), i)
                    for i, o in enumerate(options) if self.trigger(mapping(o).get('trigger', []), self.countries[tag])]
        assert eligible, 'Event has no eligible close/choice: ' + ident
        return max(eligible, key=lambda entry: (entry[0], -entry[1]))[1]

    def drain(self):
        while any(when <= self.today for when, _, _ in self.queue):
            entry = min((item for item in self.queue if item[0] <= self.today), key=lambda item: item[0])
            self.queue.remove(entry)
            _, tag, ident = entry
            if self.deliver(ident, tag):
                self.choose(ident, self.preferred(ident, tag), tag)

    def available(self, ident, tag):
        category, row = self.decision_rows[ident]
        country = self.countries[tag]
        return all(self.trigger(mapping(nodes).get(part, []), country)
                   for nodes in (self.categories[category], row) for part in ('allowed', 'visible', 'available'))

    def open_scene(self, row, chapter, war=False, capitulated=False, air=True, callback=False):
        tag = row['tag']; country = self.countries[tag]
        self.today = ucw.day(chapter['earliest'])
        self.run('ac_sq_initialize', tag)
        country.capitulated = capitulated
        country.air_manpower = int(air)
        if war:
            self.wars.add(frozenset((tag, 'ZZZ')))
        country.variables['ac_sq_chapter'] = chapter['id'] - 1
        if callback and chapter.get('callback'):
            country.flags[story_flag(row, chapter['callback']['flag'])] = None
        self.run('ac_sq_' + tag.lower() + '_dispatch', tag)
        ident = core_id(row, chapter['id'])
        assert self.deliver(ident, tag), 'Fixture did not open its actual reserved event'
        return ident, country


class Stories(unittest.TestCase):
    def test_authoring_schema_act_windows_and_generated_outputs(self):
        self.assertEqual(6, len(STORIES))
        self.assertEqual(120, sum(len(row['chapters']) for row in STORIES))
        self.assertEqual(24, sum(len(row['cast']) for row in STORIES))
        self.assertTrue(all(sum('callback' in c for c in row['chapters']) >= 6 for row in STORIES))
        result = subprocess.run([sys.executable, '-B', 'tools/squadrons/build.py', '--check'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        broken = copy.deepcopy(STORIES[0]); broken['chapters'][0]['war_text'] = 'A short replacement.'
        with self.assertRaises(ValueError): validate(broken)
        broken = copy.deepcopy(STORIES[0]); broken['endings'].append(copy.deepcopy(broken['endings'][0]))
        with self.assertRaises(ValueError): validate(broken)

    def test_every_core_option_runs_once_and_changes_only_its_personal_state(self):
        for row in STORIES:
            for chapter in row['chapters']:
                for index, option in enumerate(chapter['options']):
                    with self.subTest(tag=row['tag'], chapter=chapter['id'], option=index):
                        world = World(); ident, country = world.open_scene(row, chapter)
                        foreign = {k: v for k, v in country.variables.items() if not k.startswith('ac_sq_')}
                        before_globals = copy.deepcopy(world.globals)
                        world.choose(ident, index, row['tag'])
                        self.assertEqual(chapter['id'], country.variables['ac_sq_chapter'])
                        self.assertEqual(50 + option['cohesion'], country.variables['ac_sq_cohesion'])
                        self.assertEqual(50 + option['credibility'], country.variables['ac_sq_credibility'])
                        self.assertTrue(world.flag(country, story_flag(row, option['flag'])))
                        self.assertFalse(world.flag(country, 'ac_sq_dispatch_pending'))
                        self.assertEqual(0, country.variables['ac_sq_pending_chapter'])
                        self.assertEqual(foreign, {k: v for k, v in country.variables.items() if not k.startswith('ac_sq_')})
                        self.assertEqual(before_globals, world.globals)
                        self.assertEqual(300, country.political_power)
                        self.assertEqual({'infantry_equipment': 19}, country.equipment)
                        saved = copy.deepcopy(country)
                        for replay in range(len(chapter['options']) + 1): world.choose(ident, replay, row['tag'])
                        self.assertEqual(saved, country)

    def test_exactly_one_display_context_and_callback_and_archive_is_frozen(self):
        for row in STORIES:
            for chapter in row['chapters']:
                for war in (False, True):
                    for cap in (False, True):
                        for air in (False, True):
                            for callback in ((False, True) if chapter.get('callback') else (False,)):
                                world = World(); ident, country = world.open_scene(row, chapter, war, cap, air, callback)
                                keys = world.descriptions(ident, row['tag'])
                                variants = [v for v in chapter.get('condition_variants', []) if world.trigger(parse(v['trigger']), country)]
                                context = ('cap' if cap and chapter.get('capitulated_text') else variants[0]['id'] if variants else
                                           'war' if war and not cap and air and chapter.get('war_text') else 'base')
                                self.assertEqual([ident + '.d_' + context + ('_callback' if callback else '')], keys)
                                # A scene already displayed keeps its context while
                                # host circumstances change before it is answered.
                                country.capitulated = not cap; country.air_manpower = not air
                                world.wars.clear() if war else world.wars.add(frozenset((row['tag'], 'ZZZ')))
                                world.globals.clear()
                                world.controllers.update({310: 'ERU', 224: 'ZZZ', 335: 'ZZZ'})
                                world.faction.update({row['tag']: 'FCU', 'FCU': 'FCU', 'BLK': 'FCU', 'UST': 'FCU'})
                                if chapter.get('callback'):
                                    previous = story_flag(row, chapter['callback']['flag'])
                                    country.flags.pop(previous, None) if callback else country.flags.update({previous: None})
                                self.assertEqual(keys, world.descriptions(ident, row['tag']))
                                world.choose(ident, 0, row['tag'])
                                archive = 'ac_sq.' + str(row['base'] + 10000 + chapter['id'])
                                snapshot = copy.deepcopy((world.countries, world.globals, world.wars))
                                self.assertTrue(world.deliver(archive, row['tag']))
                                self.assertEqual(keys, world.descriptions(archive, row['tag']))
                                world.choose(archive, 0, row['tag'])
                                self.assertEqual(snapshot, (world.countries, world.globals, world.wars))

    def test_regional_conditions_are_read_from_actual_owners_and_archived(self):
        fixtures = [
            ('BLK', 8, 'training_return', (), {}, {}),
            ('BLK', 9, 'capital_displaced', (), {}, {224: 'ZZZ'}),
            ('BLK', 17, 'shared_service', (), {'BLK': 'BLK', 'UST': 'BLK'}, {}),
            ('UST', 9, 'capital_displaced', (), {}, {335: 'ZZZ'}),
            ('UST', 17, 'shared_service', (), {'BLK': 'BLK', 'UST': 'BLK'}, {}),
            ('ERU', 12, 'project_unavailable', ('ac_ucw_stonehenge_destroyed',), {}, {}),
            ('ERU', 15, 'coalition_contact', (), {'ERU': 'FCU', 'FCU': 'FCU'}, {}),
            ('SNS', 12, 'project_unavailable', ('ac_ucw_stonehenge_destroyed',), {}, {}),
            ('SNS', 15, 'district_displaced', (), {}, {310: 'ERU'}),
            ('EMM', 11, 'aid_accord', ('ac_anea_accord',), {}, {}),
            ('EMM', 16, 'sanctions_review', ('ac_anea_sanctions_active',), {}, {}),
            ('EVA', 11, 'aid_accord', ('ac_anea_accord',), {}, {}),
            ('EVA', 16, 'sanctions_review', ('ac_anea_sanctions_active',), {}, {}),
            ('EMM', 12, 'service_flight', (), {}, {}),
            ('EVA', 17, 'service_flight', (), {}, {}),
        ]
        for tag, number, context, flags, factions, controllers in fixtures:
            world = World(); world.globals = set(flags); world.faction.update(factions); world.controllers.update(controllers)
            row = BY_TAG[tag]; chapter = row['chapters'][number - 1]
            ident, country = world.open_scene(row, chapter, callback=bool(chapter.get('callback')))
            expected = ident + '.d_' + context + ('_callback' if chapter.get('callback') else '')
            self.assertEqual([expected], world.descriptions(ident, tag))
            world.choose(ident, 0, tag)
            archive = 'ac_sq.' + str(row['base'] + 10000 + number)
            # Reverse every external circumstance after the actual scene choice,
            # including a prior choice's callback. Archived prose is a delivered
            # snapshot; opening and closing it must not mutate either owner.
            world.globals.clear(); world.controllers = {310: 'SNS', 224: 'BLK', 335: 'UST'}; world.faction.clear()
            country.capitulated = True; country.air_manpower = 0
            if chapter.get('callback'):
                country.flags.pop(story_flag(row, chapter['callback']['flag']), None)
            snapshot = copy.deepcopy((world.countries, world.globals, world.controllers, world.faction,
                                      world.wars, world.queue, world.news))
            self.assertTrue(world.deliver(archive, tag))
            self.assertEqual([expected], world.descriptions(archive, tag))
            world.choose(archive, 0, tag)
            self.assertEqual(snapshot, (world.countries, world.globals, world.controllers, world.faction,
                                       world.wars, world.queue, world.news))

    def test_conditional_owner_absence_and_capitulation_fail_closed(self):
        conditional = [(row, chapter) for row in STORIES for chapter in row['chapters']
                       if chapter.get('condition_variants')]
        self.assertEqual(15, len(conditional))
        for row, chapter in conditional:
            for capitulated, owner_positive in ((False, False), (True, False), (True, True)):
                with self.subTest(tag=row['tag'], chapter=chapter['id'], capitulated=capitulated,
                                  owner_positive=owner_positive):
                    world = World()
                    # Restored control, unrelated factions and historical flags
                    # cannot substitute for the live owners. Separately make
                    # EVERY owner condition true while the host has capitulated:
                    # the current campaign then still uses its ground account.
                    world.globals = {'ac_anea_accord_interrupted', 'ac_anea_accord_withdrawn',
                                     'ac_ucw_stonehenge_seized', 'ac_anea_milestone_reviewed'}
                    world.faction = {row['tag']: row['tag'], 'ZZZ': 'ZZZ'}
                    if owner_positive:
                        world.globals = {'ac_anea_accord', 'ac_anea_sanctions_active', 'ac_ucw_stonehenge_destroyed'}
                        world.controllers.update({224: 'ZZZ', 335: 'ZZZ', 310: 'ERU'})
                        world.faction = {tag: 'FCU' for tag in world.countries}
                    ident, country = world.open_scene(row, chapter, capitulated=capitulated, air=owner_positive)
                    self.assertEqual([ident + '.d_base'], world.descriptions(ident, row['tag']))
                    self.assertFalse(any(world.trigger(parse(v['trigger']), country)
                                         for v in chapter['condition_variants']))

    def test_base_archive_does_not_gain_a_later_policy_or_capability_context(self):
        for row in STORIES:
            for chapter in row['chapters']:
                if not chapter.get('condition_variants'):
                    continue
                with self.subTest(tag=row['tag'], chapter=chapter['id']):
                    world = World(); world.globals.clear()
                    ident, country = world.open_scene(row, chapter, air=False)
                    expected = ident + '.d_base'
                    self.assertEqual([expected], world.descriptions(ident, row['tag']))
                    world.choose(ident, 0, row['tag'])
                    world.globals = {'ac_anea_accord', 'ac_anea_sanctions_active', 'ac_ucw_stonehenge_destroyed'}
                    world.controllers.update({224: 'ZZZ', 335: 'ZZZ', 310: 'ERU'})
                    world.faction = {tag: 'FCU' for tag in world.countries}
                    country.air_manpower = 2
                    if chapter.get('callback'):
                        country.flags[story_flag(row, chapter['callback']['flag'])] = None
                    self.assertTrue(any(world.trigger(parse(v['trigger']), country)
                                        for v in chapter['condition_variants']))
                    archive = 'ac_sq.' + str(row['base'] + 10000 + chapter['id'])
                    snapshot = copy.deepcopy((world.countries, world.globals, world.controllers, world.faction,
                                              world.wars, world.queue, world.news))
                    self.assertTrue(world.deliver(archive, row['tag']))
                    self.assertEqual([expected], world.descriptions(archive, row['tag']))
                    world.choose(archive, 0, row['tag'])
                    self.assertEqual(snapshot, (world.countries, world.globals, world.controllers, world.faction,
                                               world.wars, world.queue, world.news))

    def test_training_return_separates_peace_war_and_ground_without_rewriting_archive(self):
        row = BY_TAG['BLK']; chapter = row['chapters'][7]
        for war in (False, True):
            for capitulated in (False, True):
                for air in (False, True):
                    for callback in (False, True):
                        with self.subTest(war=war, capitulated=capitulated, air=air, callback=callback):
                            world = World()
                            ident, country = world.open_scene(row, chapter, war=war,
                                                              capitulated=capitulated, air=air, callback=callback)
                            context = 'base' if capitulated or not air else 'war' if war else 'training_return'
                            expected = ident + '.d_' + context + ('_callback' if callback else '')
                            self.assertEqual([expected], world.descriptions(ident, 'BLK'))
                            country.equipment.update(fighter_equipment=4, transport_plane_equipment=2)
                            physical = copy.deepcopy((country.equipment, country.air_manpower))
                            world.choose(ident, 0, 'BLK')
                            self.assertEqual(50 + chapter['options'][0]['cohesion'], country.variables['ac_sq_cohesion'])
                            self.assertEqual(50 + chapter['options'][0]['credibility'], country.variables['ac_sq_credibility'])
                            self.assertEqual(physical, (country.equipment, country.air_manpower))
                            country.capitulated = not capitulated; country.air_manpower = int(not air)
                            world.wars.clear() if war else world.wars.add(frozenset(('BLK', 'ZZZ')))
                            prior = story_flag(row, chapter['callback']['flag'])
                            country.flags.pop(prior, None) if callback else country.flags.update({prior: None})
                            archive = 'ac_sq.' + str(row['base'] + 10000 + chapter['id'])
                            saved = copy.deepcopy((world.countries, world.globals, world.wars, world.queue))
                            self.assertTrue(world.deliver(archive, 'BLK'))
                            self.assertEqual([expected], world.descriptions(archive, 'BLK'))
                            world.choose(archive, 0, 'BLK')
                            self.assertEqual(saved, (world.countries, world.globals, world.wars, world.queue))

    def test_flight_contexts_require_actual_air_service_and_do_not_consume_aircraft(self):
        flights = [(row, chapter) for row in STORIES for chapter in row['chapters']
                   if chapter.get('war_text') or any(v['id']=='service_flight' for v in chapter.get('condition_variants', []))]
        self.assertTrue(all(any(r['tag']==tag for r, _ in flights) for tag in BY_TAG))
        for row, chapter in flights:
            with self.subTest(tag=row['tag'], chapter=chapter['id']):
                world = World(); world.globals.clear()
                ident, country = world.open_scene(row, chapter, war=True, air=False)
                self.assertEqual([ident + '.d_base'], world.descriptions(ident, row['tag']))
                country.equipment.update(fighter_equipment=7, cas_equipment=3, transport_plane_equipment=2)
                inventory = copy.deepcopy((country.equipment, country.air_manpower, world.globals, world.wars))
                # Capability restored while the reader decides does not replace
                # the ground scene; neither choice manufactures physical tails.
                country.air_manpower = 2
                self.assertEqual([ident + '.d_base'], world.descriptions(ident, row['tag']))
                country.air_manpower = inventory[1]
                world.choose(ident, 0, row['tag'])
                self.assertEqual(inventory, (country.equipment, country.air_manpower, world.globals, world.wars))

    def test_expiry_advances_without_reward_and_stale_event_cannot_clear_next(self):
        for row in STORIES:
            world = World().init(); tag = row['tag']; country = world.countries[tag]
            world.run('ac_sq_' + tag.lower() + '_dispatch', tag)
            stale = core_id(row, 1)
            world.advance(30)
            world.run('ac_sq_tick', tag)
            self.assertEqual(1, country.variables['ac_sq_chapter'])
            self.assertTrue(world.flag(country, story_flag(row, 'missed_1')))
            self.assertEqual((50, 50), (country.variables['ac_sq_cohesion'], country.variables['ac_sq_credibility']))
            self.assertFalse(world.deliver(stale, tag))
            second = row['chapters'][1]
            world.today = max(world.today, ucw.day(second['earliest']))
            world.run('ac_sq_tick', tag)
            saved = copy.deepcopy(country)
            for option in range(len(row['chapters'][0]['options']) + 1): world.choose(stale, option, tag)
            self.assertEqual(saved, country)
            self.assertTrue(world.deliver(core_id(row, 2), tag))
            world.choose(core_id(row, 2), 0, tag)
            self.assertEqual(2, country.variables['ac_sq_chapter'])

    def test_act_boundary_invalidates_an_open_scene_without_its_reward(self):
        for row in STORIES:
            for act in range(3):
                chapter = row['chapters'][act * 5 + 4]
                world = World(); ident, country = world.open_scene(row, chapter)
                world.today = ucw.day(row['acts'][act][1]) + 1
                saved = copy.deepcopy(country)
                world.choose(ident, 0, row['tag'])
                self.assertEqual(saved, country)
                world.run('ac_sq_tick', row['tag'])
                self.assertTrue(world.flag(country, story_flag(row, 'missed_' + str(chapter['id']))))
                self.assertEqual(50, country.variables['ac_sq_cohesion'])
                self.assertFalse(world.flag(country, story_flag(row, chapter['options'][0]['flag'])))

    def test_actual_choice_relationship_bounds(self):
        for row in STORIES:
            chapter = row['chapters'][0]
            for initial in (0, 100):
                for index, option in enumerate(chapter['options']):
                    world = World(); ident, country = world.open_scene(row, chapter)
                    country.variables.update(ac_sq_cohesion=initial, ac_sq_credibility=initial)
                    world.choose(ident, index, row['tag'])
                    self.assertEqual(max(0, min(100, initial + option['cohesion'])), country.variables['ac_sq_cohesion'])
                    self.assertEqual(max(0, min(100, initial + option['credibility'])), country.variables['ac_sq_credibility'])

    def test_disabled_and_foreign_cloned_or_annexed_hosts_cannot_advance(self):
        for row in STORIES:
            tag = row['tag']; chapter = row['chapters'][0]
            world = World(enabled=False); before = copy.deepcopy(world.countries)
            world.action('on_startup'); world.action('on_weekly'); world.run('ac_sq_tick', tag)
            self.assertEqual(before, world.countries); self.assertFalse(world.queue)
            world = World(); ident, country = world.open_scene(row, chapter)
            clone = copy.deepcopy(country); clone.tag = 'D01'; world.countries['D01'] = clone
            before = copy.deepcopy(clone)
            world.run('ac_sq_tick', 'D01'); world.choose(ident, 0, 'D01')
            self.assertFalse(world.deliver(ident, 'D01')); self.assertEqual(before, clone)
            wrong_original = copy.deepcopy(country); wrong_original.original_tag = 'D01'
            world.countries[tag] = wrong_original; before = copy.deepcopy(wrong_original)
            world.run('ac_sq_tick', tag); world.choose(ident, 0, tag)
            self.assertEqual(before, wrong_original)
            world.countries[tag] = country
            for invalid in ('disabled', 'annexed'):
                world.enabled = invalid != 'disabled'; country.exists = invalid != 'annexed'
                before = copy.deepcopy(country); world.run('ac_sq_tick', tag)
                world.choose(ident, 0, tag); world.choose(ident, len(chapter['options']), tag)
                self.assertFalse(world.deliver(ident, tag)); self.assertEqual(before, country)

    def test_late_initialization_act_boundaries_and_after_2005_never_grants_history(self):
        for row in STORIES:
            for end in [act[1] for act in row['acts'] if act[1]]:
                for delta in (-1, 0, 1):
                    world = World(); world.today = ucw.day(end) + delta; tag = row['tag']
                    world.run('ac_sq_tick', tag); country = world.countries[tag]
                    expired = max(1, sum(5 for _, last in row['acts'] if last and world.today > ucw.day(last)))
                    self.assertEqual(expired, country.variables['ac_sq_chapter'])
                    self.assertEqual((50, 50), (country.variables['ac_sq_cohesion'], country.variables['ac_sq_credibility']))
                    self.assertFalse(world.flag(country, 'ac_sq_has_read')); self.assertFalse(country.ideas)
                    for number in range(1, expired + 1):
                        self.assertTrue(world.flag(country, story_flag(row, 'missed_' + str(number))))
                        self.assertFalse(world.deliver(core_id(row, number), tag))
            world = World('2006.1.1'); world.action('on_startup')
            country = world.countries[row['tag']]
            self.assertTrue(world.flag(country, 'ac_sq_late_archive'))
            self.assertTrue(world.flag(country, 'ac_sq_closed'))
            self.assertFalse(world.queue); self.assertFalse(country.ideas)
            self.assertEqual(0, country.variables['ac_sq_chapter'])

    def test_opening_is_not_replayed_after_its_january_window(self):
        for row in STORIES:
            tag = row['tag']
            for date, expected in (('1991.1.31', 0), ('1991.2.1', 1), ('1992.1.1', 1)):
                world = World(date); world.action('on_startup'); country = world.countries[tag]
                self.assertEqual(expected, country.variables['ac_sq_chapter'])
                self.assertEqual((50, 50), (country.variables['ac_sq_cohesion'], country.variables['ac_sq_credibility']))
                self.assertEqual(bool(expected), world.flag(country, story_flag(row, 'missed_1')))
                if expected:
                    self.assertFalse(world.deliver(core_id(row, 1), tag))

    def test_country_weekly_callback_does_not_nest_another_world_iteration(self):
        world = World().init(); original = world.execute; calls = []
        def observed(nodes, country):
            calls.extend(country.tag for key, _, _ in nodes if key == 'ac_sq_tick')
            return original(nodes, country)
        world.execute = observed
        world.action('on_weekly')
        self.assertCountEqual(list(BY_TAG), calls)

    def test_startup_and_offline_deepcopy_reload_preserve_reservations_and_choices(self):
        world = World(); world.action('on_startup')
        saved = copy.deepcopy(world)
        world.action('on_startup'); world.action('on_weekly')
        self.assertEqual(saved.countries, world.countries); self.assertEqual(saved.queue, world.queue)
        reloaded = copy.deepcopy(world)
        for candidate in (world, reloaded):
            candidate.advance(1); candidate.drain(); candidate.action('on_startup')
        self.assertEqual(world.countries, reloaded.countries)
        self.assertEqual(world.queue, reloaded.queue)
        saved = copy.deepcopy(world.countries)
        world.action('on_startup'); self.assertEqual(saved, world.countries)

    def test_pause_manual_read_and_manual_ending(self):
        for row in STORIES:
            world = World().init(); tag = row['tag']; country = world.countries[tag]; prefix = 'ac_sq_' + tag.lower()
            world.take(prefix + '_pause', tag); world.run('ac_sq_tick', tag)
            self.assertFalse(world.queue)
            self.assertTrue(world.available(prefix + '_read', tag)); world.take(prefix + '_read', tag)
            self.assertTrue(world.deliver(core_id(row, 1), tag)); world.choose(core_id(row, 1), 0, tag)
            self.assertFalse(world.available(prefix + '_read', tag))
            world.advance(31); country.variables['ac_sq_chapter'] = 20
            world.run('ac_sq_tick', tag)
            self.assertFalse(world.flag(country, 'ac_sq_ending_pending'))
            world.take(prefix + '_read', tag)
            self.assertTrue(world.flag(country, 'ac_sq_ending_pending'))
            world.take(prefix + '_resume', tag)
            self.assertFalse(world.flag(country, 'ac_sq_paused'))

    def test_every_story_has_all_three_reachable_endings_and_mixed_trusted_paths(self):
        for row in STORIES:
            states = {(50, 50): ()}
            for chapter in row['chapters']:
                nxt = {}
                for (cohesion, credibility), path in states.items():
                    for index, option in enumerate(chapter['options']):
                        state = (max(0, min(100, cohesion + option['cohesion'])), max(0, min(100, credibility + option['credibility'])))
                        nxt.setdefault(state, path + (index,))
                states = nxt
            examples = {}
            for state, path in states.items():
                kind = ending_kind(*state)
                if kind != 'trusted' or len(set(path)) > 1:
                    examples.setdefault(kind, path)
            self.assertEqual({'trusted', 'compromised', 'fractured'}, set(examples), row['tag'])
            for kind, path in examples.items():
                # Run the actual compiled options for the BFS witness, then its
                # actual finish dispatcher. The BFS is not a second runtime.
                world = World().init(); tag = row['tag']; country = world.countries[tag]
                for chapter, choice in zip(row['chapters'], path):
                    world.today = max(world.today, ucw.day(chapter['earliest']))
                    country.flags.pop('ac_sq_cooldown', None)
                    world.run('ac_sq_' + tag.lower() + '_dispatch', tag)
                    ident = core_id(row, chapter['id']); self.assertTrue(world.deliver(ident, tag))
                    world.choose(ident, choice, tag)
                world.today = ucw.day('2007.3.1')
                world.run('ac_sq_' + tag.lower() + '_finish', tag)
                index = next(i for i, item in enumerate(row['endings']) if item['id'] == kind)
                ident = core_id(row, 90 + index)
                self.assertTrue(world.deliver(ident, tag)); world.choose(ident, 0, tag)
                self.assertTrue(world.flag(country, story_flag(row, 'ending_' + kind)))
                self.assertTrue(world.flag(country, 'ac_sq_closed'))
                self.assertEqual(kind == 'trusted', 'ac_sq_professional_debrief' in country.ideas)
                saved = copy.deepcopy(country)
                world.choose(ident, 0, tag); world.run('ac_sq_' + tag.lower() + '_finish', tag)
                self.assertEqual(saved, country)
                if kind == 'trusted':
                    self.assertEqual(world.today + 365, country.ideas['ac_sq_professional_debrief'])
                    world.advance(365); self.assertNotIn('ac_sq_professional_debrief', country.ideas)

    def test_existing_final_act_can_finish_after_2005_but_unread_archive_has_no_bonus(self):
        for row in STORIES:
            tag = row['tag']; world = World().init(); country = world.countries[tag]
            country.variables.update(ac_sq_chapter=19, ac_sq_cohesion=70, ac_sq_credibility=70)
            world.today = ucw.day('2008.4.1'); world.run('ac_sq_tick', tag)
            self.assertTrue(world.deliver(core_id(row, 20), tag)); world.choose(core_id(row, 20), 0, tag)
            world.run('ac_sq_tick', tag)
            self.assertTrue(world.flag(country, 'ac_sq_ending_pending'))
            world = World().init(); country = world.countries[tag]
            country.variables.update(ac_sq_chapter=20, ac_sq_cohesion=70, ac_sq_credibility=70)
            world.today = ucw.day('2008.4.1'); world.run('ac_sq_tick', tag)
            trusted = next(i for i, ending in enumerate(row['endings']) if ending['id'] == 'trusted')
            ident = core_id(row, 90 + trusted)
            self.assertTrue(world.deliver(ident, tag)); world.choose(ident, 0, tag)
            self.assertNotIn('ac_sq_professional_debrief', country.ideas)

    def test_ending_reservation_expiry_and_stale_kind_cannot_close_a_new_assessment(self):
        for row in STORIES:
            world = World().init(); tag = row['tag']; country = world.countries[tag]
            country.variables.update(ac_sq_chapter=20, ac_sq_cohesion=50, ac_sq_credibility=50)
            world.run('ac_sq_tick', tag)
            old_kind = next(i for i, ending in enumerate(row['endings']) if ending['id'] == 'compromised')
            stale = core_id(row, 90 + old_kind)
            self.assertTrue(world.deliver(stale, tag))
            world.advance(30)
            self.assertFalse(world.deliver(stale, tag))
            country.variables.update(ac_sq_cohesion=70, ac_sq_credibility=70)
            world.run('ac_sq_tick', tag)
            saved = copy.deepcopy(country)
            world.choose(stale, 0, tag)
            self.assertEqual(saved, country)
            trusted = next(i for i, ending in enumerate(row['endings']) if ending['id'] == 'trusted')
            current = core_id(row, 90 + trusted)
            self.assertTrue(world.deliver(current, tag)); world.choose(current, 0, tag)
            self.assertTrue(world.flag(country, story_flag(row, 'ending_trusted')))
            self.assertFalse(country.ideas)  # fabricated unread assessment earns no training reward

    def test_default_weekly_calendar_reads_the_full_campaign_without_position_shortcuts(self):
        # Deterministic first-eligible choices test the shipped scheduler only.
        # This is not the native AI, actual country survival, wars or balance.
        world = World(); world.action('on_startup')
        while world.today < ucw.day('2006.2.1'):
            world.advance(7); world.drain(); world.action('on_weekly')
        for row in STORIES:
            country = world.countries[row['tag']]
            self.assertEqual(20, country.variables['ac_sq_chapter'], row['tag'])
            self.assertTrue(world.flag(country, 'ac_sq_closed'), row['tag'])
            for chapter in row['chapters']:
                self.assertTrue(world.flag(country, story_flag(row, 'chapter_' + str(chapter['id']))), (row['tag'], chapter['id']))
                self.assertFalse(world.flag(country, story_flag(row, 'missed_' + str(chapter['id']))))
            core_deliveries = [ident for tag, ident, _ in world.deliveries if tag == row['tag'] and ident in {core_id(row, n) for n in range(1, 21)}]
            self.assertEqual(20, len(core_deliveries))
            self.assertEqual(20, len(set(core_deliveries)))

    def test_delayed_delivery_and_annexation_restore_do_not_freeze_progression(self):
        for row in STORIES:
            world = World().init(); tag = row['tag']; country = world.countries[tag]
            world.run('ac_sq_' + tag.lower() + '_dispatch', tag)
            pending = core_id(row, 1)
            country.exists = False; world.advance(31); world.drain()
            self.assertFalse(world.deliveries)
            country.exists = True; world.run('ac_sq_tick', tag)
            self.assertEqual(1, country.variables['ac_sq_chapter'])
            self.assertFalse(world.flag(country, 'ac_sq_has_read'))
            world.today = max(world.today, ucw.day(row['chapters'][1]['earliest']))
            world.run('ac_sq_tick', tag)
            self.assertFalse(world.deliver(pending, tag))
            current = core_id(row, 2)
            self.assertTrue(world.deliver(current, tag))
            before = copy.deepcopy(country)
            # Repeated delivery of the same still-open scene cannot rewrite its
            # stored context or apply its option while the reader is deciding.
            self.assertTrue(world.deliver(current, tag)); self.assertEqual(before, country)
            world.choose(current, 0, tag)
            self.assertEqual(2, country.variables['ac_sq_chapter'])

    def test_cast_and_archive_decisions_are_owner_bound_and_pure(self):
        world = World().init()
        for row in STORIES:
            tag = row['tag']; prefix = 'ac_sq_' + tag.lower()
            self.assertFalse(world.available(prefix + '_archive_1', tag))
            for index, person in enumerate(row['cast']):
                ident = core_id(row, 50 + index); decision = prefix + '_cast_' + person['id']
                self.assertTrue(world.available(decision, tag))
                snapshot = copy.deepcopy((world.countries, world.globals))
                world.take(decision, tag); self.assertTrue(world.deliver(ident, tag)); world.choose(ident, 0, tag)
                self.assertEqual(snapshot, (world.countries, world.globals))
                self.assertFalse(world.available(decision, 'ZZZ')); self.assertFalse(world.deliver(ident, 'ZZZ'))

    def test_localization_owned_effects_and_event_ids_are_complete(self):
        world = World()
        self.assertEqual(282, len(world.events))  # 120core +120archive +24cast +18endings
        loc_path = MOD / 'localisation/english/ac_squadrons_l_english.yml'
        self.assertTrue(loc_path.read_bytes().startswith(b'\xef\xbb\xbf'))
        text = loc_path.read_text(encoding='utf-8-sig')
        keys = re.findall(r'^\s*([\w.]+):0 ', text, re.M)
        self.assertEqual(len(keys), len(set(keys)))
        for _, event in world.events.values():
            for key, _, value in event:
                if key in ('title', 'desc') and isinstance(value, str): self.assertIn(value, keys)
                if key == 'desc' and isinstance(value, list): self.assertIn(mapping(value)['text'], keys)
            for option in (node for key, _, node in event if key == 'option'):
                self.assertIn(mapping(option)['name'], keys)
                for kind, body in walk(option):
                    if kind == 'set_variable' or kind == 'add_to_variable':
                        self.assertTrue(body[0][0].startswith('ac_sq_'))
        effects = (MOD / 'common/scripted_effects/ac_squadrons.txt').read_text()
        self.assertNotRegex(effects, r'(?:set|clr)_global_flag|declare_war_on|transfer_state|add_to_faction|add_equipment|add_building|load_oob|recruit_character')
        contracts = json.loads((ROOT / 'tools/squadrons/engine_contracts.json').read_text())
        idea_groups = mapping(load('common/ideas/ac_squadrons.txt'))['ideas']
        debrief = mapping(mapping(idea_groups)['country'])['ac_sq_professional_debrief']
        self.assertEqual('no', mapping(debrief)['allowed_civil_war'])
        certified = contracts['country_idea_modifiers']
        self.assertTrue(contracts['sources'])
        seen = []
        for _, country_ideas in walk(load('common/ideas/ac_squadrons.txt')):
            for key, _, value in country_ideas:
                if key == 'modifier':
                    for modifier, _, amount in value:
                        seen.append(modifier)
                        self.assertIn(modifier, certified, 'Uncertified engine modifier in story reward')
                        self.assertEqual('0.02', amount)
        self.assertEqual(1, len(seen))
        self.assertNotIn('air_experience =', effects)


if __name__ == '__main__':
    unittest.main(verbosity=2)
