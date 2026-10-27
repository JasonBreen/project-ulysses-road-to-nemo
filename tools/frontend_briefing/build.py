"""Build original, reproducible briefing UI artwork. Requires Pillow.

No installed-game pixels, fonts or textures are inputs. Map silhouettes and the
existing bookmark statistics stay in the archive; this tool only authors chrome.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
OUT = MOD / 'gfx/interface/ac_briefing'
NAVY = (8, 22, 33, 255)
PANEL = (13, 32, 46, 255)
EDGE = (45, 85, 104, 255)
CYAN = (93, 208, 223, 255)
WHITE = (218, 237, 242, 255)
GOLD = (230, 181, 95, 255)
assets = []


def save(name, im, frames=1, directory='gfx/interface/ac_briefing'):
    OUT.mkdir(parents=True, exist_ok=True)
    target = MOD / directory / (name + '.dds')
    target.parent.mkdir(parents=True, exist_ok=True)
    im.save(target)  # Pillow RGBA -> legacy 32-bit BGRA DDS
    assets.append(dict(file=directory + '/' + name + '.dds',
                       width=im.width, height=im.height, frames=frames))


def panel(w, h):
    im = Image.new('RGBA', (w, h), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle((1, 1, w-2, h-2), outline=EDGE)
    d.line((2, 2, min(76, w-3), 2), fill=CYAN, width=2)
    d.line((w-76, h-3, w-3, h-3), fill=CYAN)
    return im


def box(d, rect, header=True):
    x, y, r, b = rect
    d.rectangle(rect, fill=PANEL, outline=EDGE)
    if header:
        d.rectangle((x+1, y+1, r-1, y+37), fill=(18, 44, 60, 255))
        d.line((x+1, y+38, r-1, y+38), fill=CYAN)


def glyph(im, kind, rect, color=CYAN):
    # Coordinates use a 100-unit drawing space, independent of output size.
    x,y,w,h=rect
    d=ImageDraw.Draw(im)
    def pts(p): return [(round(x+a*w/100),round(y+b*h/100)) for a,b in p]
    def line(p): d.line(pts(p), fill=color, width=max(1,round(w/24)), joint='curve')
    def poly(p): d.polygon(pts(p), fill=color)
    def ellipse(a,b,c,e): d.ellipse((x+a*w/100,y+b*h/100,x+c*w/100,y+e*h/100),outline=color,width=max(1,round(w/24)))
    if kind == 'personnel':
        ellipse(35,8,65,38);line([(18,88),(22,57),(38,48),(62,48),(78,57),(82,88)])
    elif kind == 'economy':
        line([(12,15),(12,85),(91,85)]);line([(22,29),(43,48),(61,40),(84,68)]);poly([(72,68),(88,72),(85,56)])
    elif kind == 'industry':
        line([(10,85),(10,42),(36,58),(36,42),(63,58),(63,26),(82,26),(82,85),(10,85)])
        for a in [25,47,69]:line([(a,68),(a,76)])
    elif kind == 'military':
        line([(18,82),(82,18)]);line([(18,18),(82,82)]);line([(13,65),(35,87)]);line([(65,87),(87,65)])
    elif kind == 'assembly':
        poly([(8,30),(50,9),(92,30)]);line([(10,88),(90,88)])
        for a in [24,50,76]:line([(a,39),(a,77)])
    elif kind == 'ballot':
        line([(16,45),(16,88),(84,88),(84,45),(16,45)]);line([(38,56),(62,56)])
        line([(30,23),(58,8),(76,38),(48,53),(30,23)]);line([(45,27),(54,31),(62,20)])
    elif kind == 'air':
        poly([(50,5),(57,42),(90,69),(90,77),(57,65),(57,86),(69,95),(31,95),(43,86),(43,65),(10,77),(10,69),(43,42)])
    elif kind == 'radar':
        ellipse(12,12,88,88);ellipse(29,29,71,71);line([(50,50),(79,23)]);line([(50,8),(50,92)]);line([(8,50),(92,50)])
    elif kind == 'sovereignty':
        line([(22,91),(22,10),(82,10),(70,30),(82,50),(22,50)])
    elif kind == 'crown':
        line([(16,37),(27,73),(73,73),(84,37),(63,54),(50,22),(37,54),(16,37)]);line([(27,86),(73,86)])
    elif kind == 'security':
        line([(50,8),(84,23),(79,60),(50,91),(21,60),(16,23),(50,8)]);line([(33,49),(46,63),(69,35)])
    elif kind == 'navy':
        line([(50,18),(50,83)]);ellipse(39,4,61,26);line([(25,40),(75,40)]);line([(16,63),(23,79),(50,93),(77,79),(84,63)])
    else:
        ellipse(12,12,88,88);line([(14,50),(86,50)]);line([(50,12),(50,88)]);ellipse(33,12,67,88)


def build():
    im=panel(1225,1033);d=ImageDraw.Draw(im)
    # Same map aperture, flag strip, history, information and focus rectangles.
    d.rectangle((14,12,1211,626),fill=(5,15,26,255),outline=EDGE)
    d.line((15,638,1210,638),fill=CYAN)
    d.rectangle((15,648,1210,733),fill=PANEL)
    box(d,(25,756,426,1009));box(d,(799,756,1200,1009))
    box(d,(449,787,522,858),False);box(d,(535,787,778,858),False)
    box(d,(449,879,778,975),False)
    save('country_selection',im)
    im=panel(579,512);box(ImageDraw.Draw(im),(16,295,563,487),False);save('select_date',im)
    for name,w,h in [('button148',148,36),('button221',221,36),('button123',123,36),('button261',261,36),('lobby_info',492,301),('lobby_settings',598,250)]:
        save(name,panel(w,h))
    for name,w,h in [('mini_selector',59,44),('country_entry',138,97),('bookmark_entry',232,211)]:
        im=Image.new('RGBA',(w*2,h),(0,0,0,0))
        for f in range(2):
            tile=panel(w,h);dt=ImageDraw.Draw(tile)
            if name in ['mini_selector','country_entry']:
                # These are drawn above the flag/portrait, so keep the aperture clear.
                dt.rectangle((3,4,w-4,h-4),fill=(0,0,0,0))
            if f:dt.rectangle((1,1,w-2,h-2),outline=CYAN,width=2)
            im.paste(tile,(f*w,0))
        save(name,im,2)
    im=Image.new('RGBA',(126,166),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rectangle((1,1,124,164),outline=EDGE,width=2);d.line((2,2,40,2),fill=CYAN,width=2);save('portrait_frame',im)
    im=Image.new('RGBA',(264,68),(0,0,0,0))
    for f,k in enumerate(['assembly','ballot','sovereignty','security']):glyph(im,k,(f*66+10,10,46,46))
    save('political_strip',im,4)
    # Engine-selected ideology sprites bypass the GUI's default sprite. Shadow
    # their exact VFS paths with original glyphs, preserving each source extent.
    for name,w,h,kind in [('neutrality_group',68,64,'assembly'),('communism_group',66,68,'industry'),('democratic_group',66,68,'ballot'),('fascism_group',66,68,'security'),('anarchism',66,66,'sovereignty'),('unknown',66,68,'world')]:
        im=Image.new('RGBA',(w,h),(0,0,0,0));glyph(im,kind,(10,10,w-20,h-20))
        save(name,im,directory='gfx/interface/ideologies')
    # Draw ABOVE the inherited map texticon. Transparent value apertures retain
    # all six original country-specific figures; no map pixels are edited.
    im=panel(211,298);d=ImageDraw.Draw(im)
    for row,kind in enumerate(['personnel','industry','industry','military','navy','air']):
        y=26+row*40
        d.rectangle((63,y,204,y+35),fill=(0,0,0,0))
        glyph(im,kind,(12,y+3,33,30),GOLD if row==2 else CYAN)
    save('map_statistics_overlay',im)
    # Purpose-drawn glyphs, not WWII medals or imported focus illustrations.
    for kind in ['economy','industry','military','assembly','ballot','air','radar','sovereignty','crown','security','navy','world']:
        for prefix,size in [('idea',60),('focus',95)]:
            im=Image.new('RGBA',(size,size),(0,0,0,0));d=ImageDraw.Draw(im)
            d.line([(size*.1,size*.3),(size*.1,size*.1),(size*.3,size*.1)],fill=EDGE,width=2)
            d.line([(size*.7,size*.9),(size*.9,size*.9),(size*.9,size*.7)],fill=EDGE,width=2)
            glyph(im,kind,(size*.2,size*.2,size*.6,size*.6),GOLD if kind=='economy' else CYAN)
            save(prefix+'_'+kind,im)
    (Path(__file__).parent/'assets.json').write_text(json.dumps(assets,indent=2)+'\n')


if __name__=='__main__':build()
