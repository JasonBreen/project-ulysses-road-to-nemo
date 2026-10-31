"""Repair inherited foreign capitals using the approved geographic fallback.

Existing owned capitals and dormant/placeholder histories are preserved. This
changes only the root capital assignment of the fourteen reviewed histories;
it grants nothing to existing saves and does not change state or map geometry.
"""
import argparse
import hashlib
from fractions import Fraction
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
sys.path.insert(0, str(ROOT / 'tools/anea'))
from script import parse, get
from foundation_map import topology, components

BASE = '3810d1abeb9749a265b7b48e8d9eccddf08b1be2'
# These are the reviewed invalid assignments on the verified implementation
# base, not a rule which later retargets every capital during a running game.
INVALID = {'AEM': 1, 'AZB': 1, 'CRS': 1, 'ECH': 1, 'ESN': 1,
           'GLA': 1, 'KLG': 1, 'MAY': 224, 'RMN': 1, 'SET': 1,
           'SFA': 1, 'SOA': 1, 'VER': 481, 'WEL': 1}
CAPITAL = re.compile(r'^(\s*capital\s*=\s*)\d+([^\r\n]*)$', re.M)


def centroid(provinces, centres, area):
    weight = sum(int(area[p]) for p in provinces)
    if not weight:
        raise ValueError('A selected land component has no raster area')
    # Raster moments are integer pixel-coordinate sums. Recover those integers
    # before centroid arithmetic: squaring binary floats differed in the last
    # digit between Windows and Linux. Exact fractions also make real ties use
    # the documented state-ID rule instead of a platform rounding accident.
    return tuple(Fraction(sum(round(centres[p][axis] * int(area[p])) for p in provinces), weight)
                 for axis in (0, 1))


def select(states, graph, centres, area):
    """Largest actual landmass by pixel area, central state, stable ID tie."""
    owned = set().union(*(set(row['land']) for row in states.values()))
    groups = sorted(components(owned, graph), key=lambda group: (-sum(int(area[p]) for p in group), min(group)))
    if not groups:
        raise ValueError('An active country has no owned raster land')
    mainland = groups[0]
    centre = centroid(mainland, centres, area)
    candidates = {i: centroid(set(row['land']) & mainland, centres, area)
                  for i, row in states.items() if set(row['land']) & mainland}
    distance = lambda a, b: sum((a[axis] - b[axis]) ** 2 for axis in (0, 1))
    selected = min(candidates, key=lambda i: (distance(candidates[i], centre), i))
    province = min(set(states[selected]['land']) & mainland,
                   key=lambda p: (distance(centroid({p}, centres, area), candidates[selected]), p))
    return dict(capital=selected, representative_province=province,
                mainland_provinces=sorted(mainland), mainland_pixel_area=sum(int(area[p]) for p in mainland),
                mainland_centroid=[float(round(v, 6)) for v in centre],
                selected_state_centroid=[float(round(v, 6)) for v in candidates[selected]],
                detached_components=[sorted(group) for group in groups[1:]],
                candidate_squared_distances={str(i): float(round(distance(c, centre), 6)) for i, c in sorted(candidates.items())})


def derive():
    definitions, graph, centres, area, _ = topology()
    states = {}
    for path in sorted((MOD / 'history/states').glob('*.txt')):
        body = get(parse(path.read_text(encoding='utf-8-sig')), 'state')
        hist = get(body, 'history', [])
        provinces = [int(k) for k, _, _ in get(body, 'provinces', [])]
        states[int(get(body, 'id'))] = dict(owner=get(hist, 'owner'),
            land=[p for p in provinces if definitions[p]['land'] and p in centres])
    rows, preserved, dormant = {}, [], []
    for path in sorted((MOD / 'history/countries').glob('*.txt')):
        tag = path.name[:3]
        body = parse(path.read_text(encoding='utf-8-sig'))
        capital = int(get(body, 'capital'))
        owned = {i: row for i, row in states.items() if row['owner'] == tag}
        if not owned:
            dormant.append(tag)
            continue
        if tag not in INVALID:
            if states.get(capital, {}).get('owner') != tag:
                raise ValueError('Unreviewed foreign capital; inspect before extending the manifest: ' + tag)
            preserved.append(tag)
            continue
        if 171 in owned or tag == 'PLH':
            raise ValueError('Placeholder geography must not be inferred')
        if states.get(INVALID[tag], {}).get('owner') == tag:
            raise ValueError('Reviewed baseline capital ownership has changed: ' + tag)
        row = select(owned, graph, centres, area)
        if capital not in (INVALID[tag], row['capital']):
            raise ValueError('Capital changed outside the reviewed mapping: ' + tag)
        rows[tag] = dict(name=path.stem.split(' - ', 1)[-1],
                         history=path.relative_to(MOD).as_posix(), old_capital=INVALID[tag],
                         old_capital_owner=states.get(INVALID[tag], {}).get('owner'),
                         source_layer='provisional gameplay capital district on inherited geography',
                         owned_states=sorted(owned), **row)
    if set(rows) != set(INVALID):
        raise ValueError('Expected all fourteen reviewed active countries')
    inputs = {}
    for relative in ('map/provinces.bmp', 'map/definition.csv', 'map/adjacencies.csv'):
        inputs[relative] = hashlib.sha256((MOD / relative).read_bytes()).hexdigest()
    return dict(schema=1, verified_base=BASE,
        source_layer='Approved gameplay fallback, not sourced canonical city placement',
        rule='Preserve owned capitals. For a reviewed foreign capital: largest owned-land component by pixel area, area-weighted centre, nearest owned state centroid on that component, lowest state ID on a tie. Raster shared edges minus impassable links define connectivity.',
        geography_hashes=inputs, countries=rows, preserved_owned_capitals=preserved,
        dormant_histories_preserved=dormant,
        excluded_placeholder='PLH/state171 is preserved; no country tags, ownership, cores, population, province IDs, rasters or XXX strategic regions are changed.')


def outputs(manifest):
    result = {}
    for row in manifest['countries'].values():
        path = MOD / row['history']
        text = path.read_text(encoding='utf-8-sig')
        result[path] = repair(text, row['capital']).encode('utf-8')
    result[HERE / 'placements.json'] = (json.dumps(manifest, indent=2) + '\n').encode('utf-8')
    return result


def repair(text, capital):
    if len(CAPITAL.findall(text)) != 1:
        raise ValueError('Need exactly one root capital assignment')
    return CAPITAL.sub(lambda m: m.group(1) + str(capital) + m.group(2), text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    manifest = derive()
    changed = []
    for path, data in outputs(manifest).items():
        if args.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n', b'\n') != data:
                changed.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if changed:
        raise SystemExit('Capital outputs differ: ' + ', '.join(changed))
    print(f'World capitals: 14 reviewed repairs; {len(manifest["preserved_owned_capitals"])} owned capitals and {len(manifest["dormant_histories_preserved"])} dormant histories preserved; no native acceptance claim.')


if __name__ == '__main__':
    main()
