"""Restore only24 reviewed picture bindings before whole-AST comparison."""
import copy,hashlib,json
from pathlib import Path
from event_picture_fit.fit import ROOT,MOD
from event_picture_fit.ucw import SCENES,FAMILIES
from usea_expansion.script import parse,get

HERE=Path(__file__).resolve().parent
def digest(path):
    raw=path.read_bytes()
    if path.suffix in ('.py','.txt','.gui','.gfx','.json','.md'):raw=raw.replace(b'\r\n',b'\n')
    return hashlib.sha256(raw).hexdigest()
def reviewed(relative):
    if relative=='events/ac_anea.txt':
        return {'ac_anea.'+str(n):('GFX_ac_anea_event_emm_4','GFX_ac_anea_news_emm_4') for n in (10,11,12)}
    if relative=='events/ac_ucw.txt':
        return {'ac_ucw.'+str(n):(FAMILIES[f][0],'GFX_ac_ucw_news_'+f) for n,(f,_) in SCENES.items()}
    raise ValueError('No reviewed picture exception for '+relative)

def restore(relative,nodes):
    result=copy.deepcopy(nodes);allowed=reviewed(relative);seen=set()
    for kind,_,body in result:
        if kind not in ('country_event','news_event'):continue
        ident=get(body,'id')
        if ident not in allowed:continue
        old,new=allowed[ident]
        if kind!='news_event' or ident in seen or get(body,'picture')!=new:
            raise ValueError('Reviewed news picture contract differs: '+str(ident))
        picture=[row for row in body if row[0]=='picture']
        if len(picture)!=1:raise ValueError('Missing/duplicate reviewed picture control')
        picture[0][2]=old;seen.add(ident)
    if seen!=set(allowed):raise ValueError('Missing reviewed news event: '+str(set(allowed)-seen))
    return result

def assert_picture_only(relative,nodes):
    contract=json.loads((HERE/'contract.json').read_text())
    original=parse(contract['original_event_sources'][relative])
    if restore(relative,nodes)!=original:
        raise ValueError('Non-picture event AST changed: '+relative)

def preserved():
    c=json.loads((HERE/'contract.json').read_text())
    for name,expected in c['protected_sources'].items():
        if digest(ROOT/name)!=expected:raise ValueError('Protected original changed: '+name)
    if digest(MOD/'interface/eventwindow.gui')!=c['protected_gui_sha256']:raise ValueError('Event GUI changed')
    for name,expected in c['original_anea_focus_sha256'].items():
        if digest(MOD/name)!=expected:raise ValueError('Original Anea focus DDS changed: '+name)
    for name,row in c['military_captures'].items():
        if digest(ROOT/name)!=row['sha256']:raise ValueError('Original military capture changed: '+name)
    for name in c['original_event_sources']:
        assert_picture_only(name,parse((MOD/name).read_text(encoding='utf-8-sig')))
    return c

def report():
    c=preserved();files={}
    for relative,text in c['original_event_sources'].items():
        original=parse(text);current=parse((MOD/relative).read_text(encoding='utf-8-sig'));restored=restore(relative,current)
        ast_hash=lambda value:hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
        files[relative]=dict(old_normalized_sha256=hashlib.sha256(text.replace('\r\n','\n').encode()).hexdigest(),
            new_normalized_sha256=digest(MOD/relative),original_ast_sha256=ast_hash(original),
            restored_ast_sha256=ast_hash(restored),whole_ast_preserved=original==restored,
            reviewed_bindings={key:dict(old=old,new=new) for key,(old,new) in reviewed(relative).items()})
    return dict(schema=1,scope='Only enumerated news-picture assignments may change; gameplay/options/text/IDs and original captures remain preserved',
        files=files,protected_original_files=len(c['protected_sources']),unchanged_anea_focus_DDS=len(c['original_anea_focus_sha256']),
        original_military_captures=c['military_captures'],native='No native or save-serialization acceptance')
