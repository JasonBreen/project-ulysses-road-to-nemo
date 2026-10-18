"""Port archive-only equipment references to native HOI4 1.19 identifiers."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPLACEMENTS = {
    "ifv_equipment_1": "mechanized_equipment_1",
    "modern_tank_equipment_0": "modern_tank_equipment_1",
    "main_battle_tank_0": "main_battle_tank",
    "basic_light_tank_chassis_chassis_chassis_chassis": "basic_light_tank",
    "basic_light_tank_chassis_chassis_chassis": "basic_light_tank",
    "basic_light_tank_chassis_chassis": "basic_light_tank",
    "basic_light_tank_chassis": "basic_light_tank",
    "basic_light_tank": "basic_light_tank",
    "antiair_1": "interwar_antiair",
    "spg_artillery_1": "basic_medium_art",
    "imv1": "armored_car1",
    "ifv1": "mechanised_infantry",
    "infantry_manpats": "infantry_at",
    "infantry_weapons1": "infantry_weapons",
}


def iter_targets(mod_root: Path):
    yield from (mod_root / "history" / "units").glob("*.txt")
    yield from (mod_root / "history" / "countries").glob("*.txt")
    yield mod_root / "common" / "national_focus" / "AWW_shared.txt"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    changed = 0
    for path in iter_targets(args.mod_root):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig")
        updated = text
        for old, new in REPLACEMENTS.items():
            updated = re.sub(
                rf"(?<![A-Za-z0-9_]){re.escape(old)}(?![A-Za-z0-9_])",
                new,
                updated,
            )
        if updated == text:
            continue
        changed += 1
        print(path)
        if args.apply:
            with path.open("w", encoding="utf-8", newline="") as handle:
                handle.write(updated)

    print(f"files_changed={changed} applied={args.apply}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
