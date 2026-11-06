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
    parser.add_argument('--campaign',choices=('belkan','ac04','ac05','all'),default='belkan')
    args = parser.parse_args()
    mod = args.mod_root.resolve()
    if args.campaign!='belkan':
        prefixes=['ac_campaigns']+(['ac_ucw'] if args.campaign=='ac04' else ['ac_circum_pacific'] if args.campaign=='ac05' else ['ac_ucw','ac_circum_pacific'])
        event_source='\n'.join(read(mod/'events'/(name+'.txt')) for name in prefixes)
        focus_source=read(mod/'common/national_focus/ac_campaigns.txt')
        decision_source=read(mod/'common/decisions/ac_campaigns.txt')
        owner_source='\n'.join(read(mod/'common'/folder/(name+'.txt')) for folder in ('scripted_effects','scripted_triggers') for name in prefixes)
        source='\n'.join((event_source,focus_source,decision_source,owner_source))
        definitions=set(re.findall(r'^\s*id\s*=\s*(ac_[\w]+\.\d+)',event_source,re.M))
        refs=set(re.findall(r'(?:country|news)_event\s*=\s*\{\s*id\s*=\s*(ac_[\w]+\.\d+)',source))
        owned=tuple({'ac_campaigns':'ac_camp.','ac_ucw':'ac_ucw.','ac_circum_pacific':'ac_cpw.'}[name] for name in prefixes)
        result=dict(campaign=args.campaign,focuses=sorted(set(re.findall(r'^\s*id\s*=\s*(\w+)',focus_source,re.M))),
                    events=sorted(definitions),event_refs=sorted(refs),unresolved_event_refs=sorted(r for r in refs-definitions if r.startswith(owned)),
                    external_event_refs=sorted(r for r in refs if not r.startswith(owned)),
                    flag_reads=sorted(set(re.findall(r'has_(?:country|global)_flag\s*=\s*(\w+)',source))),
                    native_status='not run; static references only')
        print(json.dumps(result,indent=2,sort_keys=True) if args.format=='json' else '\n'.join(f'{key}: {value}' for key,value in result.items()))
        return 1 if result['unresolved_event_refs'] else 0
    focus = read(mod / "common" / "national_focus" / "ac_belkan_campaign.txt")
    decisions = read(mod / "common" / "decisions" / "ac_belkan_campaign.txt")
    events = "\n".join(
        read(path)
        for path in (
            mod / "events" / "ac_belkan_campaign.txt",
            mod / "events" / "ac_continuation.txt",
        )
        if path.is_file()
    )
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
