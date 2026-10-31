"""Reconstruct the shipped macro GUI offline, using its own sprites/font atlas.

This is review evidence, never a replacement product GUI or native screenshot.
It executes the actual shipped fiscal effects through the bounded Decimal
interpreter, persists twelve settlements, and evaluates actual GUI conditions.
Native text rasterization, engine rounding, input and scaling remain untested.
"""
import argparse
import copy
from datetime import date
from decimal import Decimal as D, ROUND_HALF_UP
import hashlib
import html
import json
from pathlib import Path
import re
import sys

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
EVIDENCE = ROOT / 'docs/evidence/economy-v2'
sys.path.insert(0, str(ROOT / 'tools'))
from economy_script import parse, fields
from harness import World as FiscalWorld

PAGES = ('Overview', 'Budget', 'Industry', 'Debt', 'Ledger')
WHITE = (218, 237, 242, 255)
NAVY = (8, 22, 33, 255)
CYAN = (93, 208, 223, 255)


def first(nodes, name, default=None):
    return next((v for k, _, v in nodes if k == name), default)


def sha(path):
    data = path.read_bytes()
    if path.suffix.lower() in ('.txt', '.gui', '.gfx', '.yml', '.json', '.fnt', '.py'):
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


class AtlasFont:
    """Use delivered BMFont positions, offsets, alpha and advances unchanged."""
    def __init__(self, name):
        self.name = name
        definitions = first(parse((MOD / 'interface/ac_expansion_fonts.gfx').read_text()), 'bitmapfonts')
        definition = next(fields(body) for kind, _, body in definitions
                          if kind == 'bitmapfont' and first(body, 'name') == name)
        base = MOD / definition['path']
        value = int(definition['color'], 16)
        self.color = ((value >> 16) & 255, (value >> 8) & 255, value & 255, (value >> 24) & 255)
        self.source = base.with_suffix('.fnt')
        self.texture = base.with_suffix('.dds')
        text = self.source.read_text()
        self.line_height = int(re.search(r'lineHeight=(\d+)', text)[1])
        self.glyphs = {}
        for line in text.splitlines():
            if line.startswith('char '):
                row = {k: int(v) for k, v in re.findall(r'(\w+)=(-?\d+)', line)}
                self.glyphs[chr(row['id'])] = row
        self.atlas = Image.open(self.texture).convert('RGBA')
        self.missing = set()

    def glyph(self, char):
        if char not in self.glyphs:
            self.missing.add(char)
        return self.glyphs.get(char, self.glyphs['?'])

    def width(self, text):
        return sum(self.glyph(c)['xadvance'] for c in text)

    def lines(self, text, width):
        result = []
        for paragraph in text.replace('\\n', '\n').split('\n'):
            line = ''
            for word in paragraph.split(' '):
                candidate = line + (' ' if line else '') + word
                if line and self.width(candidate) > width:
                    result.append(line)
                    line = word
                else:
                    line = candidate
            result.append(line)
        return result

    def draw(self, image, text, x, y, width, height, align='left', color=None):
        color = self.color if color is None else color
        lines = self.lines(text, width)
        layer = Image.new('RGBA', (width, max(height, len(lines) * self.line_height + 5)))
        ink_bounds = None
        for index, line in enumerate(lines):
            pen = (width - self.width(line)) // 2 if align == 'center' else 0
            for char in line:
                g = self.glyph(char)
                tile = self.atlas.crop((g['x'], g['y'], g['x'] + g['width'], g['y'] + g['height']))
                tinted = Image.new('RGBA', tile.size, color)
                tinted.putalpha(ImageChops.multiply(tile.getchannel('A'), tinted.getchannel('A')))
                layer.alpha_composite(tinted, (pen + g['xoffset'], index * self.line_height + g['yoffset']))
                pen += g['xadvance']
        ink_bounds = layer.getbbox()
        image.alpha_composite(layer.crop((0, 0, width, height)), (x, y))
        return dict(lines=lines, line_height=self.line_height, required_height=len(lines) * self.line_height,
                    ink_bounds=ink_bounds, clipped=bool(ink_bounds and ink_bounds[3] > height),
                    horizontal_overflow=any(self.width(line) > width for line in lines))


def localization():
    text = (MOD / 'localisation/english/ac_macro_l_english.yml').read_text(encoding='utf-8-sig')
    return {m[1]: json.loads(m[2]) for m in re.finditer(r'^\s+(\w+):\d*\s+(".*")\s*$', text, re.M)}


def substitute(text, country):
    def replace(match):
        name, spec = match.groups()
        if name not in country.variables:
            raise ValueError('Unresolved GUI variable ' + name)
        value = country.variables[name]
        percent = spec.startswith('%')
        precision = int(spec[1:])
        if percent:
            value *= 100
        value = value.quantize(D(1).scaleb(-precision), rounding=ROUND_HALF_UP)
        return format(value, '.' + str(precision) + 'f') + ('%' if percent else '')
    return re.sub(r'\[\?(\w+)\|([.%]\d+)\]', replace, text)


def sample():
    """Explicit illustrative observations; all financial calculations stay owned."""
    world = FiscalWorld()
    country = world.countries['EMM']
    observations = dict(num_of_controlled_factories=44, num_of_civilian_factories=24,
                        num_of_military_factories=14, num_of_naval_factories=6,
                        deployed_army_manpower_k=90, deployed_navy_manpower_k=8,
                        deployed_airforce_manpower_k=12, num_deployed_planes=72,
                        num_ships=10, total_equipment_produced_infantry=135)
    country.observables.update(observations)
    world.action('on_startup')
    world.run('ac_macro_preset_development', 'EMM')
    snapshots = []
    for i in range(12):
        year, month = 1991 + (i + 1) // 12, (i + 1) % 12 + 1
        world.month('EMM', year, month)
        snapshots.append(dict(date=date(year, month, 1).isoformat(), variables=copy.deepcopy(country.variables)))
        if i == 5:
            # Offline copied-state reload; not HOI4 serialization evidence.
            world = copy.deepcopy(world)
            country = world.countries['EMM']
            world.action('on_startup')
    world.run('ac_macro_fund_replacements', 'EMM')
    country.variables['project_ulysses_economy_screen_open'] = D(1)
    assert country.variables['ac_macro_history_count'] == 12
    assert country.variables['ac_macro_settlements'] == 12
    return world, country, dict(tag='EMM', date=date.fromordinal(world.today).isoformat(),
        provenance='Illustrative offline World observations; not a natural campaign or claimed starting OOB.',
        observations=observations, actions=['on_startup', 'ac_macro_preset_development',
        '12 monthly callbacks February1991–January1992', 'copied-state startup after sixth month',
        'ac_macro_fund_replacements'], monthly_snapshots=snapshots, final_variables=country.variables,
        flags=country.flags)


class Review:
    def __init__(self):
        self.inputs = []
        self.gui_path = MOD / 'interface/ac_macro_economy.gui'
        self.logic_path = MOD / 'common/scripted_guis/ac_macro_economy.txt'
        tree = parse(self.gui_path.read_text())
        self.window = first(first(tree, 'guiTypes'), 'containerWindowType')
        self.size = fields(first(self.window, 'size'))
        self.width, self.height = int(self.size['width']), int(self.size['height'])
        logic = first(first(parse(self.logic_path.read_text()), 'scripted_gui'), 'ac_macro_economy_screen')
        self.visible = first(logic, 'visible')
        self.triggers = fields(first(logic, 'triggers'))
        self.properties = fields(first(logic, 'properties'))
        self.loc = localization()
        self.fonts = {name: AtlasFont(name) for name in ('ACBriefing16', 'ACBriefing20')}
        self.sprites = {}
        gfx_path = MOD / 'interface/ac_macro_economy.gfx'
        for kind, _, body in first(parse(gfx_path.read_text()), 'spriteTypes'):
            if kind != 'spriteType':
                raise ValueError('Unsupported sprite control ' + kind)
            values = fields(body)
            texture = MOD / values['texturefile']
            image = Image.open(texture).convert('RGBA')
            count = int(values.get('noOfFrames', 1))
            if image.width % count:
                raise ValueError('Invalid frame dimensions ' + values['name'])
            self.sprites[values['name']] = dict(image=image, count=count, width=image.width // count,
                                               height=image.height, texture=texture)
            self.inputs.append(texture)
        self.inputs += [self.gui_path, self.logic_path, gfx_path,
            MOD / 'localisation/english/ac_macro_l_english.yml',
            MOD / 'interface/ac_expansion_fonts.gfx', HERE / 'profiles.json']
        self.inputs += [p for font in self.fonts.values() for p in (font.source, font.texture)]
        self.inputs += list((MOD / 'common/scripted_effects').glob('ac_macro*.txt'))
        self.inputs += list((MOD / 'common/scripted_triggers').glob('ac_macro*.txt'))
        self.inputs.append(MOD / 'common/on_actions/ac_macro_on_actions.txt')

    def tile(self, name, frame=1):
        row = self.sprites[name]
        if frame < 1 or frame > row['count']:
            raise ValueError('Frame outside actual quad metadata: ' + name + ':' + str(frame))
        return row['image'].crop(((frame-1)*row['width'], 0, frame*row['width'], row['height']))

    def page(self, world, country, page):
        country.variables['ac_macro_ui_page'] = D(page)
        if not world.trigger(self.visible, country):
            raise ValueError('Actual screen visibility rejected the fixture')
        background = fields(first(self.window, 'background'))
        canvas = self.tile(background['quadTextureSprite']).copy()
        records = []
        for kind, _, body in self.window:
            if kind not in ('instantTextboxType', 'buttonType', 'iconType'):
                continue
            row = fields(body)
            name = row['name']
            condition = self.triggers.get(name + '_visible')
            if condition is not None and not world.trigger(condition, country):
                continue
            position = fields(row['position'])
            x, y = int(position['x']), int(position['y'])
            record = dict(name=name, kind=kind, x=x, y=y)
            if kind == 'instantTextboxType':
                width, height = int(row['maxWidth']), int(row['maxHeight'])
                text = substitute(self.loc[row['text']], country)
                record.update(text=text, localization=row['text'], width=width, height=height,
                    **self.fonts[row['font']].draw(canvas, text, x, y, width, height, row.get('format', 'left')))
            else:
                sprite = row['quadTextureSprite'] if kind == 'buttonType' else row['spriteType']
                enabled = world.trigger(self.triggers[name + '_click_enabled'], country) if kind == 'buttonType' else True
                frame = 1
                if kind == 'iconType' and name in self.properties:
                    variable = fields(self.properties[name])['frame']
                    frame = int(country.variables[variable])
                elif not enabled:
                    # The delivered four-frame quad convention; native state mapping remains untested.
                    frame = 4
                image = self.tile(sprite, frame)
                canvas.alpha_composite(image, (x, y))
                width, height = image.size
                record.update(sprite=sprite, frame=frame, frame_count=self.sprites[sprite]['count'],
                              enabled=enabled, width=width, height=height)
                if kind == 'buttonType':
                    font = self.fonts[row['buttonFont']]
                    text = substitute(self.loc[row['buttonText']], country)
                    th = font.line_height
                    record.update(text=text, localization=row['buttonText'], **font.draw(canvas, text, x,
                                  y+(height-th)//2, width, th, 'center'))
            record['outside_window'] = x < 0 or y < 0 or x + record['width'] > self.width or y + record['height'] > self.height
            records.append(record)
        labelled = Image.new('RGBA', (self.width, self.height + 64), NAVY)
        self.fonts['ACBriefing16'].draw(labelled, 'OFFLINE RECONSTRUCTION | '+PAGES[page]+' | synthetic EMM fixture, January1992', 16, 5, 828, 22, color=CYAN)
        self.fonts['ACBriefing16'].draw(labelled, 'Actual shipped GUI coordinates, DDS sprites and font atlas. Native rendering/input remain untested.', 16, 27, 828, 30)
        labelled.alpha_composite(canvas, (0, 64))
        return labelled, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify reconstructed evidence without rewriting it')
    args = parser.parse_args()
    review = Review()
    world, country, fixture = sample()
    outputs, pages = {}, []
    for index, title in enumerate(PAGES):
        image, controls = review.page(world, country, index)
        name = 'ui-review-' + title.lower() + '.png'
        outputs[name] = image
        pages.append(dict(page=title, image=name, controls=controls))
    issues = [dict(page=page['page'], control=row['name'], clipped=row.get('clipped', False),
                   horizontal_overflow=row.get('horizontal_overflow', False), outside_window=row['outside_window'],
                   text=row.get('text', ''), box=[row['x'],row['y'],row['width'],row['height']],
                   required_height=row.get('required_height'))
              for page in pages for row in page['controls']
              if row.get('clipped') or row.get('horizontal_overflow') or row['outside_window']]
    report = dict(status='OFFLINE reconstruction; not native acceptance',
        method='Actual shipped positions, localization, BMFont atlas and sprite metadata; actual-script Decimal World with12 settled months.',
        input_hash_convention='SHA256; CRLF normalized to LF for text inputs, binary DDS hashed unchanged.',
        limitations=['Word wrapping models glyph advances; native line breaking and rasterization remain untested.',
                     'Four-frame buttons use normal frame1 and disabled frame4; native state mapping remains untested.',
                     'Synthetic observer values and copied-state reload do not establish natural progression or HOI4 serialization.',
                     'Window rendered at1.0; drag, input, tooltips, viewport scaling and native performance are untested.'],
        inputs=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha(p)) for p in sorted(set(review.inputs))],
        fixture=fixture, issues=issues, missing_font_glyphs={name: sorted(font.missing) for name,font in review.fonts.items()}, pages=pages)
    report_text = json.dumps(report, indent=2, default=str) + '\n'
    images = ''.join('<figure><h2>'+p['page']+'</h2><img src="'+p['image']+'" alt="Offline '+p['page']+' reconstruction at shipped GUI dimensions"></figure>' for p in pages)
    issue_text = '<p>No clipped text or out-of-window control bounds found in this fixture.</p>' if not issues else '<ul>'+''.join('<li>'+html.escape(r['page']+' / '+r['control']+': '+str(r))+'</li>' for r in issues)+'</ul>'
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><title>Offline fiscal GUI review</title><style>body{background:#081621;color:#daedf2;font:16px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem}a,h1,h2{color:#5dd0df}p,li{line-height:1.6}figure{margin:2rem 0}img{max-width:100%;height:auto;border:1px solid #345262}code{overflow-wrap:anywhere}</style><h1>OFFLINE fiscal GUI reconstruction</h1><p>These review artifacts reconstruct the actual shipped860×700 GUI with delivered DDS sprites, font atlas, localization, variable bindings and visibility conditions. They are not game screenshots or a substitute product interface. The illustrative EMM fixture executes twelve actual-script monthly settlements, February1991–January1992, and retains all values in <a href="ui-review-report.json">the audit record</a>.</p><p>Native input, scaling, line breaking, tooltips and save serialization remain untested. Financial values are fictional gameplay calibration, not canonical national accounts.</p><h2>Bounds findings</h2>'+issue_text+images+'</html>\n'
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    for name,image in outputs.items():
        target = EVIDENCE/name
        if args.check:
            with Image.open(target) as old:
                assert old.size == image.size and old.convert('RGBA').tobytes() == image.tobytes(), name
        else:
            image.save(target)
    for name,text in [('ui-review-report.json',report_text),('ui-review.html',page)]:
        target=EVIDENCE/name
        if args.check:
            assert target.read_text(encoding='utf-8') == text, name
        else:
            target.write_text(text, encoding='utf-8')
    if any(report['missing_font_glyphs'].values()):
        raise SystemExit('Missing glyphs: '+str(report['missing_font_glyphs']))
    print('OFFLINE reconstruction:5 pages;12 settled months;',len(issues),'bounds/text findings; native untested')
    for row in issues:
        print(row['page'],row['control'],row['box'],'required_height',row['required_height'])
    if issues:
        raise SystemExit('Offline bounds/text review failed; inspect ui-review-report.json')


if __name__ == '__main__':
    main()
