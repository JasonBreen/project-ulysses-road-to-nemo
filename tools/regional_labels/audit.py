"""Audit effective state and authored-locality captions against primary names."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from build import MOD,HERE,OUTPUT,entries,state_context,locality_context


def report(reference,mod=MOD):
    data=json.loads((HERE/'labels.json').read_text());primary={};changed=[]
    for family,field in [('state','reference'),('locality','locality_reference')]:
        row=data[field];path=reference/row['path'].removeprefix('engine://')
        primary[family]=entries(path)
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:changed.append(row['path'])
    effective={};mod_points=set()
    paths=sorted((mod/'localisation/english').rglob('*.yml'),key=lambda p:('replace' in p.relative_to(mod/'localisation/english').parts,p.as_posix()))
    for path in paths:
        captions=entries(path);effective.update(captions);mod_points.update(k for k in captions if re.fullmatch(r'VICTORY_POINTS_\d+',k))
    states=state_context(mod);provinces,points=locality_context(mod);rows=[];protected={r['state'] for r in data['excluded']}
    def add(family,key,state,owner,province=None):
        value=effective.get(key,primary[family].get(key));problem=None
        if value is None or value=='':problem='unresolved_caption'
        elif value in set(primary[family].values()):problem='primary_earth_template_match'
        elif re.fullmatch(r'\d+|TEMP|XXX|\?+',value):problem='numeric_or_unmapped'
        if problem:rows.append(dict(family=family,key=key,state=state,owner=owner,province=province,value=value,problem=problem,protected=state in protected))
    for ident,row in states.items():add('state',row['key'],ident,row['owner'])
    point_keys=mod_points|{'VICTORY_POINTS_'+str(p) for p in points}
    orphaned=[]
    for key in sorted(point_keys):
        province=int(key.rsplit('_',1)[1]);context=provinces.get(province)
        if context is None:orphaned.append(key);continue
        add('locality',key,context['state'],context['owner'],province)
    unprotected=[r for r in rows if not r['protected']]
    return dict(schema=1,coverage='Effective English source comparison against pinned primary names; not native map rendering or canonical geography.',states=len(states),authored_victory_point_provinces=len(points),mod_locality_keys=len(mod_points),orphaned_mod_locality_keys=orphaned,reference_changes=changed,remaining=rows,unprotected_problem_count=len(unprotected),reviewed_repair_scope_passed=not unprotected and not changed,complete_map_label_acceptance=False,complete_gate_reason='Protected unresolved geography remains; unreviewed source layers and native map behavior are not certified.',native_acceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path,required=True);parser.add_argument('--output',type=Path);parser.add_argument('--gate-reviewed',action='store_true');args=parser.parse_args();data=report(args.reference)
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(data,indent=2))
    if args.gate_reviewed and not data['reviewed_repair_scope_passed']:raise SystemExit(1)
