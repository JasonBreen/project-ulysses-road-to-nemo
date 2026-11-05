"""Authoring contract for the Aurelian and Leasathian squadron stories.

Original supporting fiction, not official lore. The rules mirror the initial
schema (twenty ordered chapters, two or three consequential choices, three
personal conclusions) and the Pacific extension (twelve callbacks, two bounded
relationship changes per choice), with three additions that only these stories
need: a fixed 1991-2020 act calendar, conditional scenes that may read only
the published Aurelia-Leasath (``ac_alc_*``) and Leasath civil-war
(``ac_lcw_*``) records, and a name screen that keeps official characters and
every other story's cast out of the text.

The pinned initial ``tools/squadrons/schema.py`` is not edited: its horizon
admission is identity-based, and these rows carry their own contract here.
"""
import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORY = HERE.parent
ROOT = HERE.parents[2]
MOD = ROOT / 'mod/2985041246'

CONTRACT = 'southern_story_v1'
HORIZON = '2020.12.31'
APPROVED = {
    'AUR': dict(id='kept_in_repair', base=900,
                cast=('ciro_avellan', 'lucia_ferro', 'ines_carvalho', 'hector_mendaro')),
    'LEA': dict(id='orders_in_two_hands', base=1000,
                cast=('mateo_salvaterra', 'noemi_arcos', 'gabriel_tenorio', 'sofia_landa')),
}
# A tag is admitted (its script ships in the mod) only after its thirteen art
# masters are generated, reviewed and packaged under tools/squadrons/southern_art.
# No placeholder picture ever ships; until then the script is an offline preview.
ADMITTED = ()
ACTS = [['1991.1.1', '1999.12.31'], ['2000.1.1', '2008.12.31'], ['2009.1.1', '2019.6.30'], ['2019.7.1', None]]
CORE_SLOTS = {'1': [1, 2, 6], '2': [3, 7, 12, 16], '3': [4, 8, 13, 17], '4': [5, 9, 11, 14, 18], '5': [10, 15, 19, 20]}
ENDING_SLOTS = {'trusted': 6, 'compromised': 7, 'fractured': 8}
COUNTERPART = {'AUR': 'LEA', 'LEA': 'AUR'}

# Official people, squadrons and weapons are never characters; the stories
# assert no strategic weapon. Matched as whole words, case-sensitively.
FORBIDDEN = ('Gryphus', 'Talisman', 'Shamrock', 'Lampert', 'Navarro', 'Gaspar', 'Varcolac', 'Cuervo',
             'Nemo', 'Mobius', 'Scarface', 'Garuda', 'Galm', 'Razgriz', 'Strigon', 'Pasternak',
             'Antares', 'Gleipnir', 'Archelon', 'Nevera', 'Meson', 'Chandelier', 'Arkbird',
             'Stonehenge', 'Megalith', 'Excalibur', 'Aigaion', 'Kei', 'Nagase', 'Bartlett')
TRIGGER_KEYS = {'has_capitulated', 'has_war', 'has_war_with', 'ac_sq_air_capable', 'has_global_flag', 'NOT', 'OR', 'AND'}


def day(value):
    return date(*map(int, value.split('.')))


def published_flags():
    """Global flags the two owners actually set in the generated mod."""
    flags = set()
    for name in ('ac_southern_theater.txt', 'ac_leasath.txt'):
        path = MOD / 'common/scripted_effects' / name
        flags |= set(re.findall(r'set_global_flag = ((?:ac_alc|ac_lcw)_[a-z0-9_]+)', path.read_text(encoding='utf-8-sig')))
    return flags


def other_cast_names():
    names = set()
    for row in json.loads((STORY / 'campaigns.json').read_text())['campaigns']:
        names |= {p['name'] for p in row['cast']}
    for path in sorted((STORY / 'pacific/metadata').glob('*.json'), key=lambda p: p.as_posix()):
        names |= {p['name'] for p in json.loads(path.read_text(encoding='utf-8-sig'))['cast']}
    return names


def check_trigger(trigger, tag, flags):
    tokens = re.findall(r'[{}=]|[^\s{}=]+', trigger)
    if tokens.count('{') != tokens.count('}'):
        raise ValueError('Unbalanced conditional scene trigger: ' + trigger)
    for index, token in enumerate(tokens):
        if token in '{}=' or (index and tokens[index - 1] == '='):
            continue
        if token not in TRIGGER_KEYS:
            raise ValueError('Conditional scene may not read ' + token)
        value = tokens[index + 2] if index + 2 < len(tokens) else ''
        if token == 'has_global_flag' and value not in flags:
            raise ValueError('Conditional scene reads an unpublished flag: ' + value)
        if token == 'has_war_with' and value != COUNTERPART[tag]:
            raise ValueError('Conditional scene may observe only the counterpart war: ' + value)
        if token in ('has_capitulated', 'has_war', 'ac_sq_air_capable') and value not in ('yes', 'no'):
            raise ValueError('Boolean trigger needs yes/no: ' + token)


def screen_names(text, where, others):
    for word in FORBIDDEN:
        if re.search(r'\b' + word + r'\b', text):
            raise ValueError(where + ' names an official character or weapon: ' + word)
    for name in others:
        if name in text:
            raise ValueError(where + ' names another story\'s cast member: ' + name)
    if any(ord(ch) > 0x7e or (ord(ch) < 0x20 and ch != '\n') for ch in text):
        raise ValueError(where + ' uses a character outside the ASCII briefing contract')


def words(text):
    return len(text.split())


def validate(meta, story, flags=None, others=None):
    tag = meta.get('tag')
    contract = APPROVED.get(tag)
    if not contract or meta.get('id') != contract['id'] or meta.get('base') != contract['base']:
        raise ValueError('Unapproved southern story identity')
    if meta.get('extension_contract') != CONTRACT or meta.get('admission_until') != HORIZON:
        raise ValueError('Unapproved southern admission contract')
    if meta.get('acts') != ACTS or meta.get('chapters_by_slot') != CORE_SLOTS or meta.get('ending_slots') != ENDING_SLOTS:
        raise ValueError('Locked southern calendar or art mapping changed')
    if tuple(p['id'] for p in meta['cast']) != contract['cast']:
        raise ValueError('The four approved original cast identities must remain stable')
    flags = published_flags() if flags is None else flags
    others = other_cast_names() if others is None else others
    for person in meta['cast']:
        if words(person['portrait']) < 15 or words(person['bio']) < 40 or not person['bio'].startswith('1991 personnel file.'):
            raise ValueError('Cast record needs an appearance note and a 1991 personnel file: ' + person['id'])
        screen_names(person['bio'] + ' ' + person['name'], person['id'], others)
    if set(meta['scene_subjects']) != {str(n) for n in range(1, 9)}:
        raise ValueError('Eight scene subjects required')
    for slot, scene in meta['scene_subjects'].items():
        if not scene['title'] or words(scene['subject']) < 30:
            raise ValueError('Scene subject needs a concrete brief: ' + slot)
    if words(meta['loading_subject']) < 30:
        raise ValueError('Loading screen needs a concrete brief')
    chapters = story['chapters']
    if [c['id'] for c in chapters] != list(range(1, 21)):
        raise ValueError('Twenty ordered core chapters required: ' + tag)
    if len({c['title'] for c in chapters}) != 20:
        raise ValueError('Repeated chapter title')
    chosen = set()
    last = date(1991, 1, 1)
    first_names = {p['name'].split()[0] for p in meta['cast']}
    seen = {name: 0 for name in first_names}
    for chapter in chapters:
        number = chapter['id']
        current = day(chapter['earliest'])
        start, end = ACTS[(number - 1) // 5]
        if current < last or current > day(HORIZON) or current < day(start) or (end and current > day(end)):
            raise ValueError('Chapter release falls outside its ordered act window: ' + str(number))
        if number > 1 and (current - last).days < 35:
            raise ValueError('Chapters need a month apart for the dispatch cooldown: ' + str(number))
        last = current
        scenes = [chapter['text']] + [chapter[k] for k in ('capitulated_text', 'war_text') if k in chapter]
        variants = chapter.get('condition_variants', [])
        if len({v['id'] for v in variants}) != len(variants):
            raise ValueError('Duplicate conditional scene identity')
        for variant in variants:
            if not re.fullmatch(r'[a-z][a-z0-9_]+', variant['id']) or variant['id'] in ('cap', 'war', 'base'):
                raise ValueError('Conditional scene needs a distinct safe identity')
            check_trigger(variant['trigger'], tag, flags)
            scenes.append(variant['text'])
        for prose in scenes:
            if words(prose) < 80:
                raise ValueError('Every scene needs a substantive length: ' + tag + str(number))
            screen_names(prose, tag + str(number), others)
        for name in first_names:
            seen[name] += any(re.search(r'\b' + name + r'\b', prose) for prose in scenes)
        if not 2 <= len(chapter['options']) <= 3:
            raise ValueError('Each core scene requires two or three consequential choices')
        callback = chapter.get('callback')
        if callback:
            if callback['flag'] not in chosen:
                raise ValueError('Callback must refer to an earlier choice: ' + callback['flag'])
            if words(callback['text']) < 12:
                raise ValueError('Callback needs an authored recollection')
            screen_names(callback['text'], tag + str(number) + ' callback', others)
        for option in chapter['options']:
            if not re.fullmatch(r'[a-z][a-z0-9_]{2,40}', option['flag']) or option['flag'] in chosen:
                raise ValueError('Choice flags must be safe and distinct: ' + option['flag'])
            chosen.add(option['flag'])
            if words(option['reply']) < 8 or not option['label'].strip():
                raise ValueError('Choice needs an authored response, not only a statistic')
            screen_names(option['label'] + ' ' + option['reply'], tag + str(number) + ' option', others)
            if any(type(option.get(k)) is not int or not 1 <= abs(option[k]) <= 8 for k in ('cohesion', 'credibility')):
                raise ValueError('Choices require two explicit bounded relationship changes')
    if sum('callback' in c for c in chapters) < 12:
        raise ValueError('Southern stories require twelve persistent later callbacks')
    if any(count < 5 for count in seen.values()):
        raise ValueError('Every principal must recur in at least five chapters: ' + str(seen))
    endings = story['endings']
    if [e['id'] for e in endings] != ['trusted', 'compromised', 'fractured']:
        raise ValueError('Three distinct personal conclusions required, in kind order')
    for ending in endings:
        if words(ending['text']) < 100 or not ending['title']:
            raise ValueError('Conclusions need substantive character assessments')
        screen_names(ending['text'], tag + ' ending', others)
    return True


def stories(require_chapters=True):
    result = []
    for tag in APPROVED:
        path = HERE / 'metadata' / (tag + '.json')
        if not path.exists():
            continue
        row = json.loads(path.read_text(encoding='utf-8-sig'))
        if row.get('tag') != tag:
            raise ValueError('Metadata file and tag differ: ' + tag)
        if require_chapters:
            story = json.loads((HERE / 'chapters' / (tag + '.json')).read_text(encoding='utf-8-sig'))
            validate(row, story)
            row.update(story)
        result.append(row)
    extras = {p.stem for p in (HERE / 'metadata').glob('*.json')} - set(APPROVED)
    if extras:
        raise ValueError('Unknown southern metadata: ' + ','.join(sorted(extras)))
    return result


if __name__ == '__main__':
    rows = stories()
    print(str(len(rows)) + ' southern stories validated: ' + ', '.join(r['tag'] + ' ' + r['title'] for r in rows))
