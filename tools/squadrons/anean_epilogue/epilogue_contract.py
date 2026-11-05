"""Authoring contract for the Anean continuations, 2015-2016.

Six-chapter epilogues to two initial stories, *The Open Corridor* (Emmeria)
and *The Last Serviceable Aircraft* (Estovakia). Original supporting fiction,
not official lore. An epilogue is admitted only from the original story's
recorded personal conclusion (``ac_sq_<tag>_ending_<kind>``), and each
conclusion permits only the people it left together: a scene written for a
conclusion may name only that conclusion's permitted cast, and text shared by
every conclusion (callbacks, national context) may name only the cast every
conclusion permits. National context reads only the published Emmeria-
Estovakia War record (``ac_eew_*``). The pinned original stories are read,
never edited.
"""
import json
import re
from datetime import date
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
STORY = HERE.parent
ROOT = HERE.parents[2]
MOD = ROOT / 'mod/2985041246'
if str(STORY / 'southern') not in sys.path:
    sys.path.append(str(STORY / 'southern'))    # appended: this folder's build.py must win
from story_contract import FORBIDDEN, other_cast_names, words  # noqa: E402

NAMESPACE = 'ac_sqa'
# Admitted (shipped) only after its three scene masters are reviewed under
# tools/squadrons/southern_art; until then the script is an offline preview.
ADMITTED = ()
WINDOW = ['2015.4.20', '2016.12.31']
APPROVED = {'EMM': dict(id='open_corridor_after', source='open_corridor', base=100),
            'EVA': dict(id='last_serviceable_after', source='last_serviceable_aircraft', base=200)}
KINDS = ('trusted', 'compromised', 'fractured')
SLOTS = {'1': [1, 2], '2': [3, 4], '3': [5, 6]}
COUNTERPART = {'EMM': 'EVA', 'EVA': 'EMM'}
TRIGGER_KEYS = {'has_capitulated', 'has_war', 'has_war_with', 'ac_sq_air_capable', 'has_global_flag', 'NOT', 'OR', 'AND'}


def day(value):
    return date(*map(int, value.split('.')))


def source_story(tag):
    for row in json.loads((STORY / 'campaigns.json').read_text())['campaigns']:
        if row['tag'] == tag:
            row.update(json.loads((STORY / 'chapters' / (tag + '.json')).read_text(encoding='utf-8-sig')))
            return row
    raise ValueError('No original story for ' + tag)


def published_flags():
    path = MOD / 'common/scripted_effects/ac_anean_war.txt'
    return set(re.findall(r'set_global_flag = (ac_eew_[a-z0-9_]+)', path.read_text(encoding='utf-8-sig')))


def check_trigger(trigger, tag, flags):
    tokens = re.findall(r'[{}=]|[^\s{}=]+', trigger)
    if tokens.count('{') != tokens.count('}'):
        raise ValueError('Unbalanced context trigger: ' + trigger)
    for index, token in enumerate(tokens):
        if token in '{}=' or (index and tokens[index - 1] == '='):
            continue
        if token not in TRIGGER_KEYS:
            raise ValueError('Context may not read ' + token)
        value = tokens[index + 2] if index + 2 < len(tokens) else ''
        if token == 'has_global_flag' and value not in flags:
            raise ValueError('Context reads an unpublished flag: ' + value)
        if token == 'has_war_with' and value != COUNTERPART[tag]:
            raise ValueError('Context may observe only the counterpart war: ' + value)
        if token in ('has_capitulated', 'has_war', 'ac_sq_air_capable') and value not in ('yes', 'no'):
            raise ValueError('Boolean trigger needs yes/no: ' + token)


def screen(text, where, allowed, cast, others):
    for word in FORBIDDEN:
        if re.search(r'\b' + word + r'\b', text):
            raise ValueError(where + ' names an official character or weapon: ' + word)
    for name in others - {p['name'] for p in cast}:
        if name in text:
            raise ValueError(where + ' names another story\'s cast member: ' + name)
    for person in cast:
        first = person['name'].split()[0]
        if person['id'] not in allowed and re.search(r'\b' + first + r'\b', text):
            raise ValueError(where + ' names ' + first + ', whom this conclusion does not permit')
    if any(ord(ch) > 0x7e or (ord(ch) < 0x20 and ch != '\n') for ch in text):
        raise ValueError(where + ' uses a character outside the ASCII briefing contract')


def validate(row, flags=None, others=None):
    tag = row.get('tag')
    contract = APPROVED.get(tag)
    if not contract or row.get('id') != contract['id'] or row.get('base') != contract['base'] or row.get('source_story') != contract['source']:
        raise ValueError('Unapproved epilogue identity')
    if row.get('window') != WINDOW or row.get('chapters_by_slot') != SLOTS:
        raise ValueError('Locked epilogue window or art mapping changed')
    original = source_story(tag)
    if original['id'] != row['source_story']:
        raise ValueError('Epilogue source story changed')
    cast = original['cast']
    ids = [p['id'] for p in cast]
    permits = row['cast_by_ending']
    if list(permits) != list(KINDS) or permits['trusted'] != ids:
        raise ValueError('The trusted conclusion keeps all four; every conclusion needs a permitted cast')
    if any(not permits[k] or any(p not in ids for p in permits[k]) for k in KINDS):
        raise ValueError('A conclusion may permit only its own original cast')
    if len(permits['fractured']) > 2:
        raise ValueError('A fractured conclusion cannot reunite its four')
    shared = set.intersection(*(set(permits[k]) for k in KINDS))
    flags = published_flags() if flags is None else flags
    others = other_cast_names() if others is None else others
    if set(row['scene_subjects']) != set(SLOTS) or any(words(s['subject']) < 30 or not s['title'] for s in row['scene_subjects'].values()):
        raise ValueError('Three concrete scene subjects required')
    chapters = row['chapters']
    if [c['id'] for c in chapters] != list(range(1, 7)) or len({c['title'] for c in chapters}) != 6:
        raise ValueError('Six ordered, distinctly titled chapters required')
    chosen = set()
    last = day(WINDOW[0])
    for chapter in chapters:
        number = chapter['id']
        current = day(chapter['earliest'])
        if current < last or current > day(WINDOW[1]) or (number > 1 and (current - last).days < 35):
            raise ValueError('Epilogue chapter falls outside its ordered window: ' + str(number))
        last = current
        if list(chapter['texts']) != list(KINDS):
            raise ValueError('Each chapter needs one scene per recorded conclusion')
        for kind in KINDS:
            if words(chapter['texts'][kind]) < 80:
                raise ValueError('Every conclusion scene needs a substantive length: ' + tag + str(number) + kind)
            screen(chapter['texts'][kind], tag + str(number) + ' ' + kind, set(permits[kind]), cast, others)
        contexts = chapter['contexts']
        if not contexts or len({c['id'] for c in contexts}) != len(contexts):
            raise ValueError('Each chapter needs distinct national contexts')
        for context in contexts:
            if not re.fullmatch(r'[a-z][a-z0-9_]+', context['id']) or context['id'] == 'default':
                raise ValueError('Context needs a safe identity')
            check_trigger(context['trigger'], tag, flags)
            if words(context['text']) < 40:
                raise ValueError('Context needs a substantive paragraph')
            screen(context['text'], tag + str(number) + ' context', set(), cast, others)
        if words(chapter['default_context']) < 40:
            raise ValueError('Every chapter needs a default national context')
        screen(chapter['default_context'], tag + str(number) + ' default', set(), cast, others)
        callback = chapter.get('callback')
        if callback:
            if callback['flag'] not in chosen or words(callback['text']) < 12:
                raise ValueError('Callback must recall an earlier epilogue choice')
            screen(callback['text'], tag + str(number) + ' callback', shared, cast, others)
        if not 2 <= len(chapter['options']) <= 3:
            raise ValueError('Each chapter requires two or three choices')
        for option in chapter['options']:
            if not re.fullmatch(r'[a-z][a-z0-9_]{2,40}', option['flag']) or option['flag'] in chosen:
                raise ValueError('Choice flags must be safe and distinct: ' + option['flag'])
            chosen.add(option['flag'])
            if words(option['reply']) < 8 or not option['label'].strip():
                raise ValueError('Choice needs an authored response')
            screen(option['label'] + ' ' + option['reply'], tag + str(number) + ' option', shared, cast, others)
    if sum('callback' in c for c in chapters) < 3:
        raise ValueError('Epilogues require three callbacks to earlier epilogue choices')
    return True


def epilogues():
    result = []
    for tag in APPROVED:
        path = HERE / 'stories' / (tag + '.json')
        if path.exists():
            row = json.loads(path.read_text(encoding='utf-8-sig'))
            if row.get('tag') != tag:
                raise ValueError('Epilogue file and tag differ: ' + tag)
            validate(row)
            result.append(row)
    return result


if __name__ == '__main__':
    rows = epilogues()
    print(str(len(rows)) + ' Anean epilogues validated: ' + ', '.join(r['tag'] + ' ' + r['title'] for r in rows))
