"""Authoring contract for six original squadron narratives, not official lore."""
import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'


def day(value):
    return date(*map(int, value.split('.')))


def campaigns(require_chapters=True):
    result = json.loads((HERE / 'campaigns.json').read_text())['campaigns']
    if len(result) != 6 or len({row['tag'] for row in result}) != 6:
        raise ValueError('Expected six independent original story hosts')
    for row in result:
        if len(row['cast']) != 4 or len({p['id'] for p in row['cast']}) != 4:
            raise ValueError('Expected four recurring cast members: ' + row['tag'])
        if require_chapters:
            path = HERE / 'chapters' / (row['tag'] + '.json')
            row.update(json.loads(path.read_text(encoding='utf-8-sig')))
            validate(row)
    return result


def validate(row):
    chapters = row['chapters']
    if [c['id'] for c in chapters] != list(range(1, 21)):
        raise ValueError('Twenty ordered core chapters required: ' + row['tag'])
    flags = set()
    last = date(1991, 1, 1)
    for chapter in chapters:
        current = day(chapter['earliest'])
        if current < last or current > date(2005, 12, 31):
            raise ValueError('Unordered or out-of-scope core chapter: ' + str(chapter['id']))
        last = current
        act_start, act_end = row['acts'][(chapter['id'] - 1) // 5]
        if current < day(act_start) or (act_end and current > day(act_end)):
            raise ValueError('Chapter release falls outside its owned act window')
        if len(chapter['text'].split()) < 80:
            raise ValueError('Chapter needs a substantive scene: ' + row['tag'] + str(chapter['id']))
        if any(len(chapter[key].split()) < 80 for key in ('war_text', 'capitulated_text') if key in chapter):
            raise ValueError('Conditional scenes need the same substantive length as their base scene')
        variants = chapter.get('condition_variants', [])
        if len({v['id'] for v in variants}) != len(variants):
            raise ValueError('Duplicate conditional scene identity')
        for variant in variants:
            if not re.fullmatch(r'[a-z][a-z0-9_]+', variant['id']) or variant['id'] in ('cap', 'war', 'base'):
                raise ValueError('Conditional scene needs a distinct safe identity')
            if not variant.get('trigger') or len(variant['text'].split()) < 80:
                raise ValueError('Conditional scene needs an actual condition and substantive continuation')
        if not 2 <= len(chapter['options']) <= 3:
            raise ValueError('Each core scene requires two or three consequential choices')
        callback = chapter.get('callback')
        if callback and callback['flag'] not in flags:
            raise ValueError('Callback must refer to an earlier choice: ' + callback['flag'])
        for option in chapter['options']:
            if not re.fullmatch(r'[a-z][a-z0-9_]+', option['flag']) or option['flag'] in flags:
                raise ValueError('Choice flags must be safe and distinct: ' + option['flag'])
            flags.add(option['flag'])
            if len(option['reply'].split()) < 8:
                raise ValueError('Choice needs an authored response, not only a statistic')
            if not any(option.get(k, 0) for k in ('cohesion', 'credibility')):
                raise ValueError('Choice needs a persistent personal consequence')
            if any(abs(option.get(k, 0)) > 8 for k in ('cohesion', 'credibility')):
                raise ValueError('A single conversation cannot replace the whole relationship arc')
    endings = row['endings']
    if len(endings) != 3 or {e['id'] for e in endings} != {'trusted', 'compromised', 'fractured'}:
        raise ValueError('Three distinct personal conclusions required')
    if any(len(e['text'].split()) < 100 for e in endings):
        raise ValueError('Conclusions need substantive character assessments')
    if len({c['title'] for c in chapters}) != 20:
        raise ValueError('Repeated chapter title')
