"""Reproducible offline source/crop review; never changes a selected master."""
import argparse,html,io,json,os,re
from pathlib import Path
import PIL
from PIL import Image,ImageChops,ImageOps
from audit import HERE,ROOT,SOURCES,digest,sources

OUT=ROOT/'docs/evidence/pacific-story-art'
NAVY=(8,22,33,255);WHITE=(218,237,242,255);CYAN=(93,208,223,255)

class Atlas:
    def __init__(self):
        base=ROOT/'mod/2985041246/gfx/fonts/ACBriefing16'
        self.glyphs={}
        for line in base.with_suffix('.fnt').read_text().splitlines():
            if line.startswith('char '):
                g={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)};self.glyphs[chr(g['id'])]=g
        self.image=Image.open(base.with_suffix('.dds')).convert('RGBA');self.missing=set()
    def draw(self,image,text,x,y,color=WHITE):
        for c in text:
            if c not in self.glyphs:self.missing.add(c)
            g=self.glyphs.get(c,self.glyphs['?']);tile=self.image.crop((g['x'],g['y'],g['x']+g['width'],g['y']+g['height']))
            ink=Image.new('RGBA',tile.size,color);ink.putalpha(ImageChops.multiply(tile.getchannel('A'),ink.getchannel('A')))
            image.alpha_composite(ink,(x+g['xoffset'],y+g['yoffset']));x+=g['xadvance']

def contain(original,size):
    fitted=ImageOps.contain(original.convert('RGBA'),size,Image.Resampling.LANCZOS)
    image=Image.new('RGBA',size,NAVY);image.alpha_composite(fitted,((size[0]-fitted.width)//2,(size[1]-fitted.height)//2));return image
def crop(original,size):return ImageOps.fit(original.convert('RGBA'),size,Image.Resampling.LANCZOS,centering=(.5,.5))
def encode(image):
    buf=io.BytesIO();image.save(buf,format='PNG');return buf.getvalue()
def same_png(a,b):
    try:
        with Image.open(io.BytesIO(a)) as one,Image.open(io.BytesIO(b)) as two:return one.size==two.size and one.convert('RGBA').tobytes()==two.convert('RGBA').tobytes()
    except (OSError,ValueError):return False

def outputs():
    plan,ready=sources();atlas=Atlas();result={}
    portrait=[r for r in ready if r['file'].endswith('.png') and r['path'].parent.name=='portraits']
    sheet=Image.new('RGBA',(1280,570),NAVY)
    atlas.draw(sheet,'OFFLINE source review - 156x210 portrait fit retains full head; no native claim',8,5,CYAN)
    for i,r in enumerate(portrait):
        x=i%4*320;y=i//4*270+26
        atlas.draw(sheet,r['id'],x+8,y+1)
        with Image.open(r['path']) as image:
            sheet.alpha_composite(contain(image,(156,210)),(x+8,y+27));sheet.alpha_composite(contain(image,(140,210)),(x+174,y+27))
        atlas.draw(sheet,'156x210 fit | full source',x+8,y+242,CYAN)
    result[OUT/'portraits-review.png']=encode(sheet)
    scene=[r for r in ready if r['path'].parent.name=='scenes']
    sheet=Image.new('RGBA',(1680,936),NAVY)
    atlas.draw(sheet,'OFFLINE review - full source fit and conservative center crop at200x160; original PNGs untouched',8,4,CYAN)
    for i,r in enumerate(scene):
        x=i%4*420;y=i//4*228+24
        atlas.draw(sheet,r['id']+((' - '+r['ending']) if r.get('ending') else' - core'),x+8,y+1)
        with Image.open(r['path']) as image:
            sheet.alpha_composite(contain(image,(200,160)),(x+8,y+29));sheet.alpha_composite(crop(image,(200,160)),(x+212,y+29))
        atlas.draw(sheet,'full fit200x160 | center crop',x+8,y+198,CYAN)
    result[OUT/'scenes-review.png']=encode(sheet)
    for r in ready:
        if r['path'].parent.name!='loading':continue
        with Image.open(r['path']) as image:
            result[OUT/(r['id']+'-16x9.png')]=encode(crop(image,(960,540)))
            result[OUT/(r['id']+'-3440x1440.png')]=encode(crop(image,(860,360)))
    if atlas.missing:raise ValueError('Review font missing glyphs:'+str(atlas.missing))
    figures=[]
    for r in ready:
        relative=os.path.relpath(r['path'],OUT).replace('\\','/')
        extra=''
        if r['path'].parent.name=='loading':extra='<p><a href="'+r['id']+'-16x9.png">16:9 center crop</a> | <a href="'+r['id']+'-3440x1440.png">exact3440:1440 crop preview</a></p>'
        figures.append('<figure><a href="'+relative+'"><img loading="lazy" src="'+relative+'" alt="'+html.escape(r['id'])+'"></a><figcaption><b>'+html.escape(r['id'])+'</b> '+str(r['width'])+'x'+str(r['height'])+'<p>'+html.escape(r['review'])+'</p><p><b>Packaging:</b> '+html.escape(r['packaging_contract'])+'</p>'+extra+'</figcaption></figure>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Pacific original art review</title><style>body{background:#081621;color:#daedf2;font:16px system-ui;max-width:1500px;margin:2rem auto;padding:0 1rem}a,h1{color:#5dd0df}p{line-height:1.5}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:1rem}figure{margin:0;padding:1rem;border:1px solid #2d5568}img{width:100%;max-height:330px;object-fit:contain}figcaption{padding-top:.6rem}</style><h1>Pacific story art:26 original masters</h1><p>OFFLINE source and candidate-crop review. Original supporting fiction; these portraits do not replace national leaders. Eight portraits,16 narrative scenes and two separately composed loading masters. Core scenes are grounded and outcome-neutral; ending slots6/7/8 show trusted, compromised and fractured personal conclusions. No native game, input, DDS or loading-scaling acceptance is claimed.</p><p><a href="portraits-review.png">Portrait fits</a> | <a href="scenes-review.png">Scene fit/crop sheet</a>. The loading service returned1932x814 panoramas despite a16:9 request. Selected originals remain byte-for-byte unchanged. Separate conservative16:9 and exact3440:1440 center-cover previews expose the actual crop; runtime packaging/scaling remains the integration owner's gate.</p><section>'''+''.join(figures)+'</section></html>\n'
    result[OUT/'gallery.html']=page.encode()
    report=dict(schema=1,scope='Offline selected-source validation; no native or packaged DDS acceptance',selected_masters=26,
        portraits=8,scenes=16,independent_loadings=2,retained_prior_edits=5,missing_font_glyphs=[],
        crop_methods=dict(portraits='full-height contain156x210',scenes='full contain and conservative center-cover200x160',
            loading='independent full-bleed originals with center-cover16:9 and exact3440:1440 previews; engine scaling untested'),
        sources=[{k:r[k] for k in ('id','tag','kind','width','height','sha256','source_output','visual_reviewed','review','packaging_contract','evidence_tier')} for r in ready])
    result[OUT/'review.json']=(json.dumps(report,indent=2)+'\n').encode()
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    if PIL.__version__!='11.3.0':raise SystemExit('Review reproducibility requires Pillow11.3.0')
    changed=[]
    for path,data in outputs().items():
        if args.check:
            old=path.read_bytes() if path.exists() else b''
            equal=same_png(old,data) if path.suffix=='.png' else old.replace(b'\r\n',b'\n')==data.replace(b'\r\n',b'\n')
            if not equal:changed.append(path.relative_to(ROOT).as_posix())
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if changed:raise SystemExit('Offline review differs:'+','.join(changed))
    print('Pacific review:26 source masters;8 original/candidate-crop artifacts; no missing font glyphs;'+('reproduced' if args.check else'written'))

if __name__=='__main__':main()
