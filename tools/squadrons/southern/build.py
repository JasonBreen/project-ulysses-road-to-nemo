"""Compile the Aurelian and Leasathian stories (namespace ac_sqs).

The compiler is the initial story compiler with the Pacific component's
default-preserving seams (numeric identity receipts, annexation interrupt,
admission horizon), renamed to its own namespace and files. Nothing here
changes the initial six or the Pacific two.

Admission
---------
A story ships only when it is listed in ``story_contract.ADMITTED`` and its
thirteen art masters are reviewed (``tools/squadrons/southern_art``). Until
then the mod holds no southern file, no picture is a placeholder, and the
compiled script exists only as an offline preview:

    python -B tools/squadrons/southern/build.py --check            # source valid, mod clean, preview pinned
    python -B tools/squadrons/southern/build.py --preview <dir>    # write the preview for review or tests
    python -B tools/squadrons/southern/build.py --record           # refresh preview.json after a reviewed text change
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from story_contract import ADMITTED, MOD, STORY, stories  # noqa: E402

NAMESPACE = 'ac_sqs'
STEM = 'ac_squadrons_southern'


def legacy_builder():
    if str(STORY) not in sys.path:
        sys.path.append(str(STORY))    # the initial compiler imports its own schema module
    spec = importlib.util.spec_from_file_location('southern_original_story_compiler', STORY / 'build.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prefix(text):
    return re.sub(r'(?<![A-Za-z0-9])ac_sq(?=[_.\s"}]|$)', NAMESPACE, text).replace('rule = ' + NAMESPACE + '_stories', 'rule = ac_sq_stories')


def compile_rows(rows):
    """The Pacific seams, applied to these rows; returns {relative path: text}."""
    if not rows:
        return {}
    old = legacy_builder()
    initialize = ''
    for row in rows:
        body = ('set_country_flag = ac_sq_initialized\nset_variable = { ac_sq_identity = THIS.id }\n'
                'set_variable = { ac_sq_chapter = 0 }\nset_variable = { ac_sq_pending_chapter = 0 }\n'
                'set_variable = { ac_sq_ending_kind = -1 }\nset_variable = { ac_sq_cohesion = 50 }\nset_variable = { ac_sq_credibility = 50 }\n')
        body += old.owned_if('date > ' + row['admission_until'], 'set_country_flag = ac_sq_closed\nset_country_flag = ac_sq_late_archive\n')
        body += old.block('else_if', old.block('limit', 'date > 1991.1.31') + 'set_variable = { ac_sq_chapter = 1 }\nset_country_flag = ' + old.flag(row, 'missed_1') + '\n')
        initialize += old.owned_if(old.identity(row['tag']) + ' ac_sq_enabled = yes NOT = { has_country_flag = ac_sq_initialized }', body)
    base = old.build(rows, initialize_effect=initialize)
    base.pop('common/game_rules/ac_squadrons.txt')
    localization = 'localisation/english/ac_squadrons_l_english.yml'
    rule_keys = {'ac_sq_rule', 'ac_sq_rule_on', 'ac_sq_rule_off', 'ac_sq_rule_on_desc', 'ac_sq_rule_off_desc', 'AC_SQUADRON_RULES'}
    base[localization] = '\n'.join(line for line in base[localization].splitlines() if line.strip().split(':', 1)[0] not in rule_keys) + '\n'
    trigger = 'common/scripted_triggers/ac_squadrons.txt'
    before = old.block('ac_sq_active', 'ac_sq_enabled = yes ac_sq_host = yes has_country_flag = ac_sq_initialized NOT = { has_country_flag = ac_sq_closed }')
    after = old.block('ac_sq_active', 'ac_sq_enabled = yes ac_sq_host = yes has_country_flag = ac_sq_initialized has_variable = ac_sq_identity check_variable = { var = ac_sq_identity value = THIS.id compare = equals } NOT = { has_country_flag = ac_sq_closed }')
    if base[trigger].count(before) != 1:
        raise ValueError('Initial active-contract seam changed; review explicitly')
    base[trigger] = base[trigger].replace(before, after)
    for path in tuple(base):
        if path.startswith('events/'):
            for row in rows:
                original = old.identity(row['tag'])
                base[path] = base[path].replace(original, original + ' has_variable = ac_sq_identity check_variable = { var = ac_sq_identity value = THIS.id compare = equals }')
    category = 'common/decisions/categories/ac_squadrons.txt'
    base[category] = base[category].replace('visible = {\n\t\thas_country_flag = ac_sq_initialized',
        'visible = {\n\t\thas_country_flag = ac_sq_initialized has_variable = ac_sq_identity check_variable = { var = ac_sq_identity value = THIS.id compare = equals }')
    before = old.block('ac_sq_air_capable', 'check_variable = { deployed_airforce_manpower_k > 0 }')
    after = old.block('ac_sq_air_capable', 'check_variable = { deployed_airforce_manpower_k > 0 } check_variable = { num_deployed_planes > 0 }')
    if base[trigger].count(before) != 1:
        raise ValueError('Initial capability seam changed; review explicitly')
    base[trigger] = base[trigger].replace(before, after)
    interrupt = ''
    for row in rows:
        cleanup = ''
        for chapter in row['chapters']:
            number = chapter['id']
            cleanup += old.owned_if('check_variable = { ac_sq_pending_chapter = ' + str(number) + ' } check_variable = { ac_sq_chapter = ' + str(number - 1) + ' }',
                                    'set_country_flag = ' + old.flag(row, 'missed_' + str(number)) + '\nset_variable = { ac_sq_chapter = ' + str(number) + ' }\n')
        cleanup += 'clr_country_flag = ac_sq_dispatch_pending\nset_variable = { ac_sq_pending_chapter = 0 }\nclr_country_flag = ac_sq_ending_pending\nset_country_flag = ac_sq_interrupted\n'
        condition = ('tag = ' + row['tag'] + ' original_tag = ' + row['tag'] + ' has_country_flag = ac_sq_initialized has_variable = ac_sq_identity '
                     'check_variable = { var = ac_sq_identity value = THIS.id compare = equals } NOT = { has_country_flag = ac_sq_closed }')
        interrupt += old.owned_if(condition, cleanup)
    base['common/scripted_effects/ac_squadrons.txt'] += old.block('ac_sq_interrupt', interrupt)
    actions = base['common/on_actions/ac_squadrons.txt']
    addition = old.block('on_annex', old.block('effect', old.block('FROM', 'ac_sq_interrupt = yes'))) + old.block('on_subject_annexed', old.block('effect', 'ac_sq_interrupt = yes'))
    if not actions.rstrip().endswith('}'):
        raise ValueError('Unexpected new-story on-action root')
    base['common/on_actions/ac_squadrons.txt'] = actions.rstrip()[:-1] + addition + '}\n'
    return {relative.replace('ac_squadrons', STEM): prefix(text) for relative, text in base.items()}


def encode(relative, text):
    return text.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8')


def record(preview):
    return {relative: hashlib.sha256(encode(relative, text)).hexdigest() for relative, text in sorted(preview.items())}


def summary(rows, preview):
    return dict(schema=1, namespace=NAMESPACE, initial_owner_untouched='ac_sq', existing_rule='ac_sq_stories',
                admitted=sorted(ADMITTED),
                stories=[dict(tag=r['tag'], id=r['id'], title=r['title'], base=r['base'], core_chapters=len(r['chapters']),
                              callbacks=sum('callback' in c for c in r['chapters']),
                              conditional_scenes=sum(len(c.get('condition_variants', [])) + ('capitulated_text' in c) for c in r['chapters']),
                              cast=[p['id'] for p in r['cast']], personal_endings=len(r['endings'])) for r in rows],
                preview_sha256=record(preview), native_acceptance=False)


def mod_files():
    return sorted(p.relative_to(MOD).as_posix() for p in MOD.rglob('*') if p.is_file() and STEM in p.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--preview', type=Path)
    args = parser.parse_args()
    rows = stories()
    preview = compile_rows(rows)
    shipped = compile_rows([r for r in rows if r['tag'] in ADMITTED])
    data = summary(rows, preview)
    text = json.dumps(data, indent=2) + '\n'
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
            raise SystemExit('Stale southern story preview record: run --record after reviewing the text change')
        if sorted(shipped) != mod_files():
            raise SystemExit('Southern story files in the mod differ from the admitted set: ' + ', '.join(mod_files()))
        for relative, body in shipped.items():
            if (MOD / relative).read_bytes().replace(b'\r\n', b'\n') != encode(relative, body):
                raise SystemExit('Stale admitted southern story: ' + relative)
    elif not args.preview and not args.record:
        for relative, body in shipped.items():
            target = MOD / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encode(relative, body))
    print(str(len(rows)) + ' southern stories (' + ', '.join(r['tag'] for r in rows) + '); admitted: ' + (', '.join(sorted(ADMITTED)) or 'none') +
          '; preview files ' + str(len(preview)))


if __name__ == '__main__':
    main()
