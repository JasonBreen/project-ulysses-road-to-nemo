"""Retain rejected/edited prompt history while selecting an exact new prompt."""
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
revision=json.loads(Path(sys.argv[1]).read_text())
plan=json.loads((HERE/'plan.json').read_text())
asset=next(a for a in plan['assets'] if a['id']==revision['id'])
history={**revision,'previous_prompt':asset['prompt']}
(HERE/'prompt_revisions').mkdir(exist_ok=True)
(HERE/'prompt_revisions'/(asset['id']+'.json')).write_bytes((json.dumps(history,indent=2)+'\n').encode())
asset['prompt']=revision['prompt']
(HERE/'plan.json').write_bytes((json.dumps(plan,indent=2)+'\n').encode())
meta=HERE.parent/'sources'/Path(asset['file']).with_suffix('.json')
info=json.loads(meta.read_text());info['prompt']=revision['prompt'];info['prompt_revision']=history
meta.write_bytes((json.dumps(info,indent=2)+'\n').encode())
