"""Costed domestic allocations and removable standing commitments.

Domestic work remains useful under supervision, refusal and peaceful outcomes.
Only the public P1 payment and signed commitment/capacity interfaces are used.
"""
from content import FOCUSES,POLICIES
from fato_south_belka_builder import (block,guard,done,active,capacity,idea,decision,effect,trigger,IDEAS)

# hook: modifiers, duration (0 = standing), stock consumed, family, cadence.
ALLOCATIONS={
 'invoice_audit':({},0,{},'audit',180),
 'maintenance_interval':({'attrition':-.03,'industrial_capacity_factory':-.03},120,{},'shift',180),
 'extra_shift':({'industrial_capacity_factory':.05,'consumer_goods_factor':.01,'stability_factor':-.01},90,{},'shift',180),
 'loading_gauges':({'supply_consumption_factor':-.025,'civilian_factory_use':1},90,{},'transport',120),
 'domestic_training':({'army_experience_gain_mult':.05,'training_time_factor':-.025},120,{'infantry_equipment':100},'training',180),
 'relief_freight':({'supply_consumption_factor':-.035,'civilian_factory_use':1},120,{'motorized_equipment':10},'transport',180),
 'civil_reception':({'stability_factor':.02,'consumer_goods_factor':.01},180,{},'reception',240),
 'rest_interval':({'attrition':-.04,'training_time_factor':-.025,'industrial_capacity_factory':-.04},120,{},'shift',180),
 'support_maintenance':({'attrition':-.04,'army_org_factor':.015},120,{'support_equipment':15},'maintenance',180),
 'supervised_liaison':({'production_speed_buildings_factor':.04,'political_power_gain':-.1},180,{},'liaison',240),
 'line_continuity':({'production_factory_efficiency_gain_factor':.04,'production_factory_max_efficiency_factor':.02,'political_power_gain':-.1},120,{},'shift',180),
 'local_reconciliation':({},0,{},'reconcile',0),
 'skill_retention':({'production_factory_efficiency_gain_factor':.05,'training_time_factor':-.04,'consumer_goods_factor':.01},180,{},'shift',240),
 'suspend_warrants':({},0,{},'close',0),
 'independent_audit':({'political_power_gain':.05,'industrial_capacity_factory':-.02},0,{},'standing',0),
 'sweep_warrants':({},0,{},'sweep',30),
 'succession_review':({},0,{},'succession',0),
 'commitment_review':({'political_power_gain':.08,'industrial_capacity_factory':-.03},180,{},'review',240),
 'final_mandate':({},0,{},'final',0),
 'verify_receipts':({},0,{},'verification',0),
 'civil_charter':({'stability_factor':.02,'political_power_gain':-.05},0,{},'standing',0),
 'civil_instruction':({'army_org_factor':.025,'training_time_factor':-.03},120,{'support_equipment':10},'instruction',180),
 'maintenance_account':({'production_speed_buildings_factor':.04,'consumer_goods_factor':.005},0,{},'standing',0),
 'interruption_review':({},0,{},'interruption',0),
 'service_account':({'attrition':-.025,'consumer_goods_factor':.005},0,{},'standing',0),
 'relief_review':({'stability_factor':.02,'political_power_gain':-.05},120,{},'relief',180),
 'security_remit':({'stability_factor':.02,'army_org_factor':-.01},0,{},'standing',0),
 'workshop_round':({'production_factory_efficiency_gain_factor':.04,'attrition':-.025},120,{'support_equipment':10},'workshop',180),
 'archive_index':({},0,{},'archive',0),
 'public_interest':({},0,{},'remove',0),
 'final_arrangement':({},0,{},'final',0),
}
STANDING={r.hook:r.tag for r in FOCUSES if r.kind=='action' and r.hook in ALLOCATIONS and ALLOCATIONS[r.hook][0] and ALLOCATIONS[r.hook][1]==0}

def stock_guard(stocks):return ' '.join('has_equipment = { '+k+' > '+str(v-1)+' }' for k,v in stocks.items())
def spend_stock(stocks):return ''.join('add_equipment_to_stockpile = { type = '+k+' amount = -'+str(v)+' }\n' for k,v in stocks.items())
def stock_text(stocks):return ', '.join(str(v)+' '+k.replace('_',' ') for k,v in stocks.items()) or 'none'

def build_actions():
    assert set(ALLOCATIONS)=={r.hook for r in FOCUSES if r.kind=='action'}
    family_members={}
    for row in (r for r in FOCUSES if r.kind=='action'):
        tag,hook=row.tag,row.hook;mods,days,stocks,family,cadence=ALLOCATIONS[hook]
        ident='ac_fsb_'+tag.lower()+'_'+hook;mark=ident+'_used';cool='ac_fsb_'+tag.lower()+'_'+family+'_cooldown'
        paid=hook not in ('suspend_warrants','sweep_warrants','public_interest','interruption_review')
        pp=20 if paid else 0
        once=cadence==0 and hook not in ('suspend_warrants','public_interest','interruption_review') and hook not in STANDING
        condition=active(tag)+' '+done(tag,row.suffix)
        visible=condition
        if once:condition+=' NOT = { has_country_flag = '+mark+' }';visible+=' NOT = { has_country_flag = '+mark+' }'
        if cadence:condition+=' NOT = { has_country_flag = '+cool+' }'
        if hook in STANDING:condition+=' NOT = { has_country_flag = ac_fsb_'+hook+'_standing }'
        if paid:condition+=' ac_fsb_can_fund = yes political_power >= '+str(pp)+' check_variable = { ac_pol_capacity >= 2 }'
        if stocks:condition+=' '+stock_guard(stocks)
        if mods and days:
            for old in family_members.get((tag,family),[]):condition+=' NOT = { has_idea = '+old+' }'
            # Reverse guard every family peer, including later authored rows.
            for peer in FOCUSES:
                if peer.kind=='action' and peer.tag==tag and peer.hook!=hook and ALLOCATIONS[peer.hook][3]==family and ALLOCATIONS[peer.hook][0]:
                    condition+=' NOT = { has_idea = ac_fsb_'+tag.lower()+'_'+peer.hook+' }'
            condition+=' NOT = { has_idea = '+ident+' }'
        if hook=='suspend_warrants':condition+=' check_variable = { ac_fsb_warrants_open > 0 }'
        if hook=='public_interest':condition+=' OR = { '+' '.join('has_country_flag = ac_fsb_'+h+'_standing' for h,t in STANDING.items() if t==tag)+' }'
        if hook=='interruption_review':condition+=' check_variable = { ac_fsb_cases_open > 0 }'
        if hook=='relief_review':condition+=' OR = { has_country_flag = ac_pwi_local_response AND = { NOT = { has_global_flag = ac_postwar_contract_started } has_war = no } }'
        body='set_country_flag = '+mark+'\n'
        if cadence:body+='set_country_flag = { flag = '+cool+' days = '+str(cadence)+' }\n'
        if paid:body+='add_political_power = -'+str(pp)+'\n'+capacity(-2)
        body+=spend_stock(stocks)
        if mods:
            idea(ident,row.title,row.narrative,mods);family_members.setdefault((tag,family),[]).append(ident)
            if days:body+='add_timed_idea = { idea = '+ident+' days = '+str(days)+' }\n'
            else:body+='add_ideas = '+ident+'\nset_country_flag = ac_fsb_'+hook+'_standing\nset_country_flag = ac_fsb_fiscal_dirty\nac_fsb_sync_commitments = yes\n'
        if hook=='invoice_audit':body+='set_country_flag = ac_fsb_invoice_verified\n'+capacity(5)
        elif hook=='local_reconciliation':body+='ac_fsb_warrant_tick = yes\n'+capacity(6)
        elif hook in ('suspend_warrants','succession_review'):body+='ac_fsb_close_all_warrants = yes\nset_country_flag = ac_fsb_external_closed\n'
        elif hook=='sweep_warrants':body+='ac_fsb_warrant_tick = yes\n'
        elif hook=='commitment_review':body+=capacity(6)
        elif hook=='verify_receipts':body+='set_country_flag = ac_fsb_verified_receipts\n'
        elif hook=='archive_index':body+='set_country_flag = ac_fsb_indexed_archive\n'
        elif hook=='interruption_review':body+='ac_fsb_close_all_cases = yes\nset_country_flag = ac_fsb_interruption_recorded\n'
        elif hook=='public_interest':body+='ac_fsb_remove_standing = yes\n'
        elif hook=='final_mandate':
            for suffix,mods2 in [('supervised',{'stability_factor':.025,'political_power_gain':-.05}),('cooperative',{'army_org_factor':.02,'consumer_goods_factor':.005}),('domestic',{'production_speed_buildings_factor':.03,'industrial_capacity_factory':-.01})]:
                idea(ident+'_'+suffix,row.title+': '+suffix,'The final assessment records the actual relationship and delivery history, not a new faction or war outcome.',mods2)
            body+=guard('is_subject = yes','add_timed_idea = { idea = '+ident+'_supervised days = 365 }')+block('else_if',block('limit','check_variable = { ac_fsb_deliveries > 0 }')+'add_timed_idea = { idea = '+ident+'_cooperative days = 365 }')+block('else','add_timed_idea = { idea = '+ident+'_domestic days = 365 }')
        elif hook=='final_arrangement':
            for suffix,mods2 in [('supervised',{'stability_factor':.03,'political_power_gain':-.05}),('domestic',{'production_speed_buildings_factor':.03,'consumer_goods_factor':.005}),('accountable',{'stability_factor':.02,'army_org_factor':.015}),('interim',{'stability_factor':.01,'production_speed_buildings_factor':.02,'political_power_gain':-.05})]:
                idea(ident+'_'+suffix,row.title+': '+suffix,'The civil assessment uses the authority and cases actually held; reintegration remains with its existing owner.',mods2)
            body+=guard('is_subject = yes','add_timed_idea = { idea = '+ident+'_supervised days = 365 }')+block('else_if',block('limit','has_country_flag = ac_fsb_adviser_refused NOT = { has_country_flag = ac_fsb_adviser_accepted }')+'add_timed_idea = { idea = '+ident+'_domestic days = 365 }')+block('else_if',block('limit','check_variable = { ac_fsb_cases_resolved > 0 }')+'add_timed_idea = { idea = '+ident+'_accountable days = 365 }')+block('else','add_timed_idea = { idea = '+ident+'_interim days = 365 }')
        desc=row.purpose+'\n\n'
        if paid:desc+='Cost: '+str(pp)+' political power, 2 institutional capacity, and the public programme fee where enabled. '
        else:desc+='Administrative closure only: no cash or completion award. '
        if stocks:desc+='Consume actual stock: '+', '.join(str(v)+' '+k.replace('_',' ') for k,v in stocks.items())+'. '
        if days:desc+='Benefit lasts '+str(days)+' days. '+('Related allocations cannot overlap. ' if family in ('shift','transport') else '')
        if cadence:desc+='New authorisations have a '+str(cadence)+'-day cooldown. '
        if once:desc+='This authorisation is once only; interruption does not refund its costs. '
        if hook in STANDING:desc+='Standing full-mode annual commitment: nominal GDP / 2000, recorded exactly when the standing account is reconciled. Remove it through the campaign review. Legacy and disabled modes retain the political/physical burden without a new cash commitment.'
        if paid:body='ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded',body)
        preview=block('effect_tooltip',('add_timed_idea = { idea = '+ident+' days = '+str(days)+' }') if days else 'add_ideas = '+ident) if mods else ''
        decision(tag,hook,row.title,desc,condition,body,visible,weight=1,preview=preview)
    # Annexation suspends only this owner's ideas. A surviving/released country
    # may pay to reinstate its latest earned policy in each family; completed
    # focuses are not rerun and superseded acts cannot stack their old rewards.
    for row in (r for r in FOCUSES if r.kind=='policy'):
        family=POLICIES[row.hook][1];ident='ac_fsb_'+row.tag.lower()+'_'+row.hook
        later=[r for r in FOCUSES if r.tag==row.tag and r.kind=='policy' and POLICIES[r.hook][1]==family and r.phase>row.phase]
        condition=active(row.tag)+' '+done(row.tag,row.suffix)+' NOT = { has_idea = '+ident+' } political_power >= 15 check_variable = { ac_pol_capacity >= 1 }'
        condition+=''.join(' NOT = { '+done(row.tag,r.suffix)+' }' for r in later)
        restore='add_political_power = -15\n'+capacity(-1)+''.join('remove_ideas = ac_fsb_'+t.lower()+'_'+key+'\n' for key,(t,f,_) in POLICIES.items() if t==row.tag and f==family)+'add_ideas = '+ident
        decision(row.tag,'restore_'+row.hook,'Review the surviving policy: '+row.title,
                'Spend 15 political power and 1 institutional capacity to reinstate the latest completed policy in this family after an interruption. Its original continuing burden applies. No focus, stock, industry, expired scene or political identity is replayed.',condition,restore,condition,weight=1,preview=block('effect_tooltip','add_ideas = '+ident))
    # Capability-gated domestic alternatives are actual stock allocations, not
    # refusal rewards. They work even if the foreign system was never used.
    for hook,title,stocks,condition,mods in [
        ('support_reserve','Allocate Support Stores at Home',{'support_equipment':10},'has_country_flag = ac_fsb_domestic_support',{'attrition':-.03,'army_org_factor':.015}),
        ('transport_reserve','A Domestic Transport Interval',{'motorized_equipment':10},'OR = { has_country_flag = ac_fsb_routine_transport AND = { has_country_flag = ac_fsb_interrupted_transport has_country_flag = ac_fsb_external_closed } }',{'supply_consumption_factor':-.03,'civilian_factory_use':1}),
        ('refused_reserve','Keep a Refused Batch for Training',{'infantry_equipment':100},'has_country_flag = ac_fsb_refused_domestic has_country_flag = ac_fsb_offer_refused',{'army_experience_gain_mult':.05,'training_time_factor':-.03}),
        ('reception_liaison','Fund the Local Relief Liaison',{},'has_country_flag = ac_fsb_pwi_liaison OR = { has_country_flag = ac_pwi_local_response AND = { NOT = { has_global_flag = ac_postwar_contract_started } has_war = no } }',{'stability_factor':.025,'consumer_goods_factor':.01})]:
        ident='ac_fsb_fat_'+hook;idea(ident,title,'A paid domestic allocation; no foreign refusal, settlement or historical preparation reward is minted.',mods)
        cond=active('FAT')+' '+condition+' ac_fsb_can_fund = yes political_power >= 20 check_variable = { ac_pol_capacity >= 2 } '+stock_guard(stocks)+' NOT = { has_country_flag = ac_fsb_domestic_reserve_cooldown } NOT = { has_idea = '+ident+' }'
        body='ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded','add_political_power = -20\n'+capacity(-2)+spend_stock(stocks)+'set_country_flag = { flag = ac_fsb_domestic_reserve_cooldown days = 180 }\nadd_timed_idea = { idea = '+ident+' days = 120 }')
        decision('FAT',hook,title,'Pay 20 political power, 2 institutional capacity and the public programme fee, plus listed physical stores. A 120-day domestic allocation with a shared 180-day cooldown; no refund or free replacement stock. Stores: '+stock_text(stocks)+'.',cond,body,active('FAT')+' '+condition,preview=block('effect_tooltip','add_timed_idea = { idea = '+ident+' days = 120 }'))

def build_commitments():
    flags=' '.join('has_country_flag = ac_fsb_'+hook+'_standing' for hook in STANDING)
    remove=''
    for hook,tag in STANDING.items():remove+='clr_country_flag = ac_fsb_'+hook+'_standing\nremove_ideas = ac_fsb_'+tag.lower()+'_'+hook+'\n'
    effect('ac_fsb_remove_standing',guard('ac_fsb_participant = yes check_variable = { ac_fsb_identity = THIS.id }',remove+'set_country_flag = ac_fsb_fiscal_dirty\nac_fsb_sync_commitments = yes'))
    # The exact prior snapshot is subtracted through the owner. Landless
    # accounts defer this until readiness returns, without touching their debt.
    sync='set_temp_variable = { ac_macro_commitment_delta = ac_fsb_fiscal_applied }\nmultiply_temp_variable = { ac_macro_commitment_delta = -1 }\nac_macro_change_commitment = yes\nset_variable = { ac_fsb_fiscal_applied = 0 }\n'
    for hook,tag in STANDING.items():
        sync+=guard('tag = '+tag+' has_country_flag = ac_fsb_'+hook+'_standing',
            'set_temp_variable = { ac_fsb_commitment_piece = ac_macro_nominal_gdp }\ndivide_temp_variable = { ac_fsb_commitment_piece = 2000 }\nadd_to_variable = { ac_fsb_fiscal_applied = ac_fsb_commitment_piece }')
    sync+='set_temp_variable = { ac_macro_commitment_delta = ac_fsb_fiscal_applied }\nac_macro_change_commitment = yes\nclr_country_flag = ac_fsb_fiscal_dirty\n'
    effect('ac_fsb_sync_commitments',guard('ac_fsb_participant = yes check_variable = { ac_fsb_identity = THIS.id } has_country_flag = ac_fsb_fiscal_dirty ac_macro_ready = yes',sync))
    clear='ac_fsb_close_all_warrants = yes\nac_fsb_close_all_cases = yes\nac_fsb_close_adviser = yes\nac_fsb_remove_standing = yes\nset_country_flag = ac_fsb_interrupted\nset_country_flag = ac_fsb_external_closed\n'
    clear+=''.join('remove_ideas = '+ident+'\n' for ident in IDEAS)
    for i in list(range(1,11))+list(range(101,111)):
        stem='ac_fsb_scene_'+str(i)
        clear+=guard('has_country_flag = '+stem+'_pending','clr_country_flag = '+stem+'_pending\nclr_country_flag = '+stem+'_window\nset_country_flag = '+stem+'_seen\nset_country_flag = '+stem+'_cancelled')
    effect('ac_fsb_interrupt',guard('ac_fsb_participant = yes has_country_flag = ac_fsb_initialized check_variable = { ac_fsb_identity = THIS.id }',clear))
    effect('ac_fsb_status_interrupt',guard('ac_fsb_participant = yes','ac_fsb_close_all_warrants = yes\nac_fsb_close_adviser = yes\nset_country_flag = ac_fsb_external_closed'))
