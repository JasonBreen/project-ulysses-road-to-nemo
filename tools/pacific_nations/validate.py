"""Capture component-scoped actual-source/offline gates without starting HOI4."""
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
sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--tag',choices=('OSE','YUK'),required=True);p.add_argument('--reference',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--affected',action='store_true');p.add_argument('--composed',action='store_true');p.add_argument('--only',action='append');p.add_argument('--pin-source',action='store_true');a=p.parse_args()
    out=a.output;out.mkdir(parents=True,exist_ok=True);py=[sys.executable,'-B'];engine=str(a.reference);baseline=str(a.baseline)
    jobs=[('national-runtime',py+['tools/pacific_nations/test_runtime.py']),('national-source-art',py+['tools/pacific_nations/test_source.py']),
      ('snp-runtime',py+['tools/Test-SuperpowerProgrammes.py']),('snp-source-art',py+['tools/Test-SuperpowerAssets.py']),
      ('focus-layout',py+['tools/Test-FocusScreenRepairs.py']),('decisions',py+['tools/Test-DecisionUI.py']),
      ('usean-actors',py+['tools/Test-UseaActors.py']),('projects',py+['tools/Test-StrangerealProjects.py']),
      ('shared-real-owners',py+['tools/Test-SharedSystems.py']),('macro',py+['tools/Test-EconomyV2.py']),
      ('release-finance',py+['tools/release_foundations/test_finance.py']),('release-lifecycle',py+['tools/release_foundations/test_lifecycle.py']),
      ('release-generated',py+['tools/release_foundations/author.py','--check']),('upkeep',py+['tools/Test-ForceUpkeep.py','--engine',engine]),
      ('land',py+['tools/land_program/test_land.py','--engine',engine]),('startup',py+['tools/Test-NativeCompatibilityContracts.py']),
      ('campaign',py+['tools/validate_campaign.py']),('briefing',py+['tools/frontend_briefing/validate.py']),('typography',py+['tools/frontend_typography/validate.py']),
      ('presentation',py+['tools/check_presentation_sources.py']),('assets-strict',py+['tools/audit_visual_dependencies.py','--strict-all']),
      ('static-reference',['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246','-ReferenceGameRoot',engine,'-BaselineRoot',baseline])]
    if a.affected:jobs=[row for row in jobs if row[0]in{'national-runtime','national-source-art','focus-layout','decisions','presentation','assets-strict','static-reference','campaign'}]
    if a.composed:jobs += [
      ('air',py+['tools/air_program/test_air.py']),('naval',py+['tools/naval_program/test_naval.py','--engine',engine]),
      ('fonts',py+['tools/research_fonts/test_fonts.py']),('asset-filters',py+['tools/Test-AssetGitFilters.py']),
      ('source-snapshot',py+['tools/Test-SourceSnapshot.py']),('registry',py+['tools/world_foundation/registry.py','--check']),
      ('generated-macro',py+['tools/economy_v2/build.py','--check']),('generated-national',py+['tools/pacific_nations/build.py','--check']),
      ('release-inventory',py+['tools/world_starts/release_inventory.py','--check']),('roadmap',py+['tools/overhaul/check_release_plan.py']),
      ('fato-south-belka',py+['tools/fato_south_belka/test_campaign.py']),('reconstruction',py+['tools/Test-ReconstructionContinuations.py']),
      ('event-pictures',py+['tools/Test-EventPictures.py']),('event-style',py+['tools/Test-EventStyle.py'])]
    if a.only:
        requested=set(a.only);available={name for name,_ in jobs}
        if requested-available:raise SystemExit('Unknown check names: '+str(requested-available))
        jobs=[row for row in jobs if row[0]in requested]
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    source=capture(ROOT)if a.pin_source else None
    def run(row):
        name,cmd=row;start=time.monotonic();result=subprocess.run(cmd,cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        text=(result.stdout+result.stderr).decode('utf-8','replace');shown=['python'if c==sys.executable else c for c in cmd]
        for path,label in((ROOT,'<repository>'),(a.reference,'<installed-reference>'),(a.baseline,'<immutable-baseline-payload>')):
            for spelling in(str(path.resolve()),path.resolve().as_posix()):text=text.replace(spelling,label);shown=[c.replace(spelling,label)for c in shown]
        (out/(name+'.txt')).write_text(text.replace('\r\n','\n'),encoding='utf-8',newline='\n');print(name+': '+('PASS'if result.returncode==0 else'FAIL'),flush=True)
        return dict(name=name,command=shown,exit_code=result.returncode,seconds=round(time.monotonic()-start,3),log=name+'.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:rows=list(pool.map(run,jobs))
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()!=head:raise SystemExit('Source parent changed during verification')
    files=sorted((ROOT/'tools/pacific_nations').glob('*.py'))+[ROOT/'tools/superpowers/build.py']
    sources={path.relative_to(ROOT).as_posix():hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()for path in files}
    payload=hashlib.sha256()
    for path in sorted((ROOT/'mod/2985041246').rglob('*'),key=lambda p:p.as_posix()):
        if path.is_file():payload.update(path.relative_to(ROOT).as_posix().encode()+b'\0'+path.read_bytes())
    after=verify(source,ROOT)if source else None
    report=dict(schema=1,country=a.tag,checkout_parent=head,source_inputs=source,source_inputs_after=after,source_normalized_sha256=sources,payload_sha256=payload.hexdigest(),
        source_state='Exact clean committed source and raw tracked inputs verified before/after checks'if source else'Working-tree candidate; only listed source hashes recorded',
        payload_hash_rule='Sorted repository-relative POSIX path,NUL,raw bytes for every delivered mod file.',
        passed=sum(r['exit_code']==0 for r in rows),failed=sum(r['exit_code']!=0 for r in rows),checks=rows,native_acceptance=False)
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n');raise SystemExit(bool(report['failed']))
