"""Run the candidate gates sequentially and retain source/offline evidence.

One child at a time keeps desktop load modest. No engine is launched; --engine
is used only as a read-only definition and GUI dependency reference.
"""
import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/evidence/anea'


def main():
    global OUT
    parser = argparse.ArgumentParser();parser.add_argument('--engine', type=Path);parser.add_argument('--baseline', type=Path);parser.add_argument('--only')
    parser.add_argument('--output', type=Path, default=OUT,
                        help='Evidence directory; defaults to the original Anea record')
    parser.add_argument('--base', default='cf8fec41abe5080b1af66eb86189b35c7af522f6')
    args = parser.parse_args()
    OUT = args.output
    py = [sys.executable, '-B']
    checks = {
        'anea-foundation': py + ['tools/anea/test_foundation.py'] + (['--reference', str(args.engine)] if args.engine else []),
        'anea-campaign': py + ['tools/Test-AneaCampaign.py'],
        'anea-systems': py + ['tools/Test-AneaSystems.py'],
        'anea-integration': py + ['tools/Test-AneaIntegration.py'],
        'anea-art': py + ['tools/Test-AneaArt.py'],
        'anea-presentation': py + ['tools/Test-AneaPresentation.py'],
        'usea-expansion': py + ['tools/Test-UseaExpansion.py'],
        'interface-repairs': py + ['tools/Test-InterfaceRepairs.py'],
        'continental-war': py + ['tools/Test-ContinentalWar.py'],
        'supporting-countries': py + ['tools/Test-UseaActors.py'],
        'aftermath': py + ['tools/Test-PeaceWeInherit.py'],
        'factions': py + ['tools/Test-UlyssesFactions.py'],
        'projects': py + ['tools/Test-StrangerealProjects.py'],
        'campaign': py + ['tools/validate_campaign.py'],
        'briefing': py + ['tools/frontend_briefing/validate.py'],
        'typography': py + ['tools/frontend_typography/validate.py'],
        'economy': py + ['-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_economy.py'],
        'assets': py + ['tools/audit_visual_dependencies.py', '--strict-all'],
        'generated-war': py + ['tools/build_continental_war.py', '--check'],
        'core': [shutil.which('pwsh') or 'powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'tools/Test-UlyssesStatic.ps1', '-ModRoot', str(ROOT / 'mod/2985041246')] + (['-ReferenceGameRoot', str(args.engine)] if args.engine else []),
    }
    if args.engine:
        checks['screen-dependencies'] = py + ['tools/usea_expansion/audit_screens.py', str(args.engine), '--include-frontend-history', '--output', str(OUT / 'engine-dependencies.json')]
    if args.baseline:
        if not args.engine:raise SystemExit('--baseline requires the read-only --engine reference')
        checks['no-vanilla'] = [shutil.which('pwsh') or 'powershell', '-NoProfile', '-File', 'tools/Validate-NoVanillaAssets.ps1', '-ModRoot', str(ROOT / 'mod/2985041246'), '-ReferenceGameRoot', str(args.engine), '-BaselineRoot', str(args.baseline)]
    retained = []
    if args.only:
        wanted = set(args.only.split(','))
        if wanted - set(checks): raise SystemExit('Unknown checks: ' + str(wanted - set(checks)))
        checks = {k: v for k, v in checks.items() if k in wanted}
        if (OUT / 'static-results.json').exists(): retained = [r for r in json.loads((OUT / 'static-results.json').read_text()) if r['check'] not in wanted]
    OUT.mkdir(parents=True, exist_ok=True)
    results = retained
    for name, command in checks.items():
        start = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        raw = result.stdout + result.stderr
        (OUT / ('static-' + name + '.txt')).write_bytes(raw)
        results.append(dict(check=name, command=command, exit_code=result.returncode, seconds=round(time.monotonic() - start, 2), log='static-' + name + '.txt', coverage='static/offline; no native engine execution'))
        print(name + ': ' + ('PASS' if result.returncode == 0 else 'FAIL'), flush=True)
        (OUT / 'static-results.json').write_text(json.dumps(results, indent=2) + '\n')
    payload = []
    for path in sorted((ROOT / 'mod/2985041246').rglob('*')):
        if path.is_file(): payload.append(dict(file=path.relative_to(ROOT / 'mod/2985041246').as_posix(), sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size))
    manifest = dict(base=args.base, role='source candidate payload; not an installed/native-tested copy', files=payload)
    manifest['content_sha256'] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    (OUT / 'candidate-payload.json').write_text(json.dumps(manifest, indent=2) + '\n')
    raise SystemExit(any(r['exit_code'] for r in results))


if __name__ == '__main__': main()
