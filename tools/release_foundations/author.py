"""Legitimate-release lifecycle owner; no activation war or territorial invention.

The immutable event inputs retain existing IDs, settlements, force fractions,
leaders and narratives. Generated wrappers give their existing entry routes one
shared receipt. Unrelated top-level event text remains byte-stable.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import network

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get,render

TAGS=('AWW','REC','REL','SBK','SER','SHI','TER')
EVENT_FILES=('events/AWWNB.txt','events/Recta.txt','events/South_Belka.txt','events/Belka.txt')
BASE=HERE/'event_inputs.json'


def block(name,body):return name+' = {\n'+'\n'.join(('\t'+line.rstrip() if line.strip() else '') for line in body.splitlines())+'\n}\n'
def nodes(text):return parse(text)
def global_flag(tag,kind):return 'ac_release_'+tag+'_'+kind


def capture():
    if BASE.exists():raise ValueError('Event inputs already captured; do not replace the inherited baseline with candidate output')
    data=dict(schema=1,source_base='224c9ccb23f7745d1829b334c5f901c897e83c72',source_layer='Inherited mod provenance, not official chronology',
        files={relative:(MOD/relative).read_text(encoding='utf-8-sig') for relative in EVENT_FILES})
    BASE.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')


def replace_events(source,transforms):
    spans=[];cursor=0
    for match in re.finditer(r'(?m)^[ \t]*country_event[ \t]*=[ \t]*\{',source):
        if match.start()<cursor:continue
        depth=0;end=None
        for token in re.finditer(r'"(?:\\.|[^"\\])*"|\#[^\n]*|[{}]',source[match.end()-1:]):
            value=token.group()
            if value.startswith(('"','#')):continue
            depth+=1 if value=='{' else -1
            if depth==0:end=match.end()-1+token.end();break
        if end is None:raise ValueError('Unclosed inherited event')
        cursor=end;tree=parse(source[match.start():end]);ident=get(tree[0][2],'id').strip('"')
        if ident in transforms:
            before=tree[0][2];after=transforms[ident](copy.deepcopy(before))
            spans.append((match.start(),end,render([['country_event','=',after]])))
    if len(spans)!=len(transforms):raise ValueError('Missing or duplicate event-transform input')
    for begin,end,text in reversed(spans):source=source[:begin]+text.rstrip()+source[end:]
    parse(source)
    return source


def add_snapshot(body):
    immediate=get(body,'immediate')
    if immediate is None:body.append(['immediate','=',nodes('ac_release_snapshot_world = yes')])
    else:immediate.insert(0,['ac_release_snapshot_world','=','yes'])


def add_trigger(body,text):
    trigger=get(body,'trigger')
    if trigger is None:body.append(['trigger','=',nodes(text)])
    else:trigger.extend(nodes(text))


def guard_option(option,limit):
    fields=[n for n in option if n[0] in ('name','ai_chance','trigger','highlighted')]
    effects=[n for n in option if n[0] not in ('name','ai_chance','trigger','highlighted')]
    return fields+[['if','=',[['limit','=',nodes(limit)]]+effects]]


def guard_transfer(body,tag):
    for key,_,value in body:
        if not isinstance(value,list):continue
        if key=='BLK':
            for i,node in enumerate(value):
                if node[0]=='transfer_units_fraction' and get(node[2],'target')==tag:
                    value[i:i+1]=[['if','=',nodes('limit = { country_exists = '+tag+' NOT = { has_global_flag = '+global_flag(tag,'transfer_done')+' } }')+
                        [node]+nodes('set_global_flag = '+global_flag(tag,'transfer_done'))]]
        guard_transfer(value,tag)


def event_outputs():
    source=json.loads(BASE.read_text())['files'];out={}
    def aww_entry(body):
        add_snapshot(body);add_trigger(body,'NOT = { has_global_flag = '+global_flag('AWW','entry_begun')+' }')
        immediate=get(body,'immediate');snapshot=immediate[0]
        immediate[:]=[snapshot]+[['if','=',nodes('limit = { NOT = { has_global_flag = '+global_flag('AWW','adopted')+' } }')+immediate[1:]]]
        for node in body:
            if node[0]!='option':continue
            option=node[2];guard_transfer(option,'AWW')
            for key,_,value in option:
                if key=='AWW':value.extend(nodes('set_country_flag = { flag = ac_release_awaiting_legacy_army days = 7 }'))
            option.append(['set_global_flag','=',global_flag('AWW','entry_begun')])
            node[2]=guard_option(option,'NOT = { has_global_flag = '+global_flag('AWW','adopted')+' } NOT = { has_global_flag = '+global_flag('AWW','legacy_oob_done')+' } NOT = { has_global_flag = '+global_flag('AWW','entry_begun')+' }')
        return body
    def aww_army(body):
        gate='country_exists = AWW NOT = { has_global_flag = '+global_flag('AWW','legacy_oob_done')+' } NOT = { has_global_flag = '+global_flag('AWW','annexed')+' } AWW = { has_country_flag = ac_release_awaiting_legacy_army has_capitulated = no }'
        add_trigger(body,gate)
        for node in body:
            if node[0]!='option':continue
            node[2].extend(nodes('set_global_flag = '+global_flag('AWW','legacy_oob_done')+'\nAWW = { clr_country_flag = ac_release_awaiting_legacy_army ac_release_observe_country = yes }'))
            node[2]=guard_option(node[2],gate)
        return body
    out['events/AWWNB.txt']=replace_events(source['events/AWWNB.txt'],{'awwnb.1':aww_entry,'awwnb.2':aww_army})
    def recta(body):
        add_snapshot(body);gate='NOT = { has_global_flag = '+global_flag('REC','legacy_oob_done')+' } NOT = { has_global_flag = '+global_flag('REC','adopted')+' }';add_trigger(body,gate)
        for node in body:
            if node[0]=='option':
                node[2].extend(nodes('set_global_flag = '+global_flag('REC','legacy_oob_done')+'\nREC = { ac_release_observe_country = yes }'))
                node[2]=guard_option(node[2],gate)
        return body
    out['events/Recta.txt']=replace_events(source['events/Recta.txt'],{'recta.1':recta})
    def south(body):
        add_snapshot(body);gate='NOT = { has_global_flag = '+global_flag('SBK','entry_begun')+' } NOT = { has_global_flag = '+global_flag('SBK','adopted')+' }';add_trigger(body,gate)
        for node in body:
            if node[0]=='option':
                guard_transfer(node[2],'SBK');node[2].extend(nodes('set_global_flag = '+global_flag('SBK','entry_begun')+'\nSBK = { ac_release_observe_country = yes }'))
                node[2]=guard_option(node[2],gate)
        return body
    out['events/South_Belka.txt']=replace_events(source['events/South_Belka.txt'],{ident:south for ident in ('south_belka.2','south_belka.3','south_belka.4')})
    def treaty(body):
        add_snapshot(body)
        for node in body:
            if node[0]=='option':node[2].extend(nodes('REC = { ac_release_observe_country = yes }\nSBK = { ac_release_observe_country = yes }'))
        return body
    out['events/Belka.txt']=replace_events(source['events/Belka.txt'],{ident:treaty for ident in ('belka_dlp_war.101','belka_dlp_war.103')})
    return out


def runtime_outputs():
    intake=json.loads((HERE/'intake.json').read_text());fallback=intake['fallback_states'];by_state={row['state']:row for row in fallback}
    networks=network.outputs(json.loads((HERE/'physical_contract.json').read_text())['networks'])
    exact='OR = { '+' '.join('AND = { tag = '+tag+' original_tag = '+tag+' }' for tag in TAGS)+' }'
    triggers=block('ac_release_exact_country',exact)+block('ac_release_owned_capital','capital_scope = { is_owned_by = PREV }')
    effects='';snapshot='limit = { NOT = { has_global_flag = ac_release_registry_ready } }\n'
    for tag in TAGS:
        adopted='set_global_flag = '+global_flag(tag,'adopted')+'\n'+tag+' = { set_country_flag = ac_release_adopted_existing }\n'
        if tag in ('AWW','SBK'):adopted+='set_global_flag = '+global_flag(tag,'transfer_done')+'\nset_global_flag = '+global_flag(tag,'entry_begun')+'\n'
        if tag in ('AWW','REC'):adopted+='set_global_flag = '+global_flag(tag,'legacy_oob_done')+'\n'
        snapshot+=block('if','limit = { country_exists = '+tag+' }\n'+adopted+block('else','set_global_flag = '+global_flag(tag,'was_absent')))
    snapshot+='set_global_flag = ac_release_registry_ready\n';effects+=block('ac_release_snapshot_world',block('if',snapshot))
    for tag in TAGS:
        row=intake['countries'][tag];choices=[];historic=row['historical_capital']
        if historic in by_state:choices.append((f'owns_state = {historic}',by_state[historic]))
        seen=set()
        for case in row['known_cases']:
            ident=case['capital_state'];province=case['capital_province'];key=(tuple(case['states']),ident,province)
            if key in seen:continue
            seen.add(key);condition=' '.join('owns_state = '+str(i) for i in case['states'])+'\nall_owned_state = { OR = { '+' '.join('state = '+str(i) for i in case['states'])+' } }'
            choices.append((condition,dict(state=ident,capital_province=province)))
        choices.extend(('owns_state = '+str(candidate['state']),candidate) for candidate in fallback)
        code='clr_country_flag = ac_release_capital_selected\n'
        for index,(condition,candidate) in enumerate(choices):
            condition+='\ncontrols_province = '+str(candidate['capital_province'])
            code+=block('if' if index==0 else 'else_if',block('limit',condition)+f'set_capital = {{ state = {candidate["state"]} remember_old_capital = no }}\nset_country_flag = ac_release_capital_selected')
        effects+=block('ac_release_'+tag+'_select_owned_capital',code)
    observe='ac_release_snapshot_world = yes\n'
    annex='';interrupt='';cancel_all='';finish_due=''
    for tag in TAGS:
        scope='tag = '+tag+' original_tag = '+tag+' any_owned_state = { NOT = { state = 171 } }'
        capital='ac_release_'+tag+'_select_owned_capital = yes\n'
        after='ac_econ_adopt_release_account = yes\nac_pol_initialize = yes\nac_release_'+tag+'_physical_registration = yes\nset_country_flag = ac_release_administration_registered\nset_global_flag = '+global_flag(tag,'administration_registered')+'\n'
        if tag=='AWW':after+='set_global_flag = '+global_flag(tag,'legacy_oob_done')+'\nset_global_flag = '+global_flag(tag,'transfer_done')+'\nset_global_flag = '+global_flag(tag,'entry_begun')+'\n'
        if tag=='REC':after+='set_global_flag = '+global_flag(tag,'legacy_oob_done')+'\n'
        if tag=='SBK':after+='set_global_flag = '+global_flag(tag,'transfer_done')+'\nset_global_flag = '+global_flag(tag,'entry_begun')+'\n'
        eligible=scope+' NOT = { has_global_flag = '+global_flag(tag,'administration_registered')+' } NOT = { has_global_flag = '+global_flag(tag,'adopted')+' } has_global_flag = '+global_flag(tag,'was_absent')+' NOT = { has_capitulated = yes }'
        if tag=='AWW':eligible+=' NOT = { has_country_flag = ac_release_awaiting_legacy_army }'
        observe+=block('if',block('limit',eligible)+capital+block('if','limit = { has_country_flag = ac_release_capital_selected ac_release_owned_capital = yes }\n'+after))
        observe+=block('if','limit = { '+scope+' ac_release_owned_capital = no }\n'+capital)
        observe+=block('if','limit = { '+scope+' has_global_flag = '+global_flag(tag,'adopted')+' ac_release_owned_capital = yes }\nac_econ_adopt_release_account = yes\nac_pol_initialize = yes\nset_country_flag = ac_release_administration_registered\nset_global_flag = '+global_flag(tag,'administration_registered'))
        observe+=block('if','limit = { '+scope+' has_global_flag = '+global_flag(tag,'maintenance_registered')+' }\nac_release_'+tag+'_prepare_maintenance = yes')
        for project in ('civilian','military'):
            target=global_flag(tag,project+'_target')
            valid='any_owned_state = { has_state_flag = '+target+' is_core_of = '+tag+' is_fully_controlled_by = '+tag+' }'
            interrupt+=block('if','limit = { tag = '+tag+' original_tag = '+tag+' has_country_flag = '+global_flag(tag,project+'_active')+' OR = { has_capitulated = yes NOT = { '+valid+' } } }\nac_release_'+tag+'_cancel_'+project+' = yes')
        interrupt+=networks['cancels'][tag]
        cancel_all+=block('if','limit = { tag = '+tag+' original_tag = '+tag+' }\n'+'\n'.join('ac_release_'+tag+'_cancel_'+p+' = yes' for p in ('civilian','military','network')))
        finish_due+=block('if','limit = { tag = '+tag+' original_tag = '+tag+' has_country_flag = ac_release_project_active }\n'+'\n'.join('ac_release_'+tag+'_finish_'+p+' = yes' for p in ('civilian','military','network')))
        flags='set_global_flag = '+global_flag(tag,'annexed')+'\n'
        if tag in ('AWW','SBK'):flags+='set_global_flag = '+global_flag(tag,'transfer_done')+'\nset_global_flag = '+global_flag(tag,'entry_begun')+'\n'
        if tag in ('AWW','REC'):flags+='set_global_flag = '+global_flag(tag,'legacy_oob_done')+'\n'
        annex+=block('if','limit = { tag = '+tag+' original_tag = '+tag+' }\n'+block('if','limit = { NOT = { has_global_flag = ac_release_registry_ready } }\nset_global_flag = '+global_flag(tag,'adopted'))+flags+'clr_country_flag = ac_release_awaiting_legacy_army\nac_release_'+tag+'_cancel_civilian = yes\nac_release_'+tag+'_cancel_military = yes\nac_release_'+tag+'_cancel_network = yes')
    observe+='ac_release_interrupt_projects = yes\n'
    effects+=block('ac_release_observe_country',observe)+block('ac_release_record_annexation',annex)+block('ac_release_interrupt_projects',interrupt)+block('ac_release_cancel_all_projects',cancel_all)+block('ac_release_finish_due_projects',finish_due)
    actions='on_actions = {\n on_startup = { effect = { ac_release_snapshot_world = yes every_country = { limit = { ac_release_exact_country = yes } ac_release_observe_country = yes } } }\n on_monthly = { effect = { if = { limit = { ac_release_exact_country = yes } ac_release_observe_country = yes ac_release_finish_due_projects = yes } } }\n on_release_as_free = { effect = { ac_release_observe_country = yes } }\n on_release_as_puppet = { effect = { ac_release_observe_country = yes } }\n on_annex = { effect = { FROM = { ac_release_record_annexation = yes } } }\n on_state_control_changed = { effect = { FROM = { if = { limit = { has_country_flag = ac_release_project_active } ac_release_interrupt_projects = yes } } } }\n on_capitulation = { effect = { if = { limit = { has_country_flag = ac_release_project_active } ac_release_cancel_all_projects = yes } } }\n}\n'
    return {'common/scripted_triggers/ac_release_foundations.txt':triggers,'common/scripted_effects/ac_release_foundations.txt':effects,'common/on_actions/ac_release_foundations.txt':actions}


def outputs():return event_outputs()|runtime_outputs()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--capture-inputs',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.capture_inputs:capture()
    for relative,text in outputs().items():
        path=MOD/relative
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=text:raise SystemExit('Release lifecycle output differs: '+relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='\n')
    print('Release lifecycle generated' if not args.check else 'Release lifecycle consistent')
