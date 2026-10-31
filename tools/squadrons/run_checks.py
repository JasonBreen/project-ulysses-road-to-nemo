"""Retain source-only squadron runtime evidence; artwork has a separate gate."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/evidence/squadrons'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    checks = [
        ('generated-narrative', ['tools/squadrons/build.py', '--check']),
        ('runtime', ['tools/Test-SquadronStories.py']),
    ]
    results = []
    for name, arguments in checks:
        command = [sys.executable, '-B', *arguments]
        started = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True)
        log = (result.stdout + result.stderr).decode('utf-8', errors='replace')
        for spelling in (str(ROOT), ROOT.as_posix()):
            log = log.replace(spelling, '<repository>')
        (OUT / (name + '.txt')).write_text(log, encoding='utf-8', newline='\n')
        results.append(dict(check=name, command=['python', '-B', *arguments], exit_code=result.returncode,
                            seconds=round(time.monotonic()-started, 2), log=name+'.txt'))
        print(name + ': ' + ('PASS' if result.returncode == 0 else 'FAIL'), flush=True)
    paths = [ROOT / 'tools/Test-SquadronStories.py', ROOT / 'tools/Test-ContinentalWar.py',
             ROOT / 'tools/economy_script.py', *sorted((ROOT/'tools/squadrons').glob('*.py')),
             ROOT/'tools/squadrons/campaigns.json', ROOT/'tools/squadrons/art_plan.json',
             ROOT/'tools/squadrons/engine_contracts.json',
             *sorted((ROOT/'tools/squadrons/chapters').glob('*.json'))]
    # Artwork tooling is owned independently and is not a runtime input.
    paths = [p for p in paths if p.name not in ('build_art.py', 'run_checks.py')]
    generated = [ROOT/'mod/2985041246'/relative for relative in (
        'common/scripted_triggers/ac_squadrons.txt', 'common/scripted_effects/ac_squadrons.txt',
        'common/on_actions/ac_squadrons.txt', 'events/ac_squadrons.txt',
        'common/decisions/ac_squadrons.txt', 'common/decisions/categories/ac_squadrons.txt',
        'common/game_rules/ac_squadrons.txt', 'common/ideas/ac_squadrons.txt',
        'localisation/english/ac_squadrons_l_english.yml')]
    paths += generated
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    data = dict(coverage='Actual-script and source/offline checks only; narrative read-through is documented separately.',
                base_commit=revision, source_state='Working-tree candidate; source hashes identify this tested payload.',
                source_sha256={p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                checks=results, native_status='Paused; not tested.',
                artwork_status='Separate Test-SquadronArt.py gate; not executed by this runtime runner.')
    (OUT/'runtime-results.json').write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8', newline='\n')
    raise SystemExit(any(row['exit_code'] for row in results))


if __name__ == '__main__':
    main()
