"""Offline checks for map font routing, glyph bounds, licensing and branding."""
from pathlib import Path
import hashlib
import json
import re
import struct
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT/'mod/2985041246'


def validate():
    errors = []
    def check(ok,msg):
        if not ok:errors.append(msg)
    meta=json.loads((HERE/'font.json').read_text())
    for name,sha in meta['files'].items():
        check(hashlib.sha256((MOD/'gfx/fonts'/name).read_bytes()).hexdigest()==sha,'Font/license hash mismatch: '+name)
    check(hashlib.sha256((HERE/'source/DINish-Regular.ttf').read_bytes()).hexdigest()==meta['source_sha256'],'Source font differs from pinned release')
    data=(MOD/'gfx/fonts/hoi_mapfont4.dds').read_bytes()
    check(data[:4]==b'DDS ','Map atlas is not DDS')
    h,w=struct.unpack_from('<II',data,12)
    check((w,h)==(meta['width'],meta['height']),'Atlas dimensions differ from manifest')
    check(struct.unpack_from('<7I',data,80)==(65,0,32,0xff0000,0xff00,0xff,0xff000000),'Expected legacy 32-bit BGRA DDS')
    check(len(data)==128+w*h*4,'Incomplete font atlas')
    fnt=(MOD/'gfx/fonts/hoi_mapfont4.fnt').read_text()
    check('page id=0 file="hoi_mapfont4.dds"' in fnt,'Engine map-font page does not route to delivered atlas')
    check('outline=0' in fnt and 'bold=0' in fnt,'Expected regular-weight unoutlined labels')
    found=set()
    for line in fnt.splitlines():
        if not line.startswith('char id='):continue
        a={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
        check(a['id'] not in found,'Duplicate map glyph');found.add(a['id'])
        check(a['x']>=0 and a['y']>=0 and a['x']+a['width']<=w and a['y']+a['height']<=h,'Glyph outside atlas')
        check(a['page']==0 and a['xadvance']>0,'Invalid glyph page/advance')
    check(found==set(meta['codepoints']) and len(found)==meta['glyphs'],'Glyph inventory mismatch')
    required=set(range(32,127)) | {201,233,0x141,0x15f,0x17d,0x401,0x451,0x404,0x456,0x490} | set(range(0x410,0x450))
    check(required<=found,'Missing Latin/accent/Cyrillic coverage')
    # Check actual English country labels rather than assuming ASCII-only names.
    for p in (MOD/'localisation/english').glob('*countries*l_english.yml'):
        for line in p.read_text(encoding='utf-8-sig').splitlines():
            match=re.match(r'\s*\w+:(?:\d+)?\s+"(.*)"',line)
            if match:
                label=re.sub(r'§.','',match[1]);label=re.sub(r'\$[^$]*\$','',label)
                check(set(map(ord,label))<=found,'Country label has unsupported characters: '+line.split(':')[0].strip())
    for p in [ROOT/'mod/2985041246.mod',MOD/'descriptor.mod',MOD/'ProjectUlysses.mod']:
        check('name="Project Ulysses: Road to Nemo"' in p.read_text(),'Stale descriptor branding: '+p.name)
    loc=MOD/'localisation/english/pu_continuation_l_english.yml'
    raw=loc.read_bytes();text=raw.decode('utf-8-sig')
    check(raw.startswith(b'\xef\xbb\xbf'),'Menu localization is missing BOM')
    check('PU_MAIN_MENU_VERSION:0 "ROAD TO NEMO\\nv0.3-dev\\nTHE BELKAN PRELUDE"' in text,'Stale main-menu title')
    check('Welcome To Project Ulysses: Road to Nemo' in text,'Stale welcome heading')
    disclosure=(MOD/'localisation/english/ac_welcome_screen_l_english.yml').read_text(encoding='utf-8-sig')
    check('unofficial continuation' in disclosure and 'all credit for the original mod belongs to them' in disclosure,'Original-team disclosure was lost')
    for e in errors:print('FAIL:',e)
    if errors:return 1
    print(f'Map typography: {len(found)} glyphs, valid BGRA atlas and metrics, licenses and Road to Nemo branding pass.')
    return 0


if __name__=='__main__':sys.exit(validate())
