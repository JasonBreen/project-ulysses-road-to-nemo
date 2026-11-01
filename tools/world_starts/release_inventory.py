"""Inventory dormant country entry contracts without granting setup or changing wars.

This records inherited source and known release-owner gaps. Event definitions,
literal callers and per-event fire_only_once are observations, not proof of
native reachability, mutual exclusion or safe repeated/reloaded setup.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse,get


def walk(nodes):
    """Visit scalar effects as well as blocks; script.walk visits blocks only."""
    for key,_,value in nodes:
        yield key,value
        if isinstance(value,list):yield from walk(value)

OWNERS={'AWW':('awwnb.1','awwnb.2'),'REC':('recta.1',),'SBK':('south_belka.2','south_belka.3','south_belka.4')}

def source_digest(path):
    """Portable authored-text identity; native payload hashes remain separate."""
    return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def path_order(path):
    """Explicit case-sensitive order, independent of WindowsPath comparison."""
    return path.as_posix()


def report():
    registry=json.loads((ROOT/'tools/world_foundation/country_registry.json').read_text())
    emergent={row['tag']:row for row in registry['countries'] if row['start_classification']=='emergent'}
    if set(emergent)!={'AWW','REC','REL','SBK','SER','SHI','TER'}:raise ValueError('Dormant entry scope changed; inspect the legitimate release owners')
    files={};definitions={};callers={}
    for folder in ('events','common/on_actions','common/scripted_effects','common/national_focus','common/decisions'):
        for path in sorted((MOD/folder).rglob('*.txt'),key=path_order):
            relative=path.relative_to(MOD).as_posix();tree=parse(path.read_text(encoding='utf-8-sig'));files[relative]=tree
            if folder=='events':
                for key,_,body in tree:
                    if key in ('country_event','news_event') and isinstance(body,list):
                        definitions[get(body,'id').strip('"')]=(relative,body)
            # Top-level event definitions are excluded from literal call sites.
            for key,_,body in tree:
                for ident,value in walk(body if isinstance(body,list) else []):
                    if ident=='country_event':
                        target=get(value,'id') if isinstance(value,list) else value
                        if isinstance(target,str):callers.setdefault(target.strip('"'),[]).append(relative)
    release_path=ROOT/'tools/release_foundations/worksheet.json'
    release=json.loads(release_path.read_text())['countries'] if release_path.exists() else {}
    rows=[];used=set()
    for tag,registered in sorted(emergent.items()):
        history=MOD/registered['history'];used.add(history);source=history.read_text(encoding='utf-8-sig');tree=parse(source)
        owners=[];entry_scopes=[]
        for relative,parsed in files.items():
            for key,value in walk(parsed):
                if key==tag and isinstance(value,list):
                    operations=sorted({field for field,_ in walk(value) if field in ('transfer_state','load_oob','set_oob','set_air_oob','set_naval_oob','inherit_technology')})
                    if operations:entry_scopes.append(dict(source=relative,operations=operations));used.add(MOD/relative)
                elif key in ('release','release_puppet') and value==tag:
                    entry_scopes.append(dict(source=relative,operations=[key]));used.add(MOD/relative)
        for ident in OWNERS.get(tag,()):
            relative,body=definitions[ident];used.add(MOD/relative)
            scopes=[value for key,value in walk(body) if key==tag and isinstance(value,list)]
            owners.append(dict(event=ident,source=relative,literal_callers=sorted(set(callers.get(ident,[]))),
                fire_only_once=get(body,'fire_only_once','no'),
                transferred_states=sorted({int(value) for scope in scopes for key,value in walk(scope) if key=='transfer_state'}),
                inherited_technology_from=sorted({value for scope in scopes for key,value in walk(scope) if key=='inherit_technology'}),
                direct_force_loads=sorted({value.strip('"') for scope in scopes for key,value in walk(scope) if key in ('load_oob','set_oob','set_air_oob','set_naval_oob')}),
                received_unit_fractions=sorted({float(get(value,'size')) for key,value in walk(body) if key=='transfer_units_fraction' and get(value,'target')==tag}),
                trigger=get(body,'trigger',[])))
            used.update(MOD/p for p in callers.get(ident,[]))
        rosters=[]
        for path in sorted((MOD/'history/units').glob(tag+'_*.txt'),key=path_order):
            used.add(path);parsed=parse(path.read_text(encoding='utf-8-sig'))
            rosters.append(dict(source=path.relative_to(MOD).as_posix(),divisions=sum(key=='division' for key,_ in walk(parsed)),
                production_lines=sum(key=='add_equipment_production' for key,_ in walk(parsed))))
        gaps=['No reviewed release-time physical foundation owner with current-state eligibility, shared once guard, DLC-aware replacements, transport/resource/fuel and interrupted/re-release acceptance.']
        if tag=='AWW':gaps+=['awwnb.1 has no literal caller in the scanned authored event/focus/decision/on-action/effect source.','awwnb.2 loads nine additional formations after a 25% BLK unit transfer; no shared once-only setup flag is present in these event definitions.']
        elif tag=='REC':gaps+=['recta.1 loads ten formations without an explicit setup-once flag; later Belkan treaty state transfers can also recreate REC without calling recta.1.']
        elif tag=='SBK':gaps+=['Three individually fire-only-once events transfer a BLK army fraction; no shared group setup-once flag is established by those definitions. Belkan treaty creation is a separate path without the same transfer.']
        else:gaps+=['No authored release/setup event owner identified for this dormant tag; generic engine release behavior is not acceptance evidence.']
        status='pending_legitimate_release_owner_review'
        if tag in release:
            for relative in ('common/scripted_effects/ac_release_foundations.txt','common/scripted_effects/ac_release_maintenance.txt','common/scripted_triggers/ac_release_foundations.txt','common/scripted_triggers/ac_release_maintenance.txt','common/on_actions/ac_release_foundations.txt','events/ac_release_projects.txt'):
                target=MOD/relative
                if not target.exists():raise ValueError('Release worksheet has no actual owner: '+relative)
                used.add(target)
            status='guarded_legitimate_release_owner_source_implemented_native_pending'
            gaps=['Native release/loading, transfer selection, DLC replacement operation, supply/AI pacing and save/reload remain untested.',
                  release[tag]['unknown_footprint_status'],
                  'Replacement imports are conditional live material checks, not guaranteed authored trade contracts; existing mixed transferred roles may exceed domestic replacement capacity.']
            if tag=='AWW':gaps+=['awwnb.1 still has no authored literal activation caller; no new war/activation was invented.',
                'Preserved disarmed/no-core personnel and non-core industry liability; only the original optionA retains its existing weekly recruiting idea. Other inherited warfront OOB positions are not newly validated owned deployment sites.']
            elif tag in ('REL','SER','SHI','TER'):gaps+=['No authored forced activation route; the adapter waits for an actual legitimate engine release.']
        rows.append(dict(tag=tag,history=registered['history'],owned_states=registered['owned_states'],
            history_force_loads=[value.strip('"') for key,_,value in tree if key in ('load_oob','set_oob','set_air_oob','set_naval_oob')],
            entry_events=owners,other_observed_entry_scopes=entry_scopes,existing_tag_rosters=rosters,status=status,gaps=gaps))
    return dict(schema=1,scope='Seven nonlandowning inherited histories; no start grant, retroactive setup, new war or tag is introduced.',
        source_evidence='Literal source inventory only; native release, event reachability, transfer randomness, re-release and save/reload are not established.',
        active_tag_clarification='RAT is the active Ratio country, covered by WorldStarts; SBL is not a registered country history/tag here. South Belka is SBK.',
        excluded_placeholder='PLH/state171 remains unresolved and receives no inferred release or setup.',
        source_input_hash_convention='SHA256 of authored UTF8 text with CRLF normalized to LF; no other whitespace or content normalization. Not a native payload hash.',
        source_inputs_sha256={path.relative_to(MOD).as_posix():source_digest(path) for path in sorted(used,key=path_order)},countries=rows)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    data=report();text=json.dumps(data,indent=2)+'\n';path=HERE/'release_inventory.json'
    if args.check:
        if not path.exists() or path.read_text()!=text:raise SystemExit('Dormant release inventory differs; inspect the owning contracts before updating')
    else:path.write_text(text,encoding='utf-8',newline='\n')
    print('Dormant histories:',len(data['countries']),'; source owners and remaining entry/native obligations inventoried; no country is spawned by this inspector.')
