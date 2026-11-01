"""Owned-raster release routes; existing rails/ports are never replaced.

Only captured known footprints are eligible. Arbitrary external release shapes
receive the valid-capital/local maintenance adapter, not guessed sea links.
"""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
def block(name,body):return name+' = {\n'+'\n'.join(('\t'+line.rstrip() if line.strip() else '') for line in body.splitlines())+'\n}\n'
def capture(intake):
    path=MOD/'map/railways.txt';edges={}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        values=line.split('#')[0].split()
        if not values:continue
        level,count=map(int,values[:2]);route=list(map(int,values[2:]))
        if len(route)!=count:raise ValueError('Bad inherited railway row')
        for a,b in zip(route,route[1:]):edges[tuple(sorted((a,b)))]=max(level,edges.get(tuple(sorted((a,b))),0))
    result={}
    for tag,country in intake['countries'].items():
        cases=[];seen=set()
        for case in country['known_cases']:
            key=(tuple(case['states']),tuple(case.get('controlled_exclusions',[])))
            if key in seen:continue
            seen.add(key);missing=set();controlled=set()
            for component in case['components']:
                controlled.update(component['provinces'])
                for route in component['routes']:
                    for a,b in zip(route,route[1:]):
                        edge=tuple(sorted((a,b)))
                        if not edges.get(edge,0):missing.add(edge)
            cases.append(dict(id=case['id'],states=case['states'],capital=case['capital_state'],controlled_provinces=sorted(controlled),
                controlled_exclusions=case.get('controlled_exclusions',[]),missing_edges=[list(edge) for edge in sorted(missing)],
                components=[dict(root=c['root'],provinces=c['provinces'],receiving_ports=c['existing_receiving_ports'],capital_component=c['capital_component'],landlocked_detached=c['landlocked_detached']) for c in case['components']],
                coverage='Exact captured footprint and all required controlled provinces; existing receiving ports need continued operation. No cross-water railway, new coast, hub, port, VP or geography edit.'))
        result[tag]=cases
    return dict(schema=1,countries=result,railways_sha256=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        unknown_footprint='Capital/local maintenance only; explicit network coverage gap. The user can build through the regular construction system.',
        native='Runtime railway precedence, port capacity and engine supply delivery remain untested.')

def condition(case):
    return ' '.join('owns_state = '+str(s) for s in case['states'])+'\nall_owned_state = { OR = { '+' '.join('state = '+str(s) for s in case['states'])+' } }\n'+\
        ' '.join('controls_province = '+str(p) for p in case['controlled_provinces'])+'\n'+\
        ' '.join('NOT = { controls_province = '+str(p)+' }' for p in case['controlled_exclusions'])

def outputs(data):
    effects='';triggers='';events='';decisions={};loc=[];cancels={}
    for tag,cases in data['countries'].items():
        stem='ac_release_'+tag;active=stem+'_network_active';wait=stem+'_network_waiting';done=stem+'_network_done';event='ac_release.'+str(200+list(data['countries']).index(tag))
        eligible='tag = '+tag+' original_tag = '+tag+' ac_release_maintenance_active = yes political_power >= 50 ac_econ_can_fund_release_project = yes NOT = { has_country_flag = ac_release_project_active } NOT = { has_country_flag = ac_release_project_cooldown } NOT = { has_global_flag = '+done+' }'
        covered=[];possible=[];start='';finish='';valid=[];cleanup=''
        for n,case in enumerate(cases):
            gate=condition(case);covered.append(block('AND',gate));caseflag=stem+'_network_case'+str(n)
            if not case['missing_edges']:continue
            missing_now=block('OR',''.join('NOT = { has_railway_connection = { path = { '+str(a)+' '+str(b)+' } } }\n' for a,b in case['missing_edges']))
            possible.append(block('AND',gate+'\n'+missing_now));valid.append(block('AND','has_country_flag = '+caseflag+'\n'+gate))
            start+=block('if' if not start else 'else_if',block('limit',gate)+'set_country_flag = '+caseflag)
            routes=''.join(block('if','limit = { NOT = { has_railway_connection = { path = { '+str(a)+' '+str(b)+' } } } }\n'+block('build_railway','level = 1\npath = { '+str(a)+' '+str(b)+' }')) for a,b in case['missing_edges'])
            finish+=block('if',block('limit','has_country_flag = '+caseflag+'\n'+gate)+routes+'set_global_flag = '+done)
            cleanup+='clr_country_flag = '+caseflag+'\n'
        triggers+=block(stem+'_known_network',block('OR',''.join(covered)))
        triggers+=block(stem+'_network_target_valid',block('OR',''.join(valid)) if valid else 'always = no')
        triggers+=block(stem+'_can_repair_network',eligible+'\n'+(block('OR',''.join(possible)) if possible else 'always = no'))
        effects+=block(stem+'_start_network',block('if','limit = { '+stem+'_can_repair_network = yes }\nac_econ_try_fund_release_project = yes\n'+block('if','limit = { has_country_flag = ac_econ_release_project_funded }\nadd_political_power = -50\n'+start+'\nset_country_flag = '+active+'\nset_country_flag = ac_release_project_active\nset_country_flag = { flag = '+wait+' days = 90 }\ncountry_event = { id = '+event+' days = 90 }')))
        cleanup+='clr_country_flag = '+active+'\nclr_country_flag = '+wait+'\nclr_country_flag = ac_release_project_active\nset_country_flag = { flag = ac_release_project_cooldown days = 30 }'
        effects+=block(stem+'_cancel_network',block('if','limit = { has_country_flag = '+active+' }\n'+cleanup))
        effects+=block(stem+'_finish_network',block('if','limit = { tag = '+tag+' original_tag = '+tag+' has_country_flag = '+active+' NOT = { has_country_flag = '+wait+' } }\n'+block('if','limit = { has_capitulated = no NOT = { has_global_flag = '+done+' } }\n'+finish)+cleanup))
        events+=block('country_event','id = '+event+'\nhidden = yes\nis_triggered_only = yes\nimmediate = { '+stem+'_finish_network = yes }')
        decisions[tag]=block(stem+'_repair_network','icon = ac_up_sns_programme\nallowed = { tag = '+tag+' original_tag = '+tag+' }\nvisible = { ac_release_maintenance_active = yes NOT = { has_global_flag = '+done+' } }\navailable = { '+stem+'_can_repair_network = yes }\ncost = 0\ncomplete_effect = { '+stem+'_start_network = yes }\nai_will_do = { base = 1 }')+block(stem+'_cancel_network','icon = ac_up_sns_programme\nallowed = { tag = '+tag+' original_tag = '+tag+' }\nvisible = { has_country_flag = '+active+' }\ncost = 0\ncomplete_effect = { '+stem+'_cancel_network = yes }\nai_will_do = { base = 0 }')
        cancels[tag]=block('if','limit = { tag = '+tag+' original_tag = '+tag+' has_country_flag = '+active+' OR = { has_capitulated = yes '+stem+'_network_target_valid = no } }\n'+stem+'_cancel_network = yes')
        loc.extend([(stem+'_repair_network','Restore owned domestic connections'),(stem+'_repair_network_desc','Spend 50 political power and 0.02b (20 FU in legacy; political cost only with fiscal rules disabled) to add missing level 1 land connections after 90 days, once. Requires an exact documented release footprint and current control of every route province. Existing rail levels and receiving ports are preserved. No link crosses water; detached components rely on their existing ports and convoys. Loss of territory or control interrupts the project without refund. Unknown release shapes require normal manual construction.'),(stem+'_cancel_network','Cancel domestic connection work'),(stem+'_cancel_network_desc','Stop this funded project without a refund; a 30-day cooldown applies.')])
    return dict(effects=effects,triggers=triggers,events=events,decisions=decisions,loc=loc,cancels=cancels)
