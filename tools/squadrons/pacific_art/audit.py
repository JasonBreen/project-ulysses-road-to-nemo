"""Validate the 26 retained originals; does not claim DDS or native acceptance."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCES=HERE.parent/'sources'
PNG=b'\x89PNG\r\n\x1a\n'

def digest(raw):return hashlib.sha256(raw).hexdigest()
def text_digest(raw):return digest(raw.replace(b'\r\n',b'\n'))
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)

def validate_image(raw, metadata, actual_size, alpha):
    if not raw.startswith(PNG):raise ValueError('Invalid original PNG signature (possible text filter damage)')
    if digest(raw)!=metadata['sha256']:raise ValueError('Selected original hash differs')
    if actual_size!=(metadata['width'],metadata['height']):raise ValueError('Selected original dimensions differ')
    if alpha!=(255,255):raise ValueError('Full-bleed original has unintended transparency')

def sources():
    plan=json.loads((HERE/'plan.json').read_text())
    brief=(HERE/'brief.md').read_bytes()
    if text_digest(brief)!=plan['brief_sha256']:raise ValueError('Locked writer brief changed')
    assets=plan['assets']
    if len(assets)!=26 or len({a['id'] for a in assets})!=26:raise ValueError('Require exactly26 distinct selected masters')
    counts={family:sum(a['file'].startswith(family+'/') for a in assets) for family in ('portraits','scenes','loading')}
    if counts!={'portraits':8,'scenes':16,'loading':2}:raise ValueError('Incorrect cast/scene/loading coverage')
    ready=[]
    for a in assets:
        path=SOURCES/a['file'];m=json.loads(path.with_suffix('.json').read_text())
        if (m.get('id'),m.get('tag'),m.get('file'))!=(a['id'],a['tag'],path.name):raise ValueError('Identity mismatch: '+a['id'])
        if m.get('generator')!='built-in image_gen' or m.get('prompt')!=a['prompt']:raise ValueError('Exact built-in prompt missing: '+a['id'])
        if m.get('transparent_background') is not False or m.get('visual_reviewed') is not True:raise ValueError('Individual source review incomplete: '+a['id'])
        if not m.get('review') or 'pending' in m['review'].lower():raise ValueError('Incomplete review: '+a['id'])
        if m.get('brief_sha256')!=plan['brief_sha256']:raise ValueError('Brief provenance differs: '+a['id'])
        if m.get('generation_references',[])!=a.get('generation_references',[]):raise ValueError('Edit references differ: '+a['id'])
        with Image.open(path) as image:
            validate_image(path.read_bytes(),m,image.size,image.convert('RGBA').getchannel('A').getextrema())
            if image.width<(800 if a['file'].startswith('portraits/') else 1500):raise ValueError('Master too small')
        for ref in m.get('generation_references',[]):
            retained=(ROOT/ref).resolve()
            if not retained.is_relative_to((HERE.parent/'revisions').resolve()):raise ValueError('Original reference not retained locally')
            if digest(retained.read_bytes())!=m['revision_source_sha256']:raise ValueError('Edited-source provenance differs')
            if not m.get('base_prompt') or not m.get('revision_reason'):raise ValueError('Edit history missing')
        ready.append({**a,**m,'path':path})
    if len({r['sha256'] for r in ready})!=26:raise ValueError('Distinct subjects reuse an identical master')
    for tag in ('OSE','YUK'):
        scene=[a for a in assets if a['tag']==tag and a['file'].startswith('scenes/')]
        by_id={int(a['id'].rsplit('_',1)[1]):a for a in scene}
        if set(by_id)!=set(range(1,9)):raise ValueError('Missing host scene')
        if sorted(n for i in range(1,6) for n in by_id[i]['chapters'])!=list(range(1,21)):raise ValueError('Core chapters not covered exactly once')
        if [by_id[i]['ending'] for i in (6,7,8)]!=['trusted','compromised','fractured']:raise ValueError('Distinct personal endings missing')
        if any(by_id[i]['chapters'] for i in (6,7,8)):raise ValueError('Personal endings reused as core chapters')
    baseline=json.loads((HERE/'preserved_sources.json').read_text())
    for rel,expected in baseline['files'].items():
        p=ROOT/rel;raw=p.read_bytes()
        actual=text_digest(raw) if p.suffix=='.json' else digest(raw)
        if actual!=expected:raise ValueError('Existing source altered: '+rel)
    return plan,ready

def blob_check(ready,revision='HEAD'):
    paths=[r['path'] for r in ready]
    paths+=sorted({ROOT/ref for row in ready for ref in row.get('generation_references',[])})
    for path in paths:
        rel=path.relative_to(ROOT).as_posix()
        if git('show',revision+':'+rel)!=path.read_bytes():raise ValueError('Committed raw PNG differs: '+rel)
    return len(paths)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--git-blobs',action='store_true');p.add_argument('--revision',default='HEAD');a=p.parse_args()
    plan,ready=sources();n=blob_check(ready,a.revision) if a.git_blobs else 0
    print(f'Pacific original artwork:26/26 original masters individually reviewed/hash-verified;156 inherited source files preserved;{n} committed raw PNG blobs checked. Source/crop evidence only; native rendering untested.')

if __name__=='__main__':main()
