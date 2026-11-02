"""Ordered effective aviation contracts; no shared-bridge or engine writes.

Unlike the existing start-worksheet helper, this reader preserves repeated
module limits and mission declarations and applies duplicate-archetype role
overrides. It is a bounded source interpreter, not native designer acceptance.
"""
from collections import Counter
from decimal import Decimal as D
import hashlib
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get

STATS=('build_cost_ic','fuel_consumption','manpower','maximum_speed','air_range','air_agility','air_attack','air_defence',
       'air_ground_attack','air_bombing','naval_strike_attack','naval_strike_targetting','surface_detection','sub_detection','air_superiority','reliability','weight','thrust')
REPEATED={'module_count_limit','allow_mission_type','forbid_mission_type'}


def tokens(value):return [value.strip('"')] if isinstance(value,str) else [k for k,_,_ in value or []]


class Primary:
    def __init__(self,reference):
        self.reference=Path(reference);self.sources={};self.files={};self.duplicates={}
        self.used={'equipment':set(),'modules':set()}
        self.equipment=self.catalog('common/units/equipment','equipments','duplicate_archetypes')
        self.modules=self.catalog('common/units/equipment/modules','equipment_modules')
        self.tech=self.catalog('common/technologies','technologies')

    def record(self,path):
        base=MOD if path.is_relative_to(MOD) else self.reference;prefix='mod/' if base==MOD else 'reference/'
        self.sources[prefix+path.relative_to(base).as_posix()]=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

    def catalog(self,relative,section,duplicates=None):
        paths={p.name:p for p in (self.reference/relative).glob('*.txt')};paths.update({p.name:p for p in (MOD/relative).glob('*.txt')})
        result={}
        for path in sorted(paths.values(),key=lambda p:(p.name.casefold(),p.name)):
            tree=parse(path.read_text(encoding='utf-8-sig'))
            for key,_,body in get(tree,section,[]):
                if isinstance(body,list):result[key]=body;self.files[(section,key)]=path
            if duplicates:
                for key,_,body in get(tree,duplicates,[]):
                    if isinstance(body,list):result[key]=body;self.duplicates[key]=body;self.files[(section,key)]=path
        return result

    def merge(self,base,body):
        result={**base}
        for key,_,value in body:
            if value=='inherit':
                if key not in result:raise ValueError('Missing inherited field '+key)
                continue
            if key in REPEATED:
                result[key]=[*result.get(key,[]),value]
            elif key=='module_slots':
                parent={k:v for k,_,v in result.get(key,[])};slots={}
                for name,_,definition in value:
                    if isinstance(definition,str):
                        alias=name if definition=='inherit' else definition
                        if alias not in slots and alias not in parent:raise ValueError('Missing slot inheritance '+name+':'+alias)
                        definition=slots.get(alias,parent.get(alias))
                    slots[name]=definition
                result[key]=[[k,'=',v] for k,v in slots.items()]
            elif key=='for_each':
                for field,_,operations in value:
                    if len(operations)!=1 or operations[0][0]!='set':raise ValueError('Uninspected duplicate stat patch: '+field)
                    result[field]=operations[0][2]
            else:result[key]=value
        return result

    def resolve(self,ident,family='equipment',chain=()):
        if ident in chain:raise ValueError('Cyclic aviation definition: '+ident)
        self.used[family].add(ident)
        definitions=self.equipment if family=='equipment' else self.modules
        section='equipments' if family=='equipment' else 'equipment_modules'
        if ident not in definitions:
            if family!='equipment':raise KeyError(ident)
            for root,body in self.duplicates.items():
                if ident.startswith(root+'_'):
                    parent=get(body,'archetype')+ident[len(root):]
                    if parent in definitions:
                        self.used[family].add(root)
                        self.record(self.files[(section,root)])
                        return self.merge(self.resolve(parent,family,chain+(ident,)),body)
            raise KeyError(ident)
        body=definitions[ident];self.record(self.files[(section,ident)])
        parent=get(body,'parent',get(body,'archetype'))
        return self.merge(self.resolve(parent,family,chain+(ident,)) if parent else {},body)

    @classmethod
    def from_capture(cls,catalog,equipment=None,modules=None):
        """Replay the captured effective native subset with current authored ASTs."""
        result=cls.__new__(cls);result.reference=None;result.sources={};result.used={'equipment':set(),'modules':set()}
        result.equipment={**catalog['equipment'],**(equipment or {})};result.modules={**catalog['modules'],**(modules or {})}
        result.duplicates=catalog['duplicates'];result.tech={}
        result.files={('equipments',key):Path('captured/'+key+'.txt') for key in result.equipment}
        result.files.update({('equipment_modules',key):Path('captured/'+key+'.txt') for key in result.modules})
        result.record=lambda path:None
        return result

    def design(self,ident,selected):
        body=self.resolve(ident);slots={k:v for k,_,v in body.get('module_slots',[])};counts=Counter();categories=Counter();roles=set();contracts={}
        modules={slot:self.resolve(module,'modules') for slot,module in selected.items() if module!='empty'}
        for slot,part in modules.items():
            module=selected[slot]
            if slot not in slots:raise ValueError('Undefined module slot: '+ident+':'+slot)
            allowed=set(tokens(get(slots[slot],'allowed_module_categories',[])));category=part['category']
            if category not in allowed:raise ValueError('Incompatible module category: '+ident+':'+slot+':'+module)
            counts[module]+=1;categories[category]+=1;roles.update(tokens(part.get('add_equipment_type',[])))
            contracts[slot]=dict(module=module,category=category,allowed_categories=sorted(allowed))
        missing=[slot for slot,definition in slots.items() if get(definition,'required')=='yes' and (slot not in selected or selected[slot]=='empty')]
        if missing:raise ValueError('Missing required aircraft slots: '+str(missing))
        for limit in body.get('module_count_limit',[]):
            module=get(limit,'module');category=get(limit,'category');tests=[(op,value) for key,op,value in limit if key=='count']
            if (module is None)==(category is None) or len(tests)!=1:raise ValueError('Uninspected aircraft module limit')
            count=counts[module] if module else categories[category];op,value=tests[0];bound=int(value)
            passed={'<':count<bound,'<=':count<=bound,'=':count==bound,'>':count>bound,'>=':count>=bound}.get(op)
            if passed is None:raise ValueError('Uninspected aircraft module count comparison '+str(op))
            if not passed:raise ValueError('Aircraft module count limit exceeded: '+str(module or category))
        blocked_roles=set()
        for part in modules.values():
            for category,_,equipment_type in part.get('forbid_equipment_type_exact_match_for_category',[]):
                if categories[category]:blocked_roles.add(equipment_type)
        required=set(tokens(body.get('allowed_types',[])))
        eligible=(roles&required)-blocked_roles
        if roles and not eligible:raise ValueError('No module-defined role allowed by aircraft archetype/classification exclusions')
        configured=self.stats(ident,selected);physical=configured['stats']
        if physical['thrust']<=0 or physical['weight']>physical['thrust']:raise ValueError('Insufficient aircraft thrust for configured weight')
        if physical['build_cost_ic']<=0 or physical['fuel_consumption']<=0 or physical['manpower']<=0:raise ValueError('Unfunded configured aircraft')
        if not configured['resources'] or any(v<=0 for v in configured['resources'].values()):raise ValueError('Non-positive configured aircraft material requirement')
        return dict(slots=contracts,module_count_limits=body.get('module_count_limit',[]),
            module_roles=sorted(roles),allowed_roles=sorted(required),blocked_module_roles=sorted(blocked_roles),effective_module_roles=sorted(eligible))

    def stats(self,ident,selected=None):
        body=self.resolve(ident);stats={k:D(str(body.get(k,0))) for k in STATS};resources=Counter({k:D(v) for k,_,v in body.get('resources',[])})
        for field in ('module_add_stats_multiplier','module_multiply_stats_multiplier','module_average_stats_multiplier'):
            if body.get(field):raise ValueError('Uninspected aircraft-specific module multiplier: '+field)
        multipliers=Counter();averages={};allow=set();forbid=set()
        for declaration in body.get('allow_mission_type',[]):allow.update(tokens(declaration))
        for declaration in body.get('forbid_mission_type',[]):forbid.update(tokens(declaration))
        for module in (selected or {}).values():
            if module=='empty':continue
            part=self.resolve(module,'modules')
            for declaration in part.get('allow_mission_type',[]):allow.update(tokens(declaration))
            for declaration in part.get('forbid_mission_type',[]):forbid.update(tokens(declaration))
            for key,_,value in part.get('add_stats',[]):
                if key not in stats:raise ValueError('Uninspected aircraft additive stat: '+key)
                stats[key]+=D(value)
            for key,_,value in part.get('multiply_stats',[]):
                if key not in stats:raise ValueError('Uninspected aircraft multiplicative stat: '+key)
                multipliers[key]+=D(value)
            for key,_,value in part.get('add_average_stats',[]):
                if key not in stats:raise ValueError('Uninspected averaged aircraft stat: '+key)
                averages.setdefault(key,[]).append(D(value))
            for key,_,value in part.get('add_resources',[])+part.get('build_cost_resources',[]):resources[key]+=D(value)
        for key,values in averages.items():
            if len(values)!=1:raise ValueError('Multiple averaged contributors require native aggregation acceptance: '+key)
            stats[key]+=values[0]
        stats={k:v*(1+multipliers[k]) for k,v in stats.items()}
        return dict(stats={k:float(v) for k,v in stats.items()},resources={k:float(v) for k,v in resources.items()},
            declared_missions=sorted(allow-forbid),forbidden_missions=sorted(forbid),
            average_contributors={k:[float(v) for v in values] for k,values in averages.items()})
