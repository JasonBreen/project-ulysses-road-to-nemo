"""Select a built-in image edit, retaining the exact previous original master."""
import argparse,hashlib,io,json,os,re
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent

def generated_home():
    return (Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))/'generated_images').resolve()

def select(asset_id, receipt_path, receipt_id, prompt_path):
    receipt=json.loads(Path(receipt_path).read_text())
    row=next(r for r in receipt if r['id']==receipt_id)
    source=Path(re.sub(r'^/(?=[A-Za-z]:)','',row['source_path'])).resolve()
    if not source.is_relative_to(generated_home())or source.suffix.lower()!='.png':raise ValueError('Not an actual built-in output')
    raw=source.read_bytes()
    if not raw.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid PNG')
    plan=json.loads((HERE/'plan.json').read_text());asset=next(a for a in plan['assets'] if a['id']==asset_id)
    selected=(HERE.parent/'sources'/asset['file']).resolve()
    if not selected.is_relative_to((HERE.parent/'sources').resolve()):raise ValueError('Selected master leaves source directory')
    prior=HERE.parent/'revisions'/(asset_id+'_before_edit.png')
    edit=json.loads(Path(prompt_path).read_text());meta=selected.with_suffix('.json');info=json.loads(meta.read_text())
    if not all(isinstance(edit.get(key),str)and edit[key].strip()for key in('prompt','reason')):raise ValueError('Edit needs a prompt and reason')
    if not isinstance(info.get('prompt'),str):raise ValueError('Existing prompt metadata is missing')
    with Image.open(io.BytesIO(raw))as image:
        image.load();width,height,mode=image.width,image.height,image.mode
    selected_raw=selected.read_bytes();prior_raw=prior.read_bytes()if prior.exists()else selected_raw
    if prior.exists()and selected_raw!=raw and selected_raw!=prior_raw:raise ValueError('Unexpected source: refusing to overwrite')
    if 'base_prompt' not in info:info['base_prompt']=info['prompt']
    reference='tools/squadrons/revisions/'+prior.name
    info.update(prompt=edit['prompt'],generation_references=[reference],source_output=source.name,
        sha256=hashlib.sha256(raw).hexdigest(),revision_source_sha256=hashlib.sha256(prior_raw).hexdigest(),
        revision_reason=edit['reason'],visual_reviewed=False,review='Edited original master; awaiting individual visual review')
    info.update(width=width,height=height,mode=mode)
    asset.update(prompt=edit['prompt'],generation_references=[reference])
    metadata_bytes=(json.dumps(info,indent=2)+'\n').encode();plan_bytes=(json.dumps(plan,indent=2)+'\n').encode()
    # Validate and serialize everything before retaining or replacing a master.
    prior.parent.mkdir(exist_ok=True)
    if not prior.exists():
        with prior.open('xb')as retained:retained.write(prior_raw)
    selected.write_bytes(raw);meta.write_bytes(metadata_bytes);(HERE/'plan.json').write_bytes(plan_bytes)
    print('Selected built-in edit; prior original retained:',prior)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('asset_id');p.add_argument('receipt',type=Path);p.add_argument('receipt_id');p.add_argument('prompt',type=Path)
    a=p.parse_args();select(a.asset_id,a.receipt,a.receipt_id,a.prompt)
