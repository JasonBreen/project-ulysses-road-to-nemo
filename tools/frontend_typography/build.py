"""Build the map-name bitmap font from the bundled OFL DINish source.

Pillow is needed for rebuilding only. Installed-game and Workshop assets are not
inputs. The renderer requests hoi_mapfont4 directly, independently of UI fonts.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
MOD = HERE.parents[1] / 'mod/2985041246'
FONT = HERE / 'source/DINish-Regular.ttf'
SOURCE_SHA = 'ad45d1b0d9da9597b82e587aa54590c3f571b4254ce0ef1db6daf318cc9cc278'


def build():
    assert hashlib.sha256(FONT.read_bytes()).hexdigest() == SOURCE_SHA
    font = ImageFont.truetype(str(FONT), 84)
    # Keep English accents and extended Latin/Cyrillic/Greek where provided by
    # the source font. Do not pack repeated .notdef boxes as real characters.
    missing = bytes(font.getmask(chr(0x10ffff)))
    candidates = sorted(set(range(32,592)) | set(range(0x370,0x530)) |
                        set(range(0x2000,0x2070)) | {0x20ac,0xfffd})
    chars = [cp for cp in candidates if bytes(font.getmask(chr(cp))) != missing]
    width = 2048
    x = y = row_height = 0
    entries = []
    for cp in chars:
        left,top,right,bottom = font.getbbox(chr(cp),anchor='ls')
        gw,gh = max(1,right-left)+4,max(1,bottom-top)+4
        if x+gw > width:x,y,row_height = 0,y+row_height,0
        entries.append((cp,x,y,gw,gh,left,top,round(font.getlength(chr(cp))+1)))
        x += gw+2
        row_height = max(row_height,gh+2)
    height = 1 << (y+row_height-1).bit_length()
    # Solid white RGB plus glyph coverage alpha: no hollow letters or thick
    # black outline, and no dark RGB fringes when the engine filters the atlas.
    atlas = Image.new('RGBA',(width,height),(255,255,255,0))
    d = ImageDraw.Draw(atlas)
    lines = ['info face="AC Map Briefing" size=84 bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=2,2,2,2 spacing=1,1 outline=0',
             f'common lineHeight=84 base=70 scaleW={width} scaleH={height} pages=1 packed=0 alphaChnl=0 redChnl=4 greenChnl=4 blueChnl=4',
             'page id=0 file="hoi_mapfont4.dds"',f'chars count={len(entries)}']
    for cp,x,y,gw,gh,left,top,advance in entries:
        d.text((x+2-left,y+2-top),chr(cp),font=font,fill=(255,255,255,255),anchor='ls')
        lines.append(f'char id={cp} x={x} y={y} width={gw} height={gh} xoffset={left-2} yoffset={70+top-2} xadvance={advance} page=0 chnl=15')
    out = MOD/'gfx/fonts'
    atlas.save(out/'hoi_mapfont4.dds')
    (out/'hoi_mapfont4.fnt').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    for name in ['OFL.txt','FONTLOG.txt']:
        shutil.copyfile(HERE/'source'/name,out/('AC_MAP_'+name))
    meta = dict(family='AC Map Briefing',source_family='DINish Regular',
                source_commit='56416a590a5b4ef7f121d1c20cbbd173ebbfab51',source_sha256=SOURCE_SHA,
                width=width,height=height,glyphs=len(entries),codepoints=chars,
                files={name:hashlib.sha256((out/name).read_bytes()).hexdigest()
                       for name in ['hoi_mapfont4.fnt','hoi_mapfont4.dds','AC_MAP_OFL.txt','AC_MAP_FONTLOG.txt']})
    (HERE/'font.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(f'Built {len(entries)} glyphs in a {width}x{height} BGRA atlas.')


if __name__=='__main__':build()
