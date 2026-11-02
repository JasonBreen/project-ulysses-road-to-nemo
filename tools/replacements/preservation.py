"""Reverse only explicit reviewed changes before original_four hash checks.

The inherited fingerprints are never refreshed. Current source consistency,
force fingerprints and exact resource deltas are separate required checks.
"""
import copy
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
CHANGES=json.loads((HERE/'approved_changes.json').read_text())


def original_profile(tag,current):
    row=copy.deepcopy(current)
    for field,change in CHANGES['profiles'][tag].items():
        if row[field]!=change['after']:raise ValueError('Undeclared profile exception: '+tag+':'+field)
        if change['before_exists']:row[field]=change['before']
        else:del row[field]
    return row


def original_row(tag,current):
    row=copy.deepcopy(current)
    for state,changes in CHANGES['resources'][tag].items():
        for resource,amount in changes.items():
            row['placements'][state]['resources'][resource]-=amount
    return row


def original_generated(relative,tag,row,profile,builder):
    if relative.startswith('history/states/'):
        state=next(i for i,r in row['baseline'].items() if r['path']==relative)
        return builder.state_output(row,state,row['placements'][state])
    if relative.startswith('history/units/'):
        if '_land.' in relative:return builder.land_output(tag,row,profile)
        if '_air' in relative:return builder.air_output(tag,row,profile,'_bba.' in relative)
        if '_navy' in relative:return builder.navy_output(tag,row,profile,'_mtg.' in relative)
    if relative.startswith('common/ai_strategy/'):
        return builder.ai_output(tag,replacement_priorities=False)
    return None
