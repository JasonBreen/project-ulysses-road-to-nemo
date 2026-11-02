"""Source topology, provenance, binding and reproducible-asset gates."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest
from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(HERE))
from content import FOCUSES,COUNTRIES
import build
import build_art
from source_contract import (validate,validate_protected,REVIEWED_RELEASE_UPDATE,
                             REVIEWED_FAT_CHARACTER_UPDATE,
                             REVIEWED_STARTING_GOVERNMENT_UPDATE)
sys.path.insert(0,str(ROOT/'tools'))
from economy_script import parse

def get(body,key,default=None):return next((v for k,_,v in body if k==key),default)
def walk(body):
    for key,op,value in body:
        yield key,op,value
        if isinstance(value,list):yield from walk(value)

class SourceAndArt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs=build.outputs();cls.art,cls.manifest=build_art.outputs()
    def test_exact_country_counts_unique_purposes_dates_and_complete_english(self):
        self.assertEqual({'FAT':54,'SBK':42},Counter(r.tag for r in FOCUSES));self.assertEqual(96,len({r.id for r in FOCUSES}));self.assertEqual(96,len({r.purpose for r in FOCUSES}))
        loc=(MOD/'localisation/english/ac_fato_south_belka_l_english.yml').read_bytes();self.assertTrue(loc.startswith(b'\xef\xbb\xbf'))
        strings=dict(re.findall(r'^\s*([\w.]+):0\s+"(.*)"$',loc.decode('utf-8-sig'),re.M))
        for r in FOCUSES:
            self.assertIn(r.id,strings);self.assertIn(r.id+'_desc',strings);self.assertGreater(len(r.narrative.split()),28);self.assertIn(r.narrative,strings[r.id+'_desc'])
            self.assertIn(r.cost,(5,10))
        for tag in build.DECISIONS:
            key='ac_fsb_'+tag.lower()+'_programmes';self.assertIn(key,strings);self.assertIn(key+'_desc',strings)
        for cfg in COUNTRIES.values():self.assertIn(cfg['tree'],strings);self.assertIn(cfg['tree']+'_desc',strings)
        events=parse((MOD/'events/ac_fato_south_belka.txt').read_text());scenes=[body for key,_,body in events if key=='country_event'];self.assertEqual(20,len(scenes))
        for body in scenes:
            self.assertGreaterEqual(sum(key=='option' for key,_,_ in body),3)
            for key,_,value in walk(body):
                if key in ('name','text','title','custom_effect_tooltip'):self.assertIn(value,strings,(get(body,'id'),key,value))
        for path,payload in self.outputs.items():
            if path.suffix!='.txt':continue
            for key,_,value in walk(parse(payload.decode('utf-8-sig'))):
                if key=='tooltip' or (key=='has_country_flag' and value.startswith(('ac_fsb_','FAT_nat_','SBK_nat_'))):self.assertIn(value,strings,(path,key,value))

    def test_prerequisites_are_resolved_acyclic_exclusions_symmetric_and_positions_distinct(self):
        by_id={r.id:r for r in FOCUSES};seen=set()
        for r in FOCUSES:
            for group in r.requirements:
                self.assertTrue(group)
                for parent in group:
                    self.assertIn(r.tag+'_nat_'+parent,seen,r.id)
                    self.assertLess(by_id[r.tag+'_nat_'+parent].y,r.y,(r.id,parent))
            if r.exclusive:
                other=by_id[r.tag+'_nat_'+r.exclusive];self.assertEqual(r.suffix,other.exclusive);self.assertEqual(r.phase,other.phase)
            seen.add(r.id)
        for tag,cfg in COUNTRIES.items():
            rows=[r for r in FOCUSES if r.tag==tag];self.assertEqual(len(rows),len({(r.x,r.y) for r in rows}))
            tree=get(parse((MOD/('common/national_focus/ac_fsb_'+tag.lower()+'.txt')).read_text()),'focus_tree')
            panel=get(tree,'continuous_focus_position');self.assertGreater(int(get(panel,'x')),(max(r.x for r in rows)+1)*96);self.assertEqual('16',get(panel,'y'))
            self.assertEqual(cfg['tree'],get(tree,'id'))

    def test_each_capability_has_an_actual_condition_consumer_beyond_its_reward(self):
        consumers=Counter()
        for path in self.outputs:
            if '/scripted_' not in path.as_posix() and '/decisions/' not in path.as_posix():continue
            for key,_,value in walk(parse(path.read_text(encoding='utf-8-sig'))):
                if key=='has_country_flag':consumers[value]+=1
        for r in FOCUSES:
            if r.kind=='capability':self.assertGreater(consumers['ac_fsb_'+r.hook],0,r.id)
            elif r.kind=='action':self.assertIn(r.tag+'_fsb_'+r.hook+'_apply',build.EFFECTS,r.id)
            elif r.kind=='scene':self.assertIn('ac_fsb_scene_'+r.hook+'_queue',build.EFFECTS,r.id)

    def test_inherited_owners_territory_forces_and_leaders_are_protected(self):
        self.assertEqual(15,len(validate()['protected_sha256']))
        forbidden={'transfer_state','add_state_core','add_manpower','set_capital','load_oob','set_oob','add_equipment_production','create_equipment_variant','declare_war_on','create_faction','add_to_faction','annex_country','set_politics','set_popularities','recruit_character','promote_character','add_country_leader_role','remove_ideas'}
        # Remove_ideas is allowed only for this owner's ideas, never inherited
        # demobilisation, leadership, settlement or other programme policies.
        for path,payload in self.outputs.items():
            if path.suffix!='.txt':continue
            for key,_,value in walk(parse(payload.decode('utf-8-sig'))):
                if key=='remove_ideas':self.assertTrue(value.startswith('ac_fsb_'),(path,key,value));continue
                self.assertNotIn(key,forbidden,(path,key))
                if key in ('set_global_flag','clr_global_flag'):self.fail('National owner wrote global outcome: '+str(value))
                if key in ('set_variable','add_to_variable','subtract_from_variable','multiply_variable','divide_variable'):
                    for name,_,_ in value:self.assertTrue(name.startswith('ac_fsb_'),(path,key,name))

    def test_only_exact_reviewed_release_owner_version_is_admitted(self):
        update=REVIEWED_RELEASE_UPDATE
        capture=json.loads((HERE/'engine_contract.json').read_text())
        expected=capture['protected_sha256'][update['path']]
        self.assertEqual(update['original_sha256'],expected)
        actual=(MOD/update['path']).read_bytes()
        self.assertEqual('reviewed-release-owner',validate_protected(update['path'],expected,actual))
        for path,before,data in (
                (update['path'],expected,actual+b'\n'),
                (update['path'],'0'*64,actual),
                ('common/scripted_effects/ac_release_foundations.txt',expected,actual),
                (update['path'],expected,actual.replace(b'ac_release_manual_production_tt',b'ac_release_automatic_production_tt'))):
            with self.subTest(path=path,before=before),self.assertRaises(ValueError):
                validate_protected(path,before,data)

    def test_only_exact_reviewed_fat_character_cleanup_is_admitted(self):
        update=REVIEWED_FAT_CHARACTER_UPDATE
        capture=json.loads((HERE/'engine_contract.json').read_text())
        expected=capture['protected_sha256'][update['path']]
        self.assertEqual(update['original_sha256'],expected)
        actual=(MOD/update['path']).read_bytes()
        self.assertEqual('reviewed-fat-character-owner',
                         validate_protected(update['path'],expected,actual))
        for path,before,data in (
                (update['path'],expected,actual+b'\n'),
                (update['path'],'0'*64,actual),
                ('common/characters/ac_starting_governments.txt',expected,actual),
                (update['path'],expected,actual.replace(b'name="Hugo Havel"',b'name="Changed"'))):
            with self.subTest(path=path,before=before),self.assertRaises(ValueError):
                validate_protected(path,before,data)

    def test_only_exact_reviewed_starting_government_cleanup_is_admitted(self):
        update=REVIEWED_STARTING_GOVERNMENT_UPDATE
        capture=json.loads((HERE/'engine_contract.json').read_text())
        expected=capture['protected_sha256'][update['path']]
        self.assertEqual(update['original_sha256'],expected)
        actual=(MOD/update['path']).read_bytes()
        self.assertEqual('reviewed-starting-government-owner',
                         validate_protected(update['path'],expected,actual))
        for path,before,data in (
                (update['path'],expected,actual+b'\n'),
                (update['path'],'0'*64,actual),
                ('common/characters/FAT.txt',expected,actual),
                (update['path'],expected,actual.replace(b'SHI_ac_government_office',b'SHI_changed_office',1))):
            with self.subTest(path=path,before=before),self.assertRaises(ValueError):
                validate_protected(path,before,data)

    def test_dedicated_tree_disposition_preserves_other_67_institution_profiles(self):
        profiles=json.loads((ROOT/'tools/institutions/profiles.json').read_text());self.assertEqual(69,len(profiles))
        for r in profiles:
            if r['tag']in COUNTRIES:self.assertFalse(r['regional_tree'])
        expected=validate()['institution_profile_rows_sha256']
        for r in profiles:
            original=dict(r,regional_tree=True) if r['tag']in COUNTRIES else r
            self.assertEqual(expected[r['tag']],hashlib.sha256(json.dumps(original,sort_keys=True).encode()).hexdigest(),r['tag'])

    def test_text_and_art_outputs_match_reproducible_generators(self):
        for path,data in self.outputs.items():self.assertEqual(data,path.read_bytes(),str(path))
        for path,data in self.art.items():self.assertEqual(data,path.read_bytes(),str(path))
        self.assertEqual(json.loads(json.dumps(build.purpose_inventory())),json.loads((HERE/'purposes.json').read_text()))

    def test_all_bindings_dimensions_alpha_and_compact_rows(self):
        sprites={get(body,'name'):get(body,'texturefile') for key,_,body in get(parse((MOD/'interface/ac_fato_south_belka.gfx').read_text()),'spriteTypes') if key=='spriteType'}
        self.assertEqual(len(sprites),sum(1 for k,_,_ in get(parse((MOD/'interface/ac_fato_south_belka.gfx').read_text()),'spriteTypes') if k=='spriteType'))
        for r in self.manifest['assets']:
            raw=(MOD/r['file']).read_bytes();self.assertEqual(r['sha256'],hashlib.sha256(raw).hexdigest());self.assertEqual(r['file'],sprites[r['sprite']])
            with Image.open(MOD/r['file']) as im:
                self.assertEqual((r['width'],r['height']),im.size);self.assertEqual(1,r['frames']);self.assertEqual(im.width,r['frame_width']);self.assertEqual((r['alpha_min'],r['alpha_max']),im.getchannel('A').getextrema())
                if r['role']=='compact decision-row artwork':self.assertEqual((26,29),im.size);self.assertEqual(0,im.getpixel((0,0))[3])
                elif r['role']=='category artwork':self.assertEqual((100,100),im.size)
                elif r['role']=='original narrative illustration':self.assertEqual((210,176),im.size);self.assertEqual((255,255),im.getchannel('A').getextrema())
        for row in FOCUSES:
            self.assertIn('GFX_ac_fsb_focus_'+row.id,sprites);self.assertIn('GFX_ac_fsb_focus_'+row.id+'_shine',sprites)
        for tag,items in build.DECISIONS.items():
            for key in re.findall(r'icon = (\w+)', ''.join(items)):
                path=MOD/sprites['GFX_decision_'+key]
                with Image.open(path)as im:self.assertEqual((26,29),im.size,key)

    def test_eight_original_masters_have_prompts_individual_review_and_deliberate_scene_reuse(self):
        records=json.loads((ROOT/'source/artwork/fato_south_belka/prompts.json').read_text());self.assertEqual(8,len(records['masters']))
        seen=set();events=[]
        for r in records['masters']:
            p=ROOT/'source/artwork/fato_south_belka'/r['file'];digest=hashlib.sha256(p.read_bytes()).hexdigest();self.assertNotIn(digest,seen);seen.add(digest)
            self.assertGreater(len(r['prompt']),500);self.assertIn('visually inspected',r['status']);events+=r['event_uses']
        self.assertEqual(set(range(1,11))|set(range(101,111)),set(events));self.assertEqual(20,len(events))
        focus=[r for r in self.manifest['assets']if r['role']=='original subject-led focus composition'];self.assertEqual(96,len({r['sha256']for r in focus}))

    def test_new_on_actions_are_bounded_and_include_exact_annex_and_release_contracts(self):
        body=get(parse((MOD/'common/on_actions/ac_fato_south_belka.txt').read_text()),'on_actions')
        names={key for key,_,_ in body};self.assertNotIn('on_daily',names);self.assertTrue({'on_annex','on_release_as_free','on_release_as_puppet','on_capitulation_immediate'}<=names)
        annex=get(get(body,'on_annex'),'effect');self.assertIsNotNone(get(annex,'FROM'));self.assertIn(('ac_fsb_interrupt','=','yes'),get(annex,'FROM'))

if __name__=='__main__':unittest.main()
