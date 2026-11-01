"""Actual P1+SNP+continuation AST; adapters provide engine observations only."""
from decimal import Decimal as D
import importlib.util
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('snc_real_snp',ROOT/'tools/Test-SuperpowerProgrammes.py')
snp=importlib.util.module_from_spec(spec);sys.modules[spec.name]=snp;spec.loader.exec_module(snp)
from pacific_nations.model import MOD,countries
parse,get=snp.parse,snp.get


class World(snp.World):
    def __init__(self,mode='full',new=True):
        super().__init__(mode,new);self.continuation_actions={}
        for module in countries():
            name='ac_snc_'+module.TAG.lower()+'.txt'
            for folder,library in(('scripted_effects',self.effects),('scripted_triggers',self.triggers)):
                for key,_,value in parse((MOD/'common'/folder/name).read_text(encoding='utf-8-sig')):
                    if key in library:raise ValueError('Duplicate actual continuation symbol '+key)
                    library[key]=value
            self.continuation_actions[module.TAG]=get(parse((MOD/'common/on_actions'/name).read_text()),'on_actions')
            for key,_,value in parse((MOD/'common/national_focus'/name).read_text()):
                ident=get(value,'id')
                if ident in self.focuses:raise ValueError('Duplicate actual focus '+ident)
                self.focuses[ident]=value
            for key,_,value in parse((MOD/'events'/name).read_text()):
                if key=='country_event':self.events_by_id[get(value,'id')]=value
            self.custom.extend(parse((MOD/'common/custom_localization'/name).read_text()))

    def number(self,value,context,temp,root,previous):
        if value.startswith('ac_snc_'):return temp.get(value,context.variables.get(value,D(0)))
        return super().number(value,context,temp,root,previous)

    def execute(self,nodes,context,temp=None,root=None,previous=None):
        # Delegate entire conditionals to SNP so their real limits/order execute.
        # Its recursive self.execute calls return here for owned arithmetic.
        temp={}if temp is None else temp
        if len(nodes)==1:
            key,op,value=nodes[0]
            if key in('set_variable','add_to_variable','subtract_from_variable','multiply_variable','divide_variable','set_temp_variable')and value[0][0].startswith('ac_snc_'):
                name,_,operand=value[0];amount=self.number(operand,context,temp,root or context,previous);store=temp if'temp_variable'in key else context.variables;before=store.get(name,D(0))
                if key.startswith('set_'):store[name]=amount
                elif key.startswith('add_'):store[name]=before+amount
                elif key.startswith('subtract_'):store[name]=before-amount
                elif key.startswith('multiply_'):store[name]=before*amount
                else:store[name]=before/amount
                return
        # SNP's ordered effect loop handles its own variable prefix; recognize
        # the additive consumer prefix by a narrow adapter, without rewriting AST.
        if any(k in('set_variable','add_to_variable','subtract_from_variable','multiply_variable','divide_variable','set_temp_variable')and isinstance(v,list)and v[0][0].startswith('ac_snc_')for k,_,v in nodes):
            for row in nodes:self.execute([row],context,temp,root,previous)
            return
        return super().execute(nodes,context,temp,root,previous)

    def national_action(self,owner,name,target=None,other=None):
        self.execute(get(get(self.continuation_actions[owner],name),'effect'),self.countries.get(target),root=self.countries.get(target),previous=self.countries.get(other))


def initialized(mode='full',new=True):
    world=World(mode,new).initialize_both();world.snp_action('on_startup')
    for module in countries():world.national_action(module.TAG,'on_startup')
    for country in world.countries.values():
        country.pp=D(3000);country.variables['ac_pol_capacity']=D(200)
        if mode=='experimental':country.flags['ac_econ_initialized']=None;country.variables.update(ac_econ_treasury=D(1000),ac_econ_arrears=D(0))
    return world
