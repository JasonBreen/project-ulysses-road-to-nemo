"""Actual temporary-Git regressions for offline evidence source identity."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from source_snapshot import capture,verify


class SourceSnapshot(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.run_git('init','--quiet');self.run_git('config','user.name','Source fixture')
        self.run_git('config','user.email','source-fixture@example.invalid')
        self.run_git('config','core.autocrlf','false')
        hooks=self.root/'.git/empty-hooks';hooks.mkdir();self.run_git('config','core.hooksPath',str(hooks))
        (self.root/'tools').mkdir();(self.root/'tools/check.py').write_bytes(b'print("fixture")\n')
        (self.root/'.gitattributes').write_bytes(b'*.py text eol=lf\n')
        self.commit()

    def run_git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.root,stderr=subprocess.DEVNULL)

    def commit(self):
        self.run_git('add','--all');self.run_git('commit','--quiet','-m','Fixture input')

    def test_clean_source_pins_inputs_and_allows_generated_evidence(self):
        before=capture(self.root);self.assertEqual(2,before['files'])
        evidence=self.root/'docs/evidence/fixture';evidence.mkdir(parents=True)
        (evidence/'results.json').write_text('{}')
        self.assertEqual(before,verify(before,self.root))

    def test_staged_unstaged_and_untracked_source_are_rejected(self):
        path=self.root/'tools/check.py';original=path.read_bytes()
        path.write_bytes(original+b'# changed\n')
        with self.assertRaisesRegex(ValueError,'Dirty source'):capture(self.root)
        self.run_git('add','tools/check.py')
        with self.assertRaisesRegex(ValueError,'Dirty source'):capture(self.root)
        self.run_git('reset','--quiet','HEAD','--','tools/check.py');path.write_bytes(original)
        extra=self.root/'tools/untracked.py';extra.write_bytes(b'# fixture\n')
        with self.assertRaisesRegex(ValueError,'Dirty source'):capture(self.root)

    def test_clean_new_commit_is_not_the_same_source(self):
        before=capture(self.root);(self.root/'tools/check.py').write_bytes(b'print("other")\n');self.commit()
        with self.assertRaisesRegex(ValueError,'changed during validation'):verify(before,self.root)

    def test_raw_checkout_change_cannot_hide_behind_git_text_normalization(self):
        before=capture(self.root);path=self.root/'tools/check.py'
        path.write_bytes(path.read_bytes().replace(b'\n',b'\r\n'))
        self.run_git('add','--renormalize','--','tools/check.py')
        self.assertFalse(self.run_git('status','--porcelain','--','tools/check.py'))
        with self.assertRaisesRegex(ValueError,'changed during validation'):verify(before,self.root)


if __name__=='__main__':unittest.main(verbosity=2)
