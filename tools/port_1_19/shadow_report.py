"""Report how each mod file that shadows a same-path vanilla file differs from HOI4 1.19 vanilla."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pdx
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')).replace(os.sep, '/')

M = REPO + '/mod/2985041246/'
H = 'G:/steamlbirary/steamapps/common/Hearts of Iron IV/'


def items(p):
    s = pdx.read(p)[0]
    mask = pdx.strip_comments_mask(s)
    tops = list(pdx.children(s, 0, len(s), mask))
    out = {}
    for k, a, b, bs, be in tops:
        inner = list(pdx.children(s, bs, be, mask))
        if inner and len(tops) < 6:
            for k2, a2, b2, bs2, be2 in inner:
                out[k + '/' + k2] = ' '.join(s[a2:b2].split())
        else:
            out[k] = ' '.join(s[a:b].split())
    return out


for root in sys.argv[1:] or ['common', 'events', 'history']:
    for dp, dn, fn in os.walk(M + root):
        for f in fn:
            if not f.endswith('.txt'):
                continue
            rel = os.path.relpath(os.path.join(dp, f), M).replace(os.sep, '/')
            if not os.path.exists(H + rel):
                continue
            m = items(M + rel)
            v = items(H + rel)
            mo = [k for k in m if k not in v]
            same = sum(1 for k in m if k in v and m[k] == v[k])
            diff = [k for k in m if k in v and m[k] != v[k]]
            vo = [k for k in v if k not in m]
            print(f"{rel}\tmod={len(m)} van={len(v)} modonly={len(mo)} same={same} diff={len(diff)} vanonly={len(vo)}\t{mo[:6]}")

