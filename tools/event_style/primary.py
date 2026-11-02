"""Read-only exact primary metadata; DDS headers only, never engine pixel copies."""
import argparse,hashlib,json,struct,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT/'tools'))
from usea_expansion.script import parse,get
from event_style.migration import SPRITES
def digest(path):
    raw=path.read_bytes()
    if path.suffix in ('.gfx','.json'):raw=raw.replace(b'\r\n',b'\n')
    return hashlib.sha256(raw).hexdigest()
def capture(engine):
    sought={old for _,_,old,_ in SPRITES};result={}
    for relative in ('interface/core.gfx','interface/countryintelligenceagencyview.gfx','interface/countrypoliticsview.gfx','interface/eventpictures.gfx','interface/eventwindow.gfx'):
        path=engine/relative
        for kind,_,body in get(parse(path.read_text(encoding='utf-8-sig')),'spriteTypes',[]):
            if not isinstance(body,list):continue
            name=get(body,'name','').strip('"')
            if name not in sought:continue
            if name in result:raise ValueError('Ambiguous primary '+name)
            texture=get(body,'texturefile').strip('"').replace('//','/');file=engine/texture
            raw=file.read_bytes()[:128]
            if raw[:4]!=b'DDS ':raise ValueError('Primary not DDS '+texture)
            height,width=struct.unpack_from('<II',raw,12)
            result[name]=dict(definition=relative,definition_sha256=digest(path),kind=kind,fields=body,
                texture=texture,texture_sha256=digest(file),dimensions=[width,height],frames=int(get(body,'noOfFrames','1')))
    if set(result)!=sought:raise ValueError('Missing primary definitions '+str(sought-set(result)))
    version=engine/'launcher-settings.json';data=json.loads(version.read_text(encoding='utf-8-sig'))
    if data['rawVersion']!='1.19.4.1':raise ValueError('Primary game build changed; inspect explicitly')
    return dict(schema=1,reference_version=data['rawVersion'],version_source='launcher-settings.json',version_sha256=digest(version),
                scope='Read-only primary definitions and DDS headers; no imported pixels/native evidence',sprites=result)
def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--check',action='store_true');a=p.parse_args()
    data=(json.dumps(capture(a.engine),indent=2)+'\n').encode();path=HERE/'primary.json'
    if a.check:
        if path.read_bytes().replace(b'\r\n',b'\n')!=data:raise SystemExit('Installed primary contract differs')
    else:path.write_bytes(data)
    print('Read-only installed1.19.4.1:13 original primary sprite contracts verified; no engine pixels copied')
if __name__=='__main__':main()
