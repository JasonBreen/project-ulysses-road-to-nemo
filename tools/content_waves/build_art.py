"""Reproducible original artwork for content waves A and D.

Every texture is composed in code from the original Ulysses glyph library
(tools/usea_expansion/build_art.py); no installed-game, DLC or remote pixels and
no baked captions are used. This file and content definitions are the masters.
Run without arguments to regenerate; --check is read-only. Requires the
CI-pinned Pillow 11.3.0: DDS bytes are reproducible exactly; PNG masters and
galleries are compared by size and RGBA because compression varies by platform.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import sys

import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / "mod/2985041246"
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools/usea_expansion")]

from content_waves.framework import branch_id, focus_id  # noqa: E402
from content_waves import free_erusea, nordennavic  # noqa: E402
from content_waves.build import outputs as content_outputs  # noqa: E402
from event_picture_fit.fit import contain, same_review_png  # noqa: E402
from event_picture_fit.bitmap import BitmapFont  # noqa: E402
from script import parse  # noqa: E402

LIBRARY = ROOT / "tools/usea_expansion/build_art.py"
_spec = importlib.util.spec_from_file_location("content_waves_original_glyphs", LIBRARY)
glyphs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(glyphs)

NAVY = (8, 22, 33, 255)
LIGHT = (222, 238, 243, 255)
EDGE = (43, 78, 99, 255)
GOLD = (194, 165, 97, 255)
GRID = (18, 40, 54, 255)
ACCENT = {"ERU": (226, 132, 104, 255), "FCU": (104, 190, 226, 255), "NEC": (148, 214, 206, 255)}
SHAPES = {
    "ERU": [(30, 14), (162, 14), (178, 34), (178, 150), (150, 178), (42, 178), (14, 150), (14, 34)],
    "FCU": [(96, 10), (176, 42), (176, 140), (148, 176), (44, 176), (16, 140), (16, 42)],
    "NEC": [(22, 22), (96, 10), (170, 22), (180, 150), (158, 178), (34, 178), (12, 150)],
}
ARRANGEMENTS = [((26, 25, 119, 111), (126, 112, 45, 46)), ((23, 40, 93, 109), (111, 58, 65, 75)),
                ((55, 26, 110, 113), (26, 116, 46, 44)), ((45, 26, 104, 94), (65, 122, 66, 42)),
                ((26, 29, 109, 100), (110, 102, 61, 59)), ((41, 76, 111, 84), (73, 24, 47, 45))]
WAVES = ((free_erusea.WAVE, "free_erusea"), (nordennavic.WAVE, "nordennavic"))
OWNER_IDEAS = {"ac_fe_pressure_severe": ("security", "refugees"), "ac_fe_pressure_active": ("security", "communications"),
               "ac_fe_pressure_low": ("security", "civil"), "ac_fe_emergency_administration": ("command", "document"),
               "ac_fe_partner_assistance": ("diplomacy", "security"), "ac_fe_fcu_support_commitment": ("diplomacy", "command")}


def encoded(image, kind="DDS"):
    output = io.BytesIO()
    image.save(output, format=kind)
    return output.getvalue()


def frame(tag, settled=False):
    image = Image.new("RGBA", (192, 192))
    d = ImageDraw.Draw(image)
    accent = ACCENT[tag]
    shape = SHAPES[tag]
    d.polygon(shape, fill=NAVY)
    d.line(shape + [shape[0]], fill=accent, width=3)
    if tag == "ERU":
        d.line((40, 166, 152, 166), fill=EDGE, width=2)
    elif tag == "FCU":
        d.arc((44, 128, 148, 176), 0, 180, fill=EDGE, width=2)
    else:
        d.line((30, 160, 70, 168, 122, 168, 162, 160), fill=EDGE, width=2)
    if settled:
        d.line((52, 180, 140, 180), fill=GOLD, width=3)
        d.polygon([(87, 176), (96, 169), (105, 176), (96, 184)], fill=GOLD)
    return image


def composition(tag, primary, secondary, layout=0, settled=False):
    image = frame(tag, settled)
    a, b = ARRANGEMENTS[layout % len(ARRANGEMENTS)]
    glyphs.glyph(image, primary, a, LIGHT)
    glyphs.glyph(image, secondary, b, ACCENT[tag])
    return image


def row_icon(tag, subject, cancel=False):
    image = Image.new("RGBA", (104, 116))
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((5, 5, 98, 110), radius=11, fill=NAVY, outline=ACCENT[tag], width=5)
    glyphs.glyph(image, subject, (18, 19, 68, 75), LIGHT)
    if cancel:
        d.line((22, 95, 81, 25), fill=GOLD, width=7)
    return image.resize((26, 29), Image.Resampling.LANCZOS)


def scene(tag, subjects, news=False):
    image = Image.new("RGBA", (640, 260), NAVY)
    d = ImageDraw.Draw(image)
    accent = ACCENT[tag]
    d.rounded_rectangle((8, 8, 631, 251), radius=8, outline=accent, width=3)
    for x in range(32, 625, 24):
        d.line((x, 24, x, 235), fill=GRID, width=1)
    for y in range(34, 240, 24):
        d.line((25, y, 615, y), fill=GRID, width=1)
    d.line((35, 218, 606, 218), fill=EDGE, width=2)
    glyphs.glyph(image, subjects[0], (70, 32, 187, 169), LIGHT)
    glyphs.glyph(image, subjects[1], (361, 55, 149, 145), accent)
    d.line((272, 128, 338, 128), fill=accent, width=3)
    d.polygon([(338, 128), (327, 121), (327, 135)], fill=accent)
    d.line((70, 232, 257, 232), fill=GOLD if news else EDGE, width=2)
    return image


def idea_subjects(wave, ident):
    if ident in OWNER_IDEAS:
        return OWNER_IDEAS[ident], 3
    for b in wave.branches:
        stem = focus_id(wave, b, 0)[:-len("_register")]
        if not ident.startswith(stem + "_"):
            continue
        if "_service_" in ident:
            return b.subjects[0 if "_service_1_" in ident else 3], 4
        if "_reply_" in ident:
            return b.subjects[1 if "_public_" in ident else 2], 5
        index = 1 if "_policy_a_" in ident else 2
        return b.subjects[index], 1 if ident.endswith("_settled") else 0
    tag = ident[:3]
    primary, secondary = wave.themes[tag]
    if "_ministerial_" in ident or "_readiness_" in ident:
        primary, secondary = secondary, primary
    return (primary, secondary), 2 if "_opening_" in ident else 3


def outputs():
    if PIL.__version__ != "11.3.0":
        raise SystemExit("Reproducible art requires Pillow 11.3.0; current " + PIL.__version__)
    content, _ = content_outputs()
    result, assets, sprites = {}, [], []

    def texture(relative, image, sprite, role, tag, **metadata):
        data = encoded(image)
        result[MOD / relative] = data
        low, high = image.getchannel("A").getextrema()
        assets.append(dict(file=relative, sprite=sprite, role=role, tag=tag, width=image.width, height=image.height, frames=1,
                           alpha_min=low, alpha_max=high, format="DDS RGBA8", sha256=hashlib.sha256(data).hexdigest(),
                           source_layer="original procedural Ulysses glyph composition", **metadata))
        sprites.append(f'spriteType = {{ name = "{sprite}" texturefile = "{relative}" }}')

    for wave, name in WAVES:
        P = wave.prefix
        used = Counter()
        for b in wave.branches:
            for i, (primary, secondary) in enumerate(b.subjects):
                ident = focus_id(wave, b, i)
                key = (b.tag, primary, secondary)
                arrangement = used[key]
                used[key] += 1
                if arrangement >= len(ARRANGEMENTS):
                    raise ValueError("Add a deliberate arrangement for repeated subjects: " + str(key))
                image = composition(b.tag, primary, secondary, arrangement, settled=i == 5).resize((96, 96), Image.Resampling.LANCZOS)
                sprite = f"GFX_{P}_focus_{ident}"
                relative = f"gfx/AC_content_waves/focus/{ident}.dds"
                texture(relative, image, sprite, "focus", b.tag, id=ident, title=b.titles[i], primary=primary, secondary=secondary, arrangement=arrangement)
                sprites.append(f'spriteType = {{ name = "{sprite}_shine" texturefile = "{relative}" }}')
        ideas_file = parse(content[f"common/ideas/ac_{name}.txt"])
        for ident, _, _ in ideas_file[0][2][0][2]:
            (primary, secondary), layout = idea_subjects(wave, ident)
            image = composition(ident[:3] if ident[:3] in wave.countries else ("ERU" if ident != "ac_fe_fcu_support_commitment" else "FCU"),
                                primary, secondary, layout, settled=ident.endswith("_settled"))
            tag = ident[:3] if ident[:3] in wave.countries else ("FCU" if ident == "ac_fe_fcu_support_commitment" else "ERU")
            texture(f"gfx/AC_content_waves/ideas/{ident}.dds", image.resize((75, 75), Image.Resampling.LANCZOS), "GFX_idea_" + ident, "idea", tag,
                    id=ident, primary=primary, secondary=secondary)
        for tag, country in wave.countries.items():
            image = composition(tag, *wave.themes[tag], 3).resize((100, 100), Image.Resampling.LANCZOS)
            texture(f"gfx/AC_content_waves/categories/{P}_{tag.lower()}.dds", image, f"GFX_{P}_category_{tag.lower()}", "category", tag, title=country + ": " + wave.label)
        for category, _, entries in parse(content[f"common/decisions/ac_{name}.txt"]):
            tag = category.split("_")[-2].upper()
            for ident, _, _ in entries:
                branch = next((b for b in wave.branches if ident.startswith(focus_id(wave, b, 0)[:-len("_register")] + "_")), None)
                subject = branch.subjects[0 if ident.endswith("_1") else 3][0] if branch else wave.themes[tag][0]
                texture(f"gfx/AC_content_waves/decisions/{P}_{ident}.dds", row_icon(tag, subject, cancel="cancel_service" in ident),
                        f"GFX_decision_{P}_{ident}", "decision row", tag, id=ident)
        for tag, country in wave.countries.items():
            master = scene(tag, wave.themes[tag])
            ident = f"{tag.lower()}_national"
            result[HERE / "source/events" / f"{P}_{ident}.png"] = encoded(master, "PNG")
            texture(f"gfx/AC_content_waves/events/{P}_{ident}.dds", contain(master), f"GFX_{P}_event_{ident}", "event illustration", tag,
                    title=country + ": " + wave.label, master=f"tools/content_waves/source/events/{P}_{ident}.png",
                    transform="Full-source Lanczos contain to 210x176; opaque navy padding; no crop")
        for b in wave.branches:
            master = scene(b.tag, b.subjects[0])
            ident = branch_id(b)
            result[HERE / "source/events" / f"{P}_{ident}.png"] = encoded(master, "PNG")
            texture(f"gfx/AC_content_waves/events/{P}_{ident}.dds", contain(master), f"GFX_{P}_event_{ident}", "event illustration", b.tag,
                    title=b.titles[0], master=f"tools/content_waves/source/events/{P}_{ident}.png",
                    transform="Full-source Lanczos contain to 210x176; opaque navy padding; no crop")
    for ident, subjects, title in (("insurrection", ("security", "document"), "The Free Erusea Insurrection"),
                                   ("recedes", ("civil", "peace"), "The Insurrection Recedes")):
        master = scene("ERU", subjects, news=True)
        result[HERE / "source/events" / f"ac_fe_news_{ident}.png"] = encoded(master, "PNG")
        texture(f"gfx/AC_content_waves/events/ac_fe_news_{ident}.dds", contain(master, "news_event"), f"GFX_ac_fe_news_{ident}", "news illustration", "ERU",
                title=title, master=f"tools/content_waves/source/events/ac_fe_news_{ident}.png",
                transform="Full-source Lanczos contain to 397x153; opaque navy padding; no crop")

    result[MOD / "interface/ac_content_waves.gfx"] = ("spriteTypes = {\n" + "\n".join(sprites) + "\n}\n").encode()
    manifest = dict(schema=1, pillow="11.3.0", source_layer="original provisional artwork; no engine/DLC/remote pixels or baked text",
                    vector_sources=["tools/content_waves/build_art.py", "tools/content_waves/free_erusea.py", "tools/content_waves/nordennavic.py",
                                    "tools/usea_expansion/build_art.py", "tools/event_picture_fit/fit.py"],
                    glyph_library_sha256=hashlib.sha256(LIBRARY.read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
                    native="Not rendered in HOI4; native viewport/input acceptance remains pending", assets=assets)
    result[HERE / "assets.json"] = (json.dumps(manifest, indent=2) + "\n").encode()

    font = BitmapFont()
    for wave, _ in WAVES:
        for tag, country in wave.countries.items():
            rows = [(b, i) for b in wave.branches if b.tag == tag for i in range(6)]
            gallery = Image.new("RGBA", (1120, 70 + 220 * (len(rows) // 6)), NAVY)
            font.draw(gallery, country + ": " + wave.label, (24, 18), 1000)
            for n, (b, i) in enumerate(rows):
                x = 25 + (n % 6) * 183
                y = 62 + (n // 6) * 220
                icon = Image.open(io.BytesIO(result[MOD / f"gfx/AC_content_waves/focus/{focus_id(wave, b, i)}.dds"])).convert("RGBA")
                gallery.alpha_composite(icon, (x + 25, y))
                font.draw(gallery, b.titles[i], (x, y + 110), 153)
            result[HERE / "gallery" / f"{tag.lower()}-focuses.png"] = encoded(gallery, "PNG")
    # Link the per-country sheets rather than embedding PNG bytes, so the page
    # is byte-identical on every platform. Counts come from the manifest.
    counts = Counter((row["tag"], row["role"]) for row in assets)
    rows = "".join(f"<tr><td>{html.escape(tag)}</td><td>{html.escape(role)}</td><td>{n}</td></tr>" for (tag, role), n in sorted(counts.items()))
    sheets = "".join(f'<figure><img alt="{tag} focus icons" src="{tag.lower()}-focuses.png"><figcaption>{html.escape(country)}: {html.escape(wave.label)}</figcaption></figure>'
                     for wave, _ in WAVES for tag, country in wave.countries.items())
    page = ('<!doctype html><meta charset="utf-8"><title>Content waves original artwork</title><style>body{background:#081621;color:#daedf2;'
            'font:16px sans-serif;margin:28px}figure{margin:0 0 28px}img{max-width:100%}table{border-collapse:collapse}'
            'td{border:1px solid #34596b;padding:4px 10px}</style><h1>Content waves A and D: original artwork</h1>'
            '<p>Offline source review only. Not rendered in HOI4. Hashes are in tools/content_waves/assets.json.</p>'
            '<table><tr><td>Country</td><td>Role</td><td>Textures</td></tr>' + rows + '</table>' + sheets + "\n")
    result[HERE / "gallery/index.html"] = page.encode()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failures = []
    out = outputs()
    for path, data in out.items():
        if args.check:
            current = path.read_bytes() if path.exists() else None
            if current is not None and path.suffix in (".gfx", ".json", ".html"):
                current = current.replace(b"\r\n", b"\n")
            # PNG compression varies between platform builds of Pillow/zlib;
            # dimensions and RGBA must still match exactly. DDS stays byte-exact.
            same = current == data or (path.suffix == ".png" and current is not None and same_review_png(current, data))
            if not same:
                failures.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if failures:
        raise SystemExit("Content waves artwork differs: " + ", ".join(failures))
    print("Content waves original artwork:", len([p for p in out if p.suffix == ".dds"]), "DDS; " + ("consistent" if args.check else "generated"))


if __name__ == "__main__":
    main()
