"""Compile original squadron scenes and owned once-only progression contracts."""
import argparse
import json
from pathlib import Path

from schema import HERE, MOD, campaigns

OUT = {}
LOC = {}


def block(key, text):
    return key + ' = {\n' + '\n'.join('\t' + line for line in text.splitlines()) + '\n}\n'


def loc(key, text):
    if key in LOC:
        raise ValueError('Duplicate narrative localization: ' + key)
    LOC[key] = text
    return key


def identity(tag):
    return 'tag = ' + tag + ' original_tag = ' + tag + ' country_exists = ' + tag


def owned_if(condition, effect):
    return block('if', block('limit', condition) + effect)


def chapter_key(row, chapter):
    return 'ac_sq.' + str(row['base'] + chapter['id'])


def flag(row, short):
    return 'ac_sq_' + row['tag'].lower() + '_' + short


def scene_slot(chapter):
    for slot, indices in json.loads((HERE / 'art_plan.json').read_text())['chapters_by_slot'].items():
        if chapter in indices:
            return slot
    raise ValueError('No storyboard slot for chapter ' + str(chapter))


def contexts(chapter):
    result = []
    if chapter.get('capitulated_text'):
        result.append(('cap', 'has_capitulated = yes', chapter['capitulated_text']))
    for variant in chapter.get('condition_variants', []):
        condition = variant['trigger']
        if result:
            condition += '\n' + block('NOT', block('OR', ''.join(block('AND', rule) for _, rule, _ in result)))
        result.append((variant['id'], condition, variant['text']))
    if chapter.get('war_text'):
        condition = 'has_war = yes has_capitulated = no ac_sq_air_capable = yes'
        if result:
            condition += '\n' + block('NOT', block('OR', ''.join(block('AND', rule) for _, rule, _ in result)))
        result.append(('war', condition, chapter['war_text']))
    fallback = block('NOT', block('OR', ''.join(block('AND', condition) for _, condition, _ in result))) if result else 'always = yes'
    result.append(('base', fallback, chapter['text']))
    return result


def pending_valid(row, chapter):
    """One country, one chapter reservation, and its still-current act."""
    number = chapter['id']
    condition = (identity(row['tag']) + ' ac_sq_active = yes has_country_flag = ac_sq_dispatch_pending '
                 'check_variable = { ac_sq_chapter = ' + str(number - 1) + ' } '
                 'check_variable = { ac_sq_pending_chapter = ' + str(number) + ' } '
                 'NOT = { date < ' + chapter['earliest'] + ' } '
                 'NOT = { has_country_flag = ' + flag(row, 'chapter_' + str(number)) + ' }')
    end = row['acts'][(number - 1) // 5][1]
    if end:
        condition += ' NOT = { date > ' + end + ' }'
    return condition


def repair_pending(row):
    """An unanswered reservation expires once; its event ID is never reissued."""
    body = ''
    for chapter in row['chapters']:
        number = chapter['id']
        expired = 'NOT = { has_country_flag = ac_sq_dispatch_pending }'
        end = row['acts'][(number - 1) // 5][1]
        if end:
            expired += ' date > ' + end
        condition = (identity(row['tag']) + ' ac_sq_active = yes '
                     'check_variable = { ac_sq_pending_chapter = ' + str(number) + ' } '
                     'check_variable = { ac_sq_chapter = ' + str(number - 1) + ' } ' + block('OR', expired))
        body += owned_if(condition,
                         'set_country_flag = ' + flag(row, 'missed_' + str(number)) + '\n'
                         'set_variable = { ac_sq_chapter = ' + str(number) + ' }\n'
                         'clr_country_flag = ac_sq_dispatch_pending\n'
                         'set_variable = { ac_sq_pending_chapter = 0 }\n')
    return block('ac_sq_' + row['tag'].lower() + '_repair_pending', body)


def progression(row):
    tag = row['tag']; body = ''
    for chapter in row['chapters']:
        number = chapter['id']; start = chapter['earliest']
        end = row['acts'][(number - 1) // 5][1]
        limit = (identity(tag) + ' ac_sq_active = yes NOT = { has_country_flag = ac_sq_dispatch_pending } '
                 'check_variable = { ac_sq_chapter = ' + str(number - 1) + ' }')
        if end:
            body += owned_if(limit + ' date > ' + end,
                             'set_variable = { ac_sq_chapter = ' + str(number) + ' }\n'
                             'set_country_flag = ' + flag(row, 'missed_' + str(number)) + '\n')
        condition = limit + ' NOT = { has_country_flag = ac_sq_cooldown } NOT = { date < ' + start + ' }'
        if end:
            condition += ' NOT = { date > ' + end + ' }'
        effect = ('set_variable = { ac_sq_pending_chapter = ' + str(number) + ' }\n'
                  'set_country_flag = { flag = ac_sq_dispatch_pending days = 30 }\n'
                  'country_event = { id = ' + chapter_key(row, chapter) + ' days = 1 }\n')
        body += owned_if(condition, effect)
    return block('ac_sq_' + tag.lower() + '_dispatch', body)


def choices(row, chapter):
    number = chapter['id']; output = ''
    for index, choice in enumerate(chapter['options']):
        ident = chapter_key(row, chapter) + '.' + chr(97 + index)
        loc(ident, choice['label'])
        loc(ident + '.reply', choice['reply'])
        valid = pending_valid(row, chapter) + ' has_country_flag = ' + flag(row, 'delivered_' + str(number))
        effects = ('set_country_flag = ' + flag(row, 'chapter_' + str(number)) + '\n'
                   'set_country_flag = ' + flag(row, choice['flag']) + '\n'
                   'set_country_flag = ac_sq_has_read\n'
                   'set_variable = { ac_sq_chapter = ' + str(number) + ' }\n'
                   'add_to_variable = { ac_sq_cohesion = ' + str(choice.get('cohesion', 0)) + ' }\n'
                   'add_to_variable = { ac_sq_credibility = ' + str(choice.get('credibility', 0)) + ' }\n'
                   'clamp_variable = { var = ac_sq_cohesion min = 0 max = 100 }\n'
                   'clamp_variable = { var = ac_sq_credibility min = 0 max = 100 }\n')
        effects += ('clr_country_flag = ac_sq_dispatch_pending\nset_variable = { ac_sq_pending_chapter = 0 }\n'
                    'set_country_flag = { flag = ac_sq_cooldown days = 30 }\n')
        # Narrative responses are part of the actual option tooltip; stale or
        # console-replayed events cannot repeat a relationship change or reward.
        output += block('option', 'name = ' + ident + '\nai_chance = { factor = 50 }\n' + block('trigger', valid) +
                        'custom_effect_tooltip = ' + ident + '.reply\n' + owned_if(valid, effects))
    output += block('option', 'name = ac_sq_expired_close\n' + block('trigger', block('NOT', valid)))
    return output


def events(row):
    tag = row['tag']; result = []
    for chapter in row['chapters']:
        ident = chapter_key(row, chapter)
        loc(ident + '.t', chapter['title'])
        text = chapter['text']
        callback = chapter.get('callback')
        desc = ''
        archive_desc = ''
        context_rows = contexts(chapter)
        for context, condition, prose in context_rows:
            context_flag = flag(row, 'view_' + str(chapter['id']) + '_' + context)
            archived_condition = 'has_country_flag = ' + context_flag
            for with_callback in ((True, False) if callback else (False,)):
                key = ident + '.d_' + context + ('_callback' if with_callback else '')
                loc(key, prose + ('\n\n' + callback['text'] if with_callback else ''))
                suffix = ''
                if callback:
                    test = 'has_country_flag = ' + flag(row, 'callback_' + str(chapter['id']))
                    suffix = test if with_callback else block('NOT', test)
                desc += block('desc', 'text = ' + key + '\n' + block('trigger', archived_condition + '\n' + suffix))
                archive_desc += block('desc', 'text = ' + key + '\n' + block('trigger', archived_condition + '\n' + suffix))
        snapshot = 'set_country_flag = ' + flag(row, 'delivered_' + str(chapter['id'])) + '\n'
        for context, condition, _ in context_rows:
            snapshot += owned_if(condition, 'set_country_flag = ' + flag(row, 'view_' + str(chapter['id']) + '_' + context) + '\n')
        if callback:
            snapshot += owned_if('has_country_flag = ' + flag(row, callback['flag']),
                                 'set_country_flag = ' + flag(row, 'callback_' + str(chapter['id'])) + '\n')
        immediate = owned_if(pending_valid(row, chapter) + ' NOT = { has_country_flag = ' + flag(row, 'delivered_' + str(chapter['id'])) + ' }', snapshot)
        result.append(block('country_event', 'id = ' + ident + '\ntitle = ' + ident + '.t\n' + desc +
                            'picture = GFX_ac_sq_' + tag.lower() + '_scene_' + scene_slot(chapter['id']) + '\n'
                            'is_triggered_only = yes\n' + block('trigger', pending_valid(row, chapter)) +
                            block('immediate', immediate) + choices(row, chapter)))
        archive = 'ac_sq.' + str(row['base'] + 10000 + chapter['id'])
        result.append(block('country_event', 'id = ' + archive + '\ntitle = ' + ident + '.t\n' +
                            archive_desc +
                            'picture = GFX_ac_sq_' + tag.lower() + '_scene_' + scene_slot(chapter['id']) + '\n'
                            'is_triggered_only = yes\n' + block('trigger', identity(tag) + ' has_country_flag = ' + flag(row, 'chapter_' + str(chapter['id']))) +
                            block('option', 'name = ac_sq_archive_close\n')))
    for index, person in enumerate(row['cast']):
        ident = 'ac_sq.' + str(row['base'] + 50 + index)
        loc(ident + '.t', person['name'] + ' | ' + person['role'])
        loc(ident + '.d', person['bio'])
        result.append(block('country_event', 'id = ' + ident + '\ntitle = ' + ident + '.t\n'
                            'desc = ' + ident + '.d\npicture = GFX_ac_sq_cast_' + person['id'] + '\n'
                            'is_triggered_only = yes\n' + block('trigger', identity(tag) + ' has_country_flag = ac_sq_initialized') +
                            block('option', 'name = ac_sq_archive_close\n')))
    for index, ending in enumerate(row['endings']):
        ident = 'ac_sq.' + str(row['base'] + 90 + index)
        loc(ident + '.t', ending['title']); loc(ident + '.d', ending['text'])
        valid = (identity(tag) + ' ac_sq_active = yes check_variable = { ac_sq_chapter = 20 } has_country_flag = ac_sq_ending_pending '
                 'check_variable = { ac_sq_ending_kind = ' + str(index) + ' }')
        effect = ('set_country_flag = ac_sq_closed\nclr_country_flag = ac_sq_ending_pending\n'
                  'set_country_flag = ' + flag(row, 'ending_' + ending['id']) + '\n')
        # Personal conclusions are not a second war/peace owner. Only a bounded
        # future professional-training benefit can follow a trusted assessment.
        if ending['id'] == 'trusted':
            effect += owned_if('has_country_flag = ac_sq_has_read',
                               'add_timed_idea = { idea = ac_sq_professional_debrief days = 365 }\n')
        result.append(block('country_event', 'id = ' + ident + '\ntitle = ' + ident + '.t\ndesc = ' + ident + '.d\n'
                            'picture = GFX_ac_sq_' + tag.lower() + '_scene_8\nis_triggered_only = yes\n' + block('trigger', valid) +
                            block('option', 'name = ac_sq_end_close\n' + owned_if(valid, effect))))
    return '\n'.join(result)


def build():
    OUT.clear(); LOC.clear(); stories = campaigns()
    loc('ac_sq_archive_close', 'Return to the briefing.')
    loc('ac_sq_end_close', 'Keep their account.')
    loc('ac_sq_expired_close', 'File this dispatch without replaying its choices.')
    loc('ac_sq_pause', 'Pause squadron dispatches')
    loc('ac_sq_pause_desc', 'Pause automatic scenes. Expired historical chapters are archived without applying their choices.')
    loc('ac_sq_resume', 'Resume squadron dispatches')
    loc('ac_sq_resume_desc', 'Continue eligible scenes from the current calendar and personal history.')
    loc('ac_sq_read_next', 'Read the next eligible dispatch')
    loc('ac_sq_read_next_desc', 'Open an eligible scene. Earlier archived choices do not apply retroactive preparation or relationship rewards.')
    loc('ac_sq_professional_debrief', 'An Honest Debrief')
    loc('ac_sq_professional_debrief_desc', 'A squadron has made the hard lessons of its service available to the people following it. Its contribution to training is modest, practical and temporary.')
    loc('ac_sq_rule', 'Squadron stories'); loc('ac_sq_rule_on', 'Enabled'); loc('ac_sq_rule_off', 'Disabled')
    loc('AC_SQUADRON_RULES', 'Project Ulysses | Squadron stories')
    loc('ac_sq_rule_on_desc', 'Original recurring-character stories accompany eligible national campaigns.')
    loc('ac_sq_rule_off_desc', 'Do not initialize or advance new squadron stories.')
    hosts = 'OR = { ' + ' '.join('AND = { ' + identity(r['tag']) + ' }' for r in stories) + ' }'
    triggers = block('ac_sq_enabled', 'has_game_rule = { rule = ac_sq_stories option = enabled }\n')
    triggers += block('ac_sq_host', hosts)
    triggers += block('ac_sq_air_capable', 'check_variable = { deployed_airforce_manpower_k > 0 }')
    triggers += block('ac_sq_active', 'ac_sq_enabled = yes ac_sq_host = yes has_country_flag = ac_sq_initialized NOT = { has_country_flag = ac_sq_closed }')
    opening_expiry = ''.join(owned_if(identity(row['tag']),
                           'set_variable = { ac_sq_chapter = 1 }\nset_country_flag = ' + flag(row, 'missed_1') + '\n')
                           for row in stories)
    effects = block('ac_sq_initialize', owned_if('ac_sq_enabled = yes ac_sq_host = yes NOT = { has_country_flag = ac_sq_initialized }',
                    'set_country_flag = ac_sq_initialized\nset_variable = { ac_sq_chapter = 0 }\n'
                    'set_variable = { ac_sq_pending_chapter = 0 }\nset_variable = { ac_sq_ending_kind = -1 }\n'
                    'set_variable = { ac_sq_cohesion = 50 }\nset_variable = { ac_sq_credibility = 50 }\n' +
                    owned_if('date > 1991.1.31 NOT = { date > 2005.12.31 }', opening_expiry) +
                    owned_if('date > 2005.12.31', 'set_country_flag = ac_sq_closed\nset_country_flag = ac_sq_late_archive\n')))
    tick = 'ac_sq_initialize = yes\n'
    categories = ''; decisions = ''; event_text = 'add_namespace = ac_sq\n'
    for row in stories:
        tag = row['tag']; prefix = 'ac_sq_' + tag.lower()
        effects += repair_pending(row) + progression(row)
        # Expired pending windows cannot strand a country indefinitely. Resolve
        # only the dispatch reservation; actual choice effects stay guarded.
        tick += owned_if(identity(tag) + ' ac_sq_active = yes', prefix + '_repair_pending = yes\n')
        tick += owned_if(identity(tag) + ' ac_sq_active = yes NOT = { has_country_flag = ac_sq_paused }', prefix + '_dispatch = yes\n')
        ending = prefix + '_finish'
        ids = {e['id']: row['base'] + 90 + index for index, e in enumerate(row['endings'])}
        finish = 'set_country_flag = { flag = ac_sq_ending_pending days = 30 }\n'
        finish += (block('if', block('limit', 'NOT = { check_variable = { ac_sq_cohesion < 65 } } NOT = { check_variable = { ac_sq_credibility < 65 } }') +
                   'set_variable = { ac_sq_ending_kind = ' + str(next(i for i,e in enumerate(row['endings']) if e['id']=='trusted')) + ' }\n' +
                   'country_event = { id = ac_sq.' + str(ids['trusted']) + ' days = 1 }\n') +
                   block('else_if', block('limit', 'check_variable = { ac_sq_cohesion < 45 }') +
                         'set_variable = { ac_sq_ending_kind = ' + str(next(i for i,e in enumerate(row['endings']) if e['id']=='fractured')) + ' }\n' +
                         'country_event = { id = ac_sq.' + str(ids['fractured']) + ' days = 1 }\n') +
                   block('else', 'set_variable = { ac_sq_ending_kind = ' + str(next(i for i,e in enumerate(row['endings']) if e['id']=='compromised')) + ' }\n' +
                         'country_event = { id = ac_sq.' + str(ids['compromised']) + ' days = 1 }\n'))
        effects += block(ending, owned_if(identity(tag) + ' ac_sq_active = yes check_variable = { ac_sq_chapter = 20 } NOT = { has_country_flag = ac_sq_ending_pending }', finish))
        tick += owned_if(identity(tag) + ' NOT = { has_country_flag = ac_sq_paused }', ending + ' = yes\n')
        loc(prefix, row['title'])
        loc(prefix + '_desc', 'SQUADRON DISPATCHES\nCompleted chapters: [?ac_sq_chapter]/20\nCrew cohesion: [?ac_sq_cohesion|0]/100\nCredibility: [?ac_sq_credibility|0]/100\n\nPeople remember the promises made here. These dispatches accompany the national campaign.')
        LOC[prefix + '_desc'] = LOC[prefix + '_desc'].replace('Completed chapters:', 'Chapter position (read or archived):')
        categories += block(prefix, 'icon = GFX_ac_sq_category_' + tag.lower() + '\npriority = 45\n' +
                            block('allowed', identity(tag)) + block('visible', 'has_country_flag = ac_sq_initialized') + 'visible_when_empty = yes\n')
        rows = ''
        ready = []
        for chapter in row['chapters']:
            number = chapter['id']; end = row['acts'][(number - 1) // 5][1]
            gate = 'check_variable = { ac_sq_chapter = ' + str(number - 1) + ' } '
            gate += ('OR = { date > ' + end + ' NOT = { date < ' + chapter['earliest'] + ' } }') if end else ('NOT = { date < ' + chapter['earliest'] + ' }')
            ready.append(block('AND', gate))
        # A manually read final act can also request its personal conclusion.
        final_ready = 'check_variable = { ac_sq_chapter = 20 } NOT = { has_country_flag = ac_sq_ending_pending }'
        ready.append(block('AND', final_ready))
        triggers += block(prefix + '_next_ready', 'ac_sq_active = yes NOT = { has_country_flag = ac_sq_dispatch_pending } NOT = { has_country_flag = ac_sq_cooldown }\n' + block('OR', ''.join(ready)))
        rows += block(prefix + '_read', 'icon = ' + prefix + '_read\ncost = 0\n' +
                      block('visible', 'ac_sq_active = yes has_country_flag = ac_sq_paused') +
                      block('available', prefix + '_next_ready = yes') +
                      block('complete_effect', prefix + '_repair_pending = yes\n' + prefix + '_dispatch = yes\n' + prefix + '_finish = yes\n'))
        loc(prefix + '_read', 'Read the next eligible dispatch')
        loc(prefix + '_read_desc', 'File expired scenes without applying their choices, then open the next scene eligible at the current date. A pending dispatch or the thirty-day reading interval must finish first.')
        rows += block(prefix + '_pause', 'icon = ' + prefix + '_pause\n' + block('visible', 'ac_sq_active = yes NOT = { has_country_flag = ac_sq_paused }') +
                      'cost = 0\n' + block('complete_effect', 'set_country_flag = ac_sq_paused\n'))
        loc(prefix + '_pause', 'Pause automatic dispatches'); loc(prefix + '_pause_desc', LOC['ac_sq_pause_desc'])
        rows += block(prefix + '_resume', 'icon = ' + prefix + '_resume\n' + block('visible', 'ac_sq_active = yes has_country_flag = ac_sq_paused') +
                      'cost = 0\n' + block('complete_effect', 'clr_country_flag = ac_sq_paused\n'))
        loc(prefix + '_resume', 'Resume automatic dispatches'); loc(prefix + '_resume_desc', LOC['ac_sq_resume_desc'])
        for chapter in row['chapters']:
            key = prefix + '_archive_' + str(chapter['id'])
            loc(key, str(chapter['id']).zfill(2) + ' | ' + chapter['title']); loc(key + '_desc', 'Read the scene without replaying its choice or rewards.')
            rows += block(key, 'icon = ' + prefix + '_read\ncost = 0\n' +
                          block('visible', 'has_country_flag = ' + flag(row, 'chapter_' + str(chapter['id']))) +
                          block('complete_effect', 'country_event = { id = ac_sq.' + str(row['base'] + 10000 + chapter['id']) + ' days = 0 }\n'))
        for index, person in enumerate(row['cast']):
            key = prefix + '_cast_' + person['id']
            loc(key, person['name']); loc(key + '_desc', person['role'] + '\n\n' + person['bio'])
            rows += block(key, 'icon = ' + prefix + '_cast\ncost = 0\n' + block('visible', 'has_country_flag = ac_sq_initialized') +
                          block('complete_effect', 'country_event = { id = ac_sq.' + str(row['base'] + 50 + index) + ' days = 0 }\n'))
        decisions += block(prefix, rows)
        event_text += events(row)
    effects += block('ac_sq_tick', tick)
    actions = block('on_actions', block('on_startup', block('effect', block('every_country', block('limit', 'ac_sq_host = yes') + 'ac_sq_tick = yes\n'))) +
                    # Generic weekly callbacks already have country scope.
                    block('on_weekly', block('effect', owned_if('ac_sq_host = yes', 'ac_sq_tick = yes\n'))))
    OUT.update({'common/scripted_triggers/ac_squadrons.txt': triggers,
                'common/scripted_effects/ac_squadrons.txt': effects,
                'common/on_actions/ac_squadrons.txt': actions,
                'common/decisions/categories/ac_squadrons.txt': categories,
                'common/decisions/ac_squadrons.txt': decisions,
                'events/ac_squadrons.txt': event_text,
                'common/ideas/ac_squadrons.txt': block('ideas', block('country', block('ac_sq_professional_debrief',
                    'picture = ac_sq_professional_debrief\n' + block('allowed_civil_war', 'always = no') + block('allowed', 'always = no') +
                    block('modifier', 'experience_gain_air_factor = 0.02')))),
                'common/game_rules/ac_squadrons.txt': block('ac_sq_stories',
                    'name = ac_sq_rule\ngroup = AC_SQUADRON_RULES\n' +
                    block('default', 'name = enabled\ntext = ac_sq_rule_on\ndesc = ac_sq_rule_on_desc') +
                    block('option', 'name = disabled\ntext = ac_sq_rule_off\ndesc = ac_sq_rule_off_desc'))})
    localization = 'l_english:\n'
    for key, value in LOC.items():
        localization += ' ' + key + ':0 "' + value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"\n'
    OUT['localisation/english/ac_squadrons_l_english.yml'] = localization
    return OUT


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    for relative, text in build().items():
        data = text.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8')
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n', b'\n') != data:
                raise SystemExit('Squadron generated output differs: ' + relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    print('Six independent original squadron campaigns;120core scenes,24castcards,18conclusions; native acceptance untested.')
