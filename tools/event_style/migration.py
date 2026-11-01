"""Exactly 25 path-specific scalar substitutions, independently reversible.

The historical Event-Fit capture remains authoritative. Both lexical restoration
(including every original byte except CRLF) and ordered-AST restoration must pass.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from usea_expansion.script import parse,get

def row(path,key,old,new):return (tuple(path.split('/')),key,old,new)
P='EventWindow_Operative';L='EventWindow_leader'
SPRITES=[
 row('EventWindow/bottom_Window/event_picture','spriteType','GFX_report_event_001','GFX_ac_event_country_default'),
 row(P+'/Background','spriteType','GFX_event_operative_background','GFX_ac_event_operative_background'),
 row(P+'/top_Window/agency_insignia','quadTextureSprite','GFX_intelligence_agency_logo_prc','GFX_ac_event_agency_office'),
 row(P+'/top_Window/btn_minimize','spriteType','GFX_event_button_minimize','GFX_ac_event_minimize'),
 row(P+'/midsection/leader_picture_container/leader','spriteType','GFX_leader_unknown','GFX_ac_event_office'),
 row(P+'/midsection/leader_picture_container/paper_clip_2','spriteType','GFX_paper_clip_event','GFX_ac_event_clip'),
 row(P+'/bottom_Window/Background','spriteType','GFX_tiled_window_transparent','GFX_ac_event_transparent'),
 row(P+'/bottom_window_end/Background','spriteType','GFX_tiled_window_transparent','GFX_ac_event_transparent'),
 row(L+'/Background','spriteType','GFX_tiled_window_transparent','GFX_ac_event_transparent'),
 row(L+'/top_Window/Background','spriteType','GFX_event_report_top_win','GFX_ac_event_top'),
 row(L+'/top_Window/btn_minimize','spriteType','GFX_event_button_minimize','GFX_ac_event_minimize'),
 row(L+'/midsection/Background','quadTextureSprite','GFX_event_report_tileable_midsection','GFX_ac_event_mid'),
 row(L+'/midsection/leader_picture_container/leader','spriteType','GFX_leader_unknown','GFX_ac_event_office'),
 row(L+'/midsection/leader_picture_container/leader_frame','spriteType','GFX_event_leader_frame','GFX_ac_event_leader_frame'),
 row(L+'/bottom_Window/Background','spriteType','GFX_event_report_tileable_bottom_section','GFX_ac_event_bottom'),
 row(L+'/bottom_window_end/Background','spriteType','GFX_event_report_bottom_win_end','GFX_ac_event_end'),
 row('EventWindow_News/top_Window/event_picture','spriteType','GFX_news_event_001','GFX_ac_event_news_default')]
FONTS=[row(path,'font',old,new) for path,old,new in [
 (P+'/top_Window/Title','hoi4_typewriter22','ACEvent20'),
 (P+'/midsection/leader_details_container/leader_fullname','hoi4_typewriter16','ACEvent16'),
 (P+'/midsection/leader_details_container/leader_codename','hoi4_typewriter16','ACEvent16'),
 (P+'/midsection/Description','hoi4_typewriter16','ACEvent16'),
 (L+'/top_Window/Title','hoi4_typewriter22','ACEvent20'),
 (L+'/midsection/Description','hoi4_typewriter16','ACEvent16')]]
INSETS=[row(path+'/midsection/Description/borderSize','x','0','1') for path in ('EventWindow','EventWindow_News')]
REVIEWED=SPRITES+FONTS+INSETS
def literal(key,value):return value if key=='x' else '"'+value+'"'
def normalized(text):return text.replace('\r\n','\n')
def sha(text):return hashlib.sha256(normalized(text).encode()).hexdigest()
def source():
    text=(HERE/'SOURCE_eventwindow.gui').read_text(encoding='utf-8-sig')
    contract=json.loads((ROOT/'tools/event_picture_fit/contract.json').read_text())
    if sha(text)!=contract['protected_gui_sha256']:raise ValueError('Original event GUI capture differs from immutable fit contract')
    return text

def spans(text):
    """Independent lexical block reader: names form paths; only scalar spans edit."""
    tokens=[m for m in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|>=|<=|!=|[{}=<>]|[^\s{}=<>]+',text) if not m[0].startswith('#')]
    pos=0
    def block(nested=False):
        nonlocal pos
        out=[]
        while pos<len(tokens):
            key=tokens[pos];pos+=1
            if key[0]=='}':
                if not nested:raise ValueError('Unexpected GUI brace')
                return out
            if pos>=len(tokens) or tokens[pos][0] not in ('=','<','>','<=','>=','!='):out.append((key[0],None,None));continue
            pos+=1
            if pos>=len(tokens):raise ValueError('Missing GUI value')
            value=tokens[pos];pos+=1
            out.append((key[0],block(True) if value[0]=='{' else value,value))
        if nested:raise ValueError('Unclosed GUI block')
        return out
    result={}
    def visit(rows,path=()):
        names=[v[0].strip('"') for k,v,_ in rows if k=='name' and not isinstance(v,list)]
        if len(names)>1:raise ValueError('Duplicate GUI name')
        path=path+tuple(names)
        for key,value,_ in rows:
            if isinstance(value,list):visit(value,path+(('borderSize',) if key=='borderSize' else ()))
            elif value is not None and (key in ('spriteType','quadTextureSprite','font') or key=='x' and path[-1:] == ('borderSize',)):
                address=(path,key)
                if address in result:raise ValueError('Duplicate GUI field '+str(address))
                result[address]=value
    visit(block());return result

def replace(text,reverse=False):
    fields=spans(text);edits=[]
    for path,key,old,new in REVIEWED:
        expected,replacement=(new,old) if reverse else (old,new)
        token=fields.get((path,key))
        if token is None or token[0]!=literal(key,expected):raise ValueError('Missing/reverted/unregistered event field '+str((path,key)))
        edits.append((token.start(),token.end(),literal(key,replacement)))
    for start,end,value in sorted(edits,reverse=True):text=text[:start]+value+text[end:]
    return text

def restore_ast(tree):
    """A different traversal from lexical migration; retain all ordered nodes."""
    result=copy.deepcopy(tree);expected={(p,k):(old,new) for p,k,old,new in REVIEWED};seen=set()
    def visit(rows,path=()):
        names=[v.strip('"') for k,_,v in rows if k=='name' and isinstance(v,str)]
        if len(names)>1:raise ValueError('Duplicate control name')
        path+=tuple(names)
        for node in rows:
            key,_,value=node
            if isinstance(value,list):visit(value,path+(('borderSize',) if key=='borderSize' else ()))
            elif (path,key) in expected:
                address=(path,key);old,new=expected[address]
                if address in seen or value!=literal(key,new):raise ValueError('Reviewed event field reverted/duplicated '+str(address))
                node[2]=literal(key,old);seen.add(address)
    visit(result)
    if seen!=set(expected):raise ValueError('Missing reviewed event fields')
    return result

def assert_preserved(text):
    original=source();restored=replace(text,True)
    if sha(restored)!=sha(original):raise ValueError('Unregistered event GUI text/layout change')
    restored_ast=restore_ast(parse(text))
    if restored_ast!=parse(original):raise ValueError('Unregistered event GUI ordered AST change')
    return restored

def generated_from(original):
    """Compose the actual upstream producer only at the immutable base contract."""
    if normalized(original)!=normalized(source()):
        raise ValueError('Upstream event GUI differs from the immutable fit contract')
    output=replace(original);assert_preserved(output);return normalized(output)

def generated():
    return generated_from(source())

def report(text):
    restored=assert_preserved(text)
    ast_sha=lambda obj:hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()
    return dict(original_sha256=sha(source()),current_sha256=sha(text),restored_sha256=sha(restored),
        original_ast_sha256=ast_sha(parse(source())),restored_ast_sha256=ast_sha(restore_ast(parse(text))),
        substitutions=[dict(path=list(p),field=k,old=old,new=new) for p,k,old,new in REVIEWED],
        sprite_fields=len(SPRITES),font_fields=len(FONTS),inset_fields=len(INSETS),
        scope='Only17 sprites,6 fonts and2 provisional horizontal text insets; original capture restored exactly; no other control/geometry/action/condition/identity change')
