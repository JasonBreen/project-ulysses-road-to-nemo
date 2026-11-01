"""Compose AIR with the existing LAND and reviewed font owners, in either order."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path[:0]=[str(HERE),str(ROOT/'tools/land_program'),str(ROOT/'tools')]
import air_ui
from research_fonts.migration import migrate
from script import parse
spec=importlib.util.spec_from_file_location('air_land_ui_owner',ROOT/'tools/land_program/build_ui.py')
land=importlib.util.module_from_spec(spec);spec.loader.exec_module(land)


def outputs():
    value,_,_=land.generated();captured=(HERE/'source/research_land_base.gui').read_text(encoding='utf-8-sig')
    if air_ui.strip(parse(value))!=parse(migrate(captured)):raise ValueError('AIR changed an unrelated LAND/inherited control')
    contract=dict(schema=1,base_commit='549cad986c630334d398beb2e11c8e23939f3990',
        canonical_owner='tools/land_program/build_ui.py generated(), with explicit pure AIR extension and reviewed font migration',
        captured_land_gui='tools/air_program/source/research_land_base.gui',captured_land_gui_sha256=hashlib.sha256(captured.replace('\r\n','\n').encode()).hexdigest(),
        inherited_source='tools/land_program/source/research_base.gui',reviewed_fonts='tools/research_fonts/migration.py',
        added_controls=sorted(air_ui.NAMES),tab_x=air_ui.TAB_X,tab_frame=[89,30],card=[air_ui.CARD_W,air_ui.CARD_H],
        content=[air_ui.CONTENT_W,air_ui.CONTENT_H],blueprint_controls=16,blueprint_size=[508,248],
        search='No existing native research search/editbox/filter binding; real drag/wheel/vertical/horizontal scrolling preserved.',
        native='Page/blueprint discovery, mission/designer operation and native rendering remain untested')
    return {MOD/'interface/countrytechtreeview.gui':value.encode(),MOD/'interface/ac_air_techtree.gui':air_ui.templates().encode(),
        MOD/'interface/equipmentdesigner/planes/ac_air_blueprints.gui':air_ui.blueprints().encode(),
        HERE/'ui_contract.json':(json.dumps(contract,indent=2)+'\n').encode()}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for path,data in outputs().items():
        if args.check:
            old=path.read_bytes() if path.exists() else b''
            if old.replace(b'\r\n',b'\n')!=data:raise SystemExit('Stale composed AVIATION UI: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('LAND+AIR research composition and16blueprint controls:', 'consistent' if args.check else 'generated')
