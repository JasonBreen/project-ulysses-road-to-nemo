"""Reproducible source/offline profile; never launches the game or desktop."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[3]


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--engine',required=True,type=Path);p.add_argument('--baseline',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    out=a.output;out.mkdir(parents=True,exist_ok=True);py=[sys.executable,'-B'];engine=str(a.engine)
    jobs=[('new-runtime',py+['tools/squadrons/pacific/test_runtime.py']),('new-source-art-preservation',py+['tools/squadrons/pacific/test_source.py']),
      ('original-six-runtime',py+['tools/Test-SquadronStories.py']),('original-art-partition',py+['tools/Test-SquadronArt.py']),
      ('original-pacific-masters',py+['tools/squadrons/pacific_art/test_art.py']),('cpw-runtime',py+['tools/circum_pacific/test_runtime.py']),
      ('national-runtime',py+['tools/pacific_nations/test_runtime.py']),('shared-real-owners',py+['tools/Test-SharedSystems.py']),
      ('macro',py+['tools/Test-EconomyV2.py']),('force-upkeep',py+['tools/Test-ForceUpkeep.py']),('decisions',py+['tools/Test-DecisionUI.py']),
      ('campaign',py+['tools/validate_campaign.py']),('presentation',py+['tools/check_presentation_sources.py']),
      ('assets-strict',py+['tools/audit_visual_dependencies.py','--strict-all']),
      ('static-reference',['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246','-ReferenceGameRoot',engine,'-BaselineRoot',str(a.baseline)])]
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    def run(row):
        name,cmd=row;start=time.monotonic();r=subprocess.run(cmd,cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        text=(r.stdout+r.stderr).decode('utf-8','replace');shown=['python'if c==sys.executable else c for c in cmd]
        for path,label in((ROOT,'<repository>'),(a.engine,'<installed-reference>'),(a.baseline,'<immutable-baseline-payload>')):
            for spelling in(str(path.resolve()),path.resolve().as_posix()):text=text.replace(spelling,label);shown=[c.replace(spelling,label)for c in shown]
        (out/(name+'.txt')).write_text(text.replace('\r\n','\n'),encoding='utf-8',newline='\n');print(name+': '+('PASS'if r.returncode==0 else'FAIL'),flush=True)
        return dict(name=name,command=shown,exit_code=r.returncode,seconds=round(time.monotonic()-start,3),log=name+'.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:rows=list(pool.map(run,jobs))
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()!=head:raise SystemExit('Source parent changed during verification')
    files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()for p in sorted((ROOT/'tools/squadrons/pacific').rglob('*'))if p.is_file()and p.suffix in('.py','.json')}
    payload=hashlib.sha256()
    for path in sorted((ROOT/'mod/2985041246').rglob('*'),key=lambda p:p.as_posix()):
        if path.is_file():payload.update(path.relative_to(ROOT).as_posix().encode()+b'\0'+path.read_bytes())
    report=dict(schema=1,checkout_parent=head,source_normalized_sha256=files,payload_sha256=payload.hexdigest(),passed=sum(r['exit_code']==0 for r in rows),failed=sum(r['exit_code']!=0 for r in rows),checks=rows,native_acceptance=False)
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n');raise SystemExit(bool(report['failed']))
