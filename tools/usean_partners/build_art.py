"""Package subject-led original vector artwork using the pinned Pillow renderer.

The editable sources are content.py, this compiler and the Ulysses glyph library.
No installed-game pixels, generated captions, serial-number uniqueness or remote
art are used. --check compares all texture, binding and review-artifact bytes.
"""
import argparse
import base64
from collections import Counter
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import sys

import PIL
from PIL import Image, ImageDraw, ImageFont
from content import COUNTRIES, FOCUSES, PHASES
from scopes import SCOPES

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; MOD = ROOT / "mod/2985041246"
FONT = ROOT / "tools/frontend_typography/source/DINish-Regular.ttf"
NAVY = (8, 22, 33, 255); WHITE = (218, 237, 242, 255); EDGE = (45, 85, 104, 255)
ACCENT = {"SNS": (93, 208, 223, 255), "AMB": (133, 204, 178, 255), "UGE": (143, 185, 224, 255), "DEL": (196, 169, 209, 255)}
LIBRARY = ROOT / "tools/usea_expansion/build_art.py"
spec = importlib.util.spec_from_file_location("ulysses_partner_symbols", LIBRARY)
symbols = importlib.util.module_from_spec(spec); spec.loader.exec_module(symbols)

LAYOUTS = [
    ("service-and-record", (28, 29, 119, 113), (128, 113, 45, 44)),
    ("paired-instruments", (21, 37, 93, 108), (110, 59, 65, 74)),
    ("foreground-and-context", (56, 28, 109, 112), (26, 116, 46, 44)),
    ("vertical-workflow", (47, 28, 102, 91), (65, 121, 66, 43)),
    ("diagonal-service", (28, 29, 108, 99), (110, 102, 60, 59)),
    ("fieldwork-and-plan", (42, 76, 109, 84), (73, 24, 47, 44)),
]
VALID = {"industry", "logistics", "air", "navy", "carrier", "submarine", "assembly", "ballot", "science", "radar", "diplomacy", "economy", "civil", "rebuild", "communications", "training", "command", "meteor", "missile", "gate", "refugees", "medical", "shelter", "rail", "tools", "telescope", "satellite", "document", "scales", "peace", "fishing", "runway", "bridge", "medal", "security"}


def encoded(image, format="DDS"):
    stream = io.BytesIO(); image.save(stream, format=format); return stream.getvalue()


def frame(tag, phase):
    image = Image.new("RGBA", (192, 192)); draw = ImageDraw.Draw(image); accent = ACCENT[tag]
    shape = {
        "SNS": [(25, 18), (166, 18), (177, 119), (150, 158), (96, 179), (40, 157), (15, 119)],
        "AMB": [(19, 23), (171, 23), (177, 148), (147, 173), (46, 173), (15, 148)],
        "UGE": [(96, 8), (174, 39), (179, 124), (147, 166), (45, 166), (13, 124), (18, 39)],
        "DEL": [(41, 14), (151, 14), (176, 39), (176, 147), (149, 175), (43, 175), (16, 147), (16, 39)],
    }[tag]
    draw.polygon(shape, fill=NAVY); draw.line(shape + [shape[0]], fill=accent, width=3)
    if phase == "administration":
        draw.line((48, 163, 70, 163), fill=EDGE, width=2); draw.line((122, 163, 144, 163), fill=EDGE, width=2)
    elif phase == "preparedness":
        draw.line((43, 156, 52, 166, 61, 156), fill=accent, width=2); draw.line((130, 156, 139, 166, 148, 156), fill=accent, width=2)
    elif phase == "response":
        draw.line((42, 163, 60, 156, 78, 163), fill=accent, width=2); draw.line((114, 163, 132, 156, 150, 163), fill=accent, width=2)
    else:
        draw.arc((37, 135, 155, 176), 0, 180, fill=accent, width=2)
    return image


def composition(tag, phase, primary, secondary, index):
    if primary not in VALID or secondary not in VALID:
        raise ValueError("Unreviewed subject: " + primary + "/" + secondary)
    if index >= len(LAYOUTS):
        raise ValueError("Add a deliberate composition for repeated subject pair")
    image = frame(tag, phase); arrangement = LAYOUTS[index]
    symbols.glyph(image, primary, arrangement[1], WHITE)
    symbols.glyph(image, secondary, arrangement[2], ACCENT[tag])
    return image, arrangement[0]


def outputs():
    if PIL.__version__ != "11.3.0":
        raise SystemExit("Use the reproducible Pillow 11.3.0 renderer; current version is " + PIL.__version__)
    from build import LEASES, policy_other
    output = {}; assets = []; sprites = []; directions = []; previews = []; scope_previews = []; used = Counter()

    def texture(relative, image, role, name, **metadata):
        data = encoded(image); output[MOD / relative] = data
        extrema = image.getchannel("A").getextrema()
        row = {"file": relative, "role": role, "sprite": name, "width": image.width, "height": image.height,
               "frame_width": image.width, "frames": 1, "format": "DDS RGBA8", "alpha_min": extrema[0], "alpha_max": extrema[1],
               "sha256": hashlib.sha256(data).hexdigest(), **metadata}
        assets.append(row); sprites.append(f'spriteType = {{ name = "{name}" texturefile = "{relative}" }}')
        return row

    for row in FOCUSES:
        pair = (row.tag, row.primary, row.secondary); ordinal = used[pair]; used[pair] += 1
        image, arrangement = composition(row.tag, row.phase, row.primary, row.secondary, ordinal)
        image = image.resize((96, 96), Image.Resampling.LANCZOS)
        relative = f"gfx/AC_usean_partners/focus/{row.id}.dds"; name = "GFX_ac_up_focus_" + row.id
        asset = texture(relative, image, "original focus composition", name, tag=row.tag, phase=row.phase,
                        primary=row.primary, secondary=row.secondary, composition=arrangement)
        sprites.append(f'spriteType = {{ name = "{name}_shine" texturefile = "{relative}" }}')
        directions.append({"id": row.id, "title": row.title, **asset})
        previews.append((row, image))
    if len(directions) != 228 or len({r["sha256"] for r in directions}) != 228:
        raise ValueError("Every focus needs a distinct rendered composition without a baked caption")
    for row in FOCUSES:
        if not policy_other(row):
            continue
        ident = row.id + "_spirit"
        image, _ = composition(row.tag, row.phase, row.primary, row.secondary, 4 if row.lane == 0 else 5)
        texture(f"gfx/AC_usean_partners/policies/{ident}.dds", image.resize((75, 75), Image.Resampling.LANCZOS),
                "original enduring policy artwork", "GFX_idea_ac_up_idea_" + ident, tag=row.tag, policy=ident)
    themes = {"SNS": ("communications", "shelter"), "AMB": ("industry", "rail"), "UGE": ("logistics", "bridge"), "DEL": ("scales", "command")}
    for scope in SCOPES:
        phase = max((row.phase for row in FOCUSES if row.id in {scope.tag + '_up_' + suffix for suffix in scope.requirements}), key=PHASES.index)
        image, _ = composition(scope.tag, phase, scope.primary, scope.secondary, 3)
        image = image.resize((75, 75), Image.Resampling.LANCZOS)
        scope_previews.append((scope, image))
        texture(f"gfx/AC_usean_partners/policies/{scope.id}_spirit.dds", image,
                "original operational-scope artwork", "GFX_idea_ac_up_idea_" + scope.id + "_spirit", tag=scope.tag, policy=scope.id + "_spirit")
    for tag in COUNTRIES:
        for index, (kind, title, primary, _) in enumerate(LEASES[tag]):
            ident = f"{tag}_up_{kind}_programme_spirit"
            secondary = themes[tag][1] if primary != themes[tag][1] else "document"
            image, _ = composition(tag, "response", primary, secondary, index % len(LAYOUTS))
            texture(f"gfx/AC_usean_partners/policies/{ident}.dds", image.resize((75, 75), Image.Resampling.LANCZOS),
                    "original temporary programme artwork", "GFX_idea_ac_up_idea_" + ident, tag=tag, policy=ident)
        image, _ = composition(tag, "settlement", *themes[tag], 2)
        texture(f"gfx/AC_usean_partners/policies/{tag}_national_programme.dds", image.resize((75, 75), Image.Resampling.LANCZOS),
                "original national programme modifier artwork", "GFX_idea_ac_up_" + tag.lower() + "_programme", tag=tag)
        for size, family in [(100, "category"), (32, "decision")]:
            image, _ = composition(tag, "administration", *themes[tag], 1)
            token = "ac_up_" + tag.lower() + ("_programmes" if family == "category" else "_programme")
            name = ("GFX_decision_category_" if family == "category" else "GFX_decision_") + token
            asset = texture(f"gfx/AC_usean_partners/{family}/{tag}.dds", image.resize((size, size), Image.Resampling.LANCZOS),
                            "original " + family + " artwork", name, tag=tag)
            if family == "category":
                sprites.append(f'spriteType = {{ name = "GFX_{token}" texturefile = "{asset["file"]}" }}')
    output[MOD / "interface/ac_usean_partners.gfx"] = ("spriteTypes = {\n" + "\n".join(sprites) + "\n}\n").encode()
    # Source hashes describe code, independent of Git's host newline checkout.
    source_hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
                     for p in [HERE / "content.py", HERE / "scopes.py", HERE / "scope_rules.py", HERE / "build.py", Path(__file__), LIBRARY]}
    manifest = {"schema": 1, "renderer": "Pillow 11.3.0", "source_layer": "original code-native Ulysses artwork",
                "source_hashes": source_hashes, "source_hash_encoding": "UTF-8 with normalized LF newlines", "focus_compositions": 228, "no_baked_focus_captions": True,
                "no_added_watermarks": True, "assets": assets}
    output[HERE / "assets.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    output[HERE / "focus_art.json"] = (json.dumps(directions, indent=2) + "\n").encode()
    sheet = Image.new("RGBA", (1440, 19 * 132), NAVY); draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(FONT), 10)
    for index, (row, image) in enumerate(previews):
        x, y = (index % 12) * 120, (index // 12) * 132
        sheet.alpha_composite(image, (x + 12, y + 1))
        words = row.title.split(); lines = [""]
        for word in words:
            if len(lines[-1] + word) > 21:
                lines.append("")
            lines[-1] += word + " "
        for n, line in enumerate(lines[:3]):
            draw.text((x + 60, y + 101 + n * 10), line.strip(), font=font, anchor="mt", fill=WHITE)
    evidence = ROOT / "docs/evidence/usean-partners"
    output[evidence / "focus-contact-sheet.png"] = encoded(sheet, "PNG")
    scope_sheet = Image.new("RGBA", (900, 6 * 140), NAVY); draw = ImageDraw.Draw(scope_sheet)
    for index, (scope, image) in enumerate(scope_previews):
        x, y = (index % 5) * 180, (index // 5) * 140
        scope_sheet.alpha_composite(image, (x + 52, y + 2))
        lines = [""]
        for word in (scope.tag + ": " + scope.title).split():
            if len(lines[-1] + word) > 28: lines.append("")
            lines[-1] += word + " "
        for n, line in enumerate(lines):
            draw.text((x + 90, y + 85 + n * 11), line.strip(), font=font, anchor="mt", fill=WHITE)
    output[evidence / "scope-contact-sheet.png"] = encoded(scope_sheet, "PNG")
    cards = []
    for row, image in previews:
        source = base64.b64encode(encoded(image, "PNG")).decode()
        cards.append(f'<article data-country="{row.tag}" data-phase="{row.phase}"><img alt="" src="data:image/png;base64,{source}"><h2>{html.escape(row.title)}</h2><p>{row.tag} · {row.phase}</p><small>{row.primary} / {row.secondary}</small></article>')
    page = '<!doctype html><meta charset="utf-8"><title>Usean partner focus artwork</title><style>body{background:#081621;color:#daedf2;font:15px system-ui;margin:24px}nav{position:sticky;top:0;background:#081621;padding:12px}button{background:#102b3b;color:#daedf2;border:1px solid #5dd0df;padding:8px;margin:3px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}article{border:1px solid #2d5568;padding:12px;text-align:center}img{width:96px;height:96px}h2{font-size:15px}small{color:#95b7cb}</style><h1>Usean partner artwork: 228 original compositions</h1><p>Subject-led code-native artwork. No baked focus captions or added watermark. Source and frame metadata are committed; native rendering remains untested.</p><nav>'
    page += ''.join(f'<button onclick="filter(\'{tag}\')">{tag}</button>' for tag in ['All', *COUNTRIES]) + '</nav><main>' + ''.join(cards) + '</main><script>function filter(country){for(const card of document.querySelectorAll("article"))card.hidden=country!=="All"&&card.dataset.country!==country}</script>'
    output[evidence / "artwork-gallery.html"] = page.encode()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    failures = []
    for path, data in outputs().items():
        if args.check:
            if not path.exists() or path.read_bytes() != data:
                failures.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    if failures:
        raise SystemExit("Usean partner artwork differs: " + ", ".join(failures))
    print("Usean partner artwork: 228 unique focuses, 75 spirits/modifiers and 8 decision/category textures; " + ("consistent" if args.check else "packaged"))


if __name__ == "__main__":
    main()
