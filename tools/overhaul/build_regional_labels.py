"""Replace demonstrated template labels without asserting new canonical cities."""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import get, parse

# These are inherited Earth/placeholder labels in the four approved partners.
# Other names (San Salvacion, Meriton, ravines, Ugellas) remain untouched.
STATES = {268: 'Delarus District A', 286: 'Ugellas District A',
          294: 'Ugellas District B', 492: 'Amber District A',
          501: 'Amber Capital District', 505: 'Delarus District B',
          606: 'Amber District B'}


def outputs():
    owners = {}
    for path in sorted((MOD / 'history/states').glob('*.txt')):
        state = get(parse(path.read_text(encoding='utf-8-sig')), 'state')
        ident = int(get(state, 'id'))
        for province, _, _ in get(state, 'provinces', []):
            owners[int(province)] = (ident, get(get(state, 'history'), 'owner', ''))
    names = {p.name[:3]: p.stem.split(' - ', 1)[-1]
             for p in (MOD / 'history/countries').glob('*.txt')}
    state_text = (MOD / 'localisation/english/state_names_l_english.yml').read_text(encoding='utf-8-sig')
    point_text = (MOD / 'localisation/english/victory_points_l_english.yml').read_text(encoding='utf-8-sig')
    rows = []
    for ident, label in STATES.items():
        match = re.search(r'^\s*STATE_' + str(ident) + r':\d+\s+"([^"]*)"', state_text, re.M)
        rows.append(dict(key='STATE_' + str(ident), old=match[1], value=label,
                         state=ident, source_layer='provisional gameplay',
                         reason='Neutral district label; canonical location mapping remains unestablished.'))
    counts = {}
    for match in re.finditer(r'^\s*(VICTORY_POINTS_(\d+)):\d+\s+"(TEMP|\d+)"', point_text, re.M):
        province = int(match[2])
        state, owner = owners.get(province, (None, ''))
        if state in (None, 171) or not owner:
            continue
        counts[owner] = counts.get(owner, 0) + 1
        index = counts[owner]
        suffix = ''
        while index:
            index, letter = divmod(index - 1, 26)
            suffix = chr(65 + letter) + suffix
        rows.append(dict(key=match[1], old=match[3],
                         value=names.get(owner, owner) + ' Locality ' + suffix,
                         province=province, state=state, owner=owner,
                         source_layer='provisional gameplay',
                         reason='Readable provisional locality; no named canonical city or new victory point is inferred.'))
    text = 'l_english:\n # Provisional geography labels; see tools/overhaul/regional_labels.json.\n'
    text += ''.join(' ' + row['key'] + ':0 "' + row['value'] + '"\n' for row in rows)
    return {MOD / 'localisation/english/replace/ac_overhaul_regions_l_english.yml': text.encode('utf-8-sig'),
            HERE / 'regional_labels.json': (json.dumps(dict(schema=1, changes=rows), indent=2) + '\n').encode()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, data in outputs().items():
        if args.check:
            if not path.exists() or path.read_bytes() != data:
                raise SystemExit('Regional labels differ: ' + str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print('Provisional regional labels: no border, province, core or ownership changes.')
