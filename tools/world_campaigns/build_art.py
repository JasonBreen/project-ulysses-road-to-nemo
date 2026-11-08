"""Original technical insignia and briefing diagrams; no borrowed pixels."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import importlib.util
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
spec = importlib.util.spec_from_file_location('wc_original_glyphs', ROOT / 'tools/frontend_briefing/build.py')
glyphs = importlib.util.module_from_spec(spec); spec.loader.exec_module(glyphs)
glyph = glyphs.glyph

DOMAINS = dict(civil='assembly', industry='industry', logistics='world', air='air',
               land='military', naval='navy', intelligence='radar', research='radar', diplomacy='sovereignty')


def outputs():
    result, assets, sprites = {}, [], []
    for tag in ('SOA', 'CSO'):
        color = (93, 208, 223, 255) if tag == 'SOA' else (230, 181, 95, 255)
        for index, (domain, kind) in enumerate(DOMAINS.items()):
            for scene in (False, True):
                w, h = (200, 160) if scene else (96, 96)
                im = Image.new('RGBA', (w, h), (8, 22, 33, 255) if scene else (0, 0, 0, 0))
                draw = ImageDraw.Draw(im)
                if scene:
                    for x in range(12, w, 20):
                        draw.line((x, 12, x, h-12), fill=(18, 44, 60, 255))
                    draw.rectangle((1, 1, w-2, h-2), outline=color)
                    draw.line((18, 132, 182, 132), fill=color, width=2)
                    glyph(im, kind, (60, 26, 80, 80), color)
                else:
                    draw.polygon([(48, 2), (91, 26), (91, 70), (48, 94), (5, 70), (5, 26)], outline=color, width=2)
                    glyph(im, kind, (23, 23, 50, 50), color)
                # Sector marks distinguish research/intelligence and the entire family.
                for mark in range(index+1):
                    x = 15 + mark * 7
                    draw.line((x, h-10, x+3, h-10), fill=color, width=2)
                relative = f'gfx/AC_world_campaigns/{tag}_{domain}' + ('_scene.dds' if scene else '.dds')
                stream = io.BytesIO(); im.save(stream, format='DDS'); data = stream.getvalue()
                result[relative] = data
                sprite = f'GFX_{tag}_wc_' + ('scene_' if scene else '') + domain
                sprites.append('spriteType = { name = "' + sprite + '" texturefile = "' + relative + '" }')
                if not scene:
                    for alias in (sprite+'_shine', f'GFX_idea_{tag}_wc_{domain}', f'GFX_decision_category_{tag}_wc_{domain}'):
                        sprites.append('spriteType = { name = "' + alias + '" texturefile = "' + relative + '" }')
                    row = Image.new('RGBA',(26,29),(0,0,0,0))
                    glyph(row,kind,(4,5,18,18),color)
                    row_path = f'gfx/AC_world_campaigns/{tag}_{domain}_row.dds'
                    stream_row = io.BytesIO(); row.save(stream_row,format='DDS'); row_data=stream_row.getvalue()
                    result[row_path]=row_data
                    sprites.append(f'spriteType = {{ name = "GFX_decision_{tag}_wc_{domain}" texturefile = "{row_path}" }}')
                    assets.append(dict(file=row_path,width=26,height=29,sha256=hashlib.sha256(row_data).hexdigest(),
                        source_layer='original compact procedural icon',authoring_source='tools/world_campaigns/build_art.py',
                        inputs='geometric primitives only; independent 26x29 row extent'))
                assets.append(dict(file=relative, width=w, height=h, sha256=hashlib.sha256(data).hexdigest(),
                    source_layer='original procedural diagram', authoring_source='tools/world_campaigns/build_art.py',
                    inputs='geometric primitives only; no game/reference/downloaded pixels'))
    result['interface/ac_world_campaigns.gfx'] = ('spriteTypes = {\n' + '\n'.join(sprites) + '\n}\n').encode()
    return result, assets


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    result, assets = outputs()
    failures = []
    for relative, data in result.items():
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_bytes() != data: failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    text = json.dumps(assets, indent=2) + '\n'; path = HERE / 'assets.json'
    if args.check:
        if path.read_text() != text: failures.append('assets.json')
    else: path.write_text(text, encoding='utf-8', newline='\n')
    if failures: raise SystemExit('Artwork differs: ' + ', '.join(failures))
    print('Original Sotoan insignia and diagrams:', len(assets), '; no native rendering claim.')


if __name__ == '__main__': main()
