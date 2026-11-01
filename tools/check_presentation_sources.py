"""Strictly parse authored presentation definitions; no game/DLC/native input.

Texture existence does not prove that the containing GUI/GFX/asset file can be
read. Keep this gate separate from texture, provenance and native acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/overhaul"))
from audit_consumers import get, parse, scalar, walk
from text_structure import validate_structure


def inspect(mod):
    trees = {}
    files, failures = [], []
    for folder in ("interface", "gfx", "sound", "music"):
        for path in sorted((mod / folder).rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".gui", ".gfx", ".asset"}:
                continue
            relative = path.relative_to(mod).as_posix()
            data = path.read_bytes()
            files.append(dict(path=relative, sha256=hashlib.sha256(data).hexdigest()))
            try:
                text = data.decode("utf-8-sig")
                validate_structure(text)
                trees[relative] = parse(text)
            except (ValueError, IndexError, UnicodeError) as exc:
                failures.append(dict(path=relative, problem=str(exc)))

    counters = "interface/subuniticons.gfx"
    if counters not in trees:
        failures.append(dict(path=counters, problem="Required counter source missing or unreadable"))
    names = [scalar(get(node, "name", "")) for kind, node in walk(trees.get(counters, []))
             if kind.lower() == "spritetype"]
    for name in ("GFX_group_infantry_icon", "GFX_group_mobile_icon", "GFX_group_armor_icon"):
        if name not in names:
            failures.append(dict(path=counters, problem="Required engine-bound group sprite missing: " + name))

    category_path = "sound/superevents_category.asset"
    categories = [node for key, _, node in trees.get(category_path, [])
                  if key == "category" and scalar(get(node, "name", "")) == "SuperEvents"]
    members = []
    if len(categories) != 1:
        failures.append(dict(path=category_path, problem="Expected exactly one readable SuperEvents category"))
    else:
        members = [key for key, _, _ in get(categories[0], "soundeffects", [])]
        sounds = {scalar(get(node, "name", "")) for path, tree in trees.items()
                  if path.startswith("sound/") for kind, node in walk(tree) if kind == "soundeffect"}
        for name in members:
            if name not in sounds:
                failures.append(dict(path=category_path, problem="Unresolved category sound: " + name))
        if not members:
            failures.append(dict(path=category_path, problem="SuperEvents category unexpectedly empty"))
    return dict(schema=1, coverage="Authored text parsing and named category/group bindings only; no native rendering or audio playback",
                checked_files=len(files), files=files, counter_sprite_definitions=len(names),
                superevent_category_members=members, failures=failures, passed=not failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod-root", type=Path, default=ROOT / "mod/2985041246")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = inspect(args.mod_root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in report.items() if key != "files"}, indent=2))
    raise SystemExit(not report["passed"])


if __name__ == "__main__":
    main()
