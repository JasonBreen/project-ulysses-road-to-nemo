"""Preserved source, exact national budgets and actual presentation consumers."""
from collections import Counter
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from pacific_nations.model import HERE,MOD,countries,branches,refs,positions
from pacific_nations import build,build_art
from superpowers import build as old
from usea_expansion.script import parse,get
from event_picture_fit.audit import audit as audit_event_pictures


def descend(nodes):
    for row in nodes:
        yield row
        if isinstance(row[2],list):yield from descend(row[2])


class NationalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out,cls.manifest=build.outputs();cls.focuses={};cls.loc={};cls.assets=[]
        for module in countries():
            stem='ac_snc_'+module.TAG.lower()
            cls.focuses.update({get(v,'id'):v for k,_,v in parse(cls.out['common/national_focus/'+stem+'.txt'])if k=='shared_focus'})
            cls.loc.update(dict(re.findall(r'^ ([^ :]+):0 "(.*)"$',cls.out['localisation/english/'+stem+'_l_english.yml'],re.M)))
            cls.assets.extend(json.loads((HERE/('assets_'+module.TAG+'.json')).read_text())['assets'])

    def test_exact_independent_country_budgets_existing_tree_alternatives_and_imports(self):
        for module in countries():
            tag=module.TAG;ids={b.focus(i)for b in module.BRANCHES for i in range(len(b.steps))}
            self.assertEqual(44 if tag=='OSE'else 42,len(ids));self.assertEqual(6,len(module.BRANCHES))
            trees=parse((MOD/'common/national_focus'/f'{tag}.txt').read_text())
            self.assertEqual({'ose_focus','ose_mac_won'}if tag=='OSE'else{'yuk_reform_focus'},{get(v,'id')for k,_,v in trees if k=='focus_tree'})
            for k,_,tree in trees:
                if k=='focus_tree':
                    actual=[v for key,_,v in tree if key=='shared_focus'and v.startswith(tag+'_snc_')]
                    self.assertEqual(ids,set(actual));self.assertEqual(len(ids),len(actual))
                    self.assertEqual(48,len([v for key,_,v in tree if key=='shared_focus'and'_snp_'in v]))

    def test_prerequisites_exclusions_dates_and_every_individual_description(self):
        known=set(self.focuses)|{get(v,'id')for k,_,v in parse((MOD/'common/national_focus/ac_superpower_programmes.txt').read_text())if k=='shared_focus'}
        for b in branches():
            for i,suffix in enumerate(b.suffixes):
                ident=b.focus(i);node=self.focuses[ident]
                self.assertEqual(refs(b,i),[v for k,_,v in get(node,'prerequisite',[])])
                self.assertGreaterEqual(len(self.loc[ident+'_desc'].split()),80)
                self.assertEqual('10'if suffix in('civil','protected','settlement')else'5',get(node,'cost'))
                self.assertIn('date < '+b.opens,self.out['common/scripted_effects/ac_snc_'+b.tag.lower()+'.txt'])
                for key,_,value in descend(node):
                    if key=='focus':self.assertIn(value,known)
                exclusions=get(node,'mutually_exclusive',[])
                if exclusions:
                    other=get(exclusions,'focus');self.assertEqual(ident,get(get(self.focuses[other],'mutually_exclusive'),'focus'))
                self.assertEqual([[ident+'_apply','=','yes']],get(get(node,'completion_reward'),'hidden_effect'))
        # Actual owner graph; an added cycle must be rejected by this traversal.
        def acyclic(nodes):
            visiting=set();done=set()
            def visit(name):
                if name in visiting:raise ValueError('Focus cycle '+name)
                if name in done or name not in nodes:return
                visiting.add(name)
                for key,_,body in nodes[name]:
                    if key=='prerequisite':
                        for field,_,other in body:
                            if field=='focus':visit(other)
                visiting.remove(name);done.add(name)
            for name in nodes:visit(name)
        acyclic(self.focuses);bad=copy.deepcopy(self.focuses);first=next(iter(bad));bad[first].append(['prerequisite','=',[['focus','=',first]]])
        with self.assertRaisesRegex(ValueError,'Focus cycle'):acyclic(bad)

    def test_strict_registered_seam_preserves_old_source_and_rejects_unknown_content(self):
        for module in countries():
            tag=module.TAG;source=(MOD/'common/national_focus'/f'{tag}.txt').read_text();original=build.strip_imports(parse(source),tag)
            self.assertEqual(source,build.attach(source,tag));self.assertEqual(source,old.attach(source,tag))
            for transform in(lambda value:build.attach(old.attach(value,tag),tag),lambda value:old.attach(build.attach(value,tag),tag)):
                self.assertEqual(source,transform(source))
            bad=parse(source);tree=next(v for k,_,v in bad if k=='focus_tree');tree.append(['shared_focus','=',tag+'_snc_unregistered'])
            with self.assertRaisesRegex(ValueError,'Unregistered/missing'):build.strip_imports(bad,tag)
            bad=copy.deepcopy(original);tree=next(v for k,_,v in bad if k=='focus_tree');next(r for r in tree if r[0]=='id')[2]='changed_foreign_tree'
            self.assertNotEqual(original,bad)
            injected=source.replace(build.BEGIN,build.BEGIN+'\nshared_focus = synthetic_foreign_focus',1)
            with self.assertRaisesRegex(ValueError,'Foreign node'):build.attach(injected,tag)

    def test_only_owned_state_and_public_capacity_input_are_written(self):
        forbidden={'declare_war_on','white_peace','start_peace_conference','transfer_state','annex_country','add_to_faction','create_faction','set_politics','recruit_character','add_building_construction','add_resource','add_manpower','add_equipment_to_stockpile','set_global_flag','clr_global_flag'}
        for module in countries():
            stem='ac_snc_'+module.TAG.lower();nodes=parse(self.out['common/scripted_effects/'+stem+'.txt'])
            self.assertFalse(forbidden&{k for k,_,v in descend(nodes)})
            for key,_,value in descend(nodes):
                if key in('set_variable','add_to_variable','subtract_from_variable','set_temp_variable'):
                    self.assertTrue(value[0][0].startswith('ac_snc_')or value[0][0]=='ac_pol_capacity_delta',(key,value))
                if key in('set_country_flag','clr_country_flag'):
                    name=get(value,'flag')if isinstance(value,list)else value;self.assertTrue(name.startswith((stem,module.TAG+'_snc_')),name)
            actions=get(parse(self.out['common/on_actions/'+stem+'.txt']),'on_actions')
            self.assertEqual([[stem+'_weekly','=','yes']],get(get(actions,'on_weekly'),'effect'))
            self.assertNotIn('every_country',{k for k,_,v in descend(actions)})

    def test_all_enduring_and_narrative_spirits_have_distinct_real_costs(self):
        lower={'consumer_goods_factor','supply_consumption_factor'}
        captured={row['id']for row in json.loads((ROOT/'tools/superpowers/engine_contracts.json').read_text())['modifiers']}
        for module in countries():
            ideas=get(get(parse(self.out['common/ideas/ac_snc_'+module.TAG.lower()+'.txt']),'ideas'),'country')
            for ident,_,node in ideas:
                self.assertEqual('no',get(get(node,'allowed_civil_war'),'always'));values={k:float(v)for k,_,v in get(node,'modifier')}
                good={k for k,v in values.items()if v<0 and k in lower or v>0 and k not in lower};bad={k for k,v in values.items()if v>0 and k in lower or v<0 and k not in lower}
                self.assertTrue(good,ident);self.assertTrue(bad,ident);self.assertFalse(good&bad);self.assertTrue(set(values)<=captured,(ident,set(values)-captured))
            for b in module.BRANCHES:
                for lane,(_,benefit,cost)in enumerate(b.policies,1):
                    name=b.id+('_civil'if lane==1 else'_protected')+'_spirit';current={k:v for k,_,v in get(next(v for k,_,v in ideas if k==name),'modifier')};settled={k:v for k,_,v in get(next(v for k,_,v in ideas if k==name+'_settled'),'modifier')}
                    for key,value in cost.items():self.assertEqual(float(value),float(current[key]));self.assertEqual(float(value),float(settled[key]))

    def test_every_english_scene_callback_picture_option_and_flag_resolves(self):
        sprites={a['sprite']for a in self.assets};font=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text();glyphs=set(map(int,re.findall(r'^char id=(\d+)',font,re.M)))
        for module in countries():
            stem='ac_snc_'+module.TAG.lower();raw=(MOD/'localisation/english'/(stem+'_l_english.yml')).read_bytes();self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            events=[v for k,_,v in parse(self.out['events/'+stem+'.txt'])if k=='country_event'];self.assertEqual(14,len(events))
            custom={get(v,'name')for k,_,v in parse(self.out['common/custom_localization/'+stem+'.txt'])}
            for node in events:
                self.assertIn(get(node,'picture'),sprites)
                for key in('title','desc'):self.assertIn(get(node,key),self.loc)
                self.assertGreaterEqual(len(self.loc[get(node,'desc')].split()),80)
                for key,_,option in node:
                    if key=='option':self.assertIn(get(option,'name'),self.loc)
            for text in self.loc.values():
                for name in re.findall(r'\[(?!\?)([A-Za-z0-9_]+)\]',text):
                    if name.startswith(stem):self.assertIn(name,custom)
            for key,_,value in descend(parse(self.out['common/scripted_effects/'+stem+'.txt'])):
                if key=='has_country_flag'and value.startswith((stem,module.TAG+'_snc_')):self.assertIn(value,self.loc)
        self.assertFalse({ord(c)for value in self.loc.values()for c in value if c not in'\r\n\t'}-glyphs)

    def test_actual_textures_frames_alpha_masters_and_all_unprefixed_row_bindings(self):
        dims={'focus':(96,96),'idea':(75,75),'decision row':(26,29),'category':(100,100),'event illustration':(210,176)}
        for module in countries():
            assets=json.loads((HERE/('assets_'+module.TAG+'.json')).read_text())['assets'];sprites={get(v,'name').strip('"'):v for k,_,v in get(parse((MOD/'interface'/('ac_snc_'+module.TAG.lower()+'.gfx')).read_text()),'spriteTypes')}
            focuses=[a for a in assets if a['role']=='focus'];self.assertEqual(44 if module.TAG=='OSE'else 42,len(focuses));self.assertEqual(len(focuses),len({a['sha256']for a in focuses}))
            for a in assets:
                path=MOD/a['file']
                with Image.open(path)as im:
                    image=im.convert('RGBA');self.assertEqual(dims[a['role']],image.size);self.assertEqual((a['alpha_min'],a['alpha_max']),image.getchannel('A').getextrema())
                    if a['role']!='event illustration':self.assertEqual(0,image.getpixel((0,0))[3])
                self.assertEqual((1,a['width']),(a['frames'],a['frame_width']));self.assertEqual(a['sha256'],hashlib.sha256(path.read_bytes()).hexdigest());self.assertEqual(a['file'],get(sprites[a['sprite']],'texturefile').strip('"'))
                if'master'in a:self.assertTrue((ROOT/a['master']).is_file())
            for _,_,rows in parse(self.out['common/decisions/ac_snc_'+module.TAG.lower()+'.txt']):
                for ident,_,node in rows:
                    binding='GFX_decision_'+get(node,'icon');self.assertIn(binding,sprites);self.assertEqual('decision row',next(a['role']for a in assets if a['sprite']==binding))

    def test_actual_country_event_consumers_fit_and_keep_complete_wide_masters(self):
        modules=countries()
        report=audit_event_pictures(['events/ac_snc_'+module.TAG.lower()+'.txt'for module in modules])
        self.assertEqual(14*len(modules),report['explicit_consumers'])
        self.assertTrue(all(row['hidden']for row in report['implicit_picture_events']))
        for row in report['consumers']:
            self.assertEqual('country_event',row['event_type'])
            self.assertEqual([210.0,176.0],row['frame_size'])
            self.assertEqual([5.0,5.0,215.0,181.0],row['bounds'])
        for module in modules:
            assets=json.loads((HERE/('assets_'+module.TAG+'.json')).read_text())['assets']
            for asset in (row for row in assets if row['role']=='event illustration'):
                with self.subTest(country=module.TAG,event=asset['id']):
                    with Image.open(ROOT/asset['master'])as master:
                        self.assertEqual((640,260),master.size)
                        full=ImageOps.contain(master.convert('RGBA'),(210,176),Image.Resampling.LANCZOS)
                    expected=Image.new('RGBA',(210,176),(8,22,33,255))
                    expected.alpha_composite(full,((210-full.width)//2,(176-full.height)//2))
                    with Image.open(MOD/asset['file'])as delivered:
                        self.assertEqual(expected.tobytes(),delivered.convert('RGBA').tobytes())

    def test_exact_hash_provenance_has_no_family_or_filename_exemption(self):
        for module in countries():
            assets=json.loads((HERE/('assets_'+module.TAG+'.json')).read_text())['assets'];profile=json.loads((HERE/('audit_'+module.TAG+'.json')).read_text())
            self.assertEqual([],profile['enabled_dlc']);self.assertEqual([],profile['provider_overrides']);self.assertEqual({a['file']:a['sha256']for a in assets},{p['path']:p['sha256']for p in profile['provenance']})
            for row in profile['provenance']:self.assertEqual(('mod','authored'),(row['provider'],row['classification']));self.assertNotRegex(row['path'],r'[*?\[]');self.assertTrue(row['evidence'])

    def test_portable_png_equality_rejects_changed_pixels_and_dimensions(self):
        a=Image.new('RGBA',(8,9),(8,22,33,255));buffers=[]
        for compression in(0,9):
            stream=io.BytesIO();a.save(stream,format='PNG',compress_level=compression);buffers.append(stream.getvalue())
        self.assertNotEqual(*buffers);self.assertTrue(build_art.same_png(*buffers))
        changed=a.copy();changed.putpixel((1,1),(9,22,33,255));stream=io.BytesIO();changed.save(stream,format='PNG');self.assertFalse(build_art.same_png(buffers[0],stream.getvalue()))
        stream=io.BytesIO();a.resize((9,8)).save(stream,format='PNG');self.assertFalse(build_art.same_png(buffers[0],stream.getvalue()))

    def test_actual_git_filters_keep_every_original_png_binary_and_reject_text_override(self):
        def identities(path,cwd):
            raw=subprocess.check_output(['git','hash-object','--no-filters',str(path)],cwd=cwd,text=True).strip()
            filtered=subprocess.check_output(['git','hash-object','--path='+str(path),str(path)],cwd=cwd,text=True).strip()
            return raw,filtered
        files=sorted((HERE/'source').rglob('*.png'))+sorted((HERE/'gallery').glob('*.png'))
        self.assertTrue(files)
        for path in files:self.assertEqual(*identities(path.relative_to(ROOT),ROOT),str(path.relative_to(ROOT)))
        # Exercise Git's real clean filter, rather than trusting a claimed
        # 'binary' macro that a later folder-wide text rule can override.
        with tempfile.TemporaryDirectory()as temporary:
            scratch=Path(temporary);subprocess.run(['git','init','--quiet'],cwd=scratch,check=True,capture_output=True)
            fixture=Image.new('RGBA',(8,9),(8,22,33,255));fixture.save(scratch/'fixture.png')
            (scratch/'.gitattributes').write_text('*.png binary\n* text eol=lf\n',encoding='utf-8')
            self.assertNotEqual(*identities(Path('fixture.png'),scratch))
            (scratch/'.gitattributes').write_text('*.png binary\n',encoding='utf-8')
            self.assertEqual(*identities(Path('fixture.png'),scratch))

    def test_source_art_reproduction_and_effect_tooltip_cost_contract(self):
        for relative,text in self.out.items():self.assertEqual(text,(MOD/relative).read_text(encoding='utf-8'))
        font=build_art.BitmapFont()
        for module in countries():
            stem='ac_snc_'+module.TAG.lower()
            for _,_,rows in parse(self.out['common/decisions/'+stem+'.txt']):
                for ident,_,node in rows:
                    self.assertLessEqual(font.width(self.loc[get(node,'custom_cost_text')].replace('£pol_power',''))+24,180)
                    self.assertIn(get(get(node,'complete_effect'),'custom_effect_tooltip'),self.loc);self.assertIsNotNone(get(get(node,'complete_effect'),'hidden_effect'))
        for command in('build.py','build_art.py'):
            run=subprocess.run([sys.executable,'-B',str(HERE/command),'--check'],cwd=ROOT,capture_output=True,text=True);self.assertEqual(0,run.returncode,run.stdout+run.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
