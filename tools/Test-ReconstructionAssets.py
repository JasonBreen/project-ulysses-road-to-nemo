"""Offline source, generator, layout and original-art closure for RC60."""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from reconstruction import build
from reconstruction.content import BRANCHES,COUNTRY_NAMES,branch_id,focus_id
from usea_expansion.script import parse,get


def descend(nodes):
    for row in nodes:
        yield row
        if isinstance(row[2],list):yield from descend(row[2])


class ReconstructionAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.focuses={get(v,'id'):v for k,_,v in parse((MOD/'common/national_focus/ac_reconstruction_continuations.txt').read_text()) if k=='shared_focus'}
        cls.assets=json.loads((ROOT/'tools/reconstruction/assets.json').read_text())['assets']
        source=(MOD/'localisation/english/ac_reconstruction_l_english.yml').read_text(encoding='utf-8-sig')
        cls.loc=dict(re.findall(r'^ ([^ :]+):0 "(.*)"$',source,re.M))

    def test_sixty_exact_imports_prerequisites_exclusions_and_meaningful_rewards(self):
        self.assertEqual(60,len(self.focuses))
        self.assertEqual(Counter(NPT=18,REC=18,SAP=12,GEB=12),Counter(x[:3] for x in self.focuses))
        for b in BRANCHES:
            for i in range(6):
                ident=focus_id(b,i);node=self.focuses[ident]
                self.assertEqual('10' if i in (1,2,5) else '5',get(node,'cost'))
                self.assertEqual([[ident+'_apply','=','yes']],get(node,'completion_reward'))
                self.assertGreaterEqual(len(self.loc[ident+'_desc'].split()),18)
                refs=[v for k,_,v in descend(node) if k=='focus']
                for ref in refs:
                    self.assertTrue(ref in self.focuses or ref==b.entry,(ident,ref))
                if i in (1,2):self.assertEqual(focus_id(b,3-i),get(get(node,'mutually_exclusive'),'focus'))
            tree=get(parse((MOD/'common/national_focus'/f'{b.tag}.txt').read_text()),'focus_tree')
            imports=[v for k,_,v in tree if k=='shared_focus' and isinstance(v,str)]
            for i in range(6):self.assertEqual(1,imports.count(focus_id(b,i)))

    def test_policy_improvements_keep_the_same_cost_and_all_spirits_forbid_clone_inheritance(self):
        ideas=get(get(parse((MOD/'common/ideas/ac_reconstruction.txt').read_text()),'ideas'),'country')
        self.assertEqual(96,len(ideas));lookup=dict((k,v) for k,_,v in ideas)
        for ident,node in lookup.items():
            self.assertEqual('no',get(get(node,'allowed_civil_war'),'always'));self.assertEqual('-1',get(node,'removal_cost'))
            self.assertIn(ident,self.loc);self.assertIn(ident+'_desc',self.loc)
        for b in BRANCHES:
            for p,(_,benefits,costs) in enumerate(b.policies,1):
                ident=focus_id(b,p)+'_spirit'
                base=dict((k,float(v))for k,_,v in get(lookup[ident],'modifier'))
                settled=dict((k,float(v))for k,_,v in get(lookup[ident+'_settled'],'modifier'))
                for key,value in costs.items():self.assertEqual(value,base[key]);self.assertEqual(value,settled[key])
                for key,value in benefits.items():self.assertEqual(round(value*1.2,3),settled[key])

    def test_complete_art_binding_frames_alpha_apertures_and_original_masters(self):
        self.assertEqual(198,len(self.assets));self.assertEqual(Counter({'focus':60,'idea':96,'decision row':24,'category':4,'event illustration':14}),Counter(a['role']for a in self.assets))
        sprites={get(v,'name').strip('"'):v for k,_,v in get(parse((MOD/'interface/ac_reconstruction.gfx').read_text()),'spriteTypes')}
        self.assertEqual(258,len(sprites));self.assertEqual(60,len({a['sha256']for a in self.assets if a['role']=='focus'}))
        dimensions={'focus':(96,96),'idea':(75,75),'decision row':(26,29),'category':(100,100),'event illustration':(640,260)}
        for a in self.assets:
            path=MOD/a['file'];image=Image.open(path).convert('RGBA')
            self.assertEqual(dimensions[a['role']],image.size);self.assertEqual(1,a['frames']);self.assertEqual(image.width,a['frame_width'])
            self.assertEqual(a['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(a['file'],get(sprites[a['sprite']],'texturefile').strip('"'))
            self.assertEqual((a['alpha_min'],a['alpha_max']),image.getchannel('A').getextrema())
            if a['role']!='event illustration':
                self.assertEqual(0,image.getpixel((0,0))[3]);self.assertGreater(image.getchannel('A').getbbox()[2],image.width//2)
            if 'master'in a:self.assertTrue((ROOT/a['master']).is_file())
        for _,_,entries in parse((MOD/'common/decisions/ac_reconstruction.txt').read_text()):
            for ident,_,node in entries:
                # This is the actual unprefixed engine row-icon convention.
                binding='GFX_decision_'+get(node,'icon');self.assertIn(binding,sprites)
                a=next(a for a in self.assets if a['sprite']==binding);self.assertEqual('decision row',a['role'])

    def test_english_events_callbacks_flags_and_all_runtime_pictures_resolve(self):
        events=[v for k,_,v in parse((MOD/'events/ac_reconstruction.txt').read_text()) if k=='country_event'];self.assertEqual(28,len(events))
        sprites={a['sprite']for a in self.assets}
        for node in events:
            for key in ('title','desc'):self.assertIn(get(node,key),self.loc)
            self.assertIn(get(node,'picture'),sprites)
            self.assertGreaterEqual(len(self.loc[get(node,'desc')].split()),80)
            for key,_,value in node:
                if key=='option':self.assertIn(get(value,'name'),self.loc)
        for _,_,node in parse((MOD/'common/custom_localization/ac_reconstruction.txt').read_text()):
            for key,_,value in node:
                if key=='text':self.assertIn(get(value,'localization_key'),self.loc)
        for relative in ('common/scripted_effects/ac_reconstruction.txt','common/scripted_triggers/ac_reconstruction.txt'):
            for key,_,value in descend(parse((MOD/relative).read_text())):
                if key=='has_country_flag' and ('_rc_'in value or value.startswith('ac_rc_')):self.assertIn(value,self.loc)

    def test_continuous_panels_clear_every_resolved_node_and_fit_canvas_extent(self):
        spec=importlib.util.spec_from_file_location('rc_focus_geometry',ROOT/'tools/Test-FocusScreenRepairs.py')
        geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
        all_positions=geometry.resolved_tree_positions()
        gui=parse((MOD/'interface/nationalfocusview.gui').read_text())
        panel=geometry.named(gui,'continuous_focus_window');size=get(panel,'size');pw=int(get(size,'width'));ph=int(get(size,'height'))
        for tag in COUNTRY_NAMES:
            tree=get(parse((MOD/'common/national_focus'/f'{tag}.txt').read_text()),'focus_tree')
            pos=get(tree,'continuous_focus_position');px=int(get(pos,'x'));py=int(get(pos,'y'));nodes=all_positions[build.TREE_IDS[tag]]
            self.assertLessEqual(px+pw,max(x*96+169 for x,y in nodes.values()))
            self.assertLessEqual(py+ph,max(y*160+154 for x,y in nodes.values()))
            for ident,(x,y) in nodes.items():
                left=x*96;top=y*160
                self.assertFalse(left<px+pw and left+169>px and top<py+ph and top+154>py,(tag,ident))

    def test_generators_preserve_foreign_sections_and_are_order_independent(self):
        # Isolated source-only fixture: no actual mod or private user data.
        script=r'''
import sys,tempfile
from pathlib import Path
sys.path[:0]=[str(Path.cwd()/'tools/usea_expansion'),str(Path.cwd()/'tools')]
import build_content as exp
from reconstruction import build as rc
import build_peace_we_inherit as pwi
with tempfile.TemporaryDirectory() as folder:
    scratch=Path(folder);original=exp.MOD
    files=['NPT.txt','REC.txt','YUK.txt','NPT_pre_continental_war.txt','ac_usean_rebellion.txt','SAP.txt','GEB.txt','ac_belkan_campaign.txt','OSE.txt','UST.txt']
    for name in files:
        p=scratch/'common/national_focus'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((original/'common/national_focus'/name).read_bytes())
    exp.MOD=rc.MOD=pwi.MOD=scratch
    extra='\n# Foreign owner trailer must survive byte-for-byte.\nshared_focus = { id = synthetic_foreign_focus x = 99 y = 99 }\n'
    for name in ('NPT.txt','REC.txt','SAP.txt','GEB.txt','NPT_pre_continental_war.txt'):
        p=scratch/'common/national_focus'/name;p.write_text(p.read_text()+extra)
    def expansion():
        exp.OUT.clear();exp.LOC.clear();exp.build_trees()
        for relative,text in exp.OUT.items():(scratch/relative).write_text(text)
    def reconstruction():
        for tag in rc.COUNTRY_NAMES:
            p=scratch/'common/national_focus'/f'{tag}.txt';p.write_text(rc.attach(p.read_text(),tag))
    def aftermath():
        pwi.OUTPUT.clear();pwi.attach_focuses()
        for relative,text in pwi.OUTPUT.items():(scratch/relative).write_text(text)
    expansion();reconstruction();aftermath()
    before={p.relative_to(scratch):p.read_bytes() for p in scratch.rglob('*.txt')}
    for action in (aftermath,reconstruction,expansion,expansion,aftermath,reconstruction):action()
    assert before=={p.relative_to(scratch):p.read_bytes() for p in scratch.rglob('*.txt')}
    for name in ('NPT.txt','REC.txt','SAP.txt','GEB.txt','NPT_pre_continental_war.txt'):assert extra in (scratch/'common/national_focus'/name).read_text()
    # Historical unclosed owned marker is migrated by owned IDs, not tail split.
    p=scratch/'common/national_focus/REC.txt';p.write_text(p.read_text().replace('# END EXPANSION FOCUSES\n',''));expansion();assert extra in p.read_text()
    p.write_text(p.read_text().replace('# BEGIN EXPANSION IMPORTS','# BEGIN EXPANSION IMPORTS\n shared_focus = synthetic_foreign_focus'))
    try:expansion()
    except ValueError:pass
    else:raise AssertionError('Foreign content in an owned section must be rejected')
'''
        result=subprocess.run([sys.executable,'-B','-c',script],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)

    def test_owned_runtime_has_no_physical_grants_foreign_state_or_replaced_trees(self):
        effect=parse((MOD/'common/scripted_effects/ac_reconstruction.txt').read_text())
        forbidden={'add_building_construction','add_resource','add_equipment_to_stockpile','set_owner','transfer_state','create_faction','add_to_faction','load_focus_tree','set_politics','recruit_character','add_manpower','declare_war_on','set_global_flag','clr_global_flag'}
        self.assertFalse(forbidden & {k for k,_,v in descend(effect)})
        for key,_,value in descend(effect):
            if key in ('set_variable','add_to_variable','subtract_from_variable'):
                self.assertTrue(value[0][0].startswith('ac_rc_'),(key,value))
        actions=get(parse((MOD/'common/on_actions/ac_reconstruction.txt').read_text()),'on_actions')
        self.assertEqual([['ac_rc_weekly','=','yes']],get(get(actions,'on_weekly'),'effect'))
        self.assertNotIn('every_country',{k for k,_,v in descend(actions)})

    def test_every_modifier_and_interrupt_hook_has_a_captured_primary_contract(self):
        contract=json.loads((ROOT/'tools/reconstruction/engine_contracts.json').read_text())
        self.assertEqual('1.19.4.1',contract['version'])
        captured={row['id']for row in contract['modifiers']}
        ideas=get(get(parse((MOD/'common/ideas/ac_reconstruction.txt').read_text()),'ideas'),'country')
        actual={k for _,_,node in ideas for k,_,v in get(node,'modifier')}
        self.assertEqual(actual,captured);self.assertNotIn('air_experience_gain_factor',actual)
        actions=get(parse((MOD/'common/on_actions/ac_reconstruction.txt').read_text()),'on_actions')
        self.assertEqual(set(contract['interruption_hooks']),{k for k,_,v in actions if k not in ('on_weekly','on_startup')})
        for row in contract['modifiers']:
            self.assertTrue(row['primary_national_idea_source'].startswith('engine://'));self.assertRegex(row['source_sha256'],r'^[0-9a-f]{64}$')

    def test_reproducible_compiler_and_artwork(self):
        for command in (['tools/reconstruction/build.py','--check'],['tools/reconstruction/build_art.py','--check']):
            result=subprocess.run([sys.executable,'-B']+command,cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
