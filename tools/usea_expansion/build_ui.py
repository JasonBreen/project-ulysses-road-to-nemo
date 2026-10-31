"""Build ACES focus UI from a recorded engine control contract, not game pixels.

The JSON records required control identities and compatibility geometry for 1.19.4.
--capture-contract is an explicit developer-only metadata import; ordinary builds
need no installed game. Original textures are produced by build_art.py.
"""
import argparse,copy,json,re,sys
from pathlib import Path
from script import parse,render,get,setv,walk,xy,size

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MOD=ROOT/'mod/2985041246'


def build():
    tree=json.loads((HERE/'focus_contract.json').read_text())
    tree[0][2].extend(json.loads((HERE/'scrollbar_contract.json').read_text()))
    for kind,node in walk(tree):
        for field in ('scrollbarType','verticalScrollbar','horizontalScrollbar'):
            old=get(node,field)
            if isinstance(old,str) and old.strip('"') in ('standardtext_slider','right_vertical_slider','bottom_horizontal_slider'):
                setv(node,field,'"ac_exp_'+old.strip('"')+'"')
        for field in ('font','buttonFont'):
            old=get(node,field)
            if old:
                pts=20 if any(s in old for s in ('24','36','20')) else 16
                setv(node,field,'"ACBriefing%d"'%pts)
        # All static focus chrome has its own sprite; dynamic country flags remain
        # engine bindings whose images come from the mod's flag set.
        for field in ('spriteType','quadTextureSprite'):
            old=get(node,field)
            if old and old.strip('"') not in ('GFX_flag_small2',):
                setv(node,field,'"GFX_ac_ui_'+old.strip('"').removeprefix('GFX_')+'"')
        if get(node,'name') in ('"national_focus_detail_view"','"coninuous_focus_detail_view"'):
            setv(node,'size',size(610,680))
            setv(node,'position',xy(0,-20))
            setv(node,'orientation','CENTER');setv(node,'origo','CENTER')
            for _,child in walk(node):
                name=get(child,'name','').strip('"')
                if name=='name':
                    setv(child,'maxWidth','510');setv(child,'maxHeight','48')
                elif name=='statsarea':
                    setv(child,'position',xy(18,220));setv(child,'size',size(574,440))
                elif name=='desc':
                    setv(child,'position',xy(30,238));setv(child,'maxWidth','548')
                    setv(child,'maxHeight','190');setv(child,'format','left')
                    setv(child,'font','"ACBriefing16"');setv(child,'scrollbarType','standardtext_slider')
                elif name=='reward_bg':setv(child,'position',xy(30,442))
                elif name=='reward_label':
                    setv(child,'position',xy(32,444));setv(child,'maxWidth','540');setv(child,'maxHeight','24')
                elif name=='reward':
                    setv(child,'position',xy(30,480));setv(child,'maxWidth','548');setv(child,'maxHeight','164')
                elif name=='prerequisites_bg':setv(child,'position',xy(212,94))
                elif name=='prerequisites':
                    setv(child,'position',xy(222,102));setv(child,'maxWidth','350');setv(child,'maxHeight','100')
                elif name in ('start','stop'):setv(child,'position',xy(450,55))
        if get(node,'name') in ('"national_focus_item"','"continuous_national_focus_item"'):
            continuous=get(node,'name')=='"continuous_national_focus_item"'
            setv(node,'size',size(180 if continuous else 165,164 if continuous else 144))
            for _,child in walk(node):
                if get(child,'name')=='"name"':
                    # The shipped font has an 18px line height: three lines need 54px.
                    setv(child,'font','"ACBriefing16"');setv(child,'maxHeight','54')
                    setv(child,'position',xy(15,100 if continuous else 44))
                if continuous and get(child,'name')=='"symbol"':
                    setv(child,'position',xy(40,0))
                elif not continuous and get(child,'name')=='"symbol"':
                    #144/2-80-96/2=-56: the96px icon ends at40,
                    #where the64px caption frame begins. Grid padding below
                    #keeps the first icon clear of the screen header.
                    setv(child,'position',xy(5,-80))
                elif continuous and get(child,'name')=='"bg"':
                    setv(child,'position',xy(5,96))
                elif continuous and get(child,'name')=='"pol_power_icon"':
                    setv(child,'position',xy(142,3))
                elif continuous and get(child,'name')=='"focus_cost"':
                    setv(child,'position',xy(140,26));setv(child,'maxWidth','32')
                elif not continuous and get(child,'name')=='"historical"':
                    setv(child,'position',xy(-12,-40))
                elif not continuous and get(child,'name')=='"viewing_flag"':
                    setv(child,'position',xy(130,-40))
                elif not continuous and get(child,'name')=='"viewing_flag_border"':
                    setv(child,'position',xy(125,-45))
        if get(node,'name')=='"focus_spacing"':setv(node,'position',xy(96,160))
        if get(node,'name')=='"grid_window"':
            for child_kind,_,child in node:
                if child_kind.lower()=='gridboxtype' and isinstance(child,list) and get(child,'name')=='"grid"':
                    setv(child,'position',xy(50,66))
        if get(node,'name') in ('"exclusive_offset"','"exclusive_offset_left"'):
            #28px item offset +(-28)px route offset +16px marker centre
            #places exclusions at16px, clear of the44–98px caption band.
            setv(get(node,'position'),'y','-28')
        if get(node,'name')=='"continuous_focus_window"':
            setv(node,'size',size(770,456))
            for _,child in walk(node):
                name=get(child,'name','').strip('"')
                if name=='continuous_focus_title':setv(child,'maxHeight','24')
                elif name=='continuous_focus_desc':
                    setv(child,'position',xy(23,48));setv(child,'maxHeight','36')
                elif name=='continuous_focus_progress':setv(child,'maxHeight','24')
                elif name=='entries':
                    setv(child,'position',xy(13,88));setv(child,'size',size(744,352))
                elif name=='list':
                    setv(child,'position',xy(16,8));setv(child,'slotsize',size(180,172))
    return '# ACES briefing interface; 1.19.4 engine control contract, original presentation.\n'+render(tree)+'\n'


def main():
    p=argparse.ArgumentParser();p.add_argument('--capture-contract',type=Path);p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.capture_contract:
        tree=parse((a.capture_contract/'interface/nationalfocusview.gui').read_text(encoding='utf-8-sig'))
        (HERE/'focus_contract.json').write_text(json.dumps(tree,indent=2)+'\n')
    target=MOD/'interface/nationalfocusview.gui';result=build()
    if a.check:
        if not target.exists() or target.read_text()!=result:raise SystemExit('Focus GUI differs from authoring source')
    else:target.write_text(result,encoding='utf-8')
    print('Focus UI: bounded 190px narrative and 164px rewards; both scrollable; normal and continuous details.')


if __name__=='__main__':main()
