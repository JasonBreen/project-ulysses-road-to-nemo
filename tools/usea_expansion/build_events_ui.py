"""Bound long country/news narratives without shortening localized text.

Engine container/control names and dynamic option layout remain intact. Country
and news chrome uses original ACES textures; operative/leader layouts retain
their engine contract and are outside this repair's visual-acceptance claim.
"""
import argparse,json
from pathlib import Path
from script import render,get,setv,walk
HERE=Path(__file__).resolve().parent;MOD=HERE.parents[1]/'mod/2985041246'

def build():
    tree=json.loads((HERE/'event_contract.json').read_text())
    for kind,_,root in tree[0][2]:
        if not isinstance(root,list):continue
        name=get(root,'name','').strip('"')
        if name not in ('EventWindow','EventWindow_News','event_option_entry'):continue
        for _,node in walk([[kind,'=',root]]):
            child=get(node,'name','').strip('"')
            if child in ('Title','Description','Name'):
                setv(node,'font','"ACBriefing20"' if child=='Title' else '"ACBriefing16"')
            if child=='Description':
                setv(node,'maxHeight','200' if name=='EventWindow_News' else '230')
                setv(node,'scrollbarType','"ac_exp_standardtext_slider"')
            for field in ('spriteType','quadTextureSprite'):
                old=get(node,field)
                if old and child not in ('event_picture',):
                    setv(node,field,'"GFX_ac_ui_'+old.strip('"').removeprefix('GFX_')+'"')
    return '# 1.19.4 event control contract; scrollable narratives and original ACES chrome.\n'+render(tree)+'\n'

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    target=MOD/'interface/eventwindow.gui';text=build()
    if a.check:
        if not target.exists() or target.read_text()!=text:raise SystemExit('Event GUI differs from authoring source')
    else:target.write_text(text,encoding='utf-8')
    print('Country/news descriptions scroll independently; event IDs and option controls preserved.')
