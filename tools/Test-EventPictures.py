"""Actual event→sprite→DDS→GUI regressions; no native game or desktop."""
import copy,hashlib,io,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from event_picture_fit import audit as consumers
from event_picture_fit.fit import ROOT,MOD,SIZES,contain,assert_fits,same_review_png
from event_picture_fit.proof import preserved,assert_picture_only,restore,reviewed
from event_picture_fit.review import previous
from event_picture_fit.ucw import SCENES,FAMILIES,outputs as news_outputs
from usea_expansion.script import parse,get,render

HERE=ROOT/'tools/event_picture_fit'

class EventPictures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.contract=preserved();cls.report=consumers.audit()
    def test_primary_native_headers_and_actual_control_bindings(self):
        self.assertEqual('1.19.4.1',self.contract['primary']['version_source']['rawVersion'])
        for kind,size in SIZES.items():
            primary=self.contract['primary'][kind];self.assertEqual(size,(primary['width'],primary['height']))
        geometry=consumers.controls()
        self.assertEqual([5,5],geometry['country_event']['position']);self.assertEqual(215,geometry['country_event']['right_obstacle'])
        self.assertEqual([59,91],geometry['news_event']['position']);self.assertEqual(260,geometry['news_event']['lower_obstacle'])
    def test_all_actual_requested_consumers_resolve_and_fit(self):
        self.assertEqual(425,self.report['explicit_consumers']);self.assertEqual({'country_event':401,'news_event':24},self.report['counts'])
        self.assertEqual(32,len(self.report['implicit_picture_events']));self.assertTrue(all(r['hidden'] for r in self.report['implicit_picture_events']))
        for row in self.report['consumers']:
            with self.subTest(event=row['id']):
                self.assertLessEqual(row['bounds'][2],215 if row['event_type']=='country_event' else 456)
                self.assertLessEqual(row['bounds'][3],181 if row['event_type']=='country_event' else 244)
    def test_all40_country_textures_match_full_preserved_master_fits(self):
        self.assertEqual(40,len(self.contract['country_repairs']))
        for row in self.contract['country_repairs']:
            with self.subTest(texture=row['file']),Image.open(MOD/row['file']) as actual:
                expected=contain(ROOT/row['source'])
                self.assertEqual((210,176),actual.size);self.assertEqual((255,255),actual.convert('RGBA').getchannel('A').getextrema())
                self.assertEqual(expected.tobytes(),actual.convert('RGBA').tobytes())
                previous(row) # independently reproduce captured actual pre-repair RGBA
    def test_edge_markers_are_preserved_by_fit_and_padding_is_opaque(self):
        master=Image.new('RGBA',(640,260),(90,110,130,255))
        for xy in ((0,0),(639,0),(0,259),(639,259)):master.putpixel(xy,(255,255,255,255))
        fitted=contain(master);self.assertEqual((210,176),fitted.size)
        self.assertEqual((255,255),fitted.getchannel('A').getextrema())
        # The horizontal extremes survive; a center crop would remove both.
        self.assertNotEqual((8,22,33,255),fitted.getpixel((0,88)))
        self.assertNotEqual((8,22,33,255),fitted.getpixel((209,88)))
    def fixture(self,folder,kind='country_event',size=(640,260),frames=1,picture='GFX_fixture'):
        mod=Path(folder);(mod/'interface').mkdir();(mod/'events').mkdir();(mod/'gfx').mkdir()
        shutil.copyfile(MOD/'interface/eventwindow.gui',mod/'interface/eventwindow.gui')
        (mod/'interface/picture.gfx').write_text('spriteTypes={spriteType={name="GFX_fixture" texturefile="gfx/picture.dds" noOfFrames='+str(frames)+'}}')
        (mod/'events/test.txt').write_text(kind+'={id=fixture.1 picture='+picture+'}')
        Image.new('RGBA',size,(20,40,60,255)).save(mod/'gfx/picture.dds')
        return mod
    def test_oversized_real_consumer_dds_fails_and_native_fit_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            mod=self.fixture(folder)
            with self.assertRaisesRegex(ValueError,'exceeds'):consumers.audit(['events/test.txt'],mod)
            Image.new('RGBA',(210,176),(20,40,60,255)).save(mod/'gfx/picture.dds')
            self.assertEqual(1,consumers.audit(['events/test.txt'],mod)['explicit_consumers'])
    def test_country_sized_real_news_consumer_fails_and_news_size_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            mod=self.fixture(folder,'news_event',(210,176))
            with self.assertRaisesRegex(ValueError,'exceeds'):consumers.audit(['events/test.txt'],mod)
            Image.new('RGBA',(397,153),(20,40,60,255)).save(mod/'gfx/picture.dds')
            self.assertEqual([59,91,456,244],consumers.audit(['events/test.txt'],mod)['consumers'][0]['bounds'])
    def test_frames_are_measured_per_frame_not_whole_sheet(self):
        self.assertEqual((210,176),assert_fits('country_event',(420,176),frames=2))
        with self.assertRaisesRegex(ValueError,'frame'):assert_fits('country_event',(421,176),frames=2)
        with self.assertRaisesRegex(ValueError,'exceeds'):assert_fits('country_event',(420,176),frames=1)
    def test_real_missing_binding_and_control_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            mod=self.fixture(folder,picture='GFX_missing')
            with self.assertRaisesRegex(ValueError,'Unresolved'):consumers.audit(['events/test.txt'],mod)
            p=mod/'interface/eventwindow.gui';p.write_text(p.read_text().replace('name = "event_picture"','name = "missing_picture"',1))
            with self.assertRaisesRegex(ValueError,'Missing required'):consumers.controls(mod)
    def test_actual_scale_or_sibling_geometry_mutation_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            mod=self.fixture(folder);p=mod/'interface/eventwindow.gui';original=p.read_text()
            p.write_text(original.replace('name = "event_picture"','name = "event_picture" scale = 1.25',1))
            with self.assertRaisesRegex(ValueError,'scale'):consumers.controls(mod)
            p.write_text(original.replace('x = 215','x = 214',1))
            with self.assertRaisesRegex(ValueError,'sibling bounds'):consumers.controls(mod)
    def test_only24_reviewed_news_bindings_changed_in_whole_event_ast(self):
        self.assertEqual(24,sum(len(reviewed(p)) for p in self.contract['original_event_sources']))
        for relative in self.contract['original_event_sources']:
            assert_picture_only(relative,parse((MOD/relative).read_text()))
    def test_picture_restoration_does_not_allow_reward_text_or_country_picture_changes(self):
        relative='events/ac_anea.txt';original=parse((MOD/relative).read_text())
        for mutation in ('reward','desc','country_picture'):
            nodes=copy.deepcopy(original);body=next(v for k,_,v in nodes if k=='country_event')
            if mutation=='reward':get(body,'option').append(['set_country_flag','=','unapproved'])
            else:next(r for r in body if r[0]==('desc' if mutation=='desc' else 'picture'))[2]='unapproved'
            with self.assertRaisesRegex(ValueError,'Non-picture'):assert_picture_only(relative,nodes)
        nodes=copy.deepcopy(original);body=next(v for k,_,v in nodes if k=='news_event');next(r for r in body if r[0]=='picture')[2]='GFX_wrong'
        with self.assertRaisesRegex(ValueError,'picture contract'):assert_picture_only(relative,nodes)
    def test_new_ucw_news_is_original_distinct_and_all21_scenes_are_explicit(self):
        manifest=json.loads((HERE/'ucw_assets.json').read_text());self.assertEqual(6,len(manifest['assets']));self.assertEqual(21,len(manifest['consumers']))
        self.assertEqual(6,len({r['sha256'] for r in manifest['assets']}))
        for row in manifest['assets']:
            self.assertIn('original procedural',row['source_layer'])
            self.assertNotIn('gfx/event_pictures',row['source'])
            with Image.open(MOD/row['file']) as image:self.assertEqual((397,153),image.size)
    def test_anea_original_country_art_and_108focuses_preserved(self):
        self.assertEqual(108,len(self.contract['original_anea_focus_sha256']))
        with Image.open(MOD/'gfx/AC_anea/events/emm_4.dds') as image:self.assertEqual((200,160),image.size)
        with Image.open(MOD/'gfx/AC_anea/news/emm_4.dds') as image:self.assertEqual((397,153),image.size)
        self.assertEqual([1050,1107,1110],[r['protected_count'] for r in self.contract['military_captures'].values()])
    def test_review_compression_only_exception_rejects_pixel_and_size_mutations(self):
        image=Image.new('RGBA',(4,4),(20,40,60,255));a=io.BytesIO();b=io.BytesIO()
        image.save(a,format='PNG',compress_level=0);image.save(b,format='PNG',compress_level=9)
        self.assertTrue(same_review_png(a.getvalue(),b.getvalue()))
        image.putpixel((0,0),(21,40,60,255));b=io.BytesIO();image.save(b,format='PNG');self.assertFalse(same_review_png(a.getvalue(),b.getvalue()))
        b=io.BytesIO();image.resize((3,4)).save(b,format='PNG');self.assertFalse(same_review_png(a.getvalue(),b.getvalue()))

if __name__=='__main__':unittest.main(verbosity=2)
