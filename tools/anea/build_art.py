"""Reproduce Anea artwork from original masters, authored geometry and existing flags.

No installed-game pixels are read. Raster masters were generated once through the
built-in image tool; reproduction only requires Pillow and the committed sources.
--check compares every generated texture, manifest, binding and gallery byte.
"""
import argparse
import hashlib
import html
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
FONT = ROOT / 'tools/frontend_typography/source/DINish-Regular.ttf'
NAVY = (8, 22, 33, 255)
PANEL = (13, 32, 46, 255)
EDGE = (45, 85, 104, 255)
CYAN = (93, 208, 223, 255)
WHITE = (218, 237, 242, 255)
BLUE = (151, 183, 225, 255)

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'tools'))
from event_picture_fit.fit import contain as fit_event, same_review_png
from event_picture_fit.bitmap import BitmapFont
from content import FOCUSES, POLICIES

# Reuse the project's editable code-native symbol vocabulary, not delivered art.
spec = importlib.util.spec_from_file_location('ulysses_art_symbols', ROOT / 'tools/usea_expansion/build_art.py')
symbols = importlib.util.module_from_spec(spec)
spec.loader.exec_module(symbols)
glyph = symbols.glyph
row_spec = importlib.util.spec_from_file_location('anea_decision_rows', ROOT / 'tools/decision_row_art/geometry.py')
row_geometry = importlib.util.module_from_spec(row_spec)
row_spec.loader.exec_module(row_geometry)

OUTPUTS = {}
ASSETS = []
SPRITES = []


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(image, format='DDS'):
    stream = io.BytesIO()
    image.convert('RGBA').save(stream, format=format)
    return stream.getvalue()


def put(path, data):
    OUTPUTS[ROOT / path] = data.encode('utf-8') if isinstance(data, str) else data


def texture(relative, image, role, sprite=None, source=None, frames=1, **metadata):
    data = encoded(image)
    put('mod/2985041246/' + relative, data)
    alpha = image.convert('RGBA').getchannel('A')
    row = dict(file=relative, width=image.width, height=image.height,
               frame_width=image.width // frames, frames=frames,
               format='DDS RGBA8', alpha_min=alpha.getextrema()[0],
               alpha_max=alpha.getextrema()[1], role=role, sha256=digest(data))
    if sprite:
        row['sprite'] = sprite
        SPRITES.append(f'spriteType = {{ name = "{sprite}" texturefile = "{relative}" }}')
    if source:
        row['source'] = source.relative_to(ROOT).as_posix()
        row['source_sha256'] = digest(source.read_bytes())
    row.update(metadata)
    ASSETS.append(row)
    return row


def alias(name, relative):
    SPRITES.append(f'spriteType = {{ name = "{name}" texturefile = "{relative}" }}')


# The supporting object conveys the subject within a shared institutional family.
# Ordered patterns make e.g. a shelter medical plan different from a shelter store.
SUBJECTS = [
    ('chandelier|technical value|research|scientific|science', 'science'),
    ('ulysses|risk estimate|risk assessment', 'meteor'),
    ('shelter|evacuat', 'shelter'),
    ('medical|hospital|sanitation|water', 'medical'),
    ('rail|freight|dispatch|timetable', 'rail'),
    ('harbour|harbor|coast|flotilla|naval', 'navy'),
    ('airfield|aircrew|air maintenance|ground crew', 'runway'),
    ('air |aircraft|air service|aircrew', 'air'),
    ('workshop|repair|maintenance|spare|supplier', 'tools'),
    ('aid|assistance|receiving|relief|displaced', 'refugees'),
    ('audit|allocation|budget|account|distribution', 'scales'),
    ('documents|register|records|report|standard|protocol|inventory', 'document'),
    ('reserve|transport|stock|depot|stores|logistics|supply', 'logistics'),
    ('bridge|road|corridor', 'bridge'),
    ('cooper|neighbour|neighborhood|foreign|consult|diploma|contacts|accord', 'diplomacy'),
    ('recovery|reconstruction|rebuild', 'rebuild'),
    ('training|instructor|exercise|readiness', 'training'),
    ('communication|warning|rota|channels', 'communications'),
    ('industrial|productive|production', 'industry'),
    ('command|defence|defense|military', 'command'),
    ('civil|service|public', 'civil'),
    ('office|administration|republic|federation|compact|assessment|government', 'assembly'),
]
SUPPORT = {'assembly':'document', 'document':'assembly', 'economy':'scales',
           'civil':'medical', 'command':'communications', 'industry':'tools',
           'rail':'logistics', 'air':'runway', 'navy':'logistics', 'training':'command',
           'science':'document', 'shelter':'medical', 'logistics':'document',
           'rebuild':'tools', 'diplomacy':'document', 'refugees':'civil',
           'communications':'radar', 'tools':'industry', 'scales':'economy',
           'radar':'science', 'meteor':'shelter', 'medical':'civil',
           'security':'command', 'bridge':'rebuild', 'gate':'document',
           'runway':'air', 'telescope':'science', 'satellite':'science'}
LAYOUTS = [
    ('support-inset', (27, 29, 126, 123), (132, 116, 45, 44)),
    ('paired-instruments', (20, 36, 91, 110), (109, 58, 65, 76)),
    ('service-and-record', (50, 27, 100, 92), (64, 122, 65, 43)),
    ('diagonal-work', (28, 29, 107, 99), (108, 103, 62, 59)),
    ('foreground-context', (60, 30, 104, 111), (24, 115, 49, 46)),
    ('planning-horizon', (36, 25, 121, 100), (61, 127, 69, 36)),
    ('left-service-inset', (53, 29, 119, 122), (22, 119, 46, 43)),
    ('fieldwork-and-plan', (43, 77, 107, 82), (73, 24, 47, 45)),
    ('upper-context', (27, 65, 111, 92), (120, 30, 49, 48)),
    ('wide-service', (22, 55, 149, 97), (76, 20, 41, 38)),
    ('lower-record', (43, 29, 106, 105), (31, 133, 46, 34)),
    ('right-record', (28, 36, 107, 106), (129, 96, 43, 65)),
]


def art_direction(row, used):
    primary = row.kind
    subjects = [subject for pattern, subject in SUBJECTS
                if re.search(pattern, row.title.lower()) and subject != primary]
    secondary = subjects[0] if subjects else SUPPORT[primary]
    pair = (row.tag, primary, secondary)
    ordinal = used.get(pair, 0)
    if ordinal >= len(LAYOUTS):
        raise ValueError(f'Add a hand-authored arrangement for {pair}: {row.id}')
    used[pair] = ordinal + 1
    return primary, secondary, LAYOUTS[ordinal]


def frame(tag, phase='foundation', size=192):
    image = Image.new('RGBA', (192, 192))
    d = ImageDraw.Draw(image)
    accent = CYAN if tag == 'EMM' else BLUE
    shape = ([(22, 21), (170, 21), (170, 153), (96, 179), (22, 153)]
             if tag == 'EMM' else
             [(96, 8), (172, 35), (165, 149), (96, 177), (27, 149), (20, 35)])
    d.polygon(shape, fill=NAVY)
    d.line(shape + [shape[0]], fill=accent, width=3)
    # Structural horizon differs by act; it contains no ordinal or baked caption.
    if phase == 'foundation':
        d.line((36, 165, 71, 165), fill=EDGE, width=2)
        d.line((121, 165, 156, 165), fill=EDGE, width=2)
    elif phase == 'warning':
        d.line((35, 156, 46, 167, 57, 156), fill=accent, width=2)
        d.line((135, 156, 146, 167, 157, 156), fill=accent, width=2)
    else:
        d.arc((30, 132, 161, 177), 0, 180, fill=accent, width=2)
    return image, accent


def build_focuses():
    used = {}
    records = []
    previews = []
    for row in FOCUSES:
        primary, secondary, arrangement = art_direction(row, used)
        image, accent = frame(row.tag, row.phase)
        glyph(image, primary, arrangement[1], WHITE)
        glyph(image, secondary, arrangement[2], accent)
        image = image.resize((96, 96), Image.Resampling.LANCZOS)
        relative = f'gfx/AC_anea/focus/{row.id}.dds'
        sprite = 'GFX_ac_anea_focus_' + row.id
        asset = texture(relative, image, 'original focus composition', sprite,
                        primary=primary, secondary=secondary,
                        composition=arrangement[0], phase=row.phase, tag=row.tag)
        alias(sprite + '_shine', relative)
        records.append(dict(id=row.id, title=row.title, tag=row.tag, phase=row.phase,
                            primary=primary, secondary=secondary,
                            composition=arrangement[0], sprite=sprite,
                            asset=relative, sha256=asset['sha256']))
        previews.append((row, image))
    if len(records) != 108 or len({r['sha256'] for r in records}) != 108:
        raise ValueError('Every one of the 108 focus compositions must be distinct')
    put('tools/anea/focus_art.json', json.dumps(records, indent=2) + '\n')
    # Review labels use the shipped glyph atlas, never OS/FreeType rasterization.
    # Larger review cells retain full titles at their actual bitmap advances.
    sheet = Image.new('RGBA', (1800, 26 + 12 * 200), NAVY)
    font = BitmapFont()
    font.draw(sheet, 'OFFLINE artwork review; native focus rendering remains untested', (8, 3), 1784)
    for index, (row, image) in enumerate(previews):
        x = (index % 9) * 200
        y = 26 + (index // 9) * 200
        sheet.alpha_composite(image, (x + 52, y + 3))
        if font.draw(sheet, row.title, (x + 8, y + 105), 184) > 84:
            raise ValueError('Anea offline review title exceeds its measured cell: ' + row.id)
    put('docs/evidence/anea/focus-contact-sheet.png', encoded(sheet, 'PNG'))


SHARED = {
    'ac_anea_relief_burden': ('civil', 'refugees'),
    'ac_anea_monitored_service': ('document', 'refugees'),
    'ac_anea_sanctions': ('gate', 'scales'),
    'ac_anea_bureau': ('assembly', 'diplomacy'),
    'ac_anea_domestic_works': ('rebuild', 'tools'),
}


def emblem(primary, secondary, tag, size, layout=0):
    image, accent = frame(tag, 'recovery')
    arrangement = LAYOUTS[layout % len(LAYOUTS)]
    glyph(image, primary, arrangement[1], WHITE)
    glyph(image, secondary, arrangement[2], accent)
    return image.resize(size, Image.Resampling.LANCZOS)


def build_policies():
    for index, (ident, (title, description, modifiers, kind)) in enumerate(POLICIES.items()):
        tag = ident[:3]
        image = emblem(kind, SUPPORT[kind], tag, (75, 75), index)
        texture(f'gfx/AC_anea/policies/{ident}.dds', image, 'original national policy artwork',
                'GFX_idea_ac_anea_idea_' + ident, tag=tag, policy=ident)
    for index, (ident, (primary, secondary)) in enumerate(SHARED.items()):
        image = emblem(primary, secondary, 'EVA' if ident == 'ac_anea_sanctions' else 'EMM', (75, 75), index)
        texture(f'gfx/AC_anea/policies/{ident}.dds', image, 'original shared policy artwork',
                'GFX_idea_' + ident, policy=ident)
    for suffix, motifs in [('recovery', ('rebuild', 'civil')), ('relief', ('logistics', 'refugees'))]:
        relative = f'gfx/AC_anea/categories/{suffix}.dds'
        texture(relative, emblem(*motifs, 'EMM', (100, 100)),
                'original decision category artwork', 'GFX_ac_anea_category_' + suffix)
        alias('GFX_decision_category_ac_anea_' + suffix, relative)
        texture(f'gfx/AC_anea/decisions/{suffix}.dds', row_geometry.row_icon(suffix),
                'original compact decision row composition', 'GFX_decision_ac_anea_' + suffix,
                source=ROOT / 'tools/decision_row_art/geometry.py', subject=suffix)


def contained(source, size):
    with Image.open(source) as original:
        result = ImageOps.contain(original.convert('RGBA'), size, Image.Resampling.LANCZOS)
    image = Image.new('RGBA', size, NAVY)
    image.alpha_composite(result, ((size[0] - result.width) // 2, (size[1] - result.height) // 2))
    return image


def build_media():
    sources = json.loads((HERE / 'original_art.json').read_text())
    for row in sources:
        source = HERE / row['file']
        if row['id'].startswith('loading_'):
            name = 'ac_anea_' + row['id'].removeprefix('loading_')
            texture(f'gfx/loadingscreens/{name}.dds', contained(source, (1920, 1080)),
                    'original loading-screen illustration', source=source)
            texture(f'gfx/loadingscreens/{name}_small.dds', contained(source, (192, 144)),
                    'loading-screen picker thumbnail', 'GFX_' + name + '_small', source)
        else:
            texture(f'gfx/AC_anea/events/{row["id"]}.dds', contained(source, (200, 160)),
                    'original narrative illustration', 'GFX_ac_anea_event_' + row['id'], source)
            if row['id'] == 'emm_4':
                texture('gfx/AC_anea/news/emm_4.dds', fit_event(source, 'news_event'),
                        'separate news illustration', 'GFX_ac_anea_news_emm_4', source,
                        transform='Full-source Lanczos contain to397x153; opaque navy padding; original country art preserved',
                        packaging_helper='tools/event_picture_fit/fit.py',
                        packaging_helper_sha256=digest((ROOT/'tools/event_picture_fit/fit.py').read_bytes().replace(b'\r\n',b'\n')))
        row['source_sha256'] = digest(source.read_bytes())
        with Image.open(source) as image:
            row['width'], row['height'] = image.size
        row['review'] = 'Visually inspected: no artificial yellow mark, named portrait, legible caption, logo or UI overlay; natural scene lights/rails retained.'
    put('tools/anea/original_art.json', json.dumps(sources, indent=2) + '\n')
    put('mod/2985041246/common/frontend/backgrounds/ac_anea_backgrounds.txt',
        '# Original Anea loading rotation; provenance: tools/anea/original_art.json.\n'
        'ac_anea_emm = {}\nac_anea_eva = {}\n')


def build_cards():
    # Existing flags are presented unchanged; these do not invent people/emblems.
    for tag in ('EMM', 'EVA'):
        flag_path = MOD / 'gfx/flags' / (tag + '.tga')
        with Image.open(flag_path) as original:
            flag = original.convert('RGBA')
        office = Image.new('RGBA', (156, 210), NAVY)
        d = ImageDraw.Draw(office)
        accent = CYAN if tag == 'EMM' else BLUE
        d.rectangle((7, 7, 148, 202), outline=EDGE, width=2)
        d.line((16, 28, 140, 28), fill=accent, width=2)
        d.line((16, 182, 140, 182), fill=accent, width=2)
        flag_fit = ImageOps.contain(flag, (124, 95), Image.Resampling.LANCZOS)
        office.alpha_composite(flag_fit, ((156 - flag_fit.width) // 2, (210 - flag_fit.height) // 2))
        glyph(office, 'assembly', (57, 146, 42, 31), accent)
        texture(f'gfx/AC_anea/cards/{tag}_office.dds', office,
                'national office presentation card; no human identity',
                'GFX_ac_anea_office_' + tag.lower(), flag_path)
        source = HERE / 'sources/events' / (tag.lower() + '_1.png')
        card = contained(source, (200, 160))
        d = ImageDraw.Draw(card)
        d.rectangle((0, 0, 199, 159), outline=accent, width=2)
        d.rectangle((8, 8, 71, 49), fill=NAVY, outline=EDGE, width=1)
        badge = ImageOps.contain(flag, (58, 34), Image.Resampling.LANCZOS)
        card.alpha_composite(badge, (11 + (58 - badge.width) // 2, 11 + (34 - badge.height) // 2))
        texture(f'gfx/AC_anea/cards/{tag}_country.dds', card,
                'country briefing presentation card with established flag',
                'GFX_ac_anea_country_' + tag.lower(), source,
                national_flag=flag_path.relative_to(MOD).as_posix(),
                national_flag_sha256=digest(flag_path.read_bytes()))


def build_gallery():
    cards = []
    for row in json.loads((HERE / 'original_art.json').read_text()):
        path = '../../../tools/anea/' + row['file']
        cards.append('<figure><img src="' + path + '" alt="' + html.escape(row['id']) + '">'
                     '<figcaption>' + html.escape(row['id'].replace('_', ' ')) +
                     ' · Original provisional gameplay illustration</figcaption></figure>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anea artwork review</title><style>body{background:#081621;color:#daedf2;font:16px system-ui;margin:2rem auto;max-width:1250px;padding:0 1rem}h1,h2{color:#5dd0df}p{line-height:1.6}img{max-width:100%;height:auto}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1rem}figure{margin:0;background:#0d202e;padding:.7rem;border:1px solid #2d5568}figcaption{padding:.5rem 0;color:#b5cbd9}a{color:#5dd0df}</style>
<h1>Anea: The Burden of Recovery — original artwork</h1>
<p>108 focus compositions, eight narrative illustrations and two independent loading scenes. Illustrations describe provisional gameplay themes; they do not assert canonical city layouts, named characters or a historical unit roster. Existing national flags remain unchanged. Native rendering acceptance is separate.</p>
<h2>Focus compositions</h2><p>The contact sheet includes review captions; the game icons themselves contain no baked titles or numbers.</p><a href="focus-contact-sheet.png"><img src="focus-contact-sheet.png" alt="108 distinct focus compositions with review captions"></a>
<h2>Original illustration masters</h2><section>''' + ''.join(cards) + '''</section>
<p>Packaging, prompts, source hashes, sprite bindings and transparency metadata: <a href="../../../tools/anea/assets.json">asset manifest</a> · <a href="../../../tools/anea/original_art.json">original prompts and provenance</a> · <a href="../../../tools/anea/focus_art.json">focus art direction</a>.</p></html>'''
    put('docs/evidence/anea/artwork-gallery.html', page + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    build_focuses()
    build_policies()
    build_media()
    build_cards()
    put('mod/2985041246/interface/ac_anea_art.gfx', 'spriteTypes = {\n' + '\n'.join(SPRITES) + '\n}\n')
    put('tools/anea/assets.json', json.dumps(ASSETS, indent=2) + '\n')
    build_gallery()
    changed = []
    for path, data in OUTPUTS.items():
        if args.check:
            current = path.read_bytes() if path.exists() else b''
            if path.suffix == '.png' and current and same_review_png(current, data):
                continue
            # Pillow/zlib releases can encode identical review PNG pixels with
            # different compression streams. Delivered DDS remains byte-exact.
            if path.suffix == '.png' and current:
                with Image.open(io.BytesIO(current)) as actual, Image.open(io.BytesIO(data)) as expected:
                    if actual.size == expected.size and actual.convert('RGBA').tobytes() == expected.convert('RGBA').tobytes():
                        continue
            if path.suffix in ('.txt', '.json', '.gfx', '.html'):
                current = current.replace(b'\r\n', b'\n')
                data = data.replace(b'\r\n', b'\n')
            if current != data:
                changed.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if changed:
        raise SystemExit('Anea artwork output differs: ' + ', '.join(changed))
    print(f'Anea artwork: {len(ASSETS)} textures, {len(SPRITES)} sprite bindings; 108 distinct focus compositions; sources and output {"verified" if args.check else "packaged"}.')


if __name__ == '__main__':
    main()
