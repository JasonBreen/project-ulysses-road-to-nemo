"""Read-only geography, identity and current-capacity intake for legitimate releases.

Known entry footprints are inherited mod contracts. All capital/logistics
selection and later maintenance calibration are provisional gameplay. This
inspector never changes a state, province, capital, country history or force.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/world_starts'),str(ROOT/'tools/anea')]
from script import parse,get,walk
from foundation_map import topology,components,shortest
from technical import Engine
from policies import capture as capture_policies

TAGS=('AWW','REC','REL','SBK','SER','SHI','TER')
KNOWN={
    'AWW':[dict(id='awwnb_entry',states=[272],source='events/AWWNB.txt:awwnb.1/.2',inherited_liability=True)],
    'REC':[dict(id='recta_birth',states=[300,316,345],source='events/Recta.txt:recta.1'),
           dict(id='recta_birth_with_293',states=[293,300,316,345],source='events/Recta.txt:recta.1 conditional293'),
           dict(id='recta_treaty',states=[293,316],source='events/Belka.txt:belka_dlp_war.101/.103')],
    'SBK':[dict(id='south_belka_collapse',states=[8,302,330,364,369],source='events/South_Belka.txt:south_belka.2/.3/.4'),
           dict(id='south_belka_defeat',states=[228,270,331,584,590],added_cores=[228,270,331,584,590],source='events/Belka.txt:belka_dlp_war.101'),
           dict(id='south_belka_armistice',states=[228,270,331,584,590],source='events/Belka.txt:belka_dlp_war.103')],
}


def digest(path):
    raw=path.read_bytes()
    return hashlib.sha256(raw if path.suffix.lower()=='.bmp' else raw.replace(b'\r\n',b'\n')).hexdigest()


def scalar_nodes(nodes):
    for key,_,value in nodes:
        yield key,value
        if isinstance(value,list):yield from scalar_nodes(value)


def inspect(reference=None):
    previous=json.loads((HERE/'intake.json').read_text()) if (HERE/'intake.json').exists() else None
    defs,graph,centres,area,_=topology();states={};province_state={};inputs={}
    for path in sorted((MOD/'history/states').glob('*.txt')):
        body=get(parse(path.read_text(encoding='utf-8-sig')),'state');history=get(body,'history');ident=int(get(body,'id'))
        provinces=[int(k) for k,_,_ in get(body,'provinces')];province_state.update({p:ident for p in provinces})
        buildings=get(history,'buildings');states[ident]=dict(source=path.relative_to(MOD).as_posix(),owner=get(history,'owner'),
            cores=[v for k,_,v in history if k=='add_core_of'],population=int(get(body,'manpower')),
            provinces=provinces,resources={k:float(v) for k,_,v in get(body,'resources',[])},
            buildings={k:int(get(buildings,k,'0')) for k in ('industrial_complex','arms_factory','dockyard','infrastructure','air_base','fuel_silo')},
            ports={k:int(get(v,'naval_base','0')) for k,_,v in buildings if isinstance(v,list) and get(v,'naval_base') is not None},
            victory_points={v[0][0]:int(v[1][0]) for k,_,v in history if k=='victory_points'})
    airports={int(k):int(v[0][0]) for k,_,v in parse((MOD/'map/airports.txt').read_text()) if k.isdigit() and v}
    engine=Engine(reference) if reference else None;countries={}
    for tag in TAGS:
        path=next((MOD/'history/countries').glob(tag+' - *.txt'));source=path.read_text(encoding='utf-8-sig');history=parse(source)
        core_states=sorted(i for i,s in states.items() if tag in s['cores']);historic=int(get(history,'capital'))
        inputs[path.relative_to(MOD).as_posix()]=digest(path)
        cases=[dict(case) for case in KNOWN.get(tag,[])]+([dict(id='generic_core_release',states=core_states,source='Existing state cores; adapter awaits legitimate external release, not a new activation route.')] if core_states else [])
        if tag=='AWW':
            relative='events/AWWNB.txt';events=parse((MOD/relative).read_text(encoding='utf-8-sig'))
            event=next(body for key,_,body in events if key=='country_event' and get(body,'id')=='awwnb.2')
            blocked=sorted({int(value) for key,value in scalar_nodes(event) if key=='set_province_controller'})
            cases.append({**cases[0],'id':'awwnb_after_controller_changes','controlled_exclusions':blocked})
            inputs[relative]=digest(MOD/relative)
        for case in cases:
            selected=[states[i] for i in case['states']];owned={p for s in selected for p in s['provinces'] if defs[p]['land']}
            controlled=owned-set(case.get('controlled_exclusions',[]))
            groups=sorted(components(controlled,graph),key=lambda group:(-sum(int(area[p]) for p in group),min(group)))
            main=groups[0];weight=sum(int(area[p]) for p in main);centroid=tuple(sum(centres[p][n]*int(area[p]) for p in main)/weight for n in (0,1))
            candidates=[i for i in case['states'] if airports[i] in main] or sorted({province_state[p] for p in main})
            capital=historic if historic in case['states'] and any(province_state[p]==historic for p in controlled) else min(candidates,key=lambda i:((centres[airports[i]][0]-centroid[0])**2+(centres[airports[i]][1]-centroid[1])**2,i))
            vps={int(p):value for p,value in states[capital]['victory_points'].items() if int(p) in controlled}
            cap_province=min(vps,key=lambda p:(-vps[p],p)) if vps else airports[capital] if airports[capital] in controlled else min(p for p in controlled if province_state[p]==capital)
            case['capital_state']=capital;case['capital_province']=cap_province
            case['historical_capital_retained']=capital==historic
            case['core_population']=sum(s['population'] for i,s in zip(case['states'],selected) if tag in s['cores'] or i in case.get('added_cores',[]))
            case['owned_population']=sum(s['population'] for s in selected)
            case['raw_industry']={kind:sum(s['buildings'][kind] for s in selected) for kind in ('industrial_complex','arms_factory','dockyard')}
            case['core_industry_lower']={kind:sum(s['buildings'][kind] for i,s in zip(case['states'],selected) if tag in s['cores'] or i in case.get('added_cores',[])) for kind in ('industrial_complex','arms_factory','dockyard')}
            case['components']=[]
            for group in groups:
                existing_ports=sorted(int(p) for s in selected for p,level in s['ports'].items() if level and int(p) in group)
                root=cap_province if cap_province in group else existing_ports[0] if existing_ports else min(group)
                terminals=sorted({airports[i] for i in case['states'] if airports[i] in group and any(states[i]['buildings'][kind] for kind in ('industrial_complex','arms_factory','dockyard'))}|set(existing_ports)|{root})
                case['components'].append(dict(provinces=sorted(group),root=root,existing_receiving_ports=existing_ports,
                    terminals=terminals,routes=[shortest(root,p,graph,set(group)) for p in terminals if p!=root],
                    capital_component=cap_province in group,landlocked_detached=cap_province not in group and not existing_ports))
        required=set(core_states)|{historic}|{i for case in cases for i in case['states']}
        for i in required:inputs[states[i]['source']]=digest(MOD/states[i]['source'])
        countries[tag]=dict(history=path.relative_to(MOD).as_posix(),historical_capital=historic,core_states=core_states,
            identities=[v for k,_,v in history if k=='recruit_character'],
            opening_policies=capture_policies(source,tag,engine) if engine else previous['countries'][tag]['opening_policies'],
            state_inputs={str(i):states[i] for i in sorted(required)},known_cases=cases,
            generic_unknown_footprint='Must choose an actually owned valid capital and bounded local maintenance; no universal connectivity or force grant is inferred.',
            classification='Inherited mod entry/identity; provisional geography/capacity calibration, not official canon.')
    fallback=[]
    for ident,state in states.items():
        if ident==171:continue
        land=[p for p in state['provinces'] if defs[p]['land']]
        if not land:continue
        points={int(p):v for p,v in state['victory_points'].items() if int(p) in land}
        anchor=min(points,key=lambda p:(-points[p],p)) if points else airports[ident]
        fallback.append(dict(state=ident,land_area=sum(int(area[p]) for p in land),capital_province=anchor,airport=airports[ident],
            original_VPs=state['victory_points']))
        inputs[state['source']]=digest(MOD/state['source'])
    fallback.sort(key=lambda row:(-row['land_area'],row['state']))
    for relative in ('map/definition.csv','map/provinces.bmp','map/adjacencies.csv','map/airports.txt','map/buildings.txt'):
        inputs[relative]=digest(MOD/relative)
    protected_placeholder={states[171]['source']:digest(MOD/states[171]['source'])}
    protected_placeholder.update({path.relative_to(MOD).as_posix():digest(path) for path in (MOD/'history/countries').glob('PLH - *.txt')})
    return dict(schema=1,base='224c9ccb23f7745d1829b334c5f901c897e83c72',countries=countries,fallback_states=fallback,source_inputs_sha256=dict(sorted(inputs.items())),
        protected_placeholder_sha256=protected_placeholder,
        primary_sources_sha256=dict(sorted(engine.used.items())) if engine else previous['primary_sources_sha256'],
        capital_rule='Prefer the historical capital when owned and usable under current control. Otherwise choose the state airport nearest the area-weighted raster centroid of the largest controlled owned-land component; break ties by state ID. Retain the highest existing controlled VP as the province anchor, then a controlled airport/local fallback. Runtime control/footprint checks remain required.',
        hash_rule='BMP raster bytes are raw; UTF-8 text input hashes normalize CRLF to LF.',
        native='No native release, controller update, construction, unit transfer or serialization acceptance.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=inspect(args.reference);text=json.dumps(result,indent=2)+'\n';path=HERE/'intake.json'
    if args.check:
        if not path.exists() or path.read_text()!=text:raise SystemExit('Release intake differs; inspect source/geometry/identity changes before recapture')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    for tag,row in result['countries'].items():print(tag,[(c['id'],c['capital_state'],c['core_population'],c['core_industry_lower']) for c in row['known_cases']])
