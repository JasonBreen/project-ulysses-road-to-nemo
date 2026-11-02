"""Capture reproducible source/offline gates; never launch the game or desktop."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
COMMANDS=[
 ['python','-B','tools/Test-ReconstructionContinuations.py'],
 ['python','-B','tools/Test-ReconstructionAssets.py'],
 ['python','-B','tools/Test-UseaExpansion.py'],
 ['python','-B','tools/Test-UseaActors.py'],
 ['python','-B','tools/Test-PeaceWeInherit.py'],
 ['python','-B','tools/Test-ContinentalWar.py'],
 ['python','-B','tools/Test-UseanRebellion.py'],
 ['python','-B','tools/Test-SharedSystems.py'],
 ['python','-B','tools/Test-EconomyV2.py'],
 ['python','-B','tools/Test-EconomyLedger.py'],
 ['python','-B','tools/Test-Institutions.py'],
 ['python','-B','tools/usean_partners/build.py','--check','--require-dependencies'],
 ['python','-B','tools/usean_partners/test_content.py','--require-dependencies'],
 ['python','-B','tools/usean_partners/test_integration.py'],
 ['python','-B','tools/squadrons/build.py','--check'],
 ['python','-B','tools/Test-SquadronStories.py'],
 ['python','-B','tools/Test-SquadronArt.py'],
 ['python','-B','tools/Test-FocusScreenRepairs.py'],
 ['python','-B','tools/Test-DecisionUI.py'],
 ['python','-B','tools/Test-EffectiveDependencies.py'],
 ['python','-B','tools/check_presentation_sources.py'],
 ['python','-B','tools/Test-InterfaceRepairs.py'],
 ['python','-B','tools/Test-OverhaulRepairs.py'],
 ['python','-B','tools/build_continental_war.py','--check'],
 ['python','-B','tools/Test-UlyssesFactions.py'],
 ['python','-B','tools/validate_campaign.py'],
 ['python','-B','tools/world_foundation/test_foundation.py'],
 ['python','-B','tools/world_foundation/registry.py','--check'],
 ['python','-B','tools/overhaul/check_release_plan.py'],
 ['python','-B','tools/audit_visual_dependencies.py','--strict-all'],
 ['python','-B','tools/frontend_briefing/validate.py'],
 ['python','-B','tools/frontend_typography/validate.py'],
 ['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246'],
]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path)
 mode=p.add_mutually_exclusive_group();mode.add_argument('--only-new',action='store_true');mode.add_argument('--integration-only',action='store_true');a=p.parse_args()
 results=[]
 integration={'tools/Test-ReconstructionAssets.py','tools/Test-UseaActors.py','tools/Test-EffectiveDependencies.py','tools/check_presentation_sources.py',
  'tools/Test-FocusScreenRepairs.py','tools/Test-DecisionUI.py','tools/Test-InterfaceRepairs.py','tools/Test-OverhaulRepairs.py',
  'tools/world_foundation/registry.py','tools/overhaul/check_release_plan.py','tools/audit_visual_dependencies.py'}
 commands=COMMANDS[:2]if a.only_new else [c for c in COMMANDS if c[2]in integration]if a.integration_only else COMMANDS
 for command in commands:
  actual=[sys.executable,*command[1:]]if command[0]=='python'else command
  start=time.monotonic();r=subprocess.run(actual,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
  output=(r.stdout+r.stderr).replace(str(ROOT),'repo://').replace(str(ROOT).replace('\\','/'),'repo://')
  results.append(dict(command=command,exit_code=r.returncode,seconds=round(time.monotonic()-start,3),output=output))
  print(('PASS'if r.returncode==0 else'FAIL')+': '+' '.join(command),flush=True)
  if r.returncode:print(output[-5000:],flush=True)
 report=dict(schema=1,captured_utc=datetime.now(timezone.utc).isoformat(),evidence='Source/offline execution only; no native HOI4, input, save, AI or balance acceptance',
   source_hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted((ROOT/'tools/reconstruction').glob('*.py'))},
   passed=sum(r['exit_code']==0 for r in results),failed=sum(r['exit_code']!=0 for r in results),results=results)
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(f"Source gates: {report['passed']} passed, {report['failed']} failed",flush=True)
 raise SystemExit(bool(report['failed']))

if __name__=='__main__':main()
