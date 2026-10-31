"""Generate the additive ac_pol owner and persistent 36-focus regional tree.

No history setup grants, political replacements, borrowed war flags or macro
treasury writes. --check is read-only. Profile capture is a deliberate command.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MOD=ROOT/'mod/2985041246'
sys.path.append(str(ROOT/'tools/usea_expansion'))
from script import parse,get,walk
from content import FOCUSES,CHOICES,BESPOKE,IDEAS,FORM_PROGRAMMES

OUT={};LOC={}


def block(key,body):return key+' = {\n'+''.join(('\t'+line if line else '')+'\n' for line in body.splitlines())+'}\n'
def guarded(condition,body):return block('if',block('limit',condition)+body)
def loc(key,text):
    if key in LOC and LOC[key]!=text:raise ValueError('Localization conflict '+key)
    LOC[key]=text
def put(path,text):OUT[path]=('# Original institutional gameplay; owner: tools/institutions/build.py.\n'+text).encode('utf-8')
def effect(key,text):EFFECTS.append(block(key,text))


def capture_profiles():
    rows=[]
    party_type={'democratic':'civil_administration','communism':'party_secretariat','fascism':'command_administration','neutrality':'executive_office','monarchism':'crown_office'}
    for row in json.loads((ROOT/'tools/usea_expansion/leaders.json').read_text()):
        path=MOD/row['history']
        name=path.stem[6:]
        style='council_office' if row['tag'] in ('AWW','RAT') else party_type[row['party']]
        rows.append(dict(tag=row['tag'],name=name,history=row['history'],history_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            inherited_party=row['party'],institution=style,capacity=40,regional_tree=row['tag'] not in BESPOKE,
            source_layer='mod provenance / provisional gameplay',
            reference=row['history']+' at main3810d1a; party is context, not proof of constitutional form',
            status='implemented gameplay profile; official constitutional identity unverified'))
    (HERE/'profiles.json').write_text(json.dumps(rows,indent=2)+'\n')


def triggers(profiles):
    tags='\n'.join('original_tag = '+r['tag'] for r in profiles)
    rows=[block('ac_pol_profiled',block('OR',tags)),
          block('ac_pol_active','ac_pol_profiled = yes has_country_flag = ac_pol_initialized has_capitulated = no any_owned_state = { always = yes }'),
          block('ac_pol_uses_regional_tree',block('OR','\n'.join('original_tag = '+r['tag'] for r in profiles if r['regional_tree']))),
          block('ac_pol_can_adopt','ac_pol_active = yes political_power >= 30 check_variable = { ac_pol_capacity >= 15 } NOT = { has_country_flag = ac_pol_policy_cooldown }'),
          block('ac_pol_can_work','ac_pol_active = yes political_power >= 25 NOT = { has_country_flag = ac_pol_work_cooldown } check_variable = { ac_pol_capacity < 100 }')]
    ids=[]
    for source in [MOD/'common/national_focus/generic.txt',*sorted((MOD/'common/continuous_focus').glob('*.txt'))]:
        ids += [get(n,'id') for k,n in walk(parse(source.read_text(encoding='utf-8-sig'))) if k=='focus']
    # Use the established shipped focus-progress syntax. Completed focuses cannot
    # block a handoff; active normal or continuous focuses must block it.
    idle='\n'.join('NOT = { AND = { NOT = { has_completed_focus = '+ident+' } OR = { has_shine_effect_on_focus = '+ident+' focus_progress = { focus = '+ident+' progress > 0 } } } }' for ident in dict.fromkeys(ids))
    rows.append(block('ac_pol_legacy_idle',idle))
    put('common/scripted_triggers/ac_politics.txt','\n'.join(rows))
    return ids


def build_effects(profiles):
    global EFFECTS
    EFFECTS=[]
    forms='\n'.join('clr_country_flag = ac_pol_form_'+form for form in FORM_PROGRAMMES)
    forms+='\n'+guarded('OR = { original_tag = AWW original_tag = RAT }','set_country_flag = ac_pol_form_council_office')
    branches=''
    for party,form in [('democratic','civil_administration'),('monarchism','crown_office'),('communism','party_secretariat'),('fascism','command_administration')]:
        branches+=block('if' if not branches else 'else_if',block('limit','has_government = '+party)+'set_country_flag = ac_pol_form_'+form)
    branches+=block('else','set_country_flag = ac_pol_form_executive_office')
    forms+=block('else',branches)
    effect('ac_pol_refresh_form',forms)
    init='set_country_flag = ac_pol_initialized\nset_variable = { ac_pol_schema = 1 }\nset_variable = { ac_pol_capacity = 40 }\nset_variable = { ac_pol_fiscal_applied = 0 }\nset_variable = { ac_pol_fiscal_identity = THIS.id }\nset_country_flag = ac_pol_fiscal_dirty\nset_country_flag = ac_pol_audits_unlocked\n'
    for row in profiles:
        init+=guarded('original_tag = '+row['tag'],'set_country_flag = ac_pol_profile_'+row['tag']+'\nset_country_flag = ac_pol_form_'+row['institution'])
    init+='ac_pol_refresh_form = yes\n'+guarded('date > 1991.1.7','set_country_flag = ac_pol_late_initialization\ncustom_effect_tooltip = ac_pol_late_init_tt')
    effect('ac_pol_initialize',guarded('ac_pol_profiled = yes NOT = { has_country_flag = ac_pol_initialized } any_owned_state = { always = yes }',init))
    effect('ac_pol_bounds','clamp_variable = { var = ac_pol_capacity min = 0 max = 100 }')
    effect('ac_pol_change_capacity',guarded('ac_pol_active = yes',
        'add_to_variable = { ac_pol_capacity = ac_pol_capacity_delta }\nac_pol_bounds = yes\n'+guarded('check_variable = { ac_pol_capacity < 1 }','ac_pol_suspend_policy = yes')))
    # Foreign fiscal state is accessed only through the optional owner's API.
    # Reconcile an old exact snapshot before establishing a new policy amount.
    sync='set_temp_variable = { ac_macro_commitment_delta = ac_pol_fiscal_applied }\nmultiply_temp_variable = { ac_macro_commitment_delta = -1 }\nac_macro_change_commitment = yes\nset_variable = { ac_pol_fiscal_applied = 0 }\n'
    for policy,rate in [('civic','0.0005'),('military','0.001'),('district','0.0003')]:
        sync+=guarded('has_country_flag = ac_pol_policy_'+policy,
            'set_variable = { ac_pol_fiscal_applied = ac_macro_nominal_gdp }\nmultiply_variable = { ac_pol_fiscal_applied = '+rate+' }')
    sync+='set_temp_variable = { ac_macro_commitment_delta = ac_pol_fiscal_applied }\nac_macro_change_commitment = yes\nclr_country_flag = ac_pol_fiscal_dirty'
    reset_receipt='set_variable = { ac_pol_fiscal_applied = 0 }\nset_variable = { ac_pol_fiscal_identity = THIS.id }\nset_country_flag = ac_pol_fiscal_dirty'
    effect('ac_pol_sync_fiscal',guarded('ac_macro_ready = yes',
        guarded('NOT = { has_variable = ac_pol_fiscal_identity }',reset_receipt)+
        guarded('NOT = { check_variable = { var = ac_pol_fiscal_identity value = THIS.id compare = equals } }',reset_receipt)+
        guarded('has_country_flag = ac_pol_fiscal_dirty',sync)))
    clear='\n'.join('remove_ideas = ac_pol_'+name+'\nclr_country_flag = ac_pol_policy_'+name for name in ('civic','military','district'))
    effect('ac_pol_clear_policy',clear+'\nset_country_flag = ac_pol_fiscal_dirty')
    for name in ('civic','military','district'):
        effect('ac_pol_adopt_'+name,guarded('ac_pol_can_adopt = yes NOT = { has_country_flag = ac_pol_policy_'+name+' }',
            'add_political_power = -30\nadd_to_variable = { ac_pol_capacity = -10 }\nac_pol_clear_policy = yes\nremove_ideas = ac_pol_strained\nset_country_flag = ac_pol_policy_'+name+'\nadd_ideas = ac_pol_'+name+'\nset_country_flag = { flag = ac_pol_policy_cooldown days = 180 }\nac_pol_sync_fiscal = yes\nac_pol_bounds = yes'))
    effect('ac_pol_suspend_policy',guarded('ac_pol_active = yes OR = { has_country_flag = ac_pol_policy_civic has_country_flag = ac_pol_policy_military has_country_flag = ac_pol_policy_district }',
        'ac_pol_clear_policy = yes\nac_pol_sync_fiscal = yes\nadd_ideas = ac_pol_strained\nset_country_flag = ac_pol_suspended\ncustom_effect_tooltip = ac_pol_suspension_tt'))
    for name,gain,extra in [('audit',12,''),('records',8,'add_stability = 0.01'),('maintenance',6,'army_experience = 2'),('relief',8,'add_stability = 0.01'),('training',4,'army_experience = 4'),('external',6,'air_experience = 2')]:
        condition='ac_pol_can_work = yes'
        if name!='audit':condition+=' has_country_flag = ac_pol_'+('records' if name=='records' else name)+'_unlocked'
        effect('ac_pol_work_'+name,guarded(condition,
            'add_political_power = -25\nadd_to_variable = { ac_pol_capacity = '+str(gain)+' }\n'+extra+'\nadd_timed_idea = { idea = ac_pol_attention days = 90 }\nset_country_flag = { flag = ac_pol_work_cooldown days = 90 }\nac_pol_bounds = yes'))
    effect('ac_pol_emergency_review',guarded('ac_pol_active = yes check_variable = { ac_pol_capacity < 15 } political_power >= 10 NOT = { has_country_flag = ac_pol_recovery_cooldown }',
        'add_political_power = -10\nadd_to_variable = { ac_pol_capacity = 6 }\nadd_timed_idea = { idea = ac_pol_attention days = 90 }\nset_country_flag = { flag = ac_pol_recovery_cooldown days = 90 }\nac_pol_bounds = yes'))
    for form,(title,cost,modifier,motifs) in FORM_PROGRAMMES.items():
        effect('ac_pol_form_'+form+'_programme',guarded('ac_pol_active = yes has_country_flag = ac_pol_form_'+form+' political_power >= 25 check_variable = { ac_pol_capacity >= '+str(cost)+' } NOT = { has_country_flag = ac_pol_form_cooldown }',
            'add_political_power = -25\nset_temp_variable = { ac_pol_capacity_delta = -'+str(cost)+' }\nac_pol_change_capacity = yes\nadd_timed_idea = { idea = ac_pol_form_'+form+' days = 180 }\nset_country_flag = { flag = ac_pol_form_cooldown days = 180 }'))
    handoff='ac_pol_active = yes ac_pol_uses_regional_tree = yes has_focus_tree = generic_focus ac_pol_legacy_idle = yes'
    effect('ac_pol_enter_regional',guarded(handoff,'load_focus_tree = { tree = ac_regional_foundation keep_completed = yes }\nset_country_flag = ac_pol_regional_handoff'))
    repairs=''
    for row in CHOICES:
        tag=row[0]
        repairs+=guarded('original_tag = '+tag+' has_country_flag = '+tag+'_pol_pending OR = { ac_pol_active = no NOT = { has_country_flag = '+tag+'_pol_response_window } }',
            'clr_country_flag = '+tag+'_pol_pending\nclr_country_flag = '+tag+'_pol_response_window')
    effect('ac_pol_repair_reviews',repairs)
    weekly='ac_pol_initialize = yes\nac_pol_repair_reviews = yes\n'+guarded('ac_pol_active = yes','ac_pol_refresh_form = yes\nac_pol_sync_fiscal = yes\n'+guarded('NOT = { has_country_flag = ac_pol_weekly_paid }',
        'set_country_flag = { flag = ac_pol_weekly_paid days = 6 }\n'+
        ''.join(guarded('has_country_flag = ac_pol_policy_'+name,'add_to_variable = { ac_pol_capacity = -'+str(cost)+' }') for name,cost in [('civic',1),('military',2),('district',1)])+
        'ac_pol_bounds = yes\n'+guarded('check_variable = { ac_pol_capacity < 1 }','ac_pol_suspend_policy = yes')))
    effect('ac_pol_weekly',weekly)
    for index,row in enumerate(CHOICES,1):
        tag,issue,context,a,ca,b,cb,motifs=row
        common='original_tag = '+tag+' ac_pol_active = yes NOT = { has_country_flag = '+tag+'_pol_settled }'
        effect(tag+'_pol_open_review',guarded(common+' NOT = { has_country_flag = '+tag+'_pol_pending } NOT = { has_country_flag = '+tag+'_pol_deferred }',
            'set_country_flag = '+tag+'_pol_pending\nset_country_flag = { flag = '+tag+'_pol_response_window days = 30 }\ncountry_event = { id = ac_pol.'+str(index)+' days = 1 }'))
        for choice,condition in [('civil',ca),('reserve',cb)]:
            effect(tag+'_pol_choose_'+choice,guarded(common+' has_country_flag = '+tag+'_pol_pending has_country_flag = '+tag+'_pol_response_window '+condition,
                'clr_country_flag = '+tag+'_pol_pending\nclr_country_flag = '+tag+'_pol_response_window\nset_country_flag = '+tag+'_pol_settled\nset_country_flag = '+tag+'_pol_'+choice+'\nadd_ideas = '+tag+'_pol_'+choice+'\nadd_to_variable = { ac_pol_capacity = 5 }\nac_pol_bounds = yes'))
        effect(tag+'_pol_defer',guarded('original_tag = '+tag+' has_country_flag = '+tag+'_pol_pending',
            'clr_country_flag = '+tag+'_pol_pending\nclr_country_flag = '+tag+'_pol_response_window\nset_country_flag = { flag = '+tag+'_pol_deferred days = 90 }\ncustom_effect_tooltip = ac_pol_defer_tt'))
    put('common/scripted_effects/ac_politics.txt','\n'.join(EFFECTS))


def national_modifiers(index,side):
    # Each issue reserves a different service capability. These small authored
    # costs supplement, rather than replace, the framework's weekly mandate cost.
    domains=['stability_factor','production_factory_efficiency_gain_factor','production_speed_infrastructure_factor','research_speed_factor',
             'industrial_capacity_factory','experience_gain_air_factor','production_speed_industrial_complex_factor',
             'production_factory_max_efficiency_factor','production_speed_buildings_factor','supply_consumption_factor',
             'experience_gain_army_factor','production_speed_infrastructure_factor','stability_factor','industrial_capacity_factory',
             'production_speed_buildings_factor','production_speed_industrial_complex_factor','research_speed_factor',
             'production_factory_efficiency_gain_factor','production_factory_max_efficiency_factor','experience_gain_army_factor','experience_gain_air_factor']
    domain=domains[index]
    benefit=(-0.02 if domain=='supply_consumption_factor' else 0.02+(index//8)*0.005)
    if side=='civil':return f'{domain} = {benefit:g}\npolitical_power_gain = -0.05'
    allocation=benefit+(-0.01 if benefit<0 else 0.01)
    if domain=='production_speed_industrial_complex_factor':
        return f'{domain} = {allocation-0.02:g}\npolitical_power_gain = -0.03'
    return f'{domain} = {allocation:g}\nproduction_speed_industrial_complex_factor = -0.02\npolitical_power_gain = -0.03'


def ideas_and_events():
    rows=[];events=['add_namespace = ac_pol']
    for suffix,(title,desc,modifier,motifs) in IDEAS.items():
        ident='ac_pol_'+suffix;loc(ident,title);loc(ident+'_desc',desc)
        rows.append(block(ident,'picture = '+ident+'\nallowed = { always = no }\nremoval_cost = -1\n'+block('modifier',modifier)))
    for index,row in enumerate(CHOICES,1):
        tag,issue,context,a,ca,b,cb,motifs=row
        key='ac_pol.'+str(index);loc(key+'.t',issue);loc(key+'.d',context+'\n\nCapacity: [?ac_pol_capacity|0]/100. These are authored administrative alternatives within the existing government. A deferred mandate leaves paid audits and the limited domestic recovery route available.')
        body='id = '+key+'\ntitle = '+key+'.t\ndesc = '+key+'.d\npicture = GFX_ac_pol_event_review\nis_triggered_only = yes\n'+block('trigger','ac_pol_active = yes original_tag = '+tag+' has_country_flag = '+tag+'_pol_pending NOT = { has_country_flag = '+tag+'_pol_settled }')
        for side,label,condition in [('civil',a,ca),('reserve',b,cb)]:
            ident=tag+'_pol_'+side;loc(ident,label);loc(ident+'_desc',context+' This continuing national allocation has the listed opportunity cost; it is not a change of leadership or another campaign policy.')
            rows.append(block(ident,'picture = '+ident+'\nallowed = { always = no }\nremoval_cost = -1\n'+block('modifier',national_modifiers(index-1,side))))
            option=key+'.'+side;loc(option,label)
            body+=block('option','name = '+option+'\n'+block('trigger',condition)+block('ai_chance','factor = '+('60' if side=='civil' else '40'))+tag+'_pol_choose_'+side+' = yes')
        loc(key+'.defer','Defer the mandate and retain domestic service work.')
        body+=block('option','name = '+key+'.defer\n'+block('ai_chance','factor = 5')+tag+'_pol_defer = yes')
        events.append(block('country_event',body))
    put('common/ideas/ac_politics.txt',block('ideas',block('country','\n'.join(rows))))
    put('events/ac_politics.txt','\n'.join(events))


def decisions_and_tree(profiles):
    loc('ac_pol_institutions','National Institutions')
    loc('ac_pol_institutions_desc','[GetPoliticalInstitution]\nActive mandate: [GetPoliticalMandate]\n[GetPoliticalFiscalStatus]\n\nInstitutional capacity: [?ac_pol_capacity|0]/100. Civic and district mandates cost 1 capacity per week; a protected delivery mandate costs 2. All reserve political attention. At zero capacity the mandate suspends; recovery is a separate, paid choice. Institutional capacity is a provisional national gameplay measure.')
    rows=[]
    def decision(ident,title,desc,condition,effect,visible='ac_pol_active = yes',weight=1):
        loc(ident,title);loc(ident+'_desc',desc)
        rows.append(block(ident,'icon = ac_pol_institutions\nallowed = { ac_pol_profiled = yes }\n'+block('visible',visible)+block('available',condition)+'cost = 0\nfire_only_once = no\ndays_re_enable = 7\n'+block('ai_will_do','base = '+str(weight))+block('complete_effect',effect)))
    for name in ('civic','military','district'):
        decision('ac_pol_adopt_'+name+'_decision','Adopt '+IDEAS[name][0],
            'Pay 30 political power and 10 capacity. The current framework mandate is replaced. '+IDEAS[name][1]+' Adoption has a 180-day cooldown; paid costs are retained after suspension.',
            'ac_pol_can_adopt = yes NOT = { has_country_flag = ac_pol_policy_'+name+' }','ac_pol_adopt_'+name+' = yes')
    for form,(title,cost,modifier,motifs) in FORM_PROGRAMMES.items():
        decision('ac_pol_form_'+form+'_decision',title,f'Pay 25 political power and {cost} capacity to fund the listed institutional service allocation for 180 days. Its operating benefit and opportunity cost are shown in the national spirit. All six administrative delivery models share a 180-day service cooldown.',
            'ac_pol_active = yes has_country_flag = ac_pol_form_'+form+' political_power >= 25 check_variable = { ac_pol_capacity >= '+str(cost)+' } NOT = { has_country_flag = ac_pol_form_cooldown }',
            'ac_pol_form_'+form+'_programme = yes','ac_pol_active = yes has_country_flag = ac_pol_form_'+form)
    for name,title,gain in [('audit','Audit Administrative Duties',12),('records','Reconcile Public Records',8),('maintenance','Coordinate Maintenance Staff',6),('relief','Exercise Domestic Relief',8),('training','Run a Replacement Staff Exercise',4),('external','Review Technical Contact Duties',6)]:
        condition='ac_pol_can_work = yes'+(' has_country_flag = ac_pol_'+name+'_unlocked' if name!='audit' else '')
        extras={'audit':'','records':' Also gain 1% stability.','maintenance':' Also gain 2 army experience.','relief':' Also gain 1% stability.','training':' Also gain 4 army experience.','external':' Also gain 2 air experience.'}[name]
        decision('ac_pol_work_'+name+'_decision',title,f'Pay 25 political power and reserve civilian construction attention for 90 days. Gain {gain} capacity.'+extras+' All normal domestic programmes share the 90-day cooldown; this is continuing work, not a repeated historical milestone.',condition,'ac_pol_work_'+name+' = yes')
    decision('ac_pol_emergency_review_decision','Restore a Limited Service Office','When capacity is below 15, pay 10 political power to recover 6 capacity and reserve construction attention for 90 days. The separate 90-day recovery cooldown and small gain prevent automatic mandate renewal.',
        'ac_pol_active = yes check_variable = { ac_pol_capacity < 15 } political_power >= 10 NOT = { has_country_flag = ac_pol_recovery_cooldown }','ac_pol_emergency_review = yes')
    decision('ac_pol_suspend_decision','Suspend the Current Mandate','End the current framework mandate and its positive effects. Its exact fiscal commitment is removed through the fiscal owner when available. Paid costs remain. Audits and limited recovery work stay useful.',
        'ac_pol_active = yes OR = { has_country_flag = ac_pol_policy_civic has_country_flag = ac_pol_policy_military has_country_flag = ac_pol_policy_district }','ac_pol_suspend_policy = yes',weight=0)
    decision('ac_pol_enter_regional_decision','Adopt the Regional Foundation Programme','Replace only the old generic tree when its normal or continuous focus is idle. Keep completed focuses. This grants no starting equipment, factories, capacity bonus or historical preparation rewards.',
        'ac_pol_active = yes ac_pol_uses_regional_tree = yes has_focus_tree = generic_focus ac_pol_legacy_idle = yes','ac_pol_enter_regional = yes',
        'ac_pol_active = yes ac_pol_uses_regional_tree = yes has_focus_tree = generic_focus',0)
    for index,row in enumerate(CHOICES,1):
        tag,issue,context,*_=row
        decision(tag+'_pol_review_decision','Review '+issue,context+' The government may adopt either eligible national mandate or defer it. The review grants nothing merely for being opened.',
            'original_tag = '+tag+' ac_pol_active = yes NOT = { has_country_flag = '+tag+'_pol_settled } NOT = { has_country_flag = '+tag+'_pol_pending } NOT = { has_country_flag = '+tag+'_pol_deferred }',tag+'_pol_open_review = yes',
            'original_tag = '+tag+' ac_pol_active = yes NOT = { has_country_flag = '+tag+'_pol_settled }',2)
    put('common/decisions/categories/ac_politics.txt',block('ac_pol_institutions','icon = ac_pol_institutions\nallowed = { ac_pol_profiled = yes }\nvisible = { ac_pol_active = yes }\nvisible_when_empty = yes'))
    put('common/decisions/ac_politics.txt',block('ac_pol_institutions','\n'.join(rows)))
    focuses=[]
    for row in FOCUSES:
        ident='ac_reg_'+row.suffix;loc(ident,row.title);loc(ident+'_desc',row.desc)
        body='id = '+ident+'\nicon = GFX_ac_pol_focus_'+row.suffix+'\nx = '+str(row.x)+'\ny = '+str(row.y)+'\ncost = '+('5' if row.days==35 else '10')+'\nai_will_do = { factor = 1 }\n'
        if row.parents:body+=block('prerequisite','\n'.join('focus = ac_reg_'+ref for ref in row.parents))
        if row.excludes:body+=block('mutually_exclusive','\n'.join('focus = ac_reg_'+ref for ref in row.excludes))
        if row.reward.startswith('ac_pol_adopt_'):body+=block('available','ac_pol_can_adopt = yes')
        body+=block('completion_reward','ac_pol_initialize = yes\n'+guarded('ac_pol_active = yes NOT = { has_country_flag = ac_pol_focus_'+row.suffix+' }',
            'set_country_flag = ac_pol_focus_'+row.suffix+'\n'+row.reward+'\nac_pol_bounds = yes'))
        focuses.append(block('focus',body))
    loc('ac_regional_foundation','Regional Foundation Programme')
    loc('ac_regional_foundation_desc','A persistent 36-focus administrative, productive and readiness framework for countries without a dedicated national campaign. National profiles and selected mandates provide context; this shared programme does not pretend to be a bespoke history.')
    put('common/national_focus/ac_regional_foundation.txt',block('focus_tree','id = ac_regional_foundation\ncountry = { factor = 0 modifier = { add = 5 ac_pol_uses_regional_tree = yes } }\ndefault = no\nreset_on_civilwar = no\ncontinuous_focus_position = { x = 2400 y = 16 }\ninitial_show_position = { focus = ac_reg_register }\n'+'\n'.join(focuses)))


def localization_and_hooks(profiles):
    names={'civil_administration':'Civil administration','party_secretariat':'Party and service secretariats','command_administration':'Command administration','executive_office':'Executive service offices','crown_office':'Crown and service offices','council_office':'Council administration'}
    text=''
    for form,title in names.items():
        key='ac_pol_context_'+form;loc(key,title)
        text+=block('text','trigger = { has_country_flag = ac_pol_form_'+form+' }\nlocalization_key = '+key)
    loc('ac_pol_form_unset','Institutional profile not yet initialized')
    text+=block('text','trigger = { always = yes }\nlocalization_key = ac_pol_form_unset')
    definitions=block('defined_text','name = GetPoliticalInstitution\n'+text)
    mandate=''
    for policy in ('civic','military','district'):
        mandate+=block('text','trigger = { has_country_flag = ac_pol_policy_'+policy+' }\nlocalization_key = ac_pol_'+policy)
        loc('ac_pol_policy_'+policy,IDEAS[policy][0]+' active')
    loc('ac_pol_no_mandate','No active framework mandate')
    mandate+=block('text','trigger = { always = yes }\nlocalization_key = ac_pol_no_mandate')
    definitions+=block('defined_text','name = GetPoliticalMandate\n'+mandate)
    loc('ac_pol_fiscal_status','Annual fiscal commitment: [?ac_pol_fiscal_applied|3] billion units. Policy replacement removes its exact previous reservation.')
    loc('ac_pol_nonfiscal_status','Political and construction allocations apply. No full-model fiscal reservation is active.')
    definitions+=block('defined_text','name = GetPoliticalFiscalStatus\n'+block('text','trigger = { ac_macro_ready = yes }\nlocalization_key = ac_pol_fiscal_status')+block('text','trigger = { always = yes }\nlocalization_key = ac_pol_nonfiscal_status'))
    put('common/scripted_localisation/ac_politics.txt',definitions)
    for key,text in {
        'ac_pol_initialized':'National institutional register established',
        'ac_pol_policy_cooldown':'A mandate adopted within the last 180 days',
        'ac_pol_work_cooldown':'A normal domestic programme funded within the last 90 days',
        'ac_pol_recovery_cooldown':'A limited service review funded within the last 90 days',
        'ac_pol_form_cooldown':'An institutional service allocation funded within the last 180 days',
        'ac_pol_records_unlocked':'Common records work available',
        'ac_pol_maintenance_unlocked':'Maintenance staffing work available',
        'ac_pol_relief_unlocked':'Domestic relief work available',
        'ac_pol_training_unlocked':'Replacement staff exercises available',
        'ac_pol_external_unlocked':'Technical-contact duties available',
    }.items():loc(key,text)
    for tag,issue,*_ in CHOICES:
        loc(tag+'_pol_settled',issue+' reviewed')
        loc(tag+'_pol_pending',issue+' awaiting a response')
        loc(tag+'_pol_response_window',issue+' response window remains open for 30 days')
        loc(tag+'_pol_deferred',issue+' deferred for 90 days')
    loc('ac_pol_late_init_tt','Initialize only the institutional framework. Do not replay historical events, setup grants or preparation rewards.')
    loc('ac_pol_suspension_tt','The mandate positive effects end. Domestic audits and limited recovery remain available. Paid costs are not refunded.')
    loc('ac_pol_defer_tt','No mandate reward is paid. A new review becomes possible after 90 days; domestic work remains available.')
    startup=block('on_startup',block('effect','every_country = { limit = { ac_pol_profiled = yes } ac_pol_initialize = yes }'))
    # Generic weekly callbacks are country-scoped in the engine. Literal tag
    # hooks omit civil-war identities even though original_tag profiles and the
    # fiscal receipt API deliberately support them.
    weekly=block('on_weekly',block('effect',guarded('ac_pol_profiled = yes','ac_pol_weekly = yes')))
    put('common/on_actions/ac_politics.txt',block('on_actions',startup+weekly))
    OUT['localisation/english/ac_politics_l_english.yml']=('l_english:\n'+''.join(' '+key+':0 "'+value.replace('"','\\"').replace('\n','\\n')+'"\n' for key,value in sorted(LOC.items()))).encode('utf-8-sig')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--capture-profiles',action='store_true');args=parser.parse_args()
    if args.capture_profiles:
        if args.check:raise SystemExit('Capture is a deliberate write operation')
        capture_profiles()
    profiles=json.loads((HERE/'profiles.json').read_text())
    triggers(profiles);build_effects(profiles);ideas_and_events();decisions_and_tree(profiles);localization_and_hooks(profiles)
    differs=[]
    for relative,data in OUT.items():
        path=MOD/relative
        if args.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n',b'\n')!=data:differs.append(relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if differs:raise SystemExit('Institution output differs: '+', '.join(differs))
    print('Institutions:',len(profiles),'profiles;',len(CHOICES),'national choices;',len(FOCUSES),'regional focuses;',len(OUT),'outputs', 'verified' if args.check else 'generated')


if __name__=='__main__':main()
