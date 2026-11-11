"""Validate briefing texture formats, sprite references and layout preservation.

Run from any directory; no installed game, Pillow, or native engine required.
The geometry fingerprint is the pre-repair 1c36a33 GUI with visual properties
normalized. The separately validated Anea country-history scrolling repair is
restored to its captured original before fingerprinting. Other control names,
positions, sizes and 1.19 stubs retain their historical fingerprint coverage.
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


def sprite_blocks(gfx):
    """(kind, body) for every spriteType and corneredTileSpriteType, nested braces included."""
    for match in re.finditer(r'\b(spriteType|corneredTileSpriteType)\s*=\s*\{', gfx):
        depth = 1; index = match.end()
        while depth:
            depth += {'{': 1, '}': -1}.get(gfx[index], 0); index += 1
        yield match[1], gfx[match.end():index-1]


def mod_sprite_names():
    names = set()
    for path in (MOD/'interface').glob('*.gfx'):
        names |= set(re.findall(r'name\s*=\s*"?(GFX_\w+)"?', path.read_text(encoding='utf-8-sig', errors='replace')))
    return names


def lobby(gui, sprites, tiles, specs, check):
    """Every engine sprite left on the screen has a recorded disposition."""
    record = json.loads((HERE/'lobby_sprites.json').read_text())['sprites']
    rows = {row['sprite']: row for row in record}
    check(len(rows) == len(record), 'Duplicate lobby sprite disposition')
    bound = set(re.findall(r'(?:spriteType|quadTextureSprite)\s*=\s*"?(GFX_\w+)"?', gui))
    engine = bound - mod_sprite_names()
    for name in sorted(engine):
        row = rows.get(name)
        check(row is not None, 'Engine sprite without a disposition: '+name)
        if row:check(row['disposition'] == 'keep_engine', 'Restyled or hidden sprite still bound to the engine: '+name)
    for row in record:
        check(row['disposition'] in ('restyle', 'hide', 'keep_engine', 'mod_override') and len(row['reason']) > 20, 'Bad disposition '+row['sprite'])
        if row['disposition'] == 'keep_engine':
            check(row['sprite'] in engine, 'Kept engine sprite no longer on the screen: '+row['sprite'])
            continue
        if row['disposition'] == 'mod_override':
            # Still bound by name, but the mod now defines that name itself (the vanilla visual scrub).
            check(row['sprite'] in bound and row['sprite'] in mod_sprite_names(), 'Mod override is not bound and mod-defined: '+row['sprite'])
            continue
        check(row['sprite'] not in bound, 'Still bound: '+row['sprite'])
        check(row['replacement'] in bound, 'Replacement not bound on the screen: '+row['replacement'])
        if row['disposition'] == 'restyle':
            check(row['replacement'] in tiles, 'Restyle is not a cornered tile: '+row['replacement'])
        else:
            check(row['replacement'] == 'GFX_ac_briefing_lobby_hidden', 'Hidden sprite not bound to the transparent sprite: '+row['sprite'])
    for name, (tex, w, h, bx, by) in tiles.items():
        spec = specs.get(tex)
        check(bool(spec) and (spec['width'], spec['height']) == (w, h), 'Cornered tile size differs from its texture: '+name)
        check(2*bx < w and 2*by < h, 'Cornered tile border leaves no centre: '+name)
    hidden = MOD/sprites.get('GFX_ac_briefing_lobby_hidden', ('',))[0]
    data = hidden.read_bytes() if hidden.is_file() else b''
    check(len(data) == 132 and data[128:132] == b'\0\0\0\0', 'Hidden sprite is not one transparent pixel')


def validate():
    errors = []
    def check(ok, message):
        if not ok: errors.append(message)
    gui = (MOD / 'interface/frontendgamesetupview.gui').read_text(encoding='utf-8-sig')
    # Deliberate exception: exactly one country history text control. Verify its
    # complete repaired node and bounds, then restore its recorded original for
    # the historical fingerprint. Do not refresh the fingerprint or hide other
    # geometry/control changes behind a broad normalization rule.
    sys.path.insert(0, str(ROOT/'tools/anea'))
    try:
        from build_briefs_ui import normalize_for_fingerprint
        historical_gui = normalize_for_fingerprint(gui)
    except (ValueError, OSError, KeyError) as error:
        check(False, 'Country history scrolling contract: '+str(error))
    else:
        check(layout(historical_gui) == (HERE/'layout.sha256').read_text().strip(), 'Unmanaged frontend controls changed outside the reviewed responsive repair')
    check(not re.search(r'(?:font|buttonFont)\s*=\s*"Aces\d+_black"',gui), 'Dark briefing panel uses black text')
    check('name = "ac_briefing_map_statistics"' not in gui, 'Unbound legacy statistics layer is still visible')
    check('name = "ac_overhaul_world_overview"' in gui, 'Independent campaign overview is missing')
    gfx = (MOD/'interface/ac_frontend_briefing.gfx').read_text()
    sprites = {}; tiles = {}
    for kind, raw in sprite_blocks(gfx):
        name = re.search(r'name\s*=\s*"([^"]+)"', raw)[1]
        check(name not in sprites, 'Duplicate sprite '+name)
        tex = re.search(r'texturefile\s*=\s*"([^"]+)"', raw)[1]
        frames = re.search(r'noOfFrames\s*=\s*(\d+)', raw)
        sprites[name] = (tex, int(frames[1]) if frames else 1)
        if kind == 'corneredTileSpriteType':
            size = re.search(r'size\s*=\s*\{\s*x\s*=\s*(\d+)\s*y\s*=\s*(\d+)\s*\}', raw)
            border = re.search(r'borderSize\s*=\s*\{\s*x\s*=\s*(\d+)\s*y\s*=\s*(\d+)\s*\}', raw)
            check(bool(size and border), 'Cornered tile without size and borderSize: '+name)
            if size and border:tiles[name] = (tex, int(size[1]), int(size[2]), int(border[1]), int(border[2]))
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
    lobby(gui, sprites, tiles, specs, check)
    for error in errors:print('FAIL:',error)
    if errors:return 1
    print(f'Briefing UI: {len(specs)} BGRA textures, {len(sprites)} sprites, 30 bookmark bindings; reviewed responsive selection geometry; unmanaged controls preserved.')
    return 0


if __name__=='__main__':sys.exit(validate())
