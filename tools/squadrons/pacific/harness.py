"""Execute new personal scripts alongside actual CPW/SNC/SNP/P1 owners.

Only game observations, event delivery and the new personal arithmetic prefix
are adapters. No fiscal, political, readiness or war-owner substitute is used.
Decimal/deepcopy execution is offline evidence, not native save/gameplay proof.
"""
from decimal import Decimal as D
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'tools'))
from circum_pacific.harness import World as OwnerWorld,parse,get
from config import MOD,campaigns


class World(OwnerWorld):
    def __init__(self,mode='full',enabled=True):
        super().__init__(mode);self.story_enabled=enabled;self.story_queue=[];self.story_deliveries=[]
        for folder,library in(('scripted_effects',self.effects),('scripted_triggers',self.triggers)):
            for key,_,value in parse((MOD/'common'/folder/'ac_squadrons_pacific.txt').read_text(encoding='utf-8-sig')):
                if key in library:raise ValueError('Conflicting personal owner '+key)
                library[key]=value
        self.story_events={get(v,'id'):v for k,_,v in parse((MOD/'events/ac_squadrons_pacific.txt').read_text())if k=='country_event'}
        self.story_actions=get(parse((MOD/'common/on_actions/ac_squadrons_pacific.txt').read_text()),'on_actions')
        self.story_categories=dict((k,v)for k,_,v in parse((MOD/'common/decisions/categories/ac_squadrons_pacific.txt').read_text()))
        self.story_decisions={k:(category,v)for category,_,rows in parse((MOD/'common/decisions/ac_squadrons_pacific.txt').read_text())for k,_,v in rows}

    def number(self,value,context,temp,root,previous):
        if value.startswith('ac_sqp_'):return temp.get(value,context.variables.get(value,D(0)))
        return super().number(value,context,temp,root,previous)

    def trigger(self,nodes,context,temp=None,root=None,previous=None):
        results=[]
        for key,op,value in nodes:
            if key=='has_game_rule'and get(value,'rule')=='ac_sq_stories':
                if get(value,'option')!='enabled':raise ValueError('Unknown story option')
                answer=self.story_enabled
            else:answer=super().trigger([(key,op,value)],context,temp,root,previous)
            results.append(answer)
        return all(results)

    def execute(self,nodes,context,temp=None,root=None,previous=None):
        temp={}if temp is None else temp;root=context if root is None else root;branch=None
        for key,op,value in nodes:
            if key in('if','else_if','else'):
                if key=='if':branch=False
                elif branch is None:raise ValueError('Orphan story conditional')
                if not branch and(key=='else'or self.trigger(get(value,'limit'),context,temp,root,previous)):
                    self.execute([r for r in value if r[0]!='limit'],context,temp,root,previous);branch=True
                continue
            branch=None
            if key in('set_variable','add_to_variable')and value[0][0].startswith('ac_sqp_'):
                name,_,operand=value[0];amount=self.number(operand,context,temp,root,previous)
                context.variables[name]=amount if key=='set_variable'else context.variables.get(name,D(0))+amount
            elif key=='country_event'and get(value,'id').startswith('ac_sqp.'):
                self.story_queue.append((self.today+int(get(value,'days',0)),context.tag,get(value,'id')))
            else:super().execute([(key,op,value)],context,temp,root,previous)

    def story_action(self,name,tag=None,other=None):
        prior=self.from_country;self.from_country=self.countries.get(other)
        try:self.execute(get(get(self.story_actions,name),'effect'),self.countries.get(tag),root=self.countries.get(tag),previous=self.countries.get(other))
        finally:self.from_country=prior

    def descriptions(self,ident,tag):
        result=[];c=self.countries[tag]
        for key,_,value in self.story_events[ident]:
            if key=='desc':
                if isinstance(value,str):result.append(value)
                elif self.trigger(get(value,'trigger',[]),c):result.append(get(value,'text'))
        return result

    def deliver(self,ident,tag):
        c=self.countries[tag];node=self.story_events[ident]
        if not c.exists or not self.trigger(get(node,'trigger',[]),c):return False
        self.execute(get(node,'immediate',[]),c);self.story_deliveries.append((tag,ident,self.descriptions(ident,tag)));return True

    def options(self,ident):return [v for k,_,v in self.story_events[ident]if k=='option']

    def choose(self,ident,index,tag,stale=False):
        c=self.countries[tag];node=self.options(ident)[index]
        if stale or self.trigger(get(node,'trigger',[]),c):self.execute([r for r in node if r[0]not in('name','trigger','ai_chance')],c)

    def open_scene(self,row,chapter,callback=False):
        tag=row['tag'];c=self.countries[tag];self.at('1991.1.1');self.run('ac_sqp_initialize',tag)
        # Isolate a specified prior chapter position, then ask the real dispatch
        # effect to reserve/deliver it. Full-path tests never use this fixture.
        c.flags.pop('ac_sqp_dispatch_pending',None);c.flags.pop('ac_sqp_cooldown',None)
        c.variables['ac_sqp_pending_chapter']=D(0)
        self.story_queue=[q for q in self.story_queue if q[1]!=tag]
        self.at(chapter['earliest']);c.variables['ac_sqp_chapter']=D(chapter['id']-1)
        if callback and chapter.get('callback'):c.flags['ac_sqp_'+tag.lower()+'_'+chapter['callback']['flag']]=None
        self.run('ac_sqp_'+tag.lower()+'_dispatch',tag);ident='ac_sqp.'+str(row['base']+chapter['id'])
        if not self.deliver(ident,tag):raise AssertionError('Actual reservation did not open '+ident)
        return ident,c


def initialized(mode='full',enabled=True):
    w=World(mode,enabled).initialize_both();w.snp_action('on_startup')
    from pacific_nations.model import countries
    for module in countries():w.national_action(module.TAG,'on_startup')
    if mode=='experimental':
        for tag in('OSE','YUK'):w.run('ac_econ_legacy_initialize',tag)
    w.cpw_action('on_startup');w.story_action('on_startup');return w
