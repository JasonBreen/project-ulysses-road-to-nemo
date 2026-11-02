"""Restore only reviewed additions, then compare complete ordered source ASTs.

Independent from the authoring transforms. Country scopes, options, condition
branches, command order/values and unprotected rewards all remain significant.
Immutable event_inputs.json is never recaptured to accept a delivered mutation.
"""
import copy
from script import parse,get

META={'name','ai_chance','trigger','highlighted'}
MODIFIED={'awwnb.1','awwnb.2','recta.1','south_belka.2','south_belka.3','south_belka.4','belka_dlp_war.101','belka_dlp_war.103'}
AWW_ARMY='country_exists = AWW NOT = { has_global_flag = ac_release_AWW_legacy_oob_done } NOT = { has_global_flag = ac_release_AWW_annexed } AWW = { has_country_flag = ac_release_awaiting_legacy_army has_capitulated = no }'
GATES={'awwnb.1':'NOT = { has_global_flag = ac_release_AWW_entry_begun }',
       'awwnb.2':AWW_ARMY,
       'recta.1':'NOT = { has_global_flag = ac_release_REC_legacy_oob_done } NOT = { has_global_flag = ac_release_REC_adopted }'}
for ident in ('south_belka.2','south_belka.3','south_belka.4'):
    GATES[ident]='NOT = { has_global_flag = ac_release_SBK_entry_begun } NOT = { has_global_flag = ac_release_SBK_adopted }'


def require(condition,message):
    if not condition:raise ValueError('Protected ordered event contract changed: '+message)


def suffix(nodes,text,where):
    expected=parse(text)
    require(len(nodes)>=len(expected) and nodes[-len(expected):]==expected,where+' reviewed suffix')
    del nodes[-len(expected):]


def restore_transfer_guards(nodes,tag):
    """Only a direct BLK transfer may have this exact once-only wrapper."""
    for key,_,body in nodes:
        if not isinstance(body,list):continue
        if key=='BLK':
            for index,node in enumerate(list(body)):
                require(not(node[0]=='transfer_units_fraction'and get(node[2],'target')==tag),tag+' missing transfer guard')
                if node[0]!='if' or not isinstance(node[2],list):continue
                guarded=node[2]
                limit=parse('country_exists = '+tag+' NOT = { has_global_flag = ac_release_'+tag+'_transfer_done }')
                if get(guarded,'limit')!=limit:continue
                require(node[1]=='=' and len(guarded)==3 and guarded[0]==['limit','=',limit] and guarded[1][0]=='transfer_units_fraction' and
                        get(guarded[1][2],'target')==tag and guarded[2]==['set_global_flag','=','ac_release_'+tag+'_transfer_done'],tag+' transfer wrapper')
                body[index]=guarded[1]
        restore_transfer_guards(body,tag)


def original_option_order(original,metadata,effects,where):
    require(len(metadata)==sum(n[0]in META for n in original),where+' metadata length')
    require(len(effects)==sum(n[0]not in META for n in original),where+' effect length')
    metadata=iter(metadata);effects=iter(effects)
    return [next(metadata)if n[0]in META else next(effects)for n in original]


def restore_option(ident,original,candidate):
    if ident.startswith('belka_dlp_war.'):
        suffix(candidate,'REC = { ac_release_observe_country = yes } SBK = { ac_release_observe_country = yes }',ident)
        return candidate
    expected_metadata=[n for n in original if n[0]in META]
    require(len(candidate)==len(expected_metadata)+1 and candidate[:len(expected_metadata)]==expected_metadata,ident+' option ownership/presentation')
    wrapped=candidate[-1]
    gate=('NOT = { has_global_flag = ac_release_AWW_adopted } NOT = { has_global_flag = ac_release_AWW_legacy_oob_done } NOT = { has_global_flag = ac_release_AWW_entry_begun }'
          if ident=='awwnb.1'else GATES[ident])
    require(wrapped[0]=='if' and wrapped[1]=='=' and wrapped[2] and wrapped[2][0]==['limit','=',parse(gate)],ident+' option guard')
    effects=wrapped[2][1:]
    if ident=='awwnb.1':
        suffix(effects,'set_global_flag = ac_release_AWW_entry_begun',ident)
        for key,_,value in effects:
            if key=='AWW':suffix(value,'set_country_flag = { flag = ac_release_awaiting_legacy_army days = 7 }',ident+' AWW scope')
        restore_transfer_guards(effects,'AWW')
    elif ident=='awwnb.2':
        suffix(effects,'set_global_flag = ac_release_AWW_legacy_oob_done AWW = { clr_country_flag = ac_release_awaiting_legacy_army ac_release_observe_country = yes }',ident)
    elif ident=='recta.1':
        suffix(effects,'set_global_flag = ac_release_REC_legacy_oob_done REC = { ac_release_observe_country = yes }',ident)
    else:
        suffix(effects,'set_global_flag = ac_release_SBK_entry_begun SBK = { ac_release_observe_country = yes }',ident)
        restore_transfer_guards(effects,'SBK')
    return original_option_order(original,expected_metadata,effects,ident)


def restore_event(ident,original,candidate):
    candidate=copy.deepcopy(candidate)
    snapshot=ident!='awwnb.2';gate=GATES.get(ident)
    expected_heads=[n[:2]for n in original]
    if snapshot and get(original,'immediate')is None:expected_heads.append(['immediate','='])
    if gate and get(original,'trigger')is None:expected_heads.append(['trigger','='])
    require([n[:2]for n in candidate]==expected_heads,ident+' ordered event fields/options')
    if gate:
        trigger=get(candidate,'trigger');suffix(trigger,gate,ident+' trigger')
        if get(original,'trigger')is None:
            require(not trigger,ident+' added trigger has unrelated conditions')
            candidate[:]=[n for n in candidate if n[0]!='trigger']
    if snapshot:
        immediate=get(candidate,'immediate')
        require(immediate and immediate[0]==['ac_release_snapshot_world','=','yes'],ident+' initial snapshot')
        del immediate[0]
        if ident=='awwnb.1':
            limit=parse('NOT = { has_global_flag = ac_release_AWW_adopted }')
            require(len(immediate)==1 and immediate[0][:2]==['if','='] and immediate[0][2] and immediate[0][2][0]==['limit','=',limit],ident+' immediate adoption guard')
            immediate[:]=immediate[0][2][1:]
        if get(original,'immediate')is None:
            require(not immediate,ident+' added immediate has unrelated commands')
            candidate[:]=[n for n in candidate if n[0]!='immediate']
    original_options=[n[2]for n in original if n[0]=='option']
    options=[n for n in candidate if n[0]=='option']
    require(len(original_options)==len(options),ident+' option count')
    for old,node in zip(original_options,options):node[2]=restore_option(ident,old,node[2])
    return candidate


def validate_file(original_text,candidate_text,relative):
    original=parse(original_text);candidate=parse(candidate_text)
    require(len(original)==len(candidate),relative+' top-level length')
    for index,(old,new)in enumerate(zip(original,candidate)):
        require(old[:2]==new[:2],relative+' top-level scope/order '+str(index))
        if old[0]=='country_event':
            ident=get(old[2],'id').strip('"')
            require(get(new[2],'id')==get(old[2],'id'),relative+' event identity/order '+ident)
            restored=restore_event(ident,old[2],new[2])if ident in MODIFIED else new[2]
            require(old[2]==restored,relative+' '+ident+' complete ordered AST')
        else:require(old==new,relative+' unrelated top-level node '+str(index))
