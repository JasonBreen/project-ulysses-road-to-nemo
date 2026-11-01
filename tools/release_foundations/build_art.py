"""Original release-maintenance emblems; existing flags keep national identity."""
import argparse,hashlib,importlib.util,io,json
from pathlib import Path
import PIL
from PIL import Image,ImageDraw,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];MOD=ROOT/'mod/2985041246';LIBRARY=ROOT/'tools/usea_expansion/build_art.py'
spec=importlib.util.spec_from_file_location('release_original_symbols',LIBRARY);symbols=importlib.util.module_from_spec(spec);spec.loader.exec_module(symbols)
SUBJECTS={'AWW':('command','tools'),'REC':('rebuild','scales'),'SBK':('civil','rail'),'REL':('assembly','tools'),'SER':('economy','document'),'SHI':('fishing','security'),'TER':('industry','bridge')}
def outputs():
    if PIL.__version__!='11.3.0':raise ValueError('Use pinned Pillow11.3.0')
    out={};assets=[];sprites=[];sources={};sheet=Image.new('RGBA',(700,132),(8,22,33,255));d=ImageDraw.Draw(sheet)
    for n,(tag,subjects) in enumerate(SUBJECTS.items()):
        image=Image.new('RGBA',(200,200));draw=ImageDraw.Draw(image)
        shape=[(25,10),(175,10),(191,29),(191,161),(164,190),(36,190),(9,161),(9,29)]
        draw.polygon(shape,fill=(8,22,33,255));draw.line(shape+[shape[0]],fill=(93,208,223,255),width=3)
        symbols.glyph(image,subjects[0],(32,26,132,118),(218,237,242,255));symbols.glyph(image,subjects[1],(116,108,64,62),(93,208,223,255))
        candidates=[MOD/'gfx/flags'/f'{tag}.tga']+sorted((MOD/'gfx/flags').glob(tag+'_*.tga'));flag=next(p for p in candidates if p.exists())
        with Image.open(flag) as identity:scaled=ImageOps.contain(identity.convert('RGBA'),(60,37),Image.Resampling.LANCZOS)
        image.alpha_composite(scaled,(29,145));sources[flag.relative_to(ROOT).as_posix()]=hashlib.sha256(flag.read_bytes()).hexdigest()
        for family,size,prefix,token in [('category',100,'GFX_decision_category_',f'ac_release_{tag}_maintenance'),('decision',26,'GFX_decision_',f'ac_release_{tag}')]:
            rendered=image.resize((size,size),Image.Resampling.LANCZOS)
            if family=='decision':
                aperture=Image.new('RGBA',(26,29));aperture.alpha_composite(rendered,(0,1));rendered=aperture
            stream=io.BytesIO();rendered.save(stream,format='DDS');data=stream.getvalue();relative=f'gfx/AC_release_foundations/{family}/{tag}.dds';out[MOD/relative]=data
            name=prefix+token;sprites.append(f'spriteType = {{ name = "{name}" texturefile = "{relative}" }}')
            sprites.append(f'spriteType = {{ name = "GFX_{token}" texturefile = "{relative}" }}')
            if family=='category':sheet.alpha_composite(rendered,(100*n,0));d.text((100*n+30,111),tag,fill=(218,237,242,255))
            assets.append(dict(file=relative,sprite=name,width=rendered.width,height=rendered.height,frames=1,frame_width=rendered.width,frame_height=rendered.height,alpha_min=rendered.getchannel('A').getextrema()[0],alpha_max=255,sha256=hashlib.sha256(data).hexdigest(),role='Original '+family+' maintenance composition',subjects=subjects,identity=flag.relative_to(MOD).as_posix()))
        if tag in ('AWW','REC','SHI'):
            office=Image.new('RGBA',(156,210),(8,22,33,255));frame=ImageDraw.Draw(office)
            frame.rectangle((7,7,148,202),outline=(45,85,104,255),width=2);frame.line((16,27,140,27),fill=(93,208,223,255),width=2);frame.line((16,183,140,183),fill=(93,208,223,255),width=2)
            with Image.open(flag) as identity:emblem=ImageOps.contain(identity.convert('RGBA'),(126,100),Image.Resampling.LANCZOS)
            office.alpha_composite(emblem,((156-emblem.width)//2,(210-emblem.height)//2));stream=io.BytesIO();office.save(stream,format='DDS');data=stream.getvalue();relative=f'gfx/leaders/AC_release_governments/{tag}.dds';name='GFX_ac_release_office_'+tag
            out[MOD/relative]=data;sprites.append(f'spriteType = {{ name = "{name}" texturefile = "{relative}" }}')
            assets.append(dict(file=relative,sprite=name,width=156,height=210,frames=1,frame_width=156,frame_height=210,alpha_min=255,alpha_max=255,sha256=hashlib.sha256(data).hexdigest(),role='Existing national emblem in established original government-office frame',identity=flag.relative_to(MOD).as_posix()))
    for path in (Path(__file__),LIBRARY):sources[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_text().encode()).hexdigest()
    out[MOD/'interface/ac_release_foundations.gfx']=('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n').encode()
    out[HERE/'assets.json']=(json.dumps(dict(schema=1,renderer='Pillow11.3.0',classification='Original code-native subjects and existing national flag identity; no remote art or installed-game images read; no added watermark.',source_hashes=sources,assets=assets),indent=2)+'\n').encode()
    stream=io.BytesIO();sheet.save(stream,format='PNG');out[HERE/'contact-sheet.png']=stream.getvalue()
    return out
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for path,data in outputs().items():
        if args.check:
            actual=path.read_bytes() if path.exists() else b''
            if path.suffix in ('.json','.gfx'):actual=actual.replace(b'\r\n',b'\n');data=data.replace(b'\r\n',b'\n')
            if actual!=data:raise SystemExit('Release artwork differs: '+str(path))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print('Release artwork consistent' if args.check else 'Release artwork packaged')
