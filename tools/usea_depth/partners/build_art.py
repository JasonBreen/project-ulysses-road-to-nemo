"""Package original code-drawn art for the Usea Depth partners package. --check never writes.

Draws with the shared Ulysses glyph library (seams.glyph_library(); its save(),
build_focuses() and main() are never called) and Pillow 11.3.0. No installed-game
pixels, fonts, faces, flags or captions are used. Outputs: one unique 96x96 icon per
focus (its shine reuses the same texture), 75x75 idea icons, 156x210 office cards
for the unnamed provisional governments and 210x176 event scenes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / "tools")]

from usea_depth import seams  # noqa: E402
from content import COUNTRIES, FOCUSES, IDEAS, REGIMES  # noqa: E402
from build import PICTURES, office  # noqa: E402

MOD = ROOT / "mod/2985041246"
ART = "gfx/AC_usea_depth/partners"
G = seams.glyph_library()
NAVY, EDGE, WHITE, CYAN, GOLD = G.NAVY, G.EDGE, G.WHITE, G.CYAN, G.GOLD
PANEL = (13, 32, 46, 255)
ACCENT = {"SNS": (226, 186, 112, 255), "AMB": (230, 148, 74, 255), "UGE": (122, 203, 166, 255), "DEL": (176, 158, 222, 255)}
ERAS = ("opening", "warning", "coup", "stonehenge", "impact", "refugees", "war", "postwar")
# Placements for (primary, secondary) glyphs on a 192px canvas.
LAYOUTS = [
    ((34, 30, 112, 108), (124, 112, 48, 46)),
    ((50, 26, 104, 100), (22, 112, 50, 48)),
    ((24, 40, 92, 96), (110, 54, 64, 70)),
    ((46, 22, 100, 92), (64, 118, 64, 42)),
    ((30, 30, 100, 96), (114, 100, 56, 56)),
    ((44, 72, 104, 84), (72, 22, 48, 44)),
    ((60, 34, 98, 104), (20, 36, 48, 48)),
    ((22, 56, 88, 92), (112, 26, 58, 58)),
]


def era(row):
    gates = set(row.gates)
    for key, name in (("postwar", "postwar"), ("war", "war"), ("refugee", "refugees"), ("impact", "impact"),
                      ("henge", "stonehenge"), ("coup", "coup"), ("warn", "warning"), ("prewin", "warning")):
        if key in gates:
            return name
    if row.y >= 18:
        return "postwar"
    if row.y >= 12:
        return "war"
    return "opening"


def frame(tag, period, size=192, political=False):
    image = Image.new("RGBA", (size, size))
    draw = ImageDraw.Draw(image)
    k = size / 192
    accent = ACCENT[tag]
    outline = {
        "SNS": [(96, 10), (172, 40), (182, 112), (148, 168), (96, 184), (44, 168), (10, 112), (20, 40)],
        "AMB": [(28, 14), (164, 14), (182, 52), (182, 150), (156, 180), (36, 180), (10, 150), (10, 52)],
        "UGE": [(96, 8), (180, 56), (180, 136), (96, 184), (12, 136), (12, 56)],
        "DEL": [(20, 20), (172, 20), (172, 160), (130, 184), (62, 184), (20, 160)],
    }[tag]
    points = [(round(x * k), round(y * k)) for x, y in outline]
    draw.polygon(points, fill=NAVY)
    draw.line(points + [points[0]], fill=accent, width=max(1, round(3 * k)))
    inner = [(round(96 * k + (x * k - 96 * k) * 0.9), round(96 * k + (y * k - 96 * k) * 0.9)) for x, y in outline]
    draw.line(inner + [inner[0]], fill=EDGE, width=max(1, round(1 * k)))
    # Era band: the same small mark per era across all four countries.
    index = ERAS.index(period)
    base = round(170 * k)
    for n in range(index + 1):
        x = round((96 - 4 * index + 8 * n) * k)
        draw.rectangle((x - round(2 * k), base - round(2 * k), x + round(2 * k), base + round(2 * k)), fill=accent if n == index else EDGE)
    if political:
        top = round(22 * k)
        draw.polygon([(round(96 * k), top - round(6 * k)), (round(102 * k), top), (round(96 * k), top + round(6 * k)), (round(90 * k), top)], fill=GOLD)
    return image


def composition(tag, period, primary, secondary, layout, political=False):
    if primary not in seams.SUBJECTS or secondary not in seams.SUBJECTS:
        raise ValueError("Unreviewed subject: %s/%s" % (primary, secondary))
    image = frame(tag, period, political=political)
    first, second = LAYOUTS[layout]
    G.glyph(image, primary, first, WHITE)
    G.glyph(image, secondary, second, ACCENT[tag])
    return image


def office_card(tag, subject):
    image = Image.new("RGBA", (156, 210), NAVY)
    draw = ImageDraw.Draw(image)
    accent = ACCENT[tag]
    draw.rectangle((6, 6, 149, 203), outline=EDGE, width=2)
    draw.rectangle((12, 12, 143, 197), outline=accent, width=1)
    draw.line((22, 30, 134, 30), fill=accent, width=2)
    draw.line((22, 180, 134, 180), fill=accent, width=2)
    draw.ellipse((28, 52, 128, 152), outline=accent, width=3)
    draw.ellipse((36, 60, 120, 144), outline=EDGE, width=1)
    G.glyph(image, subject, (48, 72, 60, 60), WHITE)
    G.glyph(image, "assembly", (66, 158, 24, 18), accent)
    return image


SCENES = {
    "politics": (("assembly", (64, 40, 82, 74)), ("ballot", (14, 98, 46, 44)), ("document", (150, 98, 46, 44))),
    "warning": (("telescope", (22, 70, 80, 80)), ("meteor", (118, 18, 70, 70))),
    "coup": (("security", (70, 36, 70, 80)), ("command", (14, 104, 44, 44)), ("communications", (152, 104, 44, 44))),
    "desert": (("radar", (72, 28, 66, 66)), ("meteor", (150, 14, 44, 44))),
    "impact": (("meteor", (28, 14, 60, 60)), ("meteor", (110, 30, 46, 46)), ("shelter", (70, 100, 70, 56))),
    "refugees": (("refugees", (58, 50, 94, 92)), ("gate", (152, 96, 44, 50))),
    "war": (("air", (110, 16, 70, 64)), ("security", (30, 72, 70, 76))),
    "peace": (("peace", (64, 34, 82, 82)), ("rebuild", (14, 104, 44, 44)), ("medal", (152, 104, 44, 44))),
    "yards": (("rail", (40, 56, 128, 84)), ("logistics", (150, 18, 46, 40))),
    "depots": (("logistics", (40, 58, 96, 74)), ("shelter", (140, 74, 52, 58))),
    "records": (("document", (40, 34, 78, 98)), ("scales", (118, 56, 66, 70))),
}


def scene(name):
    image = Image.new("RGBA", (210, 176), NAVY)
    draw = ImageDraw.Draw(image)
    for y in range(176):
        shade = int(18 + 22 * y / 175)
        draw.line((0, y, 209, y), fill=(8, shade, 30 + shade // 2, 255))
    horizon = 150
    draw.rectangle((0, horizon, 209, 175), fill=PANEL)
    draw.line((0, horizon, 209, horizon), fill=EDGE, width=2)
    if name == "desert":
        # Eight battery barrels on the horizon; original geometry, not a reproduction.
        for n in range(8):
            x = 20 + n * 23
            draw.line((x, horizon - 2, x + 14, horizon - 30), fill=GOLD, width=3)
            draw.rectangle((x - 4, horizon - 6, x + 6, horizon - 1), fill=EDGE)
    for index, (subject, rect) in enumerate(SCENES[name]):
        G.glyph(image, subject, rect, WHITE if index == 0 else CYAN)
    draw.rectangle((0, 0, 209, 175), outline=EDGE, width=2)
    return image


def outputs():
    if PIL.__version__ != "11.3.0":
        raise SystemExit("Use the reproducible Pillow 11.3.0 renderer; current version is " + PIL.__version__)
    files, assets = {}, []

    def texture(relative, image, role, **metadata):
        data = seams.encoded(image)
        files[MOD / relative] = data
        assets.append({"file": relative, "role": role, "width": image.width, "height": image.height, "frames": 1,
                       "format": "DDS RGBA8", "sha256": hashlib.sha256(data).hexdigest(), **metadata})

    used = {}
    for row in FOCUSES:
        pair = (row.tag, row.subjects[0], row.subjects[1])
        layout = used.get(pair, 0)
        used[pair] = layout + 1
        if layout >= len(LAYOUTS):
            raise ValueError("Add a deliberate layout for a repeated subject pair: %s" % (pair,))
        political = any(t.startswith(("regime:", "flag:")) for t in row.reward)
        image = composition(row.tag, era(row), row.subjects[0], row.subjects[1], layout, political)
        texture("%s/focus/%s.dds" % (ART, row.id), image.resize((96, 96), Image.Resampling.LANCZOS), "original focus icon",
                sprite="GFX_ac_ud_focus_" + row.id, shine="GFX_ac_ud_focus_%s_shine" % row.id, tag=row.tag, era=era(row),
                subjects=list(row.subjects), layout=layout)
    focus_hashes = [a["sha256"] for a in assets]
    if len(set(focus_hashes)) != len(FOCUSES):
        raise ValueError("Every focus needs a distinct rendered icon")
    for index, (ident, (_title, _desc, _modifier, subjects)) in enumerate(IDEAS.items()):
        tag = ident[:3]
        image = composition(tag, "postwar" if "after" in ident else "opening", subjects[0], subjects[1], (index % 3) + 5)
        texture("%s/ideas/%s.dds" % (ART, ident), image.resize((75, 75), Image.Resampling.LANCZOS), "original idea icon",
                sprite="GFX_idea_ac_ud_" + ident, tag=tag, subjects=list(subjects))
    for slug, row in REGIMES.items():
        ident = office(slug)
        texture("%s/portraits/%s.dds" % (ART, ident), office_card(row["tag"], row["subject"]),
                "original office card for an unnamed provisional government (no face, flag or caption)",
                sprite="GFX_ac_ud_portrait_" + ident, tag=row["tag"])
    for name in PICTURES:
        texture("%s/events/%s.dds" % (ART, name), scene(name), "original event scene", sprite="GFX_ac_ud_event_" + name)
    sources = [HERE / "content.py", HERE / "build.py", Path(__file__), ROOT / "tools/usea_expansion/build_art.py"]
    manifest = {"schema": 1, "package": "partners", "renderer": "Pillow 11.3.0",
                "source_layer": "original code-drawn Ulysses artwork; no installed-game pixels",
                "source_hashes": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest() for p in sources},
                "source_hash_encoding": "UTF-8 with normalized LF newlines",
                "focus_icons": len(FOCUSES), "idea_icons": len(IDEAS), "office_cards": len(REGIMES), "event_scenes": len(PICTURES),
                "no_baked_captions": True, "assets": assets}
    files[HERE / "assets.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failures = []
    for path, data in outputs().items():
        if args.check:
            current = path.read_bytes() if path.exists() else b""
            if path.suffix == ".json":
                current = current.replace(b"\r\n", b"\n")
            if current != data:
                failures.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if failures:
        raise SystemExit("Usea Depth partner artwork differs: " + ", ".join(failures[:10]) + (" ..." if len(failures) > 10 else ""))
    print("Usea Depth partner artwork: %d focus icons, %d idea icons, %d office cards, %d event scenes; %s"
          % (len(FOCUSES), len(IDEAS), len(REGIMES), len(PICTURES), "consistent" if args.check else "packaged"))


if __name__ == "__main__":
    main()
