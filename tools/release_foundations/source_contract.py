"""Fail closed on protected entry operations, geography and primary hooks."""
import argparse,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get
from event_contract import validate_file,MODIFIED
def walk(nodes):
    for key,_,value in nodes:
        yield key,value
        if isinstance(value,list):yield from walk(value)
def events(text):return {get(body,'id'):body for key,_,body in parse(text) if key=='country_event'}
def validate_event_operations(candidates=None):
    source=json.loads((HERE/'event_inputs.json').read_text())['files']
    for relative,before in source.items():
        validate_file(before,candidates[relative]if candidates and relative in candidates else (MOD/relative).read_text(encoding='utf-8-sig'),relative)

def primary(reference):
    reference=Path(reference);paths=('documentation/effects_documentation.md','documentation/triggers_documentation.md','common/on_actions/_documentation.md','common/on_actions/00_on_actions.txt','common/on_actions/12_wuw_on_actions.txt')
    data={p:hashlib.sha256((reference/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in paths}
    hooks={'on_startup':dict(root='global',dispatch='snapshot then every exact release country'),
           'on_monthly':dict(root='country',dispatch='bounded current-country observation'),
           'on_release_as_free':dict(root='released country',previous='releaser'),
           'on_release_as_puppet':dict(root='released country',previous='overlord'),
           'on_annex':dict(root='winner',previous='annexed country'),
           'on_state_control_changed':dict(root='new controller',previous='old controller',state='FROM.FROM'),
           'on_capitulation':dict(root='capitulated country',previous='winner')}
    index=(reference/'common/on_actions/_documentation.md').read_text()
    for hook in hooks:
        if '`'+hook+'`' not in index:raise ValueError('Undocumented native hook: '+hook)
    return dict(schema=1,engine='Installed HOI4 1.19.4.1',primary_sources_sha256=data,hooks=hooks,
        scoped_operations={'set_capital':'Country effect accepts a state and remember_old_capital; no province override is invented.','has_resources_in_country':'Country balance comparison includes current imports unless restricted.','free_building_slots':'State building-slot comparison; projects recheck at completion.','build_railway':'Explicit path option; authored plans use owned adjacent land edges only.','recruit_character':'Country scope attaches an existing defined character.','add_country_leader_role':'Country/character scope can add a specified ideology role and optionally promote it.','promote_character':'Country scope accepts character plus ideology; explicit ideology disambiguates multiple roles.','has_character':'Country scope checks the character association.','has_country_leader':'Country scope accepts an existing character and ruling_only criteria.'},
        evidence='Primary source syntax/scope contract, not native parsing, event ordering, supply or save acceptance.')

def validate():
    validate_event_operations();intake=json.loads((HERE/'intake.json').read_text())
    for relative,expected in (intake['source_inputs_sha256']|intake['protected_placeholder_sha256']).items():
        path=MOD/relative;raw=path.read_bytes();raw=raw if path.suffix=='.bmp' else raw.replace(b'\r\n',b'\n')
        if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('Release source intake changed: '+relative)
    for tag in intake['countries']:
        for relative in ('common/scripted_effects/ac_release_foundations.txt','common/scripted_effects/ac_release_maintenance.txt'):
            for key,value in walk(parse((MOD/relative).read_text())):
                if key in ('set_variable','add_to_variable','subtract_from_variable') and any(name.startswith(('ac_macro_','ac_econ_')) for name,_,_ in value):raise ValueError('Release caller wrote private fiscal stock')
    return dict(countries=len(intake['countries']),protected_events=len(MODIFIED),protected_inputs=len(intake['source_inputs_sha256']),native='pending')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.reference:
        data=primary(args.reference);path=HERE/'engine_hooks.json';text=json.dumps(data,indent=2)+'\n'
        if args.check:
            if not path.exists() or path.read_text()!=text:raise SystemExit('Release primary hook contract differs')
        else:path.write_text(text,encoding='utf-8',newline='\n')
    print(json.dumps(validate(),indent=2))
