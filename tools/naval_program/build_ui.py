"""Compose NAVAL/LAND/AIR without replacing original GUI/font captures."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/land_program'),str(ROOT/'tools')]
import naval_ui
from script import parse
spec=importlib.util.spec_from_file_location('naval_land_owner',ROOT/'tools/land_program/build_ui.py')
land=importlib.util.module_from_spec(spec);spec.loader.exec_module(land)

def outputs():
    value,_,_=land.generated();captured=(HERE/'source/research_air_base.gui').read_text(encoding='utf-8-sig')
    if naval_ui.strip(parse(value))!=parse(captured):raise ValueError('NAVAL changed an unrelated AIR/LAND/inherited control')
    contract=dict(schema=1,base_commit='8586efeb98f4fa19be3fff44132caf799f3af1fd',
        canonical_owner='LAND generated(), with explicit pure AIR/NAVAL registrations and reviewed strict font restoration',
        captured_gui='tools/naval_program/source/research_air_base.gui',captured_gui_normalized_sha256=hashlib.sha256(captured.replace('\r\n','\n').encode()).hexdigest(),
        added_controls=sorted(naval_ui.NAMES),tab_x=naval_ui.TAB_X,card=[naval_ui.CARD_W,naval_ui.CARD_H],content=[naval_ui.CONTENT_W,naval_ui.CONTENT_H],
        blueprints=20,container=[512,260],topview=[508,248],required_controls=['equipment_image','module_slots','<native slot>/<category>','<category>@highlight'],
        fonts='Existing ACBriefing16/20 and reviewed ACResearch aliases; no raw FNT or DDS changes',
        native_acceptance=False,search='No existing bound research search; actual drag/wheel/vertical/horizontal scrolling retained')
    return {MOD/'interface/countrytechtreeview.gui':value.encode(),MOD/'interface/ac_naval_techtree.gui':naval_ui.templates().encode(),
        MOD/'interface/equipmentdesigner/ships/ac_naval_blueprints.gui':naval_ui.blueprints().encode(),HERE/'ui_contract.json':(json.dumps(contract,indent=2)+'\n').encode()}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for path,raw in outputs().items():
        if a.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n',b'\n')!=raw:raise SystemExit('Stale naval GUI: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    print('LAND+AIR+NAVAL research and 20 native ship blueprint controls: '+('consistent' if a.check else 'generated'))
