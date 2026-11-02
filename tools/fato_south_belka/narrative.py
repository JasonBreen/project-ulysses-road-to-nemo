"""Twenty substantive scenes, rechecked options and deliberately shared art.

All dialogue is original provisional fiction. Old historical FAT briefs are
archived after their act; contemporary SBK entry scenes never backdate aid.
"""
from content import FOCUSES
from fato_south_belka_builder import (block,guard,loc,done,active,capacity,idea,effect,EVENTS)

# number: art, first/last eligible dates, first option, second option, modifiers.
SCENES={
 1:('FAT_allocation',None,'1995.1.1','Put the public allocation record on the table.','Let the executive office reconcile the urgent orders.',
    {'stability_factor':.02,'industrial_capacity_factory':-.015},{'industrial_capacity_factory':.025,'political_power_gain':-.075}),
 2:('FAT_allocation',None,'1995.1.1','Accept locally verified border receipts.','Require a central review of every exception.',
    {'production_speed_buildings_factor':.025,'political_power_gain':-.05},{'stability_factor':.02,'production_speed_buildings_factor':-.015}),
 3:('FAT_freight',None,'1995.1.1','Publish the ceiling before accepting another request.','Permit a disclosed emergency exception for one interval.',
    {'stability_factor':.025,'industrial_capacity_factory':-.02},{'industrial_capacity_factory':.035,'consumer_goods_factor':.01,'stability_factor':-.01}),
 4:('FAT_consent','1995.1.1','2006.1.1','Respect the refusal and reserve the batch at home.','Pay for a smaller, freshly consented request procedure.',
    {'training_time_factor':-.025,'political_power_gain':-.05},{'political_power_gain':.05,'industrial_capacity_factory':-.02}),
 5:('FAT_allocation','1995.1.1','2006.1.1','Protect the maintenance interval.','Fund a limited replacement surge.',
    {'attrition':-.03,'industrial_capacity_factory':-.025},{'production_factory_efficiency_gain_factor':.04,'consumer_goods_factor':.01}),
 6:('FAT_consent','1995.1.1','2006.1.1','Hear the household repair invoices first.','Give the current industrial obligations the first hearing.',
    {'stability_factor':.025,'industrial_capacity_factory':-.02},{'production_speed_buildings_factor':.03,'political_power_gain':-.075}),
 7:('FAT_freight','1995.1.1','2006.1.1','Close the disputed local account with the record published.','Retain a funded inspection staff for one review interval.',
    {'stability_factor':.02,'political_power_gain':-.05},{'production_factory_efficiency_gain_factor':.035,'industrial_capacity_factory':-.015}),
 8:('FAT_hearing','2006.1.1','2013.1.1','Renew the public mandate with an independent hearing.','Renew a bounded executive mandate and its visible burden.',
    {'stability_factor':.025,'production_speed_buildings_factor':-.015},{'production_speed_buildings_factor':.035,'consumer_goods_factor':.01}),
 9:('FAT_hearing','2006.1.1','2013.1.1','Fund an independent inspection of the failed supplier.','Disclose the failure and authorise a limited local repair.',
    {'production_factory_efficiency_gain_factor':.035,'political_power_gain':-.05},{'attrition':-.025,'industrial_capacity_factory':-.02}),
 10:('FAT_hearing','2013.1.1',None,'Keep accountable cooperation within the published limit.','Close the external account and maintain a domestic mandate.',
    {'army_org_factor':.02,'political_power_gain':-.05},{'production_speed_buildings_factor':.03,'industrial_capacity_factory':-.015}),
 101:('SBK_registry',None,None,'Open the register to residents and witnesses.','Let the present office verify the first urgent files.',
    {'stability_factor':.025,'political_power_gain':-.05},{'production_speed_buildings_factor':.025,'consumer_goods_factor':.005}),
 102:('SBK_workshop',None,None,'Fund a verified utility-maintenance priority.','Protect an interim service while the parts are conserved.',
    {'production_speed_buildings_factor':.035,'consumer_goods_factor':.01},{'supply_consumption_factor':-.02,'stability_factor':-.01}),
 103:('SBK_remit',None,None,'Prepare a request for a narrowly permitted adviser.','Keep the inspection domestic and publish its limits.',
    {'production_factory_efficiency_gain_factor':.025,'political_power_gain':-.05},{'stability_factor':.02,'industrial_capacity_factory':-.015}),
 104:('SBK_registry',None,None,'Reconstruct household files with local witnesses.','Protect uncertain files under an interim register.',
    {'stability_factor':.025,'consumer_goods_factor':.005},{'political_power_gain':.04,'production_speed_buildings_factor':-.015}),
 105:('SBK_hearing','1995.1.1',None,'Publish a narrower remit for local security work.','Fund a supervised inspection of the present procedure.',
    {'stability_factor':.025,'army_org_factor':-.01},{'army_org_factor':.025,'political_power_gain':-.075}),
 106:('SBK_remit','1995.1.1',None,'Seek only the technical authority the counterpart can consent to.','Proceed with a domestic hearing after any refusal.',
    {'production_factory_efficiency_gain_factor':.025,'consumer_goods_factor':.005},{'stability_factor':.025,'industrial_capacity_factory':-.015}),
 107:('SBK_workshop','2006.1.1',None,'Require a public review before the next standing budget.','Fund a professional bench for the technical files.',
    {'stability_factor':.03,'production_speed_buildings_factor':-.02},{'production_speed_buildings_factor':.04,'political_power_gain':-.1}),
 108:('SBK_hearing','1995.1.1',None,'Protect an interim arrangement for the unproved claim.','Pay for a further inquiry and keep the claim unresolved.',
    {'stability_factor':.02,'political_power_gain':-.05},{'production_factory_efficiency_gain_factor':.025,'consumer_goods_factor':.005}),
 109:('SBK_remit','2006.1.1',None,'State the local remit and decline the incompatible order.','Disclose the conflict and seek limited external coordination.',
    {'stability_factor':.025,'army_org_factor':-.01},{'army_org_factor':.02,'consumer_goods_factor':.005}),
 110:('SBK_hearing','2013.1.1',None,'Keep an accountable civil promise within present authority.','Keep a narrower interim administration and its right of appeal.',
    {'stability_factor':.03,'political_power_gain':-.05},{'production_speed_buildings_factor':.025,'industrial_capacity_factory':-.01}),
}

def dates(first,last):
    return ('date > '+first+' ' if first else '')+('date < '+last+' ' if last else '')

def build_narrative():
    tick=''
    for row in (r for r in FOCUSES if r.kind=='scene'):
        number=int(row.hook);art,first,last,a,b,mods_a,mods_b=SCENES[number];stem='ac_fsb_scene_'+str(number);seen=stem+'_seen';pending=stem+'_pending';window=stem+'_window'
        eligible=active(row.tag)+' '+dates(first,last)+'NOT = { has_country_flag = '+seen+' }'
        queue='set_country_flag = '+pending+'\nset_country_flag = { flag = '+window+' days = 30 }\ncountry_event = { id = ac_fsb.'+str(number)+' days = 1 }\n'
        effect(stem+'_queue',guard(eligible+' NOT = { has_country_flag = '+pending+' }',queue)+
            (guard(active(row.tag)+' NOT = { date < '+last+' }','set_country_flag = '+seen+'\nset_country_flag = '+stem+'_archived') if last else ''))
        answer=eligible+' has_country_flag = '+pending+' has_country_flag = '+window
        ident='ac_fsb.'+str(number);loc(ident+'.t',row.title)
        # Present authority is explicit in every route, without imposing an
        # official constitution, leader term or new treaty on inherited data.
        base=row.narrative+'\n\nThe allocation office must use the authority, stores and territory actually held. This hearing neither changes the established settlement nor creates a military obligation.'
        loc(ident+'.d',base)
        loc(ident+'.d.subject',base+'\n\nExternal supervision limits the promise. The local domestic arrangement remains useful; no independence or guarantee is conferred.')
        loc(ident+'.d.war',base+'\n\nThe current fighting makes replacement costs immediate. The hearing governs this national office, not the war\'s outcome.')
        loc(ident+'.d.peace',base+'\n\nPeace leaves a real maintenance and administrative choice. No battle or victory is assumed for the account.')
        event='id = '+ident+'\ntitle = '+ident+'.t\npicture = GFX_ac_fsb_event_'+art+'\nis_triggered_only = yes\n'+block('trigger',answer)
        event+=block('desc','text = '+ident+'.d.subject\ntrigger = { is_subject = yes }')
        event+=block('desc','text = '+ident+'.d.war\ntrigger = { is_subject = no has_war = yes }')
        event+=block('desc','text = '+ident+'.d.peace\ntrigger = { is_subject = no has_war = no }')
        for index,(label,mods) in enumerate(((a,mods_a),(b,mods_b))):
            letter='a' if index==0 else 'b';name=ident+'.'+letter;loc(name,label)
            spirit=stem+'_'+letter;idea(spirit,row.title+': '+('reviewed allocation' if index==0 else 'limited alternative'),
                'Original national scene choice. A 180-day policy interval with a stated countervailing burden; no historical preparation, stock, territory or force grant.',mods)
            # The full first option is costed; the modest alternative keeps a
            # low-cash country able to conclude the scene without a fiscal fee.
            condition=answer+(' ac_fsb_can_fund = yes political_power >= 15 check_variable = { ac_pol_capacity >= 2 }' if index==0 else ' political_power >= 5 check_variable = { ac_pol_capacity >= 1 }')
            body='clr_country_flag = '+pending+'\nclr_country_flag = '+window+'\nset_country_flag = '+seen+'\nset_country_flag = '+stem+'_'+letter+'_chosen\nadd_political_power = '+('-15' if index==0 else '-5')+'\n'+capacity(-2 if index==0 else -1)+'add_timed_idea = { idea = '+spirit+' days = 180 }\n'
            # These choices additionally affect a concrete ongoing permission.
            if number==4:body+='set_country_flag = '+('ac_fsb_offer_refused' if index==0 else 'ac_fsb_small_warrant')+'\n'
            if number==10 and index==1:body+='ac_fsb_close_all_warrants = yes\nset_country_flag = ac_fsb_external_closed\n'
            if number==102 and index==1:body+='set_country_flag = ac_fsb_interim_service\n'
            if number==104 and index==0:body+='set_country_flag = ac_fsb_local_witnesses\n'
            if number in (103,106) and index==1:body+='set_country_flag = ac_fsb_adviser_refused\n'
            if number==109 and index==0:body+='ac_fsb_close_adviser = yes\nset_country_flag = ac_fsb_adviser_refused\n'
            if index==0:body='ac_fsb_pay = yes\n'+guard('has_country_flag = ac_fsb_payment_succeeded',body)
            effect(stem+'_'+letter+'_choose',guard(condition,body))
            tip=name+'_tt';loc(tip,('Pay 15 political power, 2 institutional capacity and the public programme fee where enabled.' if index==0 else 'Pay 5 political power and 1 institutional capacity; this limited alternative requires no fiscal payment.')+' Adopt the shown policy for 180 days. Repeated, expired or interrupted choices are inert.')
            event+=block('option','name = '+name+'\n'+block('trigger',condition)+'ai_chance = { factor = '+('60' if index==0 else '40')+' }\ncustom_effect_tooltip = '+tip+'\n'+block('effect_tooltip','add_ideas = '+spirit)+block('hidden_effect',stem+'_'+letter+'_choose = yes'))
        # Closing an unaffordable scene is a real no-award choice, not a soft
        # lock or a hidden grant. It retains the archive and permits progression.
        loc(ident+'.c','Record that no funded mandate could be reached.')
        effect(stem+'_defer',guard(answer,'clr_country_flag = '+pending+'\nclr_country_flag = '+window+'\nset_country_flag = '+seen+'\nset_country_flag = '+stem+'_unfunded'))
        event+=block('option','name = '+ident+'.c\nai_chance = { factor = 1 }\n'+block('hidden_effect',stem+'_defer = yes'))
        EVENTS.append(block('country_event',event))
        expire='NOT = { has_country_flag = '+window+' }'
        if last:expire='OR = { '+expire+' NOT = { date < '+last+' } }'
        tick+=guard('tag = '+row.tag+' has_country_flag = '+pending+' '+expire,'clr_country_flag = '+pending+'\nset_country_flag = '+seen+'\nset_country_flag = '+stem+'_archived')
    effect('ac_fsb_narrative_tick',tick)
