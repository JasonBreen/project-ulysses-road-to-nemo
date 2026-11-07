"""Package the minors B artwork: one generated icon per focus, idea, decision and office.

Every texture is drawn from the shared Ulysses glyph library (loaded read-only through
seams.glyph_library(); its save(), build_focuses() and main() are never called) with
the pinned Pillow 11.3.0 renderer. No installed-game pixels, fonts, faces or captions
are used. --check compares every texture, the sprite file and assets.json byte for byte.
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MOD = ROOT / "mod/2985041246"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
from schema import BANDS  # noqa: E402
from usea_depth import seams  # noqa: E402

LIB = seams.glyph_library()
NAVY, EDGE, WHITE = LIB.NAVY, LIB.EDGE, LIB.WHITE
BASE = "gfx/AC_usea_depth/minors_b"
LAYOUTS = [
    ("subject-and-detail", (28, 29, 119, 113), (128, 113, 45, 44)),
    ("paired-instruments", (21, 37, 93, 108), (110, 59, 65, 74)),
    ("foreground-and-context", (56, 28, 109, 112), (26, 116, 46, 44)),
    ("vertical-workflow", (47, 28, 102, 91), (65, 121, 66, 43)),
    ("diagonal", (28, 29, 108, 99), (110, 102, 60, 59)),
    ("fieldwork-and-plan", (42, 76, 109, 84), (73, 24, 47, 44)),
    ("high-and-low", (60, 18, 84, 84), (24, 112, 58, 52)),
    ("side-by-side", (16, 52, 78, 86), (98, 52, 78, 86)),
]


def frame(state, band, size=192):
    image = Image.new("RGBA", (size, size))
    draw = ImageDraw.Draw(image)
    scale = size / 192
    shape = [(round(x * scale), round(y * scale)) for x, y in state.SILHOUETTE]
    draw.polygon(shape, fill=NAVY)
    draw.line(shape + [shape[0]], fill=state.ACCENT, width=max(1, round(3 * scale)))
    accent = state.ACCENT
    marks = {
        "rebuilding": lambda: (draw.line((48, 163, 70, 163), fill=EDGE, width=2), draw.line((122, 163, 144, 163), fill=EDGE, width=2)),
        "preparation": lambda: (draw.line((43, 156, 52, 166, 61, 156), fill=accent, width=2), draw.line((130, 156, 139, 166, 148, 156), fill=accent, width=2)),
        "relief": lambda: (draw.line((42, 163, 60, 156, 78, 163), fill=accent, width=2), draw.line((114, 163, 132, 156, 150, 163), fill=accent, width=2)),
        "war": lambda: draw.arc((37, 135, 155, 176), 0, 180, fill=accent, width=2),
    }
    if size == 192 and band:
        marks[band]()
    return image


def compose(state, band, primary, secondary, ordinal):
    if primary not in seams.SUBJECTS or secondary not in seams.SUBJECTS:
        raise SystemExit("Unreviewed subject: %s/%s" % (primary, secondary))
    if ordinal >= len(LAYOUTS):
        raise SystemExit("%s: subject pair %s/%s repeats more than %d times; choose another pair" % (state.TAG, primary, secondary, len(LAYOUTS)))
    image = frame(state, band)
    name, first, second = LAYOUTS[ordinal]
    LIB.glyph(image, primary, first, WHITE)
    LIB.glyph(image, secondary, second, state.ACCENT)
    return image, name


def portrait(state, regime):
    image = Image.new("RGBA", (156, 210), NAVY)
    draw = ImageDraw.Draw(image)
    draw.rectangle((3, 3, 152, 206), outline=state.ACCENT, width=3)
    draw.rectangle((12, 12, 143, 150), outline=EDGE, width=2)
    LIB.glyph(image, regime.subjects[0], (30, 24, 96, 96), WHITE)
    LIB.glyph(image, regime.subjects[1], (56, 156, 44, 40), state.ACCENT)
    draw.line((18, 160, 46, 160), fill=EDGE, width=2)
    draw.line((110, 160, 138, 160), fill=EDGE, width=2)
    return image


def outputs():
    if PIL.__version__ != "11.3.0":
        raise SystemExit("Use the reproducible Pillow 11.3.0 renderer; current version is " + PIL.__version__)
    states = build.all_states()
    out, assets, sprites = {}, [], []

    def texture(relative, image, role, sprite, **metadata):
        data = seams.encoded(image)
        out[MOD / relative] = data
        alpha = image.getchannel("A").getextrema()
        assets.append({"file": relative, "role": role, "sprite": sprite, "width": image.width, "height": image.height,
                       "frames": 1, "format": "DDS RGBA8", "alpha_min": alpha[0], "alpha_max": alpha[1],
                       "sha256": hashlib.sha256(data).hexdigest(), **metadata})

    focus_hashes = []
    for state in states:
        used = Counter()
        for f in state.FOCUSES:
            ident = build.fid(state, f.slug)
            pair = tuple(f.subjects)
            image, layout = compose(state, BANDS[f.era], pair[0], pair[1], used[pair])
            used[pair] += 1
            image = image.resize((96, 96), Image.Resampling.LANCZOS)
            relative = "%s/focus/%s.dds" % (BASE, ident)
            texture(relative, image, "original focus composition", "GFX_ac_ud_focus_" + ident,
                    tag=state.TAG, band=BANDS[f.era], primary=pair[0], secondary=pair[1], composition=layout)
            focus_hashes.append(assets[-1]["sha256"])
            sprites.extend(seams.focus_sprites("minors_b", ident))
        idea_used = Counter()
        for i in state.IDEAS:
            ident = build.idea_id(state, i.slug)
            pair = tuple(i.subjects)
            image, layout = compose(state, None, pair[0], pair[1], (idea_used[pair] + 3) % len(LAYOUTS))
            idea_used[pair] += 1
            relative = "%s/ideas/%s.dds" % (BASE, ident)
            texture(relative, image.resize((75, 75), Image.Resampling.LANCZOS), "original national spirit artwork",
                    "GFX_idea_" + ident, tag=state.TAG, composition=layout)
            sprites.append('spriteType = { name = "GFX_idea_%s" texturefile = "%s" }' % (ident, relative))
        for r in state.REGIMES:
            ident = "%s_%s" % (state.TAG, r.slug)
            relative = "%s/office/%s.dds" % (BASE, ident)
            texture(relative, portrait(state, r), "original unnamed office card (no face)", "GFX_ac_ud_minb_office_" + ident, tag=state.TAG)
            sprites.append('spriteType = { name = "GFX_ac_ud_minb_office_%s" texturefile = "%s" }' % (ident, relative))
        image, _ = compose(state, None, "assembly", "document", 1)
        relative = "%s/decision/%s.dds" % (BASE, state.TAG)
        texture(relative, image.resize((32, 32), Image.Resampling.LANCZOS), "original decision artwork",
                "GFX_decision_ac_ud_minb_" + state.TAG.lower(), tag=state.TAG)
        sprites.append('spriteType = { name = "GFX_decision_ac_ud_minb_%s" texturefile = "%s" }' % (state.TAG.lower(), relative))
    if len(focus_hashes) != len(set(focus_hashes)):
        raise SystemExit("Every focus needs a distinct rendered composition")
    category = Image.new("RGBA", (192, 192))
    draw = ImageDraw.Draw(category)
    draw.ellipse((10, 10, 182, 182), fill=NAVY, outline=EDGE, width=4)
    LIB.glyph(category, "diplomacy", (40, 40, 112, 100), WHITE)
    LIB.glyph(category, "document", (74, 130, 44, 40), LIB.GOLD)
    relative = "%s/category.dds" % BASE
    texture(relative, category.resize((100, 100), Image.Resampling.LANCZOS), "original decision category artwork",
            "GFX_decision_category_ac_ud_minors_b")
    sprites.append('spriteType = { name = "GFX_decision_category_ac_ud_minors_b" texturefile = "%s" }' % relative)
    out[MOD / "interface/ac_ud_minors_b.gfx"] = ("spriteTypes = {\n\t" + "\n\t".join(sprites) + "\n}\n").encode("utf-8")
    sources = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
               for p in [HERE / "build_art.py", HERE / "schema.py", ROOT / "tools/usea_expansion/build_art.py"]}
    manifest = {"schema": 1, "renderer": "Pillow 11.3.0", "source_layer": "original code-native Ulysses artwork",
                "source_hashes": sources, "source_hash_encoding": "UTF-8 with normalized LF newlines",
                "focus_compositions": len(focus_hashes), "no_baked_captions": True, "no_faces": True, "assets": assets}
    out[HERE / "assets.json"] = (json.dumps(manifest, indent=1) + "\n").encode("utf-8")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = outputs()
    failures = []
    for path, content in data.items():
        if args.check:
            current = path.read_bytes() if path.exists() else None
            if current is None or (current != content and current.replace(b"\r\n", b"\n") != content):
                failures.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if failures:
        raise SystemExit("Minors B artwork differs: " + ", ".join(failures[:10]) + (" ..." if len(failures) > 10 else ""))
    print("Minors B artwork: %d textures and one sprite file %s" % (len(data) - 2, "verified" if args.check else "packaged"))


if __name__ == "__main__":
    main()
