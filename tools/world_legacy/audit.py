"""Actual shipped history/OOB matrix and sustainment inputs, never native QA."""
from collections import Counter
import copy
import json
from pathlib import Path

from build import HERE,ROOT,MOD,TAGS,BUDGETS,FLAG,parse,get,walk,selected,condition,normalized_hash,equipment_nodes


def geography():
    province_owner={};state_owner={};buildings={};capacities={tag:Counter() for tag in TAGS}
    for path in (MOD/'history/states').glob('*.txt'):
        body=get(parse(path.read_text(encoding='utf-8-sig')),'state');history=get(body,'history',[])
        ident=int(get(body,'id'));owner=get(history,'owner');state_owner[ident]=owner
        province_owner.update({int(p):owner for p,_,_ in get(body,'provinces',[])})
        buildings[ident]=get(history,'buildings',[])
        if owner in capacities and owner in [v for k,_,v in history if k=='add_core_of']:
            capacities[owner]['mil']+=int(get(buildings[ident],'arms_factory','0'))
            capacities[owner]['yards']+=int(get(buildings[ident],'dockyard','0'))
    return province_owner,state_owner,buildings,capacities


def actual_case(tag,bba,mtg,human=(),lar=True,nsb=False):
    contract=json.loads((HERE/'primary_contract.json').read_text())
    path=next((MOD/'history/countries').glob(tag+' - *.txt'))
    history=parse(path.read_text(encoding='utf-8-sig'))
    dlcs=({'By Blood Alone'} if bba else set())|({'Man the Guns'} if mtg else set())|({'La Resistance'} if lar else set())|({'No Step Back'} if nsb else set())
    effects=list(selected(history,dlcs,tag,human));technologies=set();variants={};rosters=[];stocks=[];errors=[]
    ideas={key for kind,_,body in effects if kind=='add_ideas' and isinstance(body,list) for key,_,_ in body}
    ideas.update(body for kind,_,body in effects if kind=='add_ideas' and isinstance(body,str))
    province_owner,state_owner,buildings,capacities=geography()
    def check_equipment(ident,version=None,production=False):
        if ident not in contract['equipment']:
            errors.append('Uncaptured equipment '+ident);return
        tech=contract['equipment'][ident]['technology']
        if tech and tech not in technologies:errors.append('Equipment before research '+ident+':'+tech)
        if version and (ident,version) not in variants:errors.append('Equipment before variant '+ident+':'+version)
        availability=contract['equipment'][ident].get('can_be_produced')
        if production and availability:
            if isinstance(availability,list):
                def substitute_predicates(nodes):
                    result=[]
                    for key,op,value in nodes:
                        if key=='has_idea':result.append(['always','=', 'yes' if value in ideas else 'no'])
                        elif key=='has_tech':result.append(['always','=', 'yes' if value in technologies else 'no'])
                        else:result.append([key,op,substitute_predicates(value) if isinstance(value,list) else value])
                    return result
                effective=list(selected(availability,dlcs,tag,human))
                if not condition(substitute_predicates(effective),dlcs,tag,human):errors.append('Equipment blocked by effective production rule '+ident)
            elif availability=='no':errors.append('Equipment not producible '+ident)
    for kind,_,body in effects:
        if kind=='set_technology':technologies.update(k for k,_,v in body if v=='1')
        elif kind=='create_equipment_variant':
            equipment=get(body,'type');name=get(body,'name');check_equipment(equipment)
            metadata=contract['equipment'][equipment];slots=metadata['module_slots'];used={};overrides={}
            for slot,_,module in get(body,'modules',[]):
                if module=='empty':continue
                row=contract['modules'][module];used[slot]=module
                if row['technology'] and row['technology'] not in technologies:errors.append('Module before research '+module)
                allowed=set(slots.get(slot,{}).get('categories',[]))|overrides.get(slot,set())
                explicit=slots.get(slot,{}).get('allowed_modules',[])
                if slot not in slots or (row['category'] not in allowed and module not in explicit):errors.append('Invalid slot/category '+equipment+':'+slot+':'+module)
                for target,categories in row.get('allowed_module_categories',{}).items():overrides.setdefault(target,set()).update(categories)
            if get(body,'modules') is not None:
                for slot,details in slots.items():
                    if details['required']=='yes' and slot not in used and metadata['default_modules'].get(slot) in (None,'empty'):errors.append('Required slot missing '+equipment+':'+slot)
            if (equipment,name) in variants:errors.append('Duplicate selected variant '+equipment+':'+name)
            variants[(equipment,name)]=dict(equipment=equipment,name=name,modules=used)
        elif kind in ('set_oob','set_air_oob','set_naval_oob'):
            name=body.strip('"');source=MOD/'history/units'/(name+'.txt');tree=parse(source.read_text(encoding='utf-8-sig'))
            divisions=[];ships=[];production=[];wings=[];templates=[]
            for key,value in walk(tree):
                if key=='division':
                    province=int(get(value,'location'));forced=[]
                    for equipment,_,details in get(value,'force_equipment_variants',[]):
                        version=get(details,'version_name');check_equipment(equipment,version,production=True)
                        forced.append(dict(equipment=equipment,version=version))
                    divisions.append(dict(name=get(value,'name'),location=province,template=get(value,'division_template'),forced_equipment=forced))
                    if province_owner.get(province)!=tag:errors.append('Invalid owned land placement '+name+':'+str(province))
                elif key=='division_template':
                    templates.append(dict(name=get(value,'name'),
                        regiments=[k for k,_,_ in get(value,'regiments',[])],
                        support=[k for k,_,_ in get(value,'support',[])]))
                elif key=='fleet':
                    province=int(get(value,'naval_base'))
                    if province_owner.get(province)!=tag:errors.append('Invalid owned port '+name+':'+str(province))
                elif key=='ship':
                    equipment,_,details=get(value,'equipment')[0];version=get(details,'version_name');check_equipment(equipment,version)
                    ships.append(dict(name=get(value,'name'),definition=get(value,'definition'),equipment=equipment,version=version))
                elif key=='add_equipment_production':
                    eq=get(value,'equipment');equipment=get(eq,'type');version=get(eq,'version_name');check_equipment(equipment,version,production=True)
                    queue=dict(equipment=equipment,version=version,factories=int(get(value,'requested_factories','0')),
                               progress=float(get(value,'progress','0')),efficiency=float(get(value,'efficiency','0')),amount=int(get(value,'amount','0')))
                    if not 0<=queue['progress']<=1 or not 0<=queue['efficiency']<=100:errors.append('Unbounded queue parameter '+name)
                    if queue['factories']<=0:errors.append('Invalid zero queue capacity '+name)
                    production.append(queue)
                elif key=='add_equipment_to_stockpile':
                    equipment=get(value,'type');version=get(value,'variant_name');check_equipment(equipment,version)
                    stocks.append(dict(equipment=equipment,version=version,amount=int(get(value,'amount')),source=name))
            for state,_,entries in get(tree,'air_wings',[]):
                destination=state.strip('"')
                if destination.isdigit():
                    state=int(destination)
                    if state_owner.get(state)!=tag:errors.append('Invalid owned air state '+name+':'+str(state))
                    if int(get(buildings[state],'air_base','0'))<=0:errors.append('Missing air base '+name+':'+str(state))
                else:
                    state=destination
                    carriers={s['name'].strip('"') for r in rosters for s in r['ships'] if s['definition']=='carrier'}
                    if destination not in carriers:errors.append('Missing selected carrier air target '+destination)
                for equipment,_,details in entries:
                    version=get(details,'version_name');check_equipment(equipment,version)
                    wings.append(dict(state=state,equipment=equipment,version=version,amount=int(get(details,'amount'))))
            rosters.append(dict(name=name,source=source.relative_to(ROOT).as_posix(),sha256=normalized_hash(source.read_bytes()),
                divisions=divisions,templates=templates,ships=ships,wings=wings,production=production))
        elif kind=='add_equipment_to_stockpile':
            equipment=get(body,'type');version=get(body,'variant_name');check_equipment(equipment,version)
            stocks.append(dict(equipment=equipment,version=version,amount=int(get(body,'amount')),source='country history'))
    names=[r['name'] for r in rosters]
    if len(names)!=len(set(names)) or len(names)!=3:errors.append('Roster loaded more/less than once '+str(names))
    on_reload=list(selected(history,dlcs,tag,human,loaded=True))
    if any(k in ('set_oob','set_air_oob','set_naval_oob','add_equipment_to_stockpile') for k,_,_ in on_reload):errors.append('Repeated setup grants survive guard')
    military=sum(q['factories'] for r in rosters if '_navy' not in r['name'] for q in r['production'])
    yards=sum(q['factories'] for r in rosters if '_navy' in r['name'] for q in r['production'])
    if military>capacities[tag]['mil'] or yards>capacities[tag]['yards']:errors.append('Production exceeds core-owned capacity')
    return dict(tag=tag,bba=bba,mtg=mtg,lar=lar,human_tags=list(human),nsb=nsb,
        capability_status='Source-equipment parity checked; native behavior untested' if lar else 'RELEASE GAP: reconnaissance-mission capability without La Resistance is not established; specialist aircraft retained',
        division_count=sum(len(r['divisions']) for r in rosters),ship_count=sum(len(r['ships']) for r in rosters),
        aircraft_count=sum(w['amount'] for r in rosters for w in r['wings']),
        core_capacity=dict(capacities[tag]),requested_capacity=dict(mil=military,yards=yards),
        selected_technology=sorted(technologies),variants=list(variants.values()),stockpiles=stocks,rosters=rosters,errors=errors)


def report():
    cases=[]
    for tag in TAGS:
        for bba,mtg,nsb in [(b,m,n) for b,m in [(False,False),(True,False),(False,True),(True,True)] for n in (False,True)]:
            for human in (((),('BLK',)) if tag=='FAT' else ((),)):
                for lar in (True,False):cases.append(actual_case(tag,bba,mtg,human,lar,nsb))
    divergences={}
    for tag in TAGS:
        data={}
        for suffix in ('navy','navy_dlc'):
            tree=parse(__import__('build').read_source('units',tag+'_'+suffix+'.txt'))
            ships=[v for k,v in walk(tree) if k=='ship']
            data[suffix]=dict(total=len(ships),roles=dict(Counter(get(v,'definition') for v in ships)),names=[get(v,'name') for v in ships])
        data['disposition']='Original definitions retained. Active designer roster is projected into a valid no-MTG roster; no active named hull is removed.'
        divergences[tag]=data
    return dict(schema=1,source_layer='Retained mod provenance plus explicit provisional compatibility/calibration.',
        evidence='Actual branch-sensitive shipped history and OOB inspection; not engine parsing, native DLC behavior, balance, supply or fuel acceptance.',
        primary_contract='tools/world_legacy/primary_contract.json',core_profiles=40,lar_disabled_gap_profiles=40,
        cases=cases,legacy_naval_divergences=divergences,
        release_gaps=['Native DLC loading, equipment consumption, crew assignments and mission operation remain untested.',
                      'La Resistance-disabled reconnaissance mission availability is not established by hidden tech grants.',
                      'Native No Step Back designer initialization and replacement operation remain untested despite valid source recipes and production gates.'])


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    data=report();text=json.dumps(data,indent=2)+'\n';path=HERE/'manifest.json'
    if args.check:
        assert path.read_text()==text,'Legacy manifest stale'
    else:path.write_text(text,encoding='utf-8',newline='\n')
    errors=[(r['tag'],r['bba'],r['mtg'],r['human_tags'],e) for r in data['cases'] for e in r['errors']]
    print('Legacy actual-source cases',len(data['cases']),'errors',len(errors))
    for row in errors[:35]:print(row)
    if len(errors)>35:print('Further errors retained in manifest.json')
    if errors:raise SystemExit(1)
