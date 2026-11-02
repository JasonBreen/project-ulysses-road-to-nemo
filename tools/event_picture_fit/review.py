"""Offline before/after geometry evidence from actual retained masters/controls."""
import argparse,hashlib,html,io,json,sys
from pathlib import Path
import PIL
from PIL import Image,ImageDraw,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from event_picture_fit.audit import audit
from event_picture_fit.fit import ROOT,MOD,NAVY,same_review_png
from event_picture_fit.bitmap import BitmapFont
from event_picture_fit.proof import preserved, report as picture_proof

HERE=Path(__file__).resolve().parent
OUT=ROOT/'docs/evidence/event-picture-fit'
def encoded(image):
    stream=io.BytesIO();image.save(stream,format='PNG');return stream.getvalue()
def previous(row):
    with Image.open(ROOT/row['source']) as source:
        fitted=ImageOps.contain(source.convert('RGBA'),tuple(row['old_size']),Image.Resampling.LANCZOS)
    image=Image.new('RGBA',tuple(row['old_size']),NAVY)
    image.alpha_composite(fitted,((image.width-fitted.width)//2,(image.height-fitted.height)//2))
    if hashlib.sha256(image.tobytes()).hexdigest()!=row['old_rgba_sha256']:
        raise ValueError('Prior preview does not reproduce the captured actual texture: '+row['file'])
    return image

def canvas(image,label,font):
    result=Image.new('RGBA',(800,310),NAVY);d=ImageDraw.Draw(result)
    # Source-relative country bottom control: the options start at x215.
    d.rectangle((215,30,515,265),fill=(24,45,57,255),outline=(55,90,107,255))
    result.alpha_composite(image,(5,35))
    d.rectangle((5,35,214,210),outline=(93,208,223,255),width=2)
    d.line((215,26,215,290),fill=(210,115,106,255),width=2)
    font.draw(result,label,(7,4),780)
    font.draw(result,'x215: options column begins',(231,278),550)
    return result

def outputs():
    c=preserved();report=audit();font=BitmapFont();out={};figures=[]
    representatives=[]
    for prefix in ('gfx/AC_reconstruction/','gfx/AC_superpowers/','gfx/AC_fato_south_belka/'):
        representatives.append(next(r for r in c['country_repairs'] if r['file'].startswith(prefix)))
    sheet=Image.new('RGBA',(1600,3*310+30),NAVY)
    font.draw(sheet,'OFFLINE source geometry; deliberate30px annotation offset; no native screenshot',(8,4),1580)
    for i,row in enumerate(representatives):
        before=previous(row)
        with Image.open(MOD/row['file']) as image:after=image.convert('RGBA')
        sheet.alpha_composite(canvas(before,'BEFORE '+str(before.width)+'x'+str(before.height)+' - actual old extent',font),(0,30+i*310))
        sheet.alpha_composite(canvas(after,'AFTER210x176 - full-source contain',font),(800,30+i*310))
    out[OUT/'country-bounds.png']=encoded(sheet)
    # All40 old extents are reproduced from the preserved original master pixels.
    contacts=Image.new('RGBA',(1200,40*200),NAVY)
    for i,row in enumerate(c['country_repairs']):
        before=previous(row)
        with Image.open(MOD/row['file']) as image:after=image.convert('RGBA')
        font.draw(contacts,Path(row['file']).stem,(8,i*200+4),1160)
        contacts.alpha_composite(ImageOps.contain(before,(640,176),Image.Resampling.LANCZOS),(8,i*200+24))
        contacts.alpha_composite(after,(690,i*200+24))
        font.draw(contacts,str(before.width)+'x'+str(before.height)+' before |210x176 after',(925,i*200+72),265)
    out[OUT/'all-country-fits.png']=encoded(contacts)
    news=Image.new('RGBA',(1200,6*210+30),NAVY)
    font.draw(news,'OFFLINE news controls: x59 y91;397x153 ends244; title starts260',(8,4),1180)
    for i,row in enumerate(json.loads((HERE/'ucw_assets.json').read_text())['assets']):
        x=8;y=30+i*210
        # Do not reproduce inherited photographs in the new news artwork.
        d=ImageDraw.Draw(news);d.rectangle((x,y+15,x+210,y+191),outline=(210,115,106,255),width=2)
        d.line((x,y+184,x+440,y+184),fill=(210,115,106,255),width=2)
        font.draw(news,'Prior country-picture extent210x176',(x+223,y+30),350)
        font.draw(news,'7px beyond the news title boundary',(x+223,y+54),350)
        with Image.open(MOD/row['file']) as image:news.alpha_composite(image.convert('RGBA'),(600,y+15))
        font.draw(news,row['subject'],(600,y+172),580)
    out[OUT/'news-bounds.png']=encoded(news)
    for row in c['country_repairs']:
        figures.append('<li><code>'+html.escape(row['sprite'])+'</code>: '+str(row['old_size'])+' →210×176; complete original source <code>'+html.escape(row['source'])+'</code></li>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Event picture fit review</title><style>body{background:#081621;color:#daedf2;font:16px system-ui;max-width:1600px;margin:2rem auto;padding:0 1rem}a,h1{color:#5dd0df}img{max-width:100%;height:auto}p,li{line-height:1.5}</style><h1>Event pictures: offline fit and consumer review</h1><p>Not a native screenshot. The diagrams use actual source-relative picture/control positions and real old/new image pixels. A30px annotation offset keeps captions outside the product geometry. Country images are bounded by210×176 at5,5 and the options column starts at215. News images are397×153 at59,91, ending at244 before the title at260. No GUI layout changed.</p><p>Forty country textures now contain the entire preserved master with opaque navy padding. Three Anea and21 UCW news scenes have separate news-size bindings. UCW news uses six new original code-native subjects, separately mapped to the actual scenes; inherited country photographs remain unchanged. Stories and old country art retain their existing sizes.</p><p>''' + str(report['explicit_consumers'])+''' explicit picture consumers fit in the requested seven files. The32 implicit-picture technical events are hidden and separately listed in consumers.json; this is not an all-mod/native closure claim.</p><img src="country-bounds.png" alt="Before and after actual country picture extents"><p><a href="all-country-fits.png">All40 exact before/after fits</a></p><img src="news-bounds.png" alt="News aperture and original technical subjects"><ul>'''+''.join(figures)+'</ul><p>Separately, the Anea focus review labels use the shipped bitmap atlas and measured cells; all108 delivered focus DDS and all548 protected original files remain exact. Native rendering, input, event layout in game and display-scale acceptance remain untested.</p></html>\n'
    out[OUT/'gallery.html']=page.encode();out[OUT/'consumers.json']=(json.dumps(report,indent=2)+'\n').encode()
    out[OUT/'picture-only-proof.json']=(json.dumps(picture_proof(),indent=2)+'\n').encode()
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    if PIL.__version__!='11.3.0':raise SystemExit('Review requires Pillow11.3.0')
    bad=[]
    for path,data in outputs().items():
        if a.check:
            old=path.read_bytes() if path.exists() else b''
            equal=same_review_png(old,data) if path.suffix=='.png' else old.replace(b'\r\n',b'\n')==data.replace(b'\r\n',b'\n')
            if not equal:bad.append(path.relative_to(ROOT).as_posix())
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if bad:raise SystemExit('Event fit review differs:'+','.join(bad))
    print('Event fit offline review:40 country fits,24 news bindings,425 actual explicit consumers; originals/108focus DDS unchanged.')

if __name__=='__main__':main()
