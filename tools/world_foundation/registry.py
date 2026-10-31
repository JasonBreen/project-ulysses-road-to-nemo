"""Reproduce the 69-country source registry; no native playability claims.

--check compares the committed report without writing. --output writes an
explicit report path; the default command prints only its aggregate summary.
"""
import argparse
from collections import Counter, defaultdict
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
    support_inputs = {}

    def support_profile(relative, collection=None):
        path = ROOT / relative
        if not path.exists():
            return {}
        raw = path.read_bytes().replace(b'\r\n', b'\n')
        support_inputs[relative] = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw)
        return data if collection == 'object' else {row['tag']: row for row in (data[collection] if collection else data)}

    fiscal_profiles = support_profile('tools/economy_v2/profiles.json', 'profiles')
    political_profiles = support_profile('tools/institutions/profiles.json')
    capital_profiles = support_profile('tools/world_capitals/placements.json', 'object').get('countries', {})
    for name, profiles in [('fiscal', fiscal_profiles), ('political', political_profiles)]:
        if profiles and len(profiles) != 69:
            raise ValueError('The integrated ' + name + ' registry must cover all69 histories')

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
    participant_declarations = defaultdict(list)
    for path in sorted((MOD / 'common/scripted_triggers').glob('*.txt')):
        for key, _, body in read(path):
            if not isinstance(body, list) or not key.endswith(('_participant', '_host')):
                continue
            tags = {value for field, _, value in nodes(body) if field in ('tag', 'original_tag') and isinstance(value, str)}
            for tag in tags:
                participant_declarations[tag].append(dict(trigger=key, source=path.relative_to(MOD).as_posix()))
    rows = []
    covered = set(json.loads((HERE / "profiles.json").read_text())["countries"])
    active_profiles = {}
    active_profiles_path = ROOT / 'tools/world_starts/profiles.json'
    if active_profiles_path.exists():
        active_profiles = support_profile('tools/world_starts/profiles.json', 'object').get('countries', {})
        covered.update(active_profiles)
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
        # Preserve the raw observations. A reviewed civil-defense role may
        # deliberately have no standing aircraft or combat fleet; never turn
        # an empty OOB into a claimed capability just to make this inventory green.
        role = active_profiles.get(tag, {})
        dispositions = {}
        if role and not role.get('air') and not any(k in role.get('production', {}) for k in ('fighter', 'cas', 'tactical')):
            reason = role.get('capability_dispositions', {}).get('combat_air')
            if reason and reason.startswith('deliberately absent:'):
                for key in ('has_direct_air_roster', 'has_airbase'):
                    if not checks[key]: dispositions[key] = reason
        if role and not role.get('navy') and 'has_direct_naval_roster' in checks and not checks['has_direct_naval_roster']:
            reason = role.get('capability_dispositions', {}).get('combat_navy')
            if reason and reason.startswith('deliberately absent:'):
                dispositions['has_direct_naval_roster'] = reason
        issues = [key for key, value in checks.items() if not value and key not in dispositions]
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
        political = political_profiles.get(tag)
        fiscal = fiscal_profiles.get(tag)
        office = bool(active) and all(ident.endswith('_ac_government_office') for ident in active)
        rows.append({"tag": tag, "name": path.stem.split(" - ", 1)[-1], "history": path.relative_to(MOD).as_posix(),
            "support_status": status, "native_acceptance": "not established by this source registry",
            "start_classification": 'placeholder' if tag == 'PLH' or 171 in owned else 'active' if owned else 'emergent',
            "classification_note": 'Landless inherited histories require their legitimate release/setup contract; no retroactive start grant is implied.',
            "capital_source_layer": 'approved provisional capital district' if tag in capital_profiles or tag == 'EVA' else 'inherited mod mapping; no new official city assertion',
            "leader_representation": dict(kind='government office' if office else 'named inherited individual' if active else 'legacy or unresolved',
                characters=active, term_source='approved provisional 1991 term' if 'FCU_robert_sinclair' in active else 'inherited or office representation; official term not newly certified'),
            "political_institution": ({key: political[key] for key in ('institution', 'capacity', 'source_layer', 'reference', 'status')} if political else {'status': 'owner profile not integrated'}),
            "fiscal_profile": ({key: fiscal[key] for key in ('gdp_billion', 'debt_ratio', 'collection', 'growth', 'inflation', 'source_layer', 'calibration')} if fiscal else {'status': 'owner profile not integrated'}),
            "tree_assignment": dict(country_aligned_definitions=focus_counts[tag],
                regional_fallback=bool(political and political['regional_tree']),
                note='Definition inventory plus integrated fallback profile; actual selection/imports are tested by their owning tree suite.'),
            "regional_contracts": sorted(participant_declarations[tag], key=lambda row: (row['source'], row['trigger'])),
            "diplomatic_eligibility": 'Runtime partner eligibility belongs to the listed regional/public owners; existence, war, subject and capitulation conditions are not replaced by this source registry.',
            "owned_states": sorted(owned), "province_count": len(owned_provinces),
            "inherited_manpower_total_not_canon_population": sum(int(get(s["body"], "manpower", "0")) for s in owned.values()),
            "capital_state": capital, "capital_current_owner": states.get(capital, {}).get("owner"),
            "buildings": dict(sorted(buildings.items())), "resources": dict(sorted(resources.items())),
            "supply_node_count": sum(p in owned_provinces for p in supply),
            "intersecting_rail_path_count": sum(any(p in owned_provinces for p in route) for route in rails),
            "tag_prefixed_focus_definitions": focus_counts[tag],
            "recruited_active_party_leaders": active, "history_roster_references": roster_refs,
            "technology_inventory_all_history_branches": sorted({tech for key, _, value in nodes(history) if key == 'set_technology' and isinstance(value, list) for tech, _, _ in value}),
            "missing_roster_files": missing, "roster_offline_parser_errors": parse_errors, "initial_production_assignments": dict(sorted(production.items())),
            "source_checks": checks, "source_gaps": issues, "role_not_required": dispositions,
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
    return {"schema": 2, "start": "1991.1.1", "evidence": "source inspection, not native acceptance",
        "support_profile_inputs_sha256": dict(sorted(support_inputs.items())),
        "support_profile_hash_normalization": "UTF-8 source bytes with CRLF normalized to LF; not a native payload or texture hash",
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
