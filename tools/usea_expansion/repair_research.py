"""Bind research GUI dependencies to explicit authored sprites and scrollbars."""
import json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
def main():
    report=json.loads((ROOT/'docs/evidence/usea-expansion/engine-dependencies.json').read_text())
    names=[row['sprite'] for row in report['countrytechtreeview.gui']['sprites'] if row['ownership']=='engine or missing']
    target=MOD/'interface/countrytechtreeview.gui';text=target.read_text(encoding='utf-8-sig')
    for name in names:text=text.replace('"'+name+'"','"GFX_ac_ui_'+name.removeprefix('GFX_')+'"')
    for bar in ('right_vertical_slider','bottom_horizontal_slider','standardtext_slider'):
        text=re.sub(r'(?<!ac_exp_)\b'+bar+r'\b','ac_exp_'+bar,text)
    target.write_text(text,encoding='utf-8')
    print('Bound',len(names),'engine research dependencies to authored presentation.')
if __name__=='__main__':main()
