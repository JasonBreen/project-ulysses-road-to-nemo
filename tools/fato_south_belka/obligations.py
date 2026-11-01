"""Finite consented stock warrants and a separately owned civil case docket.

Replies are decisions, so no queued diplomatic event can consume a later offer.
Every delivery/resolution rechecks current identity, permission and real costs.
"""
from fato_south_belka_builder import (block,guard,done,active,capacity,idea,decision,effect,trigger)
from programmes import stock_guard,spend_stock,stock_text

PARTNERS=('GEB','REC','OSE')
PARTNER_NAMES={'GEB':'Gebet','REC':'Recta','OSE':'Osea'}
WARRANTS={
 'infantry':('Infantry replacements','infantry_equipment',300,'infantry_warrant'),
 'small':('Small infantry consignment','infantry_equipment',150,'small_warrant'),
 'support':('Workshop support stores','support_equipment',30,'support_warrant'),
 'mobility':('Motor transport','motorized_equipment',20,'mobility_warrant'),
}

def build_warrants():
    trigger('ac_fsb_has_warrant_slot','OR = { check_variable = { ac_fsb_warrants_open < 1 } AND = { has_country_flag = ac_fsb_second_warrant check_variable = { ac_fsb_warrants_open < 2 } } AND = { has_country_flag = ac_fsb_third_warrant check_variable = { ac_fsb_warrants_open < 3 } } }')
    recount='set_variable = { ac_fsb_warrants_open = 0 }\n';close_all='';tick='';partner_tick='';partner_interrupt=''
    idea('ac_fsb_receiving_training','A Received Replacement Batch','Actual equipment has arrived. A short receiving and familiarisation interval follows; no faction, war outcome or further stock is granted.',{'training_time_factor':-.025,'political_power_gain':-.05})
    idea('ac_fsb_receiving_inspection','A Joint Receiving Inspection','Both authorities consented to a limited inspection, and an actual stock-backed delivery followed. The temporary staff burden remains visible.',{'training_time_factor':-.035,'army_org_factor':.01,'political_power_gain':-.1})
    for partner in PARTNERS:
        valid='ac_fsb_warrant_'+partner.lower()+'_valid'
        trigger(valid,'tag = FAT original_tag = FAT has_capitulated = no is_subject = no any_owned_state = { always = yes } country_exists = '+partner+' NOT = { has_war_with = '+partner+' } '+partner+' = { tag = '+partner+' original_tag = '+partner+' has_capitulated = no is_subject = no any_owned_state = { always = yes } }')
        for kind,(title,equipment,quantity,unlock) in WARRANTS.items():
            stem='ac_fsb_w_'+partner.lower()+'_'+kind;opened=stem+'_open';window=stem+'_window';accepted=stem+'_accepted';inspected=stem+'_inspected';notice=stem+'_notice';cool=stem+'_cooldown'
            clear='clr_country_flag = '+opened+'\nclr_country_flag = '+window+'\nclr_country_flag = '+accepted+'\nclr_country_flag = '+inspected+'\n'+partner+' = { clr_country_flag = '+notice+' }\nac_fsb_recount_warrants = yes\n'
            effect(stem+'_close',guard('tag = FAT original_tag = FAT',clear))
            recount+=guard('has_country_flag = '+opened,'add_to_variable = { ac_fsb_warrants_open = 1 }')
            close_all+=stem+'_close = yes\n'
            extra=' has_country_flag = ac_fsb_reserve_floor' if kind=='small' else ''
            condition=active('FAT')+' '+valid+' = yes has_country_flag = ac_fsb_partner_register has_country_flag = ac_fsb_'+unlock+extra+' ac_fsb_has_warrant_slot = yes ac_fsb_can_fund = yes political_power >= 15 check_variable = { ac_pol_capacity >= 1 } NOT = { has_country_flag = '+opened+' } NOT = { has_country_flag = '+cool+' }'
            request='ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded','add_political_power = -15\n'+capacity(-1)+'set_country_flag = '+opened+'\nset_country_flag = { flag = '+cool+' days = 180 }\n'+guard('has_country_flag = ac_fsb_long_consent','set_country_flag = { flag = '+window+' days = 90 }')+block('else','set_country_flag = { flag = '+window+' days = 30 }')+partner+' = { set_country_flag = '+notice+' }\nac_fsb_recount_warrants = yes')
            decision('FAT','request_'+partner.lower()+'_'+kind,'Request consent: '+title+' to '+PARTNER_NAMES[partner],
                'Offer '+str(quantity)+' '+equipment.replace('_',' ')+' from real stock, not an immediate donation. Cost: 15 political power, 1 institutional capacity and the public programme fee. The receiver must consent by decision within 30 days (90 with the consent clause). One open slot is occupied; 180-day request cooldown. Both authorities must remain eligible and independent. No faction or military access is created.',condition,request,
                active('FAT')+' has_country_flag = ac_fsb_partner_register has_country_flag = ac_fsb_'+unlock,weight=1,icon='warrant')
            answer='tag = '+partner+' original_tag = '+partner+' has_capitulated = no has_country_flag = '+notice+' country_exists = FAT FAT = { ac_fsb_active = yes '+valid+' = yes has_country_flag = '+opened+' has_country_flag = '+window+' NOT = { has_country_flag = '+accepted+' } }'
            for inspected_reply in (False,True):
                suffix='inspect' if inspected_reply else 'accept';cost=2 if inspected_reply else 1
                cond=answer+' ac_pol_active = yes political_power >= 10 check_variable = { ac_pol_capacity >= '+str(cost)+' }'
                if inspected_reply:cond+=' FAT = { has_country_flag = ac_fsb_joint_inspection has_country_flag = ac_fsb_invoice_verified }'
                body='add_political_power = -10\n'+capacity(-cost)+'clr_country_flag = '+notice+'\nFAT = { set_country_flag = '+accepted+'\n'+('set_country_flag = '+inspected if inspected_reply else '')+'\n}\n'
                decision(partner,'reply_'+partner.lower()+'_'+kind+'_'+suffix,('Accept inspected' if inspected_reply else 'Accept')+': '+title+' from FATO',
                    'Spend 10 political power and '+str(cost)+' institutional capacity to authorise this specific consignment. FATO must still deliver actual stock before the original deadline. Acceptance gives no equipment, alignment or reward by itself. The receiving authority may revoke before dispatch.',cond,body,answer,weight=2 if not inspected_reply else 1,icon='warrant')
            decision(partner,'reply_'+partner.lower()+'_'+kind+'_refuse','Decline: '+title+' from FATO',
                'Decline without an equipment or financial reward. FATO retains a useful paid domestic alternative if it has earned one. This closes the current offer and its slot.',answer,
                'FAT = { '+stem+'_close = yes set_country_flag = ac_fsb_offer_refused }',answer,weight=1,icon='warrant')
            revoke='tag = '+partner+' original_tag = '+partner+' has_country_flag = '+notice+'_unused'
            # Notice is cleared on acceptance, so revocation reads the actual
            # sender's accepted permission rather than a stale receiver marker.
            revoke='tag = '+partner+' original_tag = '+partner+' country_exists = FAT FAT = { '+valid+' = yes has_country_flag = '+opened+' has_country_flag = '+accepted+' has_country_flag = '+window+' }'
            decision(partner,'reply_'+partner.lower()+'_'+kind+'_revoke','Revoke before dispatch: '+title,
                'Cancel this unfulfilled permission. No stock is returned because none has been delivered; no new reward is granted.',revoke,
                'FAT = { '+stem+'_close = yes set_country_flag = ac_fsb_offer_refused }',revoke,weight=0,icon='warrant')
            domestic_floor=300 if equipment=='infantry_equipment' else (10 if equipment=='support_equipment' else 10)
            base=active('FAT')+' '+valid+' = yes has_country_flag = '+opened+' has_country_flag = '+window+' has_country_flag = '+accepted
            delivery=base+' '+stock_guard({equipment:quantity+domestic_floor})
            if equipment=='infantry_equipment':delivery+=' OR = { NOT = { has_country_flag = ac_fsb_reserve_floor } '+stock_guard({equipment:quantity+600})+' }'
            dispatch='send_equipment = { equipment = '+equipment+' amount = '+str(quantity)+' target = '+partner+' }\n'+guard('has_country_flag = '+inspected,partner+' = { add_timed_idea = { idea = ac_fsb_receiving_inspection days = 180 } }')+block('else',partner+' = { add_timed_idea = { idea = ac_fsb_receiving_training days = 90 } }')+'add_to_variable = { ac_fsb_deliveries = 1 }\n'+stem+'_close = yes\n'
            decision('FAT','deliver_'+partner.lower()+'_'+kind,'Dispatch: '+title+' to '+PARTNER_NAMES[partner],
                'Transfer exactly '+str(quantity)+' '+equipment.replace('_',' ')+' from current stock. Keep at least '+str(domestic_floor)+' at home (600 infantry with the reserve-floor rule). Recheck consent, deadline and both authorities. A completed shipment cannot be dispatched again.',delivery,dispatch,base,weight=4,icon='warrant')
            withdraw=active('FAT')+' has_country_flag = '+opened+' OR = { NOT = { has_country_flag = '+accepted+' } has_country_flag = ac_fsb_accepted_appeal } OR = { has_country_flag = ac_fsb_clean_withdrawal political_power >= 10 }'
            decision('FAT','withdraw_'+partner.lower()+'_'+kind,'Withdraw: '+title+' to '+PARTNER_NAMES[partner],
                'Close the current undelivered warrant. Cost 10 political power unless the clean-withdrawal procedure was earned. Accepted warrants need the later appeal procedure, or the general suspension order. No costs are refunded.',withdraw,
                guard('NOT = { has_country_flag = ac_fsb_clean_withdrawal }','add_political_power = -10')+stem+'_close = yes\nset_country_flag = ac_fsb_external_closed',active('FAT')+' has_country_flag = '+opened,weight=0,icon='warrant')
            tick+=guard('has_country_flag = '+opened+' OR = { NOT = { has_country_flag = '+window+' } '+valid+' = no }',stem+'_close = yes\nset_country_flag = ac_fsb_external_closed')
            partner_tick+=guard('tag = '+partner+' original_tag = '+partner+' has_country_flag = '+notice+' OR = { NOT = { country_exists = FAT } FAT = { '+valid+' = no } FAT = { NOT = { has_country_flag = '+opened+' } } FAT = { NOT = { has_country_flag = '+window+' } } }','clr_country_flag = '+notice+'\nFAT = { '+stem+'_close = yes set_country_flag = ac_fsb_external_closed }')
            partner_interrupt+=guard('tag = '+partner+' original_tag = '+partner,'clr_country_flag = '+notice+'\nFAT = { '+guard('has_country_flag = '+opened,stem+'_close = yes\nset_country_flag = ac_fsb_external_closed')+' }')
    effect('ac_fsb_recount_warrants',guard('tag = FAT original_tag = FAT',recount))
    effect('ac_fsb_close_all_warrants',guard('tag = FAT original_tag = FAT',close_all))
    effect('ac_fsb_warrant_tick',guard('tag = FAT original_tag = FAT',tick+'ac_fsb_recount_warrants = yes'))
    effect('ac_fsb_partner_tick',partner_tick+'\nac_fsb_adviser_receiver_tick = yes')
    effect('ac_fsb_partner_interrupt',partner_interrupt+'\nac_fsb_adviser_receiver_interrupt = yes')

CASES={
 'property':('The Property File','case_property',
    [('protected','Protect established possession',{}, {'stability_factor':.025,'production_speed_buildings_factor':-.02}),
     ('interim','Record protected interim possession',{}, {'stability_factor':.01,'political_power_gain':.025})]),
 'utilities':('The Utility Work Order','case_utilities',
    [('repair','Fund the verified repair',{'support_equipment':10},{'production_speed_buildings_factor':.05,'consumer_goods_factor':.01}),
     ('ration','Ration the current service',{}, {'supply_consumption_factor':-.02,'stability_factor':-.01})]),
 'stores':('The Stores Reconciliation','case_stores',
    [('maintain','Use stores for maintenance',{'support_equipment':15},{'attrition':-.035,'industrial_capacity_factory':-.015}),
     ('seal','Keep a sealed, inspected reserve',{}, {'production_factory_efficiency_gain_factor':.025,'political_power_gain':-.05})]),
 'security':('The Security Remit','case_security',
    [('public','Publish a narrower local remit',{}, {'stability_factor':.025,'army_org_factor':-.01}),
     ('inspect','Fund supervised service inspection',{'support_equipment':10},{'army_org_factor':.03,'political_power_gain':-.1})]),
 'access':('The Resident Access File','case_access',
    [('civil','Extend provisional civil access',{}, {'stability_factor':.03,'consumer_goods_factor':.01}),
     ('limited','Protect a limited interim service',{}, {'stability_factor':.015,'political_power_gain':-.05})]),
 'archive':('The Archive File','case_archive',
    [('witness','Reconstruct with local witnesses',{}, {'stability_factor':.02,'political_power_gain':.05,'consumer_goods_factor':.005}),
     ('protect','Keep uncertain records protected',{}, {'production_factory_efficiency_gain_factor':.025,'political_power_gain':-.05})]),
}

def build_cases():
    trigger('ac_fsb_has_case_slot','OR = { check_variable = { ac_fsb_cases_open < 1 } AND = { has_country_flag = ac_fsb_second_case check_variable = { ac_fsb_cases_open < 2 } } }')
    recount='set_variable = { ac_fsb_cases_open = 0 }\n';close_all='';tick=''
    for kind,(title,unlock,outcomes) in CASES.items():
        stem='ac_fsb_case_'+kind;opened=stem+'_open';deadline=stem+'_window';resolved=stem+'_resolved';reopened=stem+'_appealed'
        close='clr_country_flag = '+opened+'\nclr_country_flag = '+deadline+'\nac_fsb_recount_cases = yes\n'
        effect(stem+'_close',guard('tag = SBK original_tag = SBK',close))
        close_all+=stem+'_close = yes\n';recount+=guard('has_country_flag = '+opened,'add_to_variable = { ac_fsb_cases_open = 1 }')
        condition=active('SBK')+' has_country_flag = ac_fsb_'+unlock+' ac_fsb_has_case_slot = yes ac_fsb_can_fund = yes political_power >= 10 check_variable = { ac_pol_capacity >= 1 } NOT = { has_country_flag = '+opened+' } NOT = { has_country_flag = '+resolved+' }'
        opening='ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded','add_political_power = -10\n'+capacity(-1)+'set_country_flag = '+opened+'\nset_country_flag = { flag = '+deadline+' days = 120 }\nac_fsb_recount_cases = yes')
        decision('SBK','open_'+kind,'Open: '+title,
            'Open this specific civil case for up to 120 days. Cost: 10 political power, 1 institutional capacity and the public programme fee. One case slot is occupied (maximum two once authorised). Resolution is a separate real choice; expiry, occupation or reintegration grants no completion reward.',condition,opening,active('SBK')+' has_country_flag = ac_fsb_'+unlock+' NOT = { has_country_flag = '+resolved+' }',icon='docket')
        for choice,label,stocks,mods in outcomes:
            ident=stem+'_'+choice;idea(ident,label,'A resolved '+kind+' case. The temporary arrangement carries the stated benefits and burdens; it does not change territory, cores, forces or sovereignty.',mods)
            cond=active('SBK')+' has_country_flag = '+opened+' has_country_flag = '+deadline+' ac_fsb_can_fund = yes political_power >= 15 check_variable = { ac_pol_capacity >= 2 } '+stock_guard(stocks)
            if kind=='archive' and choice=='witness':cond+=' has_country_flag = ac_fsb_local_witnesses'
            if kind=='security' and choice=='inspect':cond+=' has_country_flag = ac_fsb_security_review'
            # A lower-cost interim solution is explicitly earned for these two
            # cases. Their other outcome always remains a useful alternative.
            if (kind,choice) in (('utilities','ration'),('access','limited')):cond+=' OR = { has_country_flag = ac_fsb_resident_consent has_country_flag = ac_fsb_interim_service }'
            result='add_political_power = -15\n'+capacity(-2)+spend_stock(stocks)
            result+=guard('has_country_flag = ac_fsb_verified_receipts',capacity(1))
            result+=guard('has_country_flag = ac_fsb_indexed_archive',capacity(1))
            result+=''.join('remove_ideas = '+stem+'_'+other+'\n' for other,*_ in outcomes)
            if kind in ('utilities','access'):
                result+=guard('has_country_flag = ac_fsb_standing_orders','add_timed_idea = { idea = '+ident+' days = 365 }')+block('else','add_timed_idea = { idea = '+ident+' days = 180 }')
            else:result+='add_timed_idea = { idea = '+ident+' days = 180 }\n'
            result+='set_country_flag = '+resolved+'\nadd_to_variable = { ac_fsb_cases_resolved = 1 }\n'+stem+'_close = yes\n'
            decision('SBK','resolve_'+kind+'_'+choice,label,
                'Resolve the '+kind+' case. Cost: 15 political power, 2 institutional capacity and the public programme fee, plus current stock '+stock_text(stocks)+'. Verified receipts and a common archive each return one capacity after payment. Benefit lasts 180 days (365 for future utility/access settlements with standing work orders). Each case may be appealed only once, replacing the old benefit.',cond,
                'ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded',result),active('SBK')+' has_country_flag = '+opened,icon='docket',preview=block('effect_tooltip','add_timed_idea = { idea = '+ident+' days = 180 }'))
        appeal=active('SBK')+' has_country_flag = ac_fsb_case_appeal has_country_flag = '+resolved+' NOT = { has_country_flag = '+reopened+' } ac_fsb_has_case_slot = yes ac_fsb_can_fund = yes political_power >= 20 check_variable = { ac_pol_capacity >= 2 }'
        body='ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded','add_political_power = -20\n'+capacity(-2)+'set_country_flag = '+reopened+'\nclr_country_flag = '+resolved+'\n'+''.join('remove_ideas = '+stem+'_'+choice+'\n' for choice,*_ in outcomes)+'set_country_flag = '+opened+'\nset_country_flag = { flag = '+deadline+' days = 120 }\nac_fsb_recount_cases = yes')
        decision('SBK','appeal_'+kind,'Appeal once: '+title,'Pay 20 political power, 2 institutional capacity and the public programme fee. Remove the old case benefit and reopen for 120 days. The previous cost is never refunded, and a second appeal is impossible.',appeal,body,active('SBK')+' has_country_flag = ac_fsb_case_appeal has_country_flag = '+resolved+' NOT = { has_country_flag = '+reopened+' }',weight=0,icon='docket')
        obsolete=active('SBK')+' has_country_flag = ac_fsb_close_obsolete has_country_flag = '+opened
        decision('SBK','close_'+kind,'Close without award: '+title,'Close the open case without a settlement benefit or refund. The record remains; unresolved work may be opened again at its real cost.',obsolete,stem+'_close = yes',obsolete,weight=0,icon='docket')
        tick+=guard('has_country_flag = '+opened+' NOT = { has_country_flag = '+deadline+' }',stem+'_close = yes\nset_country_flag = ac_fsb_case_expired')
    effect('ac_fsb_recount_cases',guard('tag = SBK original_tag = SBK',recount))
    effect('ac_fsb_close_all_cases',guard('tag = SBK original_tag = SBK',close_all))
    effect('ac_fsb_case_tick',guard('tag = SBK original_tag = SBK',tick+'ac_fsb_recount_cases = yes'))
    build_adviser()

def build_adviser():
    valid='tag = SBK original_tag = SBK has_capitulated = no any_owned_state = { always = yes } country_exists = OSE NOT = { has_war_with = OSE } OR = { is_subject = no is_subject_of = OSE } OSE = { tag = OSE original_tag = OSE has_capitulated = no is_subject = no any_owned_state = { always = yes } }'
    trigger('ac_fsb_adviser_valid',valid)
    clear='clr_country_flag = ac_fsb_adviser_open\nclr_country_flag = ac_fsb_adviser_window\nclr_country_flag = ac_fsb_adviser_visit\nremove_ideas = ac_fsb_sbk_limited_adviser\nOSE = { clr_country_flag = ac_fsb_adviser_notice }\n'
    effect('ac_fsb_close_adviser',guard('tag = SBK original_tag = SBK',clear))
    condition=active('SBK')+' has_country_flag = ac_fsb_adviser_request ac_fsb_adviser_valid = yes ac_fsb_can_fund = yes political_power >= 15 check_variable = { ac_pol_capacity >= 1 } NOT = { has_country_flag = ac_fsb_adviser_open } NOT = { has_country_flag = ac_fsb_adviser_request_cooldown }'
    body='ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded','add_political_power = -15\n'+capacity(-1)+'set_country_flag = ac_fsb_adviser_open\nset_country_flag = { flag = ac_fsb_adviser_window days = 60 }\nset_country_flag = { flag = ac_fsb_adviser_request_cooldown days = 365 }\nOSE = { set_country_flag = ac_fsb_adviser_notice }')
    decision('SBK','request_adviser','Request a Limited Technical Adviser','Request advice from eligible Osea, or the actual Osean overlord if subject. Cost: 15 political power, 1 institutional capacity and the public programme fee. Sixty-day consent window, one-year request cooldown. No faction, guarantee, autonomy or border change is included.',condition,body,active('SBK')+' has_country_flag = ac_fsb_adviser_request',icon='docket')
    answer='tag = OSE original_tag = OSE has_country_flag = ac_fsb_adviser_notice country_exists = SBK SBK = { ac_fsb_active = yes ac_fsb_adviser_valid = yes has_country_flag = ac_fsb_adviser_open has_country_flag = ac_fsb_adviser_window }'
    idea('ac_fsb_sbk_limited_adviser','A Limited Technical Remit','An accepted 120-day technical visit, with a public staffing burden. It conveys no sovereign or military guarantee.',{'production_factory_efficiency_gain_factor':.035,'political_power_gain':-.05})
    decision('OSE','accept_sbk_adviser','Accept the Limited South Belkan Remit','Spend 10 political power and 1 institutional capacity. A 120-day technical visit follows; it confers no guarantee, faction membership or autonomy change.',answer+' ac_pol_active = yes political_power >= 10 check_variable = { ac_pol_capacity >= 1 }','add_political_power = -10\n'+capacity(-1)+'SBK = { ac_fsb_close_adviser = yes set_country_flag = ac_fsb_adviser_accepted set_country_flag = { flag = ac_fsb_adviser_visit days = 120 } add_timed_idea = { idea = ac_fsb_sbk_limited_adviser days = 120 } }',answer,icon='docket')
    decision('OSE','refuse_sbk_adviser','Decline the South Belkan Remit','Decline without a reward. The domestic inspection option remains useful to South Belka.',answer,'SBK = { set_country_flag = ac_fsb_adviser_refused ac_fsb_close_adviser = yes }',answer,icon='docket')
    idea('ac_fsb_sbk_domestic_inspection','Domestic Workshop Inspection','A domestic technical inspection has consumed real support stores and administrative costs; no external consent is required.',{'attrition':-.03,'production_factory_efficiency_gain_factor':.025})
    cond=active('SBK')+' has_country_flag = ac_fsb_adviser_request ac_fsb_can_fund = yes political_power >= 20 check_variable = { ac_pol_capacity >= 2 } '+stock_guard({'support_equipment':10})+' NOT = { has_country_flag = ac_fsb_domestic_inspection_cooldown }'
    decision('SBK','domestic_inspection','Inspect with Domestic Specialists','Pay 20 political power, 2 institutional capacity, the public programme fee and 10 support equipment for 120 days of domestic inspection. Available after refusal, while supervised, and without a foreign partner. 180-day cooldown.',cond,'ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded','add_political_power = -20\n'+capacity(-2)+spend_stock({'support_equipment':10})+'set_country_flag = { flag = ac_fsb_domestic_inspection_cooldown days = 180 }\nadd_timed_idea = { idea = ac_fsb_sbk_domestic_inspection days = 120 }'),active('SBK')+' has_country_flag = ac_fsb_adviser_request',icon='docket',preview=block('effect_tooltip','add_timed_idea = { idea = ac_fsb_sbk_domestic_inspection days = 120 }'))
    effect('ac_fsb_adviser_tick',guard('tag = SBK original_tag = SBK',guard('has_country_flag = ac_fsb_adviser_open OR = { ac_fsb_adviser_valid = no NOT = { has_country_flag = ac_fsb_adviser_window } }','ac_fsb_close_adviser = yes\nset_country_flag = ac_fsb_adviser_refused')+guard('has_country_flag = ac_fsb_adviser_visit ac_fsb_adviser_valid = no','ac_fsb_close_adviser = yes\nset_country_flag = ac_fsb_adviser_refused')))
    effect('ac_fsb_adviser_receiver_tick',guard('tag = OSE original_tag = OSE has_country_flag = ac_fsb_adviser_notice OR = { NOT = { country_exists = SBK } SBK = { ac_fsb_adviser_valid = no } SBK = { NOT = { has_country_flag = ac_fsb_adviser_open } } SBK = { NOT = { has_country_flag = ac_fsb_adviser_window } } }','clr_country_flag = ac_fsb_adviser_notice\nSBK = { ac_fsb_close_adviser = yes set_country_flag = ac_fsb_adviser_refused }'))
    effect('ac_fsb_adviser_receiver_interrupt',guard('tag = OSE original_tag = OSE','clr_country_flag = ac_fsb_adviser_notice\nSBK = { ac_fsb_close_adviser = yes remove_ideas = ac_fsb_sbk_limited_adviser set_country_flag = ac_fsb_adviser_refused }'))
