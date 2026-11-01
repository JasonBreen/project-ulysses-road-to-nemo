"""Read-only independent review probe; writes only an explicitly named evidence file.

Uses actual generated histories/OOBs and captured technical contracts. It is not
a native game/save simulator. The stable checkpoint's contracts were separately
recomputed by the installed-reference source suite.
"""
from collections import Counter
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

AUDIT_ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(AUDIT_ROOT / "tools/usea_expansion"), str(AUDIT_ROOT / "tools/world_starts")]
from script import parse, get, walk
from inventory import selected


def inspect(root, label):
    root = root.resolve(); mod = root / "mod/2985041246"; inputs = {}; changed_during_read = set()
    def read(relative):
        path = root / relative; raw = path.read_bytes()
        metadata = dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                        modified_utc=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat())
        if relative in inputs and inputs[relative]["sha256"] != metadata["sha256"]:
            changed_during_read.add(relative)
        inputs.setdefault(relative, metadata)
        return raw.decode("utf-8-sig")
    profiles = json.loads(read("tools/world_starts/profiles.json"))["countries"]
    manifest = json.loads(read("tools/world_starts/foundation.json"))
    ideas = {}; groups = {}; defaults = {}
    for path in sorted((mod / "common/ideas").glob("*.txt")):
        tree = parse(read(path.relative_to(root).as_posix()))
        for group, _, entries in get(tree, "ideas", []):
            if not isinstance(entries, list): continue
            for name, _, node in entries:
                if not isinstance(node, list): continue
                ideas[name] = node; groups[name] = group
                if get(node, "default") == "yes": defaults[group] = name
    result = {}
    for tag, profile in profiles.items():
        row = manifest["countries"][tag]
        history = parse(read("mod/2985041246/" + row["country_history"]))
        core_pop = sum(s["manpower"] for s in row["baseline"].values() if tag in s["cores"])
        noncore_pop = sum(s["manpower"] for s in row["baseline"].values() if tag not in s["cores"])
        cases = []
        for key, contracts in row["recipe_contracts"].items():
            dlcs = {name for suffix, name in (("bba", "By Blood Alone"), ("mtg", "Man the Guns"), ("nsb", "No Step Back"))
                    if re.search(r"(?:^|_)" + suffix + "1(?:_|$)", key)}
            effects = list(selected(history, dlcs, tag)); active = dict(defaults); spirits = set()
            for name, _, value in effects:
                tokens = [value] if isinstance(value, str) else [k for k, _, _ in value] if isinstance(value, list) else []
                if name == "add_ideas":
                    for ident in tokens:
                        group = groups.get(ident)
                        if group in ("mobilization_laws", "economy", "trade_laws"):
                            active[group] = ident
                        else: spirits.add(ident)
                elif name == "remove_ideas":
                    for ident in tokens: spirits.discard(ident)
            laws = [active[g] for g in ("mobilization_laws", "economy", "trade_laws") if g in active]
            modifiers = Counter(); unknown = []
            for ident in laws + sorted(spirits):
                if ident not in ideas:
                    unknown.append(ident); continue
                for stat, _, value in get(ideas[ident], "modifier", []):
                    if stat in ("conscription", "conscription_factor", "min_export", "local_resources_factor", "fuel_gain_factor", "industrial_capacity_factory"):
                        modifiers[stat] += float(value)
            land = aircraft = ships = 0.; formations = planes = hulls = 0
            refs = [value.strip('"') for name, _, value in effects if name in ("set_oob", "load_oob", "set_air_oob", "set_naval_oob")]
            templates = {}
            for name in refs:
                tree = parse(read("mod/2985041246/history/units/" + name + ".txt"))
                for kind, _, node in tree:
                    if kind == "division_template":
                        templates[get(node, "name")] = sum(float(row["unit_contracts"][unit]["manpower"])
                            for unit, _, _ in get(node, "regiments", []) + get(node, "support", []))
                for kind, node in walk(tree):
                    if kind == "division":
                        land += templates[get(node, "division_template")]; formations += 1
                    elif kind == "ship":
                        role = get(node, "definition"); count = sum(int(get(detail, "amount", "1")) for _, _, detail in get(node, "equipment", []))
                        ships += count * contracts[role]["stats"]["manpower"]; hulls += count
                for _, _, wings in get(tree, "air_wings", []):
                    for equipment, _, details in wings:
                        count = int(get(details, "amount")); version = get(details, "version_name")
                        candidates = [role for role, c in contracts.items() if c["equipment"] == equipment
                            and role in profile["air"] and (not version or role.title() in version or role == "fighter" and "Fighter" in version or role == "cas" and "Support" in version or role == "tactical" and "Bomber" in version)]
                        if len(candidates) != 1: raise ValueError((tag, key, equipment, version, candidates))
                        aircraft += count * contracts[candidates[0]]["stats"]["manpower"]; planes += count
            pool = core_pop * modifiers["conscription"] * (1 + modifiers["conscription_factor"])
            total = land + aircraft + ships
            cases.append(dict(key=key, laws=active, spirits=sorted(spirits), unmodeled_ideas=unknown,
                law_spirit_modifiers=dict(modifiers), formations=formations, aircraft=planes, ships=hulls,
                land_personnel=land, air_personnel=aircraft, naval_personnel=ships, total_personnel=total,
                core_only_nominal_recruitable_pool=pool, headroom=pool-total,
                headroom_fraction_of_roster=(pool-total)/total if total else None,
                ten_percent_roster_reserve_margin=pool-total*1.1,
                twenty_percent_roster_reserve_margin=pool-total*1.2))
        noncore = {ident: dict(cores=old["cores"], buildings=row["placements"][ident], inherited_buildings=old["buildings"])
                   for ident, old in row["baseline"].items() if tag not in old["cores"]}
        result[tag] = dict(mode=profile.get("mode"), core_population=core_pop, owned_noncore_population=noncore_pop,
                           cases=cases, noncore_placements=noncore)
    # Known state penalties are source inputs, not invented native throughput.
    static = parse(read("mod/2985041246/common/modifiers/00_static_modifiers.txt"))
    rail = read("mod/2985041246/map/railways.txt").splitlines()
    anchor = manifest["map_baselines"]["map/railways.txt"]["lines"]; levels = {}
    for line in rail[:anchor]:
        level, _, *route = map(int, line.split())
        for a, b in zip(route, route[1:]):
            edge = tuple(sorted((a, b))); levels[edge] = max(level, levels.get(edge, 0))
    overlaps = set()
    for tag, row in manifest["countries"].items():
        for route in row["routes"]:
            for a, b in zip(route, route[1:]):
                edge = tuple(sorted((a, b)))
                if levels.get(edge, 0) > 2: overlaps.add((tag, *edge, levels[edge]))
    changed = sorted(changed_during_read | {path for path, data in inputs.items() if hashlib.sha256((root/path).read_bytes()).hexdigest() != data["sha256"]})
    return dict(schema=1, label=label, head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        captured_utc=datetime.now(timezone.utc).isoformat(), profile_count=len(profiles), stable_during_read=not changed,
        probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        profile_manifest_mismatches=[tag for tag,p in profiles.items()if hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()!=manifest["countries"][tag]["profile_sha256"]],
        changed_inputs=changed, inputs=inputs, countries=result,
        noncore_controller_modifiers=get(static, "non_core_controller"),
        higher_inherited_rail_edges_redeclared_level2=[dict(tag=t,edge=[a,b],old_level=l) for t,a,b,l in sorted(overlaps)],
        limits=["Source arithmetic, not native manpower mobilization or force-loading evidence.",
                "Non-core manpower is excluded from the conservative core-only pool; it is not asserted to be zero in the game.",
                "Ten/twenty-percent reserve scenarios are sensitivities, not newly approved policy gates.",
                "Actual law/spirit modifiers are parsed; unknown idea IDs are listed rather than silently credited.",
                "Captured technical contracts feed crew/subunit personnel; stable checkpoint contracts were separately primary-recaptured.",
                "Rail overlap is a regression blind spot; native duplicate-row precedence is unverified."])


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=AUDIT_ROOT)
    parser.add_argument("--label",required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args();report=inspect(args.root,args.label)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(dict(profiles=report["profile_count"],stable_during_read=report["stable_during_read"],
        negative_pool=[tag for tag,row in report["countries"].items()if any(c["headroom"]<0 for c in row["cases"])],
        under_ten_percent_reserve=[tag for tag,row in report["countries"].items()if any(c["ten_percent_roster_reserve_margin"]<0 for c in row["cases"])],
        higher_rail_edges=len(report["higher_inherited_rail_edges_redeclared_level2"]))))
