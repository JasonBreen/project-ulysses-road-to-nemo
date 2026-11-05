"""Retain independent process exits and exact source receipts; never run HOI4."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]


def snapshot():
    inputs={}
    for folder in ('mod/2985041246','tools'):
        for path in sorted((ROOT/folder).rglob('*')):
            if path.is_file() and path.suffix.lower() in ('.py','.ps1','.json','.txt','.yml','.gfx','.gui','.lua','.csv'):
                inputs[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    return inputs


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--powershell',help='Current host executable; also run the complete static suite and reference comparison')
    p.add_argument('--reference-game-root',help='Optional read-only installed reference for the static suite')
    args=p.parse_args()
    if args.reference_game_root and not args.powershell:p.error('--reference-game-root requires --powershell')
    out=ROOT/'runtime-output/ac04-ac05';out.mkdir(parents=True,exist_ok=True)
    checks=[
        ('campaigns-generated',['tools/ac_campaigns/build.py','--check']),
        ('campaigns-art',['tools/ac_campaigns/build_art.py','--check']),
        ('campaigns-actual-scripts',['tools/ac_campaigns/test_campaigns.py']),
        ('continental-generated',['tools/build_continental_war.py','--check']),
        ('continental',['tools/Test-ContinentalWar.py']),
        ('aviation-owner-compatibility',['tools/air_program/test_air.py']),
        ('naval-owner-compatibility',['tools/naval_program/test_naval.py']),
        ('superpower-imports',['tools/Test-SuperpowerAssets.py']),
        ('pacific-national-runtime',['tools/pacific_nations/test_runtime.py']),
        ('pacific-national-source',['tools/pacific_nations/test_source.py']),
        ('startup-chronology',['tools/Test-StartupChronology.py']),
        ('original-squadron-art',['tools/Test-SquadronArt.py']),
        ('asset-dependencies',['tools/audit_visual_dependencies.py','--strict-all']),
        ('briefing',['tools/frontend_briefing/validate.py']),
        ('typography',['tools/frontend_typography/validate.py']),
        ('faction-contracts',['tools/Test-UlyssesFactions.py']),
        ('waves-generated',['tools/content_waves/build.py','--check']),
        ('waves-art',['tools/content_waves/build_art.py','--check']),
        ('waves',['tools/content_waves/test_waves.py']),
        ('partners-generated',['tools/usean_partners/build.py','--check','--require-dependencies']),
        ('partners-art',['tools/usean_partners/build_art.py','--check']),
        ('partners',['tools/usean_partners/test_content.py','--require-dependencies']),
        ('partner-owners',['tools/usean_partners/test_integration.py']),
        ('fato-generated',['tools/fato_south_belka/build.py','--check']),
        ('fato-owners',['tools/fato_south_belka/run_checks.py']),
        ('pacific-stories',['tools/squadrons/pacific/test_runtime.py']),
        ('pacific-source',['tools/squadrons/pacific/test_source.py']),
        ('original-stories',['tools/Test-SquadronStories.py']),
        ('release-accounting',['tools/overhaul/check_release_plan.py']),
        ('shared-records',['tools/content_waves/refresh_records.py','--check']),
        ('event-style',['tools/Test-EventStyle.py']),
        ('event-pictures',['tools/Test-EventPictures.py']),
        ('event-evidence',['tools/Test-EventEvidence.py']),
        ('picture-review',['tools/event_picture_fit/review.py','--check']),
        ('decision-ui',['tools/Test-DecisionUI.py']),
        ('campaign-paths',['tools/analysis/campaign_path_report.py','--campaign','all','--format','json']),
    ]
    commands=[(name,[sys.executable,'-B',*arguments]) for name,arguments in checks]
    if args.powershell:
        static=[args.powershell,'-NoProfile','-ExecutionPolicy','Bypass','-File','tools/Test-UlyssesStatic.ps1','-ModRoot',str(ROOT/'mod/2985041246')]
        if args.reference_game_root:static+=['-ReferenceGameRoot',args.reference_game_root]
        commands += [('full-static',static),('reference-regressions',[sys.executable,'-B','tools/ac_campaigns/reference_compare.py','--powershell',args.powershell])]
    environment=dict(os.environ)
    environment['PATH']=str(Path(sys.executable).parent)+os.pathsep+environment.get('PATH','')
    environment['PYTHONDONTWRITEBYTECODE']='1'
    before=snapshot();rows=[]
    for name,command in commands:
        started=time.monotonic();print('Checking '+name,flush=True)
        result=subprocess.run(command,cwd=ROOT,capture_output=True,env=environment)
        data=result.stdout+result.stderr;(out/(name+'.log')).write_bytes(data)
        shown=['python' if token==sys.executable else 'pwsh' if token==args.powershell else token.replace(str(ROOT),'<workspace>') for token in command]
        rows.append(dict(name=name,command=shown,exit_code=result.returncode,seconds=round(time.monotonic()-started,3),log_sha256=hashlib.sha256(data).hexdigest()))
        print(name+': '+('PASS' if result.returncode==0 else 'FAIL'),flush=True)
    after=snapshot();changed=sorted(key for key in set(before)|set(after) if before.get(key)!=after.get(key))
    report=dict(schema=1,base=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip(),
                source_before=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),
                source_after=hashlib.sha256(json.dumps(after,sort_keys=True).encode()).hexdigest(),input_files=len(before),changed_inputs=changed,
                checks=rows,native_acceptance=False)
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (out/'inputs.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
    if changed or any(r['exit_code'] for r in rows):raise SystemExit('Campaign checks need attention; see runtime-output/ac04-ac05/results.json')
    print('All '+str(len(rows))+' independent checks passed; exact source unchanged; native untested.')


if __name__=='__main__':main()
