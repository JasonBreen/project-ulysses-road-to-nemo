"""Source, exact preservation, original asset and consumer regressions."""
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from PIL import Image
from config import HERE,ROOT,MOD,campaigns,legacy_builder,APPROVED
def module(name,filename):
    spec=importlib.util.spec_from_file_location(name,HERE/filename)
    result=importlib.util.module_from_spec(spec);sys.modules[name]=result;spec.loader.exec_module(result);return result
build=module('pacific_source_compiler','build.py').build
build_art=module('pacific_source_art','build_art.py')
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/overhaul')]
from usea_expansion.script import parse,get
from text_structure import validate_structure
from squadrons.schema import validate,campaigns as original_campaigns


def walk(nodes):
    for key,_,value in nodes:
        yield key,value
        if isinstance(value,list):yield from walk(value)


def matches(raw,record):
    return hashlib.sha256(raw if record['binary']else raw.replace(b'\r\n',b'\n')).hexdigest()==record['sha256']


class PacificSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=campaigns();cls.out,cls.manifest=build();cls.assets=json.loads((HERE/'assets.json').read_text())['assets']
        cls.loc=dict(re.findall(r'^ ([^ :]+):0 "(.*)"$',cls.out['localisation/english/ac_squadrons_pacific_l_english.yml'],re.M))

    def test_initial_six315_files_keep_exact_canonical_git_blobs_and_raw_media(self):
        contract=json.loads((HERE/'legacy_contract.json').read_text());self.assertEqual('856b3ee2d0e9dc0f07fc738bad18335816cb192f',contract['base']);self.assertEqual(315,len(contract['files']))
        self.assertEqual((120,24,282,78,139),tuple(contract[k]for k in('core_chapters','core_cast','events','original_masters','packaged_textures')))
        paths=list(contract['files']);r=subprocess.run(['git','hash-object','--stdin-paths'],cwd=ROOT,input='\n'.join(paths)+'\n',text=True,capture_output=True,check=True)
        for path,blob in zip(paths,r.stdout.splitlines()):
            record=contract['files'][path];self.assertEqual(record['git_blob'],blob,path)
            if record['binary']:self.assertTrue(matches((ROOT/path).read_bytes(),record),path)
        self.assertEqual(len(paths),len(r.stdout.splitlines()))
        record=dict(binary=True,sha256=hashlib.sha256(b'x\r\ny').hexdigest());self.assertTrue(matches(b'x\r\ny',record));self.assertFalse(matches(b'x\ny',record))
        for relative,text in legacy_builder().build().items():self.assertEqual(text,(MOD/relative).read_text(encoding='utf-8-sig'))

    def test_approved_hosts_horizon_and_counts_do_not_weaken_original_contract(self):
        tags=[r['tag']for r in self.rows];self.assertIn('OSE',tags);self.assertTrue(set(tags)<=set(APPROVED))
        n=len(tags);self.assertEqual(20*n,self.manifest['core_chapters']);self.assertEqual(4*n,self.manifest['cast']);self.assertEqual(3*n,self.manifest['personal_endings'])
        events=parse(self.out['events/ac_squadrons_pacific.txt']);self.assertEqual(47*n,sum(k=='country_event'for k,_,v in events))
        self.assertEqual(27*n,sum(len(v)for k,_,v in parse(self.out['common/decisions/ac_squadrons_pacific.txt'])))
        self.assertEqual(6,len(original_campaigns()));self.assertEqual(120,sum(len(r['chapters'])for r in original_campaigns()))
        for row in self.rows:
            self.assertEqual(list(range(1,21)),[c['id']for c in row['chapters']]);self.assertGreaterEqual(sum('callback'in c for c in row['chapters']),12)
            broken=copy.deepcopy(row);broken['chapters'][0]['earliest']='2021.1.1'
            with self.assertRaises(ValueError):validate(broken,horizon=row['admission_until'])
        old=original_campaigns()[0];old['extension_contract']='pacific_story_v1'
        with self.assertRaises(ValueError):validate(old,horizon='2020.12.31')
        changed=copy.deepcopy(self.rows[0]);changed['id']='unapproved_story'
        with self.assertRaises(ValueError):validate(changed,horizon='2020.12.31')

    def test_all_new_outputs_strictly_parse_reproduce_and_have_no_foreign_writers(self):
        forbidden={'declare_war_on','white_peace','create_wargoal','load_focus_tree','add_equipment_to_stockpile','add_manpower','add_building_construction','transfer_state','add_to_faction','set_politics','recruit_character','set_global_flag','clr_global_flag'}
        for relative,text in self.out.items():
            self.assertEqual(text,(MOD/relative).read_text(encoding='utf-8-sig'))
            if relative.endswith('.txt'):
                validate_structure(text);nodes=list(walk(parse(text)));self.assertFalse(forbidden&{k for k,v in nodes})
                for key,value in nodes:
                    if key in('set_country_flag','clr_country_flag'):self.assertTrue((get(value,'flag')if isinstance(value,list)else value).startswith('ac_sqp_'))
                    if key in('set_variable','add_to_variable','clamp_variable'):self.assertTrue((get(value,'var')if key=='clamp_variable'else value[0][0]).startswith('ac_sqp_'))
        self.assertNotIn('common/game_rules/ac_squadrons_pacific.txt',self.out)
        for filename in('build.py','build_art.py'):
            r=subprocess.run([sys.executable,'-B',str(HERE/filename),'--check'],cwd=ROOT,capture_output=True,text=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr)

    def test_actual_english_event_and_decision_consumers_bind_owned_sprites_at_country_size(self):
        self.assertTrue(all(k.startswith(('ac_sqp_','ac_sqp.'))for k in self.loc))
        original_keys=set(re.findall(r'^ ([^ :]+):0 ',(MOD/'localisation/english/ac_squadrons_l_english.yml').read_text(encoding='utf-8-sig'),re.M))
        self.assertFalse(original_keys&set(self.loc))
        sprites={a['sprite']:a for a in self.assets if a.get('sprite')}
        for key,node in walk(parse(self.out['events/ac_squadrons_pacific.txt'])):
            if key in('title','name')and isinstance(node,str):self.assertIn(node,self.loc)
            if key=='text'and isinstance(node,str):self.assertIn(node,self.loc)
            if key=='picture':self.assertIn(node,sprites);self.assertEqual((200,160),(sprites[node]['width'],sprites[node]['height']))
        rows=parse(self.out['common/decisions/ac_squadrons_pacific.txt'])
        for category,_,items in rows:
            self.assertIn(category,self.loc);self.assertIn(category+'_desc',self.loc)
            for ident,_,body in items:
                self.assertIn(ident,self.loc);self.assertIn(ident+'_desc',self.loc)
                name=get(body,'icon');self.assertIn('GFX_decision_'+name,sprites)
                a=sprites['GFX_decision_'+name];self.assertEqual((26,29),(a['width'],a['height']))
        forbidden={'native','telemetry','implementation','runtime','owned conflict'}
        for row in self.rows:
            for ch in row['chapters']:
                prose=[ch['text'],*(v['text']for v in ch.get('condition_variants',[]))]
                self.assertFalse(any(word in text.lower()for word in forbidden for text in prose))

    def test_exact_original_source_partition_frames_alpha_and_consumer_role_sizes(self):
        count=len(self.rows);self.assertEqual(23*count+1,len(self.assets));self.assertEqual(22*count+1,sum(bool(a.get('sprite'))for a in self.assets))
        self.assertEqual(len(self.assets),len({a['file']for a in self.assets}))
        actual={p.relative_to(MOD).as_posix()for p in(MOD/'gfx/AC_squadrons_pacific').rglob('*.dds')}
        actual.update(p.relative_to(MOD).as_posix()for p in(MOD/'gfx/loadingscreens').glob('ac_sqp_*.dds'))
        self.assertEqual({a['file']for a in self.assets},actual)
        self.assertEqual(18*count,sum(bool(a.get('source'))for a in self.assets)) #4 portraits twice+8 scenes+2 loadings.
        for a in self.assets:
            raw=(MOD/a['file']).read_bytes();self.assertEqual(a['sha256'],hashlib.sha256(raw).hexdigest())
            with Image.open(io.BytesIO(raw))as image:
                self.assertEqual((a['width'],a['height']),image.size);self.assertEqual(1,a['frames']);self.assertEqual(a['width'],a['frame_width'])
                self.assertEqual((a['alpha_min'],a['alpha_max']),image.convert('RGBA').getchannel('A').getextrema())
                if '/decisions/'in a['file']:self.assertEqual(0,image.convert('RGBA').getpixel((0,0))[3])
            if a.get('source'):
                path=ROOT/a['source'];self.assertEqual(a['source_sha256'],hashlib.sha256(path.read_bytes()).hexdigest())

    def test_full_fit_preserves_corners_and_reviewed_loading_cover_is_distinct(self):
        original=Image.new('RGBA',(800,400),(90,90,90,255));pixels=original.load()
        for x,y,color in((0,0,(255,0,0,255)),(799,0,(0,255,0,255)),(0,399,(0,0,255,255)),(799,399,(255,255,0,255))):
            Image.Image.paste(original,Image.new('RGBA',(80,80),color),(max(0,x-79),max(0,y-79)))
        import tempfile
        with tempfile.TemporaryDirectory()as tmp:
            p=Path(tmp)/'fixture.png';original.save(p);fitted=build_art.old.contained(p,(200,160));cover=build_art.loading_cover(p,(200,160))
            self.assertNotEqual(fitted.tobytes(),cover.tobytes())
            for xy in((3,33),(196,33),(3,126),(196,126)):self.assertNotEqual(build_art.old.NAVY,fitted.getpixel(xy))
        raw=b'not png'
        with self.assertRaises(Exception):build_art.same_png(raw,raw)

    def test_actual_country_event_aperture_keeps_cast_and_scene_pixels_outside_options(self):
        gui=get(parse((MOD/'interface/eventwindow.gui').read_text()),'guiTypes')
        def named(nodes,name):return next(v for k,_,v in nodes if isinstance(v,list)and get(v,'name','').strip('"')==name)
        bottom=named(named(gui,'EventWindow'),'bottom_Window');pic=named(bottom,'event_picture');options=named(bottom,'options_grid')
        self.assertEqual(1,float(get(pic,'scale','1')))
        gap=int(get(get(options,'position'),'x'))-int(get(get(pic,'position'),'x'))
        height=int(get(get(bottom,'size'),'height'))-int(get(get(pic,'position'),'y'))
        fits=lambda w,h:w<=gap and h<=height
        self.assertTrue(fits(210,176));self.assertTrue(fits(200,160));self.assertFalse(fits(640,260));self.assertFalse(fits(1672,941))
        sprites={get(v,'name').strip('"'):get(v,'texturefile').strip('"')for k,_,v in get(parse((MOD/'interface/ac_squadrons_pacific.gfx').read_text()),'spriteTypes')}
        for kind,_,node in parse(self.out['events/ac_squadrons_pacific.txt']):
            if kind=='country_event':
                with Image.open(MOD/sprites[get(node,'picture')])as image:self.assertTrue(fits(*image.size),get(node,'id'))

    def test_ose_component_bytes_and_owned_nodes_remain_exact_when_yuk_is_added(self):
        if not any(r['tag']=='YUK'for r in self.rows):self.skipTest('Independent YUK component is not admitted')
        contract=json.loads((HERE/'ose_contract.json').read_text());self.assertEqual('7776f754418d7ecbaa5309bb9925fd1825aa7796',contract['base'])
        self.assertEqual(26,len(contract['files']))
        for relative,digest in contract['files'].items():self.assertEqual(digest,hashlib.sha256((ROOT/relative).read_bytes()).hexdigest(),relative)
        for relative,expected in contract['nodes'].items():
            tree=parse((ROOT/relative).read_text());path=Path(relative)
            if path.parent.name=='events':current={get(v,'id'):v for k,_,v in tree if k=='country_event'}
            elif path.suffix=='.gfx':current={get(v,'name'):v for k,_,v in get(tree,'spriteTypes')}
            else:current={k:v for k,_,v in tree}
            for name,record in expected.items():
                value=current[name]
                if record['prefix_length']is not None:value=value[:record['prefix_length']]
                self.assertEqual(record['sha256'],hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest(),(relative,name))
        for name,digest in contract['localization'].items():self.assertEqual(digest,hashlib.sha256(self.loc[name].encode()).hexdigest(),name)


if __name__=='__main__':unittest.main(verbosity=2)
