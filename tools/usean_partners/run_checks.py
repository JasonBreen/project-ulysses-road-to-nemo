"""Retain integrated partner source evidence; never runs the game."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/evidence/usean-partners/integration'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--engine',type=Path);parser.add_argument('--core',action='store_true');args=parser.parse_args()
    py=[sys.executable,'-B']
    checks={
        'partners':py+['tools/usean_partners/test_content.py','--require-dependencies'],
        'real-owners':py+['tools/usean_partners/test_integration.py'],
        'world':py+['tools/world_foundation/test_foundation.py'],
        'macro':py+['tools/Test-EconomyV2.py'],
        'shared':py+['tools/Test-SharedSystems.py'],
        'ledger':py+['tools/Test-EconomyLedger.py'],
        'institutions':py+['tools/Test-Institutions.py'],
        'forces':py+['tools/Test-ForceUpkeep.py'],
        'partner-generation':py+['tools/usean_partners/build.py','--check','--require-dependencies'],
        'world-generation':py+['tools/world_foundation/build.py','--check'],
        'anea-generation':py+['tools/anea/foundation.py','--check'],
        'macro-generation':py+['tools/economy_v2/build.py','--check'],
        'institution-generation':py+['tools/institutions/build.py','--check'],
        'government-generation':py+['tools/usea_expansion/build_leaders.py','--check'],
        'registry':py+['tools/world_foundation/registry.py','--check'],
        'assets':py+['tools/audit_visual_dependencies.py','--strict-all'],
    }
    if args.engine:
        checks['partners']+=['--engine',str(args.engine)]
        checks['world']+=['--reference',str(args.engine)]
        checks['forces']+=['--engine',str(args.engine)]
        checks['eru-budget']=py+['tools/world_foundation/budget.py','--reference',str(args.engine),'--check']
    if (ROOT/'tools/overhaul/build_overview.py').exists():
        checks['overview-generation']=py+['tools/overhaul/build_overview.py','--check']
        checks['regional-label-generation']=py+['tools/overhaul/build_regional_labels.py','--check']
        checks['release-plan']=py+['tools/overhaul/check_release_plan.py']
    if args.core:
        checks['core']=['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246']
        if args.engine:checks['core']+=['-ReferenceGameRoot',str(args.engine)]
    for name,script in [('focus-screen','Test-FocusScreenRepairs.py'),('decisions-screen','Test-DecisionUI.py'),('overhaul','Test-OverhaulRepairs.py')]:
        if (ROOT/'tools'/script).exists():checks[name]=py+['tools/'+script]
    OUT.mkdir(parents=True,exist_ok=True)
    def run(pair):
        name,command=pair;started=time.monotonic();result=subprocess.run(command,cwd=ROOT,capture_output=True)
        text=(result.stdout+result.stderr).decode('utf-8',errors='replace').replace('\r\n','\n').replace('\r','\n')
        for path,label in [(ROOT,'<repository>'),(args.engine,'<installed-engine-reference>')]:
            if path:
                for spelling in (str(path),path.as_posix()):text=text.replace(spelling,label)
        (OUT/(name+'.txt')).write_text(text,encoding='utf-8',newline='\n')
        safe=['python' if token==sys.executable else '<installed-engine-reference>' if args.engine and token==str(args.engine) else token for token in command]
        row=dict(check=name,command=safe,exit_code=result.returncode,seconds=round(time.monotonic()-started,2),log=name+'.txt')
        print(name+': '+('PASS' if result.returncode==0 else 'FAIL'),flush=True);return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,checks.items()))
    revision=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    inputs=[*sorted((ROOT/'tools/usean_partners').glob('*.py')), *sorted((ROOT/'tools/usean_partners').glob('*.json'))]
    inputs += [ROOT/path for path in ['tools/Test-SharedSystems.py','tools/economy_v2/harness.py',
        'mod/2985041246/common/scripted_effects/ac_macro_effects.txt',
        'mod/2985041246/common/scripted_effects/ac_politics.txt',
        'mod/2985041246/common/scripted_effects/ac_usean_partners.txt',
        'mod/2985041246/common/scripted_triggers/ac_usean_partners.txt',
        'mod/2985041246/common/on_actions/ac_usean_partners.txt',
        'tools/world_foundation/country_registry.json']]
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    (OUT/'results.json').write_text(json.dumps(dict(coverage='Integrated source/offline only; fixtures and copied state are not native acceptance.',
        base_commit=revision,source_state='Working-tree candidate, including recorded integration fixes.',source_sha256=hashes,checks=results,native_status='Paused; untested.'),indent=2)+'\n',encoding='utf-8',newline='\n')
    raise SystemExit(any(row['exit_code'] for row in results))


if __name__=='__main__':main()
