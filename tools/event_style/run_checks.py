"""Exact-source bounded event-style validation; never launches HOI4."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify
def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,default=ROOT/'docs/evidence/event-style/source-checks');p.add_argument('--only',action='append');a=p.parse_args()
    source=capture(ROOT);a.output.mkdir(parents=True,exist_ok=True);py=[sys.executable,'-B']
    commands=[
        ('event-style',py+['tools/Test-EventStyle.py']),
        ('original-interfaces',py+['tools/Test-InterfaceRepairs.py']),
        ('event-fit',py+['tools/Test-EventPictures.py']),
        ('fit-review',py+['tools/event_picture_fit/review.py','--check']),
        ('primary-contract',py+['tools/event_style/primary.py','--engine',str(a.engine),'--check']),
        ('effective-base-only',py+['tools/overhaul/audit_consumers.py',str(a.engine),'--profile','docs/evidence/effective-dependencies/profiles/base-only.json','--gate-screen','eventwindow.gui','--gate-decisions','--summary-only','--output',str(a.output/'effective-base-only.json')]),
        ('font-closure',py+['tools/research_fonts/test_fonts.py']),
        ('land-preservation',py+['tools/land_program/test_land.py']),
        ('air-preservation',py+['tools/air_program/test_air.py']),
        ('naval-preservation',py+['tools/naval_program/test_naval.py']),
        ('decision-ui',py+['tools/Test-DecisionUI.py']),
        ('effective-negative-fixtures',py+['tools/Test-EffectiveDependencies.py']),
        ('presentation-source',py+['tools/Test-PresentationSources.py']),
        ('strict-authored-assets',py+['tools/audit_visual_dependencies.py','--strict-all']),
        ('static-reference',['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot',str(ROOT/'mod/2985041246'),'-ReferenceGameRoot',str(a.engine)])]
    if a.only:
        selected=set(a.only);known={name for name,_ in commands}
        if selected-known:raise SystemExit('Unknown event-style checks: '+str(selected-known))
        commands=[row for row in commands if row[0]in selected]
    rows=[]
    for name,command in commands:
        started=time.monotonic();result=subprocess.run(command,cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        (a.output/(name+'.txt')).write_bytes(result.stdout+result.stderr)
        rows.append(dict(check=name,command=command,exit_code=result.returncode,seconds=round(time.monotonic()-started,3),log=name+'.txt'))
        print(name+(': PASS' if result.returncode==0 else ': FAIL'),flush=True)
        if result.returncode:
            verify(source,ROOT);(a.output/'results.json').write_bytes((json.dumps(dict(source_before=source,checks=rows),indent=2)+'\n').encode());raise SystemExit(result.returncode)
    after=verify(source,ROOT)
    (a.output/'results.json').write_bytes((json.dumps(dict(schema=1,source_before=source,source_after=after,checks=rows,
        evidence='All bounded source/offline checks; native rendering, reflow, DLC activation and input remain unaccepted'),indent=2)+'\n').encode())
    print('Exact source identity unchanged before/after; event screen ownership0; wider presentation/native remain open.')
if __name__=='__main__':main()
