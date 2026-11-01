"""Checked subprocess runner; failures cannot be masked by PowerShell steps."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify
def main():
    p=argparse.ArgumentParser();p.add_argument('--broad',action='store_true');p.add_argument('--only',action='append');p.add_argument('--reference',type=Path);p.add_argument('--output',type=Path,default=ROOT/'runtime-output/fato-south-belka/checks');p.add_argument('--pin-source',action='store_true');a=p.parse_args()
    commands=[('national-owners',['tools/fato_south_belka/test_campaign.py']),('national-source-art',['tools/fato_south_belka/test_source.py']),
        ('generated-content',['tools/fato_south_belka/build.py','--check']),('generated-art',['tools/fato_south_belka/build_art.py','--check']),
        ('inherited-primary-contract',['tools/fato_south_belka/source_contract.py']+(['--reference',str(a.reference)]if a.reference else [])),
        ('composed-registry',['tools/world_foundation/registry.py','--check']),('institution-generator',['tools/institutions/build.py','--check']),
        ('focus-pacing',['tools/fato_south_belka/pacing.py','--check'])]
    if a.broad:commands += [
        ('shared-owners',['tools/Test-SharedSystems.py']),('institutions',['tools/Test-Institutions.py']),
        ('macro-owner',['tools/Test-EconomyV2.py']),('ledger-owner',['tools/Test-EconomyLedger.py']),('force-upkeep',['tools/Test-ForceUpkeep.py']),('legacy-economy',['tools/test_economy.py']),
        ('release-finance',['tools/release_foundations/test_finance.py']),('release-leaders',['tools/release_foundations/test_leaders.py']),
        ('release-lifecycle',['tools/release_foundations/test_lifecycle.py']),('release-source',['tools/release_foundations/test_source.py']),
        ('world-foundations',['tools/world_foundation/test_foundation.py']+(['--reference',str(a.reference)]if a.reference else [])),('world-starts',['tools/world_starts/test_world_starts.py']+(['--reference',str(a.reference)]if a.reference else [])),
        ('world-legacy',['tools/world_legacy/test_legacy.py']),('replacement-owners',['tools/replacements/test_replacements.py']),
        ('aftermath',['tools/Test-PeaceWeInherit.py']),('factions',['tools/Test-UlyssesFactions.py']),
        ('continental-war',['tools/Test-ContinentalWar.py']),('supporting-countries',['tools/Test-UseaExpansion.py']),('special-projects',['tools/Test-StrangerealProjects.py']),
        ('campaign-contracts',['tools/Test-CampaignContractMutations.py']),('campaign-reviews',['tools/Test-CampaignReviewRegressions.py']),
        ('focus-repairs',['tools/Test-FocusScreenRepairs.py']),('decision-repairs',['tools/Test-DecisionUI.py']),
        ('row-review-generated',['tools/decision_row_art/render_review.py','--check']),
        ('overview-generated',['tools/overhaul/build_overview.py','--check']),
        ('briefing',['tools/frontend_briefing/validate.py']),('typography',['tools/frontend_typography/validate.py']),
        ('all-authored-assets',['tools/audit_visual_dependencies.py','--strict-all'])]
    if a.only:
        requested=set(a.only);available={name for name,_ in commands}
        if requested-available:raise SystemExit('Unknown check names: '+str(requested-available))
        commands=[row for row in commands if row[0]in requested]
    a.output.mkdir(parents=True,exist_ok=True);rows=[]
    source=capture(ROOT)if a.pin_source else None
    for name,args in commands:
        start=time.monotonic();result=subprocess.run([sys.executable,'-B',*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (a.output/(name+'.txt')).write_text(result.stdout+result.stderr,encoding='utf-8',newline='\n')
        rows.append(dict(name=name,command=[Path(sys.executable).name,'-B',*args],exit_code=result.returncode,seconds=round(time.monotonic()-start,2)))
        print(name+': '+('PASS'if result.returncode==0 else 'FAIL'),flush=True)
    source_files=[p for p in HERE.glob('*.py')]+[ROOT/'mod/2985041246/common/scripted_effects/ac_fato_south_belka.txt']
    if source:verify(source,ROOT)
    report=dict(evidence='Static/offline source execution, not native engine, serialization or AI acceptance',native='paused',source_head=source['head']if source else None,source_inputs=source,checks=rows,
        source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()for p in source_files})
    (a.output/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    if any(r['exit_code']for r in rows):raise SystemExit('One or more checks failed; inspect '+str(a.output))
    print(str(len(rows))+' source gates pass; native paused')
if __name__=='__main__':main()
