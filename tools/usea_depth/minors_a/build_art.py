"""Draw the minor states A artwork with the shared Ulysses glyph library and Pillow 11.3.0.

python -B tools/usea_depth/minors_a/build_art.py           write textures, interface/ac_ud_minors_a.gfx and assets.json
python -B tools/usea_depth/minors_a/build_art.py --check   compare every byte; never writes

Every texture is generated here from authored geometry: one unique focus icon per
focus (its shine reuses the same texture through seams.focus_sprites), one icon
per national spirit, one office card per provisional government (the existing
mod national flag inside an original frame, never a fabricated face) and four
event scenes per state. No installed-game or vanilla pixels are read.
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import PIL
from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import content as C  # noqa: E402
from content import seams  # noqa: E402

MOD = C.MOD
GFX = "interface/ac_ud_minors_a.gfx"
BASE = "gfx/AC_usea_depth/minors_a/"
NOTE = "# Usea Depth minor states A: original generated artwork; owner tools/usea_depth/minors_a/build_art.py.\n"

# A distinct accent and silhouette for each state.
ACCENT = {
    "CHO": (126, 204, 140, 255), "PLA": (102, 178, 232, 255), "FRU": (214, 170, 96, 255), "ALR": (196, 128, 104, 255),
    "DOR": (128, 214, 214, 255), "SCA": (160, 186, 236, 255), "BLD": (206, 150, 206, 255),
}
SHAPES = {
    "CHO": [(30, 14), (162, 14), (178, 64), (170, 150), (96, 180), (22, 150), (14, 64)],
    "PLA": [(96, 8), (178, 54), (178, 138), (96, 182), (14, 138), (14, 54)],
    "FRU": [(22, 22), (170, 22), (178, 40), (178, 156), (150, 178), (42, 178), (14, 156), (14, 40)],
    "ALR": [(14, 14), (178, 14), (178, 150), (138, 180), (54, 180), (14, 150)],
    "DOR": [(56, 12), (136, 12), (180, 56), (180, 136), (136, 180), (56, 180), (12, 136), (12, 56)],
    "SCA": [(18, 30), (96, 10), (174, 30), (180, 120), (96, 182), (12, 120)],
    "BLD": [(96, 10), (182, 96), (96, 182), (10, 96)],
}
# Primary and secondary glyph rectangles inside the 192 px master.
LAYOUTS = [
    ((36, 34, 112, 112), (126, 112, 46, 46)),
    ((44, 28, 104, 104), (34, 120, 44, 44)),
    ((60, 40, 96, 96), (28, 36, 48, 48)),
    ((40, 50, 100, 100), (118, 26, 50, 50)),
    ((30, 30, 92, 92), (106, 96, 62, 62)),
    ((56, 30, 104, 92), (28, 118, 52, 44)),
    ((34, 58, 96, 96), (116, 50, 52, 64)),
    ((48, 24, 96, 96), (64, 122, 64, 44)),
]
PARTY = {"democratic": (93, 208, 223, 255), "communism": (214, 96, 96, 255), "fascism": (150, 120, 90, 255),
         "neutrality": (180, 180, 160, 255), "monarchism": (230, 181, 95, 255)}
SCENES = {
    "nation": ("civil", "industry", "rail"),
    "politics": ("assembly", "ballot", "scales"),
    "crisis": ("meteor", "shelter", "refugees"),
    "war": ("security", "air", "radar"),
}


def library():
    return seams.glyph_library()


def era_marks(draw, band, accent, edge):
    # Band 0 two short rules; 1 chevrons; 2 a wave; 3 an arc.
    if band == 0:
        draw.line((48, 166, 72, 166), fill=edge, width=2)
        draw.line((120, 166, 144, 166), fill=edge, width=2)
    elif band == 1:
        draw.line((44, 160, 54, 170, 64, 160), fill=accent, width=2)
        draw.line((128, 160, 138, 170, 148, 160), fill=accent, width=2)
    elif band == 2:
        draw.line((42, 168, 60, 160, 78, 168), fill=accent, width=2)
        draw.line((114, 168, 132, 160, 150, 168), fill=accent, width=2)
    else:
        draw.arc((40, 140, 152, 180), 0, 180, fill=accent, width=2)


def focus_icon(lib, tag, focus, ordinal):
    if ordinal >= len(LAYOUTS):
        raise ValueError("Add a layout: %s uses %s/%s more than %d times" % (tag, focus.icon[0], focus.icon[1], len(LAYOUTS)))
    image = Image.new("RGBA", (192, 192))
    draw = ImageDraw.Draw(image)
    accent, shape = ACCENT[tag], SHAPES[tag]
    draw.polygon(shape, fill=lib.NAVY)
    draw.line(shape + [shape[0]], fill=accent, width=3)
    if focus.cost == 10:
        draw.line(shape[:2], fill=lib.GOLD, width=5)
    era_marks(draw, C.ERA_BAND[focus.era], accent, lib.EDGE)
    first, second = LAYOUTS[ordinal]
    lib.glyph(image, focus.icon[0], first, lib.WHITE)
    lib.glyph(image, focus.icon[1], second, accent)
    return image.resize((96, 96), Image.Resampling.LANCZOS)


IDEA_LAYOUTS = [
    ((24, 20, 74, 74), (80, 74, 32, 32)),
    ((32, 30, 70, 70), (18, 18, 30, 30)),
    ((20, 34, 70, 70), (82, 16, 30, 30)),
    ((30, 16, 68, 68), (20, 82, 30, 28)),
]


def idea_icon(lib, tag, idea, ordinal):
    """A spirit icon; ordinal counts earlier spirits of this state with the same subject pair."""
    if ordinal >= len(IDEA_LAYOUTS):
        raise ValueError("Add a spirit layout: %s uses %s/%s more than %d times" % (tag, idea.icon[0], idea.icon[1], len(IDEA_LAYOUTS)))
    image = Image.new("RGBA", (128, 128))
    draw = ImageDraw.Draw(image)
    accent = ACCENT[tag]
    draw.rounded_rectangle((6, 6, 121, 121), radius=14, fill=lib.NAVY, outline=accent, width=3)
    first, second = IDEA_LAYOUTS[ordinal]
    lib.glyph(image, idea.icon[0], first, lib.WHITE)
    lib.glyph(image, idea.icon[1], second, accent)
    return image.resize((64, 64), Image.Resampling.LANCZOS)


def portrait(lib, state, gov):
    canvas = Image.new("RGBA", (156, 210), lib.NAVY)
    draw = ImageDraw.Draw(canvas)
    accent, party = ACCENT[state.tag], PARTY[gov.party]
    draw.rectangle((6, 6, 149, 203), outline=accent, width=2)
    draw.rectangle((12, 12, 143, 197), outline=lib.EDGE, width=1)
    draw.line((18, 30, 138, 30), fill=party, width=3)
    draw.line((18, 180, 138, 180), fill=party, width=3)
    flag = MOD / "gfx/flags" / (state.tag + ".tga")
    with Image.open(flag) as original:
        emblem = ImageOps.contain(original.convert("RGBA"), (112, 70), Image.Resampling.LANCZOS)
    canvas.alpha_composite(emblem, ((156 - emblem.width) // 2, 40))
    lib.glyph(canvas, gov.icon, (40, 116, 76, 58), lib.WHITE)
    return canvas


def scene(lib, tag, kind):
    image = Image.new("RGBA", (210, 176), lib.NAVY)
    draw = ImageDraw.Draw(image)
    accent = ACCENT[tag]
    for row in range(0, 176, 8):
        shade = 26 + (row * 18) // 176
        draw.line((0, row, 209, row), fill=(8, shade, 33 + row // 12, 255), width=8)
    draw.rectangle((3, 3, 206, 172), outline=accent, width=2)
    shape = [(x * 210 // 192, y * 176 // 192) for x, y in SHAPES[tag]]
    draw.line(shape + [shape[0]], fill=lib.EDGE, width=2)
    first, second, third = SCENES[kind]
    lib.glyph(image, first, (64, 34, 84, 84), lib.WHITE)
    lib.glyph(image, second, (20, 104, 48, 48), accent)
    lib.glyph(image, third, (142, 104, 48, 48), accent)
    return image


def outputs():
    if PIL.__version__ != "11.3.0":
        raise SystemExit("Use the reproducible Pillow 11.3.0 renderer; current version is " + PIL.__version__)
    lib = library()
    states = C.load_states()
    data, assets, sprites = {}, [], []

    def texture(relative, image, role, sprite, **metadata):
        payload = seams.encoded(image)
        data[relative] = payload
        alpha = image.getchannel("A").getextrema()
        assets.append({"file": relative, "role": role, "sprite": sprite, "width": image.width, "height": image.height,
                       "frames": 1, "format": "DDS RGBA8", "alpha_min": alpha[0], "alpha_max": alpha[1],
                       "sha256": hashlib.sha256(payload).hexdigest(), **metadata})

    for state in states:
        used = Counter()
        for focus in state.focuses:
            ident = C.fid(state.tag, focus.slug)
            pair = tuple(focus.icon)
            image = focus_icon(lib, state.tag, focus, used[pair])
            used[pair] += 1
            lines = seams.focus_sprites(C.PACKAGE, ident)
            relative = BASE + "focus/%s.dds" % ident
            if relative not in lines[0]:
                raise ValueError("Focus sprite path drift for " + ident)
            texture(relative, image, "original focus composition", "GFX_ac_ud_focus_" + ident, tag=state.tag,
                    focus=ident, primary=pair[0], secondary=pair[1])
            sprites.extend(lines)
        spirits = Counter()
        for idea in state.ideas:
            ordinal = spirits[tuple(idea.icon)]
            spirits[tuple(idea.icon)] += 1
            picture = C.idea_picture(state.tag, idea.slug)
            name = "GFX_idea_" + picture
            relative = BASE + "ideas/%s.dds" % picture
            texture(relative, idea_icon(lib, state.tag, idea, ordinal), "original national spirit composition", name, tag=state.tag,
                    idea=C.idea_id(state.tag, idea.slug))
            sprites.append('spriteType = { name = "%s" texturefile = "%s" }' % (name, relative))
        for gov in state.governments:
            ident = C.office_id(state.tag, gov.slug)
            name = "GFX_ac_ud_portrait_" + ident
            relative = BASE + "leaders/%s.dds" % ident
            texture(relative, portrait(lib, state, gov), "existing mod national flag in an original office frame", name, tag=state.tag,
                    office=ident, flag="gfx/flags/%s.tga" % state.tag)
            sprites.append('spriteType = { name = "%s" texturefile = "%s" }' % (name, relative))
        for kind in C.PICTURES:
            name = "GFX_ac_ud_event_%s_%s" % (state.tag.lower(), kind)
            relative = BASE + "events/%s_%s.dds" % (state.tag.lower(), kind)
            texture(relative, scene(lib, state.tag, kind), "original event scene", name, tag=state.tag, scene=kind)
            sprites.append('spriteType = { name = "%s" texturefile = "%s" }' % (name, relative))
    focus_hashes = [row["sha256"] for row in assets if row["role"] == "original focus composition"]
    if len(focus_hashes) != len(set(focus_hashes)):
        raise ValueError("Every focus needs a distinct icon")
    if len({row["sha256"] for row in assets}) != len(assets):
        raise ValueError("Every texture must be distinct")
    data[GFX] = (NOTE + "spriteTypes = {\n" + "".join("\t" + line + "\n" for line in sprites) + "}\n").encode("utf-8")
    manifest = (json.dumps(assets, indent=1) + "\n").encode("utf-8")
    return data, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data, manifest = outputs()
    differs = []
    for relative, payload in data.items():
        path = MOD / relative
        current = path.read_bytes() if path.exists() else None
        if relative.endswith(".gfx") and current is not None:
            current = current.replace(b"\r\n", b"\n")
        if args.check:
            if current != payload:
                differs.append(relative)
        elif current != payload:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    target = HERE / "assets.json"
    current = target.read_bytes().replace(b"\r\n", b"\n") if target.exists() else None
    if args.check and current != manifest:
        differs.append("tools/usea_depth/minors_a/assets.json")
    elif not args.check and current != manifest:
        target.write_bytes(manifest)
    if args.check:
        folder = MOD / BASE
        expected = {MOD / relative for relative in data}
        stray = sorted(p.relative_to(MOD).as_posix() for p in folder.rglob("*") if p.is_file() and p not in expected) if folder.exists() else []
        differs.extend(stray)
    if differs:
        raise SystemExit("Minor states A art differs: " + ", ".join(differs[:20]) + (" ..." if len(differs) > 20 else ""))
    print("Minor states A art: %d textures %s" % (len(data) - 1, "verified" if args.check else "written"))


if __name__ == "__main__":
    main()
