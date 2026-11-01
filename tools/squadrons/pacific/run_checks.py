"""Exact-source personal-story checks; game and desktop execution stay paused."""
import argparse
import concurrent.futures
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify
from event_picture_fit.evidence import begin,finish,write_json


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--engine',required=True,type=Path);p.add_argument('--baseline',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path);p.add_argument('--only',action='append')
    a=p.parse_args();out=a.output.resolve();py=[sys.executable,'-B'];engine=str(a.engine)
    if not any(out.is_relative_to(ROOT/folder)for folder in('docs/evidence','runtime-output')):
        p.error('Evidence must stay inside this worktree docs/evidence or ignored runtime-output')
    jobs=[
      ('new-runtime',py+['tools/squadrons/pacific/test_runtime.py']),
      ('new-source-art-preservation',py+['tools/squadrons/pacific/test_source.py']),
      ('original-six-runtime',py+['tools/Test-SquadronStories.py']),
      ('original-art-partition',py+['tools/Test-SquadronArt.py']),
      ('original-pacific-masters',py+['tools/squadrons/pacific_art/test_art.py']),
      ('committed-art-bytes',py+['tools/squadrons/pacific_art/audit.py','--git-blobs']),
      ('national-runtime',py+['tools/pacific_nations/test_runtime.py']),
      ('world-foundations',py+['tools/world_foundation/test_foundation.py','--reference',engine]),
      ('release-inventory',py+['tools/world_starts/release_inventory.py','--check']),
      ('shared-real-owners',py+['tools/Test-SharedSystems.py']),
      ('macro',py+['tools/Test-EconomyV2.py']),('force-upkeep',py+['tools/Test-ForceUpkeep.py']),
      ('decisions',py+['tools/Test-DecisionUI.py']),('campaign',py+['tools/validate_campaign.py']),
      ('presentation',py+['tools/check_presentation_sources.py']),
      ('assets-strict',py+['tools/audit_visual_dependencies.py','--strict-all']),
      ('event-pictures',py+['tools/Test-EventPictures.py']),('event-style',py+['tools/Test-EventStyle.py']),
      ('event-evidence',py+['tools/Test-EventEvidence.py']),
      ('interface-repairs',py+['tools/Test-InterfaceRepairs.py']),
      ('dependency-negatives',py+['tools/Test-EffectiveDependencies.py']),
      ('research-fonts',py+['tools/research_fonts/test_fonts.py']),
      ('dependency-consumers',py+['tools/squadrons/pacific/capture_dependencies.py','--engine',engine,'--output',str(out/'dependencies.json')]),
      ('static-reference',['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246','-ReferenceGameRoot',engine,'-BaselineRoot',str(a.baseline)])]
    if a.only:
        unknown=set(a.only)-{name for name,_ in jobs}
        if unknown:p.error('Unknown checks: '+','.join(sorted(unknown)))
        jobs=[row for row in jobs if row[0]in a.only]
    begin(out);before=after=None;rows=[];error=None;payload=None
    environment={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PATH':str(Path(sys.executable).parent)+os.pathsep+os.environ.get('PATH','')}

    def run(row):
        name,command=row;started=time.monotonic()
        try:r=subprocess.run(command,cwd=ROOT,capture_output=True,env=environment)
        except OSError as problem:r=subprocess.CompletedProcess(command,127,b'',str(problem).encode())
        text=(r.stdout+r.stderr).decode('utf-8','replace');shown=['python'if c==sys.executable else c for c in command]
        for path,label in((ROOT,'<repository>'),(a.engine,'<installed-reference>'),(a.baseline,'<immutable-baseline-payload>')):
            for spelling in(str(path.resolve()),path.resolve().as_posix()):
                text=text.replace(spelling,label);shown=[c.replace(spelling,label)for c in shown]
        raw=text.replace('\r\n','\n').encode('utf-8');(out/(name+'.txt')).write_bytes(raw)
        print(name+': '+('PASS'if r.returncode==0 else'FAIL'),flush=True)
        return dict(name=name,command=shown,exit_code=r.returncode,seconds=round(time.monotonic()-started,3),log=name+'.txt',log_sha256=hashlib.sha256(raw).hexdigest())

    try:
        before=capture(ROOT)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
            for future in concurrent.futures.as_completed([pool.submit(run,row)for row in jobs]):rows.append(future.result())
        if len(rows)!=len(jobs):raise ValueError('Incomplete source check invocation')
        after=verify(before,ROOT)
        digest=hashlib.sha256()
        for path in sorted((ROOT/'mod/2985041246').rglob('*'),key=lambda path:path.as_posix()):
            if path.is_file():digest.update(path.relative_to(ROOT).as_posix().encode()+b'\0'+path.read_bytes())
        payload=digest.hexdigest();verify(before,ROOT)
    except Exception as problem:error=str(problem)
    report=finish(out,before,after,sorted(rows,key=lambda row:row['name']),error)
    report.update(payload_sha256=payload,payload_hash_rule='Sorted repository-relative POSIX path,NUL,raw delivered mod bytes.',
        passed_groups=sum(row['exit_code']==0 for row in rows),failed_groups=sum(row['exit_code']!=0 for row in rows),required_groups=len(jobs))
    write_json(out/'results.json',report)
    if not report['passed']:raise SystemExit('Current source checks failed: '+str(out))
    print(str(len(rows))+' exact-source groups pass; native/desktop testing remains paused')


if __name__=='__main__':main()
