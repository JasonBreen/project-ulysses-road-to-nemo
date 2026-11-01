"""Record bounded row-art source/offline acceptance; no engine is launched."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/evidence/decision-rows'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--engine',type=Path,required=True);parser.add_argument('--only');args=parser.parse_args()
    py=[sys.executable,'-B'];host=shutil.which('pwsh')
    if not host:raise SystemExit('Current pwsh required for full source validation')
    checks={
        'decision-ui':py+['tools/Test-DecisionUI.py'],
        'anea-art':py+['tools/Test-AneaArt.py'],
        'institutions':py+['tools/Test-Institutions.py'],
        'projects':py+['tools/Test-StrangerealProjects.py'],
        'anea-generated':py+['tools/anea/build_art.py','--check'],
        'institutions-generated':py+['tools/institutions/build_art.py','--check'],
        'compact-generated':py+['tools/decision_row_art/build.py','--check'],
        'offline-review':py+['tools/decision_row_art/render_review.py','--check'],
        'assets':py+['tools/audit_visual_dependencies.py','--strict-all'],
        'effective-decisions':py+['tools/overhaul/audit_consumers.py',str(args.engine),'--gate-decisions','--summary-only','--output',str(OUT/'effective-dependencies.json')],
        'static':[host,'-NoProfile','-ExecutionPolicy','Bypass','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246','-ReferenceGameRoot',str(args.engine)],
    }
    old=[]
    if args.only:
        names=set(args.only.split(','))
        if names-set(checks):raise SystemExit('Unknown checks: '+str(names-set(checks)))
        checks={k:v for k,v in checks.items() if k in names}
        if (OUT/'results.json').exists():old=[r for r in json.loads((OUT/'results.json').read_text())['checks'] if r['check'] not in names]
    OUT.mkdir(parents=True,exist_ok=True)
    def run(pair):
        name,command=pair;start=time.monotonic();result=subprocess.run(command,cwd=ROOT,capture_output=True)
        text=(result.stdout+result.stderr).decode('utf-8',errors='replace').replace('\r\n','\n')
        for path,label in ((ROOT,'<repository>'),(args.engine,'<installed-primary-reference>')):
            for spelling in (str(path),path.as_posix()):text=text.replace(spelling,label)
        (OUT/(name+'.txt')).write_bytes(text.encode())
        print(name+': '+('PASS' if result.returncode==0 else 'FAIL'),flush=True)
        return dict(check=name,exit_code=result.returncode,seconds=round(time.monotonic()-start,2),log=name+'.txt',coverage='Source/offline; native rendering, visibility, scaling and input remain untested')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,checks.items()))
    data=dict(base_commit='78e573625ec2ad9265b6aca348966866a857693e',native_acceptance=False,checks=sorted(old+rows,key=lambda r:r['check']))
    (OUT/'results.json').write_bytes((json.dumps(data,indent=2)+'\n').encode())
    raise SystemExit(any(row['exit_code'] for row in data['checks']))


if __name__=='__main__':main()
