"""Fail-closed offline interpreter for the shipped macro script subset.

This executes actual generated effects, not a second implementation of their
economic formulas. Decimal arithmetic and copied state are not native precision
or native save serialization evidence.
"""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[2];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from economy_script import parse, fields


@dataclass
class Country:
    tag:str
    identity:int
    variables:dict=field(default_factory=dict)
    flags:dict=field(default_factory=dict)
    modifiers:set=field(default_factory=set)
    equipment:dict=field(default_factory=dict)
    observables:dict=field(default_factory=dict)
    war:bool=False
    capitulated:bool=False
    ai:bool=False
    tech:bool=True


@dataclass
class State:
    ident:int
    owner:str
    controller:str
    variables:dict=field(default_factory=dict)


class World:
    def __init__(self,mode='full',new=True):
        self.mode=mode;self.today=date(1991,1,1).toordinal();self.globals=set();self.events=[]
        data=json.loads((ROOT/'tools/economy_v2/profiles.json').read_text())
        self.countries={r['tag']:Country(r['tag'],i+1) for i,r in enumerate(data['profiles'])}
        self.states={s['id']:State(s['id'],s['owner'],s['owner']) for s in data['states']}
        if new:
            for c in self.countries.values():c.flags['ac_macro_history_eligible']=None
        self.effects={};self.triggers={}
        for folder,library in [('common/scripted_effects',self.effects),('common/scripted_triggers',self.triggers)]:
            for path in sorted((MOD/folder).glob('ac_*.txt')):
                if path.name.startswith(('ac_macro','ac_economy')):
                    for key,_,body in parse(path.read_text(encoding='utf-8-sig')):
                        if key in library:raise ValueError('Duplicate owned symbol '+key)
                        library[key]=body
        self.actions=fields(parse((MOD/'common/on_actions/ac_macro_on_actions.txt').read_text()))['on_actions']

    def scope(self,key,context,root,previous):
        if key=='ROOT':return root
        if key=='PREV':return previous
        if key=='THIS':return context
        if key in self.countries:return self.countries[key]
        raise ValueError('Unknown scope '+key)

    def number(self,value,context,temp,root,previous):
        try:return D(str(value))
        except Exception:pass
        if value=='date':return D(self.today)
        if '.' in value:
            scope,variable=value.split('.',1)
            target=self.scope(scope,context,root,previous)
            if variable=='id':return D(target.identity)
            return target.variables.get(variable,D(0))
        if value in temp:return temp[value]
        if value.startswith(('ac_macro_','ac_econ_')):return context.variables.get(value,D(0))
        known={'num_of_controlled_factories','num_of_civilian_factories','num_of_military_factories','num_of_naval_factories',
               'deployed_army_manpower_k','deployed_navy_manpower_k','deployed_airforce_manpower_k','num_deployed_planes',
               'num_ships','num_ships_with_type@carrier','num_ships_with_type@submarine','total_equipment_produced_infantry'}
        if value in known:return D(str(context.observables.get(value,1 if value=='num_of_military_factories' else 0)))
        raise ValueError('Unknown numeric observable '+value)

    def trigger(self,nodes,context,temp=None,root=None,previous=None):
        temp={} if temp is None else temp;root=context if root is None else root
        answers=[]
        for key,op,value in nodes:
            if key in self.triggers:answer=self.trigger(self.triggers[key],context,temp,root,previous)==(value=='yes')
            elif key in ('OR','AND','NOT'):
                values=[self.trigger([row],context,temp,root,previous) for row in value]
                answer=any(values) if key=='OR' else all(values) if key=='AND' else not all(values)
            elif key=='always':answer=value=='yes'
            elif key=='date':
                b=date(*map(int,value.split('.'))).toordinal()
                answer={'<':self.today<b,'>':self.today>b,'=':self.today==b,'>=':self.today>=b,'<=':self.today<=b}[op]
            elif key=='has_game_rule':answer=fields(value)==dict(rule='ac_economy',option=self.mode)
            elif key=='has_country_flag':
                expires=context.flags.get(value,-1);answer=value in context.flags and (expires is None or expires>self.today)
            elif key=='has_global_flag':answer=value in self.globals
            elif key=='has_variable':answer=value in context.variables
            elif key=='has_dynamic_modifier':answer=fields(value)['modifier'] in context.modifiers
            elif key=='any_owned_state':answer=any(self.trigger(value,s,temp,root,context) for s in self.states.values() if s.owner==context.tag)
            elif key=='is_owned_by':answer=context.owner==self.scope(value,context,root,previous).tag
            elif key=='is_controlled_by':answer=context.controller==self.scope(value,context,root,previous).tag
            elif key in ('original_tag','tag'):answer=context.tag==value
            elif key in ('has_war','has_capitulated','is_ai','has_tech'):
                attr=dict(has_war='war',has_capitulated='capitulated',is_ai='ai',has_tech='tech')[key]
                answer=getattr(context,attr)==(value=='yes') if key!='has_tech' else context.tech
            elif key=='check_variable':
                if len(value)==1 and value[0][0]!='var':left,comparison,right=value[0]
                else:
                    data=fields(value);left=data['var'];right=data['value'];comparison=dict(equals='=',greater_than='>',less_than='<',greater_than_or_equals='>=',less_than_or_equals='<=')[data['compare']]
                a=self.number(left,context,temp,root,previous);b=self.number(right,context,temp,root,previous)
                answer={'=':a==b,'>':a>b,'<':a<b,'>=':a>=b,'<=':a<=b,'!=':a!=b}[comparison]
            elif key=='num_of_military_factories':
                a=self.number(key,context,temp,root,previous);b=D(value);answer=a>b if op=='>' else a==b
            else:raise ValueError('Unknown trigger '+key)
            answers.append(answer)
        return all(answers)

    def execute(self,nodes,context,temp=None,root=None,previous=None):
        temp={} if temp is None else temp;root=context if root is None else root;branch=None
        for key,op,value in nodes:
            if key in ('if','else_if','else'):
                if key=='if':branch=False
                elif branch is None:raise ValueError('Orphan branch')
                condition=key=='else' or self.trigger(next(v for k,_,v in value if k=='limit'),context,temp,root,previous)
                if not branch and condition:
                    self.execute([row for row in value if row[0]!='limit'],context,temp,root,previous);branch=True
                continue
            branch=None
            if key in self.effects:
                self.execute(self.effects[key],context,temp,root,previous)
            elif key in ('every_country','every_owned_state','every_controlled_state'):
                candidates=list(self.countries.values()) if key=='every_country' else [s for s in self.states.values() if (s.owner if key=='every_owned_state' else s.controller)==context.tag]
                condition=next((v for k,_,v in value if k=='limit'),[])
                for target in candidates:
                    if self.trigger(condition,target,temp,root,context):self.execute([row for row in value if row[0]!='limit'],target,temp,root,context)
            elif key.isdigit():
                state=self.states.get(int(key))
                if state:self.execute(value,state,temp,root,context)
            elif key in ('PREV','ROOT'):
                self.execute(value,self.scope(key,context,root,previous),temp,root,context)
            elif key in ('set_variable','add_to_variable','subtract_from_variable','multiply_variable','divide_variable',
                         'set_temp_variable','add_to_temp_variable','subtract_from_temp_variable','multiply_temp_variable','divide_temp_variable'):
                if len(value)!=1:raise ValueError('Expected one arithmetic assignment')
                variable,_,operand=value[0];target=context
                amount=self.number(operand,context,temp,root,previous)
                if '.' in variable:
                    scope,variable=variable.split('.',1);target=self.scope(scope,context,root,previous)
                if not variable.startswith(('ac_macro_','ac_econ_')):raise ValueError('Variable outside fiscal owner '+variable)
                store=temp if 'temp_variable' in key else target.variables
                before=store.get(variable,D(0))
                if key.startswith('set_'):store[variable]=amount
                elif key.startswith('add_'):store[variable]=before+amount
                elif key.startswith('subtract_'):store[variable]=before-amount
                elif key.startswith('multiply_'):store[variable]=before*amount
                else:
                    if amount==0:raise ValueError('Division by zero')
                    store[variable]=before/amount
            elif key=='clamp_variable':
                data=fields(value);name=data['var'];current=context.variables.get(name,D(0))
                if 'min' in data:current=max(current,self.number(data['min'],context,temp,root,previous))
                if 'max' in data:current=min(current,self.number(data['max'],context,temp,root,previous))
                context.variables[name]=current
            elif key in ('round_variable','round_temp_variable'):
                # Engine-supported integer rounding. Graph inputs are positive;
                # this offline model uses nearest with halves away from zero.
                target=temp if key=='round_temp_variable' else context.variables
                target[value]=target.get(value,D(0)).to_integral_value(rounding=ROUND_HALF_UP)
            elif key=='set_country_flag':
                if isinstance(value,list):
                    data=fields(value);context.flags[data['flag']]=self.today+int(data['days'])
                else:context.flags[value]=None
            elif key=='clr_country_flag':context.flags.pop(value,None)
            elif key=='set_global_flag':self.globals.add(value)
            elif key=='clr_global_flag':self.globals.discard(value)
            elif key=='clear_variable':context.variables.pop(value,None)
            elif key=='add_dynamic_modifier':context.modifiers.add(fields(value)['modifier'])
            elif key=='country_event':self.events.append((context.tag,fields(value)['id']))
            elif key=='custom_effect_tooltip':pass
            elif key=='add_equipment_to_stockpile':
                data=fields(value);context.equipment[data['type']]=context.equipment.get(data['type'],0)+int(data['amount'])
            else:raise ValueError('Unknown effect '+key)

    def run(self,name,tag,temp=None):self.execute(self.effects[name],self.countries[tag],temp)

    def action(self,name,tags=None):
        body=fields(fields(self.actions)[name])['effect']
        if name=='on_startup':self.execute(body,None)
        else:
            for tag in tags or self.countries:self.execute(body,self.countries[tag])

    def month(self,tag,year=1991,month=2):
        self.today=date(year,month,1).toordinal();self.action('on_monthly',[tag])
