"""Capture SP96 source/offline evidence. Never launch HOI4 or a desktop app."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from reconstruction.validate import COMMANDS as PREVIOUS_COMMANDS
from source_snapshot import capture,verify

NEW=[['python','-B','tools/Test-SuperpowerProgrammes.py'],['python','-B','tools/Test-SuperpowerAssets.py'],
     ['python','-B','tools/Test-StartupChronology.py']]
EXTRA=[['python','-B',path]for path in(
 'tools/Test-PresentationSources.py','tools/Test-RetiredWorldNews.py','tools/Test-StrangerealProjects.py','tools/Test-ForceUpkeep.py','tools/Test-UstioContinuity.py',
 'tools/Test-NativeCompatibilityContracts.py','tools/test_economy.py',
 'tools/Test-CampaignReviewRegressions.py','tools/Test-CampaignContractMutations.py',
 'tools/anea/test_foundation.py','tools/Test-AneaCampaign.py','tools/Test-AneaSystems.py',
 'tools/Test-AneaArt.py','tools/Test-AneaPresentation.py','tools/Test-AneaIntegration.py')]
WORLD=[['python','-B',*args]for args in(
 ['tools/world_starts/test_world_starts.py'],
 ['tools/world_starts/test_legacy_logistics.py','--require-integrated-owner'],
 ['tools/world_legacy/test_legacy.py'],
 ['tools/replacements/test_replacements.py'],
 ['tools/world_starts/coverage.py','--check','--require-integrated-owner'],
 ['tools/world_starts/compile.py','--check'],
 ['tools/world_legacy/build.py','--check'],
 ['tools/world_legacy/audit.py','--check'])]


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path)
 mode=p.add_mutually_exclusive_group();mode.add_argument('--only-new',action='store_true');mode.add_argument('--integration-only',action='store_true');mode.add_argument('--review-parent',action='store_true');p.add_argument('--pin-source',action='store_true');a=p.parse_args();results=[]
 integration={'tools/Test-ReconstructionAssets.py','tools/Test-FocusScreenRepairs.py','tools/Test-DecisionUI.py',
  'tools/Test-EffectiveDependencies.py','tools/check_presentation_sources.py','tools/Test-PresentationSources.py',
  'tools/Test-InterfaceRepairs.py','tools/Test-OverhaulRepairs.py','tools/validate_campaign.py',
  'tools/world_foundation/registry.py','tools/overhaul/check_release_plan.py','tools/audit_visual_dependencies.py',
  'tools/Test-UlyssesStatic.ps1','tools/anea/test_foundation.py','tools/Test-AneaCampaign.py','tools/Test-AneaSystems.py',
  'tools/Test-AneaArt.py','tools/Test-AneaPresentation.py','tools/Test-AneaIntegration.py',
  'tools/Test-UstioContinuity.py','tools/Test-RetiredWorldNews.py','tools/Test-Institutions.py','tools/Test-StrangerealProjects.py'}
 commands=NEW if a.only_new else NEW[1:]+[c for c in PREVIOUS_COMMANDS+EXTRA if c[2]in integration or len(c)>3 and c[3]in integration]if a.integration_only else NEW+PREVIOUS_COMMANDS+EXTRA+WORLD
 if a.review_parent:commands=NEW[:2]+[['python','-B',*parts]for parts in(
  ['tools/release_foundations/test_finance.py'],['tools/release_foundations/test_physical.py'],
  ['tools/economy_v2/build.py','--check'],['tools/world_foundation/registry.py','--check'],
  ['tools/audit_visual_dependencies.py','--strict-all'],['tools/economy_v2/render_review.py','--check'])]
 before=capture(ROOT)if a.pin_source else None
 for command in commands:
  actual=[sys.executable,*command[1:]]if command[0]=='python'else command
  start=time.monotonic();r=subprocess.run(actual,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
  output=(r.stdout+r.stderr).replace(str(ROOT),'repo://').replace(str(ROOT).replace('\\','/'),'repo://')
  results.append(dict(command=command,exit_code=r.returncode,seconds=round(time.monotonic()-start,3),output=output))
  print(('PASS'if r.returncode==0 else'FAIL')+': '+' '.join(command),flush=True)
  if r.returncode:print(output[-6000:],flush=True)
 paths=sorted((ROOT/'tools/superpowers').glob('*.py'))+[ROOT/'tools/Test-SuperpowerProgrammes.py',ROOT/'tools/Test-SuperpowerAssets.py',
       ROOT/'tools/Test-StartupChronology.py',ROOT/'tools/compatibility/variant_order.py',ROOT/'tools/compatibility/research_contract.json']
 report=dict(schema=1,captured_utc=datetime.now(timezone.utc).isoformat(),evidence='Source/offline checks only; no native game, saves, AI, balance, viewport/input or engine numeric acceptance',
  source_hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},
  passed=sum(r['exit_code']==0 for r in results),failed=sum(r['exit_code']!=0 for r in results),results=results)
 payload=hashlib.sha256()
 for path in sorted((ROOT/'mod/2985041246').rglob('*'),key=lambda p:p.as_posix()):
  if path.is_file():payload.update(path.relative_to(ROOT).as_posix().encode()+b'\0'+path.read_bytes())
 report.update(source_inputs=before,source_inputs_after=verify(before,ROOT)if before else None,payload_sha256=payload.hexdigest(),native_acceptance=False)
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(f"SP96 source gates: {report['passed']} passed, {report['failed']} failed",flush=True)
 raise SystemExit(bool(report['failed']))

if __name__=='__main__':main()
