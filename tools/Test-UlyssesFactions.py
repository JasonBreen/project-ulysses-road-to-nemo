"""Execute authored faction scripts offline. This is not HOI4 native acceptance."""
import argparse
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal as D
from pathlib import Path
import copy
import re
import unittest
from economy_script import parse, fields

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"mod/2985041246"
REFERENCE=None
def load(p): return parse((MOD/p).read_text(encoding="utf-8-sig"))
def mapping(nodes): return {k:v for k,op,v in nodes}
def day(s): return date(*map(int,s.split("."))).toordinal()

@dataclass
class Country:
    tag:str
    id:int
    exists:bool=True
    owns:bool=True
    subject:bool=False
    war:bool=False
    capitulated:bool=False
    agency:bool=False
    pp:D=D(10000)
    variables:dict=field(default_factory=dict)
    flags:dict=field(default_factory=dict)
    modifiers:set=field(default_factory=set)
    faction:int=0
    bop:str=""
    bop_value:D=D(0)
    mios:list=field(default_factory=list)
    def get(self,key): return self.variables.get(key,D(0))

@dataclass(frozen=True)
class Context:
    root:Country
    source:object=None
    stack:tuple=()
    @property
    def current(self): return self.stack[-1] if self.stack else self.root
    @property
    def prev(self): return self.stack[-2] if len(self.stack)>1 else self.root
    def enter(self,c): return Context(self.root,self.source,(self.stack or (self.root,))+(c,))

class World:
    def __init__(self,dlcs=(),when="1995.1.1",fiscal=False,enabled=True):
        self.today=day(when);self.fiscal=fiscal;self.enabled=enabled;self.dlcs=set(dlcs)
        self.countries={tag:Country(tag,i+1) for i,tag in enumerate(("OSE","UST","GEB","BLK","SAP","FCU","ERU"))}
        self.effects=mapping(load("common/scripted_effects/ac_factions_effects.txt"))
        self.triggers=mapping(load("common/scripted_triggers/ac_factions_triggers.txt"))
        self.triggers.update(mapping(load("common/scripted_triggers/ac_economy_triggers.txt")))
        self.decisions={};self.categories=mapping(load("common/decisions/categories/ac_factions_categories.txt"))
        for cat,op,body in load("common/decisions/ac_factions_decisions.txt"):
            for key,op,value in body:self.decisions[key]=(cat,mapping(value))
        self.events={mapping(v)["id"]:v for k,op,v in load("events/ac_factions_events.txt") if k=="country_event"}
        self.modifiers=mapping(load("common/dynamic_modifiers/ac_factions_modifiers.txt"))
        self.actions=mapping(load("common/on_actions/ac_factions_on_actions.txt")[0][2])
        self.native=[];self.roster=[];self.queue=[];self.inbox=[];self.cooldowns={}
        self.leaders={};self.research=set();self.military=set();self.spymasters={}
        self.initiative={};self.influence={}
    def context(self,tag,source=None):return Context(self.countries[tag],self.countries.get(source))
    def scope(self,token,ctx):
        if token in ("THIS","ROOT","FROM","PREV"):
            return {"THIS":ctx.current,"ROOT":ctx.root,"FROM":ctx.source,"PREV":ctx.prev}[token]
        if token.startswith("var:"):
            ident=self.num(token[4:],ctx)
            return next((c for c in self.countries.values() if c.id==ident),None)
        if token=="faction_leader":return self.countries.get(self.leaders.get(ctx.current.faction))
        return self.countries.get(token)
    def num(self,s,ctx):
        try:return D(s)
        except Exception:pass
        c=ctx.current
        if "." in s:
            who,key=s.split(".",1);c=self.scope(who,ctx)
            if c is None:return D(0)
            return D(c.id) if key=="id" else c.get(key)
        if s=="num_faction_members":return D(sum(x.faction==c.faction and x.exists for x in self.countries.values())) if c.faction else D(0)
        if s.startswith(("ac_fac_","ac_sub_","ac_corp_","ac_econ_")):return c.get(s)
        raise ValueError("Unknown number "+s)
    def compare(self,a,op,b):
        return {"=":a==b,"equals":a==b,">":a>b,"greater_than":a>b,">=":a>=b,"greater_than_or_equals":a>=b,"<":a<b,"less_than":a<b,"<=":a<=b,"less_than_or_equals":a<=b,"!=":a!=b}[op]
    def trig(self,nodes,ctx):
        c=ctx.current
        if c is None:return False
        answers=[]
        for key,op,v in nodes:
            if key=="OR": ans=any(self.trig([n],ctx) for n in v)
            elif key in ("AND","hidden_trigger"):ans=self.trig(v,ctx)
            elif key=="NOT":ans=not self.trig(v,ctx)
            elif key in self.triggers:
                ans=self.trig(self.triggers[key],ctx)==(v=="yes")
            elif key=="always":ans=v=="yes"
            elif key=="has_game_rule":
                f=fields(v);option=("enabled" if self.enabled else "disabled") if f["rule"]=="ac_factions" else ("experimental" if self.fiscal else "disabled")
                ans=option==f["option"]
            elif key=="date":ans=self.compare(self.today,op,day(v))
            elif key=="any_owned_state":ans=c.exists and c.owns and self.trig(v,ctx)
            elif key=="has_country_flag":ans=v in c.flags and (c.flags[v] is None or c.flags[v]>self.today)
            elif key=="has_dlc":ans=v in self.dlcs
            elif key=="exists":ans=c.exists==(v=="yes")
            elif key in ("has_war","has_capitulated","is_subject"):
                ans=getattr(c,{"has_war":"war","has_capitulated":"capitulated","is_subject":"subject"}[key])==(v=="yes")
            elif key=="is_in_faction":ans=bool(c.faction)==(v=="yes")
            elif key=="is_faction_leader":ans=(self.leaders.get(c.faction)==c.tag)==(v=="yes")
            elif key=="is_in_faction_with":
                other=self.scope(v,ctx);ans=other is not None and bool(c.faction) and c.faction==other.faction
            elif key=="has_war_with":
                other=self.scope(v,ctx);ans=other is not None and c.war and other.war and c.faction!=other.faction
            elif key in ("tag","original_tag"):
                other=self.scope(v,ctx);ans=c.tag==(other.tag if other else v)
            elif key=="check_variable":
                if v[0][0]=="var":
                    f=fields(v);ans=self.compare(self.num(f["var"],ctx),f.get("compare","equals"),self.num(f["value"],ctx))
                else:
                    a,operator,b=v[0];ans=self.compare(self.num(a,ctx),operator,self.num(b,ctx))
            elif key=="has_dynamic_modifier":ans=fields(v)["modifier"] in c.modifiers
            elif key=="has_power_balance":ans=c.bop==fields(v)["id"]
            elif key=="is_in_array":
                f=fields(v);ans=c.tag in self.roster if next(iter(f))=="global.ac_fac_countries" else False
            elif key=="any_country":
                ans=any(self.trig(v,ctx.enter(x)) for x in self.countries.values() if x.exists)
            elif key=="any_faction_member":
                ans=any(self.trig(v,ctx.enter(x)) for x in self.countries.values() if x.exists and c.faction and x.faction==c.faction)
            elif key=="any_military_industrial_organization":ans=any(x["visible"] for x in c.mios)
            elif key=="has_intelligence_agency":ans=c.agency==(v=="yes")
            elif key=="has_faction_research_unlocked":ans=(c.faction in self.research)==(v=="yes")
            elif key=="has_faction_military_unlocked":ans=(c.faction in self.military)==(v=="yes")
            elif key=="has_faction_template":ans=bool(c.faction) and ("template",c.faction,v) in self.native
            elif key in ("FROM","PREV","ROOT","faction_leader") or key.startswith("var:"):
                ans=self.trig(v,ctx.enter(self.scope(key,ctx)))
            else:raise ValueError("Unknown trigger "+key)
            answers.append(ans)
        return all(answers)
    def effect(self,nodes,ctx):
        c=ctx.current
        if c is None:return
        branch=None
        for key,op,v in nodes:
            if key=="if":
                f=mapping(v);branch=self.trig(f.get("limit",[]),ctx)
                if branch:self.effect([n for n in v if n[0]!="limit"],ctx)
            elif key=="else":
                if branch is None:raise ValueError("Unpaired else")
                if not branch:self.effect(v,ctx)
                branch=None
            elif key in self.effects:self.effect(self.effects[key],ctx)
            elif key in ("set_variable","add_to_variable","subtract_from_variable","multiply_variable"):
                name,operator,value=v[0];n=self.num(value,ctx)
                c.variables[name]={"set_variable":n,"add_to_variable":c.get(name)+n,"subtract_from_variable":c.get(name)-n,"multiply_variable":c.get(name)*n}[key]
            elif key=="clear_variable":c.variables.pop(v,None)
            elif key=="set_country_flag":
                if isinstance(v,list):
                    f=fields(v);c.flags[f["flag"]]=self.today+int(f["days"]) if "days" in f else None
                else:c.flags[v]=None
            elif key=="clr_country_flag":c.flags.pop(v,None)
            elif key=="add_to_array":
                if c.tag not in self.roster:self.roster.append(c.tag)
            elif key in ("add_dynamic_modifier","remove_dynamic_modifier"):
                name=fields(v)["modifier"]
                (c.modifiers.add if key=="add_dynamic_modifier" else c.modifiers.discard)(name)
            elif key=="every_country":
                limits=mapping(v).get("limit",[])
                for x in list(self.countries.values()):
                    if x.exists and self.trig(limits,ctx.enter(x)):
                        self.effect([n for n in v if n[0]!="limit"],ctx.enter(x))
            elif key in ("ROOT","FROM","PREV","faction_leader") or key.startswith("var:"):
                self.effect(v,ctx.enter(self.scope(key,ctx)))
            elif key=="create_faction_from_template":
                assert "No Compromise, No Surrender" in self.dlcs
                c.faction=c.id;self.leaders[c.faction]=c.tag;self.native.append(("template",c.faction,v))
            elif key=="create_faction":
                c.faction=c.id;self.leaders[c.faction]=c.tag;self.native.append(("legacy",c.faction,v))
            elif key=="add_to_faction":self.scope(v,ctx).faction=c.faction
            elif key=="leave_faction":c.faction=0
            elif key=="dismantle_faction":
                old=c.faction
                for x in self.countries.values():
                    if x.faction==old:x.faction=0
            elif key in ("set_faction_research_unlocked","set_faction_military_unlocked","add_faction_initiative","add_faction_influence_score"):
                assert "No Compromise, No Surrender" in self.dlcs
                if key=="set_faction_research_unlocked":self.research.add(c.faction)
                elif key=="set_faction_military_unlocked":self.military.add(c.faction)
                elif key=="add_faction_initiative":self.initiative[c.faction]=self.initiative.get(c.faction,D(0))+D(v)
                else:self.influence[c.tag]=self.influence.get(c.tag,D(0))+D(v)
                self.native.append((key,c.tag,v))
            elif key=="set_faction_spymaster":
                assert "La Resistance" in self.dlcs and c.agency
                self.spymasters[c.faction]=c.tag;self.native.append((key,c.tag,v))
            elif key=="every_military_industrial_organization":
                assert "Arms Against Tyranny" in self.dlcs
                f=fields(v);assert set(f)=={"add_mio_funds"}
                for mio in c.mios:
                    if mio["visible"]:mio["funds"]+=D(f["add_mio_funds"])
                self.native.append((key,c.tag,None))
            elif key in ("set_power_balance","add_power_balance_value","remove_power_balance"):
                f=fields(v)
                if key!="remove_power_balance":assert "By Blood Alone" in self.dlcs
                if key=="set_power_balance":c.bop=f["id"];c.bop_value=D(f["set_value"])
                elif key=="remove_power_balance":c.bop=""
                else:c.bop_value=max(D(-1),min(D(1),c.bop_value+D(f["value"])))
                self.native.append((key,c.tag,f["id"]))
            elif key=="country_event":
                f=fields(v);self.queue.append((self.today+int(f.get("days",0)),c.tag,ctx.root.tag,f["id"]))
            else:raise ValueError("Unknown effect "+key)
    def run(self,name,tag,source=None):self.effect(self.effects[name],self.context(tag,source))
    def check(self,name,tag,source=None):return self.trig(self.triggers[name],self.context(tag,source))
    def startup(self):
        self.effect(mapping(self.actions["on_startup"])["effect"],self.context("OSE"))
    def tick(self):
        for c in list(self.countries.values()):
            if c.exists:self.effect(mapping(self.actions["on_monthly"])["effect"],Context(c))
    def decision_available(self,name,tag,source=None):
        cat,d=self.decisions[name];ctx=self.context(tag,source);c=ctx.current
        if c.tag not in self.roster:return False
        if not self.trig(mapping(self.categories[cat]).get("visible",[]),ctx):return False
        if c.pp<D(d.get("cost",0)) or self.cooldowns.get((tag,name),0)>self.today:return False
        if source and source not in self.roster:return False
        return all(self.trig(d.get(k,[]),ctx) for k in ("visible","available","target_root_trigger","target_trigger"))
    def decide(self,name,tag,source=None):
        if not self.decision_available(name,tag,source):return False
        d=self.decisions[name][1];c=self.countries[tag];c.pp-=D(d.get("cost",0))
        self.effect(d.get("complete_effect",[]),self.context(tag,source))
        if "days_re_enable" in d:self.cooldowns[tag,name]=self.today+int(d["days_re_enable"])
        return True
    def advance(self,days):
        for _ in range(days):
            self.today+=1
            for due,tag,source,eid in list(self.queue):
                if due<=self.today:
                    self.queue.remove((due,tag,source,eid))
                    self.inbox.append((self.today+20,tag,source,eid))
            for entry in list(self.inbox):
                if entry[0]<=self.today:self.respond(entry[1],0,entry=entry)
    def respond(self,tag,choice=1,entry=None):
        entry=entry or next(e for e in self.inbox if e[1]==tag)
        _,_,source,eid=entry
        options=[v for k,op,v in self.events[eid] if k=="option"]
        option=options[choice];ctx=self.context(tag,source)
        if not self.trig(mapping(option).get("trigger",[]),ctx):return False
        self.effect([n for n in option if n[0] not in ("name","trigger","ai_chance")],ctx)
        self.inbox.remove(entry);return True
    def active_modifier(self,tag,key):
        c=self.countries[tag]
        return key in c.modifiers and self.trig(mapping(self.modifiers[key])["enable"],Context(c))
    def invite(self,host,target,role="full"):
        assert self.decide("ac_sub_invite_"+role+"_decision",host,target)
        self.advance(1)
        return self.respond(target)
    def council(self):
        self.startup()
        self.run("ac_fac_found_bloc","OSE")
        self.countries["UST"].faction=self.countries["OSE"].faction
        self.run("ac_sub_found","OSE")
        assert self.invite("OSE","UST")
        return self

NCNS="No Compromise, No Surrender"
ALL=(NCNS,"Arms Against Tyranny","By Blood Alone","La Resistance")

class FactionTests(unittest.TestCase):
    def test_calendar_and_disabled(self):
        for when,enabled in (("1994.12.31",True),("1995.1.1",False)):
            w=World(when=when,enabled=enabled);w.startup();w.tick()
            self.assertFalse(w.countries["OSE"].modifiers);self.assertFalse(w.roster);self.assertFalse(w.native)
        w=World(when="2065.12.31");w.startup();self.assertTrue(w.check("ac_fac_ready","OSE"))
    def test_idempotent_startup_and_monthly(self):
        w=World();w.startup();w.run("ac_fac_support_security","OSE");before=copy.deepcopy(w.countries["OSE"].variables)
        w.startup();w.tick();self.assertEqual(before,w.countries["OSE"].variables);self.assertEqual(7,len(w.roster))
    def test_influence_conservation_no_deadlock(self):
        w=World();w.startup();c=w.countries["OSE"]
        for prefix,names in (("ac_fac",("civic","security","industry")),("ac_corp",("engineering","operations","board"))):
            for name in names:
                for _ in range(150):
                    w.run(prefix+"_support_"+name,"OSE")
                    values=[c.get(prefix+"_"+n) for n in names]
                    self.assertEqual(D(100),sum(values));self.assertTrue(all(0<=v<=100 for v in values))
            self.assertEqual(D(100),c.get(prefix+"_"+names[-1]))
        self.assertEqual(D("-0.05"),c.get("ac_fac_capture"))
    def test_influence_cooldown(self):
        w=World();w.startup();self.assertTrue(w.decide("ac_fac_support_civic_decision","OSE"))
        self.assertFalse(w.decide("ac_fac_support_industry_decision","OSE"));w.advance(30)
        self.assertTrue(w.decide("ac_fac_support_industry_decision","OSE"))
    def test_native_and_legacy_bloc_creation(self):
        for dlcs,kind in (((),"legacy"),((NCNS,),"template")):
            w=World(dlcs);w.startup();self.assertTrue(w.decide("ac_fac_found_bloc_decision","OSE"))
            self.assertEqual(kind,w.native[-1][0]);self.assertFalse(w.decide("ac_fac_found_bloc_decision","OSE"))
    def test_bloc_invitation_consent_and_war_recheck(self):
        w=World();w.startup();w.run("ac_fac_found_bloc","OSE")
        self.assertTrue(w.decide("ac_fac_invite_decision","OSE","UST"));self.assertEqual(0,w.countries["UST"].faction)
        w.advance(1);self.assertTrue(w.respond("UST"));self.assertEqual(w.countries["OSE"].faction,w.countries["UST"].faction)
        w.decide("ac_fac_invite_decision","OSE","GEB");w.advance(1);w.countries["GEB"].war=True
        self.assertFalse(w.respond("GEB"));w.advance(21);self.assertNotIn("ac_fac_invite_pending",w.countries["GEB"].flags)
    def test_bloc_stale_generation_and_decline(self):
        w=World();w.startup();w.run("ac_fac_found_bloc","OSE")
        w.decide("ac_fac_invite_decision","OSE","UST");w.advance(1)
        w.countries["OSE"].variables["ac_fac_generation"]+=1
        self.assertFalse(w.respond("UST"));self.assertTrue(w.respond("UST",0));self.assertEqual(0,w.countries["UST"].faction)
    def test_full_associate_and_cross_bloc_eligibility(self):
        w=World().council();self.assertTrue(w.check("ac_sub_full_valid","UST"))
        self.assertTrue(w.invite("OSE","GEB","associate"));self.assertTrue(w.check("ac_sub_associate_valid","GEB"))
        self.assertEqual(0,w.countries["GEB"].faction)
        w.countries["GEB"].faction=99;self.assertFalse(w.active_modifier("GEB","ac_sub_program_modifier"))
        w.tick();self.assertNotIn("ac_sub_member",w.countries["GEB"].flags)
    def test_invite_timeout_default_declines(self):
        w=World().council();w.decide("ac_sub_invite_associate_decision","OSE","GEB");w.advance(22)
        self.assertNotIn("ac_sub_member",w.countries["GEB"].flags)
        self.assertNotIn("ac_sub_invite_pending",w.countries["GEB"].flags)
    def test_double_invite_lock_and_stale_refoundation(self):
        w=World().council();self.assertTrue(w.decide("ac_sub_invite_associate_decision","OSE","GEB"))
        self.assertFalse(w.decide("ac_sub_invite_associate_decision","OSE","GEB"));w.advance(1)
        w.run("ac_sub_dissolve","OSE");w.run("ac_sub_found","OSE")
        self.assertFalse(w.respond("GEB"));self.assertNotIn("ac_sub_member",w.countries["GEB"].flags)
    def test_investment_cost_and_arrears(self):
        w=World(fiscal=True).council()
        for c in (w.countries["OSE"],w.countries["UST"]):
            c.flags["ac_econ_initialized"]=None;c.variables["ac_econ_treasury"]=D(5)
        c=w.countries["OSE"];c.variables["ac_econ_arrears"]=D(1)
        self.assertFalse(w.decide("ac_sub_invest_mobility_decision","OSE"));c.variables["ac_econ_arrears"]=D(0)
        pp=c.pp;self.assertTrue(w.decide("ac_sub_invest_mobility_decision","OSE"))
        self.assertEqual(D(3),c.get("ac_econ_treasury"));self.assertEqual(pp-35,c.pp)
        self.assertFalse(w.decide("ac_sub_invest_mobility_decision","OSE"));self.assertEqual(D(3),c.get("ac_econ_treasury"))
    def test_poor_treasury_and_fiscal_off(self):
        w=World(fiscal=True).council();c=w.countries["OSE"];c.flags["ac_econ_initialized"]=None;c.variables["ac_econ_treasury"]=D("1.99")
        self.assertFalse(w.decide("ac_sub_invest_mobility_decision","OSE"))
        w.fiscal=False;self.assertTrue(w.decide("ac_sub_invest_mobility_decision","OSE"));self.assertEqual(D("1.99"),c.get("ac_econ_treasury"))
    def test_two_member_consent_and_program_benefits(self):
        w=World().council();self.assertFalse(w.decide("ac_sub_enact_mobility_decision","OSE"))
        for tag in ("OSE","UST"):self.assertTrue(w.decide("ac_sub_invest_mobility_decision",tag))
        self.assertTrue(w.decide("ac_sub_enact_mobility_decision","OSE"));self.assertFalse(w.decide("ac_sub_enact_mobility_decision","OSE"))
        self.assertEqual(D("-0.03"),w.countries["UST"].get("ac_sub_supply"))
        self.assertTrue(w.invite("OSE","GEB","associate"));self.assertEqual(D("-0.015"),w.countries["GEB"].get("ac_sub_supply"))
        self.assertFalse(w.decide("ac_sub_invest_research_decision","GEB"))
    def test_influence_gate_and_all_tracks(self):
        w=World().council()
        for tag in ("OSE","UST"):
            self.assertFalse(w.decide("ac_sub_invest_procurement_decision",tag))
            w.run("ac_fac_support_industry",tag)
            for track in ("mobility","procurement","research"):self.assertTrue(w.decide("ac_sub_invest_"+track+"_decision",tag))
        for track in ("mobility","procurement","research"):self.assertTrue(w.decide("ac_sub_enact_"+track+"_decision","OSE"))
        self.assertEqual(D("0.05"),w.countries["UST"].get("ac_sub_efficiency"))
        self.assertEqual(D("0.02"),w.countries["UST"].get("ac_sub_science"))
    def test_chair_consent_and_live_availability(self):
        w=World().council()
        for tag in ("OSE","UST"):w.decide("ac_sub_invest_mobility_decision",tag)
        w.countries["UST"].faction=0
        pp=w.countries["OSE"].pp
        self.assertFalse(w.decide("ac_sub_enact_mobility_decision","OSE"))
        self.assertEqual(pp,w.countries["OSE"].pp)
    def test_transfer_never_revives_stale_seat(self):
        w=World().council();w.invite("OSE","GEB","associate")
        stale=w.countries["GEB"];stale.variables["ac_sub_generation"]-=1
        self.assertFalse(w.check("ac_sub_associate_valid","GEB"))
        self.assertTrue(w.decide("ac_sub_transfer_decision","OSE","UST"))
        self.assertFalse(w.check("ac_sub_associate_valid","GEB"))
    def test_ai_can_fund_authorized_council(self):
        w=World()
        for track in ("mobility","procurement","research"):
            for action in ("invest","enact"):
                d=w.decisions["ac_sub_"+action+"_"+track+"_decision"][1]
                self.assertEqual("1",fields(d["ai_will_do"])["base"])
    def test_departing_investor_cannot_authorize(self):
        w=World().council()
        for tag in ("OSE","UST"):w.decide("ac_sub_invest_mobility_decision",tag)
        w.countries["UST"].faction=0
        w.run("ac_sub_enact_mobility_effect","OSE")
        self.assertEqual(0,w.countries["OSE"].get("ac_sub_mobility"));w.tick()
        self.assertNotIn("ac_sub_member",w.countries["UST"].flags)
    def test_transfer_preserves_programs_invalidates_old_offers(self):
        w=World().council()
        for tag in ("OSE","UST"):w.decide("ac_sub_invest_mobility_decision",tag)
        w.decide("ac_sub_enact_mobility_decision","OSE")
        w.decide("ac_sub_invite_associate_decision","OSE","GEB");w.advance(1)
        self.assertTrue(w.decide("ac_sub_transfer_decision","OSE","UST"))
        self.assertTrue(w.check("ac_sub_chair_valid","UST"));self.assertTrue(w.check("ac_sub_full_valid","OSE"))
        self.assertEqual(1,w.countries["UST"].get("ac_sub_mobility"));self.assertFalse(w.respond("GEB"))
        w.tick();self.assertEqual(D("-0.03"),w.countries["OSE"].get("ac_sub_supply"))
    def test_dissolution_preserves_parent_and_no_refund(self):
        w=World().council();parent=w.countries["OSE"].faction;w.decide("ac_sub_invest_research_decision","UST");pp=w.countries["UST"].pp
        w.run("ac_sub_dissolve","OSE")
        for tag in ("OSE","UST"):
            self.assertNotIn("ac_sub_member",w.countries[tag].flags);self.assertEqual(parent,w.countries[tag].faction)
        self.assertEqual(pp,w.countries["UST"].pp)
    def test_annexed_subject_and_civilwar_cleanup(self):
        for change in ("annexed","subject","capitulated"):
            w=World().council();c=w.countries["OSE"]
            if change=="annexed":c.exists=False;c.owns=False
            else:setattr(c,change,True)
            self.assertFalse(w.active_modifier("UST","ac_sub_program_modifier"));w.tick()
            self.assertNotIn("ac_sub_member",w.countries["UST"].flags)
        w=World().council();clone=copy.deepcopy(w.countries["OSE"]);clone.tag="NEW";clone.id=999;w.countries["NEW"]=clone
        w.run("ac_fac_initialize","NEW")
        self.assertNotIn("ac_sub_chair",clone.flags);self.assertNotIn("ac_sub_member",clone.flags)
        self.assertTrue(w.check("ac_sub_chair_valid","OSE"))
    def test_rule_off_disables_and_cleans_councils_preserves_bloc(self):
        w=World(ALL).council();parent=w.countries["OSE"].faction;w.enabled=False
        self.assertFalse(w.active_modifier("UST","ac_sub_program_modifier"));w.tick()
        for c in w.countries.values():self.assertFalse(c.modifiers);self.assertNotEqual("ac_fac_power_balance",c.bop)
        self.assertEqual(parent,w.countries["OSE"].faction)
    def test_bop_preserves_country_contracts(self):
        w=World(ALL);w.countries["BLK"].bop="BLK_power_balance";w.countries["SAP"].bop="SAP_power_balance";w.startup()
        self.assertEqual("BLK_power_balance",w.countries["BLK"].bop);self.assertEqual("SAP_power_balance",w.countries["SAP"].bop)
        self.assertEqual("ac_fac_power_balance",w.countries["UST"].bop)
        w.run("ac_fac_support_security","UST");self.assertEqual(D("0.1"),w.countries["UST"].bop_value)
    def test_dlc_matrix_and_visible_mio_scope(self):
        for dlcs in ((),(NCNS,),("La Resistance",),("Arms Against Tyranny",),("By Blood Alone",),ALL):
            w=World(dlcs).council();c=w.countries["OSE"]
            c.mios=[{"visible":True,"funds":D(0)},{"visible":False,"funds":D(0)}]
            self.assertEqual("Arms Against Tyranny" in dlcs,w.decide("ac_corp_mio_workshop_decision","OSE"))
            self.assertEqual(D(25) if "Arms Against Tyranny" in dlcs else D(0),c.mios[0]["funds"]);self.assertEqual(0,c.mios[1]["funds"])
            self.assertFalse(w.decide("ac_fac_spymaster_decision","OSE","UST"));w.countries["UST"].agency=True
            self.assertEqual("La Resistance" in dlcs,w.decide("ac_fac_spymaster_decision","OSE","UST"))
            self.assertEqual(NCNS in dlcs,w.decide("ac_fac_coordination_decision","UST"))
    def test_native_research_command_gates(self):
        for dlcs in ((),ALL):
            w=World(dlcs).council();self.assertFalse(w.decide("ac_fac_joint_research_decision","OSE"))
            for tag in ("OSE","UST"):
                for track in ("mobility","research"):w.decide("ac_sub_invest_"+track+"_decision",tag)
            for track in ("mobility","research"):w.decide("ac_sub_enact_"+track+"_decision","OSE")
            self.assertEqual(bool(dlcs),w.decide("ac_fac_joint_research_decision","OSE"))
            self.assertEqual(bool(dlcs),w.decide("ac_fac_joint_command_decision","OSE"))
            if dlcs:self.assertFalse(w.decide("ac_fac_joint_command_decision","OSE"))
    def test_save_state_roundtrip_and_long_horizon(self):
        w=World().council()
        for tag in ("OSE","UST"):w.decide("ac_sub_invest_research_decision",tag)
        w.decide("ac_sub_enact_research_decision","OSE")
        restored=copy.deepcopy(w)
        for _ in range(852):
            restored.advance(30);restored.tick()
        self.assertTrue(restored.check("ac_sub_full_valid","UST"));self.assertEqual(D("0.02"),restored.countries["UST"].get("ac_sub_science"))
        self.assertEqual(D(100),sum(restored.countries["UST"].get("ac_corp_"+n) for n in ("engineering","operations","board")))
    def test_decline_and_unsupported_memberships(self):
        w=World().council()
        w.decide("ac_sub_invite_associate_decision","OSE","GEB");w.advance(1)
        self.assertTrue(w.respond("GEB",0));self.assertNotIn("ac_sub_member",w.countries["GEB"].flags)
        w.countries["GEB"].subject=True
        self.assertFalse(w.decide("ac_sub_invite_associate_decision","OSE","GEB"))
        self.assertFalse(w.decide("ac_sub_transfer_decision","OSE","GEB"))
    def test_native_political_actions_do_not_steal_existing_bloc(self):
        w=World();w.startup();w.countries["FCU"].faction=10;w.leaders[10]="FCU"
        self.assertFalse(w.decide("ac_fac_dissolve_bloc_decision","FCU"))
        self.assertFalse(w.decide("ac_fac_invite_decision","FCU","GEB"))
        w.countries["GEB"].faction=10;w.countries["GEB"].war=True
        self.assertFalse(w.decide("ac_fac_leave_decision","GEB"))
    def test_chair_epoch_survives_membership_in_another_council(self):
        w=World().council();c=w.countries["OSE"]
        w.run("ac_sub_dissolve","OSE")
        c.variables["ac_sub_epoch"]=D(20)
        c.variables["ac_sub_generation"]=D(1)
        w.run("ac_sub_found","OSE")
        self.assertEqual(21,c.get("ac_sub_generation"))
    def test_multiple_councils_are_independent(self):
        w=World().council();parent=w.countries["OSE"].faction
        w.countries["FCU"].faction=parent;w.countries["GEB"].faction=parent
        self.assertTrue(w.decide("ac_sub_found_decision","FCU"))
        self.assertTrue(w.invite("FCU","GEB"))
        for tag in ("OSE","UST"):w.decide("ac_sub_invest_research_decision",tag)
        w.decide("ac_sub_enact_research_decision","OSE")
        self.assertEqual(D("0.02"),w.countries["UST"].get("ac_sub_science"))
        self.assertEqual(0,w.countries["GEB"].get("ac_sub_science"))
        w.run("ac_sub_dissolve","OSE")
        self.assertTrue(w.check("ac_sub_full_valid","GEB"))
    def test_generation_guard_mutation_is_detected(self):
        w=World().council()
        w.decide("ac_sub_invite_associate_decision","OSE","GEB");w.advance(1)
        w.countries["OSE"].variables["ac_sub_generation"]+=1
        self.assertFalse(w.check("ac_sub_offer_valid","GEB","OSE"))
        w.triggers["ac_sub_offer_valid"]=[n for n in w.triggers["ac_sub_offer_valid"] if not (n[0]=="check_variable" and mapping(n[2]).get("var")=="ac_sub_offer_generation")]
        self.assertTrue(w.check("ac_sub_offer_valid","GEB","OSE"))
    def test_saturated_influence_does_not_charge(self):
        w=World();w.startup()
        for _ in range(100):w.run("ac_corp_support_engineering","OSE")
        w.advance(30);pp=w.countries["OSE"].pp
        self.assertFalse(w.decide("ac_corp_support_engineering_decision","OSE"))
        self.assertEqual(pp,w.countries["OSE"].pp)
    def test_engine_interfaces(self):
        if REFERENCE is None:self.skipTest("Installed reference path not supplied")
        effect=(REFERENCE/"documentation/effects_documentation.md").read_text(encoding="utf-8-sig")
        trigger=(REFERENCE/"documentation/triggers_documentation.md").read_text(encoding="utf-8-sig")
        dynamic=(REFERENCE/"documentation/dynamic_variables_documentation.md").read_text(encoding="utf-8-sig")
        effects=("create_faction","create_faction_from_template","add_to_faction","leave_faction","dismantle_faction","add_faction_initiative","add_faction_influence_score","set_faction_research_unlocked","set_faction_military_unlocked","set_faction_spymaster","every_military_industrial_organization","add_mio_funds","set_power_balance","add_power_balance_value","remove_power_balance")
        for name in effects:self.assertRegex(effect,r"(?m)^## "+name+r"\s*$")
        for name in ("has_faction_template","has_faction_research_unlocked","has_faction_military_unlocked","has_power_balance","has_intelligence_agency","any_country"):
            self.assertRegex(trigger,r"(?m)^## "+name+r"\s*$")
        self.assertIn("### num_faction_members",dynamic)
        for folder,expected in (("dlc049_no_compromise_no_surrender",NCNS),("dlc038_arms_against_tyranny","Arms Against Tyranny"),("dlc028_la_resistance","La Resistance"),("dlc036_by_blood_alone","By Blood Alone")):
            descriptors=list((REFERENCE/"dlc"/folder).glob("*.dlc"))
            self.assertTrue(descriptors)
            self.assertIn('name = "'+expected+'"',descriptors[0].read_text(encoding="utf-8-sig"))
    def test_reference_localization_and_bom(self):
        loc=MOD/"localisation/english/ac_factions_l_english.yml";self.assertTrue(loc.read_bytes().startswith(b"\xef\xbb\xbf"))
        keys=re.findall(r"^\s+([\w.]+):\d* ",loc.read_text(encoding="utf-8-sig"),re.M);self.assertEqual(len(keys),len(set(keys)));keys=set(keys)
        w=World()
        for name in list(w.decisions)+list(w.categories)+list(w.modifiers):
            self.assertIn(name,keys);self.assertIn(name+"_desc",keys)
        for eid,event in w.events.items():
            for k,op,v in event:
                if k in ("title","desc"):self.assertIn(v,keys)
        for folder in ("common/scripted_effects","common/scripted_triggers","common/decisions","events","common/factions"):
            for p in (MOD/folder).rglob("ac_factions*.txt"):parse(p.read_text(encoding="utf-8-sig"))
    def test_script_unknown_commands_fail_closed(self):
        w=World();w.startup()
        with self.assertRaises(ValueError):w.effect(parse("invent_faction = yes"),w.context("OSE"))
        with self.assertRaises(ValueError):w.trig(parse("invent_faction = yes"),w.context("OSE"))

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--mod-root",type=Path);parser.add_argument("--reference-game-root",type=Path)
    args,remaining=parser.parse_known_args()
    if args.mod_root:MOD=args.mod_root.resolve()
    if args.reference_game_root:REFERENCE=args.reference_game_root.resolve()
    unittest.main(argv=[__file__]+remaining)
