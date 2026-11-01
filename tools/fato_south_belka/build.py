"""Compile FAT54/SBK42. --check is read-only; national owners consume P1 APIs.

No private financial stocks, factories, territorial changes, force grants,
war/faction outcomes or leader replacements are authored by this compiler.
"""
import argparse
import json
import re
from pathlib import Path
import sys
from content import COUNTRIES, FOCUSES, POLICIES

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.modules.setdefault('fato_south_belka_builder',sys.modules[__name__])
OUT={};LOC={};EFFECTS={};TRIGGERS={};IDEAS={};DECISIONS={};EVENTS=[]

def block(key,body):return key+' = {\n'+''.join(('\t'+line.rstrip() if line.strip() else '')+'\n' for line in body.splitlines())+'}\n'
def guard(condition,body):return block('if',block('limit',condition)+body)
def loc(key,value):
    if key in LOC and LOC[key]!=value:raise ValueError('Conflicting localisation '+key)
    LOC[key]=value
def effect(key,body):
    if key in EFFECTS:raise ValueError('Duplicate national effect '+key)
    EFFECTS[key]=body
def trigger(key,body):
    if key in TRIGGERS:raise ValueError('Duplicate national trigger '+key)
    descriptions={
        'ac_fsb_participant':'The current country is FATO or South Belka under its own established identity.',
        'ac_fsb_active':'The national administration is registered, present, not capitulated and able to administer at least one fully controlled owned state.',
        'ac_fsb_can_fund':'The public programme fee can be paid: 0.002 abstract billion in full mode or 2 fiscal units in experimental mode. Disabled fiscal rules require no cash.',
        'ac_fsb_has_warrant_slot':'There is a free slot within the earned limit of one, two or three open warrants. Pending and accepted warrants both occupy a slot.',
        'ac_fsb_has_case_slot':'There is a free slot within the earned limit of one or two open civil cases.',
        'ac_fsb_adviser_valid':'South Belka and Osea are present, not capitulated and not at war with one another. Osea is independent; South Belka is independent or actually subject to Osea.',
    }
    if key.startswith('ac_fsb_warrant_')and key.endswith('_valid'):
        partner={'geb':'Gebet','rec':'Recta','ose':'Osea'}[key.split('_')[3]]
        text='FATO and '+partner+' are both present, independent and not capitulated, retain their established identities, and are not at war with one another.'
    else:text=descriptions[key]
    loc(key+'_tt',text);TRIGGERS[key]=block('custom_trigger_tooltip','tooltip = '+key+'_tt\n'+body)
def done(tag,suffix):return 'has_country_flag = '+tag+'_nat_'+suffix+'_done'
def active(tag):return 'ac_fsb_active = yes tag = '+tag+' original_tag = '+tag
def earliest(row):
    # Authored pacing milestones, not canonical events. A later legitimate
    # release can enter currently eligible domestic work without backdated aid.
    if row.tag=='FAT':
        if row.phase==0:year=(1991,1992,1993)[row.index//6]
        else:year=((1995,1997,2000,2003),(2006,2008,2010,2012))[row.phase-1][0 if row.index<5 else 1 if row.index<10 else 2 if row.index<14 else 3]
    elif row.phase==0:return None
    elif row.phase==1:year=(1997,1999,2001,2003)[0 if row.index<4 else 1 if row.index<8 else 2 if row.index<11 else 3]
    else:year=(2006,2008,2010,2013)[0 if row.index<4 else 1 if row.index<8 else 2 if row.index<12 else 3]
    if row.hook in ('10','110'):year=max(year,2013)
    return str(year-1)+'.12.31'
def capacity(amount):return 'set_temp_variable = { ac_pol_capacity_delta = '+str(amount)+' }\nac_pol_change_capacity = yes\n'
def idea(ident,title,desc,modifiers):
    if ident in IDEAS:raise ValueError('Duplicate national idea '+ident)
    IDEAS[ident]=modifiers;loc(ident,title);loc(ident+'_desc',desc)
def decision(tag,suffix,title,desc,condition,body,visible=None,weight=1,icon='programme',preview=''):
    ident=tag+'_fsb_'+suffix;loc(ident,title);loc(ident+'_desc',desc)
    effect(ident+'_apply',guard(condition,body))
    DECISIONS.setdefault(tag,[]).append(block(ident,
        'icon = ac_fsb_'+tag.lower()+'_'+icon+'\nallowed = { tag = '+tag+' original_tag = '+tag+' }\n'+
        block('visible',visible or active(tag))+block('available',condition)+'cost = 0\n'+
        block('complete_effect','custom_effect_tooltip = '+ident+'_tt\n'+preview+block('hidden_effect',ident+'_apply = yes'))+
        'ai_will_do = { base = '+str(weight)+' }'))
    loc(ident+'_tt',desc)
    return ident

def core():
    trigger('ac_fsb_participant','OR = { AND = { tag = FAT original_tag = FAT } AND = { tag = SBK original_tag = SBK } }')
    trigger('ac_fsb_active','ac_fsb_participant = yes has_country_flag = ac_fsb_initialized check_variable = { ac_fsb_identity = THIS.id } ac_pol_active = yes any_owned_state = { is_fully_controlled_by = PREV }')
    trigger('ac_fsb_can_fund','ac_fsb_active = yes OR = { ac_econ_enabled = no ac_econ_can_pay_programme = yes }')
    # Public compatibility payment: recheck before spending, then require the
    # full owner's result flag. Legacy payment is atomic inside the same guard.
    pay='clr_country_flag = ac_fsb_payment_succeeded\n'+guard('ac_fsb_can_fund = yes',
        guard('ac_econ_enabled = no','set_country_flag = ac_fsb_payment_succeeded')+
        block('else',guard('ac_macro_ready = yes','ac_econ_pay_programme = yes\n'+guard('has_country_flag = ac_macro_transaction_succeeded','set_country_flag = ac_fsb_payment_succeeded'))+
              block('else_if',block('limit','ac_econ_legacy_ready = yes')+'ac_econ_pay_programme = yes\nset_country_flag = ac_fsb_payment_succeeded')))
    effect('ac_fsb_pay',pay)
    effect('ac_fsb_initialize',guard('ac_fsb_participant = yes any_owned_state = { always = yes } OR = { tag = FAT has_country_flag = ac_release_administration_registered } NOT = { has_country_flag = ac_fsb_initialized }',
        'ac_pol_initialize = yes\nset_country_flag = ac_fsb_initialized\nset_variable = { ac_fsb_identity = THIS.id }\nset_variable = { ac_fsb_fiscal_applied = 0 }\nset_country_flag = ac_fsb_fiscal_dirty\n'+
        guard('date > 1991.1.7','set_country_flag = ac_fsb_late_entry')+
        'set_variable = { ac_fsb_warrants_open = 0 }\nset_variable = { ac_fsb_cases_open = 0 }\nset_variable = { ac_fsb_deliveries = 0 }\nset_variable = { ac_fsb_cases_resolved = 0 }'))
    loc('ac_fsb_cost_tt','Where enabled, pay the public programme fee (0.002 abstract billion in full mode; 2 legacy fiscal units in experimental mode). Disabled fiscal rules require no cash. Political power, institutional capacity and any listed physical stock remain real costs. No balance conversion is implied.')

def trees():
    for tag,cfg in COUNTRIES.items():
        rows=[r for r in FOCUSES if r.tag==tag]
        loc(cfg['tree'],cfg['name']+': '+cfg['category'])
        loc(cfg['tree']+'_desc','National choices, practical obligations and a later review of the authority actually held. Standing policies have continuing burdens; foreign cooperation requires consent and useful domestic work remains available.')
        body='id = '+cfg['tree']+'\ncountry = { factor = 0 modifier = { add = 45 tag = '+tag+' original_tag = '+tag+' } }\ndefault = no\nreset_on_civilwar = no\ninitial_show_position = { focus = '+rows[0].id+' }\ncontinuous_focus_position = { x = '+str((max(r.x for r in rows)+4)*96)+' y = 16 }\n'
        for row in rows:
            loc(row.id,row.title);loc(row.id+'_desc',row.narrative+'\n\n'+row.purpose+' National policy details and dialogue are authored gameplay alternatives; they do not change the established war, faction or territorial settlement.')
            loc(row.id+'_done',row.title+' completed')
            loc(row.id+'_tt',row.purpose)
            condition=active(tag)
            start=earliest(row)
            if start:condition+=' date > '+start
            node='id = '+row.id+'\nicon = GFX_ac_fsb_focus_'+row.id+'\nx = '+str(row.x)+'\ny = '+str(row.y)+'\ncost = '+str(row.cost)+'\n'
            for group in row.requirements:node+=block('prerequisite',' '.join('focus = '+tag+'_nat_'+s for s in group))
            if row.exclusive:node+=block('mutually_exclusive','focus = '+tag+'_nat_'+row.exclusive)
            node+=block('available',condition)+'cancel_if_invalid = yes\ncontinue_if_invalid = no\n'
            node+=block('ai_will_do','factor = '+('45' if row.exclusive and row.index%2 else '60'))
            preview=block('effect_tooltip','add_ideas = ac_fsb_'+tag.lower()+'_'+row.hook) if row.kind=='policy' else ''
            node+=block('completion_reward','custom_effect_tooltip = '+row.id+'_tt\n'+preview+block('hidden_effect',row.id+'_reward = yes'))
            node+='search_filters = { FOCUS_FILTER_POLITICAL FOCUS_FILTER_INDUSTRY }\n'
            body+=block('focus',node)
            reward='set_country_flag = '+row.id+'_done\n'
            if row.kind=='policy':
                _,family,mods=POLICIES[row.hook];ident='ac_fsb_'+tag.lower()+'_'+row.hook
                idea(ident,row.title,row.narrative,mods)
                reward+='\n'.join('remove_ideas = ac_fsb_'+t.lower()+'_'+other for other,(t,f,_) in POLICIES.items() if t==tag and f==family)+'\nadd_ideas = '+ident+'\n'
                reward+='set_country_flag = ac_fsb_procedure_chosen\n'
            elif row.kind=='scene':reward+='ac_fsb_scene_'+row.hook+'_queue = yes\n'
            elif row.kind=='capability':reward+='set_country_flag = ac_fsb_'+row.hook+'\n'
            elif row.kind!='action':raise ValueError(row.kind)
            effect(row.id+'_reward',guard(active(tag)+' NOT = { '+done(tag,row.suffix)+' }',reward))
        OUT['common/national_focus/ac_fsb_'+tag.lower()+'.txt']=block('focus_tree',body)
        decision(tag,'adopt_campaign','Adopt the National Campaign',
            'After any selected generic, regional or continuous focus has finished, adopt the national campaign and retain completed content. Unknown bespoke trees are not overwritten. No starting forces, industry or expired historical rewards are granted.',
            active(tag)+' ac_pol_previous_tree_idle = yes NOT = { has_focus_tree = '+cfg['tree']+' }',
            'load_focus_tree = { tree = '+cfg['tree']+' keep_completed = yes }',
            active(tag)+' NOT = { has_focus_tree = '+cfg['tree']+' }',weight=2)

def flag_names():
    """Readable conditions for every new flag, never raw developer identifiers."""
    source='\n'.join(EFFECTS.values())+'\n'+'\n'.join(TRIGGERS.values())+'\n'+'\n'.join(''.join(v)for v in DECISIONS.values())+'\n'+''.join(EVENTS)
    flags=set(re.findall(r'\b(?:has_country_flag|set_country_flag|clr_country_flag|flag)\s*=\s*(ac_fsb_\w+|(?:FAT|SBK)_nat_\w+)',source))
    features={r.hook:r.title for r in FOCUSES if r.kind in ('capability','action')};scenes={r.hook:r.title for r in FOCUSES if r.kind=='scene'}
    plain={'initialized':'The national administration is registered','late_entry':'The campaign was adopted after the opening date','payment_succeeded':'The programme fee has been paid','fiscal_dirty':'A standing account awaits reconciliation','invoice_verified':'The national invoice audit is verified','verified_receipts':'Civil work receipts are verified','indexed_archive':'The common civil archive is checked','offer_refused':'A bounded external offer was declined','external_closed':'Unfulfilled external obligations have been closed','interim_service':'A protected interim service was authorised','adviser_refused':'The external adviser route was declined or interrupted','adviser_accepted':'A technical adviser remit was accepted','adviser_open':'A limited technical adviser request is open','adviser_window':'The adviser response deadline has not expired','adviser_visit':'The limited technical visit remains active','adviser_notice':'South Belka has requested a limited technical adviser','case_expired':'A civil file expired without a settlement','interrupted':'The national programme was interrupted','interruption_recorded':'The interruption review is recorded','procedure_chosen':'A national administrative procedure was chosen'}
    for flag in sorted(flags):
        if flag in LOC:continue
        suffix=flag.removeprefix('ac_fsb_');label=None
        if suffix in plain:label=plain[suffix]
        elif suffix in features:label='Authorisation: '+features[suffix]
        elif suffix.startswith('scene_'):
            parts=suffix.split('_');title=scenes[parts[1]];state='_'.join(parts[2:])
            meaning={'pending':'The hearing awaits a decision','window':'The hearing deadline has not expired','seen':'The hearing is concluded','archived':'The historical hearing is archived','cancelled':'The interrupted hearing is closed','unfunded':'The hearing closed without a funded mandate','a_chosen':'The reviewed allocation was chosen','b_chosen':'The limited alternative was chosen'}[state]
            label=title+': '+meaning.lower()
        elif suffix.startswith('w_'):
            _,country,kind,*state=suffix.split('_');partner={'geb':'Gebet','rec':'Recta','ose':'Osea'}[country];subject={'infantry':'infantry replacements','small':'small infantry consignment','support':'support stores','mobility':'motor transport'}[kind]
            meaning={'open':'warrant open','window':'response and delivery deadline live','accepted':'receiver consent recorded','inspected':'joint inspection authorised','notice':'FATO offer awaiting a reply','cooldown':'recent request within its cooldown'}['_'.join(state)]
            label=partner+' / '+subject+': '+meaning
        elif suffix.startswith('case_'):
            _,kind,*state=suffix.split('_');meaning={'open':'file open','window':'hearing deadline live','resolved':'settlement recorded','appealed':'the unique appeal has been used'}['_'.join(state)]
            label=kind.capitalize()+' case: '+meaning
        elif suffix.endswith('_standing'):label='Standing account active: '+features[suffix.removesuffix('_standing')]
        elif suffix.endswith('_cooldown'):
            label='Recent authorisation remains within its cooldown: '+suffix.removesuffix('_cooldown').replace('fat_','FATO ').replace('sbk_','South Belka ').replace('_',' ')
        elif suffix.endswith('_used'):
            hook=suffix.removesuffix('_used').removeprefix('fat_').removeprefix('sbk_');label='Authorisation recorded: '+features.get(hook,hook.replace('_',' '))
        if label is None:raise ValueError('Author a readable national condition: '+flag)
        loc(flag,label)
    for key,text in {'ac_fsb_warrants_open':'Open equipment warrants','ac_fsb_cases_open':'Open civil files','ac_fsb_deliveries':'Completed stock-backed deliveries','ac_fsb_cases_resolved':'Completed case resolutions','ac_fsb_identity':'Registered national identity','ac_fsb_fiscal_applied':'Recorded standing administrative commitment'}.items():loc(key,text)

def outputs():
    for d in (OUT,LOC,EFFECTS,TRIGGERS,IDEAS,DECISIONS):d.clear()
    EVENTS.clear();core();trees()
    from programmes import build_actions,build_commitments
    from obligations import build_warrants,build_cases
    from narrative import build_narrative
    build_actions();build_warrants();build_cases();build_narrative();build_commitments()
    # Run once at startup and then weekly, never from UI quotes. Recount only
    # this owner's flags; annexe/subject/war callbacks close permissions early.
    tick='ac_fsb_initialize = yes\n'+guard('ac_fsb_participant = yes has_country_flag = ac_fsb_initialized check_variable = { ac_fsb_identity = THIS.id }',
        guard('ac_fsb_active = no','ac_fsb_interrupt = yes')+
        guard('ac_fsb_active = yes','ac_fsb_warrant_tick = yes\nac_fsb_case_tick = yes\nac_fsb_adviser_tick = yes\nac_fsb_narrative_tick = yes\nac_fsb_sync_commitments = yes'))
    effect('ac_fsb_weekly',tick)
    actions=block('on_startup',block('effect','FAT = { ac_fsb_weekly = yes }\nSBK = { ac_fsb_weekly = yes }'))
    for tag in COUNTRIES:actions+=block('on_weekly_'+tag,block('effect','ac_fsb_weekly = yes'))
    actions+=block('on_release_as_free',block('effect','ac_fsb_weekly = yes'))+block('on_release_as_puppet',block('effect','ac_fsb_weekly = yes'))
    actions+=block('on_annex',block('effect','FROM = { ac_fsb_interrupt = yes ac_fsb_partner_interrupt = yes }'))
    actions+=block('on_capitulation_immediate',block('effect','ac_fsb_interrupt = yes ac_fsb_partner_interrupt = yes'))
    for hook in ('on_puppet','on_subject_free','on_subject_autonomy_level_change'):
        actions+=block(hook,block('effect','ac_fsb_status_interrupt = yes ac_fsb_partner_interrupt = yes'))
    actions+=block('on_war_relation_added',block('effect','ac_fsb_warrant_tick = yes ac_fsb_adviser_tick = yes\nFROM = { ac_fsb_warrant_tick = yes ac_fsb_adviser_tick = yes }'))
    # Receiver decisions and callbacks are exact-tag guarded even on clones.
    for tag in ('GEB','REC','OSE'):actions+=block('on_weekly_'+tag,block('effect','ac_fsb_partner_tick = yes'))
    OUT['common/on_actions/ac_fato_south_belka.txt']=block('on_actions',actions)
    OUT['common/scripted_effects/ac_fato_south_belka.txt']=''.join(block(k,v) for k,v in EFFECTS.items())
    OUT['common/scripted_triggers/ac_fato_south_belka.txt']=''.join(block(k,v) for k,v in TRIGGERS.items())
    OUT['common/ideas/ac_fato_south_belka.txt']=block('ideas',block('country',''.join(block(k,
        'picture = ac_fsb_'+k+'\nallowed = { always = no }\n'+block('modifier','\n'.join(n+' = '+str(v) for n,v in mods.items()))) for k,mods in IDEAS.items())))
    categories=''
    for tag in DECISIONS:
        cat='ac_fsb_'+tag.lower()+'_programmes';loc(cat,COUNTRIES.get(tag,dict(category='Receiving permissions'))['category'])
        loc(cat+'_desc',('Authorise bounded stock-backed commitments, inspect current obligations and maintain a useful domestic reserve. Each offer needs a present eligible receiver and its consent; no faction or war outcome is promised.' if tag=='FAT' else 'Hear specific civil files, pay for current work and define the authority of the present administration. A limited external adviser needs consent; domestic inspection and civil review remain available after refusal.' if tag=='SBK' else 'Review a specific receiving permission. Accept, decline or revoke before delivery; consent alone grants no equipment, faction membership, guarantee or autonomy change.'))
        categories+=block(cat,'icon = '+cat+'\nallowed = { tag = '+tag+' original_tag = '+tag+' }\nvisible = { any_owned_state = { always = yes } }')
    OUT['common/decisions/categories/ac_fato_south_belka.txt']=categories
    OUT['common/decisions/ac_fato_south_belka.txt']=''.join(block('ac_fsb_'+tag.lower()+'_programmes',''.join(items)) for tag,items in DECISIONS.items())
    OUT['events/ac_fato_south_belka.txt']='add_namespace = ac_fsb\n\n'+''.join(EVENTS)
    flag_names()
    OUT['localisation/english/ac_fato_south_belka_l_english.yml']='\ufeffl_english:\n'+''.join(' '+k+':0 "'+v.replace('"',"'").replace('\n','\\n')+'"\n' for k,v in LOC.items())
    return {MOD/k:v.encode('utf-8') for k,v in OUT.items()}

def purpose_inventory():
    return {'schema':1,'source_layer':'provisional authored gameplay','dedicated_focuses':{'FAT':54,'SBK':42},
        'regional36_separate':True,'purposes':[dict(id=r.id,title=r.title,phase=r.phase+1,kind=r.kind,hook=r.hook,purpose=r.purpose,
            requirements=r.requirements,exclusive=r.exclusive or None,cost_days=r.cost*7,earliest_after=earliest(r),
            source_layer='provisional authored dialogue and gameplay',reference='tools/fato_south_belka/content.py:'+r.suffix+'; inherited country context is mapped in docs/FATO_SOUTH_BELKA.md; no official policy claim',
            status='implemented source; static results separate; native pending') for r in FOCUSES]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    output=outputs();output[HERE/'purposes.json']=(json.dumps(purpose_inventory(),indent=2)+'\n').encode()
    bad=[]
    for path,data in output.items():
        if a.check:
            if not path.exists() or path.read_bytes()!=data:bad.append(str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if bad:raise SystemExit('Stale FAT/SBK outputs:\n'+'\n'.join(bad))
    print(('Checked' if a.check else 'Generated'),len(output),'FAT/SBK outputs; 96 explicit purposes')
if __name__=='__main__':main()
