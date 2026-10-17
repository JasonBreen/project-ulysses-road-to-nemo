"""Migrate map/buildings.txt from the HOI4 1.14 layout to the 1.15+ spawn-point layout.

Reuses the mod's own coordinates:
  naval_base        -> naval_base_spawn (+ naval_headquarters, naval_supply_hub at the same spot)
  rocket_site       -> rocket_site_spawn
  nuclear_reactor   -> nuclear_reactor_spawn
  bunker (per land province) -> also special_project_facility_spawn
  air_base (per state)       -> also stronghold_network
Dams, locks and landmarks are tied to real-world geography and are intentionally not generated.
"""
import collections
import os
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')).replace(os.sep, '/')

P = REPO + '/mod/2985041246/map/buildings.txt'
raw = open(P, 'rb').read()
text = raw.decode('utf-8-sig')
nl = '\r\n' if '\r\n' in text else '\n'
lines = [l for l in text.split(nl) if l.strip()]
types = {l.split(';')[1] for l in lines}
assert 'naval_base_spawn' not in types, 'already migrated'

RENAME = {'naval_base': 'naval_base_spawn', 'rocket_site': 'rocket_site_spawn', 'nuclear_reactor': 'nuclear_reactor_spawn'}
COPY = {'naval_base': ['naval_headquarters', 'naval_supply_hub'],
        'bunker': ['special_project_facility_spawn'],
        'air_base': ['stronghold_network']}
out, extra = [], collections.defaultdict(list)
for l in lines:
    f = l.split(';')
    t = f[1]
    for c in COPY.get(t, []):
        extra[c].append(';'.join([f[0], c] + f[2:]))
    if t in RENAME:
        f[1] = RENAME[t]
    out.append(';'.join(f))
for c in ['naval_headquarters', 'naval_supply_hub', 'special_project_facility_spawn', 'stronghold_network']:
    out.extend(extra[c])
open(P, 'wb').write(nl.join(out).encode('utf-8') + nl.encode())
print(collections.Counter(l.split(';')[1] for l in out))

