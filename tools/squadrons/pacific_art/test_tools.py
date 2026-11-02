"""Reject invalid authoring inputs before mutations and retain provenance."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(HERE.parent)]
from gallery_bitmap import GalleryFont


def module(name):
    spec=importlib.util.spec_from_file_location('review_'+name,HERE/(name+'.py'))
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result


class AuthoringTools(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve()
        self.here=self.root/'squadrons/pacific_art';self.here.mkdir(parents=True)
        self.selected=self.here.parent/'sources/portraits/pilot_one.png';self.selected.parent.mkdir(parents=True)
        self.generated=self.root/'generated_images';self.generated.mkdir();self.output=self.generated/'edit.png'
        for path,color in((self.selected,'navy'),(self.output,'cyan')):Image.new('RGBA',(4,4),color).save(path)
        self.meta=self.selected.with_suffix('.json');self.meta.write_text(json.dumps({'prompt':'Original prompt','sha256':hashlib.sha256(self.selected.read_bytes()).hexdigest()}))
        (self.here/'plan.json').write_text(json.dumps({'assets':[{'id':'pilot_one','file':'portraits/pilot_one.png','prompt':'Original prompt'}]}))
        self.prompt=self.root/'prompt.json';self.prompt.write_text(json.dumps({'id':'pilot_one','prompt':'New prompt','reason':'Reviewed change'}))
        self.receipt=self.root/'receipt.json';self.receipt.write_text(json.dumps([{'id':'edit','source_path':str(self.output)}]))
        self.select=module('select_edit');self.revise=module('prompt_revision')

    def tearDown(self):
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()));self.tmp.cleanup()

    def snapshot(self):return {path.relative_to(self.root).as_posix():path.read_bytes()for path in self.root.rglob('*')if path.is_file()}

    def choose(self):
        with patch.object(self.select,'HERE',self.here),patch.object(self.select,'generated_home',return_value=self.generated):
            self.select.select('pilot_one',self.receipt,'edit',self.prompt)

    def test_missing_prompt_keeps_master_metadata_plan_and_history_unchanged(self):
        self.prompt.unlink();before=self.snapshot()
        with self.assertRaises(FileNotFoundError):self.choose()
        self.assertEqual(before,self.snapshot());self.assertFalse((self.here.parent/'revisions').exists())

    def test_malformed_prompt_keeps_all_existing_bytes_unchanged(self):
        self.prompt.write_text('{');before=self.snapshot()
        with self.assertRaises(json.JSONDecodeError):self.choose()
        self.assertEqual(before,self.snapshot())

    def test_signature_only_invalid_png_cannot_replace_a_master(self):
        self.output.write_bytes(b'\x89PNG\r\n\x1a\nnot a decodable image');before=self.snapshot()
        with self.assertRaises(OSError):self.choose()
        self.assertEqual(before,self.snapshot());self.assertFalse((self.here.parent/'revisions').exists())

    def test_missing_metadata_is_rejected_before_master_replacement(self):
        self.meta.unlink();before=self.snapshot()
        with self.assertRaises(FileNotFoundError):self.choose()
        self.assertEqual(before,self.snapshot())

    def test_valid_edit_retains_original_and_hashes_exact_validated_input(self):
        original=self.selected.read_bytes();edited=self.output.read_bytes();self.choose()
        self.assertEqual(edited,self.selected.read_bytes())
        self.assertEqual(original,(self.here.parent/'revisions/pilot_one_before_edit.png').read_bytes())
        info=json.loads(self.meta.read_text());self.assertEqual(hashlib.sha256(edited).hexdigest(),info['sha256'])
        self.assertEqual('Original prompt',info['base_prompt']);self.assertFalse(info['visual_reviewed'])

    def test_prompt_retry_cannot_overwrite_retained_original_history(self):
        with patch.object(self.revise,'HERE',self.here):
            first=self.revise.revise(self.prompt);self.assertEqual('Original prompt',first['previous_prompt'])
            before=self.snapshot()
            with self.assertRaises(FileExistsError):self.revise.revise(self.prompt)
            self.assertEqual(before,self.snapshot())

    def test_bad_metadata_cannot_leave_partial_prompt_revision(self):
        self.meta.write_text('{');before=self.snapshot()
        with patch.object(self.revise,'HERE',self.here),self.assertRaises(json.JSONDecodeError):self.revise.revise(self.prompt)
        self.assertEqual(before,self.snapshot());self.assertFalse((self.here/'prompt_revisions').exists())

    def test_gallery_labels_do_not_depend_on_platform_freetype(self):
        with patch.object(ImageFont,'truetype',side_effect=AssertionError('No platform font rasterizer')):
            one=Image.new('RGBA',(240,50));two=Image.new('RGBA',(240,50))
            font=GalleryFont();font.draw(one,'OSE | original fiction',(8,8),220,size=13)
            font.draw(two,'OSE | original fiction',(8,8),220,size=13)
        self.assertIsNotNone(one.getbbox());self.assertEqual(one.tobytes(),two.tobytes())


if __name__=='__main__':unittest.main(verbosity=2)
