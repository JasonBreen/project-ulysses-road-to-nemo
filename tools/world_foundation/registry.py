"""Reproduce the 69-country source registry; no native playability claims.

--check compares the committed report without writing. --output writes an
explicit report path; the default command prints only its aggregate summary.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "mod/2985041246"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
from script import parse, get, walk


def nodes(tree):
    for key, op, value in tree:
        yield key, op, value
        if isinstance(value, list):
            yield from nodes(value)


def input_path_order(path, root=MOD):
    relative = path.relative_to(root).as_posix()
    return relative.casefold(), relative


def inspect():
    inputs = set()

    def read(path):
        inputs.add(path)
        return parse(path.read_text(encoding="utf-8-sig"))

    states = {}
    province_state = {}
    for path in sorted((MOD / "history/states").glob("*.txt")):
        body = get(read(path), "state"); hist = get(body, "history", [])
        ident = int(get(body, "id")); provinces = [int(k) for k, _, _ in get(body, "provinces", [])]
        states[ident] = {"owner": get(hist, "owner"), "body": body, "history": hist, "provinces": provinces}
        province_state.update({p: ident for p in provinces})
    supply_path, rail_path = MOD / "map/supply_nodes.txt", MOD / "map/railways.txt"
    inputs.update([supply_path, rail_path])
    supply = [int(line.split()[1]) for line in supply_path.read_text().splitlines() if line.strip()]
    rails = [list(map(int, line.split()[2:])) for line in rail_path.read_text().splitlines() if line.strip()]
    focus_counts = Counter()
    for path in sorted((MOD / "common/national_focus").glob("*.txt")):
        for key, _, body in nodes(read(path)):
            if key in ("focus", "shared_focus") and isinstance(body, list):
                ident = get(body, "id", "").strip('"')
                if len(ident) >= 4 and ident[3] == "_":
                    focus_counts[ident[:3].upper()] += 1
    ideology = get(read(MOD / "common/ideologies/00_ideologies.txt"), "ideologies", [])
    ideology_group = {sub: group for group, _, body in ideology for sub, _, _ in get(body, "types", [])}
    characters = {}
    for path in sorted((MOD / "common/characters").glob("*.txt")):
        for ident, _, body in get(read(path), "characters", []):
            characters[ident] = [ideology_group.get(get(role, "ideology", "").strip('"'))
                                for k, _, role in body if k == "country_leader"
                                and get(role, "expire", '"2066.1.1"').strip('"') > "1991.1.1"]
    rows = []
    covered = set(json.loads((HERE / "profiles.json").read_text())["countries"])
    for path in sorted((MOD / "history/countries").glob("*.txt")):
        tag = path.name[:3]; history = read(path)
        owned = {i: s for i, s in states.items() if s["owner"] == tag}
        owned_provinces = {p for s in owned.values() for p in s["provinces"]}
        buildings = Counter(); resources = Counter()
        for state in owned.values():
            for key, _, value in get(state["history"], "buildings", []):
                if isinstance(value, list):
                    buildings.update({k: int(float(v)) for k, _, v in value})
                else:
                    buildings[key] += int(float(value))
            resources.update({k: int(float(v)) for k, _, v in get(state["body"], "resources", [])})
        for key in ("industrial_complex", "arms_factory", "dockyard", "infrastructure", "air_base", "naval_base", "fuel_silo", "supply_node"):
            buildings.setdefault(key, 0)
        roster_refs = sorted({value.strip('"') for key, _, value in nodes(history)
                              if key in ("set_oob", "load_oob", "set_air_oob", "set_naval_oob") and isinstance(value, str)})
        missing = []; parse_errors = []; roster_kinds = set(); production = Counter()
        for name in roster_refs:
            roster_path = MOD / "history/units" / (name + ".txt")
            if not roster_path.exists():
                missing.append(name); continue
            try:
                tree = read(roster_path)
            except (ValueError, IndexError) as exc:
                # An inventory must expose inherited gaps rather than lose all
                # 69 rows. This parser is not the native engine parser.
                parse_errors.append({"roster": name, "offline_parser_error": str(exc)})
                continue
            if get(tree, "air_wings") is not None:
                roster_kinds.add("air")
            for key, _, body in nodes(tree):
                if key == "division":
                    roster_kinds.add("land")
                if key == "ship":
                    roster_kinds.add("naval")
                if key == "add_equipment_production":
                    kind = get(get(body, "equipment", []), "type", "unknown")
                    production[kind] += int(get(body, "requested_factories", "0"))
        capital = int(get(history, "capital", "0")); party = get(get(history, "set_politics", []), "ruling_party")
        recruits = [v for k, _, v in history if k == "recruit_character"]
        active = [v for v in recruits if party in characters.get(v, [])]
        checks = {"owns_capital": capital in owned, "has_industry": sum(buildings[k] for k in ("industrial_complex", "arms_factory", "dockyard")) > 0,
            "has_infrastructure": buildings["infrastructure"] > 0, "has_supply_node": any(p in owned_provinces for p in supply),
            "has_direct_land_roster": "land" in roster_kinds, "has_direct_air_roster": "air" in roster_kinds,
            "has_airbase": buildings["air_base"] > 0, "has_recruited_ruling_party_leader": bool(active) or any(k == "create_country_leader" for k, _, _ in history),
            "referenced_rosters_resolve": bool(roster_refs) and not missing and not parse_errors, "has_initial_production": bool(production)}
        if buildings["naval_base"] > 0:
            checks["has_direct_naval_roster"] = "naval" in roster_kinds
        issues = [key for key, value in checks.items() if not value]
        if tag == "PLH" or 171 in owned:
            status = "unresolved_placeholder_do_not_infer"
        elif not owned:
            status = "dormant_or_emergent_entry_requires_review"
        elif issues:
            status = "inherited_foundation_gaps"
        elif tag in covered or tag in ("EMM", "EVA"):
            status = "authored_foundation_native_acceptance_pending"
        else:
            status = "inherited_source_checks_pass_native_acceptance_pending"
        rows.append({"tag": tag, "name": path.stem.split(" - ", 1)[-1], "history": path.relative_to(MOD).as_posix(),
            "support_status": status, "native_acceptance": "not established by this source registry",
            "owned_states": sorted(owned), "province_count": len(owned_provinces),
            "inherited_manpower_total_not_canon_population": sum(int(get(s["body"], "manpower", "0")) for s in owned.values()),
            "capital_state": capital, "capital_current_owner": states.get(capital, {}).get("owner"),
            "buildings": dict(sorted(buildings.items())), "resources": dict(sorted(resources.items())),
            "supply_node_count": sum(p in owned_provinces for p in supply),
            "intersecting_rail_path_count": sum(any(p in owned_provinces for p in route) for route in rails),
            "tag_prefixed_focus_definitions": focus_counts[tag],
            "recruited_active_party_leaders": active, "history_roster_references": roster_refs,
            "missing_roster_files": missing, "roster_offline_parser_errors": parse_errors, "initial_production_assignments": dict(sorted(production.items())),
            "source_checks": checks, "source_gaps": issues,
            "scope_note": "Direct history/OOB source inspection only. Event-driven forces and native AI, supply reach, engine parsing and balance are separate acceptance."})
    summary = {"country_histories": len(rows), "currently_landowning": sum(bool(r["owned_states"]) for r in rows),
        "support_status_counts": dict(sorted(Counter(r["support_status"] for r in rows).items())),
        "landowning_without_industry": sum(bool(r["owned_states"]) and not r["source_checks"]["has_industry"] for r in rows),
        "landowning_without_infrastructure": sum(bool(r["owned_states"]) and not r["source_checks"]["has_infrastructure"] for r in rows),
        "landowning_with_foreign_capital": sum(bool(r["owned_states"]) and not r["source_checks"]["owns_capital"] for r in rows),
        "without_direct_history_roster": sum(not r["history_roster_references"] for r in rows)}
    digest = hashlib.sha256()
    for path in sorted(inputs, key=input_path_order):
        digest.update(path.relative_to(MOD).as_posix().encode() + b"\0" + path.read_bytes())
    return {"schema": 1, "start": "1991.1.1", "evidence": "source inspection, not native acceptance",
        "input_digest_sha256": digest.hexdigest(), "input_file_count": len(inputs), "summary": summary, "countries": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true"); parser.add_argument("--output", type=Path)
    args = parser.parse_args(); report = inspect(); text = json.dumps(report, indent=2) + "\n"
    if args.check:
        target = args.output or HERE / "country_registry.json"
        if not target.exists() or target.read_text() != text:
            raise SystemExit("Country registry differs; inspect actual source changes before regenerating")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(text, encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
