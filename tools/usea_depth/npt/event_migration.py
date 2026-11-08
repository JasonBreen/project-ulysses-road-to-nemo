"""Restore only the PR #79 hosting hook before the immutable event-picture proof.

Reviewed delta: 5c479d90 -> a663cb5c, ac_ucw.32.a only.
https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/79#discussion_r4498543648
The caller still compares the complete event AST against its unchanged capture.
"""
import copy
from usea_expansion.script import get, parse


def restore_hosting(nodes):
    result = copy.deepcopy(nodes)
    matches = [body for kind, _, body in result
               if kind == 'country_event' and get(body, 'id') == 'ac_ucw.32']
    if len(matches) != 1:
        raise ValueError('Non-picture hosting event missing/duplicated')
    options = [body for kind, _, body in matches[0]
               if kind == 'option' and get(body, 'name') == 'ac_ucw.32.a']
    prefix = parse('name = ac_ucw.32.a ai_chance = { factor = 80 } ac_ud_npt_accept_hosting = yes')
    if len(options) != 1 or options[0][:3] != prefix:
        raise ValueError('Non-picture hosting option migration differs')
    del options[0][2]
    return result
