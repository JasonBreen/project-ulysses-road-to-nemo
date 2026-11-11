"""Generated art for the Central Usea (FCU) Usea Depth package.

Draws every texture from the shared Ulysses glyph library (seams.glyph_library())
with Pillow 11.3.0: one unique icon per focus, idea icons, event scenes and the two
office cards. No installed-game pixels, vanilla textures or fonts are read; the only
font is the bundled OFL DINish face. Never calls the library's save(),
build_focuses() or main().

--check compares every texture and assets.json without writing.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / "tools")]
from usea_depth import seams  # noqa: E402
import content as C  # noqa: E402

LIB = seams.glyph_library()
MOD = ROOT / "mod/2985041246"
ART = "gfx/AC_usea_depth/fcu"
FONT = LIB.FONT

# Section accents keep each part of the tree recognisable at a glance.
ACCENT = {
    "politics": (93, 208, 223, 255), "economy": (230, 181, 95, 255), "treaty": (148, 210, 186, 255),
    "skully": (120, 170, 230, 255), "evacuation": (230, 150, 110, 255), "stonehenge": (190, 160, 230, 255),
    "coup": (220, 110, 110, 255), "impact": (240, 200, 120, 255), "forces": (150, 200, 150, 255),
    "aftermath": (200, 180, 140, 255), "continuity": (93, 208, 223, 255), "isaf": (120, 200, 230, 255),
    "air": (170, 210, 240, 255), "liberation": (150, 220, 160, 255), "postwar": (230, 181, 95, 255),
}
# (name, primary box, secondary box) on a 192 px canvas.
LAYOUTS = [
    ("inset", (32, 34, 108, 104), (124, 110, 42, 42)),
    ("paired", (26, 40, 80, 96), (108, 60, 58, 64)),
    ("stacked", (48, 30, 96, 84), (72, 120, 50, 40)),
    ("diagonal", (30, 32, 92, 86), (108, 98, 58, 58)),
    ("left_inset", (52, 34, 108, 104), (24, 110, 42, 42)),
    ("lower_subject", (48, 76, 98, 82), (72, 24, 48, 44)),
    ("horizon", (40, 28, 112, 90), (66, 122, 60, 42)),
    ("triptych", (62, 34, 94, 100), (26, 114, 44, 44)),
]
OPENING_SHAPE = [(96, 8), (176, 46), (176, 146), (96, 184), (16, 146), (16, 46)]
WAR_SHAPE = [(22, 18), (170, 18), (178, 132), (96, 184), (14, 132)]


def frame(image, shape, accent):
    draw = ImageDraw.Draw(image)
    draw.polygon(shape, fill=LIB.NAVY)
    draw.line(shape + [shape[0]], fill=accent, width=4)
    return draw


def focus_icon(focus, variant):
    accent = ACCENT[focus.section]
    layout = LAYOUTS[variant % len(LAYOUTS)]
    image = Image.new("RGBA", (192, 192))
    draw = frame(image, OPENING_SHAPE if focus.tree == C.OPENING else WAR_SHAPE, accent)
    LIB.glyph(image, focus.subj[0], layout[1], LIB.WHITE)
    LIB.glyph(image, focus.subj[1], layout[2], accent)
    # A row of pips records the cost; a dash under them marks a mutually exclusive choice.
    for index in range(focus.cost // 5):
        draw.ellipse((84 + index * 16, 166, 92 + index * 16, 174), fill=accent)
    if focus.excl:
        draw.line((80, 178, 112, 178), fill=accent, width=2)
    if variant >= len(LAYOUTS):
        image = ImageOps.mirror(image)
    return image.resize((96, 96), Image.Resampling.LANCZOS)


def idea_icon(subjects, variant):
    layout = LAYOUTS[variant % len(LAYOUTS)]
    image = Image.new("RGBA", (150, 150))
    draw = ImageDraw.Draw(image)
    draw.polygon([(12, 16), (138, 16), (138, 116), (75, 144), (12, 116)], fill=LIB.NAVY, outline=LIB.CYAN)
    scale = 150 / 192
    box = lambda b: tuple(round(v * scale) for v in b)  # noqa: E731
    LIB.glyph(image, subjects[0], box(layout[1]), LIB.WHITE)
    LIB.glyph(image, subjects[1], box(layout[2]), LIB.GOLD)
    if variant >= len(LAYOUTS):
        image = ImageOps.mirror(image)
    return image.resize((75, 75), Image.Resampling.LANCZOS)


SCENES = {
    # key: (primary, secondary, sky tint)
    "assembly": ("assembly", "ballot", (20, 44, 64)), "directorate": ("command", "security", (40, 30, 40)),
    "treaty": ("diplomacy", "document", (18, 50, 52)), "islands": ("navy", "security", (16, 40, 70)),
    "warning": ("meteor", "telescope", (36, 24, 58)), "evacuation": ("refugees", "rail", (48, 36, 30)),
    "stonehenge": ("radar", "missile", (44, 40, 24)), "coup": ("security", "communications", (56, 22, 26)),
    "impact": ("meteor", "shelter", (64, 34, 20)), "economy": ("economy", "industry", (40, 44, 22)),
    "forces": ("command", "training", (22, 46, 34)), "isaf": ("diplomacy", "command", (20, 42, 66)),
    "exile": ("runway", "navy", (18, 36, 58)), "air": ("air", "radar", (26, 52, 80)),
    "landing": ("carrier", "air", (22, 46, 72)), "liberation": ("peace", "rebuild", (26, 58, 40)),
    "postwar": ("scales", "document", (50, 44, 30)),
}


def scene(key):
    primary, secondary, tint = SCENES[key]
    width, height = 420, 352
    image = Image.new("RGBA", (width, height), LIB.NAVY)
    draw = ImageDraw.Draw(image)
    for row in range(height):
        mix = row / height
        colour = tuple(round(tint[i] * (1 - mix) + LIB.NAVY[i] * mix) for i in range(3)) + (255,)
        draw.line((0, row, width, row), fill=colour)
    draw.line((0, 250, width, 250), fill=LIB.EDGE, width=3)
    for x in range(0, width, 28):
        draw.line((x, 250, x - 60, height), fill=LIB.EDGE, width=1)
    LIB.glyph(image, primary, (130, 40, 190, 190), LIB.WHITE)
    LIB.glyph(image, secondary, (30, 200, 110, 110), LIB.CYAN)
    LIB.glyph(image, secondary, (300, 210, 90, 90), LIB.GOLD)
    draw.rectangle((0, 0, width - 1, height - 1), outline=LIB.EDGE, width=4)
    return image.resize((210, 176), Image.Resampling.LANCZOS)


OFFICE_ART = {"directorate": ("command", "security", "EMERGENCY", "DIRECTORATE"),
              "unity": ("assembly", "ballot", "FEDERAL UNITY", "CABINET")}


def office_card(slug):
    primary, secondary, line1, line2 = OFFICE_ART[slug]
    image = Image.new("RGBA", (156, 210), LIB.NAVY)
    draw = ImageDraw.Draw(image)
    draw.rectangle((7, 7, 148, 202), outline=LIB.EDGE, width=2)
    draw.line((16, 27, 140, 27), fill=LIB.CYAN, width=2)
    draw.line((16, 183, 140, 183), fill=LIB.CYAN, width=2)
    LIB.glyph(image, primary, (38, 44, 80, 80), LIB.WHITE)
    LIB.glyph(image, secondary, (58, 126, 40, 30), LIB.GOLD)
    small = ImageFont.truetype(str(FONT), 13)
    draw.text((78, 17), "FCU", font=small, anchor="mm", fill=LIB.CYAN)
    draw.text((78, 164), line1, font=small, anchor="mm", fill=LIB.WHITE)
    draw.text((78, 176), line2, font=small, anchor="mm", fill=LIB.WHITE)
    return image


def assign_variants(rows):
    """A distinct (subjects, layout, mirror) for every row with the same subjects."""
    used, variants = {}, []
    for key in rows:
        index = used.get(key, 0)
        used[key] = index + 1
        if index >= 2 * len(LAYOUTS):
            raise SystemExit("Too many icons share the subjects %s; pick different subjects" % (key,))
        variants.append(index)
    return variants


def textures():
    out = {}
    focus_keys = [(f.section, f.subj) for f in C.FOCUSES]
    for focus, variant in zip(C.FOCUSES, assign_variants(focus_keys)):
        out["%s/focus/%s.dds" % (ART, focus.id)] = ("original focus icon", focus_icon(focus, variant))
    idea_keys = [subjects for _, _, _, subjects, _ in C.IDEAS]
    for (ident, _, _, subjects, _), variant in zip(C.IDEAS, assign_variants(idea_keys)):
        out["%s/ideas/%s.dds" % (ART, ident)] = ("original idea icon", idea_icon(subjects, variant))
    for key in SCENES:
        out["%s/events/%s.dds" % (ART, key)] = ("original event scene", scene(key))
    for slug in OFFICE_ART:
        out["%s/portraits/%s.dds" % (ART, slug)] = ("original office card; no person depicted", office_card(slug))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    records, stale, digests = [], [], {}
    for relative, (role, image) in sorted(textures().items()):
        data = seams.encoded(image)
        digest = hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()
        if digest in digests:
            raise SystemExit("Duplicate pixels: %s and %s" % (relative, digests[digest]))
        digests[digest] = relative
        path = MOD / relative
        if not path.exists() or path.read_bytes() != data:
            stale.append(relative)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        records.append(dict(file=relative, width=image.width, height=image.height, role=role,
                            sha256=hashlib.sha256(data).hexdigest(), pixels_sha256=digest))
    manifest = HERE / "assets.json"
    text = json.dumps(dict(generator="tools/usea_depth/fcu/build_art.py", pillow="11.3.0", textures=records), indent=2) + "\n"
    if not manifest.exists() or manifest.read_text(encoding="utf-8").replace("\r\n", "\n") != text:
        stale.append(manifest.relative_to(ROOT).as_posix())
        if not args.check:
            manifest.write_text(text, encoding="utf-8", newline="\n")
    if args.check and stale:
        raise SystemExit("Central Usea art is stale:\n- " + "\n- ".join(stale[:20]))
    print("Central Usea art: %d textures, all unique; %s." % (len(records), "verified" if args.check else "%d written" % len(stale)))


if __name__ == "__main__":
    main()
