"""Copy exact selected built-in outputs; never regenerate or edit PNG masters."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];SOURCES=HERE.parent/'sources'

def intake(receipt):
    plan=json.loads((HERE/'plan.json').read_text());assets={row['id']:row for row in plan['assets']}
    rows=json.loads(Path(receipt).read_text());rows=rows if isinstance(rows,list) else [rows]
    home=Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))/'generated_images'
    for row in rows:
        asset=assets[row['id']];source=Path(re.sub(r'^/(?=[A-Za-z]:)', '',row['source_path'])).resolve()
        if not source.is_relative_to(home.resolve()) or source.suffix.lower()!='.png':raise ValueError('Output is not an actual built-in generated PNG path')
        raw=source.read_bytes()
        if not raw.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Invalid PNG signature')
        destination=(SOURCES/asset['file']).resolve()
        if not destination.is_relative_to(SOURCES.resolve()):raise ValueError('Destination leaves story source directory')
        destination.parent.mkdir(parents=True,exist_ok=True)
        if destination.exists():
            if destination.read_bytes()!=raw:raise ValueError('Refusing to overwrite a different selected master: '+asset['id'])
        else:shutil.copyfile(source,destination)
        metadata=destination.with_suffix('.json');info=json.loads(metadata.read_text()) if metadata.exists() else {}
        with Image.open(destination) as image:width,height=image.size;mode=image.mode
        info.update(id=asset['id'],tag=asset['tag'],kind=asset['kind'],file=destination.name,
            source_layer=plan['source_layer'],generator='built-in image_gen',prompt=asset['prompt'],transparent_background=False,
            generation_references=asset.get('generation_references',[]),brief_sha256=plan['brief_sha256'],
            source_output=source.name,sha256=hashlib.sha256(raw).hexdigest(),width=width,height=height,mode=mode,
            intake_utc=datetime.now(timezone.utc).isoformat())
        if not info.get('visual_reviewed'):
            info.update(visual_reviewed=False,review='Generated original master; pending individual visual review')
        metadata.write_bytes((json.dumps(info,indent=2)+'\n').encode())
        print(asset['id'],str(destination),width,height,info['sha256'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('receipt',type=Path);a=p.parse_args();intake(a.receipt)
