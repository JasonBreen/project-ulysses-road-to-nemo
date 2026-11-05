"""Measure every decision-category description with the shipped bitmap font.

Each category's `<id>_desc` is resolved through its [slots]: defined texts
(recursively, cycle-guarded), variables at a representative four-digit width
and scope names at a representative country-name width. Two variants are
measured: every slot at its widest alternative ("longest") and at its
narrowest ("shortest"). Lines wrap at the `full_text` control width read from
interface/countrydecisionview.gui with ACBriefing16 advances and kerning.

Hard failures (a missing glyph, a word wider than the control, a slot that
resolves to nothing) fail --check. A category over the line budget in
contract.json is a finding; it fails --check unless the contract allowlists
it with a reason. Offline measurement only, not a native screenshot.
"""
import argparse
import html
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
OUT = ROOT / 'docs/evidence/decision-text'
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'tools/usea_expansion')]
from script import parse, get, walk  # noqa: E402
from land_program.render_review import Atlas  # noqa: E402
from event_style.review import locs  # noqa: E402
from event_picture_fit.fit import same_review_png  # noqa: E402

VARIABLE = '9999'
SCOPE_NAME = 'Representative Country'
SLOT = re.compile(r'\[([^\[\]]+)\]')
ICON = re.compile(r'£(\w+)£?')


def contract():
    return json.loads((HERE / 'contract.json').read_text())


def control_width(mod=MOD):
    gui = parse((mod / 'interface/countrydecisionview.gui').read_text(encoding='utf-8-sig'))
    window = next(node for _, node in walk(gui) if get(node, 'name', '').strip('"') == 'decision_category_desc')
    full = next(node for _, node in walk([['w', '=', window]]) if get(node, 'name', '').strip('"') == 'full_text')
    icons = [node for _, node in walk([['w', '=', window]]) if get(node, 'name', '').strip('"') == 'custom_icons']
    icon_y = int(get(get(icons[0], 'position'), 'y')) if icons else None
    return int(get(full, 'maxWidth')), int(get(get(full, 'position'), 'y')), get(full, 'font').strip('"'), icon_y


def defined_texts(mod=MOD):
    result = {}
    for folder in ('scripted_localisation', 'custom_localization'):
        for path in sorted((mod / 'common' / folder).glob('*.txt'), key=lambda p: p.as_posix()):
            for kind, _, node in parse(path.read_text(encoding='utf-8-sig')):
                if kind == 'defined_text':
                    result[get(node, 'name').strip('"')] = [get(body, 'localization_key').strip('"')
                                                            for key, _, body in node if key == 'text' and get(body, 'localization_key')]
    return result


def icon_widths(mod=MOD):
    widths = {}
    for path in sorted((mod / 'interface').glob('*.gfx'), key=lambda p: p.as_posix()):
        text = path.read_text(encoding='utf-8-sig', errors='replace')
        for name, texture, frames in re.findall(r'name\s*=\s*"?GFX_(\w+)"?\s*texturefile\s*=\s*"([^"]+)"(?:\s*noOfFrames\s*=\s*(\d+))?', text):
            file = mod / texture
            if file.is_file():
                try:
                    with Image.open(file) as image:
                        widths[name] = image.width // int(frames or 1)
                except OSError:
                    pass
    return widths


class Resolver:
    def __init__(self, mod=MOD):
        self.strings = locs(mod)
        self.defined = defined_texts(mod)
        self.font = Atlas('ACBriefing16')
        self.icons = icon_widths(mod)
        self.problems = []

    def width(self, text):
        text = re.sub(r'§.', '', text)
        total = 0
        for part in re.split(r'(£\w+£?)', text):
            if part.startswith('£'):
                total += self.icons.get(ICON.match(part)[1], 24)
            elif part:
                total += sum(self.font.rows.get(ord(c), {'xadvance': 8})['xadvance'] for c in part if c != '\n')
        return total

    def resolve(self, text, mode, stack=()):
        def slot(match):
            name = match[1]
            if name.startswith('?'):
                return VARIABLE
            if '.' in name:
                return SCOPE_NAME
            if name in stack:
                self.problems.append(('cycle', name))
                return ''
            if name not in self.defined:
                self.problems.append(('unresolved_slot', name))
                return ''
            options = [self.resolve(self.strings.get(key, ''), mode, stack + (name,)) for key in self.defined[name]]
            for key in self.defined[name]:
                if key not in self.strings:
                    self.problems.append(('missing_key', key))
            if not options:
                return ''
            choose = max if mode == 'longest' else min
            return choose(options, key=lambda value: (sum(self.width(line) for line in value.split('\n')), len(value)))
        text = re.sub(r'\$(\w+)\$', lambda m: self.strings.get(m[1], m[0]), text)
        return SLOT.sub(slot, text)

    def lines(self, text, width):
        """Wrapped lines; raises nothing, records missing glyphs and unbreakable words."""
        clean = re.sub(r'§.', '', text)
        missing = sorted({c for c in ICON.sub('', clean) if c != '\n' and ord(c) not in self.font.rows})
        rows, unbreakable = [], []
        for paragraph in clean.split('\n'):
            line = ''
            for word in paragraph.split():
                if self.width(word) > width:
                    unbreakable.append(word)
                candidate = line + ' ' + word if line else word
                if line and self.width(candidate) > width:
                    rows.append(line); line = word
                else:
                    line = candidate
            rows.append(line)
        return rows, missing, unbreakable


def categories(mod=MOD):
    result = []
    for path in sorted((mod / 'common/decisions/categories').glob('*.txt'), key=lambda p: p.as_posix()):
        for kind, _, node in parse(path.read_text(encoding='utf-8-sig')):
            if isinstance(node, list):
                result.append((kind, path.relative_to(mod).as_posix()))
    return result


def measurement(mod=MOD):
    terms = contract()
    width, top, font, icon_y = control_width(mod)
    resolver = Resolver(mod)
    rows = []
    for ident, file in categories(mod):
        key = ident + '_desc'
        if key not in resolver.strings:
            continue
        record = {'category': ident, 'file': file}
        for mode in ('longest', 'shortest'):
            resolver.problems = []
            text = resolver.resolve(resolver.strings[key], mode)
            lines, missing, unbreakable = resolver.lines(text, width)
            record[mode] = {'lines': len(lines), 'height_px': len(lines) * resolver.font.height,
                            'missing_glyphs': missing, 'unbreakable_words': unbreakable,
                            'problems': sorted({'%s:%s' % p for p in resolver.problems})}
            if mode == 'longest':
                record['text_longest'] = '\n'.join(lines)
        allowed = terms['allowlist'].get(ident)
        record['over_budget'] = record['longest']['lines'] > terms['line_budget']
        record['allowlisted'] = allowed
        rows.append(record)
    failures = [r['category'] for r in rows if any(r[m]['missing_glyphs'] or r[m]['unbreakable_words'] or r[m]['problems'] for m in ('longest', 'shortest'))]
    over = [r['category'] for r in rows if r['over_budget'] and not r['allowlisted']]
    stale = sorted(set(terms['allowlist']) - {r['category'] for r in rows if r['over_budget']})
    return {'schema': 1, 'coverage': 'Offline bitmap-font measurement of decision-category descriptions; not native rendering',
            'control': {'width': width, 'text_top': top, 'font': font, 'custom_icons_y': icon_y,
                        'categories_declaring_custom_icons': 0},
            'line_budget': terms['line_budget'], 'categories': len(rows),
            'hard_failures': failures, 'over_budget_not_allowlisted': over, 'stale_allowlist': stale,
            'rows': rows}


def render(data):
    font = Atlas('ACBriefing16')
    chosen = sorted(data['rows'], key=lambda r: (-r['longest']['lines'], r['category']))[:6]
    width = data['control']['width']
    panels = []
    for row in chosen:
        lines = row['text_longest'].split('\n')
        panel = Image.new('RGBA', (width + 40, 44 + len(lines) * font.height + 12), (8, 22, 33, 255))
        draw = ImageDraw.Draw(panel)
        draw.rectangle((0, 0, panel.width - 1, panel.height - 1), outline=(45, 85, 104, 255))
        font.draw(panel, '%s: %d lines (budget %d)' % (row['category'], len(lines), data['line_budget']), 14, 8, width, 24)
        draw.line((14 + width, 36, 14 + width, panel.height - 8), fill=(93, 208, 223, 255))
        y = 40
        for line in lines:
            # Measured lines are drawn unwrapped; a text icon is a cyan box at its frame width.
            cursor = 14
            for part in re.split(r'(£\w+£?)', line):
                if part.startswith('£'):
                    draw.rectangle((cursor, y + 3, cursor + 21, y + 15), outline=(93, 208, 223, 255)); cursor += 24
                    continue
                previous = None
                for char in part:
                    row = font.rows.get(ord(char), font.rows[ord('?')]); cursor += font.kern.get((previous, ord(char)), 0)
                    glyph = font.atlas.crop((row['x'], row['y'], row['x'] + row['width'], row['y'] + row['height']))
                    ink = Image.new('RGBA', glyph.size, (218, 237, 242, 255)); ink.putalpha(glyph.getchannel('A'))
                    panel.alpha_composite(ink, (cursor + row['xoffset'], y + row['yoffset'])); cursor += row['xadvance']; previous = ord(char)
            y += font.height
        panels.append(panel)
    sheet = Image.new('RGBA', (width + 40, sum(p.height + 12 for p in panels) + 12), (6, 17, 26, 255))
    y = 12
    for panel in panels:
        sheet.alpha_composite(panel, (0, y)); y += panel.height + 12
    buffer = io.BytesIO(); sheet.save(buffer, 'PNG', optimize=True)
    return buffer.getvalue()


def page(data):
    rows = ''.join('<tr%s><td><code>%s</code></td><td>%s</td><td>%d</td><td>%d</td><td>%s</td></tr>\n' % (
        ' class="over"' if r['over_budget'] else '', html.escape(r['category']), html.escape(r['file']),
        r['longest']['lines'], r['shortest']['lines'], html.escape(r['allowlisted'] or ''))
        for r in sorted(data['rows'], key=lambda r: (-r['longest']['lines'], r['category'])))
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>Decision category text</title>\n'
            '<style>body{background:#081621;color:#daedf2;font-family:sans-serif;margin:16px}td,th{border:1px solid #2d5568;padding:4px 8px}'
            'table{border-collapse:collapse}.over{color:#e0a060}img{max-width:100%%;border:1px solid #2d5568}</style></head><body>\n'
            '<h1>Decision-category descriptions (offline measurement)</h1>\n'
            '<p>Width %d px, ACBriefing16, budget %d lines. Longest and shortest resolved variants. Not native rendering evidence.</p>\n'
            '<table><tr><th>Category</th><th>File</th><th>Longest lines</th><th>Shortest lines</th><th>Allowlist reason</th></tr>\n%s</table>\n'
            '<h2>The six longest categories</h2><img src="categories-longest.png" alt="Longest category descriptions">\n</body></html>\n'
            % (data['control']['width'], data['line_budget'], rows))


def outputs(mod=MOD):
    data = measurement(mod)
    return data, {'measurements.json': (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode(),
                  'index.html': page(data).encode(), 'categories-longest.png': render(data)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, files = outputs()
    stale = []
    for name, payload in files.items():
        target = OUT / name
        if args.check:
            old = target.read_bytes() if target.exists() else b''
            if not (same_review_png(old, payload) if name.endswith('.png') else old.replace(b'\r\n', b'\n') == payload):
                stale.append(name)
        else:
            OUT.mkdir(parents=True, exist_ok=True); target.write_bytes(payload)
    longest = max(data['rows'], key=lambda r: r['longest']['lines'])
    print('Decision categories: %d measured; longest %s at %d lines; %d over budget (%d allowlisted); %d hard failures' % (
        data['categories'], longest['category'], longest['longest']['lines'],
        sum(r['over_budget'] for r in data['rows']), sum(bool(r['over_budget'] and r['allowlisted']) for r in data['rows']),
        len(data['hard_failures'])))
    problems = []
    if stale:
        problems.append('stale review: ' + ', '.join(stale))
    if data['hard_failures']:
        problems.append('hard failures: ' + ', '.join(data['hard_failures']))
    if data['over_budget_not_allowlisted']:
        problems.append('over budget: ' + ', '.join(data['over_budget_not_allowlisted']))
    if data['stale_allowlist']:
        problems.append('allowlisted but within budget: ' + ', '.join(data['stale_allowlist']))
    if problems:
        raise SystemExit('Decision text: ' + '; '.join(problems))


if __name__ == '__main__':
    main()
