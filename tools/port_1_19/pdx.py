"""Minimal Paradox-script block splitter that preserves raw text."""
import re

def read(p):
    b = open(p, 'rb').read()
    bom = b.startswith(b'\xef\xbb\xbf')
    return b.decode('utf-8-sig', errors='replace'), bom

def strip_comments_mask(s):
    """Return copy of s with comments and string contents replaced by spaces (same length)."""
    out = list(s); i = 0; n = len(s); instr = False
    while i < n:
        c = s[i]
        if instr:
            if c == '"': instr = False
            elif c != '\n': out[i] = ' '
        elif c == '"': instr = True
        elif c == '#':
            j = s.find('\n', i)
            j = n if j < 0 else j
            for k in range(i, j): out[k] = ' '
            i = j; continue
        i += 1
    return ''.join(out)

def children(s, start, end, mask=None):
    """Yield (key, raw_start, raw_end, body_start, body_end) for key = { ... } items between start and end."""
    if mask is None: mask = strip_comments_mask(s)
    i = start
    pat = re.compile(r'([A-Za-z0-9_\.:@\-]+)\s*=\s*\{')
    while True:
        m = pat.search(mask, i, end)
        if not m: return
        depth = 0; j = m.end() - 1
        while j < end:
            ch = mask[j]
            if ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0: break
            j += 1
        yield m.group(1), m.start(), j + 1, m.end(), j
        i = j + 1

def top_items(s, wrapper):
    """Items inside `wrapper = { ... }` blocks: list of (type, name, raw)."""
    mask = strip_comments_mask(s)
    res = []
    for key, a, b, bs, be in children(s, 0, len(s), mask):
        if key != wrapper: continue
        for k2, a2, b2, bs2, be2 in children(s, bs, be, mask):
            body = s[bs2:be2]
            # name = only at depth 0 of this body
            bm = mask[bs2:be2]
            name = None
            depth = 0
            for mm in re.finditer(r'[{}]|\bname\s*=', bm):
                t = mm.group(0)
                if t == '{': depth += 1
                elif t == '}': depth -= 1
                elif depth == 0:
                    name = re.search(r'name\s*=\s*"?([A-Za-z0-9_\.\-]+)', body[mm.start():]).group(1)
                    break
            res.append((k2, name, s[a2:b2]))
    return res
