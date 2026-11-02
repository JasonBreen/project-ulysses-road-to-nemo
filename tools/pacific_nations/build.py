"""Compile independent national continuation modules with fresh SNP receipts.

The SNP owner alone spends/reserves/releases its work. This consumer owns only
its policies, request dates and narrative receipts; wars and projects are read.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from pacific_nations.model import HERE,MOD,countries,branches,refs,positions
from reconstruction.build import block,guard,modifiers,improve
from usea_expansion.script import parse,get
from port_1_19.pdx import children,strip_comments_mask

BEGIN='# BEGIN PACIFIC NATIONAL CONTINUATIONS';END='# END PACIFIC NATIONAL CONTINUATIONS'


def host(tag):return 'tag = '+tag+' original_tag = '+tag
def active(tag):return 'ac_snc_'+tag.lower()+'_active = yes'
def prefix(tag):return 'ac_snc_'+tag.lower()


def strip_imports(tree,tag):
    """Remove only the registered exact additions for older preservation gates."""
    expected={b.focus(i)for b in branches()if b.tag==tag for i in range(len(b.steps))}
    result=copy.deepcopy(tree)
    for kind,_,body in result:
        if kind!='focus_tree':continue
        found=[v for k,_,v in body if k=='shared_focus'and isinstance(v,str)and v.startswith(tag+'_snc_')]
        if expected and (len(found)!=len(expected)or set(found)!=expected):raise ValueError('Unregistered/missing continuation imports '+tag)
        body[:]=[r for r in body if not(r[0]=='shared_focus'and r[2]in expected)]
    return result


def attach(source,tag):
    expected={b.focus(i)for b in branches()if b.tag==tag for i in range(len(b.steps))}
    if source.count(BEGIN)!=source.count(END):raise ValueError('Unbalanced national continuation imports')
    replacements=[];mask=strip_comments_mask(source)
    for kind,_,_,a,z in children(source,0,len(source),mask):
        if kind!='focus_tree':continue
        body=source[a:z];imports=BEGIN+'\n'+''.join('\tshared_focus = '+b.focus(i)+'\n'for b in branches()if b.tag==tag for i in range(len(b.steps)))+'\t'+END
        if BEGIN in body:
            start=body.index(BEGIN);finish=body.index(END)+len(END)
            if any(k!='shared_focus'or v not in expected for k,_,v in parse(body[start:finish])):raise ValueError('Foreign node inside continuation seam')
            body=body[:start]+imports+body[finish:]
        else:body=body.rstrip()+'\n\n\t'+imports+'\n'
        replacements.append((a,z,body))
    if len(replacements)!=(2 if tag=='OSE'else 1):raise ValueError('National tree alternatives changed')
    for a,z,body in reversed(replacements):source=source[:a]+body+source[z:]
    return source


def outputs():
    out={};coords=positions();manifest=[]
    for module in countries():
        tag=module.TAG;p=prefix(tag);loc={};effects={};triggers={};focuses=[];ideas=[];events=[];custom=[];decisions=[];messages=[]
        def text(key,value):
            if key in loc:raise ValueError('Duplicate national localization '+key)
            loc[key]=value
        def idea(ident,title,description,values):
            text(ident,title);text(ident+'_desc',description)
            ideas.append(block(ident,'picture = '+ident+'\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n'+block('modifier',modifiers(values))))
        def message(number,title,prose,visible,callback=None):
            token=p+'_message_'+str(number);messages.append(token)
            condition=active(tag)+' has_country_flag = '+token+'_pending has_country_flag = '+token+'_window NOT = { has_country_flag = '+token+'_answered }'
            triggers[token+'_answerable']=condition
            desc=prose+('\n\n['+callback+']'if callback else'')
            text(token+'.t',title);text(token+'.d',desc)
            options=''
            for index,(label,benefit,cost)in enumerate((('Place the account before the public.',{'stability_factor':.01},{'political_power_gain':-.025}),('Keep a signed professional account.',{'air_mission_efficiency':.015},{'consumer_goods_factor':.003}))):
                ident=token+'_reply_'+str(index);kind='public'if index==0 else'staff';spirit=token+'_'+kind+'_spirit'
                idea(spirit,label,'The received account changes how the office answers for this work over the next ninety days. The selected benefit carries the continuing cost shown here.',{**benefit,**cost})
                text(ident,label);text(ident+'_tt','Retain the '+kind+' account as a persistent choice. For ninety days, apply the shown benefit and its distinct continuing cost.')
                action='set_country_flag = '+token+'_answered\nset_country_flag = '+token+'_'+kind+'\nclr_country_flag = '+token+'_pending\nclr_country_flag = '+token+'_window\nadd_timed_idea = { idea = '+spirit+' days = 90 }\n'
                effects[ident]=guard(condition,action)
                options+=block('option','name = '+ident+'\nai_chance = { factor = 50 }\n'+block('trigger',condition)+'custom_effect_tooltip = '+ident+'_tt\nshow_ideas_tooltip = '+spirit+'\n'+block('hidden_effect',ident+' = yes'))
            text(token+'_expired','Keep the unanswered account in the file.')
            options+=block('option','name = '+token+'_expired\n'+block('trigger','NOT = { '+condition+' }'))
            events.append(block('country_event','id = ac_snc_'+tag.lower()+'.'+str(number)+'\ntitle = '+token+'.t\ndesc = '+token+'.d\npicture = GFX_ac_snc_'+tag.lower()+'_event_'+str(number)+'\nis_triggered_only = yes\n'+block('trigger',condition)+options))
            effects[token+'_send']=guard(active(tag)+' '+visible+' NOT = { has_country_flag = '+token+'_sent }','set_country_flag = '+token+'_sent\nset_country_flag = '+token+'_pending\nset_country_flag = { flag = '+token+'_window days = 60 }\ncountry_event = { id = ac_snc_'+tag.lower()+'.'+str(number)+' days = 1 }')
            return token
        triggers[p+'_host']=host(tag)
        triggers[p+'_active']=host(tag)+' ac_snp_active = yes has_country_flag = '+p+'_initialized check_variable = { var = '+p+'_identity value = THIS.id compare = equals }'
        effects[p+'_initialize']=guard(host(tag)+' ac_snp_active = yes NOT = { has_country_flag = '+p+'_initialized }','set_variable = { '+p+'_identity = THIS.id }\nset_country_flag = '+p+'_initialized')
        sync=[];interrupt=[];tick=[];request_repairs=[]
        opening=message(1,module.OPENING_TITLE,module.OPENING,'OR = { '+' '.join('has_country_flag = '+b.focus(0)+'_done'for b in module.BRANCHES)+' }')
        for number,b in enumerate(module.BRANCHES):
            branch=b.id
            for lane,(_,benefit,cost)in enumerate(b.policies,1):
                ident=branch+('_civil'if lane==1 else'_protected')+'_spirit'
                idea(ident,b.policies[lane-1][0],b.steps[lane][1],{**benefit,**cost})
                idea(ident+'_settled',b.policies[lane-1][0]+': Standing Review',b.steps[-1][1],improve(benefit,cost))
                done=branch+('_civil'if lane==1 else'_protected')+'_done'
                sync.append(guard(active(tag)+' has_country_flag = '+done,guard('has_country_flag = '+branch+'_settlement_done','remove_ideas = '+ident+'\nadd_ideas = '+ident+'_settled')+block('else','remove_ideas = '+ident+'_settled\nadd_ideas = '+ident))+block('else','remove_ideas = '+ident+'\nremove_ideas = '+ident+'_settled'))
            if len(b.steps)==8:
                for suffix,title,values in(('public_return','Open receiving record',{'stability_factor':.008,'political_power_gain':-.02}),('staff_return','Protected professional return',{'army_org_factor':.01,'consumer_goods_factor':.003})):
                    ident=branch+'_'+suffix+'_spirit';idea(ident,title,b.steps[5 if suffix=='public_return'else 6][1],values)
                    sync.append(guard(active(tag)+' has_country_flag = '+branch+'_'+suffix+'_done','add_ideas = '+ident)+block('else','remove_ideas = '+ident))
            fresh=[]
            for lane in(1,2):
                receipt='ac_snp_'+tag.lower()+'_'+b.parent+'_'+str(lane)
                required=p+'_'+b.key+'_required_start_'+str(lane)
                condition='has_country_flag = '+branch+('_civil_done'if lane==1 else'_protected_done')+' has_variable = '+required+' has_variable = '+receipt+'_last_completed_serial has_variable = '+receipt+'_last_completed_started has_variable = '+receipt+'_last_completed_on has_variable = '+receipt+'_last_completed_identity check_variable = { var = '+receipt+'_last_completed_identity value = THIS.id compare = equals } check_variable = { var = '+receipt+'_last_completed_serial value = '+required+' compare = greater_than_or_equals } check_variable = { var = '+receipt+'_last_completed_started value = '+p+'_'+b.key+'_requested compare = greater_than_or_equals } check_variable = { var = '+receipt+'_last_completed_on value = date compare = less_than_or_equals }'
                fresh.append(block('AND',condition))
            request='set_variable = { '+p+'_'+b.key+'_requested = date }\nset_country_flag = '+branch+'_request_open\n'
            if len(b.steps)>4:
                required_fields=[]
                for lane in(1,2):
                    serial='ac_snp_'+tag.lower()+'_'+b.parent+'_'+str(lane)+'_start_serial';required=p+'_'+b.key+'_required_start_'+str(lane);required_fields.append('has_variable = '+required)
                    request+='set_variable = { '+required+' = 1 }\n'+guard('has_variable = '+serial,'set_variable = { '+required+' = '+serial+' }\nadd_to_variable = { '+required+' = 1 }')
                triggers[branch+'_fresh_work']=active(tag)+' has_country_flag = '+branch+'_request_open has_variable = '+p+'_'+b.key+'_requested '+block('OR',''.join(fresh))
                effects[branch+'_request']=guard(active(tag)+' has_country_flag = '+branch+'_protocol_done NOT = { has_country_flag = '+branch+'_review_done }',request)
                interrupt.append('clr_country_flag = '+branch+'_request_open\n')
                request_repairs.append(guard('has_country_flag = '+branch+'_request_open NOT = { AND = { '+' '.join(required_fields)+' } }','clr_country_flag = '+branch+'_request_open'))
            for i,suffix in enumerate(b.suffixes):
                ident=b.focus(i);title,description=b.steps[i];text(ident,title);text(ident+'_desc',description)
                requirements=refs(b,i)
                condition=active(tag)+' NOT = { date < '+b.opens+' } '
                condition+=(block('OR',' '.join('has_completed_focus = '+ref for ref in requirements))if len(requirements)>1 else' '.join('has_completed_focus = '+ref for ref in requirements))
                if suffix=='review':condition+=' '+branch+'_fresh_work = yes'
                if suffix=='brief'and number==5:condition+=' '+module.FINAL_REQUIREMENT
                other=branch+'_'+('protected'if suffix=='civil'else'civil'if suffix=='protected'else'staff_return'if suffix=='public_return'else'public_return')if suffix in('civil','protected','public_return','staff_return')else None
                if other:condition+=' NOT = { has_country_flag = '+other+'_done }'
                requirement_key=ident+'_requirements_tt'
                text(requirement_key,'From '+b.opens+', an active national administration and the required earlier work are available. '+('A corresponding selected-lane funded service must have genuinely completed after this branch requested its review.'if suffix=='review'else'The selected policy remains exclusive; conclusions remain available when their real prerequisites finish after the expected calendar.'))
                action='set_country_flag = '+ident+'_done\n'
                if suffix=='protocol':action+=request
                if suffix=='review':action+='clr_country_flag = '+branch+'_request_open\n'
                action+=p+'_sync_policies = yes\n'
                effects[ident+'_apply']=guard(condition+' NOT = { has_country_flag = '+ident+'_done }',action+p+'_narrative_tick = yes')
                summary=('Open a fresh review request. Complete the corresponding selected-lane SNP service after this request; existing payments and national reservations remain owned by that service.'if suffix=='protocol'else'Record the corresponding genuinely completed funded period after this branch requested it.'if suffix=='review'else'Improve the selected continuing policy by twenty percent while keeping its unfavorable cost.'if suffix=='settlement'else'Adopt the shown benefit with its distinct continuing political, civilian or readiness cost.'if suffix in('civil','protected','public_return','staff_return')else'Open the named national continuation from its earned prior settlement.')
                text(ident+'_effect_tt',summary);shown='custom_effect_tooltip = '+ident+'_effect_tt\n'
                if suffix in('civil','protected','public_return','staff_return'):shown+='show_ideas_tooltip = '+ident+'_spirit\n'
                x,y=coords[ident];body='id = '+ident+'\nicon = GFX_ac_snc_focus_'+ident+f'\nx = {x}\ny = {y}\ncost = '+('10'if suffix in('civil','protected','settlement')else'5')+'\n'
                body+=block('prerequisite',' '.join('focus = '+ref for ref in requirements))
                if other:body+=block('mutually_exclusive','focus = '+other)
                body+=block('available',block('custom_trigger_tooltip','tooltip = '+requirement_key+'\n'+condition))+'cancel_if_invalid = yes\ncontinue_if_invalid = no\nai_will_do = { factor = 12 }\n'+block('completion_reward',shown+block('hidden_effect',ident+'_apply = yes'))
                focuses.append(block('shared_focus',body));manifest.append(dict(id=ident,tag=tag,branch=b.key,stage=suffix,x=x,y=y))
            callback=branch+'_hearing_context';records=''
            hearing_ready='has_country_flag = '+branch+'_protocol_done'if len(b.steps)>4 else'OR = { has_country_flag = '+branch+'_civil_done has_country_flag = '+branch+'_protected_done }'
            hearing=message(10+number,b.steps[0][0]+': The Hearing',b.hearing,hearing_ready)
            for kind,prose in(('public','The earlier hearing was opened to public scrutiny. Its signed objections remain attached to this assessment.'),('staff','The earlier hearing kept a signed professional account. The names beneath it remain responsible for what was omitted.'),('missed','The invitation went unanswered. This assessment records delivered work without inventing an agreement that nobody signed.')):
                key=callback+'_'+kind;text(key,prose)
                records+=block('text',('trigger = { has_country_flag = '+hearing+'_'+kind+' }\n'if kind!='missed'else'')+'localization_key = '+key)
            custom.append(block('defined_text','name = '+callback+'\n'+records))
            message(20+number,b.steps[-1][0]+': The Return',b.assessment,'has_country_flag = '+branch+('_review_done'if len(b.steps)>4 else'_settlement_done'),callback)
            if len(b.steps)>4:
                ident=branch+'_renew';text(ident,'Renew: '+b.steps[0][0]);text(ident+'_desc','Reopen this interrupted review at the present date for ten political power and two institutional-capacity points. It requires a new corresponding funded period; no old work is retroactively credited and the service pays its own usual costs.')
                can=active(tag)+' has_country_flag = '+branch+'_protocol_done NOT = { has_country_flag = '+branch+'_review_done } NOT = { has_country_flag = '+branch+'_request_open } ac_pol_active = yes political_power >= 10 check_variable = { ac_pol_capacity >= 2 }'
                effects[ident]=guard(can,'add_political_power = -10\nset_temp_variable = { ac_pol_capacity_delta = -2 }\nac_pol_change_capacity = yes\n'+request)
                text(ident+'_effect_tt','Commit ten political power and two institutional-capacity points to reopen this interrupted review at the present date. A new corresponding funded service must still complete its usual paid work after this request.')
                text(ident+'_requirements_tt','This national review was interrupted before completion. Its protocol is complete, no replacement request is open, and ten political power plus two institutional-capacity points are available.')
                shown_can=block('custom_trigger_tooltip','tooltip = '+ident+'_requirements_tt\n'+can)
                decisions.append(block(ident,'icon = '+ident+'\nallowed = { '+host(tag)+' }\nvisible = { '+active(tag)+' has_country_flag = '+branch+'_protocol_done NOT = { has_country_flag = '+branch+'_review_done } NOT = { has_country_flag = '+branch+'_request_open } }\ncost = 0\ncustom_cost_text = '+p+'_renew_cost\n'+block('custom_cost_trigger',shown_can)+block('available',shown_can)+block('complete_effect','custom_effect_tooltip = '+ident+'_effect_tt\n'+block('hidden_effect',ident+' = yes'))+'ai_will_do = { base = 2 }'))
        final=message(30,module.CONCLUSION_TITLE,module.CONCLUSION,'has_country_flag = '+module.BRANCHES[-1].id+'_settlement_done')
        # Ineligible/annexed current work cannot be revived by a rapid return.
        for token in messages:
            interrupt.append(guard('has_country_flag = '+token+'_pending','set_country_flag = '+token+'_missed\nclr_country_flag = '+token+'_pending\nclr_country_flag = '+token+'_window'))
            tick.append(guard('has_country_flag = '+token+'_pending NOT = { has_country_flag = '+token+'_window }','set_country_flag = '+token+'_missed\nclr_country_flag = '+token+'_pending'))
        effects[p+'_interrupt']=guard(host(tag),'\n'.join(interrupt))
        effects[p+'_initialize']+=guard(active(tag),'\n'.join(request_repairs))
        effects[p+'_sync_policies']=guard(host(tag),'\n'.join(sync))
        effects[p+'_narrative_tick']=guard(active(tag),'\n'.join(token+'_send = yes'for token in messages))
        effects[p+'_weekly']=guard(host(tag),p+'_initialize = yes\n'+guard('NOT = { '+active(tag)+' }',p+'_interrupt = yes')+p+'_sync_policies = yes\n'+guard(active(tag),'\n'.join(tick)+'\n'+p+'_narrative_tick = yes'))
        for name,condition in module.PUBLIC_TRIGGERS.items():triggers[name]=active(tag)+' '+condition
        for name in triggers:
            if name in loc:continue
            label=('Established '+module.NAME+' administration'if name.endswith('_host')else
                'An active national review office'if name.endswith('_active')else
                'The hearing remains open for a reply'if name.endswith('_answerable')else
                'Corresponding fresh funded work is complete'if name.endswith('_fresh_work')else
                'An earned incident-verification account'if name.endswith('_verification_earned')else
                'Established civilian scientific cooperation'if name.endswith('_science_channel_earned')else
                'An earned receiving channel')
            text(name,label)
        hooks=block('on_startup',block('effect',tag+' = { ac_snp_initialize = yes '+p+'_initialize = yes }'))+block('on_weekly',block('effect',p+'_weekly = yes'))
        hooks+=block('on_annex',block('effect','FROM = { '+p+'_interrupt = yes }'))+block('on_capitulation_immediate',block('effect',p+'_interrupt = yes'))+block('on_subject_annexed',block('effect',p+'_interrupt = yes'))
        name='ac_snc_'+tag.lower()+'.txt';note='# Original national continuation; tools/pacific_nations. Native acceptance pending.\n'
        out['common/scripted_effects/'+name]=note+'\n'.join(block(k,v)for k,v in effects.items())
        out['common/scripted_triggers/'+name]=note+'\n'.join(block(k,v)for k,v in triggers.items())
        out['common/national_focus/'+name]=note+'\n'.join(focuses)
        out['common/ideas/'+name]=note+block('ideas',block('country','\n'.join(ideas)))
        out['common/on_actions/'+name]=note+block('on_actions',hooks)
        out['events/'+name]=note+'add_namespace = ac_snc_'+tag.lower()+'\n'+'\n'.join(events)
        out['common/custom_localization/'+name]=note+'\n'.join(custom)
        category=p+'_reviews';text(category,module.NAME+': Continuing National Reviews');text(category+'_desc','Reviews use the selected branch’s actual funded national programme. Interruptions require a present-day renewal rather than credit for a cancelled or historical period.')
        text(p+'_renew_cost','£pol_power 10 / 2 cap')
        out['common/decisions/categories/'+name]=block(category,'icon = GFX_ac_snc_category_'+tag.lower()+'\npriority = 44\nallowed = { '+host(tag)+' }\nvisible = { '+active(tag)+' }\nvisible_when_empty = yes')
        out['common/decisions/'+name]=block(category,'\n'.join(decisions))
        for source in list(out.values()):
            for flagname in re.findall(r'\b(?:has_country_flag|set_country_flag|clr_country_flag)\s*=\s*([A-Za-z0-9_]+)',source):
                if flagname not in loc and (flagname.startswith(p)or flagname.startswith(tag+'_snc_')):text(flagname,'National review: '+flagname.replace('_',' ').capitalize())
        out['localisation/english/ac_snc_'+tag.lower()+'_l_english.yml']='\ufeffl_english:\n'+'\n'.join(' '+k+':0 "'+v.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"'for k,v in loc.items())+'\n'
        original=MOD/'common/national_focus'/f'{tag}.txt';out['common/national_focus/'+tag+'.txt']=attach(original.read_text(encoding='utf-8-sig'),tag)
    return out,dict(schema=1,focuses=manifest,source_layer='Original provisional national procedures; no official officeholders or institutional claims',native_acceptance=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();out,manifest=outputs();failures=[]
    for relative,text in out.items():
        path=MOD/relative;data=text.encode('utf-8')
        if args.check:
            if not path.exists()or path.read_bytes().replace(b'\r\n',b'\n')!=data:failures.append(relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    path=HERE/'manifest.json';data=(json.dumps(manifest,indent=2)+'\n').encode()
    if args.check:
        if not path.exists()or path.read_bytes().replace(b'\r\n',b'\n')!=data:failures.append('tools/pacific_nations/manifest.json')
    else:path.write_bytes(data)
    if failures:raise SystemExit('Stale national continuation: '+', '.join(failures))
    print(str(len(manifest['focuses']))+' national continuation focuses; actual SNP receipts retained; native untested')


if __name__=='__main__':main()
