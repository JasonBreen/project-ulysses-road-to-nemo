"""Reproduce partner and additive ERU placements from owned raster adjacency."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "mod/2985041246"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
sys.path.insert(0, str(ROOT / "tools/anea"))
from script import parse, get
from foundation_map import topology, components, shortest
from erusea import derive_erusea

BASE = "1f04456750b6e17a900cbfa407fddc3a4e96f3d5"


def derive():
    profiles = json.loads((HERE / "profiles.json").read_text())
    previous = json.loads((HERE / "foundation.json").read_text()) if (HERE / "foundation.json").exists() else None
    states = {}
    for path in sorted((MOD / "history/states").glob("*.txt")):
        body = get(parse(path.read_text(encoding="utf-8-sig")), "state")
        hist = get(body, "history", [])
        if get(hist, "owner") in profiles["countries"]:
            states[int(get(body, "id"))] = {"path": path.relative_to(MOD).as_posix(), "body": body,
                "owner": get(hist, "owner"), "cores": [v for k, _, v in hist if k == "add_core_of"],
                "manpower": int(get(body, "manpower")), "provinces": [int(k) for k, _, _ in get(body, "provinces")]}
    defs, graph, centroids, counts, size = topology()
    airport = {int(k): int(v[0][0]) for k, _, v in parse((MOD / "map/airports.txt").read_text()) if k.isdigit() and v}
    result = {"schema": 1, "base": BASE, "source_layer": profiles["source_layer"],
        "raster_sha256": hashlib.sha256((MOD / "map/provinces.bmp").read_bytes()).hexdigest(),
        "definition_sha256": hashlib.sha256((MOD / "map/definition.csv").read_bytes()).hexdigest(),
        "geometry_rule": "Retain owned starting capital; use its existing airport as capital supply/VP province. Select nearest true coastal port and the most distant owned state airport. Route terminals on actual pixel-edge owned-land adjacency with impassable links excluded.",
        "countries": {}, "map_baselines": {}}
    for relative in ("map/supply_nodes.txt", "map/railways.txt"):
        if previous:
            result["map_baselines"][relative] = previous["map_baselines"][relative]
        else:
            source = (MOD / relative).read_text().rstrip() + "\n"
            result["map_baselines"][relative] = {"lines": len(source.splitlines()), "sha256": hashlib.sha256(source.encode()).hexdigest()}
    for tag, profile in profiles["countries"].items():
        history_path = next((MOD / "history/countries").glob(tag + " - *.txt"))
        prior = previous["countries"].get(tag) if previous else None
        history_source = (prior["country_history_source"] if prior
                          else history_path.read_text(encoding="utf-8-sig"))
        if profile.get("preserve_inherited_economy"):
            if tag != "ERU":
                raise ValueError("Additive foundation requires a reviewed country placement owner: " + tag)
            result["countries"][tag] = derive_erusea(states, history_path.relative_to(MOD).as_posix(),
                history_source, prior, defs, graph, airport, profile)
            continue
        capital = int(get(parse(history_source), "capital"))
        owned_states = sorted(i for i, s in states.items() if s["owner"] == tag)
        if capital not in owned_states:
            raise ValueError("Foundation cannot infer a replacement capital for " + tag)
        owned = {p for i in owned_states for p in states[i]["provinces"] if defs[p]["land"]}
        groups = components(owned, graph)
        if len(groups) != 1:
            raise ValueError("Review disconnected-country logistics before extending this profile: " + tag)
        distance = lambda a, b: sum((centroids[a][n] - centroids[b][n]) ** 2 for n in (0, 1))
        cap_p = airport[capital]
        if cap_p not in owned:
            raise ValueError("Capital airport is not owned land: " + tag)
        province_state = {p: i for i in owned_states for p in states[i]["provinces"]}
        coast = [p for p in owned if defs[p]["coastal"] and any(defs[n]["kind"] == "sea" for n in graph[p])]
        port = min(coast, key=lambda p: (distance(cap_p, p), p))
        secondary = max((i for i in owned_states if i != capital), key=lambda i: (distance(cap_p, airport[i]), -i))
        hubs = list(dict.fromkeys([cap_p, port, airport[secondary]]))
        terminals = list(dict.fromkeys(hubs + [airport[i] for i in owned_states]))
        routes = [shortest(cap_p, p, graph, owned) for p in terminals if p != cap_p]
        baseline = {str(i): {key: states[i][key] for key in ("path", "owner", "cores", "manpower", "provinces")} for i in owned_states}
        if previous and baseline != previous["countries"][tag]["baseline"]:
            raise ValueError("Protected state identity changed: " + tag)
        row = {"capital": capital, "capital_province": cap_p, "states": owned_states, "provinces": sorted(owned),
            "country_history": history_path.relative_to(MOD).as_posix(), "country_history_source": history_source,
            "industry_states": [capital] + [i for i in owned_states if i != capital],
            "air_states": [capital, secondary], "airports": {str(i): airport[i] for i in (capital, secondary)},
            "ports": [{"province": port, "state": province_state[port]}], "supply_hubs": hubs, "routes": routes,
            "baseline": baseline, "placements": {}}
        for i in owned_states:
            inherited = profiles["inherited_mapped_state_names"].get(str(i))
            label = inherited or f'{profile["name"]} ' + ("Capital District" if i == capital else f"District {i}")
            row["placements"][str(i)] = {"name": label, "name_layer": "mod provenance" if inherited else "provisional gameplay",
                "infrastructure": 2, "civilian": 0, "military": 0, "dockyard": 0,
                "air_base": 2 if i == capital else 1 if i == secondary else 0,
                "fuel_silo": 1 if i == capital else 0, "naval_bases": {}, "resources": {}}
        for key in ("civilian", "military"):
            for n in range(profile[key]):
                row["placements"][str(row["industry_states"][n % len(owned_states)])][key] += 1
        row["placements"][str(province_state[port])]["dockyard"] = profile["dockyard"]
        row["placements"][str(province_state[port])]["naval_bases"][str(port)] = 2
        row["placements"][str(capital)]["resources"] = {k: profile[k] for k in ("steel", "aluminium", "oil", "tungsten")}
        result["countries"][tag] = row
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = json.dumps(derive(), indent=2) + "\n"
    target = HERE / "foundation.json"
    if args.check:
        if not target.exists() or target.read_text() != expected:
            raise SystemExit("Foundation placement manifest differs")
    else:
        target.write_text(expected, encoding="utf-8")
    print("World foundation placement manifest " + ("consistent" if args.check else "generated"))
