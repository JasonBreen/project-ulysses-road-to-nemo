"""Meaningful source, provenance, binary-safety and review-reproduction gates."""
import copy,io,json,subprocess,unittest
from pathlib import Path
from PIL import Image
from audit import HERE,ROOT,PNG,digest,sources,validate_image
from review import encode,outputs,same_png

class PacificArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plan,cls.rows=sources()
    def test_all26_actual_originals_and_required_families(self):
        self.assertEqual(len(self.rows),26)
        self.assertEqual({p:sum(r['path'].parent.name==p for r in self.rows) for p in ('portraits','scenes','loading')},{'portraits':8,'scenes':16,'loading':2})
        self.assertEqual(len({r['sha256'] for r in self.rows}),26)
    def test_actual_original_bytes_and_metadata(self):
        for row in self.rows:
            with self.subTest(id=row['id']),Image.open(row['path']) as image:
                validate_image(row['path'].read_bytes(),row,image.size,image.convert('RGBA').getchannel('A').getextrema())
                self.assertEqual(row['frames'],1);self.assertEqual(row['alpha_extrema'],[255,255])
                self.assertTrue(row['packaging_contract']);self.assertTrue(row['source_output'].startswith('exec-'))
    def test_text_filter_damage_to_real_png_header_fails(self):
        row=self.rows[0];raw=row['path'].read_bytes();damaged=raw.replace(b'\r\n',b'\n',1)
        with self.assertRaisesRegex(ValueError,'signature'):validate_image(damaged,row,(row['width'],row['height']),(255,255))
    def test_changed_original_hash_fails(self):
        row=self.rows[0];raw=row['path'].read_bytes()+b'\x00'
        with self.assertRaisesRegex(ValueError,'hash'):validate_image(raw,row,(row['width'],row['height']),(255,255))
    def test_dimension_and_alpha_aperture_mutations_fail(self):
        row=self.rows[0];raw=row['path'].read_bytes()
        with self.assertRaisesRegex(ValueError,'dimensions'):validate_image(raw,row,(row['width']+1,row['height']),(255,255))
        with self.assertRaisesRegex(ValueError,'transparency'):validate_image(raw,row,(row['width'],row['height']),(0,255))
    def test_precise_chapter_and_personal_ending_slots(self):
        for tag in ('OSE','YUK'):
            row={int(r['id'].rsplit('_',1)[1]):r for r in self.rows if r['path'].parent.name=='scenes' and r['tag']==tag}
            self.assertEqual(sorted(n for i in range(1,6) for n in row[i]['chapters']),list(range(1,21)))
            self.assertEqual([row[i]['ending'] for i in (6,7,8)],['trusted','compromised','fractured'])
            self.assertEqual([row[i]['chapters'] for i in (6,7,8)],[[],[],[]])
            self.assertEqual(len({row[i]['sha256'] for i in (6,7,8)}),3)
    def test_five_edits_retain_exact_prior_originals(self):
        edited=[r for r in self.rows if r.get('generation_references')]
        self.assertEqual({r['id'] for r in edited},{'ose_scene_4','ose_scene_8','yuk_scene_1','yuk_scene_3','yuk_scene_6'})
        for row in edited:
            prior=ROOT/row['generation_references'][0]
            self.assertEqual(digest(prior.read_bytes()),row['revision_source_sha256'])
            self.assertNotEqual(row['sha256'],row['revision_source_sha256'])
            self.assertTrue(row['base_prompt']);self.assertTrue(row['revision_reason'])
    def test_all_actual_png_paths_have_binary_git_attributes(self):
        paths=[r['path'].relative_to(ROOT).as_posix() for r in self.rows]
        paths += sorted({ref for row in self.rows for ref in row.get('generation_references',[])})
        result=subprocess.check_output(['git','check-attr','-z','text','--',*paths],cwd=ROOT).split(b'\x00')
        triples=[result[i:i+3] for i in range(0,len(result)-1,3)]
        self.assertEqual(len(triples),31)
        self.assertTrue(all(row[2]==b'unset' for row in triples),triples)
    def test_review_png_compression_changes_pass_but_pixel_or_size_changes_fail(self):
        image=Image.new('RGBA',(4,4),(12,30,50,255));a=io.BytesIO();b=io.BytesIO()
        image.save(a,format='PNG',compress_level=0);image.save(b,format='PNG',compress_level=9)
        self.assertNotEqual(a.getvalue(),b.getvalue());self.assertTrue(same_png(a.getvalue(),b.getvalue()))
        image.putpixel((1,1),(13,30,50,255));self.assertFalse(same_png(a.getvalue(),encode(image)))
        self.assertFalse(same_png(a.getvalue(),encode(image.crop((0,0,3,4)))))
    def test_offline_gallery_has_all_sources_and_exact_candidate_dimensions(self):
        rendered=outputs();page=next(data for path,data in rendered.items() if path.name=='gallery.html').decode()
        for row in self.rows:self.assertIn(row['id'],page)
        for path,data in rendered.items():
            if path.name.endswith('-16x9.png'):
                with Image.open(io.BytesIO(data)) as image:self.assertEqual(image.size,(960,540))
            if path.name.endswith('-3440x1440.png'):
                with Image.open(io.BytesIO(data)) as image:self.assertEqual(image.width*1440,image.height*3440)
    def test_inherited78_sources_and_metadata_preserved(self):
        baseline=json.loads((HERE/'preserved_sources.json').read_text())
        self.assertEqual(len(baseline['files']),156)
        self.assertEqual(sum(p.endswith('.png') for p in baseline['files']),78)
        self.assertEqual(baseline['base_commit'],'25ab6721073992fdfff31eeb4baea42cdedf81c8')

if __name__=='__main__':unittest.main(verbosity=2)
