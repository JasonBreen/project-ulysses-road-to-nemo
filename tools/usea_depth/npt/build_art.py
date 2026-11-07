"""Generated North Point art: one unique icon per focus, idea icons, office portraits and event pictures.

Authored geometry only, drawn with the shared glyph library (seams.glyph_library()).
No installed-game pixels, no fonts and no vanilla textures are read. Pillow 11.3.0.

    python -B tools/usea_depth/npt/build_art.py [--check]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE))
from usea_depth import seams  # noqa: E402
import content  # noqa: E402
import narrative  # noqa: E402

G = seams.glyph_library()
GFX = "gfx/AC_usea_depth/npt"
ACCENTS = {
    "politics": G.GOLD, "industry": (148, 210, 186, 255), "fleet": G.CYAN,
    "shelters": (202, 137, 128, 255), "relief": (151, 183, 225, 255), "late": (186, 160, 226, 255),
}
SECTIONS = list(ACCENTS)
OCTAGON = [(56, 8), (136, 8), (184, 56), (184, 136), (136, 184), (56, 184), (8, 136), (8, 56)]
# (primary rect, secondary rect) on a 192 px canvas.
LAYOUTS = [
    ((40, 30, 108, 108), (124, 120, 48, 48)),
    ((44, 30, 108, 108), (20, 120, 48, 48)),
    ((50, 62, 92, 92), (72, 18, 48, 40)),
    ((24, 44, 96, 96), (122, 44, 52, 52)),
]


def islands(draw, section, accent):
    """A short chain of 'island' dots along the lower edge; its shape marks the section."""
    index = SECTIONS.index(section)
    for k in range(index % 3 + 2):
        x = 70 + k * 18 + (index // 3) * 6
        draw.ellipse((x, 166, x + 8 + (k % 2) * 4, 174), fill=accent)


def focus_icon(focus, layout):
    accent = ACCENTS[focus.section]
    im = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.polygon(OCTAGON, fill=G.NAVY)
    draw.line(OCTAGON + [OCTAGON[0]], fill=accent, width=4)
    draw.line([(30, 22), (162, 22)], fill=G.EDGE, width=2)
    islands(draw, focus.section, accent)
    primary, secondary = LAYOUTS[layout]
    G.glyph(im, focus.subjects[0], primary, G.WHITE)
    G.glyph(im, focus.subjects[1], secondary, accent)
    return im.resize((96, 96), Image.Resampling.LANCZOS)


def idea_icon(index, idea):
    accent = list(ACCENTS.values())[index % len(ACCENTS)]
    im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((6, 6, 121, 121), radius=14, fill=G.NAVY, outline=accent, width=4)
    for k in range(index % 4 + 1):
        draw.rectangle((16 + k * 10, 108, 22 + k * 10, 113), fill=accent)
    G.glyph(im, idea.glyph, (26, 18, 76, 76), G.WHITE)
    return im.resize((64, 64), Image.Resampling.LANCZOS)


def portrait(office, accent):
    im = Image.new("RGBA", (156, 210), G.NAVY)
    draw = ImageDraw.Draw(im)
    for y in range(0, 210, 6):
        draw.line([(0, y), (155, y)], fill=G.PANEL, width=2)
    draw.ellipse((50, 34, 106, 98), fill=G.EDGE)
    draw.polygon([(18, 210), (24, 150), (52, 118), (104, 118), (132, 150), (138, 210)], fill=G.EDGE)
    draw.rectangle((0, 0, 155, 209), outline=accent, width=4)
    G.glyph(im, office.glyph, (58, 140, 40, 40), accent)
    return im


SCENES = {
    "council": ("assembly", "scales"), "harbour": ("navy", "gate"), "fleet": ("carrier", "radar"),
    "sky": ("meteor", "telescope"), "shelter": ("shelter", "civil"), "relief": ("refugees", "medical"),
    "rear": ("runway", "air"), "neutral": ("peace", "diplomacy"),
}


def event_picture(index, scene):
    big, small = SCENES[scene]
    accent = list(ACCENTS.values())[index % len(ACCENTS)]
    im = Image.new("RGBA", (210, 176), G.PANEL)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 112, 209, 175), fill=G.NAVY)
    for k, y in enumerate(range(122, 176, 12)):
        draw.line([(10 + k * 9, y), (200 - k * 7, y)], fill=G.EDGE, width=2)
    draw.polygon([(0, 112), (26, 92), (52, 100), (70, 112)], fill=G.EDGE)
    draw.polygon([(150, 112), (176, 96), (198, 104), (209, 112)], fill=G.EDGE)
    G.glyph(im, big, (66, 18, 82, 82), G.WHITE)
    G.glyph(im, small, (156, 22, 40, 40), accent)
    draw.rectangle((0, 0, 209, 175), outline=accent, width=3)
    return im


def outputs():
    """{relative path under the mod: image} plus manifest rows, in a stable order."""
    images = {}
    for index, focus in enumerate(content.FOCUSES):
        images["%s/focus/%s.dds" % (GFX, content.ident(focus.slug))] = (focus_icon(focus, index % len(LAYOUTS)), "focus icon")
    for index, idea in enumerate(content.IDEAS):
        images["%s/ideas/%s.dds" % (GFX, idea.ident)] = (idea_icon(index, idea), "idea icon")
    for office, accent in zip(content.OFFICES, (G.GOLD, ACCENTS["shelters"])):
        images["%s/portraits/NPT_ud_%s_office.dds" % (GFX, office.slug)] = (portrait(office, accent), "office portrait")
    for index, scene in enumerate(narrative.PICTURES):
        images["%s/events/%s.dds" % (GFX, scene)] = (event_picture(index, scene), "event picture")
    return images


def build(check=False):
    data, rows, failures = {}, [], []
    for relative, (image, role) in outputs().items():
        payload = seams.encoded(image)
        data[relative] = payload
        rows.append(dict(file="mod/2985041246/" + relative, width=image.width, height=image.height, role=role,
                         sha256=hashlib.sha256(payload).hexdigest()))
    for relative, payload in data.items():
        target = seams.MOD / relative
        if check:
            if not target.exists() or target.read_bytes() != payload:
                failures.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
    manifest = json.dumps(dict(generator="tools/usea_depth/npt/build_art.py", pillow="11.3.0",
                               provenance="original generated geometry; no game or third-party pixels",
                               assets=rows), indent=2) + "\n"
    path = HERE / "assets.json"
    if check:
        if not path.exists() or path.read_text(encoding="utf-8").replace("\r\n", "\n") != manifest:
            failures.append("tools/usea_depth/npt/assets.json")
    else:
        path.write_text(manifest, encoding="utf-8", newline="\n")
    return rows, failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rows, failures = build(args.check)
    if failures:
        raise SystemExit("North Point art differs: " + ", ".join(failures))
    print("North Point art:", len(rows), "textures", "verified." if args.check else "written.")


if __name__ == "__main__":
    main()
