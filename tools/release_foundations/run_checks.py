"""Run each release gate with its own inspected exit code; no shell masking."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path);parser.add_argument('--output',type=Path,default=ROOT/'runtime-output/release-foundations/checks.json');args=parser.parse_args()
    ref=['--reference',str(args.reference)] if args.reference else []
    commands=[
        ('release-finance',['tools/release_foundations/test_finance.py']),
        ('release-lifecycle',['tools/release_foundations/test_lifecycle.py']),
        ('release-physical',['tools/release_foundations/test_physical.py']),
        ('release-source',['tools/release_foundations/test_source.py']),
        ('release-office-lifecycle',['tools/release_foundations/test_leaders.py']),
        ('release-primary',['tools/release_foundations/source_contract.py','--check']+ref),
        ('release-intake',['tools/release_foundations/intake.py','--check']+ref),
        ('release-recipes',['tools/release_foundations/physical.py','--check']+ref),
        ('release-author',['tools/release_foundations/author.py','--check']),
        ('release-leaders',['tools/release_foundations/leaders.py','--check']),
        ('release-worksheet',['tools/release_foundations/release_worksheet.py','--check']+ref),
        ('release-art',['tools/release_foundations/build_art.py','--check']),
        ('canonical-economy-generator',['tools/economy_v2/build.py','--check']),
        ('registry-equality',['tools/world_foundation/registry.py','--check']),
        ('release-inventory',['tools/world_starts/release_inventory.py','--check']),
        ('release-scalar-inventory',['tools/world_starts/test_release_inventory.py']),
        ('active-owner-coverage',['tools/world_starts/coverage.py','--check','--require-integrated-owner']),
        ('authored-assets',['tools/audit_visual_dependencies.py','--strict-all']),
    ];results=[];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    for name,command in commands:
        start=time.monotonic();run=subprocess.run([sys.executable,'-B']+command,cwd=ROOT,env=env,text=True,encoding='utf-8',errors='replace',capture_output=True)
        log=args.output.parent/(name+'.txt');log.write_text(run.stdout+run.stderr,encoding='utf-8',newline='\n')
        results.append(dict(gate=name,command=command,exit_code=run.returncode,seconds=round(time.monotonic()-start,3),log=log.name))
        print(name+': '+('PASS' if run.returncode==0 else 'FAIL'),flush=True)
        args.output.write_text(json.dumps(dict(status='source/offline only; native paused',checks=results),indent=2)+'\n',encoding='utf-8')
        if run.returncode:
            print(run.stdout+run.stderr);raise SystemExit(run.returncode)
    print(str(len(results))+' release/source gates passed; native acceptance remains pending')
if __name__=='__main__':main()
