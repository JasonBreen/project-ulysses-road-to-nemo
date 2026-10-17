"""Sum duplicate numeric modifier keys that ended up in the same block after modifier migrations."""
import re, sys

KEYS = {'air_superiority_efficiency', 'air_cas_efficiency', 'air_intercept_efficiency',
        'air_strategic_bomber_bombing_factor', 'air_strategic_bomber_defence_factor', 'command_cap_increase'}
NUM = re.compile(r'^(\s*)([a-z_]+)(\s*=\s*)(-?[0-9.]+)(.*)$')

for path in sys.argv[1:]:
    raw = open(path, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')
    nl = '\r\n' if '\r\n' in text else '\n'
    lines = text.split(nl)
    stack = [{}]
    drop = set()
    for i, line in enumerate(lines):
        code = line.split('#')[0]
        m = NUM.match(code)
        if m and m.group(2) in KEYS:
            k = m.group(2)
            if k in stack[-1]:
                j = stack[-1][k]
                mj = NUM.match(lines[j].split('#')[0])
                total = round(float(mj.group(4)) + float(m.group(4)), 4)
                lines[j] = f'{mj.group(1)}{k} = {total:g} # combined after 1.19 modifier migration'
                drop.add(i)
            else:
                stack[-1][k] = i
        for ch in code:
            if ch == '{':
                stack.append({})
            elif ch == '}':
                stack.pop()
    out = [l for i, l in enumerate(lines) if i not in drop]
    open(path, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + nl.join(out).encode('utf-8'))
    print(path.rsplit('/', 1)[-1], 'merged', len(drop))
