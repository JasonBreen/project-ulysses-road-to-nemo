"""Offline Anea setup regressions, independent of campaign/aid implementation.

Set ULYSSES_GAME_ROOT or pass --reference for effective native tech/equipment
checks. Geometry, conservation, DLC parity and generated-output tests always run.
"""
import argparse, hashlib, json, os, subprocess, sys, unittest
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[0] / 'usea_expansion'))
from foundation_map import ROOT, MOD, topology, derive
from foundation import outputs, ARMY, COUNTRY
from script import parse, get, walk

ap = argparse.ArgumentParser(); ap.add_argument('--reference', default=os.environ.get('ULYSSES_GAME_ROOT')); args, tests = ap.parse_known_args()
REF = Path(args.reference) if args.reference else None
MANIFEST = json.loads((HERE / 'foundation.json').read_text())


def read(relative): return parse((MOD / relative).read_text(encoding='utf-8-sig'))


def evaluate_condition(nodes, dlcs):
    out = []
    for k, _, v in nodes:
        if k == 'has_dlc': out.append(v.strip('"') in dlcs)
        elif k.upper() == 'NOT': out.append(not evaluate_condition(v, dlcs))
        elif k.upper() == 'AND': out.append(evaluate_condition(v, dlcs))
        elif k.upper() == 'OR': out.append(any(evaluate_condition([n], dlcs) for n in v))
        else: raise AssertionError('Unhandled history condition: ' + k)
    return all(out)


def selected(nodes, dlcs):
    for k, op, v in nodes:
        if k == 'if':
            if evaluate_condition(get(v, 'limit'), dlcs):
                yield from selected([n for n in v if n[0] not in ('limit', 'else')], dlcs)
            else:
                yield from selected(get(v, 'else', []), dlcs)
        else: yield k, op, v


def tech_definitions():
    files = {}
    if REF:
        files.update({p.name: p for p in (REF / 'common/technologies').glob('*.txt')})
    files.update({p.name: p for p in (MOD / 'common/technologies').glob('*.txt')})
    result = {}
    for path in files.values():
        try: tree = parse(path.read_text(encoding='utf-8-sig'))
        except ValueError: continue
        for k, _, v in get(tree, 'technologies', []): result[k] = v
    return result


class FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defs, cls.graph, cls.centroids, cls.counts, cls.size = topology()
        cls.techs = tech_definitions()

    def test_generated_output_consistency(self):
        for relative, expected in outputs().items():
            self.assertEqual((MOD / relative).read_text(encoding='utf-8').replace('\r\n', '\n'), expected, relative)

    def test_reproducible_geometry_and_capital_rule(self):
        self.assertEqual(derive(), MANIFEST)
        self.assertEqual(MANIFEST['countries']['EMM']['capital'], 154)
        self.assertEqual(MANIFEST['countries']['EVA']['capital'], 124)

    def test_owned_capitals_and_preserved_territory_population(self):
        for tag, row in MANIFEST['countries'].items():
            self.assertIn(row['capital'], row['states'])
            capfile = next((MOD / 'history/states').glob(str(row['capital']) + '-*.txt'))
            hist = get(get(parse(capfile.read_text()), 'state'), 'history')
            points = {int(v[0][0]): int(v[1][0]) for k, _, v in hist if k == 'victory_points'}
            self.assertEqual(max(points, key=points.get), row['capital_province'])
            self.assertEqual(points[row['capital_province']], 20)
            self.assertEqual(get(get(hist, 'buildings'), 'fuel_silo'), '1')
            for ident, base in row['baseline'].items():
                path = next((MOD / 'history/states').glob(ident + '-*.txt'))
                state = get(parse(path.read_text()), 'state'); hist = get(state, 'history')
                self.assertEqual(get(hist, 'owner'), base['owner'])
                self.assertEqual([v for k, _, v in hist if k == 'add_core_of'], base['cores'])
                self.assertEqual(int(get(state, 'manpower')), base['manpower'])
                self.assertEqual([int(k) for k, _, _ in get(state, 'provinces')], base['provinces'])

    def test_industrial_budgets_and_building_capacity(self):
        categories = {'town': 4, 'city': 6, 'large_city': 8}
        for tag, expected in [('EMM', (24, 14, 6)), ('EVA', (20, 16, 4))]:
            totals = Counter()
            for ident in MANIFEST['countries'][tag]['states']:
                path = next((MOD / 'history/states').glob(str(ident) + '-*.txt'))
                state = get(parse(path.read_text()), 'state'); b = get(get(state, 'history'), 'buildings')
                for k in ('industrial_complex', 'arms_factory', 'dockyard'):
                    totals[k] += int(get(b, k, '0'))
                slots = sum(int(get(b, k, '0')) for k in ('industrial_complex', 'arms_factory', 'dockyard'))
                self.assertLessEqual(slots, categories[get(state, 'state_category')])
                self.assertGreaterEqual(int(get(b, 'infrastructure')), 1)
            self.assertEqual(tuple(totals[k] for k in ('industrial_complex', 'arms_factory', 'dockyard')), expected)

    def test_logistics_paths_reach_capital_and_never_leave_owned_land(self):
        for tag, row in MANIFEST['countries'].items():
            owned = set(row['provinces']); connected = {row['capital_province']}
            for route in row['routes']:
                self.assertEqual(route[0], row['capital_province'])
                self.assertTrue(set(route) <= owned)
                for a, b in zip(route, route[1:]): self.assertIn(b, self.graph[a])
                connected.update(route)
            for p in row['supply_hubs']: self.assertIn(p, connected)
            for p in row['airports'].values(): self.assertIn(p, connected)
            for p in row['ports']: self.assertIn(p['province'], connected)

    def test_coastal_ports_and_airfield_capacity(self):
        for tag, row in MANIFEST['countries'].items():
            for port in row['ports']:
                p = port['province']; self.assertIn(p, row['provinces'])
                self.assertTrue(self.defs[p]['coastal'])
                self.assertTrue(any(self.defs[n]['kind'] == 'sea' for n in self.graph[p]))
            for dlc in (False, True):
                oob = read(f'history/units/{tag}_anea_air' + ('_bba' if dlc else '') + '.txt')
                for state, _, wings in get(oob, 'air_wings'):
                    level = row['placements'][state]['air_base']
                    self.assertLessEqual(sum(int(get(v, 'amount')) for _, _, v in wings), level * 200)

    def test_native_logistics_rows_and_inherited_prefixes(self):
        for relative, base in MANIFEST['map_baselines'].items():
            lines = (MOD / relative).read_text().splitlines()
            original = '\n'.join(lines[:base['lines']]).rstrip() + '\n'
            self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), base['sha256'])
            for line in lines[base['lines']:]:
                self.assertTrue(all(x.isdigit() for x in line.split()))
                cells = list(map(int, line.split()))
                if relative.endswith('railways.txt'): self.assertEqual(cells[1], len(cells) - 2)
                else: self.assertEqual(len(cells), 2)

    def test_land_forces_start_supplied_and_use_own_templates(self):
        for tag, row in MANIFEST['countries'].items():
            oob = read(f'history/units/{tag}_anea_land.txt')
            templates = {get(v, 'name') for k, _, v in oob if k == 'division_template'}
            units = get(oob, 'units'); divisions = [v for k, _, v in units if k == 'division']
            self.assertEqual(len(divisions), 12 if tag == 'EMM' else 14)
            for div in divisions:
                self.assertIn(int(get(div, 'location')), row['supply_hubs'])
                self.assertIn(get(div, 'division_template'), templates)
                self.assertEqual(float(get(div, 'start_equipment_factor')), 1)

    def test_dlc_rosters_and_factories_are_mutually_exclusive_and_equivalent(self):
        for tag, row in MANIFEST['countries'].items():
            totals = []
            for bba in (False, True):
                for mtg in (False, True):
                    dlcs = ({'By Blood Alone'} if bba else set()) | ({'Man the Guns'} if mtg else set())
                    history = list(selected(read(f'history/countries/{tag} - {COUNTRY[tag]}.txt'), dlcs))
                    rosters = [v.strip('"') for k, _, v in history if k in ('set_oob', 'set_air_oob', 'set_naval_oob')]
                    self.assertEqual(len(rosters), 3)
                    self.assertEqual(sum('land' in p for p in rosters), 1)
                    air = read('history/units/' + next(p for p in rosters if '_air' in p) + '.txt')
                    navy = read('history/units/' + next(p for p in rosters if '_navy' in p) + '.txt')
                    air_amount = sum(int(get(v, 'amount')) for _, body in walk(air) for k, _, v in body if isinstance(v, list) and get(v, 'amount') is not None and get(v, 'owner') == tag)
                    ships = sum(k == 'ship' for k, _ in walk(navy))
                    totals.append((air_amount, ships))
                    factories = Counter()
                    for roster in rosters:
                        oob = read('history/units/' + roster + '.txt')
                        for k, body in walk(oob):
                            if k == 'add_equipment_production':
                                equipment = get(get(body, 'equipment'), 'type')
                                naval = equipment == 'convoy_1' or equipment.startswith('ship_hull_') or equipment in ('destroyer_2','light_cruiser_2','submarine_2')
                                factories['dockyard' if naval else 'military'] += int(get(body, 'requested_factories'))
                    self.assertEqual(factories['military'], 14 if tag == 'EMM' else 16)
                    self.assertEqual(factories['dockyard'], 6 if tag == 'EMM' else 4)
            self.assertEqual(len(set(totals)), 1)
            self.assertEqual(totals[0], (220 if tag == 'EMM' else 240, 9 if tag == 'EMM' else 8))

    def test_office_leaders_and_new_game_only_setup(self):
        for tag in ('EMM', 'EVA'):
            history = read(f'history/countries/{tag} - {COUNTRY[tag]}.txt')
            self.assertEqual([v for k, _, v in history if k == 'recruit_character'], [tag + '_ac_government_office'])
            self.assertIsNone(get(get(history, 'set_politics'), 'last_election'))
            self.assertEqual(get(history, 'set_fuel_ratio'), '1.0')
            self.assertEqual(get(history, 'set_convoys'), '120')
        for path in (MOD / 'common/on_actions').glob('*anea*'):
            text = path.read_text()
            for prohibited in ('set_oob', 'load_oob', 'add_equipment_production', 'add_building_construction', 'add_extra_state_shared_building_slots'):
                self.assertNotIn(prohibited, text)

    @unittest.skipUnless(REF and REF.exists(), 'Installed reference not supplied; effective native definitions remain a separate check')
    def test_effective_native_technology_and_equipment_unlocks(self):
        # Variant hulls and aircraft/land production must be granted by the
        # selected technology branch before the relevant roster is loaded.
        for tag in ('EMM', 'EVA'):
            for bba in (False, True):
                for mtg in (False, True):
                    dlcs = ({'By Blood Alone'} if bba else set()) | ({'Man the Guns'} if mtg else set())
                    enabled = {'convoy_1'}; modules = set(); variants = set()
                    for k, _, body in selected(read(f'history/countries/{tag} - {COUNTRY[tag]}.txt'), dlcs):
                        if k == 'set_technology':
                            for tech, _, value in body:
                                self.assertIn(tech, self.techs, (tag, tech))
                                definition = self.techs[tech]
                                for section, _, content in definition:
                                    if section == 'enable_equipments': enabled.update(n for n, _, _ in content)
                                    if section == 'enable_equipment_modules': modules.update(n for n, _, _ in content)
                        elif k == 'create_equipment_variant':
                            self.assertIn(get(body, 'type'), enabled)
                            for _, _, module in get(body, 'modules', []): self.assertIn(module, modules, (tag, module))
                            variants.add(get(body, 'name'))
                        elif k == 'add_equipment_to_stockpile':
                            self.assertIn(get(body, 'type'), enabled)
                            if get(body, 'variant_name'): self.assertIn(get(body, 'variant_name'), variants)
                        elif k in ('set_oob', 'set_air_oob', 'set_naval_oob'):
                            roster = read('history/units/' + body.strip('"') + '.txt')
                            for state, _, wings in get(roster, 'air_wings', []):
                                for equip, _, details in wings:
                                    self.assertIn(equip, enabled)
                                    if get(details, 'version_name'): self.assertIn(get(details, 'version_name'), variants)
                            for node, values in walk(roster):
                                if node == 'equipment':
                                    if get(values, 'type'):
                                        self.assertIn(get(values, 'type'), enabled)
                                    else:
                                        for equip, _, val in values:
                                            self.assertIn(equip, enabled)
                                            if get(val, 'version_name'): self.assertIn(get(val, 'version_name'), variants)


if __name__ == '__main__': unittest.main(argv=[sys.argv[0]] + tests, verbosity=2)
