"""Build compact readable briefing text from the existing bundled OFL DINish."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246'
FONT=ROOT/'tools/frontend_typography/source/DINish-Regular.ttf'
def main():
    declarations=[];manifest=[]
    for pts in (16,20):
        name='ACBriefing'+str(pts);font=ImageFont.truetype(str(FONT),pts)
        missing=bytes(font.getmask(chr(0x10ffff)))
        chars=[cp for cp in list(range(32,592))+list(range(0x2000,0x2070))+[0x20ac] if bytes(font.getmask(chr(cp)))!=missing]
        width=512;x=y=rowheight=0;entries=[]
        for cp in chars:
            left,top,right,bottom=font.getbbox(chr(cp),anchor='ls');w,h=max(1,right-left)+4,max(1,bottom-top)+4
            if x+w>width:x,y,rowheight=0,y+rowheight,0
            entries.append((cp,x,y,w,h,left,top,round(font.getlength(chr(cp)))))
            x+=w+2;rowheight=max(rowheight,h+2)
        height=1<<(y+rowheight-1).bit_length();im=Image.new('RGBA',(width,height),(255,255,255,0));d=ImageDraw.Draw(im)
        lines=[f'info face="AC Briefing" size={pts} unicode=1 padding=2,2,2,2 spacing=1,1',f'common lineHeight={pts+2} base={pts} scaleW={width} scaleH={height} pages=1 packed=0',f'page id=0 file="{name}.dds"',f'chars count={len(entries)}']
        for cp,x,y,w,h,left,top,advance in entries:
            d.text((x+2-left,y+2-top),chr(cp),font=font,fill=(255,255,255,255),anchor='ls')
            lines.append(f'char id={cp} x={x} y={y} width={w} height={h} xoffset={left-2} yoffset={pts+top-2} xadvance={advance} page=0 chnl=15')
        im.save(MOD/'gfx/fonts'/f'{name}.dds');(MOD/'gfx/fonts'/f'{name}.fnt').write_text('\n'.join(lines)+'\n')
        declarations.append(f'bitmapfont = {{ name = "{name}" path = "gfx/fonts/{name}" color = 0xffdaedf2 textcolors = {{ G = {{ 86 172 91 }} R = {{ 220 84 84 }} Y = {{ 230 181 95 }} }} }}')
        manifest.append(dict(name=name,width=width,height=height,glyphs=len(chars),source_sha256=hashlib.sha256(FONT.read_bytes()).hexdigest()))
    (MOD/'interface/ac_expansion_fonts.gfx').write_text('bitmapfonts = {\n'+'\n'.join(declarations)+'\n}\n')
    (HERE/'fonts.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
