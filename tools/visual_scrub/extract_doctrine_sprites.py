#!/usr/bin/env python3
"""Record which sprites the installed doctrine definitions ask the engine for.

The mod does not ship common/doctrines, so the 1.17+ doctrine screens resolve
their card backgrounds, subdoctrine icons, milestone badges and ornaments from
the installed game. This reads a read-only installed reference and writes the
sprite names, roles, frame counts and texture dimensions that
build_fallthroughs.py must rebind. It copies no pixels and no script.

Run after a game patch, from the repository root:

    python -B tools/visual_scrub/extract_doctrine_sprites.py --reference-game-root <HOI4 folder>
    python -B tools/visual_scrub/build_fallthroughs.py
"""
from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path

OUT = Path(__file__).resolve().parent / "doctrine_sprites.json"
SPRITE_RE = re.compile(r"(?is)\b(?:spriteType|frameAnimatedSpriteType)\s*=\s*\{(.*?)\n\s*\}")
USE_RE = re.compile(r'\b(background|icon_frame|icon)\s*=\s*"?(GFX_\w+)')
BRANCHES = ("special_forces", "air", "land", "sea")


def active(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def dds_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        height, width = struct.unpack_from("<II", handle.read(32), 12)
    return width, height


def installed_sprites(game: Path) -> dict[str, tuple[str, str, int]]:
    found = {}
    for path in sorted((game / "interface").rglob("*.gfx")):
        for match in SPRITE_RE.finditer(active(path)):
            block = match.group(1)
            name = re.search(r'(?i)\bname\s*=\s*"?(GFX_\w+)', block)
            texture = re.search(r'(?i)texturefile\s*=\s*"?([^"\s]+)', block)
            frames = re.search(r"(?i)noOfFrames\s*=\s*(\d+)", block)
            if name and texture:
                found[name.group(1).lower()] = (name.group(1), re.sub(r"/+", "/", texture.group(1)), int(frames.group(1)) if frames else 1)
    return found


def extract(game: Path) -> dict[str, dict]:
    sprites = installed_sprites(game)
    rows: dict[str, dict] = {}
    root = game / "common" / "doctrines"
    for path in sorted(root.rglob("*.txt")):
        relative = path.relative_to(root).as_posix()
        branch = next((item for item in BRANCHES if item in relative), "land")
        for role, used in USE_RE.findall(active(path)):
            definition = sprites.get(used.lower())
            if definition is None:
                continue
            name, texture, frames = definition
            width, height = dds_size(game / texture)
            rows.setdefault(name, {"role": role, "branch": branch, "frames": frames, "width": width, "height": height})
    return dict(sorted(rows.items(), key=lambda item: item[0].lower()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-game-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true", help="fail if the recorded list differs from the installed reference")
    args = parser.parse_args()
    report = {
        "source": "sprite names, roles, frame counts and texture dimensions read from the installed 1.19.4.2 common/doctrines and interface definitions; no pixels copied",
        "sprites": extract(args.reference_game_root),
    }
    text = json.dumps(report, indent=2) + "\n"
    if args.check:
        if OUT.read_text(encoding="utf-8") != text:
            raise SystemExit("Installed doctrine sprites differ from doctrine_sprites.json; re-extract and rebuild the scrub")
    else:
        OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"{len(report['sprites'])} doctrine sprites")


if __name__ == "__main__":
    main()
