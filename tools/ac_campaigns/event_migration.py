"""Restore two approved Megalith edits before the immutable picture-fit proof.

The 2026-11-05 campaign approval changes gameplay, not the older source capture.
Only the exact registered ordered nodes may be restored. The caller still
compares the complete restored AST against that unchanged historical capture.
"""
import copy
from usea_expansion.script import get,parse

MIGRATIONS=(
    dict(event='ac_ucw.60',parent='option',
         old='add_timed_idea = { idea = ac_ucw_megalith_threat days = 14 }',
         new='if = { limit = { has_global_flag = ac_camp_enabled } add_ideas = ac_ucw_megalith_threat } else = { add_timed_idea = { idea = ac_ucw_megalith_threat days = 14 } }'),
    dict(event='ac_ucw.61',parent=None,
         old='trigger = { always = yes }',
         new='trigger = { OR = { NOT = { has_global_flag = ac_camp_enabled } has_global_flag = ac_camp_megalith_success } }'),
)


def restore_reviewed(nodes):
    result=copy.deepcopy(nodes)
    for migration in MIGRATIONS:
        matches=[body for kind,_,body in result if kind=='country_event' and get(body,'id')==migration['event']]
        if len(matches)!=1:raise ValueError('Non-picture campaign event missing/duplicated: '+migration['event'])
        body=matches[0]
        if migration['parent']:
            parents=[value for key,_,value in body if key==migration['parent']]
            if len(parents)!=1:raise ValueError('Non-picture campaign parent differs: '+migration['event'])
            body=parents[0]
        expected=parse(migration['new']);positions=[i for i in range(len(body)-len(expected)+1) if body[i:i+len(expected)]==expected]
        if len(positions)!=1:raise ValueError('Non-picture campaign migration differs: '+migration['event'])
        pos=positions[0];body[pos:pos+len(expected)]=parse(migration['old'])
    return result
