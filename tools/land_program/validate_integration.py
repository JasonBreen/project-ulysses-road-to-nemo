"""Pin affected LAND integration gates to an exact source/payload; no game launch."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'docs/evidence/land-program/integration/final')
    parser.add_argument('--only',help='Comma-separated affected gates; retain earlier phases in their own output directories.')
    args=parser.parse_args()
    if not (args.baseline/'map').is_dir():raise SystemExit('Baseline must be the immutable mod payload containing map/')
    args.output.mkdir(parents=True,exist_ok=True)
    py=[sys.executable,'-B'];engine=str(args.engine.resolve());baseline=str(args.baseline.resolve())
    jobs=[
        ('land',py+['tools/land_program/test_land.py','--engine',engine]),
        ('upkeep',py+['tools/Test-ForceUpkeep.py','--engine',engine]),
        ('macro',py+['tools/Test-EconomyV2.py']),
        ('shared',py+['tools/Test-SharedSystems.py']),
        ('startup',py+['tools/Test-NativeCompatibilityContracts.py']),
        ('world-coverage',py+['tools/world_starts/coverage.py','--check','--require-integrated-owner']),
        ('registry',py+['tools/world_foundation/registry.py','--check']),
        ('decisions',py+['tools/Test-DecisionUI.py']),
        ('macro-generated',py+['tools/economy_v2/build.py','--check']),
        ('assets',py+['tools/audit_visual_dependencies.py','--strict-all']),
        ('presentation',py+['tools/check_presentation_sources.py']),
        ('research-inventory',py+['tools/overhaul/audit_consumers.py',engine,'--screen','countrytechtreeview.gui','--summary-only','--output',str(args.output/'research-dependencies.json')]),
        ('fonts',py+['tools/research_fonts/test_fonts.py']),
        ('font-generated',py+['tools/research_fonts/build.py','--check']),
        ('font-measure',py+['tools/research_fonts/measure.py','--check']),
        ('ownership',py+['tools/research_fonts/capture_reference.py','--engine',engine,'--output',str(args.output/'authored-research-dependencies.json')]),
        ('labels',py+['tools/regional_labels/test_labels.py','--reference',engine]),
        ('focus-captions',py+['tools/Test-FocusScreenRepairs.py']),
        ('static',['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246','-ReferenceGameRoot',engine,'-BaselineRoot',baseline]),
    ]
    if args.only:
        selected=set(args.only.split(','));known={name for name,_ in jobs}
        if selected-known:raise SystemExit('Unknown gates: '+', '.join(sorted(selected-known)))
        jobs=[pair for pair in jobs if pair[0]in selected]
    source=capture(ROOT);head=source['head']
    def run(pair):
        name,cmd=pair;start=time.monotonic()
        p=subprocess.run(cmd,cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        text=(p.stdout+p.stderr).decode('utf-8',errors='replace');shown=['python' if c==sys.executable else c for c in cmd]
        for path,label in ((ROOT,'<repository>'),(args.engine,'<installed-reference>'),(args.baseline,'<immutable-baseline-payload>')):
            for spelling in (str(path.resolve()),path.resolve().as_posix()):
                text=text.replace(spelling,label);shown=[c.replace(spelling,label) for c in shown]
        (args.output/(name+'.txt')).write_text(text,encoding='utf-8',newline='\n')
        print(name+': '+('PASS' if p.returncode==0 else 'FAIL'),flush=True)
        return dict(name=name,command=shown,exit_code=p.returncode,seconds=round(time.monotonic()-start,3),log=name+'.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,jobs))
    verify(source,ROOT)
    payload=hashlib.sha256()
    for path in sorted((ROOT/'mod/2985041246').rglob('*'),key=lambda p:p.as_posix()):
        if path.is_file():payload.update(path.relative_to(ROOT).as_posix().encode()+b'\0'+path.read_bytes())
    report=dict(source_head=head,source_inputs=source,payload_sha256=payload.hexdigest(),payload_hash_rule='Sorted repository-relative POSIX path,NUL,raw bytes for every delivered mod file.',checks=rows,passed=sum(r['exit_code']==0 for r in rows),failed=sum(r['exit_code']!=0 for r in rows),native_acceptance=False,research_inventory_scope='Source inventory only; no complete presentation/provenance gate was requested. Screen failures remain visible in research-dependencies.json.',full_conversion_acceptance=False)
    (args.output/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    raise SystemExit(report['failed']!=0)


if __name__=='__main__':main()
