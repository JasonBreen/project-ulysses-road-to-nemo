"""Independent Pacific narratives using default-preserving initial compiler seams.

No original story output is overwritten. ac_sqp owns only the new personal
state; the existing story rule remains the sole enable/disable preference.
"""
import argparse
import json
from pathlib import Path
import re
import sys
from config import HERE,ROOT,MOD,campaigns,legacy_builder


def prefix(text):
    return re.sub(r'(?<![A-Za-z0-9])ac_sq(?=[_.\s"}]|$)','ac_sqp',text).replace('rule = ac_sqp_stories','rule = ac_sq_stories')


def build():
    stories=campaigns();old=legacy_builder()
    if not stories:raise ValueError('No complete approved Pacific story component')
    initialize=''
    for row in stories:
        body=('set_country_flag = ac_sq_initialized\nset_variable = { ac_sq_identity = THIS.id }\n'
              'set_variable = { ac_sq_chapter = 0 }\nset_variable = { ac_sq_pending_chapter = 0 }\n'
              'set_variable = { ac_sq_ending_kind = -1 }\nset_variable = { ac_sq_cohesion = 50 }\nset_variable = { ac_sq_credibility = 50 }\n')
        body+=old.owned_if('date > '+row['admission_until'],'set_country_flag = ac_sq_closed\nset_country_flag = ac_sq_late_archive\n')
        body+=old.block('else_if',old.block('limit','date > 1991.1.31')+'set_variable = { ac_sq_chapter = 1 }\nset_country_flag = '+old.flag(row,'missed_1')+'\n')
        initialize+=old.owned_if(old.identity(row['tag'])+' ac_sq_enabled = yes NOT = { has_country_flag = ac_sq_initialized }',body)
    base=old.build(stories,initialize_effect=initialize)
    base.pop('common/game_rules/ac_squadrons.txt')
    localization='localisation/english/ac_squadrons_l_english.yml'
    # The shared rule stays wholly owned by the initial compiler, including its
    # uppercase group label. Do not shadow it with a duplicate English key.
    rule_keys={'ac_sq_rule','ac_sq_rule_on','ac_sq_rule_off','ac_sq_rule_on_desc','ac_sq_rule_off_desc','AC_SQUADRON_RULES'}
    base[localization]='\n'.join(line for line in base[localization].splitlines()if line.strip().split(':',1)[0]not in rule_keys)+'\n'
    trigger='common/scripted_triggers/ac_squadrons.txt'
    before=old.block('ac_sq_active','ac_sq_enabled = yes ac_sq_host = yes has_country_flag = ac_sq_initialized NOT = { has_country_flag = ac_sq_closed }')
    after=old.block('ac_sq_active','ac_sq_enabled = yes ac_sq_host = yes has_country_flag = ac_sq_initialized has_variable = ac_sq_identity check_variable = { var = ac_sq_identity value = THIS.id compare = equals } NOT = { has_country_flag = ac_sq_closed }')
    if base[trigger].count(before)!=1:raise ValueError('Initial active-contract seam changed; review explicitly')
    base[trigger]=base[trigger].replace(before,after)
    # Completed archives/cards are personal records too. A new numeric country
    # identity cannot inherit their visibility from copied flags alone.
    for path in tuple(base):
        if path.startswith('events/'):
            for row in stories:
                original=old.identity(row['tag'])
                base[path]=base[path].replace(original,original+' has_variable = ac_sq_identity check_variable = { var = ac_sq_identity value = THIS.id compare = equals }')
    # Category allowed is the static country eligibility contract. Keep setup
    # receipts in its live visibility, so startup ordering cannot retire it.
    category='common/decisions/categories/ac_squadrons.txt'
    base[category]=base[category].replace('visible = {\n\t\thas_country_flag = ac_sq_initialized',
        'visible = {\n\t\thas_country_flag = ac_sq_initialized has_variable = ac_sq_identity check_variable = { var = ac_sq_identity value = THIS.id compare = equals }')
    before=old.block('ac_sq_air_capable','check_variable = { deployed_airforce_manpower_k > 0 }')
    after=old.block('ac_sq_air_capable','check_variable = { deployed_airforce_manpower_k > 0 } check_variable = { num_deployed_planes > 0 }')
    if base[trigger].count(before)!=1:raise ValueError('Initial capability seam changed; review explicitly')
    base[trigger]=base[trigger].replace(before,after)
    interrupt=''
    for row in stories:
        cleanup=''
        for chapter in row['chapters']:
            number=chapter['id']
            cleanup+=old.owned_if('check_variable = { ac_sq_pending_chapter = '+str(number)+' } check_variable = { ac_sq_chapter = '+str(number-1)+' }',
                'set_country_flag = '+old.flag(row,'missed_'+str(number))+'\nset_variable = { ac_sq_chapter = '+str(number)+' }\n')
        cleanup+='clr_country_flag = ac_sq_dispatch_pending\nset_variable = { ac_sq_pending_chapter = 0 }\nclr_country_flag = ac_sq_ending_pending\nset_country_flag = ac_sq_interrupted\n'
        # Annexation still has a FROM object even when country_exists has just
        # become false. No choice, score or completed archive is manufactured.
        condition='tag = '+row['tag']+' original_tag = '+row['tag']+' has_country_flag = ac_sq_initialized has_variable = ac_sq_identity check_variable = { var = ac_sq_identity value = THIS.id compare = equals } NOT = { has_country_flag = ac_sq_closed }'
        interrupt+=old.owned_if(condition,cleanup)
    base['common/scripted_effects/ac_squadrons.txt']+=old.block('ac_sq_interrupt',interrupt)
    actions=base['common/on_actions/ac_squadrons.txt']
    # The registered root is the final brace; all original scheduling semantics
    # were generated for these new rows alone, including country-scoped weekly.
    addition=old.block('on_annex',old.block('effect',old.block('FROM','ac_sq_interrupt = yes')))+old.block('on_subject_annexed',old.block('effect','ac_sq_interrupt = yes'))
    if not actions.rstrip().endswith('}'):raise ValueError('Unexpected new-story on-action root')
    base['common/on_actions/ac_squadrons.txt']=actions.rstrip()[:-1]+addition+'}\n'
    result={relative.replace('ac_squadrons','ac_squadrons_pacific'):prefix(text)for relative,text in base.items()}
    manifest=dict(schema=1,namespace='ac_sqp',initial_owner_untouched='ac_sq',existing_rule='ac_sq_stories',
        campaigns=[dict(tag=r['tag'],id=r['id'],base=r['base'],core_chapters=20,core_cast=4,personal_endings=3,read_only_archives=20,cast_cards=4,admission_until=r['admission_until'],last_act_ongoing=True)for r in stories],
        core_chapters=20*len(stories),cast=4*len(stories),personal_endings=3*len(stories),technical_archives=20*len(stories),technical_cast_cards=4*len(stories),native_acceptance=False)
    return result,manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result,manifest=build()
    for relative,text in result.items():
        data=text.encode('utf-8-sig'if relative.endswith('.yml')else'utf-8');path=MOD/relative
        if args.check:
            if not path.exists()or path.read_bytes().replace(b'\r\n',b'\n')!=data:raise SystemExit('Stale Pacific narrative: '+relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    text=json.dumps(manifest,indent=2)+'\n';path=HERE/'manifest.json'
    if args.check:
        if not path.exists()or path.read_text()!=text:raise SystemExit('Stale Pacific story manifest')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    print(str(manifest['core_chapters'])+' new Pacific core chapters; technical archives/cards excluded; initial6 outputs untouched')
