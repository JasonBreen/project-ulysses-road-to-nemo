"""Actual-source release adapter over the real P1 fiscal/institution interpreter.

Only native observations/territorial, force-transfer and event syntax are
supplied here. No fiscal arithmetic, quote, settlement or transaction effect is
replaced. Fixtures use deterministic homogeneous transfers; native random unit
selection, controller updates, queue timing and serialization remain untested.
"""
import copy
from decimal import Decimal as D,ROUND_FLOOR
import importlib.util
import json
from pathlib import Path
import sys
from collections import Counter

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/economy_v2'),str(ROOT/'tools/usea_expansion')]
spec=importlib.util.spec_from_file_location('release_real_shared_owners',ROOT/'tools/Test-SharedSystems.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
from economy_script import parse,fields


def get(nodes,key,default=None):return next((v for k,_,v in nodes if k==key),default)
def walk(nodes):
    for key,_,value in nodes:
        yield key,value
        if isinstance(value,list):yield from walk(value)


class World(shared.World):
    def __init__(self,mode='full',new=True,dlcs=()):
        super().__init__(mode,new);self.dlcs=set(dlcs);self.from_country=None;self.external_exists=set();self.province_states={};self.province_controllers={};self.capitals={};self.armies={tag:0 for tag in self.countries};self.fuel={tag:D(0) for tag in self.countries};self.native_log=[]
        self.core_states={};self.state_flags={};self.buildings={};self.free_slots={};self.character_ids={tag:set() for tag in self.countries};self.research={tag:set() for tag in self.countries}
        self.resource_balances={tag:Counter() for tag in self.countries};self.production={tag:[] for tag in self.countries};self.variants={tag:{} for tag in self.countries}
        self.railways=[]
        self.railway_levels={}
        for line in (MOD/'map/railways.txt').read_text().splitlines():
            numbers=list(map(int,line.split()));route=numbers[2:]
            for a,b in zip(route,route[1:]):self.railway_levels[tuple(sorted((a,b)))]=max(numbers[0],self.railway_levels.get(tuple(sorted((a,b))),0))
        key='bba'+str(int('By Blood Alone' in self.dlcs))+'_mtg'+str(int('Man the Guns' in self.dlcs))
        self.recipes=json.loads((HERE/'physical_contract.json').read_text())['cases'][key]
        groups=get(parse((MOD/'common/ideologies/00_ideologies.txt').read_text(encoding='utf-8-sig')),'ideologies');self.ideology_groups={sub:group for group,_,body in groups for sub,_,_ in get(body,'types',[])}
        self.character_roles={};self.ruling_leader={tag:None for tag in self.countries}
        for path in (MOD/'common/characters').glob('*.txt'):
            for kind,_,entries in parse(path.read_text(encoding='utf-8-sig')):
                if kind!='characters':continue
                for ident,_,body in entries:self.character_roles[ident]={self.ideology_groups[get(role,'ideology')] for key,_,role in body if key=='country_leader'}
        for path in (MOD/'history/states').glob('*.txt'):
            state=get(parse(path.read_text(encoding='utf-8-sig')),'state');ident=int(get(state,'id'));history=get(state,'history')
            self.province_states.update({int(k):ident for k,_,_ in get(state,'provinces')});self.core_states[ident]={v for k,_,v in history if k=='add_core_of'}
            self.state_flags[ident]=set();self.buildings[ident]={k:int(v) for k,_,v in get(history,'buildings',[]) if isinstance(v,str)};self.free_slots[ident]=10
        for path in (MOD/'history/countries').glob('*.txt'):
            self.capitals[path.name[:3]]=int(get(parse(path.read_text(encoding='utf-8-sig')),'capital'))
        for folder,library in [('scripted_effects',self.effects),('scripted_triggers',self.triggers)]:
            for filename in ('ac_release_foundations.txt','ac_release_maintenance.txt')+ (('ac_release_governments.txt',) if folder=='scripted_effects' else ()):
                for key,_,value in parse((MOD/'common'/folder/filename).read_text()):
                    if key in library:raise ValueError('Duplicate release/shared owner '+key)
                    library[key]=value
        self.release_actions=fields(parse((MOD/'common/on_actions/ac_release_foundations.txt').read_text()))['on_actions']
        self.event_definitions={}
        for name in ('AWWNB.txt','Recta.txt','South_Belka.txt','Belka.txt','ac_release_projects.txt'):
            for kind,_,value in parse((MOD/'events'/name).read_text(encoding='utf-8-sig')):
                if kind=='country_event':self.event_definitions[get(value,'id')]=value

    def scope(self,key,context,root,previous):
        if key=='FROM':
            if self.from_country is None:raise ValueError('Missing actual FROM observation')
            return self.from_country
        return super().scope(key,context,root,previous)

    def number(self,value,context,temp,root,previous):
        if isinstance(value,str) and value.startswith('ac_release_'):return temp.get(value,context.variables.get(value,D(0)))
        return super().number(value,context,temp,root,previous)

    def controller(self,province):return self.province_controllers.get(province,self.states[self.province_states[province]].controller)

    def trigger(self,nodes,context,temp=None,root=None,previous=None):
        temp={} if temp is None else temp;root=context if root is None else root;answers=[]
        for key,op,value in nodes:
            if key=='country_exists':answer=value in self.external_exists or any(s.owner==value for s in self.states.values())
            elif key in self.countries or key=='FROM':answer=self.trigger(value,self.scope(key,context,root,previous),temp,root,context)
            elif key=='owns_state':answer=self.states[int(value)].owner==context.tag
            elif key=='controls_province':answer=self.controller(int(value))==context.tag
            elif key=='state':answer=context.ident==int(value)
            elif key=='all_owned_state':answer=all(self.trigger(value,s,temp,root,context) for s in self.states.values() if s.owner==context.tag)
            elif key=='capital_scope':answer=self.trigger(value,self.states[self.capitals[context.tag]],temp,root,context)
            elif key=='has_dlc':answer=value in self.dlcs
            elif key=='has_character':answer=value in self.character_ids[context.tag]
            elif key=='has_country_leader':answer=self.ruling_leader[context.tag]==get(value,'character')
            elif key=='any_country':answer=any(self.trigger(value,c,temp,root,context) for c in self.countries.values())
            elif key=='has_tech':answer=value in self.research[context.tag]
            elif key=='custom_trigger_tooltip':answer=self.trigger([n for n in value if n[0]!='tooltip'],context,temp,root,previous)
            elif key=='has_state_flag':answer=value in self.state_flags[context.ident]
            elif key=='is_core_of':answer=self.scope(value,context,root,previous).tag in self.core_states[context.ident]
            elif key=='is_fully_controlled_by':answer=all(self.controller(p)==self.scope(value,context,root,previous).tag for p,s in self.province_states.items() if s==context.ident)
            elif key=='free_building_slots':answer=self.free_slots[context.ident]>int(get(value,'size'))
            elif key in ('dockyard','arms_factory','industrial_complex'):answer=self.buildings[context.ident].get(key,0)>int(value)
            elif key=='num_of_naval_factories':answer=self.number(key,context,temp,root,previous)>D(value)
            elif key=='has_railway_connection':
                path=[int(k) for k,_,_ in get(value,'path')];answer=all(self.railway_levels.get(tuple(sorted((a,b))),0)>0 for a,b in zip(path,path[1:]))
            elif key=='has_resources_in_country':
                resource=get(value,'resource');bound=next(n for n in value if n[0]=='amount');a=D(self.resource_balances[context.tag][resource]);b=D(bound[2]);answer=a>=b if bound[1]=='>=' else a>b
            else:answer=super().trigger([(key,op,value)],context,temp,root,previous)
            answers.append(answer)
        return all(answers)

    def execute(self,nodes,context,temp=None,root=None,previous=None):
        temp={} if temp is None else temp;root=context if root is None else root;branch=None
        for key,op,value in nodes:
            if key=='if':
                branch=self.trigger(get(value,'limit',[]),context,temp,root,previous)
                # A body's sibling `if ... else` belongs to that inner chain.
                # Only an otherwise orphaned else is the legacy nested form
                # attached to this enclosing if. Never execute an inner else
                # merely because the enclosing guard failed.
                commands=[];alternatives=[];previous_branch=False
                for node in [n for n in value if n[0]!='limit']:
                    if node[0] in ('else','else_if') and not previous_branch:alternatives.append(node)
                    else:commands.append(node)
                    previous_branch=node[0] in ('if','else_if','else')
                if branch:self.execute(commands,context,temp,root,previous)
                else:
                    for kind,_,body in alternatives:
                        if kind=='else' or self.trigger(get(body,'limit',[]),context,temp,root,previous):
                            self.execute([n for n in body if n[0]!='limit'],context,temp,root,previous);branch=True;break
                continue
            if key in ('else','else_if'):
                if branch is None:raise ValueError('Orphan release/shared branch')
                if not branch and (key=='else' or self.trigger(get(value,'limit',[]),context,temp,root,previous)):
                    self.execute([n for n in value if n[0]!='limit'],context,temp,root,previous);branch=True
                continue
            branch=None
            if key in self.countries or key in ('ROOT','PREV','FROM'):
                self.execute(value,self.scope(key,context,root,previous),temp,root,context)
            elif key=='capital_scope':self.execute(value,self.states[self.capitals[context.tag]],temp,root,context)
            elif key=='every_state':
                for state in self.states.values():
                    if self.trigger(get(value,'limit',[]),state,temp,root,context):self.execute([n for n in value if n[0]!='limit'],state,temp,root,context)
            elif key in ('set_variable','add_to_variable','subtract_from_variable','set_temp_variable','subtract_from_temp_variable') and value[0][0].startswith('ac_release_'):
                name,_,operand=value[0];amount=self.number(operand,context,temp,root,previous);store=temp if 'temp_variable' in key else context.variables
                store[name]=(amount if key.startswith('set_') else store.get(name,D(0))+amount*(1 if key.startswith('add_') else -1))
            elif key=='set_state_flag':self.state_flags[context.ident].add(value)
            elif key=='clr_state_flag':self.state_flags[context.ident].discard(value)
            elif key=='add_building_construction':
                kind=get(value,'type');amount=int(get(value,'level'));self.buildings[context.ident][kind]=self.buildings[context.ident].get(kind,0)+amount;self.free_slots[context.ident]-=amount
                self.native_log.append(('add_building_construction',context.ident,kind,amount))
            elif key=='create_equipment_variant':self.variants[context.tag][get(value,'name').strip('"')]=copy.deepcopy(value)
            elif key=='add_equipment_production':
                equipment=get(value,'equipment');kind=get(equipment,'type');version=get(equipment,'version_name')
                recipes=[row for row in self.recipes.values() if row['equipment']==kind]
                if not recipes:raise ValueError('Unresolved release production recipe: '+kind)
                if not any(set(row['technologies'])<=self.research[context.tag] for row in recipes):raise ValueError('Release production before required research: '+kind)
                if version and version.strip('"') not in self.variants[context.tag]:raise ValueError('Release production before selected variant: '+version)
                self.production[context.tag].append(copy.deepcopy(value))
            elif key=='add_country_leader_role':
                ident=get(value,'character');group=self.ideology_groups[get(get(value,'country_leader'),'ideology')]
                assert ident in self.character_ids[context.tag],'Leader role assigned to an unrecruited character'
                self.character_roles[ident].add(group)
                if get(value,'promote_leader')=='yes' and group==context.government:self.ruling_leader[context.tag]=ident
                self.native_log.append((key,context.tag,copy.deepcopy(value)))
            elif key=='promote_character':
                ident=get(value,'character') if isinstance(value,list) else value;group=self.ideology_groups[get(value,'ideology')] if isinstance(value,list) else context.government
                assert ident in self.character_ids[context.tag] and group in self.character_roles[ident],'Unavailable promoted character/role'
                if group==context.government:self.ruling_leader[context.tag]=ident
                self.native_log.append((key,context.tag,copy.deepcopy(value)))
            elif key=='build_railway':
                path=[int(k) for k,_,_ in get(value,'path')]
                assert all(self.controller(p)==context.tag and self.states[self.province_states[p]].owner==context.tag for p in path),'Unowned or uncontrolled release railway'
                self.railways.append((context.tag,int(get(value,'level')),path))
                for a,b in zip(path,path[1:]):self.railway_levels[tuple(sorted((a,b)))]=int(get(value,'level'))
            elif key=='hidden_effect':self.execute(value,context,temp,root,previous)
            elif key=='set_capital':
                state=int(get(value,'state'));assert self.states[state].owner==context.tag,'Unowned release capital'
                self.capitals[context.tag]=state
            elif key=='transfer_state':
                state=self.states[int(value)];old=state.owner;state.owner=context.tag
                if state.controller==old:state.controller=context.tag
            elif key=='add_state_core':self.core_states[int(value)].add(context.tag)
            elif key=='set_province_controller':self.province_controllers[int(value)]=context.tag
            elif key=='load_oob':
                name=value.strip('"');tree=parse((MOD/'history/units'/(name+'.txt')).read_text(encoding='utf-8-sig'))
                self.armies[context.tag]+=sum(k=='division' for k,_ in walk(tree));self.native_log.append(('load_oob',context.tag,name))
                if get(tree,'instant_effect'):self.execute(get(tree,'instant_effect'),context,temp,root,previous)
            elif key=='transfer_units_fraction':
                target=get(value,'target');fraction=D(get(value,'size'));count=int((D(self.armies[context.tag])*fraction).to_integral_value(rounding=ROUND_FLOOR))
                self.armies[context.tag]-=count;self.armies[target]+=count
                ratio=D(get(value,'stockpile_ratio',str(fraction)))
                for equipment,amount in list(context.equipment.items()):
                    transferred=int((D(amount)*ratio).to_integral_value(rounding=ROUND_FLOOR));context.equipment[equipment]-=transferred
                    c=self.countries[target];c.equipment[equipment]=c.equipment.get(equipment,0)+transferred
                fuel=self.fuel[context.tag]*ratio;self.fuel[context.tag]-=fuel;self.fuel[target]+=fuel
                self.native_log.append(('transfer_units_fraction',context.tag,target,str(fraction)))
            elif key=='inherit_technology':self.research[context.tag]|=self.research[value]
            elif key=='set_technology':
                for ident,_,amount in value:
                    (self.research[context.tag].add if amount=='1' else self.research[context.tag].discard)(ident)
            elif key=='recruit_character':
                assert not any(value in ids for tag,ids in self.character_ids.items() if tag!=context.tag),'Character recruited by two countries'
                self.character_ids[context.tag].add(value)
                if self.ruling_leader[context.tag] is None and context.government in self.character_roles[value]:self.ruling_leader[context.tag]=value
            elif key=='country_event':self.events.append((context.tag,get(value,'id') if isinstance(value,list) else value))
            elif key in ('news_event','declare_war_on','change_tag_from','add_popularity','add_war_support','add_stability','white_peace','end_puppet','set_politics','set_popularities','load_focus_tree','mark_focus_tree_layout_dirty','add_to_faction','annex_country'):
                # Existing nonfinancial outcome commands are explicit source
                # observations. Territory/force/account behavior is executed;
                # these observations do not certify native diplomatic behavior.
                self.native_log.append((key,context.tag,copy.deepcopy(value)))
            else:super().execute([(key,op,value)],context,temp,root,previous)

    def release_action(self,name,tag=None,from_tag=None):
        old=self.from_country;self.from_country=self.countries[from_tag] if from_tag else None
        try:self.execute(get(get(self.release_actions,name),'effect'),self.countries[tag] if tag else None)
        finally:self.from_country=old

    def fire(self,ident,tag,option=0,stale=False):
        event=self.event_definitions[ident];context=self.countries[tag]
        if not stale:
            if not self.trigger(get(event,'trigger',[]),context):return False
            self.execute(get(event,'immediate',[]),context)
        choices=[v for k,_,v in event if k=='option']
        if not choices:return True
        body=choices[option]
        self.execute([n for n in body if n[0] not in ('name','ai_chance','trigger')],context)
        return True
