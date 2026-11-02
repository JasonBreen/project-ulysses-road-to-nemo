"""Pure AIR page extension; shared research composition is owned with LAND."""
import copy
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE),str(ROOT/'tools/usea_expansion')]
from script import get
from air_content import YEARS,FAMILIES,AIRCRAFT,frame_id

NAMES={'ac_air_folder','ac_air_folder_tab'}
TAB_X=1088;GRID_X=260;GRID_Y=160;ROW_PITCH=140;TIER_PITCH=240;SLOT_X=60
CARD_W=183;CARD_H=84;CONTENT_W=1260;CONTENT_H=1120


def block(key,text):return key+' = {\n'+'\n'.join('\t'+line if line.strip() else '' for line in text.splitlines())+'\n}\n'
def text(name,value,x,y,width,height,font='ACBriefing16'):
    return block('instantTextBoxType',f'name = "{name}"\nposition = {{ x = {x} y = {y} }}\nfont = "{font}"\ntext = "{value}"\nmaxWidth = {width}\nmaxHeight = {height}\nformat = left')


def folder():
    body='name = "ac_air_folder"\nposition = { x = 0 y = 47 }\nsize = { width = 100%% height = 100%% }\n'
    body+='margin = { top = 13 left = 13 bottom = 24 right = 25 }\ndrag_scroll = { left middle }\nverticalScrollbar = "ac_exp_right_vertical_slider"\nhorizontalScrollbar = "ac_exp_bottom_horizontal_slider"\nscroll_wheel_factor = 40\n'
    content=f'name = "ac_air_scroll_content"\nposition = {{ x = 0 y = 0 }}\nsize = {{ width = {CONTENT_W} height = {CONTENT_H} min = {{ width = 100%% height = 100%% }} }}\nclipping = no\n'
    content+=block('background','name = "Background"\nquadTextureSprite = "GFX_ac_air_sheet"')
    content+=text('ac_air_heading','ac_air_page_heading',24,20,1120,32,'ACBriefing20')
    content+=text('ac_air_scope','ac_air_page_scope',24,54,1150,36)
    for index,year in enumerate(YEARS):content+=text('ac_air_year_'+str(year),str(year),GRID_X+index*TIER_PITCH,102,CARD_W,24,'ACBriefing20')
    for index,family in enumerate(FAMILIES):content+=text('ac_air_label_'+family.id,'ac_air_label_'+family.id,24,GRID_Y+index*ROW_PITCH+22,204,40)
    body+=block('containerWindowType',content)
    for index,family in enumerate(FAMILIES):
        body+=block('gridBoxType',f'name = "ac_air_{family.id}_2006_tree"\nposition = {{ x = {GRID_X} y = {GRID_Y+index*ROW_PITCH} }}\nslotsize = {{ width = {SLOT_X} height = 70 }}\nformat = "LEFT"')
    return block('containerWindowType',body)


def tab():
    return block('buttonType',f'name = "ac_air_folder_tab"\nposition = {{ x = {TAB_X} y = 0 }}\nquadTextureSprite = "GFX_ac_air_folder_tab"\nframe = 1\ntext = "ac_air_tab_short"\nbuttonFont = "ACBriefing16"\nclicksound = ui_research_tab_air')


def extend(source):
    if re.search(r'name\s*=\s*"ac_air_(?:folder|folder_tab)"',source):raise ValueError('AIR extension applied twice')
    marker=re.search(r'(?m)^\s*containerWindowType\s*=\s*\{\s*\n\s*name\s*=\s*"folder_tabs"',source)
    if not marker:raise ValueError('Required research folder_tabs missing')
    result=source[:marker.start()]+'\n'+folder()+'\n'+source[marker.start():]
    marker=re.search(r'(?m)^\s*buttonType\s*=\s*\{\s*\n\s*name\s*=\s*"infantry_folder_tab"',result)
    if not marker:raise ValueError('Required native infantry tab missing')
    return result[:marker.start()]+'\n'+tab()+'\n'+result[marker.start():]


def strip(tree):
    result=copy.deepcopy(tree)
    def clean(nodes):
        kept=[]
        for key,op,value in nodes:
            if isinstance(value,list):
                name=get(value,'name','')
                if isinstance(name,str) and name.strip('"') in NAMES:continue
                clean(value)
            kept.append([key,op,value])
        nodes[:]=kept
    clean(result);return result


def item(small=False):
    name='techtree_ac_air_folder_'+('small_item' if small else 'item')
    body=f'name = "{name}"\nposition = {{ x = 0 y = 0 }}\nsize = {{ width = {CARD_W} height = {CARD_H} }}\nclipping = no\n'
    body+=block('background','name = "Background"\nquadTextureSprite = "GFX_technology_unavailable_item_bg"')
    body+=text('Name','',4,2,175,36)
    body+=block('iconType','name = "Icon"\nposition = { x = 91 y = 59 }\nspriteType = "GFX_technology_medium"\ncenterposition = yes\nalwaystransparent = yes')
    body+=block('iconType','name = "bonus_icon"\nposition = { x = 0 y = -22 }\nspriteType = "GFX_tech_bonus"')+text('bonus','',18,-22,80,20)
    body+=block('iconType','name = "can_assign_design_team_icon"\nposition = { x = 156 y = 62 }\nspriteType = "GFX_ac_ui_design_team_icon"\nscale = 0.5')
    body+=block('gridBoxType','name = "special_project_specialization_list"\nposition = { x = -20000 y = -20000 }')
    return block('containerWindowType',body)


def templates():return block('guiTypes',item()+item(True))


def blueprints():
    result=''
    for family in AIRCRAFT:
        if not family.airframe_parent:continue
        for year in YEARS:
            ident=frame_id(family.id,year)
            body=f'name = "equipment_designer_{ident}"\nposition = {{ x = 0 y = 0 }}\nsize = {{ width = 508 height = 248 }}\n'
            body+=block('iconType',f'name = "equipment_image_overlay"\nspriteType = "GFX_TC_{ident}"\nposition = {{ x = 0 y = 0 }}')
            result+=block('containerWindowType',body)
    return block('guiTypes',result)
