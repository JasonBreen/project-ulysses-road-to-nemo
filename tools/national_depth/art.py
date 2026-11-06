"""Procedural, mod-only artwork for bespoke trees: one unique icon per focus.

Every image is drawn with the shared Ulysses glyph library (tools/usea_depth/seams.py
glyph_library()) on a navy frame whose outline and accent are derived from the
country tag, so each country's icons are recognisably its own. A focus icon is
the frame plus a primary and a secondary glyph in one of six arrangements; the
compiler picks an arrangement so no two icons of a country are identical.
Textures are uncompressed RGBA DDS, the convention of every other mod package.
Requires Pillow 11.3.0 for byte-reproducible output.
"""
import hashlib
import io
from pathlib import Path
import sys

import PIL
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/usea_depth'))
import seams  # noqa: E402

NAVY = (8, 22, 33, 255)
EDGE = (45, 85, 104, 255)
GRID = (16, 38, 52, 255)
LIGHT = (218, 237, 242, 255)
GOLD = (230, 181, 95, 255)
ACCENTS = [(93, 208, 223, 255), (120, 196, 140, 255), (214, 140, 96, 255), (176, 150, 222, 255), (222, 120, 132, 255),
           (230, 200, 110, 255), (110, 160, 230, 255), (160, 210, 90, 255), (220, 160, 200, 255), (130, 220, 200, 255)]
SHAPES = [
    [(16, 16), (176, 16), (176, 176), (16, 176)],
    [(96, 10), (182, 96), (96, 182), (10, 96)],
    [(28, 12), (164, 12), (180, 96), (164, 180), (28, 180), (12, 96)],
    [(16, 16), (176, 16), (176, 126), (96, 182), (16, 126)],
    [(12, 40), (96, 12), (180, 40), (180, 152), (96, 180), (12, 152)],
    [(40, 14), (152, 14), (180, 60), (180, 132), (152, 178), (40, 178), (12, 132), (12, 60)],
]
ARRANGEMENTS = [((26, 25, 119, 111), (126, 112, 45, 46)), ((23, 40, 93, 109), (111, 58, 65, 75)),
                ((55, 26, 110, 113), (26, 116, 46, 44)), ((45, 26, 104, 94), (65, 122, 66, 42)),
                ((26, 29, 109, 100), (110, 102, 61, 59)), ((41, 76, 111, 84), (73, 24, 47, 45))]
EVENT_SIZE = (210, 176)


def require_pinned_pillow():
    if PIL.__version__ != '11.3.0':
        raise SystemExit('Reproducible art requires Pillow 11.3.0; current ' + PIL.__version__)


def style(tag):
    digest = hashlib.sha256(tag.encode()).digest()
    return ACCENTS[digest[0] % len(ACCENTS)], SHAPES[digest[1] % len(SHAPES)]


_glyphs = None


def glyph(image, subject, rect, colour):
    global _glyphs
    if _glyphs is None:
        _glyphs = seams.glyph_library()
    _glyphs.glyph(image, subject, rect, colour)


def frame(tag, mark=False):
    accent, shape = style(tag)
    image = Image.new('RGBA', (192, 192))
    draw = ImageDraw.Draw(image)
    draw.polygon(shape, fill=NAVY)
    draw.line(shape + [shape[0]], fill=accent, width=3)
    draw.line((44, 166, 148, 166), fill=EDGE, width=2)
    if mark:
        draw.polygon([(87, 176), (96, 169), (105, 176), (96, 184)], fill=GOLD)
    return image


def composition(tag, primary, secondary, arrangement=0, mark=False):
    accent, _ = style(tag)
    image = frame(tag, mark)
    a, b = ARRANGEMENTS[arrangement % len(ARRANGEMENTS)]
    glyph(image, primary, a, LIGHT)
    glyph(image, secondary, b, accent)
    return image


def focus_icon(tag, primary, secondary, arrangement, mark=False):
    return composition(tag, primary, secondary, arrangement, mark).resize((96, 96), Image.Resampling.LANCZOS)


def idea_icon(tag, primary, secondary, arrangement=2):
    return composition(tag, primary, secondary, arrangement).resize((75, 75), Image.Resampling.LANCZOS)


def scene(tag, subjects):
    accent, _ = style(tag)
    image = Image.new('RGBA', (640, 260), NAVY)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, 631, 251), radius=8, outline=accent, width=3)
    for x in range(32, 625, 24):
        draw.line((x, 24, x, 235), fill=GRID, width=1)
    for y in range(34, 240, 24):
        draw.line((25, y, 615, y), fill=GRID, width=1)
    draw.line((35, 218, 606, 218), fill=EDGE, width=2)
    glyph(image, subjects[0], (70, 32, 187, 169), LIGHT)
    glyph(image, subjects[1], (361, 55, 149, 145), accent)
    draw.line((272, 128, 338, 128), fill=accent, width=3)
    draw.polygon([(338, 128), (327, 121), (327, 135)], fill=accent)
    return image


def event_picture(tag, subjects):
    fitted = ImageOps.contain(scene(tag, subjects), EVENT_SIZE, Image.Resampling.LANCZOS)
    image = Image.new('RGBA', EVENT_SIZE, NAVY)
    image.alpha_composite(fitted, ((EVENT_SIZE[0] - fitted.width) // 2, (EVENT_SIZE[1] - fitted.height) // 2))
    return image


def portrait(tag, subject):
    """An office card for an unnamed collective leadership: an emblem, never a face."""
    accent, shape = style(tag)
    image = Image.new('RGBA', (156, 210), NAVY)
    draw = ImageDraw.Draw(image)
    draw.rectangle((4, 4, 151, 205), outline=accent, width=3)
    emblem = frame(tag).resize((120, 120), Image.Resampling.LANCZOS)
    image.alpha_composite(emblem, (18, 30))
    glyph(image, subject, (48, 60, 60, 60), LIGHT)
    draw.line((30, 172, 126, 172), fill=EDGE, width=2)
    draw.line((44, 182, 112, 182), fill=EDGE, width=2)
    return image


def encoded(image, kind='DDS'):
    stream = io.BytesIO()
    image.save(stream, format=kind)
    return stream.getvalue()


def same_pixels(a, b):
    """Decoded comparison, so DDS headers or zlib choices never fail a check."""
    with Image.open(io.BytesIO(a)) as left, Image.open(io.BytesIO(b)) as right:
        return left.size == right.size and left.convert('RGBA').tobytes() == right.convert('RGBA').tobytes()
