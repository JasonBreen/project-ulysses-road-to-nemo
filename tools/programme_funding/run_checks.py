"""Pin source and execute the three actual paid-programme owners offline."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from source_snapshot import capture,verify


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--reference',type=Path);parser.add_argument('--baseline',type=Path)
    parser.add_argument('--only',action='append')
    args=parser.parse_args();py=[sys.executable,'-B']
    jobs=[('partner-runtime',py+['tools/usean_partners/test_integration.py']),
        ('reconstruction-runtime',py+['tools/Test-ReconstructionContinuations.py']),
        ('superpower-runtime',py+['tools/Test-SuperpowerProgrammes.py']),
        ('partner-content',py+['tools/usean_partners/test_content.py','--require-dependencies']),
        ('reconstruction-art',py+['tools/Test-ReconstructionAssets.py']),
        ('superpower-art',py+['tools/Test-SuperpowerAssets.py']),
        ('partner-generated',py+['tools/usean_partners/build.py','--check']),
        ('reconstruction-generated',py+['tools/reconstruction/build.py','--check']),
        ('superpower-generated',py+['tools/superpowers/build.py','--check']),
        ('registry',py+['tools/world_foundation/registry.py','--check']),
        ('strict-assets',py+['tools/audit_visual_dependencies.py','--strict-all']),
        ('shared-owners',py+['tools/Test-SharedSystems.py']),
        ('source-snapshot',py+['tools/Test-SourceSnapshot.py'])]
    if args.reference:
        command=['pwsh','-NoProfile','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246','-ReferenceGameRoot',str(args.reference)]
        if args.baseline:command+=['-BaselineRoot',str(args.baseline)]
        jobs.append(('full-static',command))
    if args.only:
        requested=set(args.only);known={name for name,_ in jobs}
        if requested-known:raise SystemExit('Unknown checks: '+str(requested-known))
        jobs=[row for row in jobs if row[0]in requested]
    source=capture(ROOT);args.output.mkdir(parents=True,exist_ok=True)
    def run(item):
        name,command=item;start=time.monotonic()
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        output=result.stdout+result.stderr
        (args.output/(name+'.txt')).write_text(output,encoding='utf-8',newline='\n')
        print(name+': '+('PASS'if result.returncode==0 else'FAIL'),flush=True)
        if result.returncode:print('Failure excerpt; full output in '+str(args.output/(name+'.txt'))+'\n'+'\n'.join(output.splitlines()[-40:]),flush=True)
        return dict(name=name,command=['python'if part==sys.executable else part for part in command],exit_code=result.returncode,seconds=round(time.monotonic()-start,2),log=name+'.txt')
    with ThreadPoolExecutor(max_workers=2)as executor:rows=list(executor.map(run,jobs))
    payload=hashlib.sha256()
    for path in sorted((ROOT/'mod/2985041246').rglob('*'),key=lambda p:p.as_posix()):
        if path.is_file():payload.update(path.relative_to(ROOT).as_posix().encode()+b'\0'+path.read_bytes())
    after=verify(source,ROOT)
    report=dict(source_inputs=source,source_inputs_after=after,checks=rows,payload_sha256=payload.hexdigest(),
        payload_hash_rule='Sorted repository-relative POSIX path,NUL,raw delivered mod bytes.',
        scope='Exact-source actual-script/offline execution only; no native, serialized save or AI acceptance.',native_acceptance=False)
    (args.output/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    raise SystemExit(any(row['exit_code']for row in rows))


if __name__=='__main__':main()
