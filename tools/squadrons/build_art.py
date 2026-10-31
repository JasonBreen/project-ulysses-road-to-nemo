"""Package retained original squadron artwork; never read installed-game art.

Use Pillow 11.3.0. Full generation/check requires all 78 selected source masters.
--gallery-only can review an incomplete source batch without writing mod assets.
It is deliberately not the artwork acceptance gate.
"""
import argparse
import hashlib
import html
import io
import json
import math
import os
from pathlib import Path

import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps

from schema import HERE, ROOT, MOD, campaigns

NAVY = (8, 22, 33, 255)
CYAN = (93, 208, 223, 255)
WHITE = (218, 237, 242, 255)
EDGE = (45, 85, 104, 255)
FONT = ROOT / 'tools/frontend_typography/source/DINish-Regular.ttf'
EVIDENCE = ROOT / 'docs/evidence/squadrons'
OUTPUTS = {}
ASSETS = []
SPRITES = []


def digest(data):
    return hashlib.sha256(data).hexdigest()


def put(path, data):
    OUTPUTS[Path(path)] = data.encode('utf-8') if isinstance(data, str) else data


def encoded(image, kind='DDS'):
    stream = io.BytesIO()
    image.convert('RGBA').save(stream, format=kind)
    return stream.getvalue()


def sources():
    """Verify selected masters against the actual per-image production record."""
    expected = []
    for row in campaigns(False):
        expected.extend(('portraits', p['id'], row['tag']) for p in row['cast'])
    plan = json.loads((HERE / 'art_plan.json').read_text(encoding='utf-8'))
    expected.extend(('scenes', r['id'], r['tag']) for r in plan['scenes'])
    expected.extend(('loading', r['id'], r['tag']) for r in plan['loading'])
    if len(expected) != 78 or len({r[1] for r in expected}) != 78:
        raise ValueError('Require 24 portraits, 48 scene masters and six independent loading masters')
    ready, missing = [], []
    for family, ident, tag in expected:
        path = HERE / 'sources' / family / (ident + '.png')
        record_path = path.with_suffix('.json')
        if not path.exists() or not record_path.exists():
            missing.append(ident)
            continue
        row = json.loads(record_path.read_text(encoding='utf-8'))
        if row.get('id') != ident or row.get('tag') != tag or row.get('file') != path.name:
            raise ValueError('Source identity differs: ' + ident)
        if 'pending' in row.get('review', '').lower() or not row.get('review'):
            raise ValueError('Selected source needs individual visual review: ' + ident)
        if not row.get('prompt') or row.get('generator') != 'built-in image_gen':
            raise ValueError('Source needs exact generation/edit provenance: ' + ident)
        if row.get('transparent_background') is not False:
            raise ValueError('Full-bleed source transparency must be deliberate: ' + ident)
        if digest(path.read_bytes()) != row.get('sha256'):
            raise ValueError('Retained source hash differs: ' + ident)
        with Image.open(path) as image:
            if image.size != (row.get('width'), row.get('height')):
                raise ValueError('Source dimensions differ: ' + ident)
            if image.width < (800 if family == 'portraits' else 1500):
                raise ValueError('Source is too small for its master role: ' + ident)
        ready.append(dict(row, path=path, record_path=record_path, family=family))
    if len({r['sha256'] for r in ready}) != len(ready):
        raise ValueError('Distinct source compositions cannot reuse an identical master')
    return ready, missing


def contained(path, size):
    # Preserve the entire head or scene. Navy bars are authored padding, not an
    # accidental transparent aperture or a crop of another event's composition.
    with Image.open(path) as original:
        fitted = ImageOps.contain(original.convert('RGBA'), size, Image.Resampling.LANCZOS)
    result = Image.new('RGBA', size, NAVY)
    result.alpha_composite(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
    return result


def texture(relative, image, sprite, role, source=None, **metadata):
    payload = encoded(image)
    put(MOD / relative, payload)
    alpha = image.getchannel('A').getextrema()
    row = dict(file=relative, width=image.width, height=image.height,
               frame_width=image.width, frame_height=image.height, frames=1,
               format='DDS RGBA8', alpha_min=alpha[0], alpha_max=alpha[1],
               alpha_requirement='opaque' if alpha == (255, 255) else 'transparent outer corners; opaque framed motif',
               sha256=digest(payload), role=role)
    if sprite:
        row['sprite'] = sprite
        SPRITES.append(f' spriteType = {{ name = "{sprite}" texturefile = "{relative}" }}')
    if source:
        row.update(source=source['path'].relative_to(ROOT).as_posix(), source_sha256=source['sha256'],
                   provenance=source['record_path'].relative_to(ROOT).as_posix(),
                   transform='Lanczos contain, centered opaque navy padding; no subject crop')
    row.update(metadata)
    ASSETS.append(row)


def insignia(tag):
    """Existing national flag plus original radio/flight-line geometry."""
    image = Image.new('RGBA', (100, 100))
    draw = ImageDraw.Draw(image)
    draw.polygon(((12, 8), (88, 8), (94, 75), (50, 94), (6, 75)), fill=NAVY, outline=CYAN, width=2)
    flag_path = MOD / 'gfx/flags' / (tag + '.tga')
    with Image.open(flag_path) as flag:
        fitted = ImageOps.contain(flag.convert('RGBA'), (58, 36), Image.Resampling.LANCZOS)
    image.alpha_composite(fitted, ((100 - fitted.width) // 2, 19 + (36 - fitted.height) // 2))
    draw.line((23, 70, 42, 70, 50, 61, 58, 70, 77, 70), fill=CYAN, width=3)
    draw.line((50, 61, 50, 82), fill=WHITE, width=2)
    return image, flag_path


def package(ready):
    for row in ready:
        ident, tag = row['id'], row['tag'].lower()
        if row['family'] == 'portraits':
            texture(f'gfx/AC_squadrons/portraits/{ident}.dds', contained(row['path'], (156, 210)),
                    'GFX_ac_sq_portrait_' + ident, 'original narrative cast portrait; never a government binding', row)
            texture(f'gfx/AC_squadrons/cast/{ident}.dds', contained(row['path'], (200, 160)),
                    'GFX_ac_sq_cast_' + ident, 'original narrative cast event card', row)
        elif row['family'] == 'scenes':
            texture(f'gfx/AC_squadrons/events/{ident}.dds', contained(row['path'], (200, 160)),
                    'GFX_ac_sq_' + ident, 'original deliberately shared narrative scene', row)
        else:
            name = 'ac_sq_' + tag
            texture(f'gfx/loadingscreens/{name}.dds', contained(row['path'], (1920, 1080)),
                    None, 'original independent loading-screen composition', row,
                    safe_area='Central subjects composed for 16:9 and 21:9; native crop acceptance pending')
            texture(f'gfx/loadingscreens/{name}_small.dds', contained(row['path'], (192, 144)),
                    'GFX_' + name + '_small', 'loading rotation picker thumbnail', row)
    for row in campaigns(False):
        image, flag = insignia(row['tag'])
        texture(f'gfx/AC_squadrons/categories/{row["tag"].lower()}.dds', image,
                'GFX_ac_sq_category_' + row['tag'].lower(), 'original story-category frame using established national flag',
                national_flag=flag.relative_to(MOD).as_posix(), national_flag_sha256=digest(flag.read_bytes()),
                editable_geometry='tools/squadrons/build_art.py:insignia')
    image = Image.new('RGBA', (75, 75))
    draw = ImageDraw.Draw(image)
    draw.polygon(((8, 6), (67, 6), (69, 60), (37, 72), (6, 60)), fill=NAVY, outline=CYAN, width=2)
    draw.rectangle((19, 20, 53, 53), outline=WHITE, width=2)
    for y, end in ((28, 46), (35, 42), (42, 48)):
        draw.line((25, y, end, y), fill=CYAN, width=2)
    draw.line((37, 8, 37, 15), fill=CYAN, width=2)
    texture('gfx/AC_squadrons/ideas/professional_debrief.dds', image,
            'GFX_idea_ac_sq_professional_debrief', 'original professional-debrief spirit icon',
            editable_geometry='tools/squadrons/build_art.py:package')
    put(MOD / 'interface/ac_squadrons.gfx', 'spriteTypes = {\n' + '\n'.join(SPRITES) + '\n}\n')
    put(MOD / 'common/frontend/backgrounds/ac_sq_backgrounds.txt',
        '# Six independent original loading compositions. Sources: tools/squadrons/sources/loading.\n' +
        ''.join('ac_sq_' + r['tag'].lower() + ' = {}\n' for r in campaigns(False)))
    plan = json.loads((HERE / 'art_plan.json').read_text())
    mapping = [{ 'tag': row['tag'], 'chapter': n,
                 'source': row['tag'].lower() + '_scene_' + slot,
                 'reason': 'Related scenes deliberately share an outcome-neutral service composition.'}
               for row in campaigns(False) for slot, ids in plan['chapters_by_slot'].items() for n in ids]
    put(HERE / 'assets.json', json.dumps(dict(schema=1, assets=ASSETS, chapter_mapping=mapping,
        ending_mapping='All three personal conclusions use the host scene8: a quiet shared airfield, without depicting a specific victory or loss.'), indent=2) + '\n')


def galleries(ready, missing):
    font = ImageFont.truetype(str(FONT), 16)
    small = ImageFont.truetype(str(FONT), 13)
    cast = {p['id']: p for r in campaigns(False) for p in r['cast']}
    for family, columns, cell in (('portraits', 6, (192, 270)), ('scenes', 4, (300, 211)), ('loading', 2, (576, 366))):
        rows = [r for r in ready if r['family'] == family]
        if not rows:
            continue
        sheet = Image.new('RGBA', (columns * cell[0], math.ceil(len(rows) / columns) * cell[1]), NAVY)
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(rows):
            x, y = index % columns * cell[0], index // columns * cell[1]
            box = (cell[0] - 16, cell[1] - 48)
            preview = contained(row['path'], box)
            sheet.alpha_composite(preview, (x + 8, y + 5))
            title = cast.get(row['id'], {}).get('name', row['id'].replace('_', ' '))
            draw.text((x + 9, y + cell[1] - 38), title, font=font, fill=WHITE)
            draw.text((x + 9, y + cell[1] - 18), row['tag'] + ' | original supporting fiction', font=small, fill=CYAN)
        put(EVIDENCE / (family + '-contact-sheet.png'), encoded(sheet, 'PNG'))
    figures = []
    for row in ready:
        relative = os.path.relpath(row['path'], EVIDENCE).replace('\\', '/')
        who = cast.get(row['id'], {})
        caption = who.get('name', row['id'].replace('_', ' '))
        extra = who.get('bio', row.get('subject', ''))
        figures.append('<figure data-family="' + row['family'] + '"><a href="' + relative + '"><img loading="lazy" src="' + relative + '" alt="' + html.escape(caption) + '"></a><figcaption><b>' + html.escape(caption) + '</b> · ' + row['tag'] + '<p>' + html.escape(extra) + '</p></figcaption></figure>')
    title = 'Original squadron campaigns — artwork review'
    status = f'{len(ready)}/78 selected masters retained and hash-verified. ' + ('Source production incomplete; this gallery is not an artwork acceptance pass.' if missing else 'Source set complete. Native rendering acceptance remains pending.')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Squadron artwork</title>
<style>body{background:#081621;color:#daedf2;font:16px system-ui;max-width:1400px;margin:2rem auto;padding:0 1rem}h1,a{color:#5dd0df}p{line-height:1.6}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem}figure{margin:0;background:#0d202e;border:1px solid #2d5568;padding:.8rem}img{width:100%;max-height:330px;object-fit:contain}figcaption{padding-top:.7rem}button{background:#0d202e;color:#daedf2;border:1px solid #5dd0df;padding:.6rem;margin:.2rem}</style>
<h1>''' + title + '</h1><p>' + status + '''</p><p>These are original supporting characters and illustrative service scenes. Portraits do not replace national leaders. Scene geography, aircraft and personal incidents are authored fiction. Shared scene slots depict service work without asserting a war outcome; six loading screens have independent compositions.</p>
<nav><button data-show="all">All</button><button data-show="portraits">Cast</button><button data-show="scenes">Narrative</button><button data-show="loading">Loading screens</button></nav><section>''' + '\n'.join(figures) + '''</section><script>document.querySelectorAll('button').forEach(b=>b.onclick=()=>document.querySelectorAll('figure').forEach(f=>f.hidden=b.dataset.show!=='all'&&f.dataset.family!==b.dataset.show));</script></html>\n'''
    put(EVIDENCE / 'artwork-gallery.html', page)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--gallery-only', action='store_true')
    args = parser.parse_args()
    if PIL.__version__ != '11.3.0':
        raise SystemExit('Reproducible artwork requires Pillow11.3.0; found ' + PIL.__version__)
    ready, missing = sources()
    if missing and not args.gallery_only:
        raise SystemExit('Artwork source set incomplete: ' + ', '.join(missing))
    if not args.gallery_only:
        package(ready)
    galleries(ready, missing)
    changed = []
    for path, data in OUTPUTS.items():
        if args.check:
            current = path.read_bytes() if path.exists() else b''
            if path.suffix == '.png' and current:
                with Image.open(io.BytesIO(current)) as actual, Image.open(io.BytesIO(data)) as expected:
                    if actual.size == expected.size and actual.convert('RGBA').tobytes() == expected.convert('RGBA').tobytes():
                        continue
            if path.suffix in ('.json', '.html', '.txt', '.gfx'):
                current = current.replace(b'\r\n', b'\n')
                data = data.replace(b'\r\n', b'\n')
            if current != data:
                changed.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if changed:
        raise SystemExit('Squadron artwork output differs: ' + ', '.join(changed))
    print(f'Squadron artwork: {len(ready)}/78 masters; {len(ASSETS)} packaged textures; ' +
          ('partial source gallery only' if args.gallery_only else ('verified' if args.check else 'packaged')))


if __name__ == '__main__':
    main()
