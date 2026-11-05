"""Deterministic AC04/AC5 compiler. --check never writes; no native execution."""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from ac_campaigns.catalogue import NATIONS, OPERATIONS, PARTNERS
from ac_campaigns.imports import attach
from ac_campaigns.narrative import SCENES, NATIONAL, PARTNER_SCENES, PEACE
from content_waves.framework import block, guard

P = 'ac_camp'
PREFIX = 'common/'
TREE_PATHS = {'FAT':'ac_fsb_fat.txt','SBK':'ac_fsb_sbk.txt'}


def flag(key):
    return f'has_global_flag = {P}_{key}'


def terminal(op):
    results=('success','failed','cancelled','interrupted')+(('limited',) if op.key=='relief' else ())
    return 'OR = { '+ ' '.join(flag(op.key+'_'+s) for s in results)+' }'


def campaign_gate(op):
    if op.campaign == 'ucw':
        if op.key == 'megalith':
            return 'has_global_flag = ac_ucw_outcome_isaf_victory NOT = { has_global_flag = ac_ucw_megalith_destroyed }'
        return 'ac_ucw_war_running = yes'
    if op.campaign == 'cpw':
        return 'ac_cpw_course_open = yes ac_cpw_pair_at_war = yes'
    if op.campaign == 'aftermath':
        return 'ac_ucw_war_over = yes'
    if op.campaign == 'network':
        return 'ac_cpw_course_open = yes ac_cpw_pair_at_war = yes'
    if op.campaign == 'peace':
        return 'has_war = no'
    return 'always = yes'


def compile_content():
    effects, triggers, loc = {}, {}, {}
    ideas, focuses, events, categories, hooks = [], [], [], [], []
    decisions = defaultdict(list)
    inventory = []
    scene_rows = SCENES

    def text(key,value):
        if key in loc:
            raise ValueError('Duplicate localization '+key)
        loc[key] = value

    def idea(key,title,values):
        text(key,title)
        text(key+'_desc','A provisional campaign commitment. Its continuing benefit retains its administrative opportunity cost.')
        ideas.append(block(key,f'picture = {key}\nallowed = {{ always = no }}\n'+block('modifier',values)))

    def decision(tag,key,title,description,visible,available,action,ai=0):
        text(key,title); text(key+'_desc',description)
        body = f'icon = {key}\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ {visible} }}\navailable = {{ {available} }}\ncost = 0\n'
        body += block('complete_effect',action)+f'ai_will_do = {{ base = {ai} }}\n'
        decisions[f'{P}_{tag.lower()}'].append(block(key,body))

    def event(number,tag,title,body,gate,options,picture='medical',variants=None):
        key = f'{P}.{number}'
        text(key+'.t',title); text(key+'.desc',body)
        descriptions=''
        for i,variant in enumerate(variants or []):
            text(key+f'.desc.v{i}',variant['body'])
            descriptions+=block('desc',block('trigger',variant['gate'])+f'text = {key}.desc.v{i}')
        if variants:
            descriptions+=block('desc',block('trigger','NOT = { OR = { '+' '.join('AND = { '+v['gate']+' }' for v in variants)+' } }')+f'text = {key}.desc')
        else:descriptions=f'desc = {key}.desc\n'
        out = f'id = {key}\ntitle = {key}.t\n'+descriptions+f'picture = GFX_{P}_event_{picture}\nis_triggered_only = yes\n'+block('trigger',f'tag = {tag} original_tag = {tag}\n'+gate)
        for i,(label,condition,action) in enumerate(options):
            letter = chr(97+i); text(key+'.'+letter,label)
            out += block('option',f'name = {key}.{letter}\n'+block('trigger',condition)+f'ai_chance = {{ factor = {90 if i == 0 else 10} }}\n'+action)
        text(key+'.z','Close this old message.')
        out += block('option',f'name = {key}.z\n'+block('trigger','NOT = { OR = { '+ ' '.join('AND = { '+condition+' }' for _,condition,_ in options)+' } }'))
        events.append(block('country_event',out))
        return key

    participant = 'OR = { '+' '.join('AND = { tag = '+n.tag+' original_tag = '+n.tag+' }' for n in NATIONS)+' }'
    triggers[P+'_participant'] = participant
    triggers[P+'_eligible'] = f'{P}_participant = yes OR = {{ has_capitulated = no tag = SNS }} any_owned_state = {{ always = yes }}'
    triggers[P+'_can_pay'] = f'{P}_eligible = yes political_power >= 25 ac_pol_active = yes check_variable = {{ ac_pol_capacity >= 2 }} OR = {{ ac_econ_enabled = no AND = {{ ac_econ_ready = yes ac_econ_can_pay_programme = yes }} }}'
    effects[P+'_pay'] = f'clr_country_flag = {P}_paid\n'+guard(P+'_can_pay = yes',
        guard('ac_econ_enabled = no',f'set_country_flag = {P}_paid')+
        block('else', 'ac_econ_pay_programme = yes\n'+guard('OR = { ac_macro_ready = no has_country_flag = ac_macro_transaction_succeeded }',f'set_country_flag = {P}_paid'))+
        guard(f'has_country_flag = {P}_paid','add_political_power = -25\nset_temp_variable = { ac_pol_capacity_delta = -2 }\nac_pol_change_capacity = yes'))
    effects[P+'_initialize'] = guard(f'{P}_eligible = yes NOT = {{ has_country_flag = {P}_initialized }}',
        f'set_country_flag = {P}_initialized\nset_variable = {{ {P}_identity = THIS.id }}\n'+
        guard('OR = { AND = { tag = OSE date > 2010.11.28 } AND = { tag = ERU date > 2005.4.1 } }','set_country_flag = ac_camp_late_character_history'))
    effects[P+'_interrupt'] = guard(P+'_participant = yes', '\n'.join(
        guard(f'has_country_flag = {P}_{o.key}_active',f'clr_country_flag = {P}_{o.key}_active\nset_global_flag = {P}_{o.key}_interrupted\nclr_country_flag = {P}_busy') for o in OPERATIONS))

    # Four major branches per principal/Belka, one focused branch for each partner.
    for n in NATIONS:
        cat = f'{P}_{n.tag.lower()}'
        text(cat,n.name+' — campaign operations')
        text(cat+'_desc','Commit resources to preparation, conduct operations, and read the delivered scenes. Historical dates open opportunities; results depend on present conditions. All alternate routes and dialogue are authored gameplay.')
        categories.append(block(cat,f'icon = GFX_{cat}\nallowed = {{ tag = {n.tag} original_tag = {n.tag} }}\nvisible = {{ any_owned_state = {{ always = yes }} }}'))
        for lane,title in enumerate(n.lanes):
            stem=f'{n.tag}_camp_{lane}'
            policies=n.policies if isinstance(n.policies[0],str) else n.policies[lane]
            titles=(title,policies[0],policies[1],'Prepare: '+title,'Review the completed work','The standing account: '+title)
            for i,suffix in enumerate(('register','policy_a','policy_b','prepared','review','account')):
                ident=stem+'_'+suffix
                text(ident,titles[i])
                purpose = ('Open the campaign lane and its preparation record.',
                    'Choose the public or civil mandate and accept its continuing cost.',
                    'Choose the protected or command mandate and accept its continuing cost.',
                    'Authorize the corresponding paid operations; this focus does not complete them.',
                    'Require a real operation result or the recorded settlement; failed work remains reviewable.',
                    'Turn the selected mandate into a standing account without replaying its operations.')[i]
                text(ident+'_desc', title+'. '+purpose+'\n\n'+national_description(n,lane))
                body=f'id = {ident}\nicon = GFX_{ident}\nx = {100+lane*9+(-2 if i==1 else 2 if i==2 else 0)}\ny = {0 if i==0 else 1 if i<3 else i-1}\ncost = {1 if i in (3,4) else 5}\n'
                body+=block('allow_branch',f'tag = {n.tag} original_tag = {n.tag}')
                gate=f'{P}_eligible = yes date > {n.after}'
                if i:
                    req = 'register' if i in (1,2) else 'prepared' if i==4 else 'review' if i==5 else None
                    if req:body+=block('prerequisite','focus = '+stem+'_'+req)
                    else:body+=block('prerequisite','focus = '+stem+'_policy_a\nfocus = '+stem+'_policy_b')
                if i in (1,2):
                    body+=block('mutually_exclusive','focus = '+stem+('_policy_b' if i==1 else '_policy_a'))
                if i == 4:
                    relevant=[o for o in OPERATIONS if o.tag==n.tag and o.lane==lane]
                    closed=' has_global_flag = ac_ucw_war_averted has_global_flag = ac_ucw_outcome_isaf_victory has_global_flag = ac_ucw_outcome_erusean_victory has_global_flag = ac_ucw_outcome_stalemate' if n.tag in ('ERU','FCU','SNS','NPT','AMB','UGE','DEL') else ' has_global_flag = ac_cpw_prevented has_global_flag = ac_cpw_declaration_withheld has_global_flag = ac_cpw_ended' if n.tag in ('OSE','YUK') else ''
                    gate += ' OR = { '+' '.join(terminal(o) for o in relevant)+closed+' }'
                action=f'set_country_flag = {ident}\n'
                if i in (1,2):
                    spirit=ident+'_spirit'
                    benefit = 'stability_factor = 0.02\npolitical_power_factor = -0.01' if i==1 else 'planning_speed = 0.05\nconsumer_goods_factor = 0.005'
                    idea(spirit,titles[i],benefit)
                    action+='add_ideas = '+spirit+'\n'
                if i==5:action+='add_stability = 0.01\n'
                body+=block('available',gate)+block('completion_reward',guard(f'NOT = {{ has_country_flag = {ident} }}',action))+'ai_will_do = { factor = 5 }\n'
                focuses.append(block('shared_focus',body))
                inventory.append(dict(id=ident,tag=n.tag,lane=lane,purpose=purpose,source_layer='provisional gameplay',reference='tools/ac_campaigns/sources.json#fiction',status='implemented source; native pending'))

    # Operations have a paid start, maturation, finite deadline and immutable result.
    for oi,o in enumerate(OPERATIONS):
        stem=f'{P}_{o.key}'; prepared=f'{o.tag}_camp_{o.lane}_prepared'
        gate=f'{P}_eligible = yes tag = {o.tag} original_tag = {o.tag} has_country_flag = {prepared} date > {o.after} {campaign_gate(o)}'
        if o.previous:gate+=' '+flag(o.previous+'_success')
        if o.key in PARTNERS:gate+=f' country_exists = {PARTNERS[o.key]}'
        if o.key in PARTNERS:gate+=f' {PARTNERS[o.key]} = {{ has_capitulated = no is_subject = no NOT = {{ has_war_with = {o.tag} }} }}'
        if o.key=='maintenance':gate+=' NOT = { has_global_flag = ac_camp_battery_success }'
        if o.key=='rescue_cover':gate+=' date < 2010.11.29'
        if o.key in ('battery','engineers'):gate+=' has_global_flag = ac_ucw_stonehenge_seized NOT = { has_global_flag = ac_ucw_stonehenge_destroyed }'
        if o.key=='megalith':gate+=' has_global_flag = ac_ucw_megalith_active'
        if o.key=='liberation':gate+=' has_global_flag = ac_ucw_stonehenge_seized'
        if o.key=='arkbird':gate+=' has_global_flag = ac_cpw_arkbird_committed NOT = { has_global_flag = ac_cpw_arkbird_lost }'
        triggers[stem+'_context'] = gate
        payment_gate=(f'has_global_flag = ac_camp_clinic_sponsorship country_exists = FCU FCU = {{ {P}_can_pay = yes NOT = {{ has_war_with = SNS }} }}' if o.key=='relief' else P+'_can_pay = yes')
        start_extra=' NOT = { has_global_flag = ac_camp_witness_success } NOT = { has_global_flag = ac_camp_evidence_success }' if o.key=='seizure' else ''
        triggers[stem+'_can_start'] = gate+f' {o.condition} {payment_gate} NOT = {{ has_country_flag = {P}_busy }} NOT = {{ {terminal(o)} }}'+start_extra
        finish_context=f'{stem}_context = yes has_country_flag = {stem}_deadline {o.condition}'
        if o.key in PARTNERS:finish_context+=' '+flag(o.key+'_accepted')
        if o.key=='relief':finish_context+=' '+flag('clinic_civil_permission')+' '+flag('clinic_military_permission')
        if o.key=='seizure':finish_context+=' NOT = { '+flag('witness_success')+' } NOT = { '+flag('evidence_success')+' }'
        triggers[stem+'_can_finish'] = finish_context
        pay=('FCU = { '+P+'_pay = yes }' if o.key=='relief' else P+'_pay = yes')
        paid=('FCU = { has_country_flag = '+P+'_paid }' if o.key=='relief' else 'has_country_flag = '+P+'_paid')
        effects[stem+'_start'] = guard(stem+'_can_start = yes',pay+'\n'+guard(paid,
            f'set_country_flag = {P}_busy\nset_country_flag = {stem}_active\nset_country_flag = {{ flag = {stem}_waiting days = {o.days} }}\nset_country_flag = {{ flag = {stem}_deadline days = {o.days*3} }}\n'+
            (f'{PARTNERS[o.key]} = {{ country_event = {{ id = {P}.{2000+oi} days = 1 }} }}\n' if o.key in PARTNERS else '')))
        cleanup=f'clr_country_flag = {stem}_active\nclr_country_flag = {P}_busy\n'
        success=cleanup+f'set_global_flag = {stem}_success\nadd_timed_idea = {{ idea = {P}_operation_return days = 90 }}\n'
        if o.key in PARTNERS:
            support={
                'rearbase':'army_defence_factor = 0.02',
                'transport':'supply_consumption_factor = -0.02',
                'dispersal':'planning_speed = 0.04',
                'inspection':'political_power_factor = 0.02',
                'access':'supply_consumption_factor = -0.01',
                'sovereignty':'army_defence_factor = 0.01',
                'transit':'planning_speed = 0.02',
                'contribution':'stability_factor = 0.01'}[o.key]
            idea(stem+'_receiving_return',o.title+' — receiving commitment',support+'\nconsumer_goods_factor = 0.005')
            success+=f'{PARTNERS[o.key]} = {{ add_timed_idea = {{ idea = {stem}_receiving_return days = 90 }} }}\n'
        if o.key=='maintenance':success+=f'set_global_flag = {P}_yellow_four_airworthy\n'
        if o.key=='withdrawal':success+=f'set_global_flag = {P}_yellow_thirteen_preserved\n'
        if o.key=='rescue_cover':success+=f'set_global_flag = {P}_rescue_coverage_ready\n'
        if o.key=='seizure':success+=f'set_global_flag = {P}_network_strategic_access\n'
        if o.key=='seizure':success+='OSE = { add_timed_idea = { idea = ac_camp_compromised_orders days = 90 } }\nYUK = { add_timed_idea = { idea = ac_camp_compromised_orders days = 90 } }\n'
        if o.key in ('witness','evidence'):success+='ac_camp_contain_network = yes\n'
        if o.key=='battery':success+='set_country_flag = ac_camp_battery_choice_pending\ncountry_event = { id = ac_camp.2400 days = 1 }\n'
        if o.key=='megalith':success+='ac_ucw_destroy_megalith = yes\n'
        effects[stem+'_finish'] = guard(f'has_country_flag = {stem}_active NOT = {{ has_country_flag = {stem}_waiting }} {stem}_can_finish = yes',success)
        effects[stem+'_fail'] = guard(f'has_country_flag = {stem}_active',cleanup+f'set_global_flag = {stem}_failed\n')
        effects[stem+'_cancel'] = guard(f'has_country_flag = {stem}_active',cleanup+f'set_global_flag = {stem}_cancelled\n')
        effects[stem+'_tick'] = guard(f'has_country_flag = {stem}_active',
            guard(f'{stem}_context = no',cleanup+f'set_global_flag = {stem}_interrupted')+
            block('else_if',block('limit',f'NOT = {{ has_country_flag = {stem}_waiting }} {stem}_can_finish = yes')+stem+'_finish = yes')+
            (block('else_if',block('limit',f'NOT = {{ has_country_flag = {stem}_deadline }} has_global_flag = ac_camp_clinic_civil_permission NOT = {{ has_global_flag = ac_camp_clinic_military_permission }}')+cleanup+'set_global_flag = ac_camp_relief_limited') if o.key=='relief' else '')+
            block('else_if',block('limit',f'NOT = {{ has_country_flag = {stem}_deadline }}')+stem+'_fail = yes'))
        visible=f'date > {o.after} has_country_flag = {prepared}'
        payer='FCU sponsors this defined operation after its explicit consent. ' if o.key=='relief' else ''
        decision(o.tag,stem+'_start',o.title,o.objective+'\n\n'+payer+'Costs 25 political power, 2 institutional capacity and the shared programme fee when enabled. Preparation takes '+str(o.days)+' days; the deadline is '+str(o.days*3)+' days. Failure and cancellation forfeit paid costs.',visible,stem+'_can_start = yes',stem+'_start = yes',5)
        decision(o.tag,stem+'_cancel','Cancel: '+o.title,'Close the current operation. Paid costs remain spent.',f'has_country_flag = {stem}_active','always = yes',stem+'_cancel = yes')
        for result in ('success','failed','cancelled','interrupted')+(('limited',) if o.key=='relief' else ()):
            decision(o.tag,stem+'_record_'+result,o.title+' — '+result,'Read-only operation result. It grants no payment, completion or reward.',flag(o.key+'_'+result),'always = yes','')
        if o.key in PARTNERS:
            receiver=PARTNERS[o.key]
            pending=f'country_exists = {o.tag} {o.tag} = {{ has_country_flag = {stem}_active has_country_flag = {stem}_deadline }} NOT = {{ has_war_with = {o.tag} }} has_capitulated = no is_subject = no'
            event(2000+oi,receiver,'A bounded offer from '+next(n.name for n in NATIONS if n.tag==o.tag),
                partner_scene(o),'always = yes',
                [('Accept this defined commitment.',pending,f'set_global_flag = {stem}_accepted'),
                 ('Decline the offer.',pending,f'{o.tag} = {{ {stem}_cancel = yes }}')],o.glyph)

    idea(P+'_operation_return','A completed operational commitment','planning_speed = 0.03\nconsumer_goods_factor = 0.005')
    idea(P+'_garrison_limits','An enforceable inspection limit','stability_factor = 0.01\npolitical_power_factor = -0.01')
    idea(P+'_retained_correspondence','Retained correspondence files','planning_speed = 0.03\nconsumer_goods_factor = 0.005')
    idea(P+'_observation_assignment','A reserved observation commitment','planning_speed = -0.03\nconsumer_goods_factor = 0.005')
    idea(P+'_compromised_orders','A compromised command channel','planning_speed = -0.05\nconsumer_goods_factor = 0.005')
    effects[P+'_contain_network']=guard('country_exists = OSE','OSE = { remove_ideas = ac_camp_compromised_orders }')+guard('country_exists = YUK','YUK = { remove_ideas = ac_camp_compromised_orders }')
    idea(P+'_recaptured_battery','A secured engineering site','army_defence_factor = 0.02\nconsumer_goods_factor = 0.005')
    for choice in ('disabled','recaptured','destroyed'):
        action='set_global_flag = ac_camp_battery_disposition\nclr_country_flag = ac_camp_battery_choice_pending\n'
        if choice=='destroyed':action+='ac_ucw_destroy_stonehenge = yes\n'
        else:
            action+=f'set_global_flag = ac_ucw_stonehenge_{choice}\nset_global_flag = ac_ucw_stage_stonehenge\nremove_ideas = ac_ucw_under_stonehenge\nremove_ideas = ac_sp_stonehenge_battery\nERU = {{ remove_ideas = ac_ucw_stonehenge_railguns }}\nSNS = {{ remove_ideas = ac_ucw_stonehenge_garrison }}\n'
            if choice=='recaptured':action+='add_ideas = ac_camp_recaptured_battery\n'
        condition='tag = FCU original_tag = FCU has_global_flag = ac_camp_battery_success has_country_flag = ac_camp_battery_choice_pending NOT = { has_global_flag = ac_camp_battery_disposition }'
        if choice=='recaptured':condition+=' 310 = { is_controlled_by = SNS }'
        effects['ac_ucw_campaign_battery_'+choice]=guard(condition,action)
    event(2400,'FCU','What to leave standing',
        'The engineering return describes a site that can no longer be treated as an inevitable part of the landscape. The strike preparations are complete. The command must now decide what it intends to leave behind.\n\nDisabling the system preserves a damaged site whose surviving machinery remains a future responsibility. Destroying it follows the historical assault and removes the battery as a strategic threat. Securing it intact requires the site actually to be under San Salvacion\'s control; no entry in the operation file can supply that possession.\n\nThe engineers have attached separate recommendations. One concerns the immediate air campaign. Another concerns the people who would have to live beside what remains when the campaign is over. The officer receiving the return puts both on the table. Neither can be answered by quietly substituting a different plan after the decision has been made.',
        'has_global_flag = ac_camp_battery_success',[
        ('Destroy the battery.','has_country_flag = ac_camp_battery_choice_pending','ac_ucw_campaign_battery_destroyed = yes'),
        ('Disable it and preserve the site.','has_country_flag = ac_camp_battery_choice_pending','ac_ucw_campaign_battery_disabled = yes'),
        ('Secure the intact engineering site.','has_country_flag = ac_camp_battery_choice_pending 310 = { is_controlled_by = SNS }','ac_ucw_campaign_battery_recaptured = yes'),
        ('The disposition has already been recorded.','NOT = { has_country_flag = ac_camp_battery_choice_pending }','')],'radar')

    # Delivered scenes are frozen: separate dispatched variant flags select desc,
    # archives reuse those flags, and all replies recheck the finite pending window.
    for row in scene_rows:
        num,tag=row['id'],row['tag']; stem=f'{P}_scene_{num}'
        gate=row['gate']
        variants=[dict(gate=f'has_country_flag = {stem}_variant_{i}',body=row['body']+'\n\n'+v['body']) for i,v in enumerate(row.get('variants',[]))]
        capture=''.join(guard(f'has_country_flag = {v["choice"]}',f'set_country_flag = {stem}_variant_{i}') for i,v in enumerate(row.get('variants',[])))
        dispatch=guard(f'{P}_eligible = yes tag = {tag} original_tag = {tag} {gate} NOT = {{ has_country_flag = {stem}_delivered }} NOT = {{ has_country_flag = {P}_scene_wait }}',
            f'set_country_flag = {stem}_delivered\n'+capture+f'set_country_flag = {{ flag = {stem}_pending days = 30 }}\nset_country_flag = {{ flag = {P}_scene_wait days = 7 }}\ncountry_event = {{ id = {P}.{num} days = 1 }}\n')
        effects[stem+'_dispatch']=dispatch
        options=[]
        for i,option in enumerate(row['options']):
            effect=f'clr_country_flag = {stem}_pending\nset_country_flag = {stem}_resolved\nset_country_flag = {stem}_choice_{i}\n'+option.get('effect','')
            options.append((option['label'],(f'has_country_flag = {stem}_pending {P}_eligible = yes '+option.get('gate','')).rstrip(),effect))
        event(num,tag,row['title'],row['body'],f'has_country_flag = {stem}_delivered',options,row.get('glyph','document'),variants)
        archive=3000+num
        archive_options=[('Return to the journal.','always = yes','')]
        archive_options += [('Recorded choice: '+option['label'],f'has_country_flag = {stem}_choice_{i}','') for i,option in enumerate(row['options'])]
        archive_options += [('This message was left unanswered.',f'has_country_flag = {stem}_unanswered','')]
        event(archive,tag,row['title']+' — archive',row['body'],f'has_country_flag = {stem}_delivered',archive_options,row.get('glyph','document'),variants)
        decision(tag,stem+'_archive',row['title'],'Read the delivered scene. This is a read-only archive.',f'has_country_flag = {stem}_delivered','always = yes',f'country_event = {{ id = {P}.{archive} days = 1 }}')
        effects[stem+'_expire']=guard(f'has_country_flag = {stem}_delivered NOT = {{ has_country_flag = {stem}_pending }} NOT = {{ has_country_flag = {stem}_resolved }}',f'set_country_flag = {stem}_unanswered\nset_country_flag = {stem}_resolved')

    for n in NATIONS:
        tick=P+'_initialize = yes\n'+guard(P+'_eligible = no',P+'_interrupt = yes')
        tick+=P+'_character_tick = yes\n'+guard(P+'_eligible = yes','\n'.join(f'{P}_{o.key}_tick = yes' for o in OPERATIONS if o.tag==n.tag)+'\n'+
            '\n'.join(f'{P}_scene_{s["id"]}_expire = yes\n{P}_scene_{s["id"]}_dispatch = yes' for s in sorted(scene_rows,key=lambda s:(0 if 100<=s['id']<=115 else 1,s['id'])) if s['tag']==n.tag)+'\n'+
            guard('is_ai = yes','\n'.join(guard(f'{P}_{o.key}_can_start = yes',f'{P}_{o.key}_start = yes') for o in OPERATIONS if o.tag==n.tag)))
        effects[f'{P}_weekly_{n.tag.lower()}']=guard(f'tag = {n.tag} original_tag = {n.tag}',tick)
        hooks.append(block('on_weekly_'+n.tag,block('effect',f'{P}_weekly_{n.tag.lower()} = yes')))
    hooks.append(block('on_startup',block('effect',f'set_global_flag = {P}_enabled\n'+''.join(f'{n.tag} = {{ {P}_initialize = yes }}\n' for n in NATIONS))))
    for hook in ('on_capitulation_immediate','on_subject_annexed'):
        hooks.append(block(hook,block('effect',P+'_interrupt = yes')))
    hooks.append(block('on_annex',block('effect','FROM = { '+P+'_interrupt = yes }')))
    effects[P+'_character_tick'] = (
        guard('tag = ERU NOT = { has_country_flag = ac_camp_late_character_history } has_global_flag = ac_camp_battery_success NOT = { has_global_flag = ac_camp_yellow_four_settled }',
              'set_global_flag = ac_camp_yellow_four_settled\n'+guard('has_global_flag = ac_camp_yellow_four_airworthy','set_global_flag = ac_camp_yellow_four_preserved')+
              block('else','set_global_flag = ac_camp_yellow_four_lost'))+
        guard('tag = ERU NOT = { has_country_flag = ac_camp_late_character_history } has_global_flag = ac_ucw_outcome_isaf_victory NOT = { has_global_flag = ac_camp_yellow_thirteen_settled }',
              'set_global_flag = ac_camp_yellow_thirteen_settled\n'+guard('NOT = { has_global_flag = ac_camp_yellow_thirteen_preserved }','set_global_flag = ac_camp_yellow_thirteen_lost'))+
        guard('tag = OSE NOT = { has_country_flag = ac_camp_late_character_history } ac_cpw_course_open = yes date > 2010.11.28 NOT = { has_global_flag = ac_camp_chopper_settled }',
              'set_global_flag = ac_camp_chopper_settled\n'+guard('has_global_flag = ac_camp_rescue_cover_success','set_global_flag = ac_camp_chopper_preserved')+
              block('else','set_global_flag = ac_camp_chopper_lost'))+
        guard('tag = BLK has_global_flag = ac_camp_reckoning_success OR = { has_global_flag = ac_cpw_ended has_global_flag = ac_cpw_prevented has_global_flag = ac_cpw_declaration_withheld has_global_flag = ac_cpw_late_start_skipped has_global_flag = ac_cpw_principal_unable } NOT = { has_global_flag = ac_camp_network_settled }',
              'set_global_flag = ac_camp_network_settled\n'+guard('has_global_flag = ac_camp_seizure_success NOT = { has_global_flag = ac_camp_evidence_success } NOT = { has_global_flag = ac_camp_witness_success }','set_global_flag = ac_camp_network_success_ending')+
              block('else','set_global_flag = ac_camp_network_exposed_ending')))
    effects['ac_ucw_campaign_battery_custody_tick']=guard('tag = FCU has_idea = ac_camp_recaptured_battery NOT = { 310 = { is_controlled_by = SNS } }','remove_ideas = ac_camp_recaptured_battery')
    effects[P+'_weekly_fcu']+='\nac_ucw_campaign_battery_custody_tick = yes\n'
    add_peace(effects,triggers,event,decision,loc)
    text('ac_camp_clinic_sponsor_cost','Authorize this one receiving operation: FCU pays 25 political power, 2 institutional capacity and the shared programme fee only if San Salvacion starts it. No payment is made by this reply.')
    # Every exposed flag gets a readable tooltip; this pass uses generated source.
    source='\n'.join(effects.values())+'\n'.join(triggers.values())+'\n'.join(events)+'\n'.join(focuses)
    # Existing war owners retain their labels, including the five shared
    # campaign requirements exposed by the Continental owner.
    external_labels={'ac_camp_enabled','ac_camp_landing_success','ac_camp_battery_success','ac_camp_battery_disposition','ac_camp_megalith_success'}
    owned_prefixes=(P+'_',)+tuple(n.tag+'_camp_' for n in NATIONS)
    for name in re.findall(r'(?:has|set|clr)_(?:country|global)_flag\s*=\s*(\w+)',source):
        if name.startswith(owned_prefixes) and name not in external_labels:
            loc.setdefault(name,name.replace('ac_camp_','').replace('_',' ').capitalize())
    out={
        'common/scripted_effects/ac_campaigns.txt':'\n'.join(block(k,v) for k,v in effects.items()),
        'common/scripted_triggers/ac_campaigns.txt':'\n'.join(block(k,v) for k,v in triggers.items()),
        'common/national_focus/ac_campaigns.txt':'\n'.join(focuses),
        'common/ideas/ac_campaigns.txt':block('ideas',block('country','\n'.join(ideas))),
        'common/decisions/categories/ac_campaigns.txt':'\n'.join(categories),
        'common/decisions/ac_campaigns.txt':'\n'.join(block(k,'\n'.join(v)) for k,v in decisions.items()),
        'events/ac_campaigns.txt':'add_namespace = '+P+'\n'+'\n'.join(events),
        'common/on_actions/ac_campaigns.txt':block('on_actions','\n'.join(hooks)),
        'localisation/english/ac_campaigns_l_english.yml':'\ufeffl_english:\n'+''.join(' '+k+':0 "'+v.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in loc.items()),
    }
    # Imports into the live tree; legacy tree generators preserve this marker.
    for n in NATIONS:
        relative='common/national_focus/'+TREE_PATHS.get(n.tag,n.tag+'.txt')
        path=MOD/relative
        identifiers=[r['id'] for r in inventory if r['tag']==n.tag]
        out[relative]=attach(path.read_text(encoding='utf-8-sig'),identifiers)
        if n.tag=='BLK':
            relative='common/national_focus/ac_belkan_campaign.txt'
            out[relative]=attach((MOD/relative).read_text(encoding='utf-8-sig'),identifiers)
    return out,dict(schema=1,source_layer='provisional gameplay',focuses=inventory,
                    operations=[dict(**o.__dict__,source_layer='provisional gameplay',reference='tools/ac_campaigns/sources.json#fiction',status='implemented source; native pending') for o in OPERATIONS],
                    scenes=[dict(id=s['id'],tag=s['tag'],title=s['title'],words=len(s['body'].split()),variants=[dict(source_choice=v['choice'],additional_words=len(v['body'].split())) for v in s.get('variants',[])],source_layer='original supporting fiction',reference='tools/ac_campaigns/narrative.py and sources.json',status='implemented source; native pending') for s in scene_rows],native_acceptance=False)


def national_description(n,lane):
    return NATIONAL[n.tag][lane]


def partner_scene(o):
    return PARTNER_SCENES[o.key]


def add_peace(effects,triggers,event,decision,loc):
    # A stricter participant check than ordinary course observation: even own
    # subjects must be at peace before a bilateral white peace can be requested.
    safe=('ac_cpw_course_open = yes ac_cpw_pair_at_war = yes '+flag('harling_success')+' '+flag('nikanor_success')+' '+flag('solg_success')+
          ' OSE = { has_capitulated = no is_subject = no } YUK = { has_capitulated = no is_subject = no } NOT = { any_country = { NOT = { tag = OSE } NOT = { tag = YUK } OR = { has_war_with = OSE has_war_with = YUK } } }')
    triggers['ac_cpw_campaign_peace_safe']=safe
    effects['ac_cpw_campaign_peace_offer']=guard('tag = OSE original_tag = OSE ac_cpw_campaign_peace_safe = yes NOT = { has_global_flag = ac_camp_peace_offered }',
        'set_global_flag = ac_camp_peace_offered\nset_country_flag = { flag = ac_camp_peace_window days = 14 }\nYUK = { country_event = { id = ac_camp.2900 days = 1 } }')
    effects['ac_cpw_campaign_peace_accept']=guard('tag = YUK original_tag = YUK ac_cpw_campaign_peace_safe = yes OSE = { has_country_flag = ac_camp_peace_window }',
        'white_peace = OSE\n'+guard('NOT = { has_war_with = OSE }','set_global_flag = ac_camp_negotiated_peace\nac_cpw_record_end = yes\nOSE = { clr_country_flag = ac_camp_peace_window }'))
    event(2900,'YUK','An order both sides can hear',PEACE,
        'has_global_flag = ac_camp_peace_offered',
        [('Accept the reciprocal ceasefire.','ac_cpw_campaign_peace_safe = yes OSE = { has_country_flag = ac_camp_peace_window }','ac_cpw_campaign_peace_accept = yes'),
         ('The terms cannot be accepted.','ac_cpw_pair_at_war = yes OSE = { has_country_flag = ac_camp_peace_window }','set_global_flag = ac_camp_peace_refused\nOSE = { clr_country_flag = ac_camp_peace_window }')],'peace')
    decision('OSE','OSE_camp_peace_offer','Send the reciprocal ceasefire terms','Requires restored political authority, the completed interception, and an isolated campaign-owned war. Both sides must agree. The offer expires after fourteen days.',
        'ac_cpw_war_running = yes','ac_cpw_campaign_peace_safe = yes NOT = { has_global_flag = ac_camp_peace_offered }','ac_cpw_campaign_peace_offer = yes',5)
    decision('OSE','OSE_camp_peace_renew','Renew the ceasefire offer','Prepare a fresh offer after refusal or expiry. Costs the normal programme authorization; spent costs are not refunded.',
        'ac_cpw_war_running = yes has_global_flag = ac_camp_peace_offered',
        'ac_cpw_campaign_peace_safe = yes ac_camp_can_pay = yes NOT = { has_country_flag = ac_camp_peace_window } NOT = { has_country_flag = ac_camp_peace_cooldown }',
        guard('ac_cpw_campaign_peace_safe = yes ac_camp_can_pay = yes NOT = { has_country_flag = ac_camp_peace_window } NOT = { has_country_flag = ac_camp_peace_cooldown }','ac_camp_pay = yes\n'+guard('has_country_flag = ac_camp_paid','clr_global_flag = ac_camp_peace_offered\nset_country_flag = { flag = ac_camp_peace_cooldown days = 30 }\nac_cpw_campaign_peace_offer = yes')),2)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    out,manifest=compile_content();bad=[]
    targets={MOD/k:v.encode('utf-8') for k,v in out.items()}
    targets[HERE/'manifest.json']=(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode()
    for path,data in targets.items():
        if args.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n',b'\n')!=data:bad.append(str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if bad:raise SystemExit('Stale AC04/AC5 output: '+', '.join(bad))
    print(f'AC04/AC5: {len(manifest["focuses"])} focuses, {len(OPERATIONS)} operations, {len(manifest["scenes"])} core scenes; '+('consistent' if args.check else 'generated'))


if __name__=='__main__':main()
