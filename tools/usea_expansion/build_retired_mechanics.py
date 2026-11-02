"""Quarantine inherited Earth/WWII mechanics; retain IDs for queued old saves."""
import argparse,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;MOD=HERE.parents[1]/'mod/2985041246'
IDEAS=['draft_dodging','draft_dodging_2','draft_dodging_3','strikes_1','strikes_2','strikes_3','mutiny_1','mutiny_2','mutiny_3']
MISSIONS=['draft_dodging_mission','strikes_mission','mutiny_mission']

def build():
    outputs={}
    for row in json.loads((HERE/'retired_event_contract.json').read_text()):
        kind=row.get('event_kind','country_event')
        if kind not in ('country_event','news_event'):
            raise ValueError('Unsupported retired event kind: '+kind)
        text=('# Retired inherited Earth/WWII news. IDs remain harmless for queued old saves.\n' if kind=='news_event' else '# Retired WWII/generic politics mechanic. IDs remain harmless for queued old saves.\n')
        text+='\n'.join('add_namespace = '+ns for ns in row['namespaces'])+'\n'
        for ident in row['events']:
            text+=kind+' = { id = '+ident+' hidden = yes is_triggered_only = yes immediate = { '+('ac_retire_vanilla_crises = yes' if ident.startswith('stability.') else '')+' } }\n'
        outputs['events/'+row['file']]=text
    body='\n'.join('remove_ideas = '+idea for idea in IDEAS)
    body+='\n'+'\n'.join('if = { limit = { has_active_mission = '+m+' } remove_mission = '+m+' }' for m in MISSIONS)
    body+='\nclr_country_flag = crisis_in_progress\nclr_country_flag = crisis_solution_in_progress\n'
    # Safe to call from old queued events as well as startup. Only these retired
    # penalties are touched, so no once flag is needed and no rewards are paid.
    outputs['common/scripted_effects/ac_retired_mechanics.txt']='ac_retire_vanilla_crises = {\n'+body+'}\n'
    outputs['common/on_actions/ac_retired_mechanics.txt']='on_actions = { on_startup = { effect = { every_country = { ac_retire_vanilla_crises = yes } } } }\n'
    outputs['common/decisions/categories/ac_retired_mechanics.txt']='ac_retired_mechanics = { allowed = { always = no } visible = { always = no } visible_when_empty = no }\n'
    outputs['common/decisions/ac_retired_mechanics.txt']='ac_retired_mechanics = {\n'+'\n'.join(m+' = { allowed = { always = no } visible = { always = no } days_mission_timeout = 1 timeout_effect = { ac_retire_vanilla_crises = yes } }' for m in MISSIONS)+'\n}\n'
    return outputs

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for name,text in build().items():
        target=MOD/name
        if a.check:
            if not target.exists() or target.read_text()!=text:raise SystemExit('Retired mechanic output differs: '+name)
        else:target.write_text(text,encoding='utf-8',newline='\n')
    print('Retired generic ideology/crisis events; old-save crisis penalties have bounded cleanup.')
