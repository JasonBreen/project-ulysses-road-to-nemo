"""Read-only effective primary equipment, technology and unit definitions."""
from collections import Counter
import hashlib
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import parse, get


class Engine:
    def __init__(self, reference):
        self.reference = Path(reference); self.used = {}
        self.equipment, self.eq_files = self.catalog('common/units/equipment', 'equipments', 'duplicate_archetypes')
        self.modules, self.module_files = self.catalog('common/units/equipment/modules', 'equipment_modules')
        self.units, self.unit_files = self.catalog('common/units', 'sub_units')
        self.tech, self.tech_files = self.catalog('common/technologies', 'technologies')
        self.eq_unlocks = {}; self.module_unlocks = {}; self.unit_unlocks = {}
        for ident, body in self.tech.items():
            for section, _, entries in body:
                target = {'enable_equipments': self.eq_unlocks, 'enable_equipment_modules': self.module_unlocks,
                          'enable_subunits': self.unit_unlocks}.get(section)
                if target is not None:
                    for name, _, _ in entries:
                        target.setdefault(name, []).append(ident)
        self.defines = self.read_defines()

    def record(self, path):
        layer = 'mod' if path.is_relative_to(MOD) else 'reference'
        base = MOD if layer == 'mod' else self.reference
        self.used[layer + '/' + path.relative_to(base).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()

    def catalog(self, relative, section, extra=None):
        paths = {p.name: p for p in (self.reference / relative).glob('*.txt')}
        paths.update({p.name: p for p in (MOD / relative).glob('*.txt')})
        result = {}; files = {}
        for path in sorted(paths.values(), key=lambda p: (p.name.casefold(), p.name)):
            tree = parse(path.read_text(encoding='utf-8-sig'))
            entries = get(tree, section, []) + (get(tree, extra, []) if extra else [])
            for key, _, body in entries:
                if isinstance(body, list):
                    result[key] = body; files[key] = path
        return result, files

    def resolve(self, ident, definitions, files, chain=()):
        if ident in chain:
            raise ValueError('Cyclic primary definition: ' + ident)
        if ident not in definitions and definitions is self.equipment:
            # Designer role duplicates are declared by duplicate_archetypes;
            # concrete equipment inherits the matching numbered base airframe.
            for root, body in self.equipment.items():
                if ident.startswith(root + '_') and get(body, 'archetype'):
                    base = get(body, 'archetype') + ident[len(root):]
                    if base in definitions:
                        return self.resolve(base, definitions, files, chain + (ident,))
        body = definitions[ident]; self.record(files[ident])
        parent = get(body, 'parent', get(body, 'archetype'))
        values = self.resolve(parent, definitions, files, chain + (ident,)) if parent else {}
        values.update({key: value for key, _, value in body})
        return values

    def stats(self, ident, modules=()):
        body = self.resolve(ident, self.equipment, self.eq_files)
        values = {k: float(body.get(k, 0)) for k in ('build_cost_ic', 'fuel_consumption', 'manpower')}
        resources = {k: float(v) for k, _, v in body.get('resources', [])}; multipliers = Counter()
        for module in modules:
            part = self.resolve(module, self.modules, self.module_files)
            for key, _, value in part.get('add_stats', []):
                if key in values:
                    values[key] += float(value)
            for key, _, value in part.get('multiply_stats', []):
                if key in values:
                    multipliers[key] += float(value)
            for key, _, value in part.get('add_resources', []):
                resources[key] = resources.get(key, 0) + float(value)
        return {**{k: v * (1 + multipliers[k]) for k, v in values.items()}, 'resources': resources}

    def unlock(self, ident, mapping):
        options = mapping.get(ident, [])
        if not options:
            if ident == 'convoy_1':
                return None
            raise ValueError('No effective primary technology unlock: ' + ident)
        def key(tech):
            year = get(self.tech[tech], 'start_year', '0')
            try:
                year = int(float(year))
            except ValueError:
                year = 0
            return year, tech
        selected = min(options, key=key); self.record(self.tech_files[selected])
        return selected

    def equipment_tech(self, ident):
        return self.unlock(ident, self.eq_unlocks)

    def module_tech(self, ident):
        return self.unlock(ident, self.module_unlocks)

    def unit(self, ident):
        return self.resolve(ident, self.units, self.unit_files)

    def read_defines(self):
        path = self.reference / 'common/defines/00_defines.lua'; self.record(path)
        raw = path.read_text(encoding='utf-8-sig'); result = {}
        for section, names in {'NCountry': ['BASE_FUEL_GAIN_PER_OIL', 'BASE_FUEL_GAIN', 'BASE_FUEL_CAPACITY'],
                               'NProduction': ['BASE_FACTORY_SPEED_MIL', 'BASE_FACTORY_SPEED_NAV'],
                               'NBuildings': ['INFRASTRUCTURE_RESOURCE_BONUS', 'SUPPLY_PORT_LEVEL_THROUGHPUT'],
                               'NAir': ['FUEL_COST_MULT'], 'NNavy': ['FUEL_COST_MULT', 'IN_COMBAT_FUEL_COST'],
                               'NMilitary': ['ARMY_FUEL_COST_MULT']}.items():
            region = raw.split(section + ' = {', 1)[1].split('\n}', 1)[0]
            for name in names:
                result[section + '.' + name] = float(re.search(r'^\s*' + name + r'\s*=\s*([\d.]+)', region, re.M)[1])
        for path in sorted((MOD / 'common/defines').glob('*.lua')):
            self.record(path); text = path.read_text(encoding='utf-8-sig')
            for name in result:
                matches = re.findall(r'NDefines\.' + re.escape(name) + r'\s*=\s*([\d.]+)', text)
                if matches:
                    result[name] = float(matches[-1])
        return result
