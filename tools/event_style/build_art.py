"""Original geometric event chrome; Pillow 11.3.0, no imported engine pixels."""
import argparse,hashlib,io,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,__version__
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
sys.path.insert(0,str(ROOT/'tools'))
from event_style.migration import SPRITES
NAVY='#081621';PANEL='#102936';CYAN='#63ccdf';DIM='#2c6476';LIGHT='#daedf2'

class Canvas:
    def __init__(self,w,h,transparent=False):
        self.image=Image.new('RGBA',(w,h),(0,0,0,0) if transparent else NAVY);self.draw=ImageDraw.Draw(self.image)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
        if not transparent:self.svg.append(f'<rect width="{w}" height="{h}" fill="{NAVY}"/>')
    def rect(self,box,fill=None,outline=None,width=1):
        self.draw.rectangle(box,fill=fill,outline=outline,width=width);x,y,r,b=box
        self.svg.append(f'<rect x="{x}" y="{y}" width="{r-x}" height="{b-y}" fill="{fill or "none"}" stroke="{outline or "none"}" stroke-width="{width}"/>')
    def line(self,points,fill=CYAN,width=1):
        self.draw.line(points,fill=fill,width=width);points=' '.join(f'{x},{y}' for x,y in points)
        self.svg.append(f'<polyline points="{points}" fill="none" stroke="{fill}" stroke-width="{width}"/>')
    def ellipse(self,box,outline=CYAN,width=1):
        self.draw.ellipse(box,outline=outline,width=width);x,y,r,b=box
        self.svg.append(f'<ellipse cx="{(x+r)/2}" cy="{(y+b)/2}" rx="{(r-x)/2}" ry="{(b-y)/2}" fill="none" stroke="{outline}" stroke-width="{width}"/>')
    def data(self):return ('\n'.join(self.svg+['</svg>'])+'\n').encode()

SIZES={'country_default':(210,176),'news_default':(397,153),'top':(581,121),'tile':(580,66),
       'end':(581,59),'minimize':(32,33),'clip':(53,29),'leader_frame':(172,232),'office':(156,210),
       'agency_office':(234,119),'transparent':(95,95),'operative_background':(12672,596)}
ALIASES={new.removeprefix('GFX_ac_event_'):new for _,_,_,new in SPRITES}
ALIASES['mid']='GFX_ac_event_mid';ALIASES['bottom']='GFX_ac_event_bottom'

def compose(name):
    w,h=SIZES[name];c=Canvas(w,h,name in ('minimize','clip','leader_frame','agency_office','transparent'))
    if name=='transparent':return c
    if name=='leader_frame':
        # Actual scaled portrait occupies source-frame x9.411..165.411, y10.588..220.588.
        # Decorative ink stays outside its conservative integer enclosure.
        c.rect((1,1,170,230),outline=DIM,width=2)
        for x,y,sx,sy in [(4,4,1,1),(168,4,-1,1),(4,228,1,-1),(168,228,-1,-1)]:
            c.line([(x+sx*14,y),(x,y),(x,y+sy*5)],width=2)
        return c
    if name=='minimize':
        c.rect((2,2,29,30),fill=PANEL,outline=DIM);c.line([(8,19),(23,19)],width=2);return c
    if name=='clip':
        c.line([(8,25),(8,7),(43,7),(43,21),(14,21),(14,12),(36,12)],width=2);return c
    if name=='agency_office':
        for f in range(2):
            x=f*117;c.rect((x+7,10,x+109,108),fill=PANEL,outline=CYAN if f else DIM,width=2)
            c.line([(x+26,40),(x+58,22),(x+91,40),(x+26,40)],width=2)
            for dx in (34,57,80):c.rect((x+dx,46,x+dx+6,82),outline=CYAN)
            c.line([(x+24,89),(x+94,89)],width=2)
            c.line([(x+24,97),(x+94,97)],fill=DIM)
        return c
    if name=='office':
        c.rect((8,9,147,200),fill=PANEL,outline=DIM)
        c.line([(25,64),(78,34),(131,64),(25,64)],width=2)
        for x in (39,71,103):c.rect((x,73,x+12,131),outline=CYAN,width=2)
        c.line([(25,141),(131,141)],width=2)
        c.rect((33,157,122,184),outline=DIM)
        for y in (165,173):c.line([(43,y),(111,y)],fill=DIM)
        return c
    if name=='operative_background':
        for f in range(24):
            x=f*528;c.rect((x+1,1,x+526,594),fill=NAVY,outline=DIM)
            c.line([(x+12,13),(x+174,13),(x+188,27),(x+512,27)],fill=CYAN)
            c.line([(x+12,254),(x+512,254)],fill=DIM)
            c.line([(x+12,572),(x+512,572)],fill=CYAN)
            # All states preserve readable opaque body; restrained progress accents.
            c.rect((x+16,18,x+16+(f+1)*6,20),fill=CYAN)
            for q in range(4):c.line([(x+16+q*12,580),(x+22+q*12,580)],fill=CYAN if q<=f//6 else DIM)
        return c
    if name in ('country_default','news_default'):
        c.rect((5,5,w-6,h-6),fill=PANEL,outline=DIM)
        if name=='country_default':
            c.rect((31,22,131,143),outline=CYAN,width=2)
            c.line([(45,41),(113,41)],width=2)
            for y,l in [(59,63),(72,75),(85,55),(98,70),(111,45)]:c.line([(45,y),(45+l,y)],fill=DIM)
            c.ellipse((126,102,172,148));c.line([(136,126),(146,136),(163,115)],width=2)
        else:
            for x,y in [(46,49),(111,104),(191,38),(259,91),(348,48)]:
                c.ellipse((x-5,y-5,x+5,y+5));c.line([(x,y),(191,76)],fill=DIM)
            c.rect((155,54,226,98),fill=NAVY,outline=CYAN,width=2)
            for y in (65,76,87):c.line([(166,y),(214,y)],fill=DIM)
        return c
    c.rect((0,0,w-1,h-1),fill=NAVY,outline=DIM)
    if name=='top':
        c.line([(10,12),(146,12),(158,24),(w-12,24)],width=2)
        c.line([(12,107),(w-12,107)],fill=DIM)
        for x in (17,29,41):c.rect((x,33,x+5,36),fill=CYAN)
    elif name=='tile':
        # Only side-edge ink: repeated vertical native tiles have no horizontal seams.
        c.line([(1,0),(1,h-1)],fill=DIM);c.line([(w-2,0),(w-2,h-1)],fill=DIM)
    elif name=='end':c.line([(12,40),(w-12,40)],fill=CYAN)
    return c

def binding(name,key):
    texture='tile' if key in ('mid','bottom') else key
    typ='corneredTileSpriteType' if key in ('mid','bottom','transparent') else 'frameAnimatedSpriteType' if key=='operative_background' else 'spriteType'
    fields=[f'name = "{name}"',f'texturefile = "gfx/AC_event_style/{texture}.dds"']
    if key in ('mid','bottom'):fields+=['size = { x = 580 y = 66 }','borderSize = { x = 290 y = 16 }','alwaystransparent = yes']
    elif key=='transparent':fields+=['size = { x = 3 y = 3 }','borderSize = { x = 1 y = 1 }','tilingCenter = no','effectFile = "gfx/FX/buttonstate_nodowneffect.lua"']
    elif key=='operative_background':fields+=['noOfFrames = 24','animation_rate_fps = 80','looping = no','play_on_show = no','pause_on_loop = 0.0']
    elif key=='agency_office':fields+=['noOfFrames = 2']
    elif key=='office':fields+=['legacy_lazy_load = no','generate_mip_maps = yes']
    elif key in ('top','end'):fields+=['alwaystransparent = yes']
    return '  '+typ+' = { '+' '.join(fields)+' }'

def sha(data):return hashlib.sha256(data).hexdigest()
def outputs():
    if __version__!='11.3.0':raise ValueError('Packaging requires pinned Pillow 11.3.0')
    files={};assets=[]
    for key,size in SIZES.items():
        canvas=compose(key);dds=io.BytesIO();canvas.image.save(dds,format='DDS');raw=dds.getvalue();svg=canvas.data()
        runtime='mod/2985041246/gfx/AC_event_style/'+key+'.dds';source='tools/event_style/source/'+key+'.svg'
        files[runtime]=raw;files[source]=svg
        alpha=canvas.image.getchannel('A');frames=24 if key=='operative_background' else 2 if key=='agency_office' else 1
        bindings=[name for role,name in ALIASES.items() if ('tile' if role in ('mid','bottom') else role)==key]
        assets.append(dict(id=key,texture=runtime,source=source,dimensions=list(size),frames=frames,
            frame_size=[size[0]//frames,size[1]],sprites=bindings,sha256=sha(raw),source_sha256=sha(svg),
            alpha=dict(extrema=list(alpha.getextrema()),opaque_pixels=alpha.histogram()[255],transparent_pixels=alpha.histogram()[0]),
            provenance='Original authored geometric SVG/Pillow construction; no engine pixels or identity claims'))
    gfx='# Original scoped event defaults; inherited global identities remain unchanged.\nspriteTypes = {\n'
    gfx+='\n'.join(binding(name,key) for key,name in sorted(ALIASES.items()))+'\n}\n'
    for size in (16,20):gfx+=f'bitmapfont = {{ name = "ACEvent{size}" path = "gfx/fonts/ACBriefing{size}" color = 0xffdaedf2 textcolors = {{ G = {{ 86 172 91 }} R = {{ 220 84 84 }} Y = {{ 230 181 95 }} }} }}\n'
    files['mod/2985041246/interface/ac_event_style.gfx']=gfx.encode()
    sources={name:sha((HERE/name).read_bytes().replace(b'\r\n',b'\n')) for name in ('build_art.py','migration.py','SOURCE_eventwindow.gui')}
    font_files={str(p.relative_to(MOD)).replace('\\','/'):sha(p.read_bytes()) for size in (16,20) for p in (MOD/f'gfx/fonts/ACBriefing{size}.dds',MOD/f'gfx/fonts/ACBriefing{size}.fnt')}
    manifest=dict(schema=1,assets=assets,asset_count=12,sprite_count=13,source_hashes=sources,unchanged_font_bytes=font_files,
        dimensions_note='Agency normalized from primary 233x119/2 to234x119/2: nominal +0.5px per frame; native slicing unaccepted',
        native='No native rendering, animation, input or dynamic identity acceptance')
    files['tools/event_style/assets.json']=(json.dumps(manifest,indent=2)+'\n').encode();return files

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    for relative,data in outputs().items():
        target=ROOT/relative
        if a.check:
            if not target.is_file() or target.read_bytes()!=data:raise SystemExit('Generated event style differs: '+relative)
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    print('Original event style:12 textures/13 sprite aliases/2 font aliases; exact generated outputs PASS')
if __name__=='__main__':main()
