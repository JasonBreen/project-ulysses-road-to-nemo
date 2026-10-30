"""Create a disposable physical engine/profile copy; never alter normal user data."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
GAME=Path('G:/steamlbirary/steamapps/common/Hearts of Iron IV')
NORMAL=Path.home()/'Documents/Paradox Interactive/Hearts of Iron IV'
TARGET=Path('G:/Project-Ulysses-Native-20261030-Expansion')
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def protected():
    files=[p for p in NORMAL.rglob('*') if p.is_file() and (p.parent==NORMAL or 'save games' in p.parts or 'logs' in p.parts)]
    return {str(p):dict(size=p.stat().st_size,sha256=digest(p)) for p in files}
def main():
    p=argparse.ArgumentParser();p.add_argument('--sync-payload',action='store_true');p.add_argument('--verify-normal',action='store_true');a=p.parse_args()
    evidence=TARGET/'evidence';profile=TARGET/'profile';engine=TARGET/'engine'
    if a.verify_normal:
        before=json.loads((evidence/'normal_before.json').read_text());after=protected()
        changed=[p for p in before if before[p]!=after.get(p)];added=[p for p in after if p not in before]
        (evidence/'normal_verification.json').write_text(json.dumps(dict(changed=changed,added=added),indent=2))
        print('Normal profile:',len(before),'protected files;',len(changed),'changed;',len(added),'added.')
        if changed or added:raise SystemExit(1)
        return
    if not a.sync_payload:
        if TARGET.exists():raise SystemExit('Refusing to overwrite an existing native session; use --sync-payload only while the game is closed.')
        evidence.mkdir(parents=True);profile.mkdir()
        config=json.loads((GAME/'launcher-settings.json').read_text())
        assert config['rawVersion']=='1.19.4.1',config['rawVersion']
        (evidence/'normal_before.json').write_text(json.dumps(protected(),indent=2))
        for source in (NORMAL/'logs').glob('*'):
            if source.is_file():
                backup=evidence/'normal_log_backup'/source.name;backup.parent.mkdir(exist_ok=True);shutil.copy2(source,backup)
        print('Normal profile preservation manifest saved. Copying engine...',flush=True)
        shutil.copytree(GAME,engine)
        (engine/'userdir.txt').write_text(profile.as_posix())
        config['gameDataPath']=profile.as_posix();(engine/'launcher-settings.json').write_text(json.dumps(config,indent=2))
        settings=(NORMAL/'settings.txt').read_text()
        settings=re.sub(r'size\s*=\s*\{\s*x=\d+\s*y=\d+\s*}', 'size={ x=3440 y=1440 }',settings,count=1)
        settings=re.sub(r'gui_scale=[\d.]+','gui_scale=1.000000',settings)
        settings=settings.replace('borderless=no','borderless=yes')
        settings=re.sub(r'auto_save\s*=\s*"?\w+"?','auto_save="NEVER"',settings)
        settings=re.sub(r'master_volume=[\d.]+','master_volume=0.000000',settings)
        (profile/'settings.txt').write_text(settings)
        (profile/'pdx_settings.json').write_text('{}')
    payload=profile/'mod/ulysses_expansion';payload.parent.mkdir(parents=True,exist_ok=True)
    if a.sync_payload:
        query=subprocess.run(['powershell','-NoProfile','-Command',"Get-Process -Name hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Path"],capture_output=True,text=True)
        if str(engine/'hoi4.exe').lower().replace('/','\\') in query.stdout.lower():
            raise SystemExit('Close the disposable test game before replacing its payload.')
    shutil.copytree(ROOT/'mod/2985041246',payload,dirs_exist_ok=True)
    # Copy only candidate files; detect stale files rather than deleting them.
    expected={p.relative_to(ROOT/'mod/2985041246').as_posix():digest(p) for p in (ROOT/'mod/2985041246').rglob('*') if p.is_file()}
    actual={p.relative_to(payload).as_posix():digest(p) for p in payload.rglob('*') if p.is_file()}
    assert actual==expected,'Payload does not exactly match the candidate'
    (evidence/'payload_manifest.json').write_text(json.dumps(expected,indent=2))
    descriptor=(payload/'descriptor.mod').read_text()
    descriptor=re.sub(r'^name=.*$', 'name="Project Ulysses Expansion Native 20261030"',descriptor,flags=re.M)
    descriptor+='\npath="'+payload.as_posix()+'"\n'
    (profile/'mod/ulysses_expansion.mod').write_text(descriptor)
    (profile/'dlc_load.json').write_text(json.dumps(dict(disabled_dlcs=[],enabled_mods=['mod/ulysses_expansion.mod'])))
    assert digest(engine/'hoi4.exe')==digest(GAME/'hoi4.exe')
    print('Prepared isolated engine and exact payload:',len(expected),'files.',flush=True)
if __name__=='__main__':main()
