"""Bounded additive research page; preserve the inherited control contract."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools/usea_expansion'))
sys.path.insert(0,str(ROOT/'tools'))
from script import parse,get,walk
from land_content import FAMILIES
from research_fonts.migration import migrate,restore

SOURCE=HERE/'source/research_base.gui'
TARGET=MOD/'interface/countrytechtreeview.gui'
TAB_X=992;GRID_X=260;GRID_Y=160;ROW_PITCH=140;SLOT_X=60;TIER_PITCH=240
CARD_W=183;CARD_H=84;CONTENT_W=1260;CONTENT_H=1320


def block(name,text):return name+' = {\n'+'\n'.join('\t'+v for v in text.splitlines())+'\n}\n'
def text(name,value,x,y,width,height,font='ACBriefing16'):
    return block('instantTextBoxType',f'name = "{name}"\nposition = {{ x = {x} y = {y} }}\nfont = "{font}"\ntext = "{value}"\nmaxWidth = {width}\nmaxHeight = {height}\nformat = left')


def folder():
    body='name = "ac_land_folder"\nposition = { x = 0 y = 47 }\nsize = { width = 100%% height = 100%% }\n'
    body+='margin = { top = 13 left = 13 bottom = 24 right = 25 }\ndrag_scroll = { left middle }\nverticalScrollbar = "ac_exp_right_vertical_slider"\nhorizontalScrollbar = "ac_exp_bottom_horizontal_slider"\nscroll_wheel_factor = 40\n'
    content=f'name = "ac_land_scroll_content"\nposition = {{ x = 0 y = 0 }}\nsize = {{ width = {CONTENT_W} height = {CONTENT_H} min = {{ width = 100%% height = 100%% }} }}\nclipping = no\n'
    content+=block('background','name = "Background"\nquadTextureSprite = "GFX_ac_land_sheet"')
    content+=text('ac_land_heading','ac_land_page_heading',24,20,1120,32,'ACBriefing20')
    content+=text('ac_land_scope','ac_land_page_scope',24,54,1150,36)
    for index,year in enumerate((2006,2010,2015,2020)):
        content+=text('ac_land_year_'+str(year),str(year),GRID_X+index*TIER_PITCH,102,CARD_W,24,'ACBriefing20')
    for index,family in enumerate(FAMILIES):
        content+=text('ac_land_label_'+family.id,'ac_land_label_'+family.id,24,GRID_Y+index*ROW_PITCH+22,204,40)
    body+=block('containerWindowType',content)
    for index,family in enumerate(FAMILIES):
        body+=block('gridBoxType',f'name = "ac_land_{family.id}_2006_tree"\nposition = {{ x = {GRID_X} y = {GRID_Y+index*ROW_PITCH} }}\nslotsize = {{ width = {SLOT_X} height = 70 }}\nformat = "LEFT"')
    return block('containerWindowType',body)


def tab():
    return block('buttonType',f'name = "ac_land_folder_tab"\nposition = {{ x = {TAB_X} y = 0 }}\nquadTextureSprite = "GFX_ac_land_folder_tab"\nframe = 1\ntext = "ac_land_tab_short"\nbuttonFont = "ACBriefing16"\nclicksound = ui_research_tab_armor')


def item(small=False):
    name='techtree_ac_land_folder_'+('small_item' if small else 'item')
    body=f'name = "{name}"\nposition = {{ x = 0 y = 0 }}\nsize = {{ width = {CARD_W} height = {CARD_H} }}\nclipping = no\n'
    body+=block('background','name = "Background"\nquadTextureSprite = "GFX_technology_unavailable_item_bg"')
    body+=text('Name','',4,2,175,36)
    body+=block('iconType','name = "Icon"\nposition = { x = 91 y = 59 }\nspriteType = "GFX_technology_medium"\ncenterposition = yes\nalwaystransparent = yes')
    body+=block('iconType','name = "bonus_icon"\nposition = { x = 0 y = -22 }\nspriteType = "GFX_tech_bonus"')
    body+=text('bonus','',18,-22,80,20)
    body+=block('iconType','name = "can_assign_design_team_icon"\nposition = { x = 156 y = 62 }\nspriteType = "GFX_ac_ui_design_team_icon"\nscale = 0.5')
    body+=block('gridBoxType','name = "special_project_specialization_list"\nposition = { x = -20000 y = -20000 }')
    return block('containerWindowType',body)


def normalized(tree):
    tree=copy.deepcopy(tree)
    def clean(nodes):
        kept=[]
        for key,op,value in nodes:
            if isinstance(value,list):
                name=get(value,'name','').strip('"') if isinstance(get(value,'name',''),str) else ''
                if name in ('ac_land_folder','ac_land_folder_tab'):continue
                if name=='tech_info_description':value[:]=[n for n in value if n[0]!='scrollbarType']
                clean(value)
            kept.append([key,op,value])
        nodes[:]=kept
    clean(tree)
    return restore(tree,SOURCE.read_text(encoding='utf-8-sig'))


def generated():
    base=SOURCE.read_text(encoding='utf-8-sig');value=migrate(base)
    marker=re.search(r'(?m)^\s*containerWindowType\s*=\s*\{\s*\n\s*name\s*=\s*"folder_tabs"',value)
    if not marker:raise ValueError('Required research folder_tabs control missing')
    value=value[:marker.start()]+'\n'+folder()+'\n'+value[marker.start():]
    marker=re.search(r'(?m)^\s*buttonType\s*=\s*\{\s*\n\s*name\s*=\s*"infantry_folder_tab"',value)
    if not marker:raise ValueError('Required infantry tab control missing')
    value=value[:marker.start()]+'\n'+tab()+'\n'+value[marker.start():]
    # Scroll the existing narrative rectangles instead of truncating new text
    # or moving the engine-bound research/start/progress/reward controls.
    value,count=re.subn(r'(name\s*=\s*"tech_info_description"\s*\n)',r'\1\t\t\tscrollbarType = "ac_exp_standardtext_slider"\n',value)
    if count!=2:raise ValueError('Expected both inherited research detail descriptions')
    if normalized(parse(value))!=parse(base):raise ValueError('Land page changed an unrelated inherited GUI control')
    templates='guiTypes = {\n'+item()+item(True)+'}\n'
    contract=dict(base_sha256=hashlib.sha256(base.replace('\r\n','\n').encode()).hexdigest(),
        source='tools/land_program/source/research_base.gui',tab_x=TAB_X,card=[CARD_W,CARD_H],
        root_grid=[GRID_X,GRID_Y],row_pitch=ROW_PITCH,tier_pitch=TIER_PITCH,slot_width=SLOT_X,
        content=[CONTENT_W,CONTENT_H],new_roots=[f'ac_land_{v.id}_2006_tree' for v in FAMILIES],
        intentional_existing_changes='Two description scrollbarType attributes and reviewed research font substitutions only; original geometry and all other controls unchanged.',
        reviewed_font_migration='tools/research_fonts/assets.json; strict restoration preserves the unchanged captured GUI fingerprint.',
        search='No search/editbox/filter binding exists in the captured mod or installed1.19.4.1 research screen; no unbound search widget is added.',
        native='New tab/control discovery, native scrolling and state rendering remain untested.')
    return value,templates,json.dumps(contract,indent=2)+'\n'


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    value,templates,contract=generated()
    for path,text in [(TARGET,value),(MOD/'interface/ac_land_techtree.gui',templates),(HERE/'ui_contract.json',contract)]:
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=text:raise SystemExit('Stale land GUI: '+str(path))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(text.encode('utf-8'))
    print('Land research GUI '+('consistent' if args.check else 'generated'))
