"""Author the immutable initial portfolio receipt once; never silently rebaseline."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from config import HERE,ROOT,legacy_contract_files

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',required=True);args=p.parse_args()
    target=HERE/'legacy_contract.json'
    if target.exists():raise SystemExit('Legacy contract exists; review explicitly rather than overwrite it')
    rows={}
    for relative in legacy_contract_files(args.base):
        raw=subprocess.check_output(['git','show',args.base+':'+relative],cwd=ROOT)
        blob=subprocess.check_output(['git','rev-parse',args.base+':'+relative],cwd=ROOT,text=True).strip()
        rows[relative]=dict(git_blob=blob,sha256=hashlib.sha256(raw).hexdigest(),binary=Path(relative).suffix in('.png','.dds'))
    target.write_text(json.dumps(dict(schema=1,base=args.base,initial_hosts=['BLK','UST','ERU','SNS','EMM','EVA'],core_chapters=120,core_cast=24,events=282,original_masters=78,packaged_textures=139,
        rule='Canonical Git blobs remain exact; PNG/DDS must also preserve raw working bytes. Compiler/schema tools have only reviewed default-preserving seams and are checked by original output reproduction.',files=rows),indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Pinned',len(rows),'immutable initial portfolio files')
