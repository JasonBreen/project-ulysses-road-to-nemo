"""Retain rejected/edited prompt history while selecting an exact new prompt."""
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent

def revise(path):
    revision=json.loads(Path(path).read_text())
    if not isinstance(revision.get('prompt'),str)or not revision['prompt'].strip():raise ValueError('Revision needs a prompt')
    plan=json.loads((HERE/'plan.json').read_text());asset=next(a for a in plan['assets']if a['id']==revision['id'])
    history_path=HERE/'prompt_revisions'/(asset['id']+'.json')
    if history_path.exists():raise FileExistsError('Retained prompt history already exists; refusing to overwrite: '+str(history_path))
    meta=HERE.parent/'sources'/Path(asset['file']).with_suffix('.json')
    info=json.loads(meta.read_text());history={**revision,'previous_prompt':asset['prompt']}
    asset['prompt']=revision['prompt'];info['prompt']=revision['prompt'];info['prompt_revision']=history
    history_bytes=(json.dumps(history,indent=2)+'\n').encode();plan_bytes=(json.dumps(plan,indent=2)+'\n').encode();metadata_bytes=(json.dumps(info,indent=2)+'\n').encode()
    history_path.parent.mkdir(exist_ok=True)
    with history_path.open('xb')as retained:retained.write(history_bytes)
    (HERE/'plan.json').write_bytes(plan_bytes);meta.write_bytes(metadata_bytes)
    return history


if __name__=='__main__':revise(sys.argv[1])
