"""Retain bounded, sequential source/offline evidence; never launch the game."""
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/evidence/institutions'


def main():
    checks={
        'institution-contracts':['tools/Test-Institutions.py'],
        'authored-assets':['tools/audit_visual_dependencies.py','--strict-all'],
        'existing-campaign':['tools/validate_campaign.py'],
        'usean-rebellion':['tools/Test-UseanRebellion.py'],
    }
    OUT.mkdir(parents=True,exist_ok=True);results=[]
    for name,args in checks.items():
        proc=subprocess.run([sys.executable,'-B']+args,cwd=ROOT,capture_output=True)
        log='static-'+name+'.txt';(OUT/log).write_bytes(proc.stdout+proc.stderr)
        results.append(dict(check=name,command=['python','-B']+args,exit_code=proc.returncode,log=log,coverage='source/static/offline; no native engine execution'))
        print(name+': '+('PASS' if proc.returncode==0 else 'FAIL'),flush=True)
    import PIL
    report=dict(time_utc=datetime.now(timezone.utc).isoformat(),base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        python=platform.python_version(),pillow=PIL.__version__,native='paused; not performed',
        fiscal_dependency='actual commitment owner loaded when present; otherwise recorded API body with quote-boundary stub',checks=results)
    sources=[]
    for path in sorted((ROOT/'tools/institutions').glob('*')):
        if path.is_file():sources.append(dict(file=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    report['authoring_sources']=sources
    (OUT/'static-results.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(any(row['exit_code'] for row in results))


if __name__=='__main__':main()
