"""Portable review labels using the already shipped ACBriefing bitmap glyphs."""
from pathlib import Path
import sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from event_picture_fit.bitmap import BitmapFont


class GalleryFont:
    def __init__(self):self.font=BitmapFont()

    def draw(self,image,text,xy,width,size=16,color=(218,237,242,255)):
        padding=8;advance=max(1,self.font.width(text))
        tile=Image.new('RGBA',(advance+2*padding,self.font.height+2*padding))
        self.font.draw(tile,text,(padding,padding),advance+1)
        alpha=tile.getchannel('A')
        if color[3]!=255:alpha=alpha.point([value*color[3]//255 for value in range(256)])
        ink=Image.new('RGBA',tile.size,color);ink.putalpha(alpha)
        scale=min(size/16,width/ink.width)
        if scale!=1:ink=ink.resize((max(1,round(ink.width*scale)),max(1,round(ink.height*scale))),Image.Resampling.LANCZOS)
        offset=round(padding*scale);image.alpha_composite(ink,(xy[0]-offset,xy[1]-offset))
