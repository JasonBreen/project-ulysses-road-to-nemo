"""One-time authoring capture of inherited sources at the verified parent."""
import json,subprocess
from pathlib import Path
from audit import HERE,ROOT,digest,text_digest
BASE='25ab6721073992fdfff31eeb4baea42cdedf81c8'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','tools/squadrons/sources'],cwd=ROOT,text=True).splitlines()
assert len(paths)==156
files={}
for rel in paths:
    raw=subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT)
    files[rel]=(text_digest if rel.endswith('.json') else digest)(raw)
target=HERE/'preserved_sources.json'
if target.exists():raise SystemExit('Refusing to recapture immutable inherited source map')
target.write_bytes((json.dumps(dict(schema=1,base_commit=BASE,scope='78 inherited PNG originals/raw hashes and78 metadata records/LF-normalized text',files=files),indent=2)+'\n').encode())
plan=json.loads((HERE/'plan.json').read_text())
for a in plan['assets']:
    m=json.loads((HERE.parent/'sources'/Path(a['file']).with_suffix('.json')).read_text())
    if m.get('visual_reviewed'):a['status']='original master visually reviewed'
(HERE/'plan.json').write_bytes((json.dumps(plan,indent=2)+'\n').encode())
print('Captured156 inherited files from exact verified parent; original art unchanged.')
