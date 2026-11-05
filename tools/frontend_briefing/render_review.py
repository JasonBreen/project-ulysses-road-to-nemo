"""Offline review of the lobby restyle: each replacement tile stretched to the
size of a control that uses it, by the corneredTileSpriteType nine-slice rule,
and the disposition of every engine sprite on the screen.

Not a native screenshot: the engine's own stretching, the hidden decorations
and the kept engine controls are confirmed only in a native session (#8).
--check compares index.html byte for byte and the PNG by size and RGBA.
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
OUT = ROOT / 'docs/evidence/frontend-briefing'
sys.path[:0] = [str(ROOT / 'tools'), str(HERE)]
from land_program.render_review import Atlas  # noqa: E402
from event_picture_fit.fit import same_review_png  # noqa: E402
from validate import sprite_blocks  # noqa: E402

# A control that uses each restyled tile, at its size in frontendgamesetupview.gui
# (percent widths drawn at a representative 1200 px).
SAMPLES = [
    ('GFX_ac_briefing_lobby_upper_bar', 'top bar (102% x 128)', 1200, 128),
    ('GFX_ac_briefing_lobby_lower_bar', 'bottom bar (102% x 128)', 1200, 128),
    ('GFX_ac_briefing_lobby_window', 'random-country window (500 x 400)', 500, 400),
    ('GFX_ac_briefing_lobby_thin_window', 'game-rule dropdown (300 x 300)', 300, 300),
    ('GFX_ac_briefing_lobby_list', 'load list (350 x 415)', 350, 415),
    ('GFX_ac_briefing_lobby_header', 'setting group header (630 x 40)', 630, 40),
    ('GFX_ac_briefing_lobby_row', 'difficulty row (630 x 40)', 630, 40),
    ('GFX_ac_briefing_lobby_settings_bg', 'multiplayer settings (484 x 97)', 484, 97),
]
BACK = (6, 17, 26, 255)
WHITE = (218, 237, 242, 255)


def tiles():
    gfx = (MOD / 'interface/ac_frontend_briefing.gfx').read_text()
    result = {}
    for kind, raw in sprite_blocks(gfx):
        if kind != 'corneredTileSpriteType':
            continue
        name = re.search(r'name\s*=\s*"([^"]+)"', raw)[1]
        texture = re.search(r'texturefile\s*=\s*"([^"]+)"', raw)[1]
        border = re.search(r'borderSize\s*=\s*\{\s*x\s*=\s*(\d+)\s*y\s*=\s*(\d+)', raw)
        result[name] = (texture, int(border[1]), int(border[2]))
    return result


def nine_slice(source, width, height, bx, by):
    out = Image.new('RGBA', (width, height))
    sw, sh = source.size
    xs = [(0, bx, 0, bx), (bx, sw - bx, bx, width - bx), (sw - bx, sw, width - bx, width)]
    ys = [(0, by, 0, by), (by, sh - by, by, height - by), (sh - by, sh, height - by, height)]
    for sx0, sx1, dx0, dx1 in xs:
        for sy0, sy1, dy0, dy1 in ys:
            if dx1 > dx0 and dy1 > dy0 and sx1 > sx0 and sy1 > sy0:
                piece = source.crop((sx0, sy0, sx1, sy1)).resize((dx1 - dx0, dy1 - dy0), Image.Resampling.NEAREST)
                out.alpha_composite(piece, (dx0, dy0))
    return out


def composite():
    font = Atlas('ACBriefing16')
    found = tiles()
    canvas = Image.new('RGBA', (1240, 1500), BACK)
    font.draw(canvas, 'OFFLINE LOBBY RESTYLE REVIEW / nine-slice at control sizes / not a native screenshot', 20, 10, 1200, 24)
    y = 44
    row_x = 20; row_bottom = y
    for name, label, width, height in SAMPLES:
        texture, bx, by = found[name]
        with Image.open(MOD / texture) as image:
            drawn = nine_slice(image.convert('RGBA'), width, height, bx, by)
        text = name.removeprefix('GFX_ac_briefing_') + ': ' + label
        span = max(width, font.measure(text))
        if row_x + span > 1220:
            row_x = 20; y = row_bottom + 12
        font.draw(canvas, text, row_x, y, span + 8, 20)
        canvas.alpha_composite(drawn, (row_x, y + 24))
        row_bottom = max(row_bottom, y + 24 + height)
        row_x += span + 24
    canvas = canvas.crop((0, 0, 1240, row_bottom + 20))
    buffer = io.BytesIO(); canvas.save(buffer, 'PNG', optimize=True)
    return buffer.getvalue()


def page():
    record = json.loads((HERE / 'lobby_sprites.json').read_text())
    counts = {kind: sum(r['disposition'] == kind for r in record['sprites']) for kind in ('restyle', 'hide', 'keep_engine')}
    rows = ''.join('<tr class="%s"><td><code>%s</code></td><td>%s</td><td><code>%s</code></td><td>%s</td></tr>\n' % (
        r['disposition'], html.escape(r['sprite']), r['disposition'], html.escape(r.get('replacement', '')), html.escape(r['reason']))
        for r in sorted(record['sprites'], key=lambda r: (r['disposition'] != 'restyle', r['disposition'] != 'hide', r['sprite'])))
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>Lobby restyle</title>\n'
            '<style>body{background:#081621;color:#daedf2;font-family:sans-serif;margin:16px}td,th{border:1px solid #2d5568;padding:4px 8px}'
            'table{border-collapse:collapse}.restyle td:nth-child(2){color:#5dd0df}.hide td:nth-child(2){color:#e6b55f}'
            'img{max-width:100%%;border:1px solid #2d5568}</style></head><body>\n'
            '<h1>Country-selection lobby: engine sprites (offline review)</h1>\n'
            '<p>%s</p>\n<p>%d restyled, %d hidden, %d kept on the engine. Not native rendering evidence.</p>\n'
            '<img src="lobby-composite.png" alt="Restyled lobby tiles at control sizes">\n'
            '<table><tr><th>Engine sprite</th><th>Disposition</th><th>Replacement</th><th>Reason</th></tr>\n%s</table>\n</body></html>\n'
            % (html.escape(record['decision']), counts['restyle'], counts['hide'], counts['keep_engine'], rows))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = {'lobby-composite.png': composite(), 'index.html': page().encode()}
    stale = []
    for name, data in files.items():
        target = OUT / name
        if args.check:
            old = target.read_bytes() if target.exists() else b''
            if not (same_review_png(old, data) if name.endswith('.png') else old.replace(b'\r\n', b'\n') == data):
                stale.append(name)
        else:
            OUT.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    if stale:
        raise SystemExit('Stale lobby review: ' + ', '.join(stale))
    print('Lobby review: %d tiles %s' % (len(SAMPLES), 'consistent' if args.check else 'written'))


if __name__ == '__main__':
    main()
