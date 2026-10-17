"""Replace pre-1.15 per-mission air modifiers with their HOI4 1.19 efficiency equivalents."""
import re, sys

TARGET = {
    'air_superiority': 'air_superiority_efficiency',
    'close_air_support': 'air_cas_efficiency',
    'interception': 'air_intercept_efficiency',
    'strategic_bomber': 'air_strategic_bomber_bombing_factor',
}
LINE = re.compile(r'^(\s*)air_(air_superiority|close_air_support|interception|strategic_bomber)_(attack|agility|defence)_factor\s*=\s*(-?[0-9.]+)(.*)$')

for path in sys.argv[1:]:
    raw = open(path, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')
    nl = '\r\n' if '\r\n' in text else '\n'
    lines = text.split(nl)
    out, i, changed = [], 0, 0
    while i < len(lines):
        m = LINE.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent, mission = m.group(1), m.group(2)
        vals = {}
        while i < len(lines) and (m := LINE.match(lines[i])) and m.group(2) == mission:
            vals[m.group(3)] = m.group(4); i += 1
        main = vals.get('attack') or vals.get('agility') or vals.get('defence')
        out.append(f'{indent}{TARGET[mission]} = {main} # was air_{mission}_* (removed in 1.15+)')
        if mission == 'strategic_bomber' and 'defence' in vals:
            out.append(f'{indent}air_strategic_bomber_defence_factor = {vals["defence"]}')
        changed += 1
    open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + nl.join(out).encode('utf-8'))
    print(path.rsplit('/', 1)[-1], 'groups replaced:', changed)
