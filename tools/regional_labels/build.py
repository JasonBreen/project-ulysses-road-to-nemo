"""Replace explicitly reviewed Earth-template captions; preserve physical geography."""
import argparse
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import get,parse

OUTPUT='localisation/english/replace/ac_world_regional_labels_l_english.yml'
PATTERN=re.compile(r'^\s*([^\s:#]+):\d*\s+"((?:\\.|[^"\\])*)"',re.M)


def entries(path):return dict(PATTERN.findall(path.read_text(encoding='utf-8-sig')))


def state_context(mod=MOD):
    states={}
    for path in (mod/'history/states').glob('*.txt'):
        body=get(parse(path.read_text(encoding='utf-8-sig')),'state');ident=int(get(body,'id'))
        states[ident]=dict(key=get(body,'name').strip('"'),owner=get(get(body,'history'),'owner'))
    return states


def locality_context(mod=MOD):
    provinces={};points=set()
    for path in (mod/'history/states').glob('*.txt'):
        body=get(parse(path.read_text(encoding='utf-8-sig')),'state');ident=int(get(body,'id'));history=get(body,'history');owner=get(history,'owner')
        for province,_,_ in get(body,'provinces',[]):provinces[int(province)]={'state':ident,'owner':owner}
        for key,_,value in history:
            if key=='victory_points' and isinstance(value,list) and len(value)>=2 and float(value[1][0])>0:points.add(int(value[0][0]))
    return provinces,points


def all_changes(data):return data['changes']+data.get('localities',[])+data.get('institution_captions',[])


def validate(data,mod=MOD):
    states=state_context(mod);seen=set();values=set();source_cache={}
    replacements={path.relative_to(mod).as_posix():entries(path)
                  for path in (mod/'localisation/english/replace').glob('*.yml')
                  if path.relative_to(mod).as_posix()!=OUTPUT}
    protected={row['state'] for row in data['excluded']}
    if protected!={171,607}:raise ValueError('Protected unresolved geography must retain its existing source requirements')
    for row in data['changes']:
        ident=row['state'];key=row['key']
        if ident in protected or ident in seen:raise ValueError('Protected or duplicate state mapping: '+str(ident))
        seen.add(ident)
        if states.get(ident)!={'key':key,'owner':row['owner']}:raise ValueError('State name/ownership contract changed: '+str(ident))
        source=row['source_file']
        if source not in source_cache:source_cache[source]=entries(mod/source)
        if source_cache[source].get(key)!=row['old']:raise ValueError('Inherited source changed; review the provisional caption before replacing it: '+key)
        kind=row.get('source_kind','earth_template_match')
        if row['source_layer']!='provisional gameplay' or kind not in ('earth_template_match','empty_caption') or (kind=='earth_template_match' and not row['reference_keys']) or (kind=='empty_caption' and row['old']!=''):raise ValueError('Missing provisional/source evidence: '+key)
        value=row['value']
        if value==row['old'] or value in values or not re.fullmatch(r'.+ (?:District [A-Z]+|Capital District)',value):raise ValueError('Invalid or conflicting neutral district caption: '+key)
        values.add(value)
        for captions in replacements.values():
            other=captions.get(key)
            if other is not None and other!=value:raise ValueError('Another regional owner already supplies a different caption: '+key)
    if len(seen)!=206 or sum(r.get('source_kind')=='empty_caption' for r in data['changes'])!=2:raise ValueError('Reviewed label scope changed; inspect the manifest instead of auto-approving candidates')
    provinces,points=locality_context(mod);keys={row['key'] for row in data['changes']}
    effective={}
    paths=sorted((mod/'localisation/english').rglob('*.yml'),key=lambda p:('replace' in p.relative_to(mod/'localisation/english').parts,p.as_posix()))
    for path in paths:
        if path.relative_to(mod).as_posix()!=OUTPUT:effective.update(entries(path))
    for row in data.get('localities',[]):
        if row['state'] in protected or provinces.get(row['province'])!={'state':row['state'],'owner':row['owner']} or row['province'] not in points:raise ValueError('Locality must retain its existing owned victory-point placement: '+row['key'])
        kind=row.get('source_kind')
        if row['key']!='VICTORY_POINTS_'+str(row['province']) or row['source_layer']!='provisional gameplay' or kind not in ('earth_template_match','missing_caption'):raise ValueError('Invalid locality identity/provenance')
        if kind=='missing_caption' and (row['old'] is not None or row['source_file'] is not None or row['reference_keys']):raise ValueError('Missing-caption record must not invent an inherited name')
        if kind=='earth_template_match' and (not row['reference_keys'] or not isinstance(row['source_file'],str)):raise ValueError('Missing primary locality evidence')
        if row['source_file'] and row['source_file'].startswith('engine://') and (row['source_file']!=data['locality_reference']['path'] or row['key'] not in row['reference_keys']):raise ValueError('Unverified engine locality binding')
        if effective.get(row['key'],row['old'])!=row['old']:raise ValueError('Existing locality owner changed: '+row['key'])
        if not re.fullmatch(r'.+ Locality [A-Z]+',row['value']) or row['value'] in values:raise ValueError('Invalid or duplicate locality caption')
        values.add(row['value'])
    if len(data.get('localities',[]))!=37 or sum(r.get('source_kind')=='missing_caption' for r in data['localities'])!=24 or len(data.get('institution_captions',[]))!=4:raise ValueError('Reviewed locality/institution scope changed')
    for row in all_changes(data):
        if row not in data['changes']:
            if row['key'] in keys:raise ValueError('Duplicate localization ownership: '+row['key'])
            keys.add(row['key'])
        source=row['source_file']
        if source is not None and not source.startswith('engine://'):
            if source not in source_cache:source_cache[source]=entries(mod/source)
            if source_cache[source].get(row['key'])!=row['old']:raise ValueError('Original caption changed: '+row['key'])
        if row['source_layer']!='provisional gameplay':raise ValueError('Missing provisional caption classification')
        for captions in replacements.values():
            if row['key'] in captions and captions[row['key']]!=row['value']:raise ValueError('Conflicting replacement caption: '+row['key'])


def build(data=None,mod=MOD):
    if data is None:data=json.loads((HERE/'labels.json').read_text())
    validate(data,mod)
    text='l_english:\n # Provisional districts/localities and adapted school captions, not canonical place claims. Provenance: tools/regional_labels/labels.json.\n'
    text+=''.join(' '+row['key']+':0 '+json.dumps(row['value'],ensure_ascii=False)+'\n' for row in all_changes(data))
    return {OUTPUT:text.encode('utf-8-sig')}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for relative,data in build().items():
        path=MOD/relative
        if args.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n',b'\n')!=data:raise SystemExit('Stale regional caption output: '+relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('206 state and 37 locality captions repaired; four school captions adapted; physical geography and protected states 171/607 unchanged.')
