"""Actual generated national + P1 + release owners, with native observations.

Financial formulae, payment, readiness, ledger and capacity are never replaced.
The adapter supplies diplomatic/focus/stock/annex observations only. Homogeneous
stock movement and copied-state reload are not native model selection or saves.
"""
import copy
from decimal import Decimal as D
import importlib.util
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/release_foundations'))
from release_harness import World as ReleaseWorld,parse,get,walk

class World(ReleaseWorld):
    def __init__(self,mode='full',new=True,dlcs=()):
        super().__init__(mode,new,dlcs)
        for c in self.countries.values():
            c.subject_of=None;c.wars=set();c.tree='generic_focus';c.completed=set();c.selected=None;c.progress=D(0);c.idea_expiry={}
        for folder,library in [('scripted_effects',self.effects),('scripted_triggers',self.triggers)]:
            for key,_,value in parse((MOD/'common'/folder/'ac_fato_south_belka.txt').read_text()):
                if key in library:raise ValueError('Duplicate actual national/shared owner '+key)
                library[key]=value
        self.fsb_actions=get(parse((MOD/'common/on_actions/ac_fato_south_belka.txt').read_text()),'on_actions')
        self.decisions={key:body for _,_,category in parse((MOD/'common/decisions/ac_fato_south_belka.txt').read_text()) for key,_,body in category}
        self.focuses={}
        for tag in ('fat','sbk'):
            tree=get(parse((MOD/('common/national_focus/ac_fsb_'+tag+'.txt')).read_text()),'focus_tree')
            self.focuses.update({get(body,'id'):body for key,_,body in tree if key=='focus'})
        self.event_definitions.update({get(body,'id'):body for key,_,body in parse((MOD/'events/ac_fato_south_belka.txt').read_text()) if key=='country_event'})

    def number(self,value,context,temp,root,previous):
        if value.startswith('ac_fsb_'):return temp.get(value,context.variables.get(value,D(0)))
        return super().number(value,context,temp,root,previous)

    def trigger(self,nodes,context,temp=None,root=None,previous=None):
        temp={} if temp is None else temp;root=context if root is None else root;answers=[]
        for key,op,value in nodes:
            if key=='is_subject':answer=(context.subject_of is not None)==(value=='yes')
            elif key=='is_subject_of':answer=context.subject_of==self.scope(value,context,root,previous).tag
            elif key=='has_war_with':answer=self.scope(value,context,root,previous).tag in context.wars
            elif key=='has_equipment':
                equipment,comparison,amount=value[0];a=D(context.equipment.get(equipment,0));b=self.number(amount,context,temp,root,previous)
                answer={'=':a==b,'>':a>b,'<':a<b,'>=':a>=b,'<=':a<=b}[comparison]
            elif key=='has_focus_tree':answer=context.tree==value
            elif key=='has_completed_focus':answer=value in context.completed
            elif key=='has_shine_effect_on_focus':answer=context.selected==value
            elif key=='focus_progress':
                ident=get(value,'focus');target=next(n for n in value if n[0]=='progress');p=D(1) if ident in context.completed else context.progress if context.selected==ident else D(0)
                answer=p>D(target[2])
            else:answer=super().trigger([(key,op,value)],context,temp,root,previous)
            answers.append(answer)
        return all(answers)

    def execute(self,nodes,context,temp=None,root=None,previous=None):
        temp={} if temp is None else temp;root=context if root is None else root;branch=None
        for key,op,value in nodes:
            if key=='if':
                branch=self.trigger(get(value,'limit',[]),context,temp,root,previous)
                # The inherited release owner still has valid nested else
                # bodies. Preserve that grammar while distinguishing sibling
                # if/else chains in the new owner and the real P1 formulae.
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
            if key in ('else_if','else'):
                if branch is None:raise ValueError('Orphan national branch')
                if not branch and (key=='else' or self.trigger(get(value,'limit',[]),context,temp,root,previous)):
                    self.execute([n for n in value if n[0]!='limit'],context,temp,root,previous);branch=True
                continue
            branch=None
            if key in ('set_variable','add_to_variable','subtract_from_variable','multiply_variable','divide_variable','set_temp_variable','add_to_temp_variable','subtract_from_temp_variable','multiply_temp_variable','divide_temp_variable') and value[0][0].startswith('ac_fsb_'):
                name,_,operand=value[0];amount=self.number(operand,context,temp,root,previous);store=temp if 'temp_variable' in key else context.variables;before=store.get(name,D(0))
                store[name]=amount if key.startswith('set_') else before+amount if key.startswith('add_') else before-amount if key.startswith('subtract_') else before*amount if key.startswith('multiply_') else before/amount
            elif key=='send_equipment':
                equipment=get(value,'equipment');amount=int(get(value,'amount'));target=self.scope(get(value,'target'),context,root,previous)
                assert amount>0 and context.equipment.get(equipment,0)>=amount,'Unbacked national shipment'
                context.equipment[equipment]-=amount;target.equipment[equipment]=target.equipment.get(equipment,0)+amount
                self.native_log.append((key,context.tag,target.tag,equipment,amount))
            elif key=='load_focus_tree':context.tree=get(value,'tree');self.native_log.append((key,context.tag,context.tree))
            elif key=='effect_tooltip':pass  # engine preview, never a second award
            elif key=='add_timed_idea':
                ident=get(value,'idea');context.ideas.add(ident);context.idea_expiry[ident]=self.today+int(get(value,'days'))
            elif key=='remove_ideas':context.ideas.discard(value);context.idea_expiry.pop(value,None)
            elif key=='annex_country':
                # Execute the exact on_annex callback with its primary ROOT /
                # FROM contract after transferring the observed footprint.
                tag=get(value,'target');target=self.countries[tag]
                for state in self.states.values():
                    if state.owner==tag:
                        state.owner=context.tag
                        if state.controller==tag:state.controller=context.tag
                self.armies[context.tag]+=self.armies[tag];self.armies[tag]=0
                self.fsb_action('on_annex',context.tag,tag)
                self.native_log.append((key,context.tag,tag))
            else:super().execute([(key,op,value)],context,temp,root,previous)

    def fsb_action(self,name,tag=None,from_tag=None):
        old=self.from_country;self.from_country=self.countries[from_tag] if from_tag else None
        try:self.execute(get(get(self.fsb_actions,name),'effect'),self.countries[tag] if tag else None)
        finally:self.from_country=old

    def choose(self,ident,tag):
        c=self.countries[tag];body=self.decisions[ident]
        if not self.trigger(get(body,'available'),c):return False
        self.execute(get(body,'complete_effect'),c);return True

    def complete(self,ident,tag):
        c=self.countries[tag];body=self.focuses[ident]
        if ident in c.completed or not self.trigger(get(body,'available'),c):return False
        for key,_,group in body:
            if key=='prerequisite' and not any(f in c.completed for name,_,f in group if name=='focus'):return False
            if key=='mutually_exclusive' and any(f in c.completed for name,_,f in group if name=='focus'):return False
        c.completed.add(ident);self.execute(get(body,'completion_reward'),c);return True

    def advance(self,days):
        self.today+=days
        for c in self.countries.values():
            for ident,expires in list(c.idea_expiry.items()):
                if expires<=self.today:c.ideas.discard(ident);del c.idea_expiry[ident]

def baseline(mode='full',sbk=True):
    w=World(mode);w.action('on_startup');w.release_action('on_startup')
    if sbk:
        w.states[302].owner=w.states[302].controller='SBK';w.release_action('on_release_as_free','SBK','BLK')
    # Recta is not a 1991 active partner. A legitimate later release fixture
    # supplies the positive bilateral cases; absence is tested separately.
    w.states[316].owner=w.states[316].controller='REC';w.release_action('on_release_as_free','REC','BLK')
    for tag in ('FAT','SBK','GEB','REC','OSE'):
        c=w.countries[tag];w.run('ac_pol_initialize',tag);w.run('ac_fsb_initialize',tag)
        c.pp=D(1000);c.variables['ac_pol_capacity']=D(80)
        if mode=='full':c.variables.update(ac_macro_cash=D(10),ac_macro_arrears=D(0))
        elif mode=='experimental':c.flags['ac_econ_initialized']=None;c.variables.update(ac_econ_treasury=D(100),ac_econ_arrears=D(0))
        c.equipment.update(infantry_equipment=2000,support_equipment=200,motorized_equipment=200)
    return w
