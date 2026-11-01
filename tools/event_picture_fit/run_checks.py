"""Pin clean source before/after bounded offline checks; never launch HOI4."""
import argparse,json,subprocess,sys,time,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify

def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path);p.add_argument('--output',type=Path,default=ROOT/'docs/evidence/event-picture-fit/source-checks');a=p.parse_args()
    before=capture(ROOT);a.output.mkdir(parents=True,exist_ok=True);py=[sys.executable,'-B']
    commands=[
      ('event-pictures',py+['tools/Test-EventPictures.py']),
      ('anea-art',py+['tools/Test-AneaArt.py']),
      ('reconstruction-art',py+['tools/Test-ReconstructionAssets.py']),
      ('superpower-art',py+['tools/Test-SuperpowerAssets.py']),
      ('fato-source',py+['tools/fato_south_belka/test_source.py']),
      ('anea-system-generated',py+['tools/anea/build_system.py','--check']),
      ('continental-war',py+['tools/Test-ContinentalWar.py']),
      ('offline-review',py+['tools/event_picture_fit/review.py','--check']),
      ('land-preservation',py+['tools/land_program/test_land.py']),
      ('air-preservation',py+['tools/air_program/test_air.py']),
      ('naval-preservation',py+['tools/naval_program/test_naval.py']),
      ('presentation-source',py+['tools/Test-PresentationSources.py']),
      ('strict-authored-assets',py+['tools/audit_visual_dependencies.py','--strict-all']),
    ]
    core=['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot',str(ROOT/'mod/2985041246')]
    if a.engine:core+=['-ReferenceGameRoot',str(a.engine)]
    commands.append(('static-reference',core));results=[]
    for name,command in commands:
        started=time.monotonic();result=subprocess.run(command,cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        log=name+'.txt';(a.output/log).write_bytes(result.stdout+result.stderr)
        row=dict(check=name,command=command,exit_code=result.returncode,seconds=round(time.monotonic()-started,3),log=log,
                 coverage='Source/offline only; no native execution')
        results.append(row);print(name+(': PASS' if result.returncode==0 else ': FAIL'),flush=True)
        if result.returncode:
            verify(before,ROOT);(a.output/'results.json').write_bytes((json.dumps(dict(source=before,checks=results),indent=2)+'\n').encode())
            raise SystemExit(result.returncode)
    if a.engine:
        name='broader-eventwindow-ownership';output=a.output/'effective-eventwindow.json'
        command=py+['tools/overhaul/audit_consumers.py',str(a.engine),'--gate-screen','eventwindow.gui','--gate-decisions','--summary-only','--output',str(output)]
        result=subprocess.run(command,cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});(a.output/(name+'.txt')).write_bytes(result.stdout+result.stderr)
        report=json.loads(output.read_text());failures=report['gate_covered_screens']['eventwindow.gui']['failures']
        expected=['font:hoi4_typewriter16:engine_fallback','font:hoi4_typewriter22:engine_fallback']+[
          'sprite:'+s+':engine_fallback' for s in ('GFX_event_button_minimize','GFX_event_leader_frame','GFX_event_operative_background',
          'GFX_event_report_bottom_win_end','GFX_event_report_tileable_bottom_section','GFX_event_report_tileable_midsection',
          'GFX_event_report_top_win','GFX_intelligence_agency_logo_prc','GFX_leader_unknown','GFX_news_event_001',
          'GFX_paper_clip_event','GFX_report_event_001','GFX_tiled_window_transparent')]
        matched=result.returncode==1 and set(failures)==set(expected) and not report['gate_covered_screens']['countrydecisionview.gui']['failures']
        results.append(dict(check=name,command=command,exit_code=result.returncode,expected_legacy_ownership_failure=True,
            exact_backlog_matches=matched,eventwindow_failures=failures,decision_failures=[],log=name+'.txt',
            coverage='Unchanged wider screen ownership backlog; not accepted as whole-screen/native closure'))
        print('broader-eventwindow-ownership: FAIL (15 preserved fallbacks; separately recorded)' if matched else 'broader-eventwindow-ownership: UNEXPECTED RESULT',flush=True)
        if not matched:raise SystemExit('Broader ownership classification changed; inspect instead of updating the capture')
    after=verify(before,ROOT)
    (a.output/'results.json').write_bytes((json.dumps(dict(schema=1,source_before=before,source_after=after,checks=results,
        evidence='Required bounded source checks pass; wider15-fallback ownership failure remains explicit; native paused'),indent=2)+'\n').encode())
    print('Exact source identity verified before/after; native rendering untested.',flush=True)

if __name__=='__main__':main()
