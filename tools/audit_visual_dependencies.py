#!/usr/bin/env python3
"""Audit every explicit art path and fail on unresolved focus/dashboard visuals.

The repository's old hash audit detects copied files, not references to engine
sprites. This audit intentionally distinguishes resolved Ulysses textures from
unresolved engine fallbacks; use --strict-all when all borrowed sprites are gone.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

MOD = Path(__file__).resolve().parents[1] / "mod" / "2985041246"
GFX_RE = re.compile(r'\btexturefile\s*=\s*(?:"([^"]+)"|([^\s}#]+))', re.I)
SPRITE_RE = re.compile(r"(?i)\bspriteType\s*=\s*\{")
NAME_RE = re.compile(r'\bname\s*=\s*"?(GFX_[A-Za-z0-9_]+)', re.I)
FOCUS_RE = re.compile(r"(?m)^\s*icon\s*=\s*(GFX_[A-Za-z0-9_]+)\s*(?:#.*)?$")
GUI_SPRITE_RE = re.compile(r'\b(?:spriteType|quadTextureSprite)\s*=\s*"(GFX_[A-Za-z0-9_]+)"')

def normal(path: str) -> str:
    return re.sub(r"/+", "/", path.replace("\\", "/")).lstrip("/").lower()

def blocks(text: str):
    for match in SPRITE_RE.finditer(text):
        start = match.end()
        depth = 1
        pos = start
        quoted = False
        while pos < len(text) and depth:
            c = text[pos]
            if c == '"' and (pos == 0 or text[pos - 1] != "\\"):
                quoted = not quoted
            elif not quoted:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
            pos += 1
        yield text[start:pos - 1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-all", action="store_true",
                        help="Fail if ANY authored .gfx texture is not shipped with Ulysses")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    images = {normal(str(p.relative_to(MOD))) for p in MOD.rglob("*") if p.is_file()}
    artwork = {}
    missing_textures = []
    count = 0
    for path in sorted(MOD.rglob("*.gfx")):
        for block in blocks(path.read_text(encoding="utf-8-sig")):
            name = NAME_RE.search(block)
            texture = GFX_RE.search(block)
            if not name or not texture:
                continue
            count += 1
            sprite = name.group(1)
            asset = normal(texture.group(1) or texture.group(2))
            # Multiple definitions can coexist. Prefer one with local artwork.
            locally_owned = asset in images
            if sprite not in artwork or locally_owned:
                artwork[sprite] = (locally_owned, asset)
            if not locally_owned:
                missing_textures.append((str(path.relative_to(MOD)), sprite, asset))

    # Completed graphical families may not regain engine-supplied artwork.
    clean_art_files = {
        "interface/Technologies.gfx",
        "interface/ac_tech_icons.gfx",
        "interface/ac_goals.gfx",
    }
    visual_regressions = [x for x in missing_textures if x[0] in clean_art_files]
    # Four inherited aircraft-role and multi-frame niche strip entries still
    # require purpose-built sprite sheets; do not allow any new fallbacks.
    plane_remainder = [x for x in missing_textures if x[0] == "interface/ac_plane_modules_icons.gfx"]
    if len(plane_remainder) > 4:
        visual_regressions.extend(plane_remainder)
    # All land counters should use mod art; unconverted naval counters remain.
    visual_regressions.extend(x for x in missing_textures
                              if x[0] == "interface/subuniticons.gfx"
                              and not (x[2].startswith("gfx/interface/counters/ships_small/")
                                       or x[2].startswith("gfx/interface/navalcombat/ships/")))

    focus_icons = []
    bad_focus = []
    for path in sorted((MOD / "common" / "national_focus").glob("*.txt")):
        for line, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            match = FOCUS_RE.match(raw)
            if not match:
                continue
            sprite = match.group(1)
            focus_icons.append((path.name, line, sprite))
            if sprite not in artwork or not artwork[sprite][0]:
                bad_focus.append((path.name, line, sprite))

    gui = (MOD / "interface" / "ac_economy_gui.gui").read_text(encoding="utf-8-sig")
    sg = (MOD / "common" / "scripted_guis" / "ac_economy.txt").read_text(encoding="utf-8-sig")
    category = (MOD / "common" / "decisions" / "categories" / "ac_economy_categories.txt").read_text()
    economy_visuals = sorted(set(GUI_SPRITE_RE.findall(gui)))
    bad_economy_visuals = [x for x in economy_visuals if x not in artwork or not artwork[x][0]]
    problems = []
    if "parent_window_token = politics_tab" in sg:
        problems.append("Legacy politics-tab economy launcher remains")
    if "parent_window_token = top_bar" not in sg:
        problems.append("Economy launcher is not HUD/topbar anchored")
    if "visible = { always = no }" not in category:
        problems.append("Duplicate economy Decisions panel is still visible")
    for old in ("MILS_COST_LOC", "CIVS_COST_LOC", "DOCKS_COST_LOC", "GFX_browser_forward",
                "GFX_tiled_plain_bg", "GFX_closebutton"):
        if old in gui:
            problems.append("Legacy/vanilla economy UI remains: " + old)
    for effect in (
        "ac_econ_refresh_budget", "ac_econ_borrow", "ac_econ_repay",
        "ac_econ_set_low_tax", "ac_econ_set_standard_tax",
        "ac_econ_set_high_tax", "ac_econ_set_basic_services",
        "ac_econ_set_reconstruction", "ac_econ_order_infantry",
        "ac_econ_cancel_procurement"
    ):
        if effect + " = yes" not in sg:
            problems.append("Missing GUI economic action: " + effect)

    report = {
        "authored_sprite_definitions": count,
        "focus_icons_checked": len(focus_icons),
        "regressions_in_cleaned_visual_families": visual_regressions,
        "focus_icons_borrowing_vanilla_or_missing": bad_focus,
        "economy_ui_sprites": economy_visuals,
        "economy_ui_missing_or_vanilla_sprites": bad_economy_visuals,
        "economy_contract_problems": problems,
        "all_gfx_missing_asset_references": len(missing_textures),
        "all_gfx_missing_asset_by_file": dict(sorted(Counter(x[0] for x in missing_textures).items())),
        "all_gfx_missing_samples": missing_textures[:20]
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for key, value in report.items():
            if key not in ("all_gfx_missing_samples", "focus_icons_borrowing_vanilla_or_missing"):
                print(key, "=", value)
        for item in bad_focus[:20]:
            print("UNRESOLVED FOCUS", *item)
    if bad_focus or bad_economy_visuals or problems or visual_regressions:
        raise SystemExit(1)
    if args.strict_all and missing_textures:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
