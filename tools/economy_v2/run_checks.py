"""Retain reproducible source/offline results for the macroeconomic package."""
import argparse, concurrent.futures, hashlib, json, shutil, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/evidence/economy-v2'


def clean_output(data,engine=None):
    """Keep retained diagnostics independent of the developer's drive layout."""
    text=data.decode('utf-8',errors='replace')
    for path,label in ((ROOT,'<repository>'),(engine,'<installed-engine-reference>')):
        if path:
            for spelling in (str(path),path.as_posix()):text=text.replace(spelling,label)
    return text.encode('utf-8')


def compact_screen_report(path):
    """Keep this package's closure; Package 0 owns the complete backlog ledger."""
    data=json.loads(path.read_text())
    data['coverage']='Economy v2 selected-screen loose-file dependency closure; global counts are inventory only, not conversion or native acceptance.'
    data['gate_covered_screens']={key:value for key,value in data['gate_covered_screens'].items() if key=='ac_macro_economy.gui'}
    data['scripted_gui_bindings']=[row for row in data['scripted_gui_bindings'] if row['source']=='common/scripted_guis/ac_macro_economy.txt']
    data.pop('consumers',None)
    data.pop('statically_retired_consumers',None)
    data['global_backlog_note']='The full consumer-level ledger belongs to Package 0. Re-run audit_consumers.py without this compaction for the complete inventory.'
    path.write_text(json.dumps(data,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path);p.add_argument('--core',action='store_true');a=p.parse_args()
    py=[sys.executable,'-B']
    checks={
        'macro':py+['tools/Test-EconomyV2.py'],
        'ledger':py+['tools/Test-EconomyLedger.py'],
        'forces':py+['tools/Test-ForceUpkeep.py'],
        'shared-owners':py+['tools/Test-SharedSystems.py'],
        'institutions':py+['tools/Test-Institutions.py'],
        'legacy':py+['-m','unittest','discover','-s','tools','-p','test_economy.py'],
        'factions':py+['tools/Test-UlyssesFactions.py'],
        'interfaces':py+['tools/Test-InterfaceRepairs.py'],
        'generated-macro':py+['tools/economy_v2/build.py','--check'],
        'generated-anea':py+['tools/anea/foundation.py','--check'],
        'assets':py+['tools/audit_visual_dependencies.py','--strict-all'],
    }
    if a.engine:
        checks['factions']+=['--reference-game-root',str(a.engine)]
        checks['forces']+=['--engine',str(a.engine)]
    if a.core:
        ps_host = shutil.which('pwsh')
        if not ps_host:
            raise SystemExit('--core requires the current PowerShell (pwsh) host; WindowsPowerShell5.1 does not satisfy the full validation contract.')
        checks['core']=[ps_host,'-NoProfile','-ExecutionPolicy','Bypass','-File','tools/Test-UlyssesStatic.ps1','-ModRoot','mod/2985041246']
        if a.engine:checks['core']+=['-ReferenceGameRoot',str(a.engine)]
    audit=ROOT/'tools/overhaul/audit_consumers.py'
    if a.engine and audit.exists():
        checks['screen-dependencies']=py+[str(audit.relative_to(ROOT)),str(a.engine),'--gate-screen','ac_macro_economy.gui','--output',str(OUT/'engine-dependencies.json')]
    OUT.mkdir(parents=True,exist_ok=True)
    def run(pair):
        name,command=pair;start=time.monotonic()
        result=subprocess.run(command,cwd=ROOT,capture_output=True)
        if name=='screen-dependencies' and (OUT/'engine-dependencies.json').exists():compact_screen_report(OUT/'engine-dependencies.json')
        (OUT/(name+'.txt')).write_bytes(clean_output(result.stdout+result.stderr,a.engine))
        safe=['python' if token==sys.executable else 'pwsh' if a.core and token==ps_host else '<installed-engine-reference>' if a.engine and token==str(a.engine) else token for token in command]
        row=dict(check=name,command=safe,exit_code=result.returncode,seconds=round(time.monotonic()-start,2),log=name+'.txt',coverage='source/offline; not native acceptance')
        print(name+': '+('PASS' if result.returncode==0 else 'FAIL'),flush=True);return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,checks.items()))
    revision=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
    (OUT/'results.json').write_text(json.dumps(dict(coverage='source and offline validation only',base_commit=revision,
                         source_state='working-tree candidate; validation logs are not native evidence',checks=rows,native_status='paused; untested'),indent=2)+'\n')
    raise SystemExit(any(row['exit_code'] for row in rows))


if __name__=='__main__':main()
