"""Build original briefing decision chrome around the 1.19 control contract.

The capture step reads control metadata and image dimensions only. It never
imports engine pixels, fonts, audio, or executable code. Normal builds and
--check are independent of an installed game. Pillow packages original RGBA DDS.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import re
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / "mod/2985041246"
sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
from script import get, parse, render, setv, walk, xy

NAVY = (8, 22, 33, 255)
PANEL = (13, 32, 46, 255)
CYAN = (93, 208, 223, 255)
LIGHT = (218, 237, 242, 255)
GOLD = (230, 181, 95, 255)
MUTED = (52, 82, 98, 255)
RED = (204, 98, 104, 255)
CONTRACT = HERE / "decisions_contract.json"
ASSET_DIR = "gfx/interface/ac_overhaul/decisions"
SCROLLBAR = "ac_decisions_right_vertical_slider"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def scalar(value):
    return value.strip('"') if isinstance(value, str) else value


def refs(tree):
    return {scalar(value) for _, node in walk(tree) for key, _, value in node
            if key.lower() in ("spritetype", "quadtexturesprite")
            and isinstance(value, str) and value}


def capture(engine):
    """Record engine compatibility metadata, with no original image payloads."""
    source = engine / "interface/countrydecisionview.gui"
    tree = parse(source.read_text(encoding="utf-8-sig"))
    core = parse((engine / "interface/core.gui").read_text(encoding="utf-8-sig"))
    bars = [[kind, "=", node] for kind, node in walk(core)
            if kind.lower() == "extendedscrollbartype"
            and scalar(get(node, "name")) == "right_vertical_slider"]
    if len(bars) != 1:
        raise ValueError("Expected one reference decision scrollbar contract")
    source_defs = {}
    # Only direct compatibility fields are retained. Shader paths are references
    # to engine services, not copied shader contents.
    for path in sorted((engine / "interface").glob("*.gfx")):
        try:
            parsed = parse(path.read_text(encoding="utf-8-sig", errors="replace"))
        except (ValueError, IndexError):
            continue
        for kind, _, node in get(parsed, "spriteTypes", []):
            if not isinstance(node, list):
                continue
            name = scalar(get(node, "name", ""))
            if name:
                source_defs[name] = (kind, node, path)
    selected = refs(tree) | refs(bars)
    # Runtime defaults are selected in engine code even when no icon is written
    # in the decision/category. Shadow only the engine's decisions.gfx family;
    # authored national icons retain their existing definitions.
    runtime_source = engine / "interface/decisions.gfx"
    runtime = get(parse(runtime_source.read_text(encoding="utf-8-sig")), "spriteTypes", [])
    selected.update(scalar(get(node, "name", "")) for _, _, node in runtime
                    if isinstance(node, list))
    specs = []
    runtime_names = {scalar(get(node, "name", "")) for _, _, node in runtime
                     if isinstance(node, list)}
    for name in sorted(selected):
        if name not in source_defs:
            if name != "GFX_category_end_bg":
                raise ValueError("Missing engine sprite metadata: " + name)
            # 1.19.4's GUI requests category_end_bg, but its GFX defines only
            # event_end_bg. Supply an original separator rather than perpetuate
            # this unresolved inherited reference.
            specs.append(dict(name=name, kind="spriteType", frames=1, fields=[],
                              textures=[dict(field="texturefile", width=502, height=20)],
                              runtime=False, metadata_source="authored missing separator repair",
                              inherited_missing=True))
            continue
        kind, node, path = source_defs[name]
        textures = []
        for key, _, value in node:
            if key.lower() in ("texturefile", "texturefile1", "texturefile2"):
                relative = scalar(value).replace("\\", "/")
                source_image = engine / relative
                if source_image.suffix.lower() == ".dds":
                    header = source_image.read_bytes()[:128]
                    height, width = struct.unpack_from("<II", header, 12)
                else:
                    with Image.open(source_image) as image:
                        width, height = image.size
                textures.append(dict(field=key, width=width, height=height))
        if not textures:
            raise ValueError("Sprite has no recorded texture dimensions: " + name)
        fields = [[key, op, copy.deepcopy(value)] for key, op, value in node
                  if key.lower() not in ("name", "texturefile", "texturefile1", "texturefile2")]
        for field in fields:
            if field[0].lower() == "effectfile" and scalar(field[2]).endswith(".lua"):
                shader = scalar(field[2])[:-4] + ".shader"
                if (engine / shader).is_file():
                    field[2] = '"' + shader + '"'
        specs.append(dict(name=name, kind=kind, frames=int(get(node, "noOfFrames", "1")),
                          fields=fields, textures=textures,
                          runtime=name in runtime_names,
                          metadata_source=path.relative_to(engine).as_posix()))
    return dict(schema=1, source_layer="engine compatibility metadata only",
                engine_version="1.19.4.1", gui_sha256=sha(source.read_bytes()),
                gui=tree, scrollbar=bars, sprites=specs)


def new_name(spec):
    # Preserve runtime fallback names by replacing their owning engine file.
    return spec["name"] if spec["runtime"] else "GFX_ac_dec_" + spec["name"].removeprefix("GFX_")


def icon(draw, name, box, color):
    """Original, semantic briefing glyphs; no installed artwork is sampled."""
    x, y, w, h = box
    def line(points, width=2):
        draw.line([(x + round(a*w), y + round(b*h)) for a, b in points],
                  fill=color, width=max(1, width), joint="curve")
    words = name.lower()
    if "close" in words:
        line([(0.25, .25), (.75, .75)]); line([(.25, .75), (.75, .25)])
    elif "checkbox" in words:
        draw.rectangle((x+1, y+1, x+w-2, y+h-2), outline=color)
    elif "collapse" in words or "scroll_up" in words:
        line([(.2, .65), (.5, .3), (.8, .65)])
    elif "scroll_down" in words:
        line([(.2, .35), (.5, .7), (.8, .35)])
    elif "timer" in words:
        draw.ellipse((x+2, y+2, x+w-3, y+h-3), outline=color, width=2)
        line([(.5, .2), (.5, .5), (.72, .5)])
    elif "select" in words:
        line([(.2, .53), (.42, .76), (.82, .25)], 3)
    elif any(s in words for s in ("air", "plane", "pilot", "aviation")):
        line([(.5, .1), (.5, .9)]); line([(.1, .65), (.5, .4), (.9, .65)])
        line([(.3, .9), (.5, .75), (.7, .9)])
    elif any(s in words for s in ("naval", "navy", "fleet", "ship")):
        line([(.1, .6), (.9, .6), (.7, .85), (.3, .85), (.1, .6)])
        line([(.5, .6), (.5, .15), (.75, .4), (.5, .4)])
    elif any(s in words for s in ("industry", "factory", "production", "construction")):
        line([(.1, .9), (.1, .4), (.35, .55), (.35, .3), (.6, .5), (.6, .15), (.8, .15), (.8, .9), (.1, .9)])
    elif any(s in words for s in ("politic", "diploma", "government", "category")):
        line([(.1, .3), (.5, .08), (.9, .3), (.1, .3)])
        for a in (.25, .5, .75): line([(a, .4), (a, .82)])
        line([(.1, .92), (.9, .92)])
    elif any(s in words for s in ("research", "science", "technology")):
        draw.ellipse((x+2, y+2, x+w-3, y+h-3), outline=color, width=2)
        line([(.1, .5), (.9, .5)]); line([(.5, .1), (.5, .9)])
    elif any(s in words for s in ("war", "army", "military", "defen", "attack")):
        line([(.5, .05), (.88, .25), (.8, .7), (.5, .95), (.2, .7), (.12, .25), (.5, .05)])
        line([(.3, .4), (.7, .7)]); line([(.3, .7), (.7, .4)])
    elif "locator" in words or "infiltrate" in words:
        draw.ellipse((x+w*.2, y+h*.1, x+w*.8, y+h*.7), outline=color, width=2)
        line([(.22, .55), (.5, .95), (.78, .55)])
    else:
        line([(.2, .08), (.65, .08), (.85, .28), (.85, .92), (.2, .92), (.2, .08)])
        line([(.65, .08), (.65, .28), (.85, .28)])
        for b in (.43, .58, .73): line([(.32, b), (.72, b)], 1)


def artwork(spec, texture):
    w, h, frames = texture["width"], texture["height"], spec["frames"]
    # Two inherited strips have fractional frame widths. Authored sheets use
    # complete integer frames; record source dimensions separately below.
    w = ((w + frames - 1) // frames) * frames
    name = spec["name"].lower()
    image = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fw = w // frames
    mask = "mask" in name or spec["kind"].lower() == "maskedshieldtype"
    for frame in range(frames):
        tile = Image.new("RGBA", (fw, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(tile)
        color = (CYAN, LIGHT, GOLD, MUTED)[frame % 4]
        if "transparent" in name or "empty_picture" in name:
            pass
        elif spec["kind"].lower() == "maskedshieldtype":
            # Original opaque mask + transparent border aperture. The engine
            # supplies the country's own national flag through maskedflag.lua.
            if texture["field"].lower().endswith("2"):
                d.rectangle((1, 1, fw-2, h-2), fill=(255, 255, 255, 255))
            else:
                d.rectangle((0, 0, fw-1, h-1), outline=CYAN)
        elif "flag" in name:
            d.rectangle((0, 0, fw-1, h-1), outline=color)
        elif "progress" in name:
            # textureFile1 is the completed portion; textureFile2 is the
            # remainder. An opaque identical pair conceals every timer change.
            fill = (RED if "bad" in name else CYAN) if texture['field'].lower().endswith('1') else MUTED
            d.rectangle((0, 0, fw-1, h-1), fill=fill)
        elif any(s in name for s in ("header_bg", "item_bg", "end_bg", "tiled", "scroll_track", "scrollbar_vertical_bg")):
            d.rectangle((0, 0, fw-1, h-1), fill=PANEL if "item" in name else NAVY)
            d.line((0, h-1, fw-1, h-1), fill=MUTED)
            if "header" in name:
                d.rectangle((0, 0, min(3, fw-1), h-1), fill=CYAN)
                d.line((0, 0, fw-1, 0), fill=MUTED)
            if "item" in name and frame == 1:
                d.rectangle((0, 0, fw-1, h-1), outline=CYAN)
            if "item" in name and frame == 2:
                d.rectangle((0, 0, fw-1, h-1), outline=GOLD)
        elif "scroll_drager" in name:
            d.rectangle((1, 0, fw-2, h-1), fill=MUTED, outline=CYAN)
        else:
            if any(s in name for s in ("checkbox", "select", "close", "collapse")):
                d.rectangle((0, 0, fw-1, h-1), fill=PANEL, outline=MUTED)
            margin = max(1, min(fw, h)//8)
            icon(d, name, (margin, margin, fw-2*margin, h-2*margin), color)
            if "checkbox" in name and frame > 0:
                d.line([(fw*.25, h*.5), (fw*.45, h*.7), (fw*.8, h*.25)], fill=color, width=2)
        image.alpha_composite(tile, (frame*fw, 0))
    return image


def build(contract):
    tree = copy.deepcopy(contract["gui"])
    scrollbar = copy.deepcopy(contract["scrollbar"])
    setv(scrollbar[0][2], "name", '"' + SCROLLBAR + '"')
    tree[0][2].extend(scrollbar)
    names = {spec["name"]: new_name(spec) for spec in contract["sprites"]}
    for kind, node in walk(tree):
        for field in ("spriteType", "quadTextureSprite"):
            value = scalar(get(node, field))
            if value:
                setv(node, field, '"' + names[value] + '"')
        for field in ("font", "buttonFont"):
            if get(node, field):
                setv(node, field, '"ACBriefing20"' if scalar(get(node, "name")) == "decisionview_title" else '"ACBriefing16"')
        if scalar(get(node, "verticalScrollbar")) == "right_vertical_slider":
            setv(node, "verticalScrollbar", '"' + SCROLLBAR + '"')
        name = scalar(get(node, "name", ""))
        if name == "decisionview_title":
            setv(node, "position", xy(24, 13)); setv(node, "maxHeight", "24")
        if name == "decision_grid_container":
            setv(node, "vertical_scroll_step", "104")
        if name == "category_header":
            for _, child in walk([[kind, "=", node]]):
                if scalar(get(child, "name")) == "name_text":
                    setv(child, "position", xy(74, 20)); setv(child, "maxHeight", "32")
                    setv(child, "maxWidth", "354"); setv(child, "format", "left")
        if name in ("events_popup_text", "minor_events_popup_text", "news_popup_text"):
            setv(node, "maxHeight", "20")
        if name == "event_item":
            for _, child in walk([[kind, "=", node]]):
                if scalar(get(child, "name")) == "name_text":
                    setv(child, "maxWidth", "285")
        if name in ("decision_item", "timed_decision_item", "targeted_decision_item"):
            setv(node, "size", [["width", "=", "100%"], ["height", "=", "104"]])
            for _, child in walk([[kind, "=", node]]):
                child_name = scalar(get(child, "name"))
                if child_name == "name_text":
                    setv(child, "position", xy(62, 4)); setv(child, "maxWidth", "356")
                    setv(child, "maxHeight", "54")
                elif child_name == "cost_and_timer_text":
                    setv(child, "position", xy(62, 62)); setv(child, "maxHeight", "22")
                    setv(child, "maxWidth", "180")
                elif child_name == "timer_text":
                    setv(child, "position", xy(260, 62)); setv(child, "maxWidth", "130"); setv(child, "maxHeight", "22")
                elif child_name == "track_decision_checkbox":
                    setv(child, "position", xy(429, 18))
                elif child_name == "btn_select":
                    setv(child, "position", xy(464, 17))
                elif child_name == "timer_icon":
                    setv(child, "position", xy(480, 40))
                elif child_name in ("btn_progress_good", "btn_progress_bad"):
                    setv(child, "position", xy(9, 90))
        if name == "on_map_decision_locator_item":
            setv(node, "size", [["width", "=", "100%"], ["height", "=", "56"]])
    outputs = {"interface/countrydecisionview.gui":
               ("# Authored ACES decision presentation; engine control metadata preserved.\n" + render(tree) + "\n").encode()}
    sprites = []; runtime = []; assets = []
    specifications = copy.deepcopy(contract["sprites"])
    for spec in specifications:
        if spec["name"] == "GFX_decision_item_bg":
            for texture in spec["textures"]:
                texture["height"] = 104
    # Authored archive scripts contain these unresolved icon tokens. Keep the
    # gameplay scripts stable and give each runtime convention a real binding.
    for name in ("GFX_decision_mission_icon", "GFX_decision_xxx", "GFX_decision_XXX",
                 "GFX_decision_placeholder", "GFX_decision_category_XXX", "GFX_decision_category_placeholder"):
        if not any(s["name"] == name for s in specifications):
            width = 70 if "category" in name else 38
            specifications.append(dict(name=name, kind="spriteType", frames=1, fields=[], runtime=True,
                                       textures=[dict(field="texturefile", width=width, height=width)]))
    for spec in specifications:
        body = [["name", "=", '"' + new_name(spec) + '"']] + copy.deepcopy(spec["fields"])
        for index, texture in enumerate(spec["textures"]):
            # GFX identifiers can differ only by case, but Windows paths cannot.
            # A content-independent identifier digest prevents those collisions.
            identity = new_name(spec) + ("_" + str(index) if len(spec["textures"]) > 1 else "")
            relative = ASSET_DIR + "/" + identity + "_" + sha(identity.encode())[:8] + ".dds"
            image = artwork(spec, texture)
            buffer = io.BytesIO(); image.save(buffer, format="DDS")
            data = buffer.getvalue(); outputs[relative] = data
            body.append([texture["field"], "=", '"' + relative + '"'])
            assets.append(dict(file=relative, sprite=new_name(spec), width=image.width, height=image.height,
                               frames=spec["frames"], frame_width=image.width//spec["frames"],
                               compatibility_width=texture["width"],
                               alpha=list(image.getchannel("A").getextrema()), sha256=sha(data),
                               provenance="original procedural navy/cyan geometry",
                               source="tools/overhaul/build_decisions_ui.py", role="runtime icon" if spec["runtime"] else "decision chrome"))
        (runtime if spec["runtime"] else sprites).append([spec["kind"], "=", body])
    outputs["interface/countrydecisionview.gfx"] = ("# Original decision chrome; no engine image pixels imported.\n" + render([["spriteTypes", "=", sprites]]) + "\n").encode()
    outputs["interface/decisions.gfx"] = ("# Original runtime decision icon family, replacing engine fallback imagery.\n" + render([["spriteTypes", "=", runtime]]) + "\n").encode()
    manifest = dict(schema=1, source_layer="original procedural artwork",
                    compatibility_source="decisions_contract.json; engine control/format metadata only",
                    fonts="existing authored ACBriefing16/20; tools/usea_expansion/fonts.json",
                    native_status="not tested", assets=assets)
    return outputs, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-contract", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.capture_contract:
        CONTRACT.parent.mkdir(parents=True, exist_ok=True)
        CONTRACT.write_text(json.dumps(capture(args.capture_contract), indent=2) + "\n", encoding="utf-8")
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    outputs, manifest = build(contract)
    manifest_target = HERE / "decisions_assets.json"
    if not args.check and manifest_target.exists():
        previous = json.loads(manifest_target.read_text())
        wanted = {row["file"].lower() for row in manifest["assets"]}
        asset_root = (MOD / ASSET_DIR).resolve()
        for row in previous["assets"]:
            old = (MOD / row["file"]).resolve()
            # Delete only previously generated, directly owned DDS files.
            if old.parent == asset_root and old.suffix.lower() == ".dds" and row["file"].lower() not in wanted:
                old.unlink(missing_ok=True)
    for relative, data in outputs.items():
        target = MOD / relative
        if args.check:
            if not target.exists() or target.read_bytes() != data:
                raise SystemExit("Decision output differs: " + relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    target = HERE / "decisions_assets.json"
    data = (json.dumps(manifest, indent=2) + "\n").encode()
    if args.check:
        if not target.exists() or target.read_bytes() != data:
            raise SystemExit("Decision asset manifest differs")
    else:
        target.write_bytes(data)
    print(f"Decision UI: preserved control contract, {len(manifest['assets'])} original texture bindings; native rendering untested.")


if __name__ == "__main__":
    main()
