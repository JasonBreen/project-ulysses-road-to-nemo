"""Branch-sensitive research/design chronology for explicit startup consumers.

This interprets only history selection and named equipment consumption. It is
not HOI4, a module-fit audit, an OOB personnel model or native DLC acceptance.
Unknown selectors/unlocks fail closed. Installed fallback metadata is captured
separately; current same-path mod technology definitions are read live.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from decimal import Decimal
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from economy_script import parse


def get(nodes,key,default=None):return next((v for k,_,v in nodes if k==key),default)


def walk(nodes):
    for row in nodes:
        yield row
        if isinstance(row[2],list):yield from walk(row[2])


def unlock_rows(source):
    """Retain facts about direct unlocks, never installed script/media bytes."""
    rows={}
    for kind,_,body in parse(source):
        if kind!='technologies':continue
        for ident,_,node in body:
            if not isinstance(node,list):continue
            # Repeated list assignments occur in the effective electronics
            # override. Inspect every authored list, including a later nonempty
            # one; taking only the first assignment would invent missing tech.
            rows[ident]={family:[k for key,_,items in node if key==field
                                for k,_,v in items]
                         for family,field in (('equipment','enable_equipments'),
                                              ('modules','enable_equipment_modules'))}
    return rows


def capture(reference,target):
    reference=Path(reference);files={}
    for path in sorted((reference/'common/technologies').glob('*.txt')):
        data=path.read_bytes();files[path.relative_to(reference).as_posix()]=dict(sha256=hashlib.sha256(data).hexdigest(),technologies=unlock_rows(data.decode('utf-8-sig')))
    convoy=reference/'common/units/equipment/convoys.txt'
    report=dict(schema=1,source_layer='Read-only installed primary unlock identifiers and file hashes; no complete script or media payload copied',
        installed_version=json.loads((reference/'launcher-settings.json').read_text(encoding='utf-8-sig'))['rawVersion'],
        fallback_files=files,always_available_equipment=['convoy_1'],
        inherent_note='convoy_1 has no equipment-unlock technology in the primary technology catalogue; retained primary convoy definition and all technology file hashes bound this explicit baseline exception.',
        inherent_source=dict(path='engine://common/units/equipment/convoys.txt',sha256=hashlib.sha256(convoy.read_bytes()).hexdigest()))
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')


def catalog(mod,contract):
    files={relative:row['technologies']for relative,row in contract['fallback_files'].items()}
    for path in sorted((mod/'common/technologies').glob('*.txt')):files[path.relative_to(mod).as_posix()]=unlock_rows(path.read_text(encoding='utf-8-sig'))
    by_tech={}
    for source,rows in sorted(files.items()):
        for ident,unlocks in rows.items():
            canonical={k:sorted(set(v))for k,v in unlocks.items()}
            if ident in by_tech and by_tech[ident]!=canonical:raise ValueError('Conflicting effective research unlock '+ident+' in '+source)
            by_tech[ident]=canonical
    result={'equipment':defaultdict(set),'modules':defaultdict(set)}
    for tech,row in by_tech.items():
        for family in result:
            for ident in row[family]:result[family][ident].add(tech)
    return result


def selected(nodes,dlcs,ai,tags,flags=None,scope=None):
    """Execute supported history selectors, including sibling/nested else."""
    flags={}if flags is None else flags
    def condition(rows,who):
        answers=[]
        for key,_,value in rows:
            lower=key.lower()
            if lower=='has_dlc':answer=value in dlcs
            elif lower=='is_ai':answer=ai.get(who,True)==(value=='yes')
            elif lower=='has_country_flag':answer=value in flags.setdefault(who,set())
            elif lower=='always':answer=value=='yes'
            elif lower in('and','or','not'):
                items=[condition([r],who)for r in value]
                answer=all(items)if lower=='and'else any(items)if lower=='or'else not all(items)
            elif key in tags:answer=condition(value,key)
            else:raise ValueError('Unsupported startup selector '+key)
            answers.append(answer)
        return all(answers)
    branch=None
    for key,op,value in nodes:
        if key=='if':
            branch=condition(get(value,'limit',[]),scope)
            if branch:yield from selected([r for r in value if r[0]not in('limit','else','else_if')],dlcs,ai,tags,flags,scope)
            else:
                for kind,_,body in[r for r in value if r[0]in('else','else_if')]:
                    if kind=='else'or condition(get(body,'limit',[]),scope):
                        yield from selected([r for r in body if r[0]!='limit'],dlcs,ai,tags,flags,scope);branch=True;break
        elif key in('else','else_if'):
            if branch is None:raise ValueError('Orphan startup '+key)
            if not branch and(key=='else'or condition(get(value,'limit',[]),scope)):
                yield from selected([r for r in value if r[0]!='limit'],dlcs,ai,tags,flags,scope);branch=True
        else:
            branch=None
            if key=='set_country_flag':flags.setdefault(scope,set()).add(get(value,'flag')if isinstance(value,list)else value)
            elif key=='clr_country_flag':flags.setdefault(scope,set()).discard(value)
            yield key,op,value


def equipment_uses(tree):
    """Typed wings, ships, forced designs, stockpiles and production orders."""
    for kind,_,node in walk(tree):
        if not isinstance(node,list):continue
        if kind=='add_equipment_to_stockpile':yield get(node,'type'),get(node,'variant_name'),get(node,'producer'),'stockpile'
        elif kind=='add_equipment_production':
            eq=get(node,'equipment',[]);yield get(eq,'type'),get(eq,'version_name'),get(eq,'creator'),'production'
        elif kind=='ship':
            for equipment,_,details in get(node,'equipment',[]):yield equipment,get(details,'version_name'),get(details,'creator'),'ship'
        elif kind=='force_equipment_variants':
            for equipment,_,details in node:
                if get(details,'version_name'):yield equipment,get(details,'version_name'),get(details,'creator'),'forced design'
    for _,_,wings in get(tree,'air_wings',[]):
        for equipment,_,details in wings:yield equipment,get(details,'version_name'),get(details,'creator'),'air wing'


def inspect_history(tag,history,unit_reader,unlocks,always_available,dlcs,ai,tags):
    technologies=set();variants={};errors=[];uses=0;flags={};loading=[]
    local={(get(v,'type'),get(v,'name'))for k,_,v in walk(history)if k=='create_equipment_variant'}
    def researched(ident,family,where):
        if family=='equipment'and ident in always_available:return
        choices=unlocks[family].get(ident,set())
        if not choices:errors.append(f'{where}: no effective captured {family} unlock for {ident}')
        elif not choices&technologies:errors.append(f'{where}: {family} {ident} used before required research {sorted(choices)}')
    def use(equipment,version,creator,where):
        nonlocal uses
        uses+=1;researched(equipment,'equipment',where)
        # A country's named designs must exist before their actual consumers.
        # An unrelated/unused declaration can legitimately occur later. The
        # required type and selected design's modules are checked at use, not
        # merely on creation of an otherwise unused historical template.
        pair=(equipment,version)
        if version:
            if creator not in (None,tag):
                errors.append(f'{where}: foreign producer {creator} needs an explicit cross-country startup proof for {equipment}/{version}')
            elif pair not in local:
                errors.append(f'{where}: named variant {equipment}/{version} has no country-history or loaded-OOB declaration')
            elif pair not in variants:
                errors.append(f'{where}: variant {equipment}/{version} used before its selected declaration')
            else:
                for slot,module in variants[pair]:
                    if module!='empty':researched(module,'modules',where+':'+version+'/'+slot)
    military=('create_equipment_variant','set_oob','set_air_oob','set_naval_oob',
              'add_equipment_to_stockpile','add_equipment_production','force_equipment_variants')
    def execute(nodes,where='country'):
        for key,op,value in selected(nodes,dlcs,ai,tags,flags,scope=tag):
            if key=='set_technology':
                for name,_,amount in value:
                    if Decimal(amount)>=1:technologies.add(name)
                    else:technologies.discard(name)
            elif key=='create_equipment_variant':
                equipment=get(value,'type');name=get(value,'name')
                variants[equipment,name]=[(slot,module)for slot,_,module in get(value,'modules',[])]
            elif key in('set_oob','set_air_oob','set_naval_oob'):
                if value in loading:
                    errors.append(value+': recursive startup OOB load');continue
                try:tree=unit_reader(value)
                except (OSError,ValueError,KeyError)as error:errors.append(value+': uninspectable OOB source: '+str(error));continue
                local.update((get(v,'type'),get(v,'name'))for k,_,v in walk(tree)if k=='create_equipment_variant')
                loading.append(value)
                execute(tree,value)
                loading.pop()
            elif key=='instant_effect':
                # OOB effects are country effects. In particular the NSB and
                # legacy production branches are alternatives, not two queues.
                execute(value,where)
            elif key in ('units','air_wings','division_template'):
                if any(k in ('if','else','else_if')for k,_,v in walk(value)):
                    errors.append(where+': unsupported conditional inside OOB '+key);continue
                for equipment,version,creator,kind in equipment_uses([(key,op,value)]):
                    use(equipment,version,creator,where+':'+kind)
            elif key=='add_equipment_to_stockpile':
                use(get(value,'type'),get(value,'variant_name'),get(value,'producer'),
                    where+' stockpile'if where=='country'else where+':stockpile')
            elif key=='add_equipment_production':
                eq=get(value,'equipment',[])
                use(get(eq,'type'),get(eq,'version_name'),get(eq,'creator'),
                    where+' production'if where=='country'else where+':production')
            elif isinstance(value,list)and any(k in military for k,_,v in walk(value)):
                errors.append('Unsupported nested startup military wrapper '+key)
    execute(history)
    return dict(errors=errors,explicit_equipment_uses=uses,selected_technologies=len(technologies),selected_variants=len(variants))


def inspect_mod(mod,contract):
    mod=Path(mod);unlocks=catalog(mod,contract);histories={p.name[:3]:parse(p.read_text(encoding='utf-8-sig'))for p in(mod/'history/countries').glob('*.txt')}
    dlc_names=sorted({v for tree in histories.values()for k,_,v in walk(tree)if k=='has_dlc'})
    if len(dlc_names)>6:raise ValueError('Startup DLC selector matrix exceeds the explicitly bounded six-selector audit')
    # Vary every country identity actually read by an AI selector, plus the
    # current country. Never assign contradictory AI states to the same tag.
    units={}
    def unit_reader(name):
        if name not in units:units[name]=parse((mod/'history/units'/(name+'.txt')).read_text(encoding='utf-8-sig'))
        return units[name]
    cases=[]
    for tag,tree in sorted(histories.items()):
        ai_tags={tag}
        def ai_reads(nodes,scope):
            for key,_,value in nodes:
                if key=='is_ai':ai_tags.add(scope)
                if isinstance(value,list):ai_reads(value,key if key in histories else scope)
        ai_reads(tree,tag)
        if len(ai_tags)>6:raise ValueError('Startup AI selector matrix exceeds the bounded six-country audit')
        names=sorted(ai_tags)
        for bits in product((False,True),repeat=len(dlc_names)):
            dlcs={name for name,on in zip(dlc_names,bits)if on}
            for ai_bits in product((False,True),repeat=len(names)):
                ai=dict(zip(names,ai_bits))
                row=inspect_history(tag,tree,unit_reader,unlocks,set(contract['always_available_equipment']),dlcs,ai,set(histories))
                cases.append(dict(tag=tag,dlcs=sorted(dlcs),ai=dict(sorted(ai.items())),**row))
    return dict(schema=1,evidence='Selected startup script order and explicit typed consumers; not native research, module fit, DLC missions or land battalion-equipment inference',
        countries=len(histories),dlc_selectors=dlc_names,cases=cases,error_count=sum(len(r['errors'])for r in cases))


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mod-root',type=Path,default=ROOT/'mod/2985041246');p.add_argument('--contract',type=Path,default=HERE/'research_contract.json');p.add_argument('--capture-reference',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
 if a.capture_reference:capture(a.capture_reference,a.contract)
 result=inspect_mod(a.mod_root,json.loads(a.contract.read_text()))
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
 print('Selected startup chronology:',len(result['cases']),'cases,',result['error_count'],'errors')
 unique=sorted({(r['tag'],error)for r in result['cases']for error in r['errors']})
 for tag,error in unique[:35]:print(tag+': '+error)
 if len(unique)>35:print('Further unique errors:',len(unique)-35)
 raise SystemExit(bool(result['error_count']))

if __name__=='__main__':main()
