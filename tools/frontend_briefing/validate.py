"""Validate briefing texture formats, sprite references and layout preservation.

Run from any directory; no installed game, Pillow, or native engine required.
The geometry fingerprint is the pre-repair 1c36a33 GUI with only visual property
values normalized. All control names, positions, sizes and 1.19 stubs are covered.
"""
from pathlib import Path
import hashlib
import json
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
HERE = Path(__file__).parent


def layout(text):
    text = re.sub(r'iconType\s*=\s*\{\s*name\s*=\s*"ac_briefing_map_statistics".*?alwaystransparent\s*=\s*yes\s*\}', '', text, flags=re.S)
    text = re.sub(r'#[^\n]*', '', text)
    text = re.sub(r'\b(?:quadTextureSprite|spriteType|font|buttonFont)\s*=\s*"[^"]*"', 'VISUAL', text)
    return hashlib.sha256(re.sub(r'\s+', '', text).encode()).hexdigest()


def validate():
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    gui = (MOD / 'interface/frontendgamesetupview.gui').read_text(encoding='utf-8-sig')
    check(layout(gui) == (HERE/'layout.sha256').read_text().strip(), 'Original frontend layout or control contract changed')
    check(not re.search(r'(?:font|buttonFont)\s*=\s*"Aces\d+_black"',gui), 'Dark briefing panel uses black text')
    check(re.search(r'name = "ac_briefing_map_statistics"\s+spriteType = "GFX_ac_briefing_map_statistics_overlay"\s+position = \{ x = 975 y = -300 \}\s+alwaystransparent = yes',gui), 'Statistics overlay moved or intercepts input')
    gfx = (MOD/'interface/ac_frontend_briefing.gfx').read_text()
    sprites = {}
    for raw in re.findall(r'spriteType\s*=\s*\{([^{}]+)\}', gfx):
        name = re.search(r'name\s*=\s*"([^"]+)"', raw)[1]
        check(name not in sprites, 'Duplicate sprite '+name)
        tex = re.search(r'texturefile\s*=\s*"([^"]+)"', raw)[1]
        frames = re.search(r'noOfFrames\s*=\s*(\d+)', raw)
        sprites[name] = (tex, int(frames[1]) if frames else 1)
    specs = {a['file']:a for a in json.loads((HERE/'assets.json').read_text())}
    for name, (tex,frames) in sprites.items():
        check(tex in specs, 'Unrecorded texture '+tex)
        check((MOD/tex).exists(), 'Missing texture '+tex)
        if tex in specs:check(frames == specs[tex]['frames'], 'Frame mismatch '+name)
    for tex, a in specs.items():
        data = (MOD/tex).read_bytes()
        check(data[:4] == b'DDS ', 'Not DDS: '+tex)
        h,w = struct.unpack_from('<II', data,12)
        flags,fourcc,bits,r,g,b,alpha = struct.unpack_from('<7I', data,80)
        check((w,h)==(a['width'],a['height']), 'Wrong dimensions '+tex)
        check((flags,fourcc,bits,r,g,b,alpha)==(65,0,32,0xff0000,0xff00,0xff,0xff000000), 'Expected 32-bit BGRA with alpha: '+tex)
        check(len(data)==128+w*h*4, 'Incomplete texture '+tex)
        check(w % a['frames'] == 0, 'Invalid frame strip '+tex)
        if tex.endswith('/mini_selector.dds'):
            for frame in range(2):
                # GUI draws this ABOVE the flag, not behind it.
                check(data[128+((22*w)+(frame*59+29))*4+3]==0, 'Flag frame aperture is opaque')
        if tex.endswith('/map_statistics_overlay.dds'):
            for row in range(6):
                check(data[128+((40+row*40)*w+130)*4+3]==0, 'Statistics value aperture is opaque')
    for entry in json.loads((HERE/'maps.json').read_text()):
        check(hashlib.sha256((MOD/entry['file']).read_bytes()).hexdigest()==entry['sha256'], 'Inherited map geography/statistics changed: '+entry['file'])
    # Check the paths selected by the engine at runtime, not only GUI defaults.
    for name in ['neutrality_group','democratic_group','fascism_group','communism_group','anarchism','unknown']:
        check('gfx/interface/ideologies/'+name+'.dds' in specs, 'Missing ideology VFS override '+name)
    for name in re.findall(r'"(GFX_ac_briefing_[^"]+)"', gui):
        check(name in sprites, 'Undefined frontend sprite '+name)
    for record in json.loads((HERE/'content.json').read_text()):
        check(record['sprite'] in sprites, 'Missing bookmark artwork '+record['id'])
        text = (ROOT/record['file']).read_text(encoding='utf-8-sig')
        expected = record['sprite'].removeprefix('GFX_idea_') if record['kind']=='idea' else record['sprite']
        pattern = (r'\b'+record['id']+r'\s*=\s*\{\s*picture\s*=\s*'+expected+r'\b') if record['kind']=='idea' else (r'\bid\s*=\s*'+record['id']+r'\s+icon\s*=\s*'+expected+r'\b')
        check(re.search(pattern,text), 'Bookmark lost its artwork binding: '+record['id'])
    for error in errors:print('FAIL:',error)
    if errors:return 1
    print(f'Briefing UI: {len(specs)} BGRA textures, {len(sprites)} sprites, 30 bookmark bindings; original geometry and controls preserved.')
    return 0


if __name__=='__main__':sys.exit(validate())
