"""Compare the reference validator with an immutable Git text snapshot, offline."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',default='5b74e504ad9104cd9734aa123adeb0cb4cf87132')
    parser.add_argument('--powershell',required=True)
    args=parser.parse_args()
    revision=subprocess.check_output(['git','rev-parse','--verify',args.base+'^{commit}'],cwd=ROOT,text=True).strip()
    output=ROOT/'runtime-output/ac04-ac05';output.mkdir(parents=True,exist_ok=True)
    baseline=output/('reference-base-'+revision[:12]);baseline.mkdir(exist_ok=True)
    # Export data only. Never execute the exported mod or touch preserved sources.
    folders=['mod/2985041246/'+part for part in ('common','events','localisation','history','interface')]
    data=subprocess.check_output(['git','archive','--format=zip',revision,'--',*folders],cwd=ROOT)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for member in archive.infolist():
            target=(baseline/member.filename).resolve()
            if not target.is_relative_to(baseline.resolve()):raise ValueError('Unsafe archive member')
            if member.is_dir():target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(archive.read(member))
    reports={};hashes={}
    for name,mod in (('base',baseline/'mod/2985041246'),('current',ROOT/'mod/2985041246')):
        command=[args.powershell,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'tools/Validate-UlyssesReferences.ps1'),'-ModRoot',str(mod),'-Json']
        result=subprocess.run(command,cwd=ROOT,capture_output=True)
        raw=result.stdout+result.stderr;(output/('references-'+name+'.log')).write_bytes(raw)
        if result.returncode:raise SystemExit('Reference audit failed: '+name)
        reports[name]=json.loads(result.stdout.decode('utf-8-sig'))
        hashes[name]=hashlib.sha256(raw).hexdigest()
        # Disregard absolute roots and shifted source line numbers, retain the
        # actual warning text and the consumer file to detect new regressions.
        import re
        reports[name]['normalized_warnings']=sorted(set(re.sub(r':\d+\)',')',w.replace(str(mod.resolve()),'<mod>')) for w in reports[name]['Warnings']))
    previous=set(reports['base']['normalized_warnings']);current=set(reports['current']['normalized_warnings'])
    report=dict(schema=1,base=revision,command='Validate-UlyssesReferences.ps1 -ModRoot <base/current> -Json',
                baseline=reports['base']['Summary'],current=reports['current']['Summary'],
                new_warnings=sorted(current-previous),removed_warnings=sorted(previous-current),
                log_sha256=hashes,native_acceptance=False)
    (output/'reference-comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    if report['new_warnings']:raise SystemExit('New reference warnings require review')


if __name__=='__main__':main()
