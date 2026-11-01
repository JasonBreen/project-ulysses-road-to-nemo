"""Retain bounded NAVAL source/offline results; never launches the engine."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/evidence/naval-program'
sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--engine',type=Path);parser.add_argument('--core',action='store_true');parser.add_argument('--only');parser.add_argument('--exact-source',action='store_true')
    args=parser.parse_args();py=[sys.executable,'-B'];reference=['--reference',str(args.engine)] if args.engine else []
    if args.exact_source and args.only:raise SystemExit('An exact-source receipt requires a full run; retained earlier checks cannot be relabelled for a new commit')
    before=capture(ROOT) if args.exact_source else None
    checks={
        'naval':py+['tools/naval_program/test_naval.py']+(['--engine',str(args.engine)] if args.engine else []),
        'air':py+['tools/air_program/test_air.py'],
        'land':py+['tools/land_program/test_land.py'],
        'fonts':py+['tools/research_fonts/test_fonts.py'],
        'macro':py+['tools/Test-EconomyV2.py'],
        'upkeep':py+['tools/Test-ForceUpkeep.py']+(['--engine',str(args.engine)] if args.engine else []),
        'world-50':py+['tools/world_starts/test_world_starts.py']+reference,
        'anea-2':py+['tools/anea/test_foundation.py']+reference,
        'world-5':py+['tools/world_foundation/test_foundation.py'],
        'legacy-4':py+['tools/world_legacy/test_legacy.py'],
        'replacements':py+['tools/replacements/test_replacements.py'],
        'all-61-selected-starts':py+['tools/world_starts/coverage.py','--check','--require-integrated-owner'],
        'interfaces':py+['tools/Test-InterfaceRepairs.py'],
        'assets':py+['tools/audit_visual_dependencies.py','--strict-all'],
        'generated-macro':py+['tools/economy_v2/build.py','--check'],
        'capability-contract':py+['tools/naval_program/audit.py','--check']+reference,
        'source-snapshot':py+['tools/Test-SourceSnapshot.py'],
    }
    # audit's read-only argument is --reference; the same reference list applies.
    if args.core:
        host=shutil.which('pwsh')
        if not host:raise SystemExit('Current pwsh is required for full source/map validation')
        checks['static']=[host,'-NoProfile','-ExecutionPolicy','Bypass','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246']
        if args.engine:checks['static']+=['-ReferenceGameRoot',str(args.engine)]
    if args.engine:
        checks['research-consumers']=py+['tools/overhaul/audit_consumers.py',str(args.engine),
            '--profile','tools/research_fonts/audit_profile.json','--summary-only',
            '--gate-screen','countrytechtreeview.gui','--gate-screen','ac_air_techtree.gui',
            '--gate-screen','equipmentdesigner/planes/ac_air_blueprints.gui','--gate-screen','ac_naval_techtree.gui','--gate-screen','equipmentdesigner/ships/ac_naval_blueprints.gui',
            '--output','docs/evidence/naval-program/research-consumers.json']
    old=[]
    if args.only:
        names=set(args.only.split(','))
        if names-set(checks):raise SystemExit('Unknown checks: '+str(names-set(checks)))
        checks={k:v for k,v in checks.items() if k in names}
        if (OUT/'results.json').exists():old=[r for r in json.loads((OUT/'results.json').read_text())['checks'] if r['check'] not in names]
    OUT.mkdir(parents=True,exist_ok=True)
    def run(pair):
        name,command=pair;start=time.monotonic();result=subprocess.run(command,cwd=ROOT,capture_output=True)
        output=(result.stdout+result.stderr).decode('utf-8',errors='replace').replace('\r\n','\n')
        for path,label in [(ROOT,'<repository>'),(args.engine,'<installed-primary-reference>')]:
            if path:
                for spelling in (str(path),path.as_posix()):output=output.replace(spelling,label)
        (OUT/(name+'.txt')).write_bytes(output.encode('utf-8'))
        safe=['python' if part==sys.executable else '<installed-primary-reference>' if args.engine and part==str(args.engine) else part for part in command]
        print(name+': '+('PASS' if result.returncode==0 else 'FAIL'),flush=True)
        return dict(check=name,command=safe,exit_code=result.returncode,seconds=round(time.monotonic()-start,2),log=name+'.txt',coverage='source/offline; no native game execution')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,checks.items()))
    after=verify(before,ROOT) if before else None
    result=dict(schema=1,base_commit=json.loads((ROOT/'tools/naval_program/preserved_sources.json').read_text())['base_commit'],
        source_state='Exact clean committed source verified before/after all checks' if before else 'Working-tree candidate; retained results may cover earlier source',source_snapshot=after,native_acceptance=False,
        native_status='Paused; ship missions, research UI/designer/AI/construction/refit/save behavior remains untested',checks=sorted(old+rows,key=lambda r:r['check']))
    (OUT/'results.json').write_bytes((json.dumps(result,indent=2)+'\n').encode('utf-8'))
    if before:
        receipt=dict(schema=1,tested_code_commit=before['head'],before=before,after=after,source_inputs_unchanged=before==after,
            passed=not any(r['exit_code'] for r in rows),check_count=len(rows),native_acceptance=False,
            scope='Exact clean source/raw bytes and selected source/offline gates only; docs/evidence excluded, no native acceptance')
        (OUT/'source-receipt.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
    raise SystemExit(any(r['exit_code'] for r in result['checks']))


if __name__=='__main__':main()
