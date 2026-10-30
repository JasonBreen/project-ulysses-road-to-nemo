"""Restore the engine background canvas/picker while retaining Ulysses menu layout."""
from pathlib import Path
import re
from script import parse,render,get,setv,walk,xy
ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'mod/2985041246/interface/frontendmainview.gui'

def span(text,name):
    found=re.search(r'\bname\s*=\s*"'+name+'"',text)
    start=text.rfind('containerWindowType',0,found.start())
    opening=text.index('{',start);depth=1;pos=opening+1
    while depth:
        if text[pos]=='{':depth+=1
        elif text[pos]=='}':depth-=1
        pos+=1
    return start,pos

def build(text):
    a,b=span(text,'frontend_background')
    text=text[:a]+'''containerWindowType = {
        name = "frontend_background"
        position = { x=0 y=0 }
        size = {
            width = 1920 height = 1080
            min = { width=100% height=100% }
            max = { width=10000 height=10000 }
            preserve_aspect_ratio = yes
        }
        orientation = center
        origo = center
        clipping = no
        background = {
            name = "Background"
            quadTextureSprite = "GFX_frontend_bg"
            alwaysTransparent = yes
        }
    }'''+text[b:]
    a,b=span(text,'change_background');tree=parse(text[a:b])
    setv(tree[0][2],'position',xy(-20,-20))
    aliases={'GFX_button_238x38':'GFX_ac_ui_button_238x38',
             'GFX_tiled_window2_1b_border':'GFX_ac_ui_tiled_window2_1b_border',
             'GFX_generic_checkbox':'GFX_ac_ui_generic_checkbox',
             'GFX_tiled_window_transparent':'GFX_ac_ui_tiled_window_transparent'}
    for _,node in walk(tree):
        for field in ('quadTextureSprite','spriteType'):
            old=get(node,field,'').strip('"')
            if old in aliases:setv(node,field,'"'+aliases[old]+'"')
        for field in ('font','buttonFont'):
            if get(node,field):setv(node,field,'"Aces16"')
        if get(node,'verticalScrollbar'):setv(node,'verticalScrollbar','"ac_exp_right_vertical_slider"')
    return text[:a]+render(tree)+text[b:]

if __name__=='__main__':
    text=TARGET.read_text(encoding='utf-8-sig');TARGET.write_text(build(text),encoding='utf-8')
    print('Full-viewport briefing background and selectable original/official artwork restored.')
