"""Additive ERU placements on retained industry and exact owned-land components.

Every added facility/resource is gameplay calibration, not a geographic claim.
The captured economic baseline is immutable; generated additions are explicit.
"""
import copy
from decimal import Decimal

from script import get
from foundation_map import components, shortest


def inherited_economy(state):
    body = state["body"]; hist = get(body, "history"); buildings = get(hist, "buildings")
    return {
        "infrastructure": int(get(buildings, "infrastructure", "0")),
        "civilian": int(get(buildings, "industrial_complex", "0")),
        "military": int(get(buildings, "arms_factory", "0")),
        "dockyard": int(get(buildings, "dockyard", "0")),
        "air_base": int(get(buildings, "air_base", "0")),
        "fuel_silo": int(get(buildings, "fuel_silo", "0")),
        "naval_bases": {key: int(get(value, "naval_base")) for key, _, value in buildings
                        if isinstance(value, list) and get(value, "naval_base") is not None},
        "resources": {key: value for key, _, value in get(body, "resources", [])},
        "victory_points": [copy.deepcopy(v) for k, _, v in hist if k == "victory_points"],
        "state_category": get(body, "state_category"),
    }


def derive_erusea(states, history_path, history_source, previous, defs, graph, airports, profile):
    capital = 349
    owned_states = sorted(i for i, s in states.items() if s["owner"] == "ERU")
    if capital not in owned_states:
        raise ValueError("Retained ERU capital is no longer owned")
    owned = {p for i in owned_states for p in states[i]["provinces"] if defs[p]["land"]}
    province_state = {p: i for i in owned_states for p in states[i]["provinces"]}
    baseline = {str(i): {k: copy.deepcopy(states[i][k]) for k in ("path", "owner", "cores", "manpower", "provinces")}
                for i in owned_states}
    if previous and (set(baseline) != set(previous["baseline"]) or
                     any(baseline[i] != {k: previous["baseline"][i][k] for k in baseline[i]} for i in baseline)):
        raise ValueError("Protected state identity changed: ERU")
    for i in owned_states:
        baseline[str(i)]["economy"] = (copy.deepcopy(previous["baseline"][str(i)]["economy"]) if previous
                                         else inherited_economy(states[i]))
        current = inherited_economy(states[i]); original = baseline[str(i)]["economy"]
        if any(current[k] != original[k] for k in ("civilian", "military", "dockyard")):
            raise ValueError("Inherited ERU factory placement changed: " + str(i))
    cap_points = baseline[str(capital)]["economy"]["victory_points"]
    cap_p = max(cap_points, key=lambda v: (int(v[1][0]), -int(v[0][0])))[0][0]
    cap_p = int(cap_p)
    groups = components(owned, graph)
    if cap_p not in groups[0]:
        raise ValueError("ERU capital must remain on its retained mainland")
    row = {"capital": capital, "capital_province": cap_p, "states": owned_states, "provinces": sorted(owned),
           "country_history": history_path, "country_history_source": history_source,
           "preserve_inherited_economy": True, "baseline": baseline, "placements": {},
           "industry_states": [i for i in owned_states if sum(baseline[str(i)]["economy"][k] for k in ("civilian", "military", "dockyard"))],
           "air_states": [349, 298, 240, 262, 350, 467],
           "ports": [], "supply_hubs": [], "routes": [], "components": [], "new_victory_points": []}
    row["geometry_rule"] = "Retain highest existing capital-state VP644, connect existing airport1118; exact owned-land components and sorted BFS. Retain all16 valid ports. Each detached component lacking a port receives its coastal operational airport or lowest valid coastal province as a provisional receiving terminal; never a cross-water rail."
    row["source_base"] = "fb3e8c3"
    row["airports"] = {str(i): airports[i] for i in row["air_states"]}
    for i in owned_states:
        original = baseline[str(i)]["economy"]
        cfg = {k: copy.deepcopy(original[k]) for k in ("infrastructure", "civilian", "military", "dockyard", "air_base", "fuel_silo", "naval_bases")}
        cfg.update({"name": "STATE_" + str(i), "name_layer": "retained localisation", "preserve_names": True,
                    "resources": copy.deepcopy(original["resources"])})
        # Minimum local access for the operational island states. No industry
        # or population is moved to an island, and mainland levels never fall.
        if i in row["air_states"]:
            cfg["air_base"] = max(cfg["air_base"], 2 if i in (349, 298) else 1)
            cfg["infrastructure"] = max(cfg["infrastructure"], 1)
        if i == 349:
            cfg["fuel_silo"] = max(cfg["fuel_silo"], 1)
        for resource, addition in profile["resource_additions"].get(str(i), {}).items():
            if addition < 0:
                raise ValueError("ERU resource calibration must be additive")
            value = Decimal(str(cfg["resources"].get(resource, 0))) + Decimal(str(addition))
            cfg["resources"][resource] = int(value) if value == int(value) else str(value)
        row["placements"][str(i)] = cfg
    existing_ports = {int(p): level for cfg in row["placements"].values() for p, level in cfg["naval_bases"].items()}
    original_vps = {int(v[0][0]) for b in baseline.values() for v in b["economy"]["victory_points"]}
    for index, group in enumerate(groups):
        coast = sorted(p for p in group if defs[p]["coastal"] and any(defs[n]["kind"] == "sea" for n in graph[p]))
        ports = sorted(p for p in group if p in existing_ports)
        for p in ports:
            if p not in coast:
                raise ValueError("Inherited ERU port is not true coast: " + str(p))
        operational_airports = sorted(p for p in row["airports"].values() if p in group)
        if not ports:
            if not coast:
                raise ValueError("Detached ERU component has no valid receiving coast")
            # Existing operational airport breaks the choice if coastal; all
            # remaining unmapped receiving ports use the lowest valid ID.
            p = next((p for p in operational_airports if p in coast), coast[0])
            row["placements"][str(province_state[p])]["naval_bases"][str(p)] = 1
            ports = [p]
        root = cap_p if cap_p in group else ports[0]
        terminals = sorted(set(ports + [airports[i] for i in owned_states if airports[i] in group]))
        hubs = [cap_p] if index == 0 else []
        if index == 0:
            # Retained mainland industrial and air/deployment centres are all
            # linked. Four distributed supply hubs avoid one-capital stacks.
            hubs += [airports[i] for i in (298, 333, 457)]
        elif operational_airports:
            hubs += [root]
        terminals = list(dict.fromkeys(hubs + terminals))
        routes = [shortest(root, p, graph, group) for p in terminals if p != root]
        row["routes"].extend(routes); row["supply_hubs"].extend(hubs)
        for p in ports:
            row["ports"].append({"province": p, "state": province_state[p], "component": index,
                                 "inherited": p in existing_ports})
        row["components"].append({"index": index, "provinces": sorted(group), "root": root,
            "root_kind": "retained capital" if index == 0 else "port-fed receiving terminal",
            "ports": ports, "terminals": terminals, "supply_hubs": hubs,
            "operational_airports": operational_airports, "routes": routes,
            "deployment": index == 0 or bool(operational_airports)})
    row["new_victory_points"] = [p for p in row["supply_hubs"] if p not in original_vps]
    # Explicit deployment map: eight mainland formations; one on each of the
    # four operational island-state components. No troops on isolated islets.
    mainland_hubs = row["components"][0]["supply_hubs"]
    island_hubs = [c["root"] for c in row["components"][1:] if c["deployment"]]
    row["land_deployments"] = [mainland_hubs[n % len(mainland_hubs)] for n in range(8)] + island_hubs
    if len(row["land_deployments"]) != profile["divisions"]:
        raise ValueError("ERU deployment budget differs from reviewed profile")
    row["air_deployments"] = [{"state": 349, "fighters": 48, "cas": 24}, {"state": 298, "fighters": 48, "cas": 0}]
    row["naval_base"] = cap_p
    return row
