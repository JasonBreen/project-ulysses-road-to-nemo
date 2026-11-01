"""Select a built-in image edit, retaining the exact previous original master."""
import argparse,hashlib,json,os,re,shutil
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent

def select(asset_id, receipt_path, receipt_id, prompt_path):
    receipt=json.loads(Path(receipt_path).read_text())
    row=next(r for r in receipt if r['id']==receipt_id)
    source=Path(re.sub(r'^/(?=[A-Za-z]:)','',row['source_path'])).resolve()
    home=Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))/'generated_images'
    if not source.is_relative_to(home.resolve()):raise ValueError('Not an actual built-in output')
    raw=source.read_bytes()
    if not raw.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid PNG')
    plan=json.loads((HERE/'plan.json').read_text());asset=next(a for a in plan['assets'] if a['id']==asset_id)
    selected=HERE.parent/'sources'/asset['file']
    prior=HERE.parent/'revisions'/(asset_id+'_before_edit.png');prior.parent.mkdir(exist_ok=True)
    if not prior.exists():shutil.copyfile(selected,prior)
    elif selected.read_bytes()!=raw and selected.read_bytes()!=prior.read_bytes():raise ValueError('Unexpected source: refusing to overwrite')
    shutil.copyfile(source,selected)
    edit=json.loads(Path(prompt_path).read_text());meta=selected.with_suffix('.json');info=json.loads(meta.read_text())
    if 'base_prompt' not in info:info['base_prompt']=info['prompt']
    reference='tools/squadrons/revisions/'+prior.name
    info.update(prompt=edit['prompt'],generation_references=[reference],source_output=source.name,
        sha256=hashlib.sha256(raw).hexdigest(),revision_source_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),
        revision_reason=edit['reason'],visual_reviewed=False,review='Edited original master; awaiting individual visual review')
    with Image.open(selected) as image:info.update(width=image.width,height=image.height,mode=image.mode)
    asset.update(prompt=edit['prompt'],generation_references=[reference])
    meta.write_bytes((json.dumps(info,indent=2)+'\n').encode());(HERE/'plan.json').write_bytes((json.dumps(plan,indent=2)+'\n').encode())
    print('Selected built-in edit; prior original retained:',prior)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('asset_id');p.add_argument('receipt',type=Path);p.add_argument('receipt_id');p.add_argument('prompt',type=Path)
    a=p.parse_args();select(a.asset_id,a.receipt,a.receipt_id,a.prompt)
