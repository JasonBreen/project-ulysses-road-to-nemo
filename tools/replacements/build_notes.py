"""Visible starting production references; no production automation or grants."""
import argparse
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
from script import parse

NOTES={
 'EMM':('Emmerian Replacement Plan',
  'Twelve military factories support ground equipment. One aviation factory replaces fighters and one replaces close air support aircraft. The six dockyards are assigned to one convoy line, three escort yards, one submarine yard and one patrol-cruiser yard. All four naval roles have starting production; they still depend on materials, repairs and available crews.'),
 'EVA':('Estovakian Replacement Plan',
  'Fourteen military factories support ground equipment. One aviation factory replaces fighters and one replaces close air support aircraft. Each of the four dockyards supports a different role: convoys, escorts, coastal submarines and patrol cruisers. Expanding one role requires capacity from another unless more industry becomes available.'),
 'SNS':('San Salvacion Replacement Plan',
  'The five military factories support one line each for infantry equipment, support equipment, artillery, fighters and close air support aircraft. Keep one dockyard on convoys. The other begins on escorts; switch that combat line to coastal submarines when necessary, then restore escort production. The fielded submarine is not a stored replacement hull. Escort and submarine replacements do not run simultaneously on this budget.'),
 'AMB':('Amber Replacement Plan',
  'The four military factories support infantry equipment, support equipment, artillery and one aviation line. Aviation begins on close air support. The fielded 36 fighters have 12 reserve fighters, while the fielded 12 close air support aircraft have 6 reserve aircraft. Switch the aviation line between fighters and close air support as losses require. Keep one dockyard on convoys and manually switch the other between escorts and coastal submarines. The fielded submarine is not a stored replacement hull. These competing roles cannot all receive production at once.'),
 'UGE':('Ugellas Replacement Plan',
  'The single dockyard begins on convoys. The two escorts are the fielded fleet, with no stored replacement hulls. To replace an escort, switch the dockyard to the available coastal-escort design in Production and resume convoys after the replacement. Escort construction pauses convoy output. Plan construction around transport losses and the fleet\'s condition.'),
 'DEL':('Delarus Replacement Plan',
  'The single dockyard begins on convoys. The two escorts are the fielded fleet, with no stored replacement hulls. Switch the yard to the available coastal-escort design when a replacement is needed, then restore convoy output. Both roles draw on the same yard; neither can receive concurrent production during the other\'s construction.')}


def outputs():
    tags=' '.join('tag = '+tag for tag in NOTES)
    category='ac_rp_replacements = {\n icon = ac_anea_recovery\n allowed = { OR = { '+tags+' } }\n visible = { OR = { '+tags+' } }\n}\n'
    decisions='ac_rp_replacements = {\n'
    loc='\ufeffl_english:\n ac_rp_replacements:0 "Replacement Production"\n ac_rp_replacements_desc:0 "Read the starting replacement allocations before changing a line. Use Production to make the manual switches described here. Losses, damaged industry and disrupted trade can change the balance."\n'
    for tag,(title,narrative) in NOTES.items():
        ident=tag+'_rp_production_notes'
        decisions+=f' {ident} = {{\n  icon = ac_anea_recovery\n  visible = {{ tag = {tag} }}\n  available = {{ always = no }}\n  cost = 0\n  complete_effect = {{ custom_effect_tooltip = ac_rp_reference_only }}\n }}\n'
        loc+=f' {ident}:0 "{title}"\n {ident}_desc:0 "{narrative}"\n'
    decisions+='}\n'
    loc+=' ac_rp_reference_only:0 "Production reference. Change the line in the Production screen; this note does not switch factories or dockyards."\n'
    result={'common/decisions/categories/ac_replacement_notes.txt':category,
            'common/decisions/ac_replacement_notes.txt':decisions,
            'localisation/english/ac_replacement_notes_l_english.yml':loc}
    for name,body in result.items():
        if not name.endswith('.yml'):parse(body)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for name,body in outputs().items():
        path=MOD/name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=body:raise SystemExit('Stale replacement notes: '+name)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body,encoding='utf-8',newline='\n')
    print('Replacement notes '+('consistent' if args.check else 'generated'))
