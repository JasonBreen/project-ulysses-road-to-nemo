"""Compose explicit additive source receipts; never recapture preserved sources."""
import hashlib
import json
from pathlib import Path
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
    return files
