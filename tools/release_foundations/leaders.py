"""Institutional fallback for unknown officeholders in genuinely new regimes.

Never rewrite a named character's ideology or replace a saved/adopted leader.
The three fallback IDs reuse national emblems, contain no biography and are
promoted only when no recruited authored identity fits the actual government.
"""
import argparse,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get
TAGS=('AWW','REC','SHI')
SUBTYPES={'democratic':'centrism','communism':'socialism','fascism':'fascism_ideology','neutrality':'centrism_na','monarchism':'constitutional_monarchy'}
def block(name,body):return name+' = {\n'+'\n'.join(('\t'+line.rstrip() if line.strip() else '') for line in body.splitlines())+'\n}\n'
def capture():
    intake=json.loads((HERE/'intake.json').read_text());path=MOD/'common/ideologies/00_ideologies.txt';groups={sub:group for group,_,body in get(parse(path.read_text(encoding='utf-8-sig')),'ideologies') for sub,_,_ in get(body,'types',[])}
    for group,subtype in SUBTYPES.items():
        if groups.get(subtype)!=group:raise ValueError('Release office subtype no longer belongs to government: '+subtype)
    wanted={ident for tag in TAGS for ident in intake['countries'][tag]['identities']};roles={};role_subtypes={};authored=[];inputs={path.relative_to(MOD).as_posix():hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()}
    for path in sorted((MOD/'common/characters').glob('*.txt')):
        if path.name=='ac_release_governments.txt':continue
        for kind,_,entries in parse(path.read_text(encoding='utf-8-sig')):
            if kind!='characters':continue
            for ident,_,body in entries:
                if any(key=='country_leader' for key,_,_ in body):authored.append(ident);inputs[path.relative_to(MOD).as_posix()]=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
                if ident not in wanted:continue
                roles[ident]=sorted({groups[get(role,'ideology')] for key,_,role in body if key=='country_leader' and get(role,'expire','"2066.1.1"').strip('"')>'2020.12.31'})
                role_subtypes[ident]={groups[get(role,'ideology')]:get(role,'ideology') for key,_,role in body if key=='country_leader' and get(role,'expire','"2066.1.1"').strip('"')>'2020.12.31'}
                inputs[path.relative_to(MOD).as_posix()]=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    if set(roles)!=wanted:raise ValueError('Missing inherited released-country character definition')
    return dict(schema=1,countries={tag:dict(identities={ident:roles[ident] for ident in intake['countries'][tag]['identities']},role_subtypes={ident:role_subtypes[ident] for ident in intake['countries'][tag]['identities']},fallback=tag+'_ac_release_government_office') for tag in TAGS},subtypes=SUBTYPES,authored_leader_ids=sorted(set(authored)),
        source_inputs_sha256=dict(sorted(inputs.items())),classification='Inherited named roles remain unchanged; provisional government-office representation is used only for an unknown officeholder in a genuinely new incompatible regime.',native='Source role/recruit/promote guards only; native portrait/government/save acceptance pending.')
def outputs(data=None):
    data=data or capture();characters='';effects='';loc=[]
    for tag,row in data['countries'].items():
        ident=row['fallback'];review='ac_release_'+tag+'_office_reviewed';known=[]
        for person,groups in row['identities'].items():
            for group in groups:known.append(block('AND','has_character = '+person+' has_government = '+group))
        known.extend('has_country_leader = { character = '+person+' ruling_only = yes }\n' for person in data['authored_leader_ids'])
        ruling=block('OR',''.join('has_country_leader = { character = '+person+' ruling_only = yes }\n' for person in data['authored_leader_ids']))
        promote_known=''
        for person,groups in row['role_subtypes'].items():
            for group,subtype in groups.items():promote_known+=block('if' if not promote_known else 'else_if','limit = { has_character = '+person+' has_government = '+group+' }\npromote_character = { character = '+person+' ideology = '+subtype+' }')
        code=''
        for group,subtype in data['subtypes'].items():
            action='if = { limit = { NOT = { has_character = '+ident+' } } recruit_character = '+ident+' }\n'
            if group=='democratic':action+='promote_character = { character = '+ident+' ideology = '+subtype+' }'
            else:action+=block('add_country_leader_role','character = '+ident+'\npromote_leader = yes\n'+block('country_leader','ideology = '+subtype+'\nexpire = "2066.1.1.1"\ntraits = { }\ndesc = '+ident+'_desc'))
            code+=block('if','limit = { has_government = '+group+' }\n'+action)
        eligible='tag = '+tag+' original_tag = '+tag+' has_global_flag = ac_release_'+tag+'_was_absent NOT = { has_global_flag = ac_release_'+tag+'_adopted } NOT = { has_global_flag = ac_release_'+tag+'_annexed } NOT = { has_global_flag = '+review+' } has_capitulated = no ac_release_owned_capital = yes any_owned_state = { NOT = { state = 171 } }'
        supported=block('OR','\n'.join('has_government = '+group for group in data['subtypes']))
        effects+=block('ac_release_'+tag+'_ensure_ruling_office',block('if',block('limit',eligible+'\n'+supported)+block('if',block('limit','NOT = { '+ruling+' }')+promote_known)+block('if',block('limit','NOT = { '+block('OR',''.join(known))+' }')+code)+'set_global_flag = '+review))
        characters+=block(ident,'name = '+ident+'\nportraits = { civilian = { large = "GFX_ac_release_office_'+tag+'" } }\n'+block('country_leader','ideology = centrism\nexpire = "2066.1.1.1"\ntraits = { }\ndesc = '+ident+'_desc'))
        loc.extend([(ident,'National Administration'),(ident+'_desc','The office represents this newly formed government. Its individual officeholder has not been established in the mod chronology; the existing national emblem identifies the administration. Established named leaders and their political identities are retained separately.')])
    return {'common/characters/ac_release_governments.txt':block('characters',characters),'common/scripted_effects/ac_release_governments.txt':effects,'localisation/english/ac_release_governments_l_english.yml':'l_english:\n'+'\n'.join(' '+key+':0 "'+value+'"' for key,value in loc)+'\n'}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();data=capture();path=HERE/'leader_contract.json';text=json.dumps(data,indent=2)+'\n'
    if args.check:
        if not path.exists() or path.read_text()!=text:raise SystemExit('Release leader identity contract differs')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    for relative,text in outputs(data).items():
        path=MOD/relative;encoding='utf-8-sig' if relative.endswith('.yml') else 'utf-8'
        if args.check:
            if not path.exists() or path.read_text(encoding=encoding)!=text:raise SystemExit('Release office output differs: '+relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding=encoding,newline='\n')
    print('Release office identities consistent' if args.check else 'Release office identities generated')
