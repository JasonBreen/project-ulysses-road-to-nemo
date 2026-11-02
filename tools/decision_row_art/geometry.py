"""Original compact26x29 decision subjects, independently composed for rows.

No illustrations, flags or external pixels are inputs. The editable geometry
uses a simple primary silhouette at row resolution, not a category thumbnail.
"""
from PIL import Image,ImageDraw

NAVY=(8,22,33,255);CYAN=(93,208,223,255);WHITE=(218,237,242,255)


def row_icon(subject):
    scale=4;im=Image.new('RGBA',(26*scale,29*scale));d=ImageDraw.Draw(im)
    def line(points,color=WHITE,width=1.3):d.line([(round(x*scale),round(y*scale)) for x,y in points],fill=color,width=round(width*scale),joint='curve')
    def polygon(points,fill=NAVY,outline=CYAN,width=1):d.polygon([(round(x*scale),round(y*scale)) for x,y in points],fill=fill,outline=outline,width=round(width*scale))
    def box(bounds,fill=NAVY,outline=CYAN,width=1):d.rectangle(tuple(round(v*scale) for v in bounds),fill=fill,outline=outline,width=round(width*scale))
    polygon([(2,3),(23,3),(23,23),(13,27),(2,23)])
    if subject=='recovery':
        polygon([(5,15),(13,8),(21,15)],outline=WHITE)
        box((7,15,19,23));line([(12,23),(12,18),(15,18),(15,23)],WHITE)
        line([(5,9),(8,9),(8,6)],CYAN);line([(21,20),(21,23),(18,23)],CYAN)
    elif subject=='relief':
        box((5,10,20,21),outline=WHITE);line([(5,13),(20,13)],CYAN)
        line([(13,15),(13,20)],WHITE);line([(10,17.5),(16,17.5)],WHITE)
        line([(7,7),(19,7)],CYAN)
    elif subject=='institutions':
        polygon([(5,11),(13,6),(21,11)],outline=WHITE)
        for x in (7,11,15,19):line([(x,13),(x,21)],WHITE)
        line([(5,23),(21,23)],CYAN,1.6)
    elif subject=='excalibur':
        line([(13,20),(13,9),(9,5)],WHITE);line([(13,9),(21,5)],CYAN)
        line([(6,23),(13,17),(20,23)],WHITE)
        line([(17,9),(21,9),(21,13)],CYAN)
    elif subject=='v2':
        polygon([(10,19),(10,10),(13,5),(16,10),(16,19),(19,22),(16,22),(13,20),(10,22),(7,22)],outline=WHITE)
        line([(13,23),(13,25)],CYAN,2)
    elif subject=='stonehenge':
        box((5,19,21,23),outline=WHITE)
        line([(8,18),(8,14),(18,7)],WHITE,2)
        line([(15,18),(15,15),(22,10)],CYAN,1.6)
        line([(4,25),(22,25)],CYAN)
    elif subject=='arkbird':
        polygon([(3,17),(11,12),(13,6),(15,12),(23,17),(15,17),(13,23),(11,17)],outline=WHITE)
        line([(5,7),(8,5),(18,5),(21,7)],CYAN)
    elif subject=='megalith':
        polygon([(5,23),(6,14),(10,14),(10,10),(16,10),(16,14),(20,14),(21,23)],outline=WHITE)
        line([(9,23),(9,19),(17,19),(17,23)],CYAN)
        line([(13,6),(13,8)],WHITE)
    elif subject=='rhongomyniad':
        polygon([(10,23),(11,11),(13,5),(15,11),(16,23)],outline=WHITE)
        line([(6,24),(20,24)],CYAN);line([(7,12),(19,12)],CYAN)
        line([(8,9),(6,7)],WHITE);line([(18,9),(20,7)],WHITE)
    elif subject.startswith('garrison_'):
        rank={'none':0,'low':1,'mid':2,'big':3}[subject.removeprefix('garrison_')]
        polygon([(6,8),(9,8),(9,11),(12,11),(12,8),(15,8),(15,11),(18,11),(18,8),(21,8),(21,21),(6,21)],outline=WHITE)
        for n in range(rank):box((8+n*4,14,10+n*4,19),fill=CYAN,outline=CYAN)
        line([(6,24),(21,24)],CYAN)
    else:raise ValueError('Unknown compact decision subject: '+subject)
    im=im.resize((26,29),Image.Resampling.LANCZOS)
    # Remove near-transparent Lanczos RGB fringe from the deliberate aperture.
    im.putdata([(0,0,0,0) if a<4 else (r,g,b,a) for r,g,b,a in im.getdata()])
    return im
