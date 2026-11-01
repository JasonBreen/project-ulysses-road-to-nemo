"""Measure authored glyph alpha, including side bearings, without native claims."""
from __future__ import annotations


def glyph_ink(font, ident):
    row = font.rows[ident]
    alpha = font.atlas.crop((row['x'], row['y'], row['x'] + row['width'],
                            row['y'] + row['height'])).getchannel('A')
    box = alpha.getbbox()
    if box is None:
        return None
    return [box[0] + row['xoffset'], box[1] + row['yoffset'],
            box[2] + row['xoffset'], box[3] + row['yoffset']]


def envelope(font):
    rows = [dict(id=ident, character=chr(ident), ink=glyph_ink(font, ident),
                 advance=row['xadvance']) for ident, row in sorted(font.rows.items())]
    visible = [row for row in rows if row['ink'] is not None]
    return dict(glyph_count=len(rows), visible_glyphs=len(visible),
                ink_top=min(row['ink'][1] for row in visible),
                ink_bottom=max(row['ink'][3] for row in visible),
                left_overhangs=[row for row in visible if row['ink'][0] < 0],
                right_overhangs=[row for row in visible if row['ink'][2] > row['advance']],
                glyphs=rows)


def text_ink(font, lines):
    bounds = []
    for number, line in enumerate(lines):
        cursor = 0
        previous = None
        for char in line:
            ident = ord(char)
            row = font.rows[ident]
            cursor += font.kern.get((previous, ident), 0)
            box = glyph_ink(font, ident)
            if box:
                bounds.append([cursor + box[0], number * font.height + box[1],
                               cursor + box[2], number * font.height + box[3]])
            cursor += row['xadvance']
            previous = ident
    if not bounds:
        return None
    return [min(b[0] for b in bounds), min(b[1] for b in bounds),
            max(b[2] for b in bounds), max(b[3] for b in bounds)]


def fits(box, width, height):
    return box is None or (0 <= box[0] and 0 <= box[1] and
                           box[2] <= width and box[3] <= height)
