"""Review evidence for bespoke trees: a rendered tree image and a content page per country.

    python -B tools/national_depth/review.py           # write docs/evidence/national-depth/
    python -B tools/national_depth/review.py --check   # compare (PNG by decoded pixels)

The image draws every node at half the in-game pitch with its real compiled
icon and the title in the shipped ACBriefing16 bitmap font, prerequisite lines,
branch lanes, the shared institutional block and the continuous-focus panel.
It is an offline review aid, not an engine screenshot.
"""
import argparse
import html
import io
from pathlib import Path
import re
import sys

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
OUT = ROOT / 'docs/evidence/national-depth'
sys.path[:0] = [str(HERE), str(ROOT / 'tools/usea_expansion')]
import art  # noqa: E402
from compile import compile_country, institutional_block, names  # noqa: E402
import package  # noqa: E402

NAVY = (8, 22, 33, 255)
WHITE = (218, 237, 242, 255)
DIM = (20, 44, 58, 255)
EDGE = (45, 85, 104, 255)
CYAN = (93, 208, 223, 255)
PITCH = (48, 80)          # half of the in-game 96 x 160


def atlas_font():
    text = (MOD / 'gfx/fonts/ACBriefing16.fnt').read_text()
    metrics = {int(v['id']): {k: int(x) for k, x in v.items()} for line in text.splitlines() if line.startswith('char id=')
               for v in [dict(re.findall(r'(\w+)=(-?\d+)', line))]}
    return metrics, Image.open(MOD / 'gfx/fonts/ACBriefing16.dds').convert('RGBA')


def write(canvas, font, x, y, text, colour=WHITE):
    metrics, atlas = font
    for char in text:
        m = metrics.get(ord(char), metrics[ord('?')])
        glyph = atlas.crop((m['x'], m['y'], m['x'] + m['width'], m['y'] + m['height']))
        if colour != WHITE:
            tint = Image.new('RGBA', glyph.size, colour)
            tint.putalpha(glyph.getchannel('A'))
            glyph = tint
        canvas.alpha_composite(glyph, (x + m['xoffset'], y + m['yoffset']))
        x += m['xadvance']


def width(font, text):
    return sum(font[0].get(ord(c), font[0][ord('?')])['xadvance'] for c in text)


def wrap(font, text, limit=92, lines=2):
    out, line = [], ''
    for word in text.split():
        trial = (line + ' ' + word).strip()
        if width(font, trial) <= limit:
            line = trial
        else:
            out.append(line)
            line = word
    out.append(line)
    if len(out) > lines:
        out = out[:lines]
        out[-1] = out[-1][:-1] + '.'
    return out


def tree_image(module, outputs, budget, positions, font):
    c = module.COUNTRY
    n = names(c)
    ids, block = institutional_block()
    own = {n['infix'] and '%s_%s_%s' % (c.tag, n['infix'], k): v for k, v in positions.items()}
    every = dict(block)
    every.update(own)
    max_x = max(x for x, _ in every.values())
    max_y = max(y for _, y in every.values())
    panel_x, panel_y = budget['panel']
    w = max(int((max_x + 3) * PITCH[0]), panel_x // 2 + 400)
    h = int((max_y + 2) * PITCH[1])
    canvas = Image.new('RGBA', (w + 120, h + 60), NAVY)
    draw = ImageDraw.Draw(canvas)

    def at(x, y):
        return int(60 + x * PITCH[0] + PITCH[0] / 2), int(40 + y * PITCH[1])
    write(canvas, font, 20, 10, '%s: %s own focuses + %d shared institutional (%d total)' % (
        c.name, budget['own_focuses'], budget['shared_focuses'], budget['total']))
    draw.rectangle((60 + panel_x // 2, 40 + panel_y // 2, 60 + panel_x // 2 + 385, 40 + panel_y // 2 + 228), outline=CYAN, width=2)
    write(canvas, font, 68 + panel_x // 2, 48 + panel_y // 2, 'Continuous focus panel', CYAN)
    by_key = {f.key: f for b in module.BRANCHES for f in b.focuses}
    for key, f in by_key.items():
        for parent in (*f.after, *f.after_any):
            draw.line((*at(*positions[parent]), *at(*positions[key])), fill=EDGE, width=2)
    for ident, (x, y) in block.items():
        cx, cy = at(x, y)
        draw.rounded_rectangle((cx - 20, cy, cx + 20, cy + 34), radius=6, fill=DIM, outline=EDGE)
    write(canvas, font, 64, int(40 + 11 * PITCH[1]) - 30, 'Shared institutional programme (36 focuses, rows 0-10)', EDGE)
    for b in module.BRANCHES:
        keys = [f.key for f in b.focuses]
        xs = [positions[k][0] for k in keys]
        ys = [positions[k][1] for k in keys]
        x0, y0 = at(min(xs), min(ys))
        x1, y1 = at(max(xs), max(ys))
        draw.rectangle((x0 - 30, y0 - 18, x1 + 30, y1 + 66), outline=EDGE)
        write(canvas, font, x0 - 26, y0 - 16, b.title[:28] + ' (%d)' % b.era, CYAN)
    for key, f in by_key.items():
        ident = '%s_%s_%s' % (c.tag, n['infix'], key)
        cx, cy = at(*positions[key])
        icon = Image.open(io.BytesIO(outputs['%s/focus/%s.dds' % (n['gfx'], ident)])).convert('RGBA').resize((40, 40))
        canvas.alpha_composite(icon, (cx - 20, cy))
        for i, line in enumerate(wrap(font, f.title)):
            write(canvas, font, cx - width(font, line) // 2, cy + 42 + 15 * i, line)
    return canvas


def page(rows):
    parts = ['<!doctype html><meta charset="utf-8"><title>National depth review</title>',
             '<style>body{font:14px system-ui;background:#081621;color:#dae;max-width:1100px;margin:auto}table{border-collapse:collapse}'
             'td,th{border:1px solid #2d5568;padding:4px 8px;text-align:left}img{max-width:100%}h2{color:#5dd0df}</style>',
             '<h1>National depth: bespoke trees for review</h1><p>Offline evidence; not an engine screenshot. Native untested (#8).</p>']
    for module, budget in rows:
        c = module.COUNTRY
        parts.append('<h2>%s (%s)</h2><p>%d own focuses, %d branches, %d shared institutional focuses, %d events, %d ideas, %d offices.</p>' % (
            html.escape(c.name), c.tag, budget['own_focuses'], len(module.BRANCHES), budget['shared_focuses'], budget['events'],
            budget['ideas'], budget['offices']))
        parts.append('<img src="%s.png" alt="%s tree">' % (c.tag.lower(), html.escape(c.name)))
        parts.append('<table><tr><th>Branch</th><th>Era</th><th>Focuses</th><th>Filter</th></tr>' + ''.join(
            '<tr><td>%s</td><td>%d</td><td>%d</td><td>%s</td></tr>' % (html.escape(b.title), b.era, len(b.focuses), b.filter)
            for b in module.BRANCHES) + '</table>')
        if module.OFFICES:
            parts.append('<p>Offices: ' + '; '.join('%s (%s / %s)' % (html.escape(o.title), o.party, o.ideology) for o in module.OFFICES) + '</p>')
        parts.append('<h3>Sample focuses</h3><dl>' + ''.join(
            '<dt>%s</dt><dd>%s</dd>' % (html.escape(b.focuses[0].title), html.escape(b.focuses[0].desc)) for b in module.BRANCHES) + '</dl>')
        if module.EVENTS:
            e = module.EVENTS[0]
            parts.append('<h3>Sample event: %s</h3>' % html.escape(e.title) + ''.join('<p>%s</p>' % html.escape(p) for p in e.paragraphs))
            parts.append('<p>Events: ' + '; '.join(html.escape(e.title) for e in module.EVENTS) + '</p>')
        parts.append('<p>Sources: ' + '; '.join('%s: %s' % (s.layer, html.escape(s.note)) for s in module.SOURCES) + '</p>')
    return '\n'.join(parts) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    art.require_pinned_pillow()
    font = atlas_font()
    rows, files = [], {}
    for path in package.discover():
        module = package.load(path)
        outputs, budget, _, positions = compile_country(module)
        image = tree_image(module, outputs, budget, positions, font)
        files['%s.png' % module.COUNTRY.tag.lower()] = art.encoded(image, 'PNG')
        rows.append((module, budget))
    files['index.html'] = page(rows).encode('utf-8')
    stale = []
    for name, data in files.items():
        target = OUT / name
        if args.check:
            if not target.exists():
                stale.append(name)
            elif name.endswith('.png'):
                if not art.same_pixels(target.read_bytes(), data):
                    stale.append(name)
            elif target.read_bytes().replace(b'\r\n', b'\n') != data:
                stale.append(name)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    if stale:
        raise SystemExit('Stale national-depth review: ' + ', '.join(stale))
    print('National depth review: %d trees %s' % (len(rows), 'consistent' if args.check else 'written'))


if __name__ == '__main__':
    main()
