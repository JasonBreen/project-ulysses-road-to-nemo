"""Bind actual checked subprocess receipts to the delivered national payload.

Does not run or impersonate tests. Earlier failures are retained explicitly;
only a later actual invocation of the same named check supersedes its result.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
RUNTIME=ROOT/'runtime-output/fato-south-belka';DEST=ROOT/'docs/evidence/fato-south-belka'
REPORTS=('checks','followup-checks','primary-start-checks','final-component-checks','final-presentation-checks','formatting-checks','formatting-presentation')

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    checks={};attempts=[];DEST.mkdir(parents=True,exist_ok=True);(DEST/'logs').mkdir(exist_ok=True)
    for folder in REPORTS:
        report=json.loads((RUNTIME/folder/'checks.json').read_text())
        for row in report['checks']:
            log=RUNTIME/folder/(row['name']+'.txt')
            delivered=DEST/'logs'/(folder+'-'+row['name']+'.txt')
            delivered.write_text(log.read_text(),encoding='utf-8',newline='\n')
            item=dict(row,source_report=folder,log=delivered.relative_to(ROOT).as_posix(),log_sha256=sha(delivered))
            match=re.search(r'Ran (\d+) tests?',log.read_text())
            if match:item['unittest_methods']=int(match.group(1))
            if row['name']in checks:attempts.append(checks[row['name']])
            checks[row['name']]=item
    failures=[r for r in checks.values()if r['exit_code']]
    if failures:raise SystemExit('Current check failure: '+str(failures))
    static=RUNTIME/'full-static-final.txt'
    if 'Static regression checks passed.'not in static.read_text():raise SystemExit('Full static success marker absent')
    (DEST/'logs/full-static-final.txt').write_text(static.read_text(),encoding='utf-8',newline='\n')
    paths=set()
    for folder in ('common/decisions','common/decisions/categories','common/ideas','common/on_actions','common/scripted_effects','common/scripted_triggers','events'):
        paths.add(MOD/folder/'ac_fato_south_belka.txt')
    paths.update((MOD/'common/national_focus/ac_fsb_fat.txt',MOD/'common/national_focus/ac_fsb_sbk.txt',MOD/'interface/ac_fato_south_belka.gfx',MOD/'localisation/english/ac_fato_south_belka_l_english.yml'))
    paths.update((MOD/'gfx/AC_fato_south_belka').rglob('*.dds'))
    paths.update(HERE.glob('*.py'));paths.update(HERE.glob('*.svg'));paths.add(HERE/'focus-review.png');paths.update((HERE/'assets.json',HERE/'purposes.json',HERE/'pacing.json',HERE/'engine_contract.json'))
    paths.update((ROOT/'source/artwork/fato_south_belka').glob('*'))
    paths.update(ROOT/p for p in ('tools/institutions/content.py','tools/institutions/profiles.json','mod/2985041246/common/scripted_triggers/ac_politics.txt','tools/world_foundation/country_registry.json'))
    for folder in ('common/scripted_effects','common/scripted_triggers','common/on_actions'):
        paths.update(p for p in (MOD/folder).glob('ac_*.txt')if p.name.startswith(('ac_macro','ac_economy','ac_politics')))
    paths.update(ROOT/'tools/economy_v2'/name for name in ('build.py','money.py','ledger.py','forces.py','force_observables.json','profiles.json'))
    paths.add(ROOT/'tools/institutions/build.py')
    payload={p.relative_to(ROOT).as_posix():sha(p)for p in sorted(paths)}
    receipt=dict(schema=1,parent='172b0726e0170012cc60650994ea3d3fe9c07551',source_layer='provisional national gameplay and original artwork',
        installed_reference=dict(rawVersion='1.19.4.1',source='read-only launcher-settings.json; verified separately from generic PE version metadata'),
        evidence='Actual source/Decimal execution and static validation only. No native, shortcut runtime, natural AI, user-save or installation acceptance.',
        native='paused',publication='not pushed; parent review owns PR publication',payload_sha256=payload,
        latest_checks=list(checks.values()),superseded_attempts=attempts,
        correction='The first broad runner referenced a nonexistent supporting-country filename; the corrected Test-UseaExpansion.py invocation passed. This failed attempt is retained, not treated as gameplay evidence.',
        full_static=dict(log='docs/evidence/fato-south-belka/logs/full-static-final.txt',sha256=sha(DEST/'logs/full-static-final.txt'),exit_code=0),
        formatting_followup=json.loads((DEST/'formatting-followup.json').read_text()),
        counts=dict(country_focuses={'FAT':54,'SBK':42},scenes=20,original_scene_masters=8,focus_compositions=96,dds_textures=218,decision_row_variants_measured=981))
    (DEST/'source-receipts.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(str(len(checks))+' current source gates pass; '+str(len(payload))+' payload/source receipts; earlier attempts retained; native paused')
if __name__=='__main__':main()
