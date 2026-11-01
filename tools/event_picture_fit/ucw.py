"""Original news-only UCW compositions; inherited country photos stay unchanged."""
import hashlib,importlib.util,io,json,re
from pathlib import Path
from PIL import Image,ImageDraw
from event_picture_fit.fit import ROOT,MOD,NAVY,contain

HERE=Path(__file__).resolve().parent
LIBRARY=ROOT/'tools/usea_expansion/build_art.py'
spec=importlib.util.spec_from_file_location('ucw_original_news_symbols',LIBRARY)
symbols=importlib.util.module_from_spec(spec);spec.loader.exec_module(symbols)

# Every listed actual news scene has a reviewed outcome-neutral subject.
FAMILIES={
 'dispatch':('GFX_report_event_bad_news_2','document','communications','Changed circumstances and public reporting'),
 'accord':('GFX_report_event_treaty_2','peace','scales','An accord or negotiated armistice'),
 'operations':('GFX_report_event_blk_army_attack','radar','logistics','An operational dispatch, without an illustrated winner'),
 'institution':('GFX_report_event_treaty_1','assembly','document','Institutional communique and public oversight'),
 'liaison':('GFX_report_event_ose_war_committee','command','communications','Command liaison and headquarters coordination'),
 'assessment':('GFX_report_event_flag_osea_1','air','scales','An allied campaign assessment, without a national flag'),
}
SCENES={12:('dispatch','Erusea closes its border'),25:('accord','A continental accord'),
20:('operations','Erusea invades San Salvacion'),40:('operations','Stonehenge is seized'),
31:('institution','ISAF is founded'),41:('operations','Fall back to Los Canas'),
42:('liaison','ISAF headquarters moves to North Point'),43:('operations','Land on the Usean continent'),
44:('operations','Stonehenge is destroyed'),70:('operations','Mount Shezna radar'),
71:('operations','Comberth Harbor'),72:('operations','Comona Islands'),73:('operations','Istas Fortress'),
74:('operations','Stonehenge engineers escape'),75:('operations','Ice Creek landing'),
76:('operations','San Salvacion'),77:('operations','Whiskey Corridor'),
50:('assessment','Farbanti falls'),51:('dispatch','Erusea wins the Continental War'),
52:('accord','An armistice in Usea'),62:('institution','Erusea provisional government')}

def news_picture(number,old_picture):
    family,_=SCENES[number]
    if old_picture!=FAMILIES[family][0]:raise ValueError('Unreviewed UCW news-picture mapping: '+str(number))
    return 'GFX_ac_ucw_news_'+family

def encoded(image,kind):
    stream=io.BytesIO();image.save(stream,format=kind);return stream.getvalue()

def outputs():
    out={};assets=[];sprites=[]
    localization=MOD/'localisation/english/ac_ucw_l_english.yml'
    titles={m[1]:json.loads(m[2]) for m in re.finditer(r'^ ([^ :]+):0 (".*")$',localization.read_text(encoding='utf-8-sig'),re.M)}
    for index,(family,(old,primary,secondary,subject)) in enumerate(FAMILIES.items()):
        master=Image.new('RGBA',(794,306),NAVY);d=ImageDraw.Draw(master)
        cyan=(93,208,223,255);light=(218,237,242,255);grid=(21,45,60,255)
        d.rounded_rectangle((9,9,784,296),radius=11,outline=cyan,width=4)
        for x in range(33,780,32):d.line((x,24,x,281),fill=grid,width=1)
        for y in range(34,290,32):d.line((23,y,771,y),fill=grid,width=1)
        # Original subject geometry and asymmetric accents, without flags/text.
        left=(57+index*3,47,207,202);right=(509-index*3,61,180,173)
        symbols.glyph(master,primary,left,light);symbols.glyph(master,secondary,right,cyan)
        d.line((302,151,451,151),fill=cyan,width=4)
        d.rectangle((341,117,405,185),outline=grid,width=3)
        for step in range(index+1):d.line((305+step*22,256,317+step*22,256),fill=cyan,width=3)
        source=HERE/'source/ucw'/f'{family}.png';out[source]=encoded(master,'PNG')
        image=contain(master,'news_event');relative=f'gfx/AC_ucw/news/{family}.dds';payload=encoded(image,'DDS')
        out[MOD/relative]=payload;sprite='GFX_ac_ucw_news_'+family
        sprites.append(f'spriteType = {{ name = "{sprite}" texturefile = "{relative}" }}')
        assets.append(dict(file=relative,sprite=sprite,width=397,height=153,frames=1,frame_width=397,frame_height=153,
            alpha_min=255,alpha_max=255,sha256=hashlib.sha256(payload).hexdigest(),source=source.relative_to(ROOT).as_posix(),
            source_sha256=hashlib.sha256(out[source]).hexdigest(),source_layer='original procedural Ulysses briefing composition',
            subject=subject,motifs=[primary,secondary],transform='Full-source Lanczos contain; no crop, caption, national flag or historical incident added'))
    out[MOD/'interface/ac_ucw_news.gfx']=('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n').encode()
    manifest=dict(schema=1,source_layer='New original news compositions, separate from inherited country photographs',
        primary_consumer='eventwindow.gui/news_event_window/event_picture; native397x153 at59,91',
        assets=assets,consumers=[dict(id='ac_ucw.'+str(number),title=titles['ac_ucw.'+str(number)+'.t'],subject=family,
            old_country_picture=FAMILIES[family][0],news_picture='GFX_ac_ucw_news_'+family) for number,(family,title) in SCENES.items()],
        source_files={'tools/event_picture_fit/ucw.py':hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                      'tools/usea_expansion/build_art.py':hashlib.sha256(LIBRARY.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                      'tools/event_picture_fit/fit.py':hashlib.sha256((HERE/'fit.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                      localization.relative_to(ROOT).as_posix():hashlib.sha256(localization.read_bytes().replace(b'\r\n',b'\n')).hexdigest()},
        native='Source and offline consumer bounds only; no native acceptance')
    out[HERE/'ucw_assets.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    return out
