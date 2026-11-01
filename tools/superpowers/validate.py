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

NEW=[['python','-B','tools/Test-SuperpowerProgrammes.py'],['python','-B','tools/Test-SuperpowerAssets.py'],
     ['python','-B','tools/Test-StartupChronology.py']]
EXTRA=[['python','-B',path]for path in(
 'tools/Test-StrangerealProjects.py','tools/Test-ForceUpkeep.py','tools/Test-UstioContinuity.py',
 'tools/Test-NativeCompatibilityContracts.py','tools/test_economy.py',
 'tools/Test-CampaignReviewRegressions.py','tools/Test-CampaignContractMutations.py',
 'tools/anea/test_foundation.py','tools/Test-AneaCampaign.py','tools/Test-AneaSystems.py',
 'tools/Test-AneaArt.py','tools/Test-AneaPresentation.py','tools/Test-AneaIntegration.py')]


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path);p.add_argument('--only-new',action='store_true');a=p.parse_args();results=[]
 for command in NEW if a.only_new else NEW+PREVIOUS_COMMANDS+EXTRA:
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
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(f"SP96 source gates: {report['passed']} passed, {report['failed']} failed",flush=True)
 raise SystemExit(bool(report['failed']))

if __name__=='__main__':main()
