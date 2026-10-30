"""Run the release's static/offline checks and retain exact commands/results."""
import argparse,concurrent.futures,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/evidence/usea-expansion'

def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path);p.add_argument('--only',help='Comma-separated affected checks; retain previous unaffected results');a=p.parse_args()
    py=[sys.executable,'-B'];checks={
      'expansion':py+['tools/Test-UseaExpansion.py'],
      'interface-repairs':py+['tools/Test-InterfaceRepairs.py'],
      'continental-war':py+['tools/Test-ContinentalWar.py'],
      'supporting-countries':py+['tools/Test-UseaActors.py'],
      'aftermath':py+['tools/Test-PeaceWeInherit.py'],
      'factions':py+['tools/Test-UlyssesFactions.py'],
      'projects':py+['tools/Test-StrangerealProjects.py'],
      'campaign':py+['tools/validate_campaign.py'],
      'briefing':py+['tools/frontend_briefing/validate.py'],
      'typography':py+['tools/frontend_typography/validate.py'],
      'economy':py+['-m','unittest','discover','-s','tools','-p','test_economy.py'],
      'assets':py+['tools/audit_visual_dependencies.py','--strict-all'],
      'generated-war':py+['tools/build_continental_war.py','--check'],
      'core':['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File','tools/Test-UlyssesStatic.ps1','-ModRoot',str(ROOT/'mod/2985041246')],
    }
    if a.engine:
        checks['core']+=['-ReferenceGameRoot',str(a.engine)]
        checks['screen-dependencies']=py+['tools/usea_expansion/audit_screens.py',str(a.engine),'--output',str(OUT/'engine-dependencies.json')]
    OUT.mkdir(parents=True,exist_ok=True)
    retained=[]
    if a.only:
        wanted=set(a.only.split(','))
        if wanted-set(checks):raise SystemExit('Unknown checks: '+str(wanted-set(checks)))
        checks={k:v for k,v in checks.items() if k in wanted}
        previous=OUT/'static-results.json'
        if previous.exists():retained=[r for r in json.loads(previous.read_text()) if r['check'] not in wanted]
    def run(pair):
        name,command=pair;start=time.monotonic()
        result=subprocess.run(command,cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        raw=result.stdout+result.stderr;(OUT/('static-'+name+'.txt')).write_bytes(raw)
        row=dict(check=name,command=command,exit_code=result.returncode,seconds=round(time.monotonic()-start,2),log='static-'+name+'.txt',coverage='static/offline; not native acceptance')
        print(name+': '+('PASS' if result.returncode==0 else 'FAIL'),flush=True);return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,checks.items()))
    results=retained+results
    (OUT/'static-results.json').write_text(json.dumps(results,indent=2)+'\n')
    raise SystemExit(any(r['exit_code'] for r in results))

if __name__=='__main__':main()
