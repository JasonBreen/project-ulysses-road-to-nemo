"""Execute committed institutional scripts offline, with fail-closed syntax.

The public fiscal API fixture is its real narrow owner body; quote recomputation
is a tested boundary stub here. Full budget settlement belongs to economy_v2.
This harness is not native parsing, AI pacing or engine save serialization.
"""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mod/2985041246'
SRC=ROOT/'tools/institutions'
sys.path.insert(0,str(ROOT/'tools'))
from economy_script import parse,fields
sys.path.append(str(ROOT/'tools/usea_expansion'))
from script import parse as gui_parse,get as gui_get,walk as gui_walk
spec=importlib.util.spec_from_file_location('institutions_anea_harness',ROOT/'tools/Test-AneaSystems.py')
anea=importlib.util.module_from_spec(spec);spec.loader.exec_module(anea)
ucw=anea.ucw


def load(relative):return parse((MOD/relative).read_text(encoding='utf-8-sig'))
def mapping(nodes):return {k:v for k,_,v in nodes}
def walk(nodes):
    for key,_,value in nodes:
        if isinstance(value,list):yield key,value;yield from walk(value)


class World(anea.World):
    def __init__(self,when='1991.1.1',fiscal=False):
        super().__init__(when,fiscal=fiscal)
        self.profiles=json.loads((SRC/'profiles.json').read_text())
        self.countries={row['tag']:ucw.Country(row['tag']) for row in self.profiles}
        for index,row in enumerate(self.profiles,1):
            c=self.countries[row['tag']];c.political_power=300.;c.active_focus=None;c.owned=True;c.government=row['inherited_party']
            c.original_tag=row['tag']
            c.identity=index
            c.experience={key:0 for key in ('army_experience','air_experience','navy_experience')}
            c.variables.update(ac_macro_nominal_gdp=100.,ac_macro_commitments_annual=3.,ac_macro_identity=index)
        self.effects.update(mapping(load('common/scripted_effects/ac_politics.txt')))
        self.triggers.update(mapping(load('common/scripted_triggers/ac_politics.txt')))
        # Match the actual shipped API owner after integration; otherwise use
        # the recorded read-only fixture for this branch's declared dependency.
        macro=MOD/'common/scripted_effects/ac_macro_effects.txt'
        owner=mapping(parse(macro.read_text())) if macro.exists() else mapping(parse((SRC/'fiscal_api_fixture.txt').read_text()))
        self.effects['ac_macro_change_commitment']=owner['ac_macro_change_commitment']
        self.effects['ac_macro_quote']=[]
        self.events.update({mapping(n)['id']:(kind,n) for kind,_,n in load('events/ac_politics.txt') if kind=='country_event'})
        self.focuses={mapping(n)['id']:n for kind,_,n in load('common/national_focus/ac_regional_foundation.txt')[0][2] if kind=='focus'}
        self.decisions={ident:n for _,_,category in load('common/decisions/ac_politics.txt') for ident,_,n in category}

    def trigger(self,nodes,country):
        results=[]
        for key,op,value in nodes:
            if key=='original_tag':results.append(country.original_tag==value)
            elif key=='any_owned_state':results.append(country.exists and country.owned and self.trigger(value,country))
            elif key=='has_government':results.append(country.government==value)
            elif key=='ac_macro_ready':results.append((self.fiscal and country.exists and country.owned and country.variables['ac_macro_identity']==country.identity)==(value=='yes'))
            elif key=='check_variable' and value[0][0]=='var':
                data=fields(value);a=self.number(data['var'],country);b=self.number(data['value'],country)
                if data['compare']!='equals':raise AssertionError('Unsupported structured comparison '+data['compare'])
                results.append(a==b)
            else:results.append(super().trigger([(key,op,value)],country))
        return all(results)

    def number(self,value,country):
        if value=='THIS.id':return country.identity
        return super().number(value,country)

    def execute(self,nodes,country):
        branch=None
        for key,operator,value in nodes:
            if key in ('if','else_if','else'):
                if key=='if':branch=False
                elif branch is None:raise AssertionError('Orphaned '+key)
                condition=key=='else' or self.trigger(mapping(value)['limit'],country)
                if not branch and condition:
                    self.execute([node for node in value if node[0]!='limit'],country);branch=True
                continue
            branch=None
            if key in ('multiply_variable','multiply_temp_variable'):
                name,_,operand=value[0];country.variables[name]*=self.number(operand,country)
            elif key=='set_temp_variable':
                name,_,operand=value[0];country.variables[name]=self.number(operand,country)
            elif key=='clamp_variable':
                data=fields(value);name=data['var'];country.variables[name]=min(float(data.get('max','inf')),max(float(data.get('min','-inf')),country.variables[name]))
            elif key=='every_country':
                for target in self.countries.values():
                    if target.exists and self.trigger(mapping(value).get('limit',[]),target):self.execute([node for node in value if node[0]!='limit'],target)
            else:super().execute([(key,operator,value)],country)

    def init(self):
        for tag in self.countries:self.run('ac_pol_initialize',tag)
        return self

    def tick(self,tag='SNS'):
        self.run('ac_pol_weekly',tag)

    def weekly_action(self,tag):
        actions=mapping(load('common/on_actions/ac_politics.txt')[0][2])
        for name in ('on_weekly','on_weekly_'+tag):
            if name in actions:self.execute(mapping(actions[name])['effect'],self.countries[tag])

    def advance(self,days):self.today+=days

    def complete(self,ident,tag):
        c=self.countries[tag];node=self.focuses[ident]
        assert ident not in c.focuses,'Focus already completed'
        for key,_,value in node:
            if key=='prerequisite':assert any(ref in c.focuses for _,_,ref in value),'Prerequisite not complete'
            if key=='mutually_exclusive':assert not any(ref in c.focuses for _,_,ref in value),'Excluded focus completed'
        assert self.trigger(mapping(node).get('available',[]),c),'Focus unavailable'
        c.focuses.add(ident);self.execute(mapping(node)['completion_reward'],c)


class Institutions(unittest.TestCase):
    def test_generation_and_exact_art_packaging(self):
        for script in ('build.py','build_art.py'):
            result=subprocess.run([sys.executable,'-B',str(SRC/script),'--check'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)

    def test_sixty_nine_profiles_have_source_and_no_fabricated_people(self):
        profiles=json.loads((SRC/'profiles.json').read_text());self.assertEqual(69,len(profiles))
        self.assertEqual(69,len({row['tag'] for row in profiles}))
        histories={path.name[:3] for path in (MOD/'history/countries').glob('*.txt')}
        self.assertEqual(histories,{row['tag'] for row in profiles})
        w=World().init()
        for row in profiles:
            self.assertTrue((MOD/row['history']).exists());self.assertIn('mod provenance',row['source_layer'])
            c=w.countries[row['tag']];self.assertIn('ac_pol_form_'+row['institution'],c.flags)
            self.assertEqual(row['regional_tree'],w.trigger(w.triggers['ac_pol_uses_regional_tree'],c))
        self.assertEqual(6,len({row['institution'] for row in profiles}))

    def test_initialization_startup_late_reload_and_unowned(self):
        for when in ('1991.1.1','1991.1.8','1999.7.8','2000.1.1','2005.12.31','2020.1.1'):
            w=World(when).init();c=w.countries['SNS'];c.variables['ac_pol_capacity']=27
            c.variables['ac_ucw_pressure']=31;c.variables['ac_anea_preparedness']=12
            before=copy.deepcopy(c);w.run('ac_pol_initialize','SNS');self.assertEqual(before,c)
            self.assertEqual(when!='1991.1.1',w.flag(c,'ac_pol_late_initialization'))
            self.assertEqual([],w.queue);self.assertEqual(300,c.political_power)
        w=World();w.countries['PLH'].owned=False;w.run('ac_pol_initialize','PLH')
        self.assertNotIn('ac_pol_initialized',w.countries['PLH'].flags)
        startup=mapping(load('common/on_actions/ac_politics.txt')[0][2])['on_startup']
        w.execute(mapping(startup)['effect'],w.countries['SNS']);self.assertIn('ac_pol_initialized',w.countries['SNS'].flags)

    def test_mandates_exact_cost_exclusive_once_and_cooldown(self):
        for policy in ('civic','military','district'):
            w=World().init();c=w.countries['SNS'];w.run('ac_pol_adopt_'+policy,'SNS')
            self.assertEqual(270,c.political_power);self.assertEqual(30,c.variables['ac_pol_capacity'])
            self.assertEqual(['ac_pol_'+policy],[name for name in c.ideas if name in ('ac_pol_civic','ac_pol_military','ac_pol_district')])
            before=copy.deepcopy(c);w.run('ac_pol_adopt_'+policy,'SNS');self.assertEqual(before,c)
            for other in ('civic','military','district'):
                if other!=policy:w.run('ac_pol_adopt_'+other,'SNS');self.assertEqual(before,c)
            w.advance(180);w.run('ac_pol_adopt_'+('military' if policy!='military' else 'civic'),'SNS')
            self.assertEqual(240,c.political_power);self.assertNotIn('ac_pol_'+policy,c.ideas)

    def test_weekly_accounting_repeated_tick_reload_and_failure(self):
        for policy,cost in [('civic',1),('military',2),('district',1)]:
            w=World().init();c=w.countries['SNS'];w.run('ac_pol_adopt_'+policy,'SNS');w.tick()
            self.assertEqual(30-cost,c.variables['ac_pol_capacity'])
            saved=copy.deepcopy(w);before=copy.deepcopy(c);saved.tick();self.assertEqual(before,saved.countries['SNS'])
            w.advance(7);w.tick();self.assertEqual(30-2*cost,c.variables['ac_pol_capacity'])
            c.variables['ac_pol_capacity']=cost;w.advance(7);w.tick()
            self.assertEqual(0,c.variables['ac_pol_capacity']);self.assertNotIn('ac_pol_'+policy,c.ideas)
            self.assertIn('ac_pol_strained',c.ideas);self.assertIn('ac_pol_suspended',c.flags)
            w.advance(7);w.tick();self.assertEqual(0,c.variables['ac_pol_capacity'])

    def test_paid_work_shared_cooldown_limits_and_failure_recovery(self):
        w=World().init();c=w.countries['SNS'];w.take('ac_pol_work_audit_decision','SNS')
        self.assertEqual((275,52),(c.political_power,c.variables['ac_pol_capacity']))
        self.assertIn('ac_pol_attention',c.ideas)
        before=copy.deepcopy(c);w.run('ac_pol_work_audit','SNS');self.assertEqual(before,c)
        w.advance(90);c.variables['ac_pol_capacity']=98;w.run('ac_pol_work_audit','SNS');self.assertEqual(100,c.variables['ac_pol_capacity'])
        w.advance(90);c.variables['ac_pol_capacity']=0;w.run('ac_pol_emergency_review','SNS')
        self.assertEqual(6,c.variables['ac_pol_capacity']);before=copy.deepcopy(c);w.run('ac_pol_emergency_review','SNS');self.assertEqual(before,c)
        c.political_power=0;w.advance(90);before=copy.deepcopy(c);w.run('ac_pol_work_audit','SNS');w.run('ac_pol_emergency_review','SNS');self.assertEqual(before,c)

    def test_full_fiscal_scaled_exact_reversal_disable_and_late_ready(self):
        for fiscal in (False,True):
            w=World(fiscal=fiscal).init();c=w.countries['SNS'];w.run('ac_pol_adopt_civic','SNS')
            self.assertAlmostEqual(3.05 if fiscal else 3,c.variables['ac_macro_commitments_annual'])
            before=copy.deepcopy(c);w.run('ac_pol_sync_fiscal','SNS');self.assertEqual(before,c)
            c.variables['ac_macro_nominal_gdp']=200;w.run('ac_pol_suspend_policy','SNS')
            self.assertAlmostEqual(3,c.variables['ac_macro_commitments_annual'])
            before=copy.deepcopy(c);w.run('ac_pol_suspend_policy','SNS');self.assertEqual(before,c)
        w=World().init();c=w.countries['SNS'];w.run('ac_pol_adopt_military','SNS');w.fiscal=True;w.tick()
        self.assertAlmostEqual(3.1,c.variables['ac_macro_commitments_annual'])
        w.fiscal=False;w.run('ac_pol_suspend_policy','SNS');self.assertAlmostEqual(3.1,c.variables['ac_macro_commitments_annual'])
        w.fiscal=True;w.run('ac_pol_sync_fiscal','SNS');self.assertAlmostEqual(3,c.variables['ac_macro_commitments_annual'])
        # A small economy pays its ownGDP-scaled amount, not a flat billion.
        w=World(fiscal=True).init();c=w.countries['SNS'];c.variables['ac_macro_nominal_gdp']=.1;w.run('ac_pol_adopt_military','SNS')
        self.assertAlmostEqual(3.0001,c.variables['ac_macro_commitments_annual'])

    def test_public_capacity_api_clamps_and_stops_exhausted_mandates(self):
        w=World(fiscal=True).init();c=w.countries['SNS'];w.run('ac_pol_adopt_military','SNS')
        c.variables['ac_pol_capacity_delta']=-1000;w.run('ac_pol_change_capacity','SNS')
        self.assertEqual(0,c.variables['ac_pol_capacity']);self.assertNotIn('ac_pol_military',c.ideas)
        self.assertAlmostEqual(3,c.variables['ac_macro_commitments_annual'])
        c.variables['ac_pol_capacity_delta']=1000;w.run('ac_pol_change_capacity','SNS');self.assertEqual(100,c.variables['ac_pol_capacity'])
        self.assertNotIn('ac_pol_military',c.ideas)
        c.capitulated=True;before=copy.deepcopy(c);w.run('ac_pol_change_capacity','SNS');self.assertEqual(before,c)

    def test_copied_fiscal_receipt_is_rebound_without_subtracting_other_accounts(self):
        w=World(fiscal=True).init();original=w.countries['SNS'];w.run('ac_pol_adopt_civic','SNS')
        original_receipt=original.variables['ac_pol_fiscal_applied'];self.assertAlmostEqual(.05,original_receipt)
        clone=copy.deepcopy(original);clone.identity=900
        clone.variables.update(ac_macro_identity=900,ac_macro_commitments_annual=3.,ac_macro_nominal_gdp=200.)
        w.countries['SNS']=clone
        self.assertNotIn('ac_pol_fiscal_dirty',clone.flags)
        w.run('ac_pol_sync_fiscal','SNS');self.assertAlmostEqual(3.1,clone.variables['ac_macro_commitments_annual'])
        self.assertEqual(900,clone.variables['ac_pol_fiscal_identity'])
        before=copy.deepcopy(clone.variables);w.run('ac_pol_sync_fiscal','SNS');self.assertEqual(before,clone.variables)
        w.run('ac_pol_suspend_policy','SNS');self.assertAlmostEqual(3.,clone.variables['ac_macro_commitments_annual'])
        self.assertAlmostEqual(3.05,original.variables['ac_macro_commitments_annual'])

    def test_generic_weekly_dispatch_charges_a_real_cloned_tag_and_repairs_reviews(self):
        w=World(fiscal=True).init();original=w.countries['SNS'];w.run('ac_pol_adopt_civic','SNS')
        clone=copy.deepcopy(original);clone.tag='D01';clone.identity=900
        clone.variables.update(ac_macro_identity=900,ac_macro_commitments_annual=3.,ac_macro_nominal_gdp=200.)
        clone.flags['SNS_pol_pending']=None  # No response window: repair owns it.
        w.countries['D01']=clone;w.advance(7);w.weekly_action('D01')
        self.assertEqual(29,clone.variables['ac_pol_capacity'])
        self.assertAlmostEqual(3.1,clone.variables['ac_macro_commitments_annual'])
        self.assertNotIn('SNS_pol_pending',clone.flags)
        self.assertEqual(900,clone.variables['ac_pol_fiscal_identity'])
        self.assertEqual(30,original.variables['ac_pol_capacity'])
        self.assertAlmostEqual(3.05,original.variables['ac_macro_commitments_annual'])
        saved=copy.deepcopy(clone);w.weekly_action('D01');self.assertEqual(saved,clone)

    def test_distinct_institutional_models_have_paid_service_routes_and_refresh(self):
        expected=[('SNS','civil_administration',3),('FRU','executive_office',4),('SAP','crown_office',3),
                  ('YUK','party_secretariat',4),('MST','command_administration',5),('AWW','council_office',3)]
        for tag,form,cost in expected:
            w=World().init();c=w.countries[tag];decision='ac_pol_form_'+form+'_decision'
            self.assertTrue(w.available(decision,tag));w.take(decision,tag)
            self.assertEqual(275,c.political_power);self.assertEqual(40-cost,c.variables['ac_pol_capacity'])
            self.assertIn('ac_pol_form_'+form,c.ideas);before=copy.deepcopy(c)
            w.run('ac_pol_form_'+form+'_programme',tag);self.assertEqual(before,c)
        w=World().init();c=w.countries['SNS'];c.government='monarchism';w.tick()
        self.assertIn('ac_pol_form_crown_office',c.flags);self.assertNotIn('ac_pol_form_civil_administration',c.flags)
        self.assertTrue(w.available('ac_pol_form_crown_office_decision','SNS'))

    def test_legacy_idle_handoff_preserves_completion_and_bespoke_exclusion(self):
        w=World().init();c=w.countries['SNS'];c.tree='generic_focus';c.focuses={'army_effort','industrial_effort'}
        before=(c.political_power,copy.deepcopy(c.variables),copy.deepcopy(c.ideas))
        c.active_focus='equipment_effort';w.run('ac_pol_enter_regional','SNS');self.assertEqual('generic_focus',c.tree)
        c.active_focus='continuous_air_production';w.run('ac_pol_enter_regional','SNS');self.assertEqual('generic_focus',c.tree)
        c.active_focus=None;w.run('ac_pol_enter_regional','SNS');self.assertEqual('ac_regional_foundation',c.tree)
        self.assertEqual({'army_effort','industrial_effort'},c.focuses)
        self.assertEqual(before,(c.political_power,c.variables,c.ideas))
        for tag in ('BLK','UST','OSE','SAP','GEB','EMM','EVA','ERU','FCU','NPT','REC','YUK','AWW'):
            c=w.countries[tag];c.tree='generic_focus';w.run('ac_pol_enter_regional',tag);self.assertEqual('generic_focus',c.tree)

    def test_twenty_one_choices_refusal_late_replies_and_distinct_conditions(self):
        w=World().init();events=[key for key in w.events if key.startswith('ac_pol.')];self.assertEqual(21,len(events))
        for event in events:
            body=w.events[event][1];tag=mapping(mapping(body)['trigger'])['original_tag']
            w.run(tag+'_pol_open_review',tag);w.choose(event,0,tag)
            c=w.countries[tag];self.assertIn(tag+'_pol_settled',c.flags)
            before=copy.deepcopy(c);w.choose(event,1,tag);w.run(tag+'_pol_open_review',tag);self.assertEqual(before,c)
        # Subject status invalidates an independent mandate after the review
        # opens. Its useful domestic reserve path remains eligible.
        w=World().init();c=w.countries['UST'];w.run('UST_pol_open_review','UST');c.subject=True
        w.choose('ac_pol.21',0,'UST');self.assertNotIn('UST_pol_settled',c.flags)
        w.choose('ac_pol.21',1,'UST');self.assertIn('UST_pol_reserve',c.ideas)
        # Refusal pays nothing and cannot be farmed; audits remain available.
        w=World().init();c=w.countries['SNS'];w.run('SNS_pol_open_review','SNS');w.choose('ac_pol.1',2,'SNS')
        self.assertEqual(40,c.variables['ac_pol_capacity']);self.assertTrue(w.available('ac_pol_work_audit_decision','SNS'))
        before=copy.deepcopy(c);w.run('SNS_pol_open_review','SNS');self.assertEqual(before,c)
        w.advance(90);w.run('SNS_pol_open_review','SNS');self.assertIn('SNS_pol_pending',c.flags)
        # Capitulation cancels the reward, with no stranded mandatory focus.
        c.capitulated=True;before=copy.deepcopy(c);w.choose('ac_pol.1',0,'SNS');self.assertEqual(before,c)

    def test_interrupted_or_expired_reviews_reopen_without_duplicate_rewards(self):
        for cause in ('capitulation','annexation','no_reply'):
            w=World().init();c=w.countries['SNS'];w.run('SNS_pol_open_review','SNS')
            if cause=='capitulation':c.capitulated=True
            if cause=='annexation':c.owned=False;c.exists=False
            w.advance(31)
            # Model an undelivered/rejected event by removing its queued item;
            # the shipped weekly repair owns reopening, not a harness reschedule.
            w.queue=[];c.capitulated=False;c.exists=True;c.owned=True;w.tick()
            self.assertNotIn('SNS_pol_pending',c.flags)
            self.assertEqual(40,c.variables['ac_pol_capacity'])
            w.take('SNS_pol_review_decision','SNS');w.choose('ac_pol.1',0,'SNS')
            self.assertIn('SNS_pol_settled',c.flags);self.assertEqual(45,c.variables['ac_pol_capacity'])
            before=copy.deepcopy(c);w.choose('ac_pol.1',0,'SNS');self.assertEqual(before,c)
        # Before expiry, incapacity also cancels the pending review so a
        # restored administration can reopen at the next eligible pulse.
        w=World().init();c=w.countries['SNS'];w.run('SNS_pol_open_review','SNS');c.capitulated=True;w.tick()
        self.assertNotIn('SNS_pol_pending',c.flags);c.capitulated=False
        w.take('SNS_pol_review_decision','SNS');self.assertIn('SNS_pol_pending',c.flags)

    def test_regional_tree_prerequisites_exclusions_positions_counts_and_late_assessment(self):
        w=World('2020.1.1').init();self.assertEqual(36,len(w.focuses))
        positions={}
        for ident,node in w.focuses.items():
            d=mapping(node);positions[ident]=(int(d['x']),int(d['y']))
            self.assertIn(d['cost'],('5','10'))
            for kind,body in walk(node):
                if kind in ('prerequisite','mutually_exclusive'):
                    for key,_,ref in body:self.assertIn(ref,w.focuses)
        for a,(ax,ay) in positions.items():
            for b,(bx,by) in positions.items():
                if a!=b:self.assertFalse(abs(ax-bx)*96<147 and abs(ay-by)*160<54,(a,b))
        c=w.countries['SNS'];c.focuses.update(('ac_reg_institution_review','ac_reg_central_register','ac_reg_inspectors','ac_reg_succession_rules'))
        w.complete('ac_reg_institutional_settlement','SNS');self.assertIn('ac_pol_regional_assessed',c.flags)
        before=copy.deepcopy(c);w.execute(mapping(w.focuses['ac_reg_institutional_settlement'])['completion_reward'],c);self.assertEqual(before,c)
        # Each major root opens a real paid programme, using its shipped effect
        # and decision eligibility rather than looking only for a token string.
        for ident,programme in [('register','audit'),('survey','maintenance'),('emergency_register','relief'),
                                ('defense_register','training'),('external_register','external'),('institution_review','audit')]:
            fresh=World().init();fresh.complete('ac_reg_'+ident,'SNS')
            self.assertTrue(fresh.available('ac_pol_work_'+programme+'_decision','SNS'))
            before=fresh.countries['SNS'].political_power
            fresh.take('ac_pol_work_'+programme+'_decision','SNS')
            self.assertEqual(before-25,fresh.countries['SNS'].political_power)

    def test_every_focus_reward_executes_once_with_fixture_prerequisites(self):
        # Shortcut effect coverage, not a natural progression or pacing claim.
        for ident in World().focuses:
            w=World().init();c=w.countries['SNS'];node=w.focuses[ident]
            for kind,_,body in node:
                if kind=='prerequisite':c.focuses.add(body[0][2])
            w.complete(ident,'SNS');before=copy.deepcopy(c)
            w.execute(mapping(node)['completion_reward'],c);self.assertEqual(before,c,ident)

    def test_shipped_font_advances_fit_regional_captions_and_no_prerequisite_cycle(self):
        font=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text()
        line_height=int(re.search(r'common lineHeight=(\d+)',font)[1])
        advances={int(c):int(a) for c,a in re.findall(r'char id=(\d+).*?xadvance=(\d+)',font)}
        localization={m[1]:m[2] for m in re.finditer(r'^\s*([\w.]+):0 "(.*)"',(MOD/'localisation/english/ac_politics_l_english.yml').read_text(encoding='utf-8-sig'),re.M)}
        gui=gui_parse((MOD/'interface/nationalfocusview.gui').read_text(encoding='utf-8-sig'))
        item=next(node for _,node in gui_walk(gui) if gui_get(node,'name')=='"national_focus_item"')
        caption=next(node for _,node in gui_walk(item) if gui_get(node,'name')=='"name"')
        width=int(gui_get(caption,'maxWidth'));height=int(gui_get(caption,'maxHeight'))
        w=World();edges={ident:[ref for key,body in walk(node) if key=='prerequisite' for _,_,ref in body] for ident,node in w.focuses.items()}
        def visit(ident,stack=()):
            self.assertNotIn(ident,stack)
            for ref in edges[ident]:visit(ref,stack+(ident,))
        for ident in w.focuses:
            visit(ident);lines=['']
            for word in localization[ident].split():
                candidate=(lines[-1]+' '+word).strip()
                if lines[-1] and sum(advances[ord(c)] for c in candidate)>width:lines.append(word)
                else:lines[-1]=candidate
            self.assertLessEqual(len(lines)*line_height,height,(ident,lines))
            self.assertTrue(all(sum(advances[ord(c)] for c in line)<=width for line in lines))

    def test_new_localization_and_art_cover_all_consumers(self):
        loc=(MOD/'localisation/english/ac_politics_l_english.yml').read_text(encoding='utf-8-sig')
        keys={m[1] for m in re.finditer(r'^\s*([\w.]+):0 ',loc,re.M)}
        w=World()
        for ident in list(w.focuses)+list(w.decisions)+['ac_regional_foundation','ac_pol_institutions']:
            self.assertIn(ident,keys);self.assertIn(ident+'_desc',keys)
        ideas=mapping(mapping(load('common/ideas/ac_politics.txt'))['ideas'])['country']
        assets=json.loads((SRC/'assets.json').read_text());bindings={sprite for row in assets for sprite in row['sprite_bindings']}
        for ident,_,node in ideas:
            self.assertIn(ident,keys);self.assertIn(ident+'_desc',keys);self.assertIn('GFX_idea_'+mapping(node)['picture'],bindings)
            # Duplicate modifier keys can silently discard the intended
            # benefit/cost, even when every token is valid engine syntax.
            fields(mapping(node)['modifier'])
        hashes=[]
        for row in assets:
            path=MOD/row['file'];self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
            with Image.open(path) as image:
                self.assertEqual((row['width'],row['height']),image.size)
                if row['width']==96:
                    self.assertEqual(0,image.getchannel('A').getpixel((0,0)));hashes.append(row['sha256'])
        self.assertEqual(36,len(hashes));self.assertEqual(36,len(set(hashes)))
        self.assertEqual(101,len(assets))

    def test_foreign_owners_and_legacy_generic_contract_are_preserved(self):
        text=(MOD/'common/scripted_effects/ac_politics.txt').read_text()
        self.assertNotRegex(text,r'(?:set|clr)_global_flag\s*=')
        self.assertNotRegex(text,r'(?:set|add_to|subtract_from)_variable\s*=\s*\{\s*ac_(?:ucw|pwi|anea|econ|macro)_')
        self.assertNotRegex(text,r'recruit_character|set_politics|transfer_state|add_to_faction|declare_war_on|load_oob|create_equipment_variant')
        generic=load('common/national_focus/generic.txt')
        tree=next(n for k,_,n in generic if k=='focus_tree')
        self.assertEqual('generic_focus',mapping(tree)['id'])
        self.assertEqual(54,len([n for k,_,n in tree if k=='focus']))


if __name__=='__main__':unittest.main(verbosity=2)
