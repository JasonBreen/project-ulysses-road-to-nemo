"""Technical resampling/format conversion only; source artwork stays untouched."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageOps

HERE=Path(__file__).resolve().parent
MOD=HERE.parents[1]/'mod/2985041246'

def main():
    records=[];sprites=[]
    def save(source,relative,dimensions,sprite=None):
        original=Image.open(source).convert('RGBA')
        image=ImageOps.contain(original,dimensions,Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',dimensions,(0,0,0,0) if sprite and 'portrait' in sprite else (8,22,33,255))
        canvas.alpha_composite(image,((dimensions[0]-image.width)//2,(dimensions[1]-image.height)//2))
        target=MOD/relative;target.parent.mkdir(parents=True,exist_ok=True);canvas.save(target)
        records.append(dict(file=relative,source=source.relative_to(HERE).as_posix(),width=dimensions[0],height=dimensions[1],frames=1,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),sprite=sprite))
        if sprite:sprites.append('spriteType = { name = "'+sprite+'" texturefile = "'+relative+'" }')
    for row in json.loads((HERE/'original_art.json').read_text()):
        # 1.19.4 country events reserve a 200px picture column beside options.
        # Preserve the wide master with navy letterboxing, rather than letting
        # a news-event-sized image cover the country-event option buttons.
        save(HERE/row['file'],'gfx/event_pictures/ac_exp_'+row['id']+'.dds',(200,160),'GFX_ac_exp_event_'+row['id'])
    backgrounds=[]
    for ident,file in [('cockpit','AC8-key-feature-screenshot-1.jpg'),('formation','AC8-key-feature-screenshot-2.jpg'),('pilot','AC8-key-feature-screenshot-3_V2.jpg'),('joker_flight','AC8_KF_4.png')]:
        source=HERE/'sources/official_ac8'/file
        name='ac8_'+ident;backgrounds.append(name+' = {}')
        save(source,'gfx/loadingscreens/'+name+'.dds',(1920,1080))
        save(source,'gfx/loadingscreens/'+name+'_small.dds',(192,144),'GFX_'+name+'_small')
    for source in sorted((HERE/'sources/official_ac8').glob('*-thumbnail.png')):
        ident=source.stem.removesuffix('-thumbnail').lower().replace('-','_')
        save(source,'gfx/leaders/AC8/portrait_'+ident+'.dds',(156,210),'GFX_ac8_portrait_'+ident)
    (MOD/'interface/ac_expansion_media.gfx').write_text('spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n')
    p=MOD/'common/frontend/backgrounds/base_backgrounds.txt'
    text=p.read_text().split('# AC8 official art rotation')[0].rstrip()
    p.write_text(text+'\n\n# AC8 official art rotation; see tools/usea_expansion/official_art.json.\n'+'\n'.join(backgrounds)+'\n')
    (HERE/'media_assets.json').write_text(json.dumps(records,indent=2)+'\n')
    print('Packaged',len(records),'event, loading-screen and named portrait textures.')

if __name__=='__main__':main()
