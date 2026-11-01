"""Bounded release maintenance; no new combat roster or invented activation.

Funded building projects recheck current territory and slots. Recipe certification
does not promise unallocated production capacity. Initial registration grants only a
small transport reserve and templates to genuinely future releases. Future
workshops/civilian capacity cost PP, public-owner money and90days, once each.
No resource deposits, manpower, cores, financial stocks or borders are minted.
"""
import argparse,json,sys
from pathlib import Path
from itertools import product
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(ROOT/'tools/usea_expansion'),str(ROOT/'tools/world_starts')]
from script import parse,get,render
from technical import Engine
from capabilities import COMMON_TECH,equipment_for,design_for
import network

TAGS=('AWW','REC','REL','SBK','SER','SHI','TER')
ROLES={'rifles':('infantry_equipment_1','Infantry replacements'),
       'support':('support_equipment_1','Engineer and support stores'),
       'artillery':('artillery_equipment_1','Artillery replacements'),
       'trucks':('motorized_equipment_1','Truck replacements'),
       'trains':('train_equipment_1','Rail maintenance'),
       'fighter':('fighter','Fighter replacements'),'cas':('cas','Air support replacements'),
       'convoy':('convoy','Convoy replacements'),'escort':('destroyer','Escort replacements'),
       'submarine':('submarine','Submarine replacements')}
NAVAL={'convoy','escort','submarine'}
def block(name,body):return name+' = {\n'+'\n'.join(('\t'+line.rstrip() if line.strip() else '') for line in body.splitlines())+'\n}\n'
def flag(tag,suffix):return 'ac_release_'+tag+'_'+suffix
def exact(tag):return 'tag = '+tag+' original_tag = '+tag

def contract(reference=None):
    path=HERE/'physical_contract.json'
    if reference is None:return json.loads(path.read_text())
    engine=Engine(reference);cases={}
    for bba,mtg in product((False,True),repeat=2):
        roles={}
        for role,(kind,label) in ROLES.items():
            equipment=equipment_for(kind,bba,mtg);design=design_for(kind,bba,mtg)
            modules=design['modules'] if design else {};tech={engine.equipment_tech(equipment)}-{None}
            tech.update(engine.module_tech(module) for module in modules.values())
            if design:engine.design_slots(equipment,modules)
            roles[role]=dict(equipment=equipment,modules=modules,technologies=sorted(tech),stats=engine.stats(equipment,modules.values()),label=label)
        for tech in COMMON_TECH:
            if tech not in engine.tech:raise ValueError('Undefined maintenance technology: '+tech)
            engine.record(engine.tech_files[tech])
        cases[f'bba{int(bba)}_mtg{int(mtg)}']=roles
    return dict(schema=1,cases=cases,common_technologies=COMMON_TECH,
        networks=network.capture(json.loads((HERE/'intake.json').read_text())),
        primary_sources_sha256=dict(sorted(engine.used.items())),transport_reserve={'train_equipment_1':2,'motorized_equipment_1':12,'convoy_1':6},
        classification='Provisional maintenance calibration; no canonical equipment/model/deposit claim.',
        source_limits='Replacement queues require current available resources and industry; no starting import contract, operating aircraft or stored hulls are invented. Templates alone create no personnel. Existing transferred mixed forces can retain uncovered roles; see release worksheet and player production rotation.',
        efficiency='Preserves installed history/OOB50 convention; standalone effect documentation shows0.1. Native interpretation remains pending.')

def case_limit(bba,mtg):return ('has_dlc = "By Blood Alone"' if bba else 'NOT = { has_dlc = "By Blood Alone" }')+'\n'+('has_dlc = "Man the Guns"' if mtg else 'NOT = { has_dlc = "Man the Guns" }')
def decision_presentation(text):
    """Expose plain-language costs/requirements, not private receipt flags."""
    tree=parse(text)
    for _,_,category in tree:
        for ident,_,body in category:
            kind=('maintenance' if ident.endswith('_maintenance_access') else 'certify' if '_certify_' in ident else 'queue' if '_queue_' in ident else 'develop' if '_develop_' in ident else 'network' if ident.endswith('_repair_network') else 'cancel' if '_cancel_' in ident else None)
            if kind is None:raise ValueError('Unreviewed release decision presentation: '+ident)
            for node in body:
                if node[0]=='available':node[2]=[['custom_trigger_tooltip','=',[['tooltip','=','ac_release_'+kind+'_requirements_tt']]+node[2]]]
                elif node[0]=='complete_effect':node[2]=[['custom_effect_tooltip','=','ac_release_'+kind+'_effect_tt'],['hidden_effect','=',node[2]]]
    return render(tree)

def outputs(data=None):
    data=data or contract();intake=json.loads((HERE/'intake.json').read_text());out={};effects='';triggers='';decisions='';ai='';events='add_namespace = ac_release\n';loc=[]
    networks=network.outputs(data['networks']);effects+=networks['effects'];triggers+=networks['triggers'];events+=networks['events'];loc+=networks['loc']
    base='ac_release_exact_country = yes has_country_flag = ac_release_administration_registered has_capitulated = no ac_release_owned_capital = yes'
    triggers+=block('ac_release_maintenance_active',base+'\nhas_country_flag = ac_release_maintenance_registered')
    triggers+=block('ac_release_can_invest',base+'\npolitical_power >= 100 ac_econ_can_fund_release_project = yes NOT = { has_country_flag = ac_release_project_active } NOT = { has_country_flag = ac_release_project_cooldown }\ncapital_scope = { is_core_of = PREV is_fully_controlled_by = PREV free_building_slots = { building = industrial_complex size > 0 } }')
    # Retired compatibility API. Total factories minus historical purchases was
    # never an observation of current Production allocation. Existing counters
    # remain inert serialized history; do not reset or reuse them as reservations.
    effects+=block('ac_release_quote_maintenance_capacity','custom_effect_tooltip = ac_release_manual_production_tt')
    for tag in TAGS:
        stem='ac_release_'+tag;country=intake['countries'][tag]
        prepare=block('if','limit = { '+exact(tag)+' has_capitulated = no any_owned_state = { NOT = { state = 171 } } ac_release_owned_capital = yes NOT = { has_global_flag = '+flag(tag,'maintenance_registered')+' } }\n'+
            block('set_technology','\n'.join(tech+' = 1' for tech in data['common_technologies']))+
            f'load_oob = "{tag}_release_templates"\nset_global_flag = {flag(tag,"maintenance_registered")}')
        prepare+=block('if','limit = { '+exact(tag)+' has_global_flag = '+flag(tag,'maintenance_registered')+' }\nset_country_flag = ac_release_maintenance_registered')
        effects+=block(stem+'_prepare_maintenance',prepare)
        kit='limit = { '+exact(tag)+' has_capitulated = no has_global_flag = '+flag(tag,'was_absent')+' ac_release_owned_capital = yes any_owned_state = { NOT = { state = 171 } } NOT = { has_global_flag = '+flag(tag,'transport_delivered')+' } NOT = { has_global_flag = '+flag(tag,'adopted')+' } NOT = { has_global_flag = '+flag(tag,'annexed')+' } }\n'
        for equipment,amount in data['transport_reserve'].items():kit+=block('add_equipment_to_stockpile',f'type = {equipment}\namount = {amount}\nproducer = {tag}')
        kit+='set_global_flag = '+flag(tag,'transport_delivered')
        effects+=block(stem+'_deliver_transport_reserve',block('if',kit))
        registration=stem+'_prepare_maintenance = yes\n'+stem+'_deliver_transport_reserve = yes'
        # Recruit only established definitions; never change a ruling party or
        # promote a different person over an already implemented leader.
        for ident in country['identities']:registration+= '\n'+block('if','limit = { NOT = { has_character = '+ident+' } NOT = { any_country = { has_character = '+ident+' } } }\nrecruit_character = '+ident)
        # The existing office is an institutional representation, not a named
        # person's invented ideological conversion. Generic puppet releases
        # may adopt the master's ruling party; give that same office a role
        # only on its first new registration, preserving named identities.
        offices=[ident for ident in country['identities'] if ident.endswith('_ac_government_office')]
        subtypes={'democratic':'centrism','communism':'socialism','fascism':'fascism_ideology','neutrality':'centrism_na','monarchism':'constitutional_monarchy'}
        inherited=next((row['party'] for row in json.loads((ROOT/'tools/usea_expansion/leaders.json').read_text()) if row['tag']==tag),None)
        for ident in offices:
            for group,subtype in subtypes.items():
                if group==inherited:continue
                registration+='\n'+block('if','limit = { has_government = '+group+' has_character = '+ident+' }\n'+block('add_country_leader_role','character = '+ident+'\npromote_leader = yes\n'+block('country_leader','ideology = '+subtype+'\nexpire = "2066.1.1.1"\ntraits = { }\ndesc = '+ident+'_desc')))
        if tag in ('AWW','REC','SHI'):registration+='\n'+stem+'_ensure_ruling_office = yes'
        effects+=block(stem+'_physical_registration',block('if','limit = { '+exact(tag)+' has_capitulated = no has_global_flag = '+flag(tag,'was_absent')+' NOT = { has_global_flag = '+flag(tag,'adopted')+' } NOT = { has_global_flag = '+flag(tag,'annexed')+' } NOT = { has_global_flag = '+flag(tag,'physical_registered')+' } any_owned_state = { NOT = { state = 171 } } ac_release_owned_capital = yes }\n'+registration+'\nset_global_flag = '+flag(tag,'physical_registered')))
        out[f'history/units/{tag}_release_templates.txt']=block('division_template',f'name = "{tag} Territorial Infantry"\ndivision_names_group = {tag}_RELEASE_INF\n'+block('regiments','\n'.join('infantry = { x = '+str(x)+' y = '+str(y)+' }' for x in range(2) for y in range(2))))
        out[f'history/units/{tag}_release_templates.txt']+=block('division_template',f'name = "{tag} Local Security Detachment"\ndivision_names_group = {tag}_RELEASE_INF\n'+block('regiments','infantry = { x = 0 y = 0 }\ninfantry = { x = 0 y = 1 }'))
        out[f'common/units/names_divisions/{tag}_release_foundation.txt']=block(tag+'_RELEASE_INF',f'name = "Territorial Infantry"\nfor_countries = {{ {tag} }}\ncan_use = {{ always = yes }}\ndivision_types = {{ "infantry" }}\nfallback_name = "%d Territorial Infantry"')
        # No positive upgrade priority converts the inherited birth/transfer
        # army into this smaller optional future-recruitment template.
        target=block(tag+'_release_territorial_target','upgrade_prio = { factor = 0 }\n'+block('target_template',block('regiments','infantry = 4')))
        out[f'common/ai_templates/{tag}_release_foundation.txt']=block(tag+'_release_territorial',f'available_for = {{ {tag} }}\nrole = {tag}_release_territorial\nupgrade_prio = {{ factor = 0 }}\n'+target)
        decision_rows=''
        # Adopted saves receive no kit/template replay automatically. They can
        # deliberately purchase current maintenance access as future content.
        decision_rows+=block(stem+'_maintenance_access','icon = '+icon()+'\nallowed = { '+exact(tag)+' }\nvisible = { '+base+' NOT = { has_country_flag = ac_release_maintenance_registered } }\navailable = { political_power >= 25 }\ncost = 0\ncomplete_effect = { if = { limit = { '+base+' political_power >= 25 NOT = { has_country_flag = ac_release_maintenance_registered } } add_political_power = -25 '+stem+'_prepare_maintenance = yes } }\nai_will_do = { base = 1 }')
        loc.extend([(stem+'_maintenance_access','Register current maintenance'),(stem+'_maintenance_access_desc','Adopt maintenance templates and existing technical support. Costs 25 political power. Existing saves receive no transport reserve, army, aircraft, ship or historical reward from this action.')])
        for role,(_,label) in ROLES.items():
            licenses='';unlicensed=[]
            for bba,mtg in product((False,True),repeat=2):
                row=data['cases'][f'bba{int(bba)}_mtg{int(mtg)}'][role]
                licensed=flag(tag,'licensed_'+role+f'_bba{int(bba)}_mtg{int(mtg)}')
                licensing=case_limit(bba,mtg)+' NOT = { has_global_flag = '+licensed+' }';unlicensed.append(block('AND',licensing))
                code=block('set_technology','\n'.join(t+' = 1' for t in row['technologies']))
                if row['modules']:code+=block('create_equipment_variant',f'name = "{tag} Release {role}"\ntype = {row["equipment"]}\n'+block('modules','\n'.join(k+' = '+v for k,v in row['modules'].items())))
                licenses+=block('if',block('limit',licensing)+code+'set_global_flag = '+licensed)
            effects+=block(stem+'_license_'+role,block('if','limit = { '+exact(tag)+' ac_release_maintenance_active = yes }\n'+licenses))
            triggers+=block(stem+'_can_certify_'+role,exact(tag)+' ac_release_maintenance_active = yes political_power >= 5\n'+block('OR',''.join(unlicensed)))
            effects+=block(stem+'_certify_'+role,block('if','limit = { '+stem+'_can_certify_'+role+' = yes }\n'+stem+'_license_'+role+' = yes\nadd_political_power = -5'))
            decision_rows+=block(stem+'_certify_'+role,'icon = '+icon()+'\nallowed = { '+exact(tag)+' }\nvisible = { ac_release_maintenance_active = yes '+block('OR',''.join(unlicensed))+' }\navailable = { '+stem+'_can_certify_'+role+' = yes }\ncost = 0\ncomplete_effect = { '+stem+'_certify_'+role+' = yes }\nai_will_do = { base = 0 }')
            loc.extend([(stem+'_certify_'+role,'Certify '+label.lower()),(stem+'_certify_'+role+'_desc','Spend 5 political power to prepare the selected DLC technical recipe. Assign or rotate factories and dockyards in the Production screen afterward. Check materials, imports and fuel before manufacturing. Certification grants no production line, industry, resources, equipment or personnel and is once per selected technical configuration.')])
            # Preserve stable IDs and historical receipts without consuming them.
            # Even a stale/direct completion performs no purchase or mutation.
            triggers+=block(stem+'_can_queue_'+role,'always = no')
            effects+=block(stem+'_queue_'+role,'custom_effect_tooltip = ac_release_manual_production_tt')
            decision_rows+=block(stem+'_queue_'+role,'icon = '+icon()+'\nallowed = { '+exact(tag)+' }\nvisible = { always = no }\navailable = { always = no }\ncost = 0\ncomplete_effect = { '+stem+'_queue_'+role+' = yes }\nai_will_do = { base = 0 }')
            loc.extend([(stem+'_queue_'+role,label),(stem+'_queue_'+role+'_desc','Use recipe certification and assign factories or dockyards in the Production screen. This retired action changes no existing line and charges no political power.')])
        for index,(project,building,title) in enumerate((('civilian','industrial_complex','Develop a civilian workshop'),('military','arms_factory','Develop a maintenance arsenal'))):
            receipt=flag(tag,project+'_built');target=flag(tag,project+'_target');active=flag(tag,project+'_active');wait=flag(tag,project+'_waiting');event=f'ac_release.{100+TAGS.index(tag)*2+index}'
            can=exact(tag)+' ac_release_can_invest = yes NOT = { has_global_flag = '+receipt+' }'
            effects+=block(stem+'_start_'+project,block('if','limit = { '+can+' }\nac_econ_try_fund_release_project = yes\n'+block('if','limit = { has_country_flag = ac_econ_release_project_funded }\nadd_political_power = -100\ncapital_scope = { set_state_flag = '+target+' }\nset_country_flag = '+active+'\nset_country_flag = ac_release_project_active\nset_country_flag = { flag = '+wait+' days = 90 }\ncountry_event = { id = '+event+' days = 90 }')))
            valid='any_owned_state = { has_state_flag = '+target+' is_core_of = '+tag+' is_fully_controlled_by = '+tag+' free_building_slots = { building = '+building+' size > 0 } }'
            gate=exact(tag)+' has_country_flag = '+active+' NOT = { has_country_flag = '+wait+' } NOT = { has_global_flag = '+receipt+' } has_capitulated = no '+valid
            finish=block('if','limit = { '+gate+' }\nevery_owned_state = { limit = { has_state_flag = '+target+' is_core_of = '+tag+' is_fully_controlled_by = '+tag+' } add_building_construction = { type = '+building+' level = 1 instant_build = yes } }\nset_global_flag = '+receipt)
            cleanup='clr_country_flag = '+active+'\nclr_country_flag = '+wait+'\nclr_country_flag = ac_release_project_active\nset_country_flag = { flag = ac_release_project_cooldown days = 30 }\nevery_state = { limit = { has_state_flag = '+target+' } clr_state_flag = '+target+' }'
            effects+=block(stem+'_finish_'+project,block('if','limit = { has_country_flag = '+active+' NOT = { has_country_flag = '+wait+' } }\n'+finish+cleanup))
            effects+=block(stem+'_cancel_'+project,block('if','limit = { has_country_flag = '+active+' }\n'+cleanup))
            events+=block('country_event','id = '+event+'\nhidden = yes\nis_triggered_only = yes\nimmediate = { '+stem+'_finish_'+project+' = yes }')
            decision_rows+=block(stem+'_develop_'+project,'icon = '+icon()+'\nallowed = { '+exact(tag)+' }\nvisible = { '+base+' NOT = { has_global_flag = '+receipt+' } }\navailable = { '+can+' }\ncost = 0\ncomplete_effect = { '+stem+'_start_'+project+' = yes }\nai_will_do = { base = 1 }')
            decision_rows+=block(stem+'_cancel_'+project,'icon = '+icon()+'\nallowed = { '+exact(tag)+' }\nvisible = { has_country_flag = '+active+' }\ncost = 0\ncomplete_effect = { '+stem+'_cancel_'+project+' = yes }\nai_will_do = { base = 0 }')
            loc.extend([(stem+'_develop_'+project,title),(stem+'_develop_'+project+'_desc','Fund one additional '+('civilian factory' if project=='civilian' else 'military factory')+' in the current controlled core capital. Costs 100 political power and 0.02b in full economy mode or 20 FU in legacy mode; fiscal-disabled campaigns pay the political cost. Takes 90 days. One successful project of each type per country. Loss of control, annexation, capitulation or lost slots can interrupt it; spent funds are not refunded. No cores, population, deposits or financial balances are granted.'),(stem+'_cancel_'+project,'Cancel '+title.lower()),(stem+'_cancel_'+project+'_desc','Stop this funded project. Costs already spent are not refunded. A 30-day cooldown applies before another development project.')])
        decisions+=block(stem+'_maintenance',(decision_rows+networks['decisions'][tag]).replace('ac_up_sns_programme','ac_release_'+tag))
        loc.extend([(stem+'_maintenance','Release administration and maintenance'),(stem+'_maintenance_desc','Current capacity determines what this government can support. Baseline transport stock is a once-only future-release grant:2 trains,12 trucks and6 convoys; existing saves receive none. Paid projects do not change territorial settlements or cores. Fuel imports, reinforcement deficits and manual production rotation remain visible responsibilities. AWW and non-core treaty governments retain their inherited recruitment and capacity limits.')])
        allowed='allowed = { '+exact(tag)+' }\nenable = { ac_release_maintenance_active = yes }\nabort_when_not_enabled = yes\n'
        ai+=block(stem+'_sustainment',allowed+block('ai_strategy','type = equipment_production_factor\nid = infantry\nvalue = 25')+block('ai_strategy','type = build_building\nid = industrial_complex\nvalue = 30')+block('ai_strategy','type = ai_wanted_divisions_factor\nvalue = -80'))
        research=f'name = {stem}_research_name\ndesc = {stem}_research_desc\n'+allowed+block('research','industry = 15\ninfantry_tech = 15\nsupport_tech = 12\nelectronics = 5')+'weight = { factor = 1 }\n'
        out[f'common/ai_strategy_plans/{tag}_release_foundation.txt']=block(stem+'_research',research)
        loc.extend([(stem+'_research_name','Domestic maintenance priorities'),(stem+'_research_desc','Prioritize affordable industry, infantry, technical support and communications. Maintain existing formations; future recruitment still needs real manpower and equipment. Small governments should rotate limited air and naval production manually.')])
    explanations={
        'maintenance':('Requires an active administration, owned capital and25 political power.','Spend25 political power to prepare current maintenance templates and technical support. No historical stock or army grant is replayed.'),
        'certify':('Requires an active maintenance administration and5 political power. This recipe must not already be certified for the current technical configuration.','Spend5 political power to certify this recipe for manual production rotation; no line, equipment or personnel is granted.'),
        'queue':('Use recipe certification and the Production screen to assign or rotate factories and dockyards.','This retired action charges nothing and changes no production line, equipment, resources or historical receipt.'),
        'develop':('Requires100 political power, a controlled core capital with a free slot, no active project/cooldown and the current fiscal fee where enabled.','Pay100 political power and0.02b in full mode or20FU in legacy mode. Fund the selected90-day development project once; fiscal-disabled campaigns retain the political/time/territory costs.'),
        'network':('Requires50 political power, a documented controlled footprint with a missing connection, no active project/cooldown and the fiscal fee where enabled.','Pay50 political power and0.02b in full mode or20FU in legacy mode. Fund90-day owned domestic connections; existing rail levels and receiving ports are retained.'),
        'cancel':('Requires the selected project to be active.','Cancel without refunding spent costs. A30-day development cooldown applies.')}
    for kind,(required,effect) in explanations.items():
        for before,after in [('and0.02b','and 0.02b'),('or20FU','or 20 FU'),('selected90-day','selected 90-day'),('Fund90-day','Fund 90-day')]:required=required.replace(before,after);effect=effect.replace(before,after)
        import re
        required=re.sub(r'(?<=[A-Za-z])(?=\d)',' ',required);effect=re.sub(r'(?<=[A-Za-z])(?=\d)',' ',effect)
        loc.extend([('ac_release_'+kind+'_requirements_tt',required),('ac_release_'+kind+'_effect_tt',effect)])
    loc.append(('ac_release_manual_production_tt','Certify a recipe, then assign or rotate factories and dockyards in the Production screen. Check materials, imports and fuel before manufacturing. This action charges nothing and changes no existing line or historical receipt.'))
    out.update({'common/scripted_effects/ac_release_maintenance.txt':effects,'common/scripted_triggers/ac_release_maintenance.txt':triggers,'common/decisions/ac_release_maintenance.txt':decision_presentation(decisions),'common/ai_strategy/ac_release_maintenance.txt':ai,'events/ac_release_projects.txt':events,'common/decisions/categories/ac_release_maintenance.txt':''.join(block('ac_release_'+tag+'_maintenance','icon = ac_release_'+tag+'_maintenance\nallowed = { '+exact(tag)+' }\nvisible = { has_country_flag = ac_release_administration_registered }') for tag in TAGS),'localisation/english/ac_release_maintenance_l_english.yml':'l_english:\n'+'\n'.join(' '+key+':0 "'+value+'"' for key,value in loc)+'\n'})
    return out

def icon():return 'ac_up_sns_programme'

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args();data=contract(args.reference);path=HERE/'physical_contract.json';text=json.dumps(data,indent=2)+'\n'
    if args.check:
        if path.read_text()!=text:raise SystemExit('Release primary maintenance contract differs')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    for relative,text in outputs(data).items():
        path=MOD/relative;encoding='utf-8-sig' if relative.endswith('.yml') else 'utf-8'
        if args.check:
            if not path.exists() or path.read_text(encoding=encoding)!=text:raise SystemExit('Release maintenance output differs: '+relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding=encoding,newline='\n')
    print('Release maintenance outputs consistent' if args.check else 'Release maintenance generated')
