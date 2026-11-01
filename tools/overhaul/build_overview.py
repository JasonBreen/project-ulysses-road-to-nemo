"""Render the inherited 1991 campaign geography, independently of bookmark prose.

Inputs are the editable mod's province raster, definitions and state histories.
No installed-game pixels or new geographic claims are used. This is deliberately
a static overview: there is no invented frontend selected-country binding.
"""
import argparse
import hashlib
import io
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import get, parse

TEXTURE = 'gfx/interface/ac_overhaul/world_overview.dds'
SPRITE = 'GFX_ac_overhaul_world_overview'
WIDTH, HEIGHT = 1197, 594


def strip_inline_maps(text):
    return re.sub(r'£GFX_map_(?:belka|osea|ustio|gebet|sapin)_map\\n', '', text)


def outputs():
    definitions = MOD / 'map/definition.csv'
    raster = MOD / 'map/provinces.bmp'
    province_owner = {}
    sources = [definitions, raster]
    for path in sorted((MOD / 'history/states').glob('*.txt')):
        state = get(parse(path.read_text(encoding='utf-8-sig')), 'state')
        owner = get(get(state, 'history', []), 'owner', 'unassigned')
        for province, _, _ in get(state, 'provinces', []):
            province_owner[int(province)] = owner
        sources.append(path)
    tags = sorted(set(province_owner.values()))
    colors = np.zeros((1 << 24, 3), dtype=np.uint8)
    colors[:] = (5, 15, 26)
    owners = np.zeros(1 << 24, dtype=np.uint8)
    for line in definitions.read_text(encoding='utf-8-sig').splitlines():
        fields = line.split(';')
        if len(fields) < 5 or not fields[0].isdigit():
            continue
        ident, r, g, b = map(int, fields[:4])
        if fields[4] != 'land':
            continue
        tag = province_owner.get(ident, 'unassigned')
        digest = hashlib.sha256(tag.encode()).digest()
        key = (r << 16) | (g << 8) | b
        colors[key] = (18 + digest[0] % 12, 47 + digest[1] % 24, 62 + digest[2] % 28)
        owners[key] = tags.index(tag) + 1 if tag in tags else 255
    rgb = np.asarray(Image.open(raster).convert('RGB'), dtype=np.uint32)
    keys = (rgb[:, :, 0] << 16) | (rgb[:, :, 1] << 8) | rgb[:, :, 2]
    pixels = colors[keys]
    owner_map = owners[keys]
    boundary = np.zeros(owner_map.shape, dtype=bool)
    boundary[1:, :] |= owner_map[1:, :] != owner_map[:-1, :]
    boundary[:, 1:] |= owner_map[:, 1:] != owner_map[:, :-1]
    boundary &= owner_map != 0
    pixels[boundary] = (93, 180, 198)
    geography = Image.fromarray(pixels).resize((1165, 424), Image.Resampling.LANCZOS)
    image = Image.new('RGBA', (WIDTH, HEIGHT), (5, 15, 26, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=(45, 85, 104, 255))
    for x in range(16, WIDTH - 16, 80):
        draw.line((x, 45, x, HEIGHT - 45), fill=(12, 30, 43, 255))
    for y in range(45, HEIGHT - 45, 80):
        draw.line((16, y, WIDTH - 17, y), fill=(12, 30, 43, 255))
    image.paste(geography, (16, 85))
    draw.line((16, 43, WIDTH - 17, 43), fill=(93, 208, 223, 255))
    draw.line((16, HEIGHT - 44, WIDTH - 17, HEIGHT - 44), fill=(45, 85, 104, 255))
    buffer = io.BytesIO()
    image.save(buffer, format='DDS')
    texture = buffer.getvalue()
    sprite = f'''# Static campaign overview; no selected-country statistic binding.
spriteTypes = {{
    spriteType = {{
        name = "{SPRITE}"
        texturefile = "{TEXTURE}"
    }}
}}
'''
    localization = '''l_english:
 AC_OVERHAUL_OVERVIEW_TITLE:0 "STRANGEREAL | 1991 CAMPAIGN OVERVIEW"
 AC_OVERHAUL_OVERVIEW_NOTE:0 "Campaign frontiers at the 1991 start. Select a country below for its briefing."
'''
    manifest = dict(schema=1, kind='static campaign overview', source_layer='mod provenance',
                    file=TEXTURE, sprite=SPRITE, width=WIDTH, height=HEIGHT, frames=1,
                    transparency='opaque map; GUI is transparent to input',
                    sha256=hashlib.sha256(texture).hexdigest(),
                    sources=[dict(file=p.relative_to(ROOT).as_posix(),
                                  sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sources])
    bookmarks = MOD / 'localisation/english/bookmarks_l_english.yml'
    prose = strip_inline_maps(bookmarks.read_text(encoding='utf-8-sig'))
    return {MOD / TEXTURE: texture,
            bookmarks: prose.encode('utf-8-sig'),
            MOD / 'interface/ac_overhaul_overview.gfx': sprite.encode(),
            MOD / 'localisation/english/ac_overhaul_frontend_l_english.yml': localization.encode('utf-8-sig'),
            HERE / 'overview_assets.json': (json.dumps(manifest, indent=2) + '\n').encode()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, data in outputs().items():
        if args.check:
            if not path.exists() or path.read_bytes() != data:
                raise SystemExit('Overview differs from source: ' + str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print('Static campaign overview: 1197x594; inherited state ownership and geography.')


if __name__ == '__main__':
    main()
