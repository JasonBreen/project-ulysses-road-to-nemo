"""Derive Anea placements from the inherited province raster, without changing it.

No names or geography are inferred as canon. The only adjacency used for a
railway is an actual shared pixel edge between owned land provinces.
"""
from collections import defaultdict, deque
from pathlib import Path
import csv, hashlib, json, sys
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import parse, get


def read_states():
    states = {}
    for path in sorted((MOD / 'history/states').glob('*.txt')):
        body = get(parse(path.read_text(encoding='utf-8-sig')), 'state')
        if body is None:
            continue
        owner = get(get(body, 'history', []), 'owner')
        if owner in ('EMM', 'EVA'):
            ident = int(get(body, 'id'))
            states[ident] = dict(path=path.relative_to(MOD).as_posix(), owner=owner,
                provinces=[int(k) for k, _, _ in get(body, 'provinces')],
                manpower=int(get(body, 'manpower')), body=body)
    return states


def topology():
    definitions = {}
    for row in csv.reader((MOD / 'map/definition.csv').read_text(encoding='utf-8-sig').splitlines(), delimiter=';'):
        if len(row) >= 8:
            i, r, g, b = map(int, row[:4])
            definitions[i] = dict(rgb=(r, g, b), land=row[4] == 'land', kind=row[4], coastal=row[5] == 'true')
    picture = np.asarray(Image.open(MOD / 'map/provinces.bmp').convert('RGB'), dtype=np.uint32)
    packed = picture[:, :, 0] * 65536 + picture[:, :, 1] * 256 + picture[:, :, 2]
    colors = np.array(sorted((d['rgb'][0] * 65536 + d['rgb'][1] * 256 + d['rgb'][2], i) for i, d in definitions.items()), dtype=np.uint32)
    index = np.searchsorted(colors[:, 0], packed)
    if not np.array_equal(colors[index, 0], packed):
        raise ValueError('Unknown province raster color')
    pixels = colors[index, 1]
    counts = np.bincount(pixels.ravel(), minlength=max(definitions) + 1)
    sums_x = np.bincount(pixels.ravel(), weights=np.tile(np.arange(pixels.shape[1]), pixels.shape[0]), minlength=len(counts))
    sums_y = np.bincount(pixels.ravel(), weights=np.repeat(np.arange(pixels.shape[0]), pixels.shape[1]), minlength=len(counts))
    centroids = {i: (float(sums_x[i] / counts[i]), float(sums_y[i] / counts[i])) for i in definitions if counts[i]}
    pairs = []
    for a, b in ((pixels[:, :-1], pixels[:, 1:]), (pixels[:-1, :], pixels[1:, :])):
        mask = a != b
        av, bv = a[mask], b[mask]
        pairs.append(np.minimum(av, bv).astype(np.uint64) * 65536 + np.maximum(av, bv))
    edges = np.unique(np.concatenate(pairs))
    graph = defaultdict(set)
    for packed_edge in edges:
        a, b = divmod(int(packed_edge), 65536)
        graph[a].add(b); graph[b].add(a)
    # Explicit impassable links override a visible shared edge.
    for row in csv.reader((MOD / 'map/adjacencies.csv').read_text().splitlines()[1:], delimiter=';'):
        if len(row) > 2 and row[2] == 'impassable':
            a, b = map(int, row[:2]); graph[a].discard(b); graph[b].discard(a)
    return definitions, graph, centroids, counts, pixels.shape


def components(provinces, graph):
    unseen = set(provinces); out = []
    while unseen:
        seed = min(unseen); unseen.remove(seed); group = {seed}; q = deque([seed])
        while q:
            for v in sorted(graph[q.popleft()] & unseen):
                unseen.remove(v); group.add(v); q.append(v)
        out.append(group)
    return sorted(out, key=lambda s: (-len(s), min(s)))


def shortest(start, goal, graph, allowed):
    q = deque([start]); parent = {start: None}
    while q:
        u = q.popleft()
        if u == goal:
            out = []
            while u is not None:
                out.append(u); u = parent[u]
            return out[::-1]
        for v in sorted(graph[u] & allowed):
            if v not in parent:
                parent[v] = u; q.append(v)
    raise ValueError(f'No owned-land path from {start} to {goal}')


def derive():
    states = read_states()
    defs, graph, centroids, counts, size = topology()
    airports = {int(k): int(v[0][0]) for k, _, v in parse((MOD / 'map/airports.txt').read_text()) if k.isdigit() and isinstance(v, list) and v}
    result = dict(schema=1, source_layer='provisional gameplay on inherited mod geography',
        base='cf8fec41abe5080b1af66eb86189b35c7af522f6',
        raster_sha256=hashlib.sha256((MOD / 'map/provinces.bmp').read_bytes()).hexdigest(),
        definition_sha256=hashlib.sha256((MOD / 'map/definition.csv').read_bytes()).hexdigest(),
        geometry_rule='Largest owned-land component by pixel area; area-weighted pixel centroid; capital state nearest state centroid; state ID breaks ties. EMM retains 154.',
        countries={}, map_baselines={})
    for relative in ('map/railways.txt', 'map/supply_nodes.txt'):
        # Railway/node files use a numeric row format; the native parser and
        # existing validator do not accept source comments in these files.
        raw = (MOD / relative).read_text().split('# BEGIN ANEA FOUNDATION')[0]
        existing_manifest = Path(__file__).with_name('foundation.json')
        if '# BEGIN ANEA FOUNDATION' not in (MOD / relative).read_text() and existing_manifest.exists():
            old = json.loads(existing_manifest.read_text()).get('map_baselines', {}).get(relative)
            if old:
                raw = '\n'.join(raw.splitlines()[:old['lines']])
        raw = raw.rstrip() + '\n'
        result['map_baselines'][relative] = dict(lines=len(raw.splitlines()), sha256=hashlib.sha256(raw.encode()).hexdigest())
    for tag in ('EMM', 'EVA'):
        owned = {p for s in states.values() if s['owner'] == tag for p in s['provinces'] if defs[p]['land']}
        groups = sorted(components(owned, graph), key=lambda g: (-sum(int(counts[p]) for p in g), min(g)))
        mainland = groups[0]
        centre = tuple(sum(centroids[p][n] * int(counts[p]) for p in mainland) / sum(int(counts[p]) for p in mainland) for n in (0, 1))
        state_centres = {}
        for i, s in states.items():
            valid = set(s['provinces']) & mainland
            if s['owner'] == tag and valid:
                state_centres[i] = tuple(sum(centroids[p][n] * int(counts[p]) for p in valid) / sum(int(counts[p]) for p in valid) for n in (0, 1))
        distance = lambda a, b: sum((a[n] - b[n]) ** 2 for n in (0, 1))
        cap = 154 if tag == 'EMM' else min(state_centres, key=lambda i: (distance(state_centres[i], centre), i))
        cap_prov = min(set(states[cap]['provinces']) & mainland, key=lambda p: (distance(centroids[p], state_centres[cap]), p))
        ports = [p for p in mainland if defs[p]['coastal'] and any(defs[n]['kind'] == 'sea' for n in graph[p])]
        port1 = min(ports, key=lambda p: (distance(centroids[p], centre), p))
        port2 = max(ports, key=lambda p: (distance(centroids[p], centroids[port1]), -p))
        # Four separated mainland industrial areas plus the two port states.
        industry = [cap]
        while len(industry) < 8:
            candidates = set(state_centres) - set(industry)
            industry.append(max(candidates, key=lambda i: (min(distance(state_centres[i], state_centres[j]) for j in industry), -i)))
        province_state = {p: i for i, s in states.items() for p in s['provinces']}
        port_states = [province_state[port1], province_state[port2]]
        # Route every selected industrial centre to the capital, with actual
        # supply hubs at four separated centres and both coastal terminals.
        hubs = [cap_prov]
        for i in industry[1:4]:
            hubs.append(min(set(states[i]['provinces']) & mainland, key=lambda p: (distance(centroids[p], state_centres[i]), p)))
        terminals = list(dict.fromkeys(hubs + [port1, port2] + [airports[i] for i in industry]))
        routes = [shortest(cap_prov, p, graph, mainland) for p in terminals if p != cap_prov]
        # Every airport chosen for a starting wing is a reachable state airport.
        air_states = [i for i in industry if airports[i] in mainland][:3]
        row = dict(capital=cap, capital_province=cap_prov, mainland_centroid=[round(x, 4) for x in centre],
            mainland_provinces=sorted(mainland), detached_components=[sorted(s) for s in groups[1:]],
            states=sorted(i for i, s in states.items() if s['owner'] == tag),
            provinces=sorted(owned), industry_states=industry, ports=[dict(province=p, state=province_state[p]) for p in (port1, port2)],
            air_states=air_states, airports={str(i): airports[i] for i in air_states},
            supply_hubs=list(dict.fromkeys(hubs + [port1, port2])), routes=routes,
            placements={}, baseline={})
        for i in row['states']:
            s = states[i]; c = state_centres.get(i)
            direction = 'Island' if c is None else ('Northern' if c[1] < centre[1] - 40 else 'Southern' if c[1] > centre[1] + 40 else 'Central')
            if c is not None:
                direction += ' Western' if c[0] < centre[0] - 60 else ' Eastern' if c[0] > centre[0] + 60 else ''
            name = ('Emmerian' if tag == 'EMM' else 'Estovakian') + (' Capital District' if i == cap else f' {direction} District {i}')
            row['placements'][str(i)] = dict(name=name, infrastructure=2 if c is not None else 1,
                civilian=0, military=0, dockyard=0, air_base=0, fuel_silo=1 if i == cap else 0, naval_bases={}, resources={})
            row['baseline'][str(i)] = dict(manpower=s['manpower'], provinces=s['provinces'], owner=tag,
                cores=[v for k, _, v in get(s['body'], 'history') if k == 'add_core_of'])
        for key, total in (('civilian', 24 if tag == 'EMM' else 20), ('military', 14 if tag == 'EMM' else 16)):
            for n in range(total):
                row['placements'][str(industry[n % len(industry)])][key] += 1
        for n in range(6 if tag == 'EMM' else 4):
            row['placements'][str(port_states[n % 2])]['dockyard'] += 1
        for i in air_states:
            row['placements'][str(i)]['air_base'] = 2
        for p in (port1, port2):
            row['placements'][str(province_state[p])]['naval_bases'][str(p)] = 3
        # A deliberately modest abstract industrial-resource baseline. This is
        # not a claim of deposits; shortages still require normal trade.
        for key, amount in (('steel', 24 if tag == 'EMM' else 20), ('aluminium', 12), ('oil', 12), ('tungsten', 4)):
            row['placements'][str(cap)]['resources'][key] = amount
        result['countries'][tag] = row
    return result


if __name__ == '__main__':
    manifest = Path(__file__).with_name('foundation.json')
    manifest.write_text(json.dumps(derive(), indent=2) + '\n', encoding='utf-8')
    print(manifest)
