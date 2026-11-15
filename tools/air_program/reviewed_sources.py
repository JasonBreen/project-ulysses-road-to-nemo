"""Compose explicit additive source receipts; never recapture preserved sources."""
import hashlib
import json
from pathlib import Path
import re
from script import parse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CAMPAIGN='mod/2985041246/common/scripted_effects/ac_campaign_effects.txt'
OUTCOME='ac_dispatch_belkan_war_outcome'


def validate_outcome(previous, receipt, text):
    if (receipt['schema'] != 1 or
        receipt['source_base_commit'] != 'bc5e6c18e587ed555179a815ae98e8dc1a10d8e5' or
        receipt['reviewed_change_commit'] != '47328d73450a262b28e066b72b6ea167fbcfd4bf' or
        set(receipt['files']) != {CAMPAIGN}):
        raise ValueError('Unexpected outcome receipt scope')
    row=receipt['files'][CAMPAIGN]
    if (row['old_sha256'] != previous['new_sha256'] or row['added'] != [OUTCOME] or
        row['changed'] or row['removed']):
        raise ValueError('Outcome receipt must add only the reviewed handoff')
    existing={**previous['unchanged_function_ast_sha256'],**previous['reviewed_function_ast_sha256']}
    if row['unchanged_function_ast_sha256'] != existing or set(row['reviewed_function_ast_sha256']) != {OUTCOME}:
        raise ValueError('Outcome receipt changed an existing source contract')
    actual=hashlib.sha256(text.replace('\r\n','\n').encode()).hexdigest()
    if actual != row['new_sha256']:
        raise ValueError('Outcome source digest changed')
    nodes=parse(text)
    names=[name for name,_,_ in nodes]
    expected={**existing,**row['reviewed_function_ast_sha256']}
    if len(names) != len(set(names)) or set(names) != set(expected):
        raise ValueError('Outcome source contains unreviewed effects')
    for name,_,body in nodes:
        actual=hashlib.sha256(json.dumps(body,separators=(',',':')).encode()).hexdigest()
        if actual != expected[name]:
            raise ValueError('Outcome source changed effect '+name)
    return row


def reviewed_updates():
    files={}
    for name in ('reviewed_owner_updates.json','reviewed_campaign_updates.json'):
        for path,row in json.loads((HERE/name).read_text())['files'].items():
            if path in files:
                raise ValueError('Duplicate reviewed source update '+path)
            files[path]=row
    receipt=json.loads((HERE/'reviewed_outcome_updates.json').read_text())
    previous=files[CAMPAIGN]
    row=validate_outcome(previous,receipt,(ROOT/CAMPAIGN).read_text(encoding='utf-8-sig'))
    # The original preserved hash is retained; only the explicitly chained tip changes.
    files[CAMPAIGN]={**previous,'new_sha256':row['new_sha256']}
    files[PWI] = validate_pwi_layout((ROOT/PWI).read_text(encoding='utf-8-sig'))
    receipt=json.loads((HERE/'reviewed_native_syntax_updates.json').read_text())
    if receipt['schema'] != 1 or set(receipt['files']) != NATIVE_SYNTAX_FILES:
        raise ValueError('Unexpected native syntax receipt scope')
    for path,row in receipt['files'].items():
        previous=files.get(path)
        validate_native_syntax(previous,row,(ROOT/path).read_text(encoding='utf-8-sig'))
        # The original preserved hash is retained; only the explicitly chained tip changes.
        files[path]={**(previous or {'old_sha256':row['old_sha256']}),'new_sha256':row['new_sha256']}
    return files


UCW = 'mod/2985041246/common/scripted_effects/ac_ucw.txt'
HOSTING = 'ac_ucw_stage_north_point'


def validate_hosting(previous, receipt, text):
    """Allow one reviewed hosting call; retain every earlier owner fingerprint."""
    if (receipt['schema'] != 1 or
        receipt['source_base_commit'] != '5c479d902c7c5b0dd7b4f45f0438a6de35972f4e' or
        receipt['reviewed_change_commit'] != 'a663cb5caf517bf81ce3307d74f61096d5366c44' or
        set(receipt['files']) != {UCW}):
        raise ValueError('Unexpected hosting receipt scope')
    row = receipt['files'][UCW]
    existing = {**previous['unchanged_function_ast_sha256'], **previous['reviewed_function_ast_sha256']}
    if (row['old_sha256'] != previous['new_sha256'] or row['added'] or row['removed'] or
        row['changed'] != [HOSTING] or
        row['old_changed_function_ast_sha256'] != {HOSTING: existing[HOSTING]} or
        set(row['reviewed_function_ast_sha256']) != {HOSTING} or
        row['unchanged_function_ast_sha256'] != {k: v for k, v in existing.items() if k != HOSTING}):
        raise ValueError('Hosting receipt changed an existing source contract')
    source = text.replace('\r\n', '\n')
    hook = '\t\t\t\t\tac_ud_npt_accept_hosting = yes\n'
    anchor = '\t\t\t\t\tadd_ideas = ac_ucw_npt_isaf_rear_base\n'
    if source.count(hook) != 1 or source.count(anchor + hook) != 1:
        raise ValueError('Hosting hook must follow the existing rear-base grant exactly once')
    if hashlib.sha256(source.replace(hook, '').encode()).hexdigest() != previous['new_sha256']:
        raise ValueError('UCW source differs beyond the reviewed hosting hook')
    if hashlib.sha256(source.encode()).hexdigest() != row['new_sha256']:
        raise ValueError('Hosting source digest changed')
    nodes = parse(source)
    names = [name for name, _, _ in nodes]
    expected = {**row['unchanged_function_ast_sha256'], **row['reviewed_function_ast_sha256']}
    if len(names) != len(set(names)) or set(names) != set(expected):
        raise ValueError('Hosting source contains unreviewed effects')
    for name, _, body in nodes:
        actual = hashlib.sha256(json.dumps(body, separators=(',', ':')).encode()).hexdigest()
        if actual != expected[name]:
            raise ValueError('Hosting source changed effect ' + name)
    return row


def reviewed_ucw_updates():
    files = json.loads((ROOT / 'tools/ac_campaigns/reviewed_owner_updates.json').read_text())['files']
    previous = files[UCW]
    receipt = json.loads((ROOT / 'tools/usea_depth/npt/reviewed_owner_updates.json').read_text())
    row = validate_hosting(previous, receipt, (ROOT / UCW).read_text(encoding='utf-8-sig'))
    # Compose the two explicit deltas back to the unchanged original protected capture.
    files[UCW] = {**previous, 'new_sha256': row['new_sha256'],
                  'changed': previous['changed'] + [HOSTING],
                  'old_changed_function_ast_sha256': {**previous['old_changed_function_ast_sha256'],
                                                     **row['old_changed_function_ast_sha256']},
                  'reviewed_function_ast_sha256': {**previous['reviewed_function_ast_sha256'],
                                                  **row['reviewed_function_ast_sha256']},
                  'unchanged_function_ast_sha256': {k: v for k, v in previous['unchanged_function_ast_sha256'].items()
                                                   if k != HOSTING}}
    return files


# PR #89, f70dc7b5e7b4bf5649cbaad815388a00c9a974b7, based on d3c17cc9.
# Retain the original air/naval capture and admit only the reviewed layout hook.
PWI = 'mod/2985041246/common/scripted_effects/ac_pwi.txt'
PWI_LAYOUT_UPDATE = {
    'old_sha256': '06449b2ad9a9a02924fab2066e9ea73bc808b73ab1e500ef91c1e705ce2a84e3',
    'new_sha256': 'e64c3c2004a6391ef88286552a7fba3073c67afdd196531684327430ee0566d4',
}


def validate_pwi_layout(text):
    """Prove every byte outside the reviewed one-time layout refresh is preserved."""
    source = text.replace('\r\n', '\n')
    hook = ('\t\t# Reveal the hidden aftermath branches now that allow_branch passes.\n'
            '\t\tmark_focus_tree_layout_dirty = yes\n')
    anchor = '\t\tcountry_event = { id = ac_pwi.1 days = 1 }\n'
    if source.count(hook) != 1 or source.count(anchor + hook) != 1:
        raise ValueError('PWI layout hook must follow the opening event exactly once')
    if hashlib.sha256(source.replace(hook, '').encode()).hexdigest() != PWI_LAYOUT_UPDATE['old_sha256']:
        raise ValueError('PWI source differs beyond the reviewed layout hook')
    if hashlib.sha256(source.encode()).hexdigest() != PWI_LAYOUT_UPDATE['new_sha256']:
        raise ValueError('PWI layout source digest changed')
    return dict(PWI_LAYOUT_UPDATE)


# Native playtest N007 and N008 (docs/evidence/native-belka-20261108/BUGS.md).
# In the native session "<scripted trigger> = no" did not invert the seed gate,
# the log rejected the >= / <= check_variable shorthand, and a bare
# variable-operand "date" read as an unset variable instead of global.date.
# Only those spellings may differ from the previously admitted text.
ECONOMY = 'mod/2985041246/common/scripted_effects/ac_economy_compat.txt'
MACRO = 'mod/2985041246/common/scripted_effects/ac_macro_effects.txt'
RECONSTRUCTION = 'mod/2985041246/common/scripted_effects/ac_reconstruction.txt'
NATIVE_SYNTAX_FILES = {ECONOMY, MACRO, RECONSTRUCTION}
COMPARISONS = (('greater_than_or_equals', '>='), ('less_than_or_equals', '<='))


def undo_native_syntax(source, substitutions):
    """Spell the reviewed native forms the way the previously admitted text did."""
    if set(substitutions) != {'global_date', 'negated_triggers', 'comparison_operators'}:
        raise ValueError('Unexpected native syntax substitutions')
    text = source
    if substitutions['global_date']:
        text = text.replace('global.date', 'date')
    for name in substitutions['negated_triggers']:
        if not re.fullmatch(r'ac_\w+', name):
            raise ValueError('Unexpected negated trigger ' + name)
        text = text.replace('NOT = { ' + name + ' = yes }', name + ' = no')
    if substitutions['comparison_operators']:
        for word, operator in COMPARISONS:
            text = re.sub(r'check_variable = \{ var = (\S+) value = (\S+) compare = ' + word + r' \}',
                          r'check_variable = { \1 ' + operator + r' \2 }', text)
    return text


def function_hashes(text):
    return {name: hashlib.sha256(json.dumps(body, separators=(',', ':')).encode()).hexdigest()
            for name, _, body in parse(text)}


def validate_native_syntax(previous, row, text):
    """Prove every byte outside the reviewed native spellings is preserved.

    previous is the already admitted receipt row, or None for a source whose
    original preserved capture was still current.
    """
    source = text.replace('\r\n', '\n')
    if row['added'] or row['removed']:
        raise ValueError('Native syntax receipt may not add or remove effects')
    if previous is not None and row['old_sha256'] != previous['new_sha256']:
        raise ValueError('Native syntax receipt does not continue the admitted source')
    restored = undo_native_syntax(source, row['substitutions'])
    if hashlib.sha256(restored.encode()).hexdigest() != row['old_sha256']:
        raise ValueError('Source differs beyond the reviewed native syntax')
    if hashlib.sha256(source.encode()).hexdigest() != row['new_sha256']:
        raise ValueError('Native syntax source digest changed')
    before = function_hashes(restored)
    after = function_hashes(source)
    changed = {name for name in after if after[name] != before.get(name)}
    if (set(before) != set(after) or not changed or set(row['changed']) != changed or
        row['old_changed_function_ast_sha256'] != {name: before[name] for name in changed} or
        row['reviewed_function_ast_sha256'] != {name: after[name] for name in changed}):
        raise ValueError('Native syntax receipt does not name exactly the respelled effects')
    if previous is not None:
        existing = {**previous['unchanged_function_ast_sha256'], **previous['reviewed_function_ast_sha256']}
        if before != existing:
            raise ValueError('Native syntax receipt changed an existing source contract')
    return row
