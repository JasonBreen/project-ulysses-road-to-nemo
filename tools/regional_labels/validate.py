"""Pin caption-repair source gates to an exact candidate without native testing."""
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


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path,required=True);parser.add_argument('--baseline',type=Path,required=True);parser.add_argument('--output',type=Path,default=ROOT/'docs/evidence/regional-labels/final');args=parser.parse_args()
    if not (args.baseline/'map').is_dir():raise SystemExit('Baseline must be the immutable mod payload containing map/')
    args.output.mkdir(parents=True,exist_ok=True);py=[sys.executable,'-B'];engine=str(args.reference.resolve());baseline=str(args.baseline.resolve())
    jobs=[('labels',py+['tools/regional_labels/test_labels.py','--reference',engine]),('caption-audit',py+['tools/regional_labels/audit.py','--reference',engine,'--gate-reviewed','--output',str(args.output/'caption-audit.json')]),('focus',py+['tools/Test-FocusScreenRepairs.py']),('decisions',py+['tools/Test-DecisionUI.py']),('privacy-screenshots',py+['tools/Test-OverhaulRepairs.py']),('registry',py+['tools/world_foundation/registry.py','--check']),('assets',py+['tools/audit_visual_dependencies.py','--strict-all']),('static',['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246','-ReferenceGameRoot',engine,'-BaselineRoot',baseline])]
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    def run(pair):
        name,cmd=pair;start=time.monotonic();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});text=(p.stdout+p.stderr).decode('utf-8',errors='replace');shown=['python' if c==sys.executable else c for c in cmd]
        for path,label in ((ROOT,'<repository>'),(args.reference,'<installed-reference>'),(args.baseline,'<immutable-baseline-payload>')):
            for spelling in (str(path.resolve()),path.resolve().as_posix()):text=text.replace(spelling,label);shown=[c.replace(spelling,label) for c in shown]
        (args.output/(name+'.txt')).write_text(text,encoding='utf-8',newline='\n');print(name+': '+('PASS' if p.returncode==0 else 'FAIL'),flush=True)
        return dict(name=name,command=shown,exit_code=p.returncode,seconds=round(time.monotonic()-start,3),log=name+'.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,jobs))
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()!=head:raise SystemExit('Source commit changed during verification')
    payload=hashlib.sha256()
    for path in sorted((ROOT/'mod/2985041246').rglob('*'),key=lambda p:p.as_posix()):
        if path.is_file():payload.update(path.relative_to(ROOT).as_posix().encode()+b'\0'+path.read_bytes())
    report=dict(source_head=head,payload_sha256=payload.hexdigest(),payload_hash_rule='Sorted repository-relative POSIX path,NUL,raw bytes for every delivered mod file.',checks=rows,passed=sum(r['exit_code']==0 for r in rows),failed=sum(r['exit_code']!=0 for r in rows),source_scope='206state/37locality/four school captions; existing geography, points and descriptions preserved.',native_acceptance=False,complete_map_label_acceptance=False)
    (args.output/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n');raise SystemExit(report['failed']!=0)


if __name__=='__main__':main()
