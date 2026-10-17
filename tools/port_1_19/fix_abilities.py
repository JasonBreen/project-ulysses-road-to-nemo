"""Port Project Ulysses leader abilities to the HOI4 1.19 ability format."""
import re
import os
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')).replace(os.sep, '/')

M = REPO + '/mod/2985041246/common/abilities/'
H = 'G:/steamlbirary/steamapps/common/Hearts of Iron IV/common/abilities/'

# 1) generic abilities: 1.19 vanilla file + the mod's "cheap ability" exclusions
s = open(H + 'generic_leader_abilities.txt', encoding='utf-8-sig').read()
for ability, trig in [('force_attack', 'has_cheap_force_attack'), ('last_stand', 'has_cheap_last_stand')]:
    start = s.index('\t%s = {' % ability)
    owner = s.index('OWNER = {', start)
    s = s[:owner + len('OWNER = {')] + '\n\t\t\t\t%s = no # Project Ulysses: cheap variant replaces this' % trig + s[owner + len('OWNER = {'):]
open(M + 'generic_leader_abilities.txt', 'w', encoding='utf-8-sig', newline='\n').write(
    '# Project Ulysses: HOI4 1.19.3 vanilla abilities plus exclusions for the cheap_* variants in cheap_leader_abilities.txt\n' + s)

# 2) cheap abilities: one_time_effect/add_temporary_buff_to_units was removed; use unit_modifiers
p = M + 'cheap_leader_abilities.txt'
s = open(p, encoding='utf-8-sig').read()
rename = {'combat_offense': 'offence', 'combat_breakthrough': 'breakthrough_factor', 'combat_defense': 'defence'}
pat = re.compile(r'one_time_effect = \{\s*add_temporary_buff_to_units = \{(.*?)\}\s*\}', re.S)


def repl(m):
    lines = []
    for line in m.group(1).splitlines():
        t = line.strip()
        if not t or t.startswith('days') or t.startswith('tooltip'):
            continue
        k, v = [x.strip() for x in t.split('=', 1)]
        lines.append('\t\t\t%s = %s' % (rename.get(k, k), v))
    return 'unit_modifiers = {\n' + '\n'.join(lines) + '\n\t\t}'


s, n = pat.subn(repl, s)
assert n == 2, n
open(p, 'w', encoding='utf-8-sig', newline='\n').write(s)
print('converted', n)

