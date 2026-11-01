"""Static import, provenance, geometry, localization and SP96 asset closure."""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

from PIL import Image

ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from superpowers import build
from superpowers.content import BRANCHES,focus_id
from superpowers.mechanics import COUNTRIES,SERVICES
from usea_expansion.script import parse,get


def descend(nodes):
    for row in nodes:
        yield row
        if isinstance(row[2],list):yield from descend(row[2])


class SuperpowerAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.focuses={get(v,'id'):v for k,_,v in parse((MOD/'common/national_focus/ac_superpower_programmes.txt').read_text())if k=='shared_focus'}
        cls.assets=json.loads((ROOT/'tools/superpowers/assets.json').read_text())['assets']
        source=(MOD/'localisation/english/ac_superpower_programmes_l_english.yml').read_text(encoding='utf-8-sig')
        cls.loc=dict(re.findall(r'^ ([^ :]+):0 "(.*)"$',source,re.M))

    def test_exact_96_nodes_all_alternative_imports_dates_and_actual_branch_links(self):
        self.assertEqual(96,len(self.focuses));self.assertEqual(Counter(OSE=48,YUK=48),Counter(k[:3]for k in self.focuses))
        for tag in COUNTRIES:
            expected={focus_id(b,i)for b in BRANCHES if b.tag==tag for i in range(6)}
            trees=[v for k,_,v in parse((MOD/'common/national_focus'/f'{tag}.txt').read_text())if k=='focus_tree']
            self.assertEqual({'ose_focus','ose_mac_won'}if tag=='OSE'else{'yuk_reform_focus'},{get(t,'id')for t in trees})
            for tree in trees:
                imported=[v for k,_,v in tree if k=='shared_focus'and isinstance(v,str)and'_snp_'in v]
                self.assertEqual(expected,set(imported));self.assertEqual(48,len(imported))
        for b in BRANCHES:
            for i in range(6):
                ident=focus_id(b,i);node=self.focuses[ident]
                self.assertEqual('10'if i in(1,2,5)else'5',get(node,'cost'))
                self.assertGreaterEqual(len(self.loc[ident+'_desc'].replace('\\n','\n').split()),90)
                reward=get(node,'completion_reward')
                self.assertEqual([[ident+'_apply','=','yes']],get(reward,'hidden_effect'))
                self.assertIn(get(reward,'custom_effect_tooltip'),self.loc)
                self.assertEqual(build.prerequisites(b,i),[v for k,_,v in get(node,'prerequisite',[])if k=='focus'])
                if i in(1,2):self.assertEqual(focus_id(b,3-i),get(get(node,'mutually_exclusive'),'focus'))
                for key,_,ref in descend(node):
                    if key=='focus':self.assertIn(ref,self.focuses)

    def test_foreign_national_ast_is_preserved_except_owned_imports_and_panel_positions(self):
        contract=json.loads((ROOT/'tools/superpowers/tree_contracts.json').read_text())
        for tag,row in contract['countries'].items():
            source=parse((MOD/'common/national_focus'/f'{tag}.txt').read_text())
            for key,_,tree in source:
                if key=='focus_tree':tree[:]=[r for r in tree if r[0]!='continuous_focus_position'and not(r[0]=='shared_focus'and isinstance(r[2],str)and'_snp_'in r[2])]
            digest=hashlib.sha256(json.dumps(source,separators=(',',':')).encode()).hexdigest()
            self.assertEqual(row['normalized_foreign_ast_sha256'],digest,tag)

    def test_original_assets_are_complete_and_every_row_uses_its_native_aperture(self):
        self.assertEqual(320,len(self.assets));self.assertEqual(Counter({'focus':96,'idea':136,'decision row':68,'category':2,'event illustration':18}),Counter(a['role']for a in self.assets))
        sprites={get(v,'name').strip('"'):v for k,_,v in get(parse((MOD/'interface/ac_superpower_programmes.gfx').read_text()),'spriteTypes')}
        self.assertEqual(416,len(sprites));self.assertEqual(96,len({a['sha256']for a in self.assets if a['role']=='focus'}))
        dims={'focus':(96,96),'idea':(75,75),'decision row':(26,29),'category':(100,100),'event illustration':(640,260)}
        for a in self.assets:
            path=MOD/a['file'];image=Image.open(path).convert('RGBA');self.assertEqual(dims[a['role']],image.size)
            self.assertEqual((1,image.width),(a['frames'],a['frame_width']));self.assertEqual(a['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(a['file'],get(sprites[a['sprite']],'texturefile').strip('"'));self.assertEqual((a['alpha_min'],a['alpha_max']),image.getchannel('A').getextrema())
            if a['role']!='event illustration':self.assertEqual(0,image.getpixel((0,0))[3]);self.assertGreater(image.getchannel('A').getbbox()[2],image.width//2)
            if'master'in a:self.assertTrue((ROOT/a['master']).is_file())
        for _,_,rows in parse((MOD/'common/decisions/ac_superpower_programmes.txt').read_text()):
            for ident,_,node in rows:
                binding='GFX_decision_'+get(node,'icon');self.assertIn(binding,sprites)
                self.assertEqual('decision row',next(a['role']for a in self.assets if a['sprite']==binding))

    def test_english_narratives_callbacks_font_glyphs_and_runtime_bindings_resolve(self):
        self.assertTrue((MOD/'localisation/english/ac_superpower_programmes_l_english.yml').read_bytes().startswith(b'\xef\xbb\xbf'))
        events=[v for k,_,v in parse((MOD/'events/ac_superpower_programmes.txt').read_text())if k=='country_event']
        self.assertEqual(68,len(events));self.assertEqual(32,sum(get(e,'hidden')=='yes'for e in events))
        sprites={a['sprite']for a in self.assets}
        for node in events:
            if get(node,'hidden')=='yes':continue
            for key in('title','desc'):self.assertIn(get(node,key),self.loc)
            self.assertGreaterEqual(len(self.loc[get(node,'desc')].replace('\\n','\n').split()),90);self.assertIn(get(node,'picture'),sprites)
            for key,_,body in node:
                if key=='option':self.assertIn(get(body,'name'),self.loc)
        defined={get(v,'name')for k,_,v in parse((MOD/'common/custom_localization/ac_superpower_programmes.txt').read_text())}
        for _,_,node in parse((MOD/'common/custom_localization/ac_superpower_programmes.txt').read_text()):
            for key,_,value in node:
                if key=='text':self.assertIn(get(value,'localization_key'),self.loc)
        for value in self.loc.values():
            for name in re.findall(r'\[(?!\?)([A-Za-z0-9_]+)\]',value):self.assertIn(name,defined)
        font=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text();glyphs=set(map(int,re.findall(r'^char id=(\d+)',font,re.M)))
        self.assertFalse({ord(c)for value in self.loc.values()for c in value if c not in'\r\n\t'}-glyphs)

    def test_policy_costs_remain_and_wartime_variants_are_deliberately_reduced(self):
        ideas=dict((k,v)for k,_,v in get(get(parse((MOD/'common/ideas/ac_superpower_programmes.txt').read_text()),'ideas'),'country'))
        self.assertEqual(136,len(ideas))
        for ident,node in ideas.items():
            self.assertEqual('no',get(get(node,'allowed_civil_war'),'always'));self.assertEqual('-1',get(node,'removal_cost'))
            self.assertIn(ident,self.loc);self.assertIn(ident+'_desc',self.loc)
        for b in BRANCHES:
            for i,(_,benefits,costs)in enumerate(b.policies,1):
                ident=focus_id(b,i)+'_spirit';base=dict((k,float(v))for k,_,v in get(ideas[ident],'modifier'));settled=dict((k,float(v))for k,_,v in get(ideas[ident+'_settled'],'modifier'))
                for key,value in costs.items():self.assertEqual(value,base[key]);self.assertEqual(value,settled[key])
                for key,value in benefits.items():self.assertEqual(round(value*1.2,3),settled[key])
        for s in SERVICES:
            ordinary=dict((k,float(v))for k,_,v in get(ideas[s.id+'_spirit'],'modifier'));domestic=dict((k,float(v))for k,_,v in get(ideas[s.id+'_domestic_spirit'],'modifier'))
            self.assertEqual(s.modifiers,ordinary);self.assertEqual({k:round(v*.65,3)for k,v in ordinary.items()},domestic)

    def test_every_non_service_spirit_has_a_distinct_real_countervailing_modifier(self):
        lower_is_better={'consumer_goods_factor','supply_consumption_factor'}
        ideas=get(get(parse((MOD/'common/ideas/ac_superpower_programmes.txt').read_text()),'ideas'),'country')
        checked=0
        for ident,_,node in ideas:
            if'_service_'in ident:continue # Explicitly paid90-day periods, separately cost-tested.
            values={k:float(v)for k,_,v in get(node,'modifier')}
            favorable={k for k,v in values.items()if v<0 and k in lower_is_better or v>0 and k not in lower_is_better}
            adverse={k for k,v in values.items()if v>0 and k in lower_is_better or v<0 and k not in lower_is_better}
            self.assertTrue(favorable,ident);self.assertTrue(adverse,ident);self.assertFalse(favorable&adverse,ident)
            checked+=1
        self.assertEqual(72,checked)

    def test_owned_provenance_profile_pins_exactly_320_resources_without_family_exemptions(self):
        profile=json.loads((ROOT/'tools/superpowers/audit_profile.json').read_text())
        self.assertEqual([],profile['enabled_dlc']);self.assertEqual([],profile['provider_overrides']);self.assertEqual([],profile['payload_overrides'])
        records=profile['provenance'];self.assertEqual(320,len(records))
        self.assertEqual({a['file']:a['sha256']for a in self.assets},{r['path']:r['sha256']for r in records})
        for row in records:
            self.assertEqual(('mod','authored'),(row['provider'],row['classification']));self.assertNotRegex(row['path'],r'[*?\[]');self.assertTrue(row['reason']);self.assertTrue(row['evidence'])

    def test_all_continuous_panels_clear_resolved_nodes_and_fit_the_expanded_canvas(self):
        spec=importlib.util.spec_from_file_location('snp_geometry',ROOT/'tools/Test-FocusScreenRepairs.py');geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
        positions=geometry.resolved_tree_positions();gui=parse((MOD/'interface/nationalfocusview.gui').read_text());panel=geometry.named(gui,'continuous_focus_window');size=get(panel,'size');pw=int(get(size,'width'));ph=int(get(size,'height'))
        for tag in COUNTRIES:
            for kind,_,tree in parse((MOD/'common/national_focus'/f'{tag}.txt').read_text()):
                if kind!='focus_tree':continue
                pos=get(tree,'continuous_focus_position');px=int(get(pos,'x'));py=int(get(pos,'y'));nodes=positions[get(tree,'id')]
                self.assertLessEqual(px+pw,max(x*96+169 for x,y in nodes.values()));self.assertLessEqual(py+ph,max(y*160+154 for x,y in nodes.values()))
                for ident,(x,y)in nodes.items():self.assertFalse(x*96<px+pw and x*96+169>px and y*160<py+ph and y*160+154>py,(tag,ident))

    def test_only_owned_state_and_public_capacity_inputs_are_written(self):
        nodes=parse((MOD/'common/scripted_effects/ac_superpower_programmes.txt').read_text())
        forbidden={'set_global_flag','clr_global_flag','add_building_construction','add_resource','add_equipment_to_stockpile','add_manpower','set_owner','transfer_state','declare_war_on','add_to_faction','create_faction','load_focus_tree','recruit_character','set_politics'}
        self.assertFalse(forbidden&{k for k,_,v in descend(nodes)})
        for key,_,value in descend(nodes):
            if key in('set_variable','add_to_variable','subtract_from_variable','set_temp_variable','add_to_temp_variable','subtract_from_temp_variable'):
                self.assertTrue(value[0][0].startswith('ac_snp_')or value[0][0]=='ac_pol_capacity_delta',(key,value))
            if key in('set_country_flag','clr_country_flag'):
                name=get(value,'flag')if isinstance(value,list)else value
                self.assertTrue(name.startswith(('ac_snp_','OSE_snp_','YUK_snp_')),name)
        actions=get(parse((MOD/'common/on_actions/ac_superpower_programmes.txt').read_text()),'on_actions')
        self.assertEqual([['ac_snp_weekly','=','yes']],get(get(actions,'on_weekly'),'effect'));self.assertNotIn('every_country',{k for k,_,v in descend(actions)})

    def test_primary_modifier_contract_covers_actual_values_and_no_strategic_owner_alias_is_created(self):
        contract=json.loads((ROOT/'tools/superpowers/engine_contracts.json').read_text())
        ideas=get(get(parse((MOD/'common/ideas/ac_superpower_programmes.txt').read_text()),'ideas'),'country')
        actual={k for _,_,node in ideas for k,_,v in get(node,'modifier')};self.assertEqual(actual,{x['id']for x in contract['modifiers']})
        self.assertEqual('1.19.4.1',contract['version']);self.assertNotIn('air_experience_gain_factor',actual)
        for family in('scripted_effects','scripted_triggers'):
            for key,_,node in parse((MOD/'common'/family/'ac_superpower_programmes.txt').read_text()):self.assertFalse(key.startswith('ac_sp_'),key)

    def test_player_effects_hide_bookkeeping_and_costs_fit_the_actual_row_text_area(self):
        from reconstruction.build_art import BitmapFont
        font=BitmapFont()
        for _,_,entries in parse((MOD/'common/decisions/ac_superpower_programmes.txt').read_text()):
            for ident,_,node in entries:
                shown=get(node,'complete_effect');self.assertIn(get(shown,'custom_effect_tooltip'),self.loc)
                self.assertIsNotNone(get(shown,'hidden_effect'))
                self.assertTrue(all(k in('custom_effect_tooltip','hidden_effect')for k,_,v in shown))
                title=self.loc[ident];line='';lines=1
                for word in title.split():
                    candidate=(line+' '+word).strip()
                    if line and font.width(candidate)>356:lines+=1;line=word
                    else:line=candidate
                self.assertLessEqual(lines*font.height,54,ident)
                if get(node,'custom_cost_text'):self.assertIn(get(node,'custom_cost_text'),self.loc)
        for key in('ac_snp_cost_35','ac_snp_cost_30','ac_snp_cost_15','ac_snp_cost_10','ac_snp_cost_consult','ac_snp_cost_yuk'):
            value=self.loc[key];self.assertLessEqual(font.width(value.replace('£pol_power',''))+24,180,key)

    def test_both_generator_orders_preserve_all_foreign_tails_and_old_contracts(self):
        script=r'''
import sys,tempfile
from pathlib import Path
sys.path[:0]=[str(Path.cwd()/'tools/usea_expansion'),str(Path.cwd()/'tools')]
import build_content as exp
import build_peace_we_inherit as pwi
from superpowers import build as snp
from reconstruction import build as rc
with tempfile.TemporaryDirectory()as folder:
 scratch=Path(folder);original=exp.MOD
 files=['NPT.txt','REC.txt','YUK.txt','NPT_pre_continental_war.txt','ac_usean_rebellion.txt','SAP.txt','GEB.txt','ac_belkan_campaign.txt','OSE.txt','UST.txt']
 for name in files:
  p=scratch/'common/national_focus'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((original/'common/national_focus'/name).read_bytes())
 exp.MOD=pwi.MOD=snp.MOD=rc.MOD=scratch
 extra='\n# Independent synthetic owner; keep this trailer byte-for-byte.\nshared_focus = { id = synthetic_foreign_focus x = 99 y = 99 }\n'
 for tag in('OSE','YUK'):
  p=scratch/'common/national_focus'/f'{tag}.txt';p.write_text(p.read_text()+extra)
 def expansion():
  exp.OUT.clear();exp.LOC.clear();exp.build_trees()
  for relative,text in exp.OUT.items():(scratch/relative).write_text(text)
 def aftermath():
  pwi.OUTPUT.clear();pwi.attach_focuses()
  for relative,text in pwi.OUTPUT.items():(scratch/relative).write_text(text)
 def national():
  for tag in('OSE','YUK'):
   p=scratch/'common/national_focus'/f'{tag}.txt';p.write_text(snp.attach(p.read_text(),tag))
 def reconstruction():
  for tag in rc.COUNTRY_NAMES:
   p=scratch/'common/national_focus'/f'{tag}.txt';p.write_text(rc.attach(p.read_text(),tag))
 expansion();aftermath();reconstruction();national()
 before={p.relative_to(scratch):p.read_bytes()for p in scratch.rglob('*.txt')}
 for action in(national,reconstruction,aftermath,expansion,national,aftermath,reconstruction,expansion):action()
 assert before=={p.relative_to(scratch):p.read_bytes()for p in scratch.rglob('*.txt')}
 for tag in('OSE','YUK'):assert extra in(scratch/'common/national_focus'/f'{tag}.txt').read_text()
 p=scratch/'common/national_focus/OSE.txt';p.write_text(p.read_text().replace(snp.BEGIN,snp.BEGIN+'\n shared_focus = synthetic_foreign_focus',1))
 try:national()
 except ValueError:pass
 else:raise AssertionError('Foreign content inside an owned SNP section was accepted')
'''
        result=subprocess.run([sys.executable,'-B','-c',script],cwd=ROOT,capture_output=True,text=True);self.assertEqual(0,result.returncode,result.stdout+result.stderr)

    def test_reproducible_compiled_content_and_all_original_artwork(self):
        for command in(['tools/superpowers/build.py','--check'],['tools/superpowers/build_art.py','--check']):
            result=subprocess.run([sys.executable,'-B']+command,cwd=ROOT,capture_output=True,text=True);self.assertEqual(0,result.returncode,result.stdout+result.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
