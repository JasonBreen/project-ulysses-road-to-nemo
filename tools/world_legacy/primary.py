"""Read-only effective equipment facts; no installed pixels or payload imports."""
from pathlib import Path
import copy
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import parse, get


class Primary:
    def __init__(self, reference):
        self.reference = Path(reference)
        self.sources = {}
        self.equipment = self.catalog('common/units/equipment', ('equipments', 'duplicate_archetypes'))
        self.modules = self.catalog('common/units/equipment/modules', ('equipment_modules',))
        self.tech = self.catalog('common/technologies', ('technologies',))
        self.unlocks = {'equipment': {}, 'modules': {}}
        for ident, body in self.tech.items():
            for key, _, entries in body:
                family = {'enable_equipments': 'equipment', 'enable_equipment_modules': 'modules'}.get(key)
                if family:
                    for item, _, _ in entries:
                        self.unlocks[family].setdefault(item, []).append(ident)

    def catalog(self, relative, sections):
        paths = {p.name: p for p in (self.reference / relative).glob('*.txt')}
        paths.update({p.name: p for p in (MOD / relative).glob('*.txt')})
        output = {}
        for path in sorted(paths.values()):
            layer = 'mod' if path.is_relative_to(MOD) else 'reference'
            base = MOD if layer == 'mod' else self.reference
            key = layer + '/' + path.relative_to(base).as_posix()
            self.sources[key] = hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
            tree = parse(path.read_text(encoding='utf-8-sig'))
            for section in sections:
                for ident, _, body in get(tree, section, []):
                    if isinstance(body, list):
                        output[ident] = body
        return output

    def resolve(self, ident, family='equipment', seen=()):
        if ident in seen:
            raise ValueError('Definition cycle ' + ident)
        definitions = getattr(self, family)
        if ident not in definitions:
            for prefix, body in definitions.items():
                if ident.startswith(prefix + '_') and get(body, 'archetype'):
                    target = get(body, 'archetype') + ident[len(prefix):]
                    if target in definitions:
                        return self.resolve(target, family, seen + (ident,))
            raise KeyError(ident)
        body = definitions[ident]
        parent = get(body, 'parent', get(body, 'archetype'))
        result = self.resolve(parent, family, seen + (ident,)) if parent else {}
        for key, _, value in body:
            if value == 'inherit':
                continue
            if key == 'module_slots' and isinstance(value, list):
                inherited = {k: v for k, op, v in result.get(key, [])}
                resolved = {}
                for name, op, entry in value:
                    if entry == 'inherit':
                        if name not in inherited:raise ValueError('Unknown inherited slot '+ident+':'+name)
                        entry=inherited[name]
                    elif isinstance(entry,str):
                        if entry not in resolved and entry not in inherited:
                            raise ValueError('Unknown module-slot alias ' + ident + ':' + entry)
                        entry=resolved.get(entry,inherited.get(entry))
                    resolved[name]=copy.deepcopy(entry)
                result[key] = [[k,'=',v] for k,v in resolved.items()]
            else:
                result[key] = value
        return result

    def unlock(self, ident, family):
        options = self.unlocks[family].get(ident, [])
        if not options:
            return None
        return min(options, key=lambda key: (float(get(self.tech[key], 'start_year', '0')), key))

    def equipment_row(self, ident):
        body = self.resolve(ident)
        slots = {key: dict(required=get(entry, 'required', 'no'),
                          categories=[k for k, _, _ in get(entry, 'allowed_module_categories', [])],
                          allowed_modules=[k for k,_,_ in get(entry,'allowed_modules',[])])
                 for key, _, entry in body.get('module_slots', []) if isinstance(entry, list)}
        missions = body.get('allow_mission_type', [])
        return dict(technology=self.unlock(ident, 'equipment'),
                    resources={k: float(v) for k, _, v in body.get('resources', [])},
                    build_cost_ic=float(body.get('build_cost_ic', '0')),
                    fuel_consumption=float(body.get('fuel_consumption', '0')),
                    can_be_produced=body.get('can_be_produced'),
                    module_slots=slots,
                    default_modules={k:v for k,_,v in body.get('default_modules',[])},
                    allowed_missions=[k for k, _, _ in missions] if isinstance(missions, list) else missions)

    def module_row(self, ident):
        body = self.resolve(ident, 'modules')
        return dict(technology=self.unlock(ident, 'modules'), category=body.get('category'),
                    add_resources={k: float(v) for k, _, v in body.get('add_resources', [])},
                    add_stats={k: float(v) for k, _, v in body.get('add_stats', [])},
                    multiply_stats={k: float(v) for k, _, v in body.get('multiply_stats', [])},
                    build_cost_resources={k:float(v) for k,_,v in body.get('build_cost_resources',[])},
                    allowed_module_categories={k:[c for c,_,_ in v] for k,_,v in body.get('allowed_module_categories',[])})
