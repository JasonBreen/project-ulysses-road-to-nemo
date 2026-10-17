"""Fill the mod's empty strategic-region weather blocks (required by HOI4 1.15+).

For each mod region: mean pixel latitude (row in provinces.bmp) and land/sea type.
Weather is copied from the vanilla region of the same type whose mean latitude is closest.
Both maps are 5632x2048 with the same projection, so rows are comparable latitudes.
"""
import os, re, csv, sys
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')).replace(os.sep, '/')

MOD = REPO + '/mod/2985041246/map/'
VAN = 'G:/steamlbirary/steamapps/common/Hearts of Iron IV/map/'


def province_rows(root):
    img = np.asarray(Image.open(root + 'provinces.bmp').convert('RGB'), dtype=np.uint32)
    key = (img[:, :, 0] << 16) | (img[:, :, 1] << 8) | img[:, :, 2]
    color_to_id, kind = {}, {}
    with open(root + 'definition.csv', encoding='utf-8', errors='replace') as f:
        for row in csv.reader(f, delimiter=';'):
            if len(row) < 5 or not row[0].isdigit():
                continue
            pid = int(row[0])
            color_to_id[(int(row[1]) << 16) | (int(row[2]) << 8) | int(row[3])] = pid
            kind[pid] = row[4].strip()
    flat = key.ravel()
    rows = np.repeat(np.arange(key.shape[0]), key.shape[1])
    uniq, inv = np.unique(flat, return_inverse=True)
    sums = np.bincount(inv, weights=rows)
    cnts = np.bincount(inv)
    mean_row = {}
    for c, s, n in zip(uniq.tolist(), sums.tolist(), cnts.tolist()):
        pid = color_to_id.get(c)
        if pid is not None:
            mean_row[pid] = (s / n, n)
    return mean_row, kind


def regions(root):
    out = []
    d = root + 'strategicregions/'
    for fn in sorted(os.listdir(d)):
        s = open(d + fn, encoding='utf-8-sig', errors='replace').read()
        body = re.sub(r'#[^\n]*', '', re.search(r'provinces\s*=\s*\{([^}]*)\}', s).group(1))
        provs = [int(x) for x in body.split() if x.isdigit()]
        out.append((fn, s, provs))
    return out


def weather_block(s):
    m = re.search(r'\bweather\s*=\s*\{', s)
    i, depth = m.end() - 1, 0
    while True:
        if s[i] == '{': depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0: return m.start(), i + 1
        i += 1


def profile(provs, mean_row, kind):
    tot = w = 0.0; sea = land = 0
    for p in provs:
        if p in mean_row:
            r, n = mean_row[p]; tot += r * n; w += n
            if kind.get(p) == 'sea': sea += n
            else: land += n
    return (tot / w if w else None), ('sea' if sea > land else 'land')


vrow, vkind = province_rows(VAN)
vanilla = []
for fn, s, provs in regions(VAN):
    a, b = weather_block(s)
    if 'period' not in s[a:b]:
        continue
    lat, typ = profile(provs, vrow, vkind)
    if lat is not None:
        vanilla.append((lat, typ, s[a:b], fn))

mrow, mkind = province_rows(MOD)
done = 0
for fn, s, provs in regions(MOD):
    a, b = weather_block(s)
    if 'period' in s[a:b]:
        continue
    lat, typ = profile(provs, mrow, mkind)
    if lat is None:
        lat = 1024.0
    cands = [v for v in vanilla if v[1] == typ] or vanilla
    best = min(cands, key=lambda v: abs(v[0] - lat))
    new = s[:a] + best[2] + s[b:]
    open(MOD + 'strategicregions/' + fn, 'w', encoding='utf-8', newline='\n').write(new)
    done += 1
    if done <= 5 or '--verbose' in sys.argv:
        print(f'{fn}: {typ} row={lat:.0f} <- {best[3]} row={best[0]:.0f}')
print('regions filled:', done)

