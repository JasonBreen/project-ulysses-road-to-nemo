#!/usr/bin/env python3
"""Report the static focus/decision/event graph for the campaign arc.

Inspired by MD-OEM's path-report tooling, but kept Ulysses-specific and
offline. The report describes references; it cannot prove engine reachability.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=Path(__file__).resolve().parents[2] / "mod" / "2985041246")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    mod = args.mod_root.resolve()
    focus = read(mod / "common" / "national_focus" / "ac_belkan_campaign.txt")
    decisions = read(mod / "common" / "decisions" / "ac_belkan_campaign.txt")
    events = read(mod / "events" / "ac_belkan_campaign.txt")
    result = {
        "focuses": sorted(set(re.findall(r"^\s*id\s*=\s*(ac_[A-Za-z0-9_]+)", focus, re.MULTILINE))),
        "focus_event_refs": sorted(set(re.findall(r"country_event\s*=\s*\{\s*id\s*=\s*(ac_campaign\.\d+)", focus))),
        "decision_event_refs": sorted(set(re.findall(r"country_event\s*=\s*\{\s*id\s*=\s*(ac_campaign\.\d+)", decisions))),
        "events": sorted(set(re.findall(r"^\s*id\s*=\s*(ac_campaign\.\d+)", events, re.MULTILINE))),
        "event_idea_refs": sorted(set(re.findall(r"(?:add|remove)(?:_timed)?_ideas?\s*=\s*(?:\{\s*idea\s*=\s*)?([A-Za-z0-9_]+)", events))),
        "decision_flags": sorted(set(re.findall(r"(?:set_country_flag|has_country_flag)\s*=\s*(?:\{\s*flag\s*=\s*)?([A-Za-z0-9_]+)", decisions))),
        "native_status": "not run; static references only",
    }
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Project Ulysses campaign path report")
        print("Static references only; this does not prove native reachability.")
        for key, values in result.items():
            if isinstance(values, list):
                print(f"\n{key} ({len(values)}):")
                for value in values:
                    print(f"  - {value}")
            else:
                print(f"\n{key}: {values}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
