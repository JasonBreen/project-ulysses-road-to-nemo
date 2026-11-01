"""Retain offline evidence for stories on the complete prerequisite stack.

The installed game is an optional read-only script reference. This never launches
the game or automates the desktop, and it cannot establish native acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/evidence/squadrons/integration'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', type=Path)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    python_checks = [
        ('narrative', ['tools/squadrons/build.py', '--check']),
        ('runtime', ['tools/Test-SquadronStories.py']),
        ('artwork', ['tools/Test-SquadronArt.py']),
        ('partner-owner-contracts', ['tools/usean_partners/test_integration.py']),
        ('world-foundation', ['tools/world_foundation/test_foundation.py']),
        ('country-registry', ['tools/world_foundation/registry.py', '--check']),
        ('focus-canvas', ['tools/Test-FocusScreenRepairs.py']),
        ('decisions', ['tools/Test-DecisionUI.py']),
        ('overhaul', ['tools/Test-OverhaulRepairs.py']),
        ('roadmap', ['tools/overhaul/check_release_plan.py']),
        ('assets', ['tools/audit_visual_dependencies.py', '--strict-all']),
    ]
    checks = [(name, [sys.executable, '-B', *arguments]) for name, arguments in python_checks]
    pwsh = shutil.which('pwsh')
    if not pwsh:
        raise SystemExit('PowerShell 7 (pwsh) is required for the full static suite')
    core = [pwsh, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
            'tools/Test-UlyssesStatic.ps1', '-ModRoot', 'mod/2985041246']
    if args.engine:
        core += ['-ReferenceGameRoot', str(args.engine.resolve())]
    checks.append(('core', core))
    results = []
    for name, command in checks:
        started = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True)
        log = (result.stdout + result.stderr).decode('utf-8', errors='replace')
        shown = ['python' if command[0] == sys.executable else 'pwsh', *command[1:]]
        for spelling in (str(ROOT), ROOT.as_posix()):
            log = log.replace(spelling, '<repository>')
        if args.engine:
            log = log.replace(str(args.engine), '<installed-engine-reference>')
            shown = [part.replace(str(args.engine.resolve()), '<installed-engine-reference>') for part in shown]
        (OUT / (name + '.txt')).write_text(log, encoding='utf-8', newline='\n')
        results.append(dict(check=name, command=shown, exit_code=result.returncode,
                            seconds=round(time.monotonic() - started, 2), log=name + '.txt'))
        print(name + ': ' + ('PASS' if result.returncode == 0 else 'FAIL'), flush=True)
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    digest = hashlib.sha256()
    paths = sorted((ROOT / 'mod/2985041246').rglob('*'), key=lambda p: p.as_posix())
    for path in paths:
        if path.is_file():
            digest.update(path.relative_to(ROOT).as_posix().encode() + b'\0' + path.read_bytes())
    record = dict(coverage='Source/offline and image inspection only; no native game execution.',
                  source_base_commit=revision, payload_sha256=digest.hexdigest(),
                  payload_hash_rule='Sorted repository-relative POSIX path, NUL, raw file bytes for each delivered mod file.',
                  checks=results, native_status='Paused; untested.')
    (OUT / 'results.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(any(row['exit_code'] for row in results))


if __name__ == '__main__':
    main()
