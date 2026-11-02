"""Ordered naval source replay with explicit once-only default composition."""
from collections import Counter
from decimal import Decimal as D
from pathlib import Path
import importlib.util
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
spec=importlib.util.spec_from_file_location('naval_ordered_inheritance',ROOT/'tools/air_program/air_primary.py')
ordered=importlib.util.module_from_spec(spec);spec.loader.exec_module(ordered)
Ordered=ordered.Primary;tokens=ordered.tokens
from script import get

STATS=('build_cost_ic','fuel_consumption','manpower','naval_speed','naval_range','max_strength','reliability','surface_detection','sub_detection',
       'surface_visibility','sub_visibility','lg_attack','hg_attack','lg_armor_piercing','hg_armor_piercing','torpedo_attack','sub_attack','anti_air_attack',
       'armor_value','carrier_size','carrier_surface_detection','carrier_sub_detection','naval_dominance_factor','naval_weather_penalty_factor','naval_torpedo_hit_chance_factor')

class Primary(Ordered):
    def stats(self,ident,selected=None):
        body=self.resolve(ident)
        # A complete ship is still a native default-module recipe. Never bake
        # its default contributions and then add its modules a second time.
        selected=dict((k,v) for k,_,v in body.get('default_modules',[])) if selected is None else selected
        stats={k:D(str(body.get(k,0))) for k in STATS};resources=Counter({k:D(v) for k,_,v in body.get('resources',[])})
        for field in ('module_add_stats_multiplier','module_multiply_stats_multiplier','module_average_stats_multiplier'):
            if body.get(field):raise ValueError('Uninspected naval hull multiplier: '+field)
        types=set(tokens(body.get('type',[])));multipliers=Counter();averages={};crew=D(0)
        for module in selected.values():
            if module=='empty':continue
            part=self.resolve(module,'modules');types.update(tokens(part.get('add_equipment_type',[])))
            crew+=D(str(part.get('manpower',0))) # Native deck manpower is outside add_stats.
            for key,_,value in part.get('add_stats',[]):
                if key not in stats:raise ValueError('Uninspected naval additive stat: '+key)
                stats[key]+=D(value)
            for key,_,value in part.get('multiply_stats',[]):
                if key not in stats:raise ValueError('Uninspected naval multiplicative stat: '+key)
                multipliers[key]+=D(value)
            for key,_,value in part.get('add_average_stats',[]):
                if key not in stats:raise ValueError('Uninspected naval averaged stat: '+key)
                averages.setdefault(key,[]).append(D(value))
            for key,_,value in part.get('add_resources',[])+part.get('build_cost_resources',[]):resources[key]+=D(value)
        for key,values in averages.items():
            if len(values)!=1:raise ValueError('Multiple averaged naval contributors require native acceptance: '+key)
            stats[key]+=values[0]
        stats['manpower']+=crew;stats={k:v*(1+multipliers[k]) for k,v in stats.items()}
        # Native heavy batteries promote cruisers from screening to capital role.
        if 'capital_ship' in types:types.discard('screen_ship')
        return dict(stats={k:float(v) for k,v in stats.items()},resources={k:float(v) for k,v in resources.items()},
            effective_types=sorted(types),selected_modules=selected,external_module_crew=float(crew),
            average_contributors={k:[float(v) for v in values] for k,values in averages.items()})

    def design(self,ident,selected=None,complete=False):
        body=self.resolve(ident);slots={k:v for k,_,v in body.get('module_slots',[])}
        defaults={k:v for k,_,v in body.get('default_modules',[])};selected=defaults if selected is None else selected
        if complete and set(defaults)!=set(slots):raise ValueError('Complete naval default slot coverage differs from effective slots')
        counts=Counter();categories=Counter();contracts={}
        for slot,module in selected.items():
            if slot not in slots:raise ValueError('Undefined naval module slot: '+slot)
            if module=='empty':continue
            part=self.resolve(module,'modules');category=part['category'];allowed=set(tokens(get(slots[slot],'allowed_module_categories',[])))
            if category not in allowed:raise ValueError('Incompatible naval module category: '+slot+':'+module)
            counts[module]+=1;categories[category]+=1;contracts[slot]=dict(module=module,category=category,allowed_categories=sorted(allowed))
        missing=[s for s,b in slots.items() if get(b,'required')=='yes' and selected.get(s,'empty')=='empty']
        if missing:raise ValueError('Missing required naval slots: '+str(missing))
        for limit in body.get('module_count_limit',[]):
            module=get(limit,'module');category=get(limit,'category');tests=[(op,v) for k,op,v in limit if k=='count']
            if (module is None)==(category is None) or len(tests)!=1:raise ValueError('Uninspected naval count limit')
            n=counts[module] if module else categories[category];op,v=tests[0];v=int(v)
            if not {'<':n<v,'<=':n<=v,'=':n==v,'>':n>v,'>=':n>=v}.get(op,False):raise ValueError('Naval module count limit exceeded: '+str(module or category))
        physical=self.stats(ident,selected)
        if any(physical['stats'][k]<=0 for k in ('build_cost_ic','fuel_consumption','manpower','naval_speed','naval_range','max_strength')):raise ValueError('Unfunded or inoperable naval design')
        if not physical['resources'] or any(v<=0 for v in physical['resources'].values()):raise ValueError('Non-positive naval material requirement')
        return dict(slots=contracts,all_slots=sorted(slots),module_count_limits=body.get('module_count_limit',[]),**physical)
