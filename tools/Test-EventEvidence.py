"""Real subprocess crashes/freshness and failed-current-receipt regressions."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from event_picture_fit.evidence import begin,run_json_audit,screen_failures,finish


class EventEvidence(unittest.TestCase):
    def run_audit(self,folder,code):
        output=Path(folder)/'effective-eventwindow.json'
        command=[sys.executable,'-B','-c',code,str(output)]
        return run_json_audit(command,output,capture_output=True)

    def test_begin_invalidates_prior_passing_receipt_and_retains_its_logs(self):
        with tempfile.TemporaryDirectory()as folder:
            out=Path(folder);prior=dict(passed=True,checks=[dict(log='audit.txt')])
            (out/'results.json').write_text(json.dumps(prior));(out/'audit.txt').write_text('original log')
            begin(out);current=json.loads((out/'results.json').read_text())
            self.assertFalse(current['passed']);self.assertEqual('running',current['status'])
            old=out/current['superseded_report'];self.assertEqual(prior,json.loads(old.read_text()))
            self.assertEqual('original log',(old.parent/'audit.txt').read_text())

    def test_real_crash_cannot_reuse_old15_report_or_passing_receipt(self):
        with tempfile.TemporaryDirectory()as folder:
            out=Path(folder);(out/'results.json').write_text('{"passed":true}')
            (out/'effective-eventwindow.json').write_text('{"gate_covered_screens":{"eventwindow.gui":{"failures":["old"]}}}')
            begin(out);proc,report,error=self.run_audit(out,'raise SystemExit(1)')
            self.assertEqual(1,proc.returncode);self.assertIsNone(report);self.assertIn('fresh audit',error)
            self.assertFalse((out/'effective-eventwindow.json').exists())
            row=dict(exit_code=proc.returncode,accepted_contract=False,decision_failures=screen_failures(report,'countrydecisionview.gui'))
            result=finish(out,{'head':'fixture'},{'head':'fixture'},[row],error)
            self.assertEqual('failed',result['status']);self.assertFalse(result['passed'])
            self.assertIsNone(json.loads((out/'results.json').read_text())['checks'][0]['decision_failures'])

    def test_invalid_fresh_json_is_not_a_current_report(self):
        with tempfile.TemporaryDirectory()as folder:
            proc,report,error=self.run_audit(folder,"from pathlib import Path;import sys;Path(sys.argv[1]).write_text('{');raise SystemExit(1)")
            self.assertEqual(1,proc.returncode);self.assertIsNone(report);self.assertIn('invalid fresh',error)

    def test_fresh_decision_failures_are_recorded_instead_of_erased(self):
        payload={'gate_covered_screens':{'eventwindow.gui':{'failures':['changed']},'countrydecisionview.gui':{'failures':['sprite:broken']}}}
        with tempfile.TemporaryDirectory()as folder:
            code='from pathlib import Path;import sys;Path(sys.argv[1]).write_text('+repr(json.dumps(payload))+');raise SystemExit(1)'
            proc,report,error=self.run_audit(folder,code);self.assertIsNone(error)
            decisions=screen_failures(report,'countrydecisionview.gui');self.assertEqual(['sprite:broken'],decisions)
            row=dict(exit_code=proc.returncode,accepted_contract=False,decision_failures=decisions)
            result=finish(folder,{'head':'fixture'},{'head':'fixture'},[row],'Unexpected ownership result')
            self.assertFalse(result['passed']);self.assertEqual(decisions,result['checks'][0]['decision_failures'])

    def test_missing_or_malformed_screen_is_not_an_empty_failure_list(self):
        for report in (None,[],{},dict(gate_covered_screens=[]),dict(gate_covered_screens={'eventwindow.gui':{'failures':False}})):
            with self.subTest(report=report):self.assertIsNone(screen_failures(report,'eventwindow.gui'))

    def test_changed_source_cannot_receive_a_passing_receipt(self):
        with tempfile.TemporaryDirectory()as folder:
            result=finish(folder,{'head':'before'},{'head':'after'},[dict(exit_code=0)])
            self.assertFalse(result['passed']);self.assertEqual('failed',result['status'])

    def test_fresh_known_backlog_remains_explicit_in_a_bounded_contract(self):
        with tempfile.TemporaryDirectory()as folder:
            row=dict(exit_code=1,accepted_contract=True,expected_legacy_ownership_failure=True,decision_failures=[])
            result=finish(folder,{'head':'fixture'},{'head':'fixture'},[row])
            self.assertTrue(result['passed']);self.assertEqual(1,result['checks'][0]['exit_code'])
            self.assertFalse(result['native_acceptance'])

    def test_empty_run_cannot_certify_any_checks(self):
        with tempfile.TemporaryDirectory()as folder:
            self.assertFalse(finish(folder,{'head':'fixture'},{'head':'fixture'},[])['passed'])


if __name__=='__main__':unittest.main(verbosity=2)
