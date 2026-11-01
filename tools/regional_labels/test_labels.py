"""Actual localization, narrow ownership and inherited-name preservation."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

from build import ROOT,MOD,HERE,OUTPUT,build,entries,validate,state_context,locality_context,all_changes

parser=argparse.ArgumentParser();parser.add_argument('--reference',type=Path);args,rest=parser.parse_known_args()


class RegionalLabels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads((HERE/'labels.json').read_text())

    def test_exact_reviewed_scope_has_provisional_provenance_and_stable_keys(self):
        validate(self.data)
        self.assertEqual(206,len(self.data['changes']));self.assertEqual(206,len({r['value'] for r in self.data['changes']}))
        self.assertEqual({171,607},{r['state'] for r in self.data['excluded']})
        self.assertTrue(all(r['source_layer']=='provisional gameplay' for r in self.data['changes']))
        self.assertEqual(204,sum(r['source_kind']=='earth_template_match' and bool(r['reference_keys']) for r in self.data['changes']))

    def test_actual_effective_replacement_is_unambiguous_and_readable(self):
        actual=entries(MOD/OUTPUT);self.assertEqual(247,len(actual));self.assertTrue((MOD/OUTPUT).read_bytes().startswith(b'\xef\xbb\xbf'))
        replacements=[entries(p) for p in (MOD/'localisation/english/replace').glob('*.yml')]
        for row in all_changes(self.data):
            self.assertEqual(row['value'],actual[row['key']]);self.assertNotEqual(row['old'],actual[row['key']])
            values={captions[row['key']] for captions in replacements if row['key'] in captions}
            self.assertEqual({row['value']},values)

    def test_other_established_and_protected_names_are_not_owned_by_generator(self):
        output=entries(MOD/OUTPUT);selected={r['key'] for r in all_changes(self.data)};self.assertEqual(selected,set(output))
        states=state_context();base=entries(MOD/'localisation/english/state_names_l_english.yml')
        self.assertNotIn(states[171]['key'],output);self.assertNotIn(states[607]['key'],output)
        self.assertEqual('XXX',base[states[607]['key']])
        self.assertNotIn('STATE_4',output);self.assertEqual('Chopinburg',base['STATE_4'])
        self.assertEqual({OUTPUT},set(build()))

    def test_all_thirty_seven_localities_already_have_owned_victory_points(self):
        provinces,points=locality_context();self.assertEqual(37,len(self.data['localities']))
        for row in self.data['localities']:
            self.assertIn(row['province'],points);self.assertEqual({'state':row['state'],'owner':row['owner']},provinces[row['province']])
        data=copy.deepcopy(self.data);data['localities'][0]['province']=0
        with self.assertRaises(ValueError):validate(data)

    def test_school_caption_adaptations_keep_ids_purpose_and_descriptions(self):
        original=entries(MOD/'localisation/english/country_SAP_l_english.yml');output=entries(MOD/OUTPUT)
        self.assertEqual(4,len(self.data['institution_captions']))
        for key,expected in self.data['preserved_description_sha256'].items():
            self.assertNotIn(key,output);self.assertEqual(expected,hashlib.sha256(original[key].encode('utf-8')).hexdigest())
        for row in self.data['institution_captions']:
            self.assertEqual(row['old'],original[row['key']]);self.assertEqual(row['value'],output[row['key']])

    def test_changed_source_ownership_duplicate_and_protected_mutations_fail(self):
        for mutation in ('owner','duplicate','protected','original','caption'):
            data=copy.deepcopy(self.data)
            if mutation=='owner':data['changes'][0]['owner']='PLH'
            elif mutation=='duplicate':data['changes'][1]=copy.deepcopy(data['changes'][0])
            elif mutation=='protected':data['changes'][0]['state']=607
            elif mutation=='original':data['changes'][0]['old']='A different inherited label'
            else:data['changes'][0]['value']='123'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):validate(data)

    def test_generation_is_exact_and_its_output_has_no_physical_paths(self):
        for relative,data in build().items():
            self.assertEqual(data,(MOD/relative).read_bytes().replace(b'\r\n',b'\n'))
            self.assertTrue(relative.startswith('localisation/english/replace/'))
        for name in ('build.py','render_review.py'):
            p=subprocess.run([sys.executable,'-B',str(HERE/name),'--check'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(0,p.returncode,p.stdout+p.stderr)

    @unittest.skipUnless(args.reference,'Primary metadata recapture not supplied; source provenance is not native acceptance')
    def test_installed_primary_names_match_only_the_reviewed_captions(self):
        for field,rows in [('reference',self.data['changes']),('locality_reference',self.data['localities'])]:
            ref=self.data[field];path=args.reference/ref['path'].removeprefix('engine://')
            self.assertEqual(ref['sha256'],hashlib.sha256(path.read_bytes()).hexdigest());names=entries(path)
            for row in rows:
                if row['source_kind']=='earth_template_match':self.assertEqual(set(row['reference_keys']),{key for key,value in names.items() if value==row['old']})
        missing=set(self.data['missing_loose_english_caption_keys'])
        for path in (args.reference/'localisation/english').rglob('*.yml'):
            self.assertFalse(missing&set(entries(path)),str(path))
        from audit import report
        current=report(args.reference)
        self.assertTrue(current['reviewed_repair_scope_passed'],current['remaining'])
        self.assertFalse(current['complete_map_label_acceptance'])


if __name__=='__main__':unittest.main(argv=[sys.argv[0],*rest],verbosity=2)
