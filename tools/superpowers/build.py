"""Compile distinct Osean commitment and Yuktobanian allocation programmes.

This owner writes only ac_snp/national programme state and guarded P1 API inputs.
The strategic-project owner ac_sp, wars, elections, rosters and histories remain
authoritative. All quantitative values and domestic procedures are provisional.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from superpowers.content import BRANCHES,focus_id,focus_description
from superpowers.mechanics import COUNTRIES,LATER_PARENT,LAYOUT,SERVICES
from reconstruction.build import block,guard,modifiers,improve
from usea_expansion.script import parse,get
from port_1_19.pdx import children,strip_comments_mask

NOTE='# Original provisional gameplay; source: tools/superpowers. Native acceptance pending.\n'
BEGIN='# BEGIN SUPERPOWER NATIONAL PROGRAMMES';END='# END SUPERPOWER NATIONAL PROGRAMMES'


def bid(b):return b.tag+'_snp_'+b.key
def host(tag):return 'tag = '+tag+' original_tag = '+tag
def active(tag):return 'ac_snp_active = yes '+host(tag)


def attach(source,tag):
    """Replace owned imports in every stable national alternative in place."""
    expected={focus_id(b,i)for b in BRANCHES if b.tag==tag for i in range(6)}
    if source.count(BEGIN)!=source.count(END):raise ValueError('Unbalanced SNP imports '+tag)
    replacements=[];mask=strip_comments_mask(source)
    for kind,_,_,a,z in children(source,0,len(source),mask):
        if kind!='focus_tree':continue
        body=source[a:z]
        if body.count(BEGIN)>1:raise ValueError('Duplicate SNP section '+tag)
        imports=BEGIN+'\n'+''.join('\tshared_focus = '+focus_id(b,i)+'\n'for b in BRANCHES if b.tag==tag for i in range(6))+'\t'+END
        if BEGIN in body:
            start=body.index(BEGIN);finish=body.index(END)+len(END)
            if any(k!='shared_focus'or v not in expected for k,_,v in parse(body[start:finish])):raise ValueError('Foreign content in SNP imports')
            body=body[:start]+imports+body[finish:]
        else:body=body.rstrip()+'\n\n\t'+imports+'\n'
        position=re.search(r'continuous_focus_position\s*=\s*\{[^{}]*\}',body)
        if not position:raise ValueError('Missing continuous panel '+tag)
        body=body[:position.start()]+f'continuous_focus_position = {{ x = {LAYOUT[tag][3]} y = 16 }}'+body[position.end():]
        replacements.append((a,z,body))
    if len(replacements)!=(2 if tag=='OSE'else 1):raise ValueError('Unexpected national tree containers '+tag)
    for a,z,body in reversed(replacements):source=source[:a]+body+source[z:]
    return source


def positions():
    result={};counts=defaultdict(int)
    for b in BRANCHES:
        n=counts[b.tag];counts[b.tag]+=1;columns,early,late,_=LAYOUT[b.tag]
        x=columns[n%4];y=early if n<4 else late
        for i in range(6):result[focus_id(b,i)]=(x+(-2 if i==1 else 2 if i==2 else 0),y+(0 if i==0 else 1 if i in(1,2)else i-1))
    return result


def prerequisites(b,index):
    if index==0:
        parent=LATER_PARENT.get(b.key)
        if not parent:return []
        foundation=next(row for row in BRANCHES if row.tag==b.tag and row.key==parent)
        return [focus_id(foundation,5)]
    if index in(1,2):return [focus_id(b,0)]
    if index==3:return [focus_id(b,1),focus_id(b,2)]
    return [focus_id(b,index-1)]


def requirement_text(b,index):
    refs=prerequisites(b,index)
    text=' '.join('has_completed_focus = '+ref for ref in refs)
    if len(refs)>1:text='OR = { '+text+' }'
    if index==4:text+=' has_country_flag = '+bid(b)+'_service_completed'
    return text


def output():
    loc={};effects={};triggers={};ideas=[];focuses=[];decisions=defaultdict(list);custom=[];timers=[]
    def text(key,value):
        if key in loc:raise ValueError('Duplicate SNP localization '+key)
        loc[key]=value
    def idea(ident,title,description,values):
        text(ident,title);text(ident+'_desc',description)
        ideas.append(block(ident,'picture = '+ident+'\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n'+block('modifier',modifiers(values))))
    def decision(ident,tag,title,description,visible,available,effect,fee=True,cost_key=None):
        text(ident,title);text(ident+'_desc',description)
        shown_available=available
        if cost_key:
            key=ident+'_requirements_tt'
            text(key,('The receiving support lane is below fifty and the hearing cooldown is clear. Commit twenty political power and two institutional-capacity points.'if tag=='OSE'else'The donating allocation retains at least twenty points and all existing reservations. Commit two institutional-capacity points and fifteen political power, or ten after the existing reform assessment.'))
            shown_available=block('custom_trigger_tooltip','tooltip = '+key+'\n'+available).strip()
        body='icon = ac_snp_'+ident+'\nallowed = { '+host(tag)+' }\nvisible = { '+active(tag)+' '+visible+' }\navailable = { '+shown_available+' }\ncost = 0\n'
        if fee or cost_key:
            key=cost_key or 'ac_snp_cost_yuk'
            if fee and tag=='OSE':key='ac_snp_cost_ose_'+('civil'if ident.endswith('_1')else'protected')
            body+='custom_cost_trigger = { '+shown_available+' }\ncustom_cost_text = '+key+'\n'
        summary=('Authorize the named ninety-day receiving scope. Reserve its national capacity and pay the displayed political, institutional and applicable fiscal costs. Wartime work uses the reduced domestic-continuity variant.'if fee else
                 'End this specific period, retain its delivered time and spent costs, and release its reservation without completed-service credit.'if ident.endswith('_cancel')else
                 'Restore up to eight support points toward the ordinary baseline of fifty; commit twenty political power and two institutional-capacity points, with a shared thirty-day hearing cooldown.'if tag=='OSE'else
                 'Reassign ten existing allocation points while protecting active reservations. Commit the displayed political cost and two institutional-capacity points, with a shared thirty-day reassignment cooldown.')
        text(ident+'_effect_tt',summary)
        weight='base = '+('2'if fee else'0')
        if tag=='OSE'and ident.endswith('_consultation'):
            lane='public'if'_public_'in ident else'security'
            weight='base = 2\n'+block('modifier','factor = 0\ncheck_variable = { ac_snp_ose_'+lane+' >= 30 }')
        body+=block('complete_effect','custom_effect_tooltip = '+ident+'_effect_tt\n'+block('hidden_effect',effect))+block('ai_will_do',weight)
        decisions['ac_snp_'+tag.lower()+'_programmes'].append(block(ident,body))

    triggers['ac_snp_participant']='OR = { AND = { '+host('OSE')+' } AND = { '+host('YUK')+' } }'
    triggers['ac_snp_eligible']='ac_snp_participant = yes OR = { AND = { '+host('OSE')+' any_owned_state = { is_controlled_by = OSE } } AND = { '+host('YUK')+' any_owned_state = { is_controlled_by = YUK } } } has_capitulated = no date > 1990.12.31'
    triggers['ac_snp_active']='ac_snp_eligible = yes has_country_flag = ac_snp_initialized'
    triggers['ac_snp_service_resources']='ac_snp_active = yes ac_pol_active = yes check_variable = { ac_pol_capacity >= 4 } OR = { ac_econ_enabled = no ac_econ_can_pay_programme = yes }'
    initialize=''
    for name,value in [('ose_public',50),('ose_security',50),('ose_used',0),('yuk_civil',50),('yuk_command',50),('yuk_civil_used',0),('yuk_command_used',0),('yuk_offices',0),('completed',0),('last_interrupted',0),('last_interrupted_days',0)]:
        tag='OSE'if name.startswith('ose_')else'YUK'if name.startswith('yuk_')else None
        body=guard('NOT = { has_variable = ac_snp_'+name+' }','set_variable = { ac_snp_'+name+' = '+str(value)+' }')
        initialize+=guard(host(tag),body)if tag else body
    initialize+='set_country_flag = ac_snp_initialized\n'
    effects['ac_snp_initialize']=guard('ac_snp_eligible = yes NOT = { has_country_flag = ac_snp_initialized }',initialize+'ac_snp_reconcile = yes')

    # Reservation totals are derived from this host's active owned receipts.
    reconcile=''
    for tag in COUNTRIES:
        body='set_variable = { ac_snp_ose_used = 0 }\n'if tag=='OSE'else'set_variable = { ac_snp_yuk_civil_used = 0 }\nset_variable = { ac_snp_yuk_command_used = 0 }\nset_variable = { ac_snp_yuk_offices = 0 }\n'
        for s in SERVICES:
            if s.branch.tag!=tag:continue
            amount='add_to_variable = { ac_snp_ose_used = '+str(s.weight)+' }'if tag=='OSE'else'add_to_variable = { ac_snp_yuk_'+('civil'if s.index==0 else'command')+'_used = 25 }\nadd_to_variable = { ac_snp_yuk_offices = 1 }'
            body+=guard('has_country_flag = '+s.id+'_active',amount)
        if tag=='OSE':
            for lane in('public','security'):body+='clamp_variable = { var = ac_snp_ose_'+lane+' min = 0 max = 100 }\n'
        else:
            body+='clamp_variable = { var = ac_snp_yuk_civil min = 20 max = 80 }\n'
            body+='set_temp_variable = { ac_snp_civil_max = 100 }\nsubtract_from_temp_variable = { ac_snp_civil_max = ac_snp_yuk_command_used }\n'
            body+='clamp_variable = { var = ac_snp_yuk_civil min = ac_snp_yuk_civil_used max = ac_snp_civil_max }\nset_variable = { ac_snp_yuk_command = 100 }\nsubtract_from_variable = { ac_snp_yuk_command = ac_snp_yuk_civil }\n'
        reconcile+=guard(host(tag),body)
    effects['ac_snp_reconcile']=guard('ac_snp_participant = yes has_country_flag = ac_snp_initialized',reconcile+'ac_snp_sync_standing = yes')
    standing=''
    for name,title,condition,values in [
        ('ose_public','Osea: A Credible Civil Mandate',host('OSE')+' check_variable = { ac_snp_ose_public >= 65 }',{'stability_factor':.015,'political_power_gain':-.03}),
        ('ose_security','Osea: Accountable Readiness Support',host('OSE')+' check_variable = { ac_snp_ose_security >= 65 }',{'army_org_factor':.015,'consumer_goods_factor':.003}),
        ('yuk_civil','Yuktobania: Civil Allocation Priority',host('YUK')+' check_variable = { ac_snp_yuk_civil >= 60 }',{'repair_speed_factor':.02,'army_org_factor':-.005}),
        ('yuk_command','Yuktobania: Command Allocation Priority',host('YUK')+' check_variable = { ac_snp_yuk_command >= 60 }',{'army_org_factor':.02,'consumer_goods_factor':.004})]:
        ident='ac_snp_'+name+'_standing';idea(ident,title,'The national register sustains this priority while retaining the political, civilian or readiness cost shown here.',values)
        standing+=guard('ac_snp_active = yes '+condition,'add_ideas = '+ident)+block('else','remove_ideas = '+ident)
    effects['ac_snp_sync_standing']=guard('ac_snp_participant = yes',standing)

    def fee():
        return guard('ac_econ_ready = yes','ac_econ_pay_programme = yes\n'+guard('OR = { ac_macro_ready = no has_country_flag = ac_macro_transaction_succeeded }','set_country_flag = ac_snp_payment_authorized'))+block('else','set_country_flag = ac_snp_payment_authorized')
    for s in SERVICES:
        tag=s.branch.tag;ident=s.id;prefix=s.prefix;unlock=focus_id(s.branch,0 if s.index==0 else 3)
        support='ac_snp_ose_'+('public'if s.index==0 else'security')
        price='political_power >= 35'
        if tag=='OSE':price='OR = { political_power >= 35 AND = { check_variable = { '+support+' >= 65 } political_power >= 30 } }'
        reservations='check_variable = { ac_snp_ose_used <= '+str(3-s.weight)+' } check_variable = { '+support+' >= 30 }'if tag=='OSE'else'check_variable = { ac_snp_yuk_offices < 2 } check_variable = { var = ac_snp_yuk_'+('civil'if s.index==0 else'command')+' value = '+prefix+'_needed compare = greater_than_or_equals }'
        # YUK needed is a pure current quote, calculated by reconcile below.
        if tag=='YUK':
            lane='civil'if s.index==0 else'command'
            reservations='check_variable = { ac_snp_yuk_offices < 2 } check_variable = { var = ac_snp_yuk_'+lane+' value = '+prefix+'_needed compare = greater_than_or_equals }'
        condition=active(tag)+' ac_snp_service_resources = yes '+price+' has_completed_focus = '+unlock+' NOT = { has_country_flag = '+ident+'_active } NOT = { has_country_flag = '+ident+'_cooldown } '+reservations
        lane_note=('Reserve '+str(s.weight)+' of the federal register\'s three commitment units; the '+('civil'if s.index==0 else'readiness')+' support lane needs at least thirty points.'if tag=='OSE'else'Reserve twenty-five points from the '+('civilian'if s.index==0 else'command')+' share and one of the two national receiving offices.')
        text(ident+'_requirements_tt',lane_note+' The scope must be unlocked and outside its cooldown. Four institutional-capacity points, the displayed political cost and any applicable programme fee must be available.')
        text(ident+'_can_start',s.title+': authorization requirements')
        triggers[ident+'_can_start']=block('custom_trigger_tooltip','tooltip = '+ident+'_requirements_tt\n'+condition).strip()
        pay_pp=guard('check_variable = { '+support+' >= 65 }','add_political_power = -30')+block('else','add_political_power = -35')if tag=='OSE'else'add_political_power = -35\n'
        start='clr_country_flag = ac_snp_payment_authorized\n'+guard(ident+'_can_start = yes',fee()+guard('has_country_flag = ac_snp_payment_authorized',
            'clr_country_flag = ac_snp_payment_authorized\n'+pay_pp+'set_temp_variable = { ac_pol_capacity_delta = -4 }\nac_pol_change_capacity = yes\n'+
            'set_country_flag = '+ident+'_active\nset_variable = { '+prefix+'_started = date }\nset_variable = { '+prefix+'_due = date }\nadd_to_variable = { '+prefix+'_due = 90 }\nset_variable = { '+prefix+'_elapsed = 0 }\n'+
            guard('has_war = yes','set_country_flag = '+ident+'_wartime\nadd_timed_idea = { idea = '+ident+'_domestic_spirit days = 90 }')+
            block('else','clr_country_flag = '+ident+'_wartime\nadd_timed_idea = { idea = '+ident+'_spirit days = 90 }')+
            'country_event = { id = '+s.event+' days = 90 }\nac_snp_reconcile = yes'))
        effects[ident+'_start']=start
        progress=guard('has_country_flag = '+ident+'_active has_variable = '+prefix+'_started','set_variable = { '+prefix+'_elapsed = date }\nsubtract_from_variable = { '+prefix+'_elapsed = '+prefix+'_started }\nclamp_variable = { var = '+prefix+'_elapsed min = 0 max = 90 }')
        effects[ident+'_progress']=guard(host(tag),progress)
        finishable=active(tag)+' has_country_flag = '+ident+'_active has_variable = '+prefix+'_started has_variable = '+prefix+'_due check_variable = { var = '+prefix+'_due value = date compare = less_than_or_equals } check_variable = { var = '+prefix+'_started value = date compare = less_than } OR = { has_war = no has_country_flag = '+ident+'_wartime }'
        triggers[ident+'_finishable']=finishable
        release='remove_ideas = '+ident+'_spirit\nremove_ideas = '+ident+'_domestic_spirit\nclr_country_flag = '+ident+'_active\n'
        support_reward=''
        if tag=='OSE':support_reward='add_to_variable = { '+support+' = 3 }\nadd_to_variable = { ac_snp_ose_'+('security'if s.index==0 else'public')+' = 1 }\n'
        finish=('set_country_flag = '+ident+'_completed\nset_country_flag = '+bid(s.branch)+'_service_completed\nadd_to_variable = { ac_snp_completed = 1 }\nset_variable = { '+prefix+'_elapsed = 90 }\n'+release+
            guard('has_country_flag = '+ident+'_wartime','set_country_flag = '+bid(s.branch)+'_last_domestic')+block('else','clr_country_flag = '+bid(s.branch)+'_last_domestic')+
            'clr_country_flag = '+ident+'_wartime\nset_country_flag = { flag = '+ident+'_cooldown days = 90 }\n'+support_reward+'ac_snp_reconcile = yes\n')
        effects[ident+'_finish']=ident+'_progress = yes\n'+guard(ident+'_finishable = yes check_variable = { '+prefix+'_elapsed >= 90 }',finish)
        effects[ident+'_cancel']=guard(host(tag)+' has_country_flag = '+ident+'_active',ident+'_progress = yes\n'+release+
            'set_country_flag = '+ident+'_interrupted\nset_variable = { ac_snp_last_interrupted = '+str(s.number+1)+' }\nset_variable = { ac_snp_last_interrupted_days = '+prefix+'_elapsed }\nclr_country_flag = '+ident+'_wartime\n'+('add_to_variable = { '+support+' = -3 }\n'if tag=='OSE'else'')+'ac_snp_reconcile = yes')
        # Exact due-date dispatch rejects an old/delayed timer. Weekly recovery
        # handles legitimate current work whose engine timer was not delivered.
        timer_condition=ident+'_finishable = yes check_variable = { var = '+prefix+'_due value = date compare = equals }'
        timers.append(block('country_event','id = '+s.event+'\nhidden = yes\nis_triggered_only = yes\ntrigger = { '+timer_condition+' }\n'+block('immediate',guard(timer_condition,ident+'_finish = yes'))))
        idea(ident+'_spirit',s.title,s.branch.institution+' sustains this ninety-day funded period. '+s.objective,s.modifiers)
        idea(ident+'_domestic_spirit',s.title+': Domestic Continuity',
            'During war, the receiving office limits this ninety-day period to domestic continuity. Records, training liaison and maintenance administration receive a reduced schedule while other staff answer urgent national needs.',
            {k:round(v*.65,3)for k,v in s.modifiers.items()})
        decision(ident,tag,s.title,s.objective+'\n\nLatest observed work: [?'+prefix+'_elapsed|0]/90 days.\n\nA funded period lasts ninety days. Wartime authorization performs reduced domestic continuity work. Annexation, capitulation, loss of all controlled national territory or cancellation ends the period without completion credit; spent resources remain committed. Successful completion starts this scope\'s ninety-day cooldown.',
            'has_completed_focus = '+unlock,ident+'_can_start = yes',ident+'_start = yes')
        decision(ident+'_cancel',tag,'End: '+s.title,'Stop this specific receiving period. Delivered time and spent resources remain in the record; incomplete work receives no review credit.',
            'has_country_flag = '+ident+'_active',active(tag)+' has_country_flag = '+ident+'_active',ident+'_cancel = yes',fee=False)

    # YUK service quotes are recomputed with every reservation/allocation change.
    quote=''
    for s in SERVICES:
        if s.branch.tag=='YUK':quote+='set_variable = { '+s.prefix+'_needed = ac_snp_yuk_'+('civil'if s.index==0 else'command')+'_used }\nadd_to_variable = { '+s.prefix+'_needed = 25 }\n'
    effects['ac_snp_reconcile']=effects['ac_snp_reconcile'].replace('ac_snp_sync_standing = yes',guard(host('YUK'),quote)+'ac_snp_sync_standing = yes')

    # National political actions have real resource costs and bounded consumers.
    for lane in('public','security'):
        ident='ac_snp_ose_'+lane+'_consultation';condition=active('OSE')+' ac_pol_active = yes political_power >= 20 check_variable = { ac_pol_capacity >= 2 } check_variable = { ac_snp_ose_'+lane+' < 50 } NOT = { has_country_flag = ac_snp_consultation_cooldown }'
        effects[ident]=guard(condition,'add_political_power = -20\nset_temp_variable = { ac_pol_capacity_delta = -2 }\nac_pol_change_capacity = yes\nadd_to_variable = { ac_snp_ose_'+lane+' = 8 }\nclamp_variable = { var = ac_snp_ose_'+lane+' max = 50 }\nset_country_flag = { flag = ac_snp_consultation_cooldown days = 30 }\nac_snp_reconcile = yes')
        decision(ident,'OSE','Hear '+('Civil-Service Objections'if lane=='public'else'Readiness Objections'),
            'Commit twenty political power and two institutional-capacity points to a receiving-office hearing. Restore up to eight support points, at most the ordinary baseline of fifty. This cannot purchase an earned high-support mandate. Both hearings share a thirty-day cooldown.',
            'check_variable = { ac_snp_ose_'+lane+' < 50 }',condition,ident+' = yes',fee=False,cost_key='ac_snp_cost_consult')
    for lane,delta in(('civil',10),('command',-10)):
        ident='ac_snp_yuk_shift_'+lane;donor='command'if lane=='civil'else'civil'
        condition=active('YUK')+' ac_pol_active = yes check_variable = { ac_pol_capacity >= 2 } NOT = { has_country_flag = ac_snp_allocation_cooldown } check_variable = { ac_snp_yuk_'+donor+' >= 30 } check_variable = { var = ac_snp_yuk_'+donor+' value = ac_snp_yuk_'+donor+'_shift_floor compare = greater_than_or_equals } OR = { political_power >= 15 AND = { has_completed_focus = YUK_army_reform_complete political_power >= 10 } }'
        effects[ident]=guard(condition,guard('has_completed_focus = YUK_army_reform_complete','add_political_power = -10')+block('else','add_political_power = -15')+
            'set_temp_variable = { ac_pol_capacity_delta = -2 }\nac_pol_change_capacity = yes\nadd_to_variable = { ac_snp_yuk_civil = '+str(delta)+' }\nset_country_flag = { flag = ac_snp_allocation_cooldown days = 30 }\nac_snp_reconcile = yes')
        decision(ident,'YUK','Reassign Ten Points to '+('Civil Receiving Offices'if lane=='civil'else'Command Support'),
            'Reassign ten of the existing hundred allocation points. The receiving office cannot take points already reserved by active work. This costs fifteen political power, or ten after the inherited army-reform assessment, plus two institutional-capacity points. Reassignments share a thirty-day cooldown. The inherited intervention, command reform and Arkbird policies remain in force.',
            '',condition,ident+' = yes',fee=False,cost_key='ac_snp_cost_reallocate')
    effects['ac_snp_reconcile']=effects['ac_snp_reconcile'].replace('ac_snp_sync_standing = yes',guard(host('YUK'),''.join('set_variable = { ac_snp_yuk_'+lane+'_shift_floor = ac_snp_yuk_'+lane+'_used }\nadd_to_variable = { ac_snp_yuk_'+lane+'_shift_floor = 10 }\n'for lane in('civil','command')))+'ac_snp_sync_standing = yes')

    coords=positions()
    for b in BRANCHES:
        for p,(title,benefit,cost)in enumerate(b.policies,1):
            ident=focus_id(b,p)+'_spirit';idea(ident,title,focus_description(b,p),{**benefit,**cost})
            idea(ident+'_settled',title+': Standing Settlement',focus_description(b,5)+' The chosen continuing cost remains.',improve(benefit,cost))
        for i in range(6):
            ident=focus_id(b,i);text(ident,b.titles[i]);text(ident+'_desc',focus_description(b,i));x,y=coords[ident]
            available=(active(b.tag)+' date > '+('1990.12.31'if b.opens=='1991.1.1'else'2005.12.31')+' '+requirement_text(b,i)).strip()
            other=focus_id(b,3-i)if i in(1,2)else None
            if other:available+=' NOT = { has_country_flag = '+other+'_done }'
            reward='set_country_flag = '+ident+'_done\n'
            if i in(1,2):
                reward+='add_ideas = '+ident+'_spirit\n'
                if b.tag=='OSE':reward+='add_to_variable = { ac_snp_ose_public = '+('4'if i==1 else'-2')+' }\nadd_to_variable = { ac_snp_ose_security = '+('-2'if i==1 else'4')+' }\n'
                else:reward+='add_to_variable = { ac_snp_yuk_civil = '+('5'if i==1 else'-5')+' }\n'
            if i==5:
                for p in(1,2):
                    policy=focus_id(b,p);reward+=guard('has_country_flag = '+policy+'_done','remove_ideas = '+policy+'_spirit\nadd_ideas = '+policy+'_spirit_settled')
            reward+='ac_snp_reconcile = yes\nac_snp_narrative_tick = yes\n'
            effects[ident+'_apply']=guard(available+' NOT = { has_country_flag = '+ident+'_done }',reward)
            body=f'id = {ident}\nicon = GFX_ac_snp_focus_{ident}\nx = {x}\ny = {y}\ncost = {10 if i in(1,2,5)else 5}\n'
            refs=prerequisites(b,i)
            if refs:body+=block('prerequisite','\n'.join('focus = '+ref for ref in refs))
            if other:body+=block('mutually_exclusive','focus = '+other)
            summary={0:'Unlock '+b.services[0][0]+', a funded ninety-day national service.',
                1:'Adopt '+b.policies[0][0]+', with the benefit and continuing opportunity cost shown below.',
                2:'Adopt '+b.policies[1][0]+', with the benefit and continuing opportunity cost shown below.',
                3:'Unlock '+b.services[1][0]+', a second specific funded receiving scope.',
                4:'Record the branch’s genuinely completed service period as the basis for a standing settlement.',
                5:'Improve the selected policy’s benefit by twenty percent while retaining its same continuing cost.'}[i]
            if i in(1,2):summary+=(' Civil support '+('+4 and readiness support -2.'if i==1 else'-2 and readiness support +4.')if b.tag=='OSE'else' Move up to five existing allocation points toward '+('civil receiving offices'if i==1 else'command support')+', protecting active reservations and the allocation bounds.')
            text(ident+'_effect_tt',summary)
            shown='custom_effect_tooltip = '+ident+'_effect_tt\n'
            if i in(1,2):shown+='show_ideas_tooltip = '+ident+'_spirit\n'
            if i==5:
                for p in(1,2):shown+=guard('has_country_flag = '+focus_id(b,p)+'_done','show_ideas_tooltip = '+focus_id(b,p)+'_spirit_settled')
            body+=block('available',available)+'cancel_if_invalid = yes\ncontinue_if_invalid = no\nai_will_do = { factor = 12 }\n'+block('completion_reward',shown+block('hidden_effect',ident+'_apply = yes'))
            focuses.append(block('shared_focus',body))

    from superpowers.narrative import narrative
    stories,story_custom=narrative(effects,triggers,text,idea)
    custom.append(story_custom)
    text('ac_snp_cost_ose_civil','[ac_snp_ose_civil_price_text]')
    text('ac_snp_cost_ose_protected','[ac_snp_ose_protected_price_text]')
    text('ac_snp_cost_35','£pol_power 35 / 4 cap');text('ac_snp_cost_30','£pol_power 30 / 4 cap')
    text('ac_snp_cost_consult','£pol_power 20 / 2 cap')
    text('ac_snp_cost_reallocate','[ac_snp_yuk_reallocation_price_text]')
    text('ac_snp_cost_15','£pol_power 15 / 2 cap');text('ac_snp_cost_10','£pol_power 10 / 2 cap')
    for lane,index in(('civil','public'),('protected','security')):
        custom.append(block('defined_text','name = ac_snp_ose_'+lane+'_price_text\n'+block('text','trigger = { check_variable = { ac_snp_ose_'+index+' >= 65 } }\nlocalization_key = ac_snp_cost_30')+block('text','localization_key = ac_snp_cost_35')))
    custom.append(block('defined_text','name = ac_snp_yuk_reallocation_price_text\n'+block('text','trigger = { has_completed_focus = YUK_army_reform_complete }\nlocalization_key = ac_snp_cost_10')+block('text','localization_key = ac_snp_cost_15')))
    text('ac_snp_cost_yuk','£pol_power 35 / 4 cap')
    text('ac_snp_fee_macro','Programme fee: 0.002 billion abstract fiscal units.')
    text('ac_snp_fee_legacy','Programme fee: 2 provisional fiscal units.')
    text('ac_snp_fee_none','No fiscal fee currently applies. Political and institutional costs remain.')
    custom.append(block('defined_text','name = ac_snp_fee_text\n'+block('text','trigger = { ac_macro_ready = yes }\nlocalization_key = ac_snp_fee_macro')+block('text','trigger = { ac_econ_ready = yes }\nlocalization_key = ac_snp_fee_legacy')+block('text','localization_key = ac_snp_fee_none')))
    text('ac_snp_no_interruption','No interrupted service period is recorded.')
    interrupted_records=''
    for s in SERVICES:
        key=s.id+'_interrupted_record';text(key,'Last interrupted period: '+s.title+', [?ac_snp_last_interrupted_days|0]/90 days delivered. Spent resources were retained.')
        interrupted_records+=block('text','trigger = { '+host(s.branch.tag)+' check_variable = { ac_snp_last_interrupted = '+str(s.number+1)+' } }\nlocalization_key = '+key)
    custom.append(block('defined_text','name = ac_snp_interruption_text\n'+interrupted_records+block('text','localization_key = ac_snp_no_interruption')))
    categories=[]
    for tag,name in COUNTRIES.items():
        ident='ac_snp_'+tag.lower()+'_programmes';text(ident,name+': '+('Federal Commitment Register'if tag=='OSE'else'National Allocation Docket'))
        desc=('Federal schedule: [?ac_snp_ose_used|0]/3 commitment units reserved. Civil periods use one; protected periods use two.\nCivil support: [?ac_snp_ose_public|0]/100. Readiness support: [?ac_snp_ose_security|0]/100. A lane needs thirty support to authorize work. At sixty-five, its service costs thirty rather than thirty-five political power and sustains its earned mandate with the shown continuing cost.'if tag=='OSE'else'Civil allocation: [?ac_snp_yuk_civil|0]/100, reserving [?ac_snp_yuk_civil_used|0]. Command allocation: [?ac_snp_yuk_command|0]/100, reserving [?ac_snp_yuk_command_used|0]. The shares always total one hundred. Each period reserves twenty-five points from its lane, with at most two national offices active. Priority at sixty points sustains the corresponding standing policy and its continuing cost.')
        desc+='\n\n[ac_snp_fee_text]\nService authorization also commits four institutional-capacity points. Every scope has a ninety-day completed-service cooldown. Wartime periods perform reduced domestic continuity work. Completed periods: [?ac_snp_completed|0].\n[ac_snp_interruption_text]\n\n'
        for s in SERVICES:
            if s.branch.tag!=tag:continue
            key=s.id+'_status';text(key+'_active',s.title+': active, [?'+s.prefix+'_elapsed|0]/90 days.\n');text(key+'_idle','')
            text(key+'_domestic',s.title+': domestic continuity, [?'+s.prefix+'_elapsed|0]/90 days.\n')
            text(key+'_cooldown',s.title+': completed; the ninety-day recovery interval is active.\n')
            custom.append(block('defined_text','name = '+key+'\n'+block('text','trigger = { has_country_flag = '+s.id+'_active has_country_flag = '+s.id+'_wartime }\nlocalization_key = '+key+'_domestic')+block('text','trigger = { has_country_flag = '+s.id+'_active }\nlocalization_key = '+key+'_active')+block('text','trigger = { has_country_flag = '+s.id+'_cooldown }\nlocalization_key = '+key+'_cooldown')+block('text','localization_key = '+key+'_idle')))
            desc+='['+key+']'
        text(ident+'_desc',desc)
        visible='OR = { '+' '.join('has_country_flag = '+focus_id(b,0)+'_done'for b in BRANCHES if b.tag==tag)+' }'
        categories.append(block(ident,'icon = GFX_ac_snp_category_'+tag.lower()+'\nallowed = { '+host(tag)+' }\nvisible = { '+active(tag)+' '+visible+' }'))

    interrupted='';war='';observe=''
    for s in SERVICES:
        interrupted+=s.id+'_cancel = yes\n'
        war+=guard('NOT = { has_country_flag = '+s.id+'_wartime }',s.id+'_cancel = yes')
        observe+=s.id+'_progress = yes\n'+s.id+'_finish = yes\n'
    effects['ac_snp_interrupt_services']=guard('ac_snp_participant = yes',interrupted+'ac_snp_sync_standing = yes')
    effects['ac_snp_war_interruption']=guard('ac_snp_participant = yes',war)
    effects['ac_snp_interrupt']='ac_snp_interrupt_services = yes\nac_snp_interrupt_messages = yes\n'
    effects['ac_snp_weekly']=guard('ac_snp_participant = yes','ac_snp_initialize = yes\n'+guard('ac_snp_active = no','ac_snp_interrupt = yes')+guard('ac_snp_active = yes',guard('has_war = yes','ac_snp_war_interruption = yes')+'ac_snp_reconcile = yes\n'+observe+'ac_snp_narrative_tick = yes'))
    hooks=block('on_startup',block('effect','OSE = { ac_snp_initialize = yes }\nYUK = { ac_snp_initialize = yes }'))+block('on_weekly',block('effect','ac_snp_weekly = yes'))
    hooks+=block('on_annex',block('effect','FROM = { ac_snp_interrupt = yes }'))+block('on_capitulation_immediate',block('effect','ac_snp_interrupt = yes'))+block('on_subject_annexed',block('effect','ac_snp_interrupt = yes'))
    hooks+=block('on_war_relation_added',block('effect','ac_snp_war_interruption = yes\nFROM = { ac_snp_war_interruption = yes }'))
    out={
        'common/national_focus/ac_superpower_programmes.txt':NOTE+'\n'.join(focuses),
        'common/scripted_effects/ac_superpower_programmes.txt':NOTE+'\n'.join(block(k,v)for k,v in effects.items()),
        'common/scripted_triggers/ac_superpower_programmes.txt':NOTE+'\n'.join(block(k,v)for k,v in triggers.items()),
        'common/ideas/ac_superpower_programmes.txt':NOTE+block('ideas',block('country','\n'.join(ideas))),
        'common/decisions/categories/ac_superpower_programmes.txt':NOTE+'\n'.join(categories),
        'common/decisions/ac_superpower_programmes.txt':NOTE+'\n'.join(block(k,'\n'.join(v))for k,v in decisions.items()),
        'common/custom_localization/ac_superpower_programmes.txt':NOTE+'\n'.join(custom),
        'common/on_actions/ac_superpower_programmes.txt':NOTE+block('on_actions',hooks),
        'events/ac_superpower_programmes.txt':NOTE+'add_namespace = ac_snp\n'+stories+'\n'+'\n'.join(timers)}
    for tag in COUNTRIES:
        relative='common/national_focus/'+tag+'.txt';out[relative]=attach((MOD/relative).read_text(encoding='utf-8-sig'),tag)
    def descend(nodes):
        for row in nodes:
            yield row
            if isinstance(row[2],list):yield from descend(row[2])
    for source in list(out.values()):
        for key,_,value in descend(parse(source)):
            if key in('has_country_flag','set_country_flag','clr_country_flag'):
                flag=get(value,'flag')if isinstance(value,list)else value
                if flag not in loc and ('_snp_'in flag or flag.startswith('ac_snp_')):
                    text(flag,'National programmes: '+re.sub(r'^(?:ac_snp_|(?:OSE|YUK)_snp_)','',flag).replace('_',' ').capitalize())
    for key in('ac_snp_participant','ac_snp_eligible','ac_snp_active','ac_snp_service_resources'):
        text(key,{'ac_snp_participant':'Established national administration','ac_snp_eligible':'An eligible national receiving office','ac_snp_active':'National register initialized','ac_snp_service_resources':'Institutional capacity and the applicable programme fee are available'}[key])
    out['localisation/english/ac_superpower_programmes_l_english.yml']='\ufeffl_english:\n'+'\n'.join(' '+k+':0 "'+v.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"'for k,v in loc.items())+'\n'
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();failures=[]
    for relative,text in output().items():
        path=MOD/relative
        if a.check:
            if not path.exists()or path.read_text(encoding='utf-8')!=text:failures.append(relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='\n')
    manifest=dict(schema=1,source_layer='Original provisional gameplay',focuses=[dict(id=focus_id(b,i),tag=b.tag,branch=b.key,opens=b.opens,x=positions()[focus_id(b,i)][0],y=positions()[focus_id(b,i)][1])for b in BRANCHES for i in range(6)],
        services=[dict(id=s.id,tag=s.branch.tag,lane=s.lane,reservation=s.weight,days=90,cooldown=90,event=s.event)for s in SERVICES],native_accepted=False)
    path=HERE/'manifest.json';text=json.dumps(manifest,indent=2)+'\n'
    if a.check:
        if not path.exists()or path.read_text()!=text:failures.append('tools/superpowers/manifest.json')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    if failures:raise SystemExit('Superpower programme output differs: '+', '.join(failures))
    print('SP96:96 definitions,32 funded scopes; '+('consistent'if a.check else'generated'))

if __name__=='__main__':main()
