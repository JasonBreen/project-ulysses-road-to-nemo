"""Restore the original Project Ulysses frontend GUI files and make them 1.19-safe.

The original mod layout is kept exactly. Elements that HOI4 1.19 code looks up but the
1.14-era files lack are copied from vanilla and parked off-screen, so the engine finds them
without them being visible (no vanilla visuals on screen).
"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import pdx
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'frontend_briefing'))
from style_gui import style as briefing_style
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')).replace(os.sep, '/')
BASELINE = 'c452cf3'  # 'Establish Project Ulysses continuation baseline' (original v0.2 files)

M = REPO + '/mod/2985041246/interface/'
H = 'G:/steamlbirary/steamapps/common/Hearts of Iron IV/interface/'
OFF = 'position = { x = -20000 y = -20000 }'
NAME = re.compile(r'\bname\s*=\s*"?([A-Za-z0-9_]+)')


def original(f):
    return subprocess.run(['git', '-C', REPO, 'show', BASELINE + ':mod/2985041246/interface/' + f],
                          capture_output=True, check=True).stdout.decode('utf-8-sig')


class Node:
    def __init__(self, s, mask, a, b, bs, be, key):
        self.a, self.b, self.bs, self.be, self.key = a, b, bs, be, key
        self.name = None
        depth = 0
        for m in re.finditer(r'[{}]|\bname\s*=', mask[bs:be]):
            t = m.group(0)
            if t == '{': depth += 1
            elif t == '}': depth -= 1
            elif depth == 0:
                self.name = NAME.match(s[bs + m.start():]).group(1)
                break
        self.kids = [Node(s, mask, *c[1:], c[0]) for c in pdx.children(s, bs, be, mask)]

    def named(self):
        out = {}
        for k in self.kids:
            if k.name: out[k.name] = k
            for n, v in k.named().items(): out.setdefault(n, v)
        return out


def tree(s):
    mask = pdx.strip_comments_mask(s)
    root = [c for c in pdx.children(s, 0, len(s), mask) if c[0] == 'guiTypes'][0]
    return Node(s, mask, *root[1:], 'guiTypes')


def park(text):
    # positionType elements are invisible anchors the engine moves windows to: keep vanilla coordinates
    if text.lstrip().lower().startswith('positiontype'):
        return text
    # move the element's own (first, top-level) position off-screen; add one if absent
    body_start = text.index('{') + 1
    mask = pdx.strip_comments_mask(text)
    depth = 0
    for m in re.finditer(r'[{}]|\bposition\s*=\s*\{[^}]*\}', mask[body_start:]):
        t = m.group(0)
        if t == '{': depth += 1
        elif t == '}': depth -= 1
        elif depth == 0:
            a = body_start + m.start(); b = body_start + m.end()
            return text[:a] + OFF + ' # 1.19 compatibility stub, intentionally hidden' + text[b:]
    return text[:body_start] + '\n\t\t' + OFF + ' # 1.19 compatibility stub, intentionally hidden' + text[body_start:]


def restore(f, hide_new_types, transform=None):
    ms = original(f)
    if transform: ms = transform(ms)
    vs, _ = pdx.read(H + f)
    mt, vt = tree(ms), tree(vs)
    mtop = {k.name: k for k in mt.kids}
    inserts = []  # (pos, text)
    appended = []
    for vk in vt.kids:
        if vk.name not in mtop:
            t = vs[vk.a:vk.b]
            appended.append(park(t) if vk.name in hide_new_types else t)
            continue
        mk = mtop[vk.name]
        have = set(mk.named()) | {mk.name}

        def walk(vnode, mnode):
            for c in vnode.kids:
                if not c.name:
                    continue
                if c.name in have:
                    target = mnode.named().get(c.name) if mnode else None
                    walk(c, target or mnode)
                else:
                    host = mnode or mk
                    inserts.append((host.be, '\n\t\t' + park(vs[c.a:c.b]) + '\n\t'))
        walk(vk, mk)
    out = ms
    for pos, t in sorted(inserts, key=lambda x: -x[0]):
        out = out[:pos] + t + out[pos:]
    gt = tree(out)
    out = out[:gt.be] + '\n\t# ---- HOI4 1.19 GUI types required by the engine ----\n\t' + '\n\n\t'.join(appended) + '\n' + out[gt.be:]
    header = '# Project Ulysses original layout; 1.19-required elements added as hidden stubs (see restore_original_gui.py)\n'
    open(M + f, 'w', encoding='utf-8', newline='\n').write(header + out.replace('\r\n', '\n'))
    print(f, 'child stubs:', len(inserts), 'types appended:', len(appended))


def menu_fixes(s):
    s = s.replace('text = "OPEN ALPHA v.0.2 ------------------- UNDER OUR TREADS"', 'text = "PU_MAIN_MENU_VERSION"')
    assert 'PU_MAIN_MENU_VERSION' in s
    # no vanilla visuals: park the Paradox developer/publisher logos off-screen
    for sprite in ('GFX_frontend_dev_logo', 'GFX_pdx_int_logo'):
        s, n = re.subn(r'(spriteType = "%s"\s*\n\s*)position = \{[^}]*\}' % sprite,
                       r'\g<1>' + OFF + ' # hidden: no vanilla visuals', s)
        assert n == 1, sprite
    return s


restore('frontendmainview.gui', {'mainmenu_dlc_ownership', 'change_background'}, menu_fixes)
restore("frontendgamesetupview.gui", set(), briefing_style)
restore("countrytechtreeview.gui", set())

