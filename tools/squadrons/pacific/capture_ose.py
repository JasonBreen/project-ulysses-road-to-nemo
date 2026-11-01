"""One explicit reviewed-parent capture; never an automatic generation target.

The original six-country contract is deliberately not read or rewritten here.
Only the first Osean story component is pinned for the second-country delta.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from config import ROOT,HERE
from usea_expansion.script import parse,get

REVIEWED_OSE_SOURCE='7776f754418d7ecbaa5309bb9925fd1825aa7796'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true',required=True)
    a=p.parse_args();revision=subprocess.check_output(['git','rev-parse',REVIEWED_OSE_SOURCE],cwd=ROOT,text=True).strip()
    target=HERE/'ose_contract.json';contract=json.loads(target.read_text())
    if contract['base']not in('fa0506ecf3d564e03baf51be1466798929fcf44d',revision):raise ValueError('Unexpected Osean capture; review required')
    if contract['base']=='fa0506ecf3d564e03baf51be1466798929fcf44d':
        prior=ROOT/'docs/evidence/pacific-stories/YUK-independent/draft-ose-contract.json'
        prior.parent.mkdir(parents=True,exist_ok=True);prior.write_bytes(target.read_bytes())
    def source(relative):return subprocess.check_output(['git','show',revision+':'+relative],cwd=ROOT)
    for relative in contract['files']:contract['files'][relative]=hashlib.sha256(source(relative)).hexdigest()
    for relative,records in contract['nodes'].items():
        tree=parse(source(relative).decode('utf-8-sig'));path=Path(relative)
        if path.parent.name=='events':nodes={get(v,'id'):v for k,_,v in tree if k=='country_event'}
        elif path.suffix=='.gfx':nodes={get(v,'name'):v for k,_,v in get(tree,'spriteTypes')}
        else:nodes={k:v for k,_,v in tree}
        for name,record in records.items():
            value=nodes[name]
            if record['prefix_length']is not None:record['prefix_length']=len(value)
            record['sha256']=hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
    text=source('mod/2985041246/localisation/english/ac_squadrons_pacific_l_english.yml').decode('utf-8-sig')
    contract['localization']={key:hashlib.sha256(value.encode()).hexdigest()for key,value in re.findall(r'^ ([^ :]+):0 "(.*)"$',text,re.M)}
    contract['base']=revision;contract['capture_scope']='Final independently packaged Osean content; earlier unpublished draft capture retained separately. Initial six-country315-file contract unchanged.'
    target.write_text(json.dumps(contract,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Pinned reviewed Osean parent '+revision+'; no original-six contract recaptured')


if __name__=='__main__':main()
