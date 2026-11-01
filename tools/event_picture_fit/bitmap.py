"""Existing shipped bitmap glyph pixels/metrics, isolated from art generators."""
import re
from PIL import Image
from event_picture_fit.fit import MOD

class BitmapFont:
    def __init__(self):
        self.atlas=Image.open(MOD/'gfx/fonts/ACBriefing16.dds').convert('RGBA')
        raw=(MOD/'gfx/fonts/ACBriefing16.fnt').read_text();self.glyphs={}
        for line in raw.splitlines():
            if not line.startswith('char id='):continue
            row={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)};self.glyphs[row['id']]=row
        self.height=int(re.search(r'common lineHeight=(\d+)',raw)[1])
    def width(self,text):return sum(self.glyphs.get(ord(c),self.glyphs[63])['xadvance'] for c in text)
    def draw(self,image,text,xy,width):
        lines=[];line=''
        for word in text.split():
            candidate=(line+' '+word).strip()
            if line and self.width(candidate)>width:lines.append(line);line=word
            else:line=candidate
        if line:lines.append(line)
        for n,line in enumerate(lines):
            x=xy[0]
            for c in line:
                g=self.glyphs.get(ord(c),self.glyphs[63]);sprite=self.atlas.crop((g['x'],g['y'],g['x']+g['width'],g['y']+g['height']))
                image.alpha_composite(sprite,(x+g['xoffset'],xy[1]+n*self.height+g['yoffset']));x+=g['xadvance']
        return len(lines)*self.height
