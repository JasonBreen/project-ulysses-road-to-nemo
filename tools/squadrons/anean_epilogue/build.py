"""Compile the Anean continuations (namespace ac_sqa), 2015-2016.

Admission reads the original story's recorded personal conclusion
(``ac_sq_<tag>_ending_<kind>``, written by the pinned initial compiler) and
snapshots it once into ``ac_sqa_<tag>_kind_<kind>``; every scene thereafter is
the one written for that conclusion, with its permitted cast. National context
is read when a scene is delivered and frozen with it. Options record personal
choices only: no score, reward, money, equipment or national effect.

Expiry: a scene unanswered for 30 days, or still unanswered when the window
closes, is filed as missed and never replayed; a save that first reaches the
host after the window closes never opens the epilogue. Annexation interrupts
it. The existing ``ac_sq_stories`` rule is the only preference.

Like the southern stories, an epilogue ships only when admitted
(``epilogue_contract.ADMITTED``) with its three reviewed scene masters; until
then the script is an offline preview (``--preview``, ``--check``, ``--record``).
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from epilogue_contract import ADMITTED, KINDS, MOD, NAMESPACE, WINDOW, epilogues  # noqa: E402

N = NAMESPACE
STEM = 'ac_squadrons_anean_epilogue'


def block(key, text):
    return key + ' = {\n' + '\n'.join('\t' + line if line else line for line in text.rstrip('\n').split('\n')) + '\n}\n'


def owned_if(condition, effect):
    return block('if', block('limit', condition) + effect)


def quote(text):
    return text.replace('"', '\\"').replace('\n', '\\n')


def identity(tag):
    return 'tag = ' + tag + ' original_tag = ' + tag + ' country_exists = ' + tag


def flag(row, short):
    return N + '_' + row['tag'].lower() + '_' + short


def event_id(row, number):
    return N + '.' + str(row['base'] + number)


def contexts(chapter):
    """Ordered, mutually exclusive national contexts; the default takes the rest."""
    result = []
    for context in chapter['contexts']:
        condition = context['trigger']
        if result:
            condition += '\n' + block('NOT', block('OR', ''.join(block('AND', rule) for _, rule, _ in result)))
        result.append((context['id'], condition, context['text']))
    rest = block('NOT', block('OR', ''.join(block('AND', rule) for _, rule, _ in result)))
    result.append(('default', rest, chapter['default_context']))
    return result


def compile_rows(rows):
    if not rows:
        return {}
    loc = {}
    effects = triggers = events = ''
    triggers += block(N + '_enabled', 'has_game_rule = { rule = ac_sq_stories option = enabled }')
    triggers += block(N + '_host', 'OR = { ' + ' '.join('AND = { ' + identity(r['tag']) + ' }' for r in rows) + ' }')
    triggers += block(N + '_active', N + '_enabled = yes ' + N + '_host = yes has_country_flag = ' + N + '_initialized '
                      'has_variable = ' + N + '_identity check_variable = { var = ' + N + '_identity value = THIS.id compare = equals } '
                      'NOT = { has_country_flag = ' + N + '_closed }')
    tick = ''
    loc[N + '_close'] = 'Keep their account.'
    loc[N + '_expired_close'] = 'File this scene without replaying its choices.'
    for row in rows:
        tag, low = row['tag'], row['tag'].lower()
        ending = {kind: 'ac_sq_' + low + '_ending_' + kind for kind in KINDS}
        # Admission: once, inside the window, from the recorded conclusion.
        admit = ''
        for index, kind in enumerate(KINDS):
            body = ('set_country_flag = ' + N + '_initialized\nset_variable = { ' + N + '_identity = THIS.id }\n'
                    'set_variable = { ' + N + '_chapter = 0 }\nset_variable = { ' + N + '_pending_chapter = 0 }\n'
                    'set_country_flag = ' + flag(row, 'kind_' + kind) + '\n')
            admit += block('if' if index == 0 else 'else_if', block('limit', 'has_country_flag = ' + ending[kind]) + body)
        tick += owned_if(identity(tag) + ' ' + N + '_enabled = yes NOT = { has_country_flag = ' + N + '_initialized } '
                         'NOT = { has_country_flag = ' + N + '_closed } NOT = { date < ' + WINDOW[0] + ' } NOT = { date > ' + WINDOW[1] + ' }', admit)
        tick += owned_if(identity(tag) + ' NOT = { has_country_flag = ' + N + '_initialized } NOT = { has_country_flag = ' + N + '_closed } date > ' + WINDOW[1],
                         'set_country_flag = ' + N + '_closed\nset_country_flag = ' + N + '_late_archive\n')
        live = identity(tag) + ' ' + N + '_active = yes'
        dispatch = ''
        for chapter in row['chapters']:
            number = chapter['id']
            ident = event_id(row, number)
            pending = (live + ' has_country_flag = ' + N + '_dispatch_pending check_variable = { ' + N + '_chapter = ' + str(number - 1) + ' } '
                       'check_variable = { ' + N + '_pending_chapter = ' + str(number) + ' } NOT = { date > ' + WINDOW[1] + ' }')
            # Expiry: an unanswered reservation, or the window's end, files the scene as missed.
            dispatch += owned_if(live + ' check_variable = { ' + N + '_pending_chapter = ' + str(number) + ' } check_variable = { ' + N + '_chapter = ' + str(number - 1) + ' } '
                                 'OR = { NOT = { has_country_flag = ' + N + '_dispatch_pending } date > ' + WINDOW[1] + ' }',
                                 'set_country_flag = ' + flag(row, 'missed_' + str(number)) + '\nset_variable = { ' + N + '_chapter = ' + str(number) + ' }\n'
                                 'clr_country_flag = ' + N + '_dispatch_pending\nset_variable = { ' + N + '_pending_chapter = 0 }\n')
            dispatch += owned_if(live + ' NOT = { has_country_flag = ' + N + '_dispatch_pending } NOT = { has_country_flag = ' + N + '_cooldown } '
                                 'check_variable = { ' + N + '_chapter = ' + str(number - 1) + ' } NOT = { date < ' + chapter['earliest'] + ' } NOT = { date > ' + WINDOW[1] + ' }',
                                 'set_variable = { ' + N + '_pending_chapter = ' + str(number) + ' }\nset_country_flag = { flag = ' + N + '_dispatch_pending days = 30 }\n'
                                 'country_event = { id = ' + ident + ' days = 1 }\n')
            # The event: one scene per conclusion, one national paragraph, the callback if earned.
            loc[ident + '.t'] = chapter['title']
            desc = ''
            snapshot = 'set_country_flag = ' + flag(row, 'delivered_' + str(number)) + '\n'
            callback = chapter.get('callback')
            rows_context = contexts(chapter)
            for context, condition, _ in rows_context:
                snapshot += owned_if(condition, 'set_country_flag = ' + flag(row, 'view_' + str(number) + '_' + context) + '\n')
            if callback:
                snapshot += owned_if('has_country_flag = ' + flag(row, callback['flag']), 'set_country_flag = ' + flag(row, 'callback_' + str(number)) + '\n')
            for kind in KINDS:
                for context, _, paragraph in rows_context:
                    for with_callback in ((True, False) if callback else (False,)):
                        key = ident + '.d_' + kind + '_' + context + ('_callback' if with_callback else '')
                        loc[key] = chapter['texts'][kind] + '\n\n' + paragraph + ('\n\n' + callback['text'] if with_callback else '')
                        test = 'has_country_flag = ' + flag(row, 'kind_' + kind) + ' has_country_flag = ' + flag(row, 'view_' + str(number) + '_' + context)
                        if callback:
                            seen = 'has_country_flag = ' + flag(row, 'callback_' + str(number))
                            test += ' ' + (seen if with_callback else block('NOT', seen).strip())
                        desc += block('desc', 'text = ' + key + '\n' + block('trigger', test))
            options = ''
            valid = pending + ' has_country_flag = ' + flag(row, 'delivered_' + str(number))
            for index, choice in enumerate(chapter['options']):
                name = ident + '.' + chr(97 + index)
                loc[name] = choice['label']
                loc[name + '.reply'] = choice['reply']
                effect = ('set_country_flag = ' + flag(row, 'chapter_' + str(number)) + '\nset_country_flag = ' + flag(row, choice['flag']) + '\n'
                          'set_variable = { ' + N + '_chapter = ' + str(number) + ' }\nclr_country_flag = ' + N + '_dispatch_pending\n'
                          'set_variable = { ' + N + '_pending_chapter = 0 }\nset_country_flag = { flag = ' + N + '_cooldown days = 30 }\n')
                if number == len(row['chapters']):
                    effect += 'set_country_flag = ' + flag(row, 'complete') + '\nset_country_flag = ' + N + '_closed\n'
                options += block('option', 'name = ' + name + '\nai_chance = { factor = 50 }\n' + block('trigger', valid) +
                                 'custom_effect_tooltip = ' + name + '.reply\n' + owned_if(valid, effect))
            options += block('option', 'name = ' + N + '_expired_close\n' + block('trigger', block('NOT', valid)))
            slot = next(s for s, indices in row['chapters_by_slot'].items() if number in indices)
            events += block('country_event', 'id = ' + ident + '\ntitle = ' + ident + '.t\n' + desc +
                            'picture = GFX_' + N + '_' + low + '_scene_' + slot + '\nis_triggered_only = yes\n' + block('trigger', pending) +
                            block('immediate', owned_if(pending + ' NOT = { has_country_flag = ' + flag(row, 'delivered_' + str(number)) + ' }', snapshot)) + options)
        # The window closes an unfinished epilogue after its last reservation is filed.
        dispatch += owned_if(live + ' date > ' + WINDOW[1] + ' NOT = { has_country_flag = ' + N + '_dispatch_pending }',
                             'set_country_flag = ' + flag(row, 'unfinished') + '\nset_country_flag = ' + N + '_closed\n')
        effects += block(N + '_' + low + '_dispatch', dispatch)
        tick += owned_if(live, N + '_' + low + '_dispatch = yes\n')
        interrupt = owned_if('tag = ' + tag + ' original_tag = ' + tag + ' has_country_flag = ' + N + '_initialized NOT = { has_country_flag = ' + N + '_closed }',
                             'clr_country_flag = ' + N + '_dispatch_pending\nset_variable = { ' + N + '_pending_chapter = 0 }\n'
                             'set_country_flag = ' + N + '_interrupted\nset_country_flag = ' + N + '_closed\n')
        effects += block(N + '_' + low + '_interrupt', interrupt)
    effects = block(N + '_tick', tick) + effects
    effects += block(N + '_interrupt', ''.join(N + '_' + r['tag'].lower() + '_interrupt = yes\n' for r in rows))
    actions = block('on_actions', block('on_weekly', block('effect', owned_if(N + '_host = yes', N + '_tick = yes\n'))) +
                    block('on_annex', block('effect', block('FROM', N + '_interrupt = yes\n'))) +
                    block('on_subject_annexed', block('effect', N + '_interrupt = yes\n')))
    yml = 'l_english:\n' + ''.join(' ' + key + ':0 "' + quote(value) + '"\n' for key, value in loc.items())
    return {'common/scripted_effects/' + STEM + '.txt': effects, 'common/scripted_triggers/' + STEM + '.txt': triggers,
            'common/on_actions/' + STEM + '.txt': actions, 'events/' + STEM + '.txt': 'add_namespace = ' + N + '\n\n' + events,
            'localisation/english/' + STEM + '_l_english.yml': yml}


def encode(relative, text):
    return text.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8')


def summary(rows, preview):
    return dict(schema=1, namespace=N, existing_rule='ac_sq_stories', window=WINDOW, admitted=sorted(ADMITTED),
                epilogues=[dict(tag=r['tag'], id=r['id'], title=r['title'], base=r['base'], source_story=r['source_story'],
                                chapters=len(r['chapters']), cast_by_ending=r['cast_by_ending'],
                                contexts=sum(len(c['contexts']) + 1 for c in r['chapters']),
                                callbacks=sum('callback' in c for c in r['chapters'])) for r in rows],
                preview_sha256={k: hashlib.sha256(encode(k, v)).hexdigest() for k, v in sorted(preview.items())},
                native_acceptance=False)


def mod_files():
    return sorted(p.relative_to(MOD).as_posix() for p in MOD.rglob('*') if p.is_file() and STEM in p.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--preview', type=Path)
    args = parser.parse_args()
    rows = epilogues()
    preview = compile_rows(rows)
    shipped = compile_rows([r for r in rows if r['tag'] in ADMITTED])
    text = json.dumps(summary(rows, preview), indent=2) + '\n'
    path = HERE / 'preview.json'
    if args.preview:
        for relative, body in preview.items():
            target = args.preview / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encode(relative, body))
    if args.record:
        path.write_text(text, encoding='utf-8', newline='\n')
    if args.check:
        if not path.exists() or path.read_text(encoding='utf-8').replace('\r\n', '\n') != text:
            raise SystemExit('Stale epilogue preview record: run --record after reviewing the text change')
        if sorted(shipped) != mod_files():
            raise SystemExit('Epilogue files in the mod differ from the admitted set: ' + ', '.join(mod_files()))
        for relative, body in shipped.items():
            if (MOD / relative).read_bytes().replace(b'\r\n', b'\n') != encode(relative, body):
                raise SystemExit('Stale admitted epilogue: ' + relative)
    elif not args.preview and not args.record:
        for relative, body in shipped.items():
            target = MOD / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encode(relative, body))
    print(str(len(rows)) + ' Anean epilogues (' + ', '.join(r['tag'] for r in rows) + '); admitted: ' + (', '.join(sorted(ADMITTED)) or 'none') +
          '; preview files ' + str(len(preview)))


if __name__ == '__main__':
    main()
