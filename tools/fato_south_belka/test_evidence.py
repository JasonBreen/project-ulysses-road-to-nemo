"""Real subprocess/temp-Git regressions for ordering and tested-source binding."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from evidence_journal import begin,finish,read_current
from record_evidence import collect,capture,export


class EvidenceContracts(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.git('init','-q')
        (self.root/'.gitignore').write_text('runtime-output/\n',encoding='utf-8')
        (self.root/'content.py').write_text('value = 1\n',encoding='utf-8')
        (self.root/'mod/2985041246').mkdir(parents=True)
        (self.root/'mod/2985041246/payload.txt').write_text('actual payload\n',encoding='utf-8')
        self.commit()

    def git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.root,stderr=subprocess.STDOUT)

    def commit(self):
        self.git('add','.')
        self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Fixture source')

    def invoke(self,folder,code=0,pinned=True):
        source=capture(self.root)if pinned else None
        output=self.root/'runtime-output'/folder;output.mkdir(parents=True,exist_ok=True)
        directory,invocation=begin(self.root,output,['actual-check'],source)
        result=subprocess.run([sys.executable,'-c','print("actual subprocess");raise SystemExit('+str(code)+')'],capture_output=True)
        (output/'actual-check.txt').write_bytes(result.stdout+result.stderr)
        report=dict(source_inputs=source,checks=[dict(name='actual-check',exit_code=result.returncode)])
        finish(directory,invocation,report,output)
        return directory,invocation

    def test_fresh_failed_default_folder_supersedes_old_formatting_success(self):
        old,_=self.invoke('formatting-checks');data=(old/'actual-check.txt').read_bytes()
        self.invoke('checks',7)
        with self.assertRaisesRegex(ValueError,'Latest invocation failed'):collect(self.root)
        self.assertEqual(data,(old/'actual-check.txt').read_bytes())

    def test_later_success_retains_failure_and_exact_tested_source(self):
        first,_=self.invoke('checks',3);last,invocation=self.invoke('followup-checks')
        receipt=collect(self.root)
        self.assertEqual(invocation['sequence'],receipt['latest_checks'][0]['invocation']['sequence'])
        self.assertEqual(3,receipt['superseded_attempts'][0]['exit_code'])
        self.assertEqual(capture(self.root),receipt['latest_checks'][0]['source_inputs'])
        self.assertTrue((first/'actual-check.txt').is_file());self.assertTrue((last/'actual-check.txt').is_file())

    def test_changed_uncommitted_source_cannot_receive_old_results(self):
        self.invoke('checks');(self.root/'content.py').write_text('value = 2\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Dirty source inputs'):collect(self.root)

    def test_clean_new_source_commit_cannot_receive_old_results(self):
        self.invoke('checks');(self.root/'content.py').write_text('value = 2\n',encoding='utf-8');self.commit()
        with self.assertRaisesRegex(ValueError,'different or unpinned source'):collect(self.root)

    def test_incomplete_latest_invocation_blocks_older_success(self):
        self.invoke('checks');begin(self.root,self.root/'runtime-output/new-run',['actual-check'],capture(self.root))
        with self.assertRaisesRegex(ValueError,'incomplete'):collect(self.root)

    def test_archive_log_tampering_is_rejected(self):
        directory,_=self.invoke('checks');(directory/'actual-check.txt').write_text('replaced success\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Archived log changed'):collect(self.root)

    def test_unpinned_and_legacy_folder_reports_cannot_certify_current_source(self):
        output=self.root/'runtime-output/fato-south-belka/formatting-checks';output.mkdir(parents=True)
        (output/'checks.json').write_text(json.dumps(dict(checks=[dict(name='actual-check',exit_code=0)])),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'No durable invocations'):collect(self.root)
        self.invoke('checks',pinned=False)
        with self.assertRaisesRegex(ValueError,'different or unpinned source'):collect(self.root)

    def test_duplicate_sequence_or_changed_source_metadata_is_rejected(self):
        first,_=self.invoke('checks');last,_=self.invoke('other')
        path=last/'invocation.json';value=json.loads(path.read_text());value['sequence']=json.loads((first/'invocation.json').read_text())['sequence'];path.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError,'duplicate invocation sequence'):collect(self.root)
        value['sequence']=2;path.write_text(json.dumps(value))
        report=json.loads((last/'checks.json').read_text());report['source_inputs']['sha256']='wrong';(last/'checks.json').write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError,'metadata disagree'):collect(self.root)

    def test_concurrent_allocations_have_unique_durable_monotonic_order(self):
        source=capture(self.root)
        def allocate(index):return begin(self.root,self.root/f'runtime-output/threads/{index}',['actual-check'],source)[1]['sequence']
        with ThreadPoolExecutor(max_workers=2)as executor:sequences=list(executor.map(allocate,range(8)))
        self.assertEqual(list(range(1,9)),sorted(sequences))
        self.assertEqual(9,allocate(9))

    def test_relative_delivery_path_exports_receipt_and_immutable_logs(self):
        self.invoke('checks',3);self.invoke('checks')
        receipt=collect(self.root)
        output=export(self.root,Path('docs/evidence/review/receipt.json'),receipt)
        delivered=json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(self.root/'docs/evidence/review/receipt.json',output)
        self.assertEqual(capture(self.root),delivered['source_inputs'])
        for row in delivered['latest_checks']+delivered['superseded_attempts']:
            self.assertTrue((self.root/row['archived_report']).is_file())
            self.assertTrue((self.root/row['archived_log']).is_file())


if __name__=='__main__':unittest.main()
