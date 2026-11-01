"""Pin clean source before/after bounded offline checks; never launch HOI4."""
import argparse,json,subprocess,sys,time,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify
from event_picture_fit.evidence import begin,run_json_audit,screen_failures,finish,write_json

def complete(output,before,checks,error=None,metadata=None):
    after=None
    if before is not None:
        try:after=verify(before,ROOT)
        except Exception as problem:error=(str(error)+'; 'if error else'')+'Source verification failed: '+str(problem)
    report=finish(output,before,after,checks,error)
    for key in ('event_screen_contract','screen_contract_only'):
        if metadata and key in metadata:report[key]=metadata[key]
    write_json(Path(output)/'results.json',report)
    if not report['passed']:raise SystemExit(error or 'Current source checks failed; inspect '+str(output))
    return report

SCREEN_CONTRACTS=('event-style','original-fit')
ORIGINAL_FAILURES=['font:hoi4_typewriter16:engine_fallback','font:hoi4_typewriter22:engine_fallback']+[
    'sprite:'+s+':engine_fallback' for s in ('GFX_event_button_minimize','GFX_event_leader_frame','GFX_event_operative_background',
    'GFX_event_report_bottom_win_end','GFX_event_report_tileable_bottom_section','GFX_event_report_tileable_midsection',
    'GFX_event_report_top_win','GFX_intelligence_agency_logo_prc','GFX_leader_unknown','GFX_news_event_001',
    'GFX_paper_clip_event','GFX_report_event_001','GFX_tiled_window_transparent')]

def require_screen_source(contract):
    """Explicit reviewed owner, never an automatic missing-owner exemption."""
    if contract not in SCREEN_CONTRACTS:raise ValueError('Unknown event screen contract')
    gui=ROOT/'mod/2985041246/interface/eventwindow.gui'
    if contract=='event-style':
        from event_style.migration import assert_preserved
        from event_style.validate import validate_art
        assert_preserved(gui.read_text(encoding='utf-8-sig'));validate_art()
    else:
        from event_picture_fit.proof import digest
        original=json.loads((ROOT/'tools/event_picture_fit/contract.json').read_text())['protected_gui_sha256']
        if digest(gui)!=original:raise ValueError('original-fit requires its original unstyled GUI; use the explicit event-style contract on the composed tree')

def screen_matches(report,returncode,contract):
    if contract not in SCREEN_CONTRACTS:raise ValueError('Unknown event screen contract')
    event=screen_failures(report,'eventwindow.gui');decisions=screen_failures(report,'countrydecisionview.gui')
    if event is None or decisions is None:return False
    if contract=='original-fit':return returncode==1 and set(event)==set(ORIGINAL_FAILURES) and len(event)==15 and not decisions
    provider=report.get('dlc_archive_coverage',{})
    if not isinstance(provider,dict):return False
    return (returncode==0 and not event and not decisions and provider.get('status')=='explicit_profile_inspected'
            and provider.get('selected_descriptors')==[])

def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path)
    p.add_argument('--event-screen-contract',choices=SCREEN_CONTRACTS,default='event-style',help='Explicit reviewed screen owner; composed source defaults to event-style, original-fit requires its original GUI')
    p.add_argument('--screen-contract-only',action='store_true',help='Rerun only this dependency contract with independent source receipts')
    p.add_argument('--output',type=Path,default=ROOT/'docs/evidence/event-picture-fit/composed-source-checks');a=p.parse_args()
    if a.screen_contract_only and not a.engine:p.error('--screen-contract-only requires --engine')
    metadata=dict(event_screen_contract=a.event_screen_contract,screen_contract_only=a.screen_contract_only)
    begin(a.output)
    try:
        require_screen_source(a.event_screen_contract);before=capture(ROOT)
    except Exception as problem:complete(a.output,None,[],str(problem),metadata)
    py=[sys.executable,'-B']
    environment={**os.environ,'PYTHONDONTWRITEBYTECODE':'1',
        'PATH':str(Path(sys.executable).parent)+os.pathsep+os.environ.get('PATH','')}
    commands=[
      ('event-pictures',py+['tools/Test-EventPictures.py']),
      ('event-evidence',py+['tools/Test-EventEvidence.py']),
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
    commands.append(('static-reference',core))
    if a.screen_contract_only:commands=[]
    results=[]
    for name,command in commands:
        started=time.monotonic();result=subprocess.run(command,cwd=ROOT,capture_output=True,env=environment)
        log=name+'.txt';(a.output/log).write_bytes(result.stdout+result.stderr)
        row=dict(check=name,command=command,exit_code=result.returncode,seconds=round(time.monotonic()-started,3),log=log,
                 coverage='Source/offline only; no native execution')
        results.append(row);print(name+(': PASS' if result.returncode==0 else ': FAIL'),flush=True)
        if result.returncode:
            complete(a.output,before,results,'Required check failed: '+name,metadata)
    if a.engine:
        name='eventwindow-ownership-'+a.event_screen_contract;output=a.output/'effective-eventwindow.json'
        command=py+['tools/overhaul/audit_consumers.py',str(a.engine),'--gate-screen','eventwindow.gui','--gate-decisions','--summary-only','--output',str(output)]
        if a.event_screen_contract=='event-style':command+=['--profile','docs/evidence/effective-dependencies/profiles/base-only.json']
        result,report,report_error=run_json_audit(command,output,cwd=ROOT,capture_output=True,env=environment)
        (a.output/(name+'.txt')).write_bytes(result.stdout+result.stderr)
        failures=screen_failures(report,'eventwindow.gui');decisions=screen_failures(report,'countrydecisionview.gui')
        matched=report_error is None and screen_matches(report,result.returncode,a.event_screen_contract)
        results.append(dict(check=name,command=command,exit_code=result.returncode,screen_contract=a.event_screen_contract,
            expected_legacy_ownership_failure=a.event_screen_contract=='original-fit',exact_contract_matches=matched,accepted_contract=matched,
            eventwindow_failures=failures,decision_failures=decisions,report_error=report_error,log=name+'.txt',
            coverage='Only explicit eventwindow/decision ownership; wider pools/global/native acceptance remain open'))
        print(name+(': PASS (reviewed zero screen failures)' if matched and a.event_screen_contract=='event-style' else ': historical15-failure contract matched' if matched else ': UNEXPECTED RESULT'),flush=True)
        if not matched:complete(a.output,before,results,report_error or 'Explicit screen contract changed; inspect instead of updating the capture',metadata)
    complete(a.output,before,results,metadata=metadata)
    print('Exact source identity verified before/after; native rendering untested.',flush=True)

if __name__=='__main__':main()
