"""Explicit new-country admission; the initial six-row registry is untouched."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;STORY=HERE.parent;ROOT=HERE.parents[2];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools'),str(STORY)]
from schema import validate

APPROVED={'OSE':dict(id='second_frequency',base=700,cast=('rhea_calder','malik_renn','june_carver','sana_ivers')),
          'YUK':dict(id='names_on_the_board',base=800,cast=('irina_sokol','anton_rask','daria_vesnin','lev_miren'))}
CORE_SLOTS={'1':[1,2,6],'2':[3,7,12,16],'3':[4,8,13,17],'4':[5,9,11,14,18],'5':[10,15,19,20]}
ENDING_SLOTS={'trusted':6,'compromised':7,'fractured':8}


def campaigns(require_chapters=True):
    result=[]
    for tag,contract in APPROVED.items():
        path=HERE/'metadata'/(tag+'.json')
        if not path.exists():continue # Separate approved components may land independently.
        row=json.loads(path.read_text(encoding='utf-8-sig'))
        if row.get('tag')!=tag or row.get('id')!=contract['id']or row.get('base')!=contract['base']:raise ValueError('Unapproved Pacific story identity')
        if row.get('extension_contract')!='pacific_story_v1'or row.get('admission_until')!='2020.12.31':raise ValueError('Unapproved Pacific admission contract')
        if tuple(p['id']for p in row['cast'])!=contract['cast']:raise ValueError('The four approved original cast identities must remain stable')
        if row.get('chapters_by_slot')!=CORE_SLOTS or row.get('ending_slots')!=ENDING_SLOTS:raise ValueError('Locked Pacific core/ending art mapping changed')
        if require_chapters:
            row.update(json.loads((STORY/'chapters'/(tag+'.json')).read_text(encoding='utf-8-sig')))
            validate(row,horizon=row['admission_until'])
            if sum('callback'in c for c in row['chapters'])<12:raise ValueError('Pacific stories require twelve persistent later callbacks')
            for chapter in row['chapters']:
                for option in chapter['options']:
                    if any(type(option.get(k))is not int or not 1<=abs(option[k])<=8 for k in('cohesion','credibility')):raise ValueError('Pacific choices require two explicit bounded relationship changes')
        result.append(row)
    extras={p.stem for p in(HERE/'metadata').glob('*.json')}-set(APPROVED)
    if extras:raise ValueError('Unknown Pacific metadata: '+','.join(sorted(extras)))
    return result


def legacy_builder():
    spec=importlib.util.spec_from_file_location('pacific_original_story_compiler',STORY/'build.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def legacy_contract_files(base):
    import subprocess
    files=subprocess.check_output(['git','ls-tree','-r','--name-only',base],cwd=ROOT,text=True).splitlines()
    explicit={'tools/squadrons/campaigns.json','tools/squadrons/art_plan.json','tools/squadrons/assets.json','mod/2985041246/interface/ac_squadrons.gfx','mod/2985041246/common/frontend/backgrounds/ac_sq_backgrounds.txt'}
    return [p for p in files if p in explicit or p.startswith(('tools/squadrons/chapters/','tools/squadrons/sources/','mod/2985041246/gfx/AC_squadrons/'))or('/gfx/loadingscreens/ac_sq_'in p and p.endswith('.dds'))or Path(p).name in{'ac_squadrons.txt','ac_squadrons_l_english.yml'}]
