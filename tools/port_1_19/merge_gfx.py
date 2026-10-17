"""Append vanilla sprite definitions that a mod's same-named .gfx override drops."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import pdx
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')).replace(os.sep, '/')
M = REPO + '/mod/2985041246/interface/'
H = 'G:/steamlbirary/steamapps/common/Hearts of Iron IV/interface/'
MARK = '# --- HOI4 1.19.3 vanilla sprites missing from the Project Ulysses override (auto-merged) ---'
for f in sys.argv[1:]:
    ms, bom = pdx.read(M + f); vs, _ = pdx.read(H + f)
    if MARK in ms:
        print(f, 'already merged'); continue
    mnames = {n.lower() for _, n, _ in pdx.top_items(ms, 'spriteTypes')}
    missing = [raw for _, n, raw in pdx.top_items(vs, 'spriteTypes') if n and n.lower() not in mnames]
    mask = pdx.strip_comments_mask(ms)
    last = [c for c in pdx.children(ms, 0, len(ms), mask) if c[0] == 'spriteTypes'][-1]
    ins = '\n\t' + MARK + '\n\t' + '\n\t'.join(missing) + '\n'
    out = ms[:last[4]] + ins + ms[last[4]:]
    with open(M + f, 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='') as fh: fh.write(out)
    print(f, 'added', len(missing))

