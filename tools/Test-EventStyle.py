"""Event defaults: actual consumers, immutable restoration and negative fixtures."""
import copy,hashlib,json,shutil,subprocess,sys,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
from PIL import Image
from event_style import migration as m
from event_style import build_art as art
from event_style import review
from event_style.validate import validate_art
from event_picture_fit.proof import preserved
from usea_expansion.script import parse,get,render
ROOT=m.ROOT;MOD=m.MOD;HERE=m.HERE

class EventStyle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current=(MOD/'interface/eventwindow.gui').read_text(encoding='utf-8-sig')
        cls.manifest=json.loads((HERE/'assets.json').read_text());cls.measure=review.measurement()
    def test_exact_17sprite_6font_changes_independently_diffed(self):
        differences=[]
        def diff(a,b,path=()):
            self.assertEqual(len(a),len(b))
            names=[v.strip('"') for k,_,v in a if k=='name' and isinstance(v,str)];path+=tuple(names)
            for left,right in zip(a,b):
                self.assertEqual(left[:2],right[:2]);key,_,value=left
                if isinstance(value,list):self.assertIsInstance(right[2],list);diff(value,right[2],path)
                elif value!=right[2]:differences.append((path,key,value.strip('"'),right[2].strip('"')))
        diff(parse(m.source()),parse(self.current))
        self.assertEqual(23,len(differences));self.assertCountEqual(m.REVIEWED,differences)
        self.assertEqual(17,sum(k!='font' for _,k,_,_ in differences));self.assertEqual(6,sum(k=='font' for _,k,_,_ in differences))
    def test_original_fit_capture_unchanged_and_whole_source_restores(self):
        self.assertEqual(m.source(),m.assert_preserved(self.current));self.assertEqual(parse(m.source()),m.restore_ast(parse(self.current)))
        capture=json.loads((ROOT/'tools/event_picture_fit/contract.json').read_text())
        self.assertEqual(capture['protected_gui_sha256'],m.sha(m.source()));preserved()
    def test_altered_original_source_cannot_be_recaptured_or_normalized(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'SOURCE_eventwindow.gui';source.write_text(m.source().replace('x = 215','x = 216',1),encoding='utf-8')
            with patch.object(m,'HERE',Path(folder)),self.assertRaisesRegex(ValueError,'immutable fit contract'):m.generated()
    def test_all23_reverted_wrong_or_missing_fields_fail(self):
        fields=m.spans(self.current)
        for path,key,old,new in m.REVIEWED:
            token=fields[(path,key)]
            for replacement in ('"'+old+'"','"GFX_unregistered"'):
                with self.subTest(path=path,key=key,replacement=replacement),self.assertRaises(ValueError):m.assert_preserved(self.current[:token.start()]+replacement+self.current[token.end():])
            with self.subTest(path=path,key=key),self.assertRaises(ValueError):m.assert_preserved(self.current[:token.start()]+'""'+self.current[token.end():])
    def test_lexical_escape_safety_and_unknown_layout_action_condition_fail(self):
        for old,new in [('x = 215','x = 216'),('clicksound = click_default','clicksound = another_sound'),('moveable = yes','moveable = no'),('Orientation = CENTER','Orientation = UPPER_LEFT'),('size = {','unreviewed_condition = yes\nsize = {')]:
            with self.subTest(change=new),self.assertRaises(ValueError):m.assert_preserved(self.current.replace(old,new,1))
        # A quoted display string containing escaped assignment-like text is untouched.
        source=m.source().replace('Title text here!','Title \\" font = \\"hoi4_typewriter22')
        migrated=m.replace(source)
        self.assertIn('Title \\" font = \\"hoi4_typewriter22',migrated)
    def test_ordered_ast_missing_duplicate_or_unknown_nodes_fail(self):
        for change in ('remove','duplicate','unknown','order'):
            nodes=parse(self.current);gui=get(nodes,'guiTypes');body=next(v for k,_,v in gui if isinstance(v,list) and get(v,'name')=='"EventWindow_Operative"')
            if change=='remove':body.pop(0)
            elif change=='duplicate':body.append(copy.deepcopy(next(r for r in body if r[0]=='background')))
            elif change=='unknown':body.append(['unknown_action','=','yes'])
            else:body[0],body[1]=body[1],body[0]
            with self.subTest(change=change),self.assertRaises(ValueError):m.assert_preserved(render(nodes))
    def test_primary_metadata_and_actual_dimensions_not_manifest_only(self):
        rows=validate_art();self.assertEqual(13,len(rows));self.assertEqual(12,len({r['texture'] for r in rows}))
        with tempfile.TemporaryDirectory() as folder:
            mod=Path(folder);shutil.copytree(MOD/'gfx/AC_event_style',mod/'gfx/AC_event_style');(mod/'interface').mkdir()
            shutil.copyfile(MOD/'interface/ac_event_style.gfx',mod/'interface/ac_event_style.gfx')
            shutil.copyfile(MOD/'interface/eventwindow.gui',mod/'interface/eventwindow.gui')
            Image.new('RGBA',(640,260),(10,30,45,255)).save(mod/'gfx/AC_event_style/country_default.dds')
            with self.assertRaisesRegex(ValueError,'dimensions'):validate_art(mod)
    def test_font_aliases_require_native_registration_not_root_or_nested_declarations(self):
        gfx=(MOD/'interface/ac_event_style.gfx').read_text();tree=parse(gfx)
        fonts=get(tree,'bitmapfonts');self.assertEqual(2,len(fonts))
        root_only=[node for node in tree if node[0]!='bitmapfonts']+fonts
        with self.assertRaisesRegex(ValueError,'bitmapfonts'):validate_art(gfx=render(root_only))
        nested=[node for node in tree if node[0]!='bitmapfonts']+[['unregistered_wrapper','=',[['bitmapfonts','=',fonts]]]]
        with self.assertRaisesRegex(ValueError,'bitmapfonts'):validate_art(gfx=render(nested))
    def test_all24_operative_frames_actual_kind_and_animation_metadata(self):
        image=Image.open(MOD/'gfx/AC_event_style/operative_background.dds').convert('RGBA')
        self.assertEqual((12672,596),image.size);self.assertEqual(24,len({hashlib.sha256(image.crop((n*528,0,(n+1)*528,596)).tobytes()).hexdigest() for n in range(24)}))
        gfx=(MOD/'interface/ac_event_style.gfx').read_text()
        for old,new in [('noOfFrames = 24','noOfFrames = 1'),('animation_rate_fps = 80','animation_rate_fps = 30'),('looping = no','looping = yes'),('play_on_show = no','play_on_show = yes'),('frameAnimatedSpriteType','spriteType')]:
            with self.subTest(change=new),self.assertRaisesRegex(ValueError,'metadata'):validate_art(gfx=gfx.replace(old,new,1))
    def test_tiles_agency_integer_frames_and_transparent_quad_contract(self):
        gfx=(MOD/'interface/ac_event_style.gfx').read_text()
        for old,new in [('x = 3 y = 3','x = 95 y = 95'),('x = 290 y = 16','x = 1 y = 1')]:
            with self.assertRaisesRegex(ValueError,'metadata'):validate_art(gfx=gfx.replace(old,new,1))
        with Image.open(MOD/'gfx/AC_event_style/agency_office.dds') as image:self.assertEqual((234,119),image.size)
        with Image.open(MOD/'gfx/AC_event_style/transparent.dds') as image:self.assertEqual((0,0),image.getchannel('A').getextrema())
    def test_actual_scaled_portrait_and_agency_apertures(self):
        a=review.apertures();self.assertTrue(a['leader']['fully_transparent']);self.assertTrue(a['agency']['inside_body']);self.assertTrue(a['agency']['clear_of_title'])
        self.assertEqual([9,10,166,221],a['leader']['conservative_integer_aperture'])
        self.assertEqual([361,35,478,154],a['agency']['bounds'])
        with tempfile.TemporaryDirectory() as folder:
            mod=Path(folder);shutil.copytree(MOD/'gfx/AC_event_style',mod/'gfx/AC_event_style');(mod/'interface').mkdir()
            for name in ('eventwindow.gui','ac_event_style.gfx'):shutil.copyfile(MOD/'interface'/name,mod/'interface'/name)
            image=Image.open(mod/'gfx/AC_event_style/leader_frame.dds').convert('RGBA');image.putpixel((10,11),(80,190,210,255));image.save(mod/'gfx/AC_event_style/leader_frame.dds')
            with self.assertRaisesRegex(ValueError,'aperture'):validate_art(mod)
    def test_same_sized_opaque_bound_frame_rebinding_fails_file_and_supplied_gfx(self):
        with tempfile.TemporaryDirectory() as folder:
            mod=Path(folder);shutil.copytree(MOD/'gfx/AC_event_style',mod/'gfx/AC_event_style');(mod/'interface').mkdir()
            for name in ('eventwindow.gui','ac_event_style.gfx'):shutil.copyfile(MOD/'interface'/name,mod/'interface'/name)
            opaque=mod/'gfx/opaque_frame.dds';Image.new('RGBA',(172,232),(30,60,90,255)).save(opaque)
            path=mod/'interface/ac_event_style.gfx';original=path.read_text()
            rebound=original.replace('gfx/AC_event_style/leader_frame.dds','gfx/opaque_frame.dds')
            self.assertEqual(1,rebound.count('gfx/opaque_frame.dds'))
            with self.assertRaisesRegex(ValueError,'aperture'):validate_art(mod,gfx=rebound)
            path.write_text(rebound)
            with self.assertRaisesRegex(ValueError,'aperture'):validate_art(mod)
            self.assertFalse(review.apertures(mod)['leader']['fully_transparent'])
            self.assertEqual('gfx/opaque_frame.dds',review.apertures(mod)['leader']['frame_binding']['texture'])
    def test_existing_atlas_raw_bytes_and_no_global_alias_override(self):
        for relative,digest in self.manifest['unchanged_font_bytes'].items():self.assertEqual(digest,hashlib.sha256((MOD/relative).read_bytes()).hexdigest())
        gfx=(MOD/'interface/ac_event_style.gfx').read_text()
        for old in {old for _,_,old,_ in m.REVIEWED}:self.assertNotIn('name = "'+old+'"',gfx)
    def test_actual_localized_titles_and_descriptions_and_honest_stress(self):
        self.assertGreater(self.measure['measured_fields'],1600);self.assertFalse(self.measure['static_title_clips']);self.assertFalse(self.measure['unscrollable_static_body_clips'])
        self.assertFalse(self.measure['missing_glyph_fields']);self.assertGreater(self.measure['scrollable_overlength_bodies'],0)
        for name in ('EventWindow_leader','EventWindow_Operative'):self.assertEqual(0,self.measure['template_text_counts'][name])
        self.assertEqual(4,len(self.measure['leader_template_stress']))
        self.assertTrue(any(row['clipped'] for row in self.measure['leader_template_stress']))
    def text_body(self,width=120,height=18):
        body=copy.deepcopy(review.named(parse(self.current))[('EventWindow','midsection','Description')])
        for node in body:
            if node[0]=='maxWidth':node[2]=str(width)
            if node[0]=='maxHeight':node[2]=str(height)
        return body
    def test_vertical_scroll_only_accesses_wrapped_bottom_overflow(self):
        positive=review.metrics('alpha beta gamma '*80,self.text_body())
        self.assertTrue(positive['overflow']['bottom']);self.assertTrue(positive['accessible_by_scroll'])
        for text in ('MMMMMMMMMMMMMMMMMMMMMMMMMMMM','first\nMMMMMMMMMMMMMMMMMMMMMMMMMMMM'):
            row=review.metrics(text,self.text_body(width=12))
            self.assertTrue(row['clipped']);self.assertTrue(row['overflow']['unbreakable_word']);self.assertFalse(row['accessible_by_scroll'])
        font=review.FONTS['ACBriefing16'];old=font.rows[ord('A')]
        for key,value,overflow in [('xoffset',-30,'left'),('yoffset',-40,'top')]:
            with patch.dict(font.rows,{ord('A'):{**old,key:value}}):
                row=review.metrics('A word '*80,self.text_body())
                self.assertTrue(row['overflow'][overflow]);self.assertTrue(row['overflow']['bottom']);self.assertFalse(row['accessible_by_scroll'])
    def test_every_repeated_title_description_and_conditional_variant_is_measured(self):
        with tempfile.TemporaryDirectory() as folder:
            mod=Path(folder);(mod/'interface').mkdir();(mod/'events').mkdir();(mod/'localisation').mkdir()
            shutil.copyfile(MOD/'interface/eventwindow.gui',mod/'interface/eventwindow.gui')
            (mod/'events/test.txt').write_text('country_event={id=fixture.1 title=title_short title={trigger={always=yes} text=title_long} desc=desc_short desc={text=desc_long} desc={random_valid={text=desc_narrow text=desc_missing}}}')
            strings={'title_short':'Short title','title_long':'W'*400,'desc_short':'Short description','desc_long':'alpha beta '*300,'desc_narrow':'W'*800}
            (mod/'localisation/test_l_english.yml').write_text('l_english:\n'+''.join(' '+key+':0 "'+value+'"\n' for key,value in strings.items()),encoding='utf-8-sig')
            result=review.measurement(mod,include_stress=False)
            self.assertEqual(5,result['measured_fields']);self.assertEqual(list(strings),[row['key'] for row in result['fields']])
            self.assertEqual(['title_long'],[row['key'] for row in result['static_title_clips']])
            self.assertEqual(['desc_narrow'],[row['key'] for row in result['unscrollable_static_body_clips']])
            self.assertEqual(['desc_missing'],[row['key'] for row in result['unresolved_localization']])
            self.assertEqual([0,1,0,1,2],[row['field_occurrence'] for row in result['fields']])
            self.assertTrue(result['fields'][3]['accessible_by_scroll']);self.assertFalse(result['fields'][4]['accessible_by_scroll'])
    def test_art_sources_frames_alpha_and_no_yellow_artifact(self):
        self.assertEqual(12,len(self.manifest['assets']))
        for row in self.manifest['assets']:
            self.assertEqual(row['sha256'],hashlib.sha256((ROOT/row['texture']).read_bytes()).hexdigest())
            self.assertEqual(row['source_sha256'],hashlib.sha256((ROOT/row['source']).read_bytes()).hexdigest())
            with Image.open(ROOT/row['texture']) as image:
                self.assertEqual(tuple(row['dimensions']),image.size)
                colors=image.convert('RGBA').getcolors(4096)
                self.assertIsNotNone(colors,'Unexpected non-geometric full-color event texture')
                self.assertFalse(any(r>150 and g>130 and b<100 and a>0 for _,(r,g,b,a) in colors))
    def test_generated_source_art_and_review(self):
        for command in (['tools/usea_expansion/build_events_ui.py','--check'],['tools/event_style/build.py','--check'],['tools/event_style/review.py','--check']):
            result=subprocess.run([sys.executable,'-B']+command,cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)

    def test_original_event_producer_composes_only_the_registered_style(self):
        from usea_expansion import build_events_ui
        original=build_events_ui.build_base()
        self.assertEqual(m.source(),original)
        self.assertEqual(self.current,build_events_ui.build())
        for before,after in (('x = 215','x = 216'),('moveable = yes','moveable = no'),('clicksound = click_default','clicksound = changed_sound')):
            with self.subTest(change=after),self.assertRaisesRegex(ValueError,'Upstream event GUI'):
                m.generated_from(original.replace(before,after,1))

if __name__=='__main__':unittest.main(verbosity=2)
