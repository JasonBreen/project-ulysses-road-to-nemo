"""Original generated artwork for the Erusea package: focus icons, national spirits,
event pictures and the unnamed office portraits.

Everything is drawn from authored geometry with the shared Ulysses glyph library
(seams.glyph_library(), loaded read-only; its save(), build_focuses() and main()
are never called). No installed-game pixels, fonts, faces or baked captions are
used. Run through build.py, which writes or checks these outputs with the rest
of the package; --check here checks only the artwork.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / "tools"), str(HERE)]
from usea_depth import seams  # noqa: E402
import content  # noqa: E402
import narrative  # noqa: E402

MOD = ROOT / "mod/2985041246"
GFX = "gfx/AC_usea_depth/eru"
LIB = seams.glyph_library()
NAVY, EDGE, WHITE, CYAN, GOLD = LIB.NAVY, LIB.EDGE, LIB.WHITE, LIB.CYAN, LIB.GOLD

# One accent per lane; the opening and war trees use different frames.
ACCENT = {
    "court": (230, 181, 95, 255), "crown": (222, 160, 82, 255), "constitution": (120, 186, 236, 255),
    "regency": (196, 112, 98, 255), "industry": (156, 196, 132, 255), "army": (180, 170, 120, 255),
    "air": (93, 208, 223, 255), "fleet": (98, 150, 214, 255), "diplomacy": (178, 156, 214, 255),
    "crown_war": (214, 150, 70, 255), "assembly_war": (110, 170, 226, 255), "regency_war": (186, 100, 88, 255),
    "home_front": (200, 190, 150, 255), "aegir_war": (88, 136, 204, 255), "air_war": (84, 196, 214, 255),
    "megalith": (210, 120, 200, 255), "occupation": (170, 150, 110, 255), "postwar_isaf": (150, 210, 190, 255),
    "postwar_victory": (226, 196, 120, 255), "postwar_armistice": (170, 196, 214, 255),
}
LAYOUTS = [
    ("service-and-record", (28, 29, 119, 113), (128, 113, 45, 44)),
    ("paired-instruments", (21, 37, 93, 108), (110, 59, 65, 74)),
    ("foreground-and-context", (56, 28, 109, 112), (26, 116, 46, 44)),
    ("vertical-workflow", (47, 28, 102, 91), (65, 121, 66, 43)),
    ("diagonal-service", (28, 29, 108, 99), (110, 102, 60, 59)),
    ("fieldwork-and-plan", (42, 76, 109, 84), (73, 24, 47, 44)),
    ("high-and-low", (40, 22, 112, 80), (40, 108, 112, 50)),
    ("side-by-side", (16, 48, 84, 84), (100, 48, 76, 84)),
]
OPENING_FRAME = [(25, 18), (166, 18), (177, 119), (150, 158), (96, 179), (40, 157), (15, 119)]
WAR_FRAME = [(96, 8), (174, 39), (179, 124), (147, 166), (45, 166), (13, 124), (18, 39)]
EVENT_THEMES = {
    "court": ("medal", "assembly"), "assembly": ("assembly", "ballot"), "command": ("command", "security"),
    "industry": ("rail", "industry"), "fleet": ("navy", "submarine"), "air": ("air", "runway"),
    "diplomacy": ("diplomacy", "document"), "sky": ("meteor", "telescope"), "battery": ("missile", "radar"),
    "security": ("security", "gate"), "refugees": ("refugees", "shelter"), "megalith": ("meteor", "missile"),
    "occupation": ("gate", "scales"), "peace": ("peace", "rebuild"),
}
PORTRAIT_THEMES = {"constitutional_cabinet": ("ballot", "assembly"), "general_staff_regency": ("command", "security"),
                   "crown_council": ("medal", "peace")}


def band_mark(draw, band, accent):
    """Small band marks at the frame foot, so era-gated focuses read at a glance."""
    if band == "ulysses":
        for x in (54, 70, 122, 138):
            draw.ellipse((x - 3, 158, x + 3, 164), fill=accent)
    elif band == "coup":
        draw.line((44, 161, 74, 161), fill=accent, width=3)
        draw.line((118, 161, 148, 161), fill=accent, width=3)
    elif band == "stonehenge":
        draw.line((43, 156, 52, 166, 61, 156), fill=accent, width=2)
        draw.line((131, 156, 140, 166, 149, 156), fill=accent, width=2)
    elif band == "impact":
        draw.arc((37, 135, 155, 176), 0, 180, fill=accent, width=2)
    elif band == "war":
        draw.line((48, 156, 62, 168), fill=accent, width=2)
        draw.line((62, 156, 48, 168), fill=accent, width=2)
        draw.line((130, 156, 144, 168), fill=accent, width=2)
        draw.line((144, 156, 130, 168), fill=accent, width=2)
    else:
        draw.line((48, 163, 70, 163), fill=EDGE, width=2)
        draw.line((122, 163, 144, 163), fill=EDGE, width=2)


def focus_band(row):
    if row.band:
        return row.band
    return "war" if "ac_ucw_war_started" in row.gate or "war_running" in row.gate else ""


def focus_image(row, layout):
    image = Image.new("RGBA", (192, 192))
    draw = ImageDraw.Draw(image)
    accent = ACCENT[row.lane]
    shape = OPENING_FRAME if row.tree == "opening" else WAR_FRAME
    draw.polygon(shape, fill=NAVY)
    draw.line(shape + [shape[0]], fill=accent, width=3)
    if row.cost >= 10:
        draw.line([(p[0], p[1] + (6 if p[1] < 96 else -6)) for p in shape] + [(shape[0][0], shape[0][1] + 6)], fill=EDGE, width=1)
    band_mark(draw, focus_band(row), accent)
    name, primary, secondary = LAYOUTS[layout]
    LIB.glyph(image, row.art[0], primary, WHITE)
    LIB.glyph(image, row.art[1], secondary, accent)
    return image.resize((96, 96), Image.Resampling.LANCZOS), name


def idea_image(ident, art, index, repeat):
    image = Image.new("RGBA", (150, 150))
    draw = ImageDraw.Draw(image)
    accent = (GOLD, CYAN, (178, 156, 214, 255), (156, 196, 132, 255), (196, 112, 98, 255))[index % 5]
    shape = [(20, 8), (130, 8), (142, 20), (142, 130), (130, 142), (20, 142), (8, 130), (8, 20)]
    draw.polygon(shape, fill=NAVY)
    draw.line(shape + [shape[0]], fill=accent, width=3)
    if repeat >= len(LAYOUTS):
        raise ValueError("Add a deliberate composition for the repeated spirit subjects of " + ident)
    _, primary, secondary = LAYOUTS[repeat]
    scale = lambda r: tuple(round(v * 150 / 192) for v in r)
    LIB.glyph(image, art[0], scale(primary), WHITE)
    LIB.glyph(image, art[1], scale(secondary), accent)
    return image.resize((75, 75), Image.Resampling.LANCZOS)


def event_image(theme, index):
    width, height = 210, 176
    image = Image.new("RGBA", (width, height), NAVY)
    draw = ImageDraw.Draw(image)
    for y in range(0, height, 22):
        draw.line((0, y, width, y), fill=(13, 32, 46, 255), width=1)
    horizon = 118 + (index % 3) * 6
    draw.line((0, horizon, width, horizon), fill=EDGE, width=2)
    draw.rectangle((2, 2, width - 3, height - 3), outline=EDGE, width=2)
    primary, secondary = EVENT_THEMES[theme]
    LIB.glyph(image, primary, (52, 22, 104, 98), WHITE)
    LIB.glyph(image, secondary, (12 + (index % 4) * 4, 128, 44, 38), CYAN)
    LIB.glyph(image, secondary, (154 - (index % 4) * 4, 128, 44, 38), GOLD)
    return image


def portrait_image(slug):
    image = Image.new("RGBA", (156, 210), NAVY)
    draw = ImageDraw.Draw(image)
    draw.rectangle((3, 3, 152, 206), outline=GOLD, width=3)
    draw.ellipse((28, 30, 128, 130), outline=EDGE, width=3)
    primary, secondary = PORTRAIT_THEMES[slug]
    LIB.glyph(image, primary, (44, 46, 68, 68), WHITE)
    LIB.glyph(image, secondary, (53, 146, 50, 46), CYAN)
    return image


def outputs():
    if PIL.__version__ != "11.3.0":
        raise SystemExit("Use the reproducible Pillow 11.3.0 renderer; current version is " + PIL.__version__)
    out, assets, sprites = {}, [], []

    def texture(relative, image, role, sprite, **metadata):
        data = seams.encoded(image)
        out[MOD / relative] = data
        alpha = image.getchannel("A").getextrema()
        assets.append({"file": relative, "role": role, "sprite": sprite, "width": image.width, "height": image.height,
                       "frames": 1, "format": "DDS RGBA8", "alpha_min": alpha[0], "alpha_max": alpha[1],
                       "sha256": hashlib.sha256(data).hexdigest(), **metadata})

    used = Counter()
    for row in content.FOCUSES:
        key = (row.lane, focus_band(row), row.art)
        layout = used[key]
        used[key] += 1
        if layout >= len(LAYOUTS):
            raise ValueError("Add a deliberate composition for repeated subjects: %s" % (key,))
        image, name = focus_image(row, layout)
        texture("%s/focus/%s.dds" % (GFX, row.id), image, "original focus composition", "GFX_ac_ud_focus_" + row.id,
                focus=row.id, lane=row.lane, primary=row.art[0], secondary=row.art[1], composition=name)
        sprites.extend(seams.focus_sprites("eru", row.id))
    repeats = Counter()
    for index, (ident, (_, _, _, art)) in enumerate(sorted(content.IDEAS.items())):
        sprite = "GFX_idea_" + ident
        image = idea_image(ident, art, index, repeats[art])
        repeats[art] += 1
        texture("%s/ideas/%s.dds" % (GFX, ident), image, "original national spirit", sprite, idea=ident)
        sprites.append('spriteType = { name = "%s" texturefile = "%s/ideas/%s.dds" }' % (sprite, GFX, ident))
    themes = sorted({event["picture"] for event in narrative.EVENTS.values()})
    for index, theme in enumerate(themes):
        sprite = "GFX_ac_ud_eru_event_" + theme
        texture("%s/events/%s.dds" % (GFX, theme), event_image(theme, index), "original event picture", sprite, theme=theme)
        sprites.append('spriteType = { name = "%s" texturefile = "%s/events/%s.dds" }' % (sprite, GFX, theme))
    for slug in sorted(content.OFFICES):
        ident = "ERU_ud_%s_office" % slug
        sprite = "GFX_ac_ud_portrait_" + ident
        texture("%s/portraits/%s.dds" % (GFX, ident), portrait_image(slug), "original office emblem portrait", sprite, office=ident)
        sprites.append('spriteType = { name = "%s" texturefile = "%s/portraits/%s.dds" }' % (sprite, GFX, ident))
    focus_hashes = [a["sha256"] for a in assets if a["role"] == "original focus composition"]
    if len(focus_hashes) != len(content.FOCUSES) or len(set(focus_hashes)) != len(focus_hashes):
        raise ValueError("Every focus needs a distinct rendered composition")
    if len({a["sha256"] for a in assets}) != len(assets):
        raise ValueError("Every texture must be distinct")
    out[MOD / "interface/ac_ud_eru.gfx"] = ("spriteTypes = {\n" + "\n".join("\t" + s for s in sprites) + "\n}\n").encode("utf-8")
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")).hexdigest()
              for p in (HERE / "content.py", HERE / "narrative.py", Path(__file__), ROOT / "tools/usea_expansion/build_art.py")}
    manifest = {"schema": 1, "renderer": "Pillow 11.3.0", "package": "eru",
                "source_layer": "original code-native Ulysses artwork; no engine, DLC, remote or vanilla pixels",
                "source_hashes": hashes, "source_hash_encoding": "UTF-8 with normalized LF newlines",
                "focus_compositions": len(focus_hashes), "no_baked_focus_captions": True, "no_added_watermarks": True,
                "native": "Not rendered in HOI4; native acceptance remains under #8", "assets": assets}
    out[HERE / "assets.json"] = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path, data in outputs().items():
        if args.check:
            if not path.exists() or path.read_bytes() != data:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if stale:
        raise SystemExit("Erusea artwork differs: " + ", ".join(stale[:20]))
    print("Erusea artwork " + ("consistent" if args.check else "written"))


if __name__ == "__main__":
    main()
