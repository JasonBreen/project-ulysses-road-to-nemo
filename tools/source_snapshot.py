"""Pin clean repository inputs before/after offline validation.

Generated docs/evidence is excluded deliberately. All other tracked files are
hashed as raw working-tree bytes; staged, unstaged and untracked source changes
are rejected. This is a boundary check, not an immutable execution sandbox.
"""
import hashlib
from pathlib import Path
import subprocess

PATHS=('.',':(exclude)docs/evidence/**')


def git(root,*arguments):
    return subprocess.check_output(['git',*arguments],cwd=root)


def capture(root):
    root=Path(root)
    head=git(root,'rev-parse','HEAD').decode().strip()
    def require_clean():
        if git(root,'status','--porcelain=v1','-z','--untracked-files=all','--',*PATHS):
            raise ValueError('Dirty source inputs: commit or isolate staged, unstaged and untracked changes outside docs/evidence before validation')
    require_clean();digest=hashlib.sha256();count=0
    for name in sorted(git(root,'ls-files','-z','--',*PATHS).split(b'\0')):
        if not name:continue
        path=root/name.decode('utf-8')
        if not path.is_file():raise ValueError('Tracked source input is missing: '+name.decode('utf-8'))
        digest.update(name+b'\0'+path.read_bytes());count+=1
    require_clean()
    if git(root,'rev-parse','HEAD').decode().strip()!=head:
        raise ValueError('Source commit changed during input capture')
    return dict(head=head,files=count,sha256=digest.hexdigest(),
                rule='Sorted tracked repository-relative UTF8 path,NUL,raw working-tree bytes; docs/evidence excluded. Clean Git source required.')


def verify(before,root):
    after=capture(root)
    if before!=after:raise ValueError('Source input commit or raw bytes changed during validation; no final exact-source result may be issued')
    return after
