"""Compose declared foundation logistics without accepting opaque foreign tails.

The oldest recorded prefix remains immutable. Every later row belongs to an
explicit manifest and country, and foreign rows must match that manifest.
Regenerating one owner may repair its own rows, but cannot bless changed rows
belonging to another owner. Files remain numeric-only for the native parser.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "usea_expansion"))
from script import parse, get

FILES = ("map/supply_nodes.txt", "map/railways.txt")


def declared_owners(root):
    spec = json.loads((root / "tools/logistics_owners.json").read_text())
    owners = []
    for row in spec["owners"]:
        path = root / row["manifest"]
        if path.exists():
            owners.append((row["id"], json.loads(path.read_text())))
    return owners


def manifest_rows(manifest, relative):
    rows = []
    for country in manifest["countries"].values():
        if relative.endswith("supply_nodes.txt"):
            rows.extend(f"1 {p}" for p in country["supply_hubs"])
        else:
            rows.extend("2 " + str(len(route)) + " " + " ".join(map(str, route))
                        for route in country["routes"])
    if len(set(rows)) != len(rows):
        raise ValueError("Duplicate declared logistics row: " + relative)
    return rows


def row_provinces(line, relative):
    cells = line.split()
    if not cells or not all(c.isdigit() for c in cells):
        raise ValueError("Non-numeric logistics row: " + relative)
    values = list(map(int, cells))
    if relative.endswith("supply_nodes.txt"):
        if len(values) != 2 or values[0] < 1:
            raise ValueError("Invalid supply-node row")
        return values[1:]
    if len(values) < 4 or values[1] != len(values) - 2 or not 1 <= values[0] <= 5:
        raise ValueError("Invalid railway row")
    return values[2:]


def compose(root, mod, owner=None):
    owners = declared_owners(root)
    if not owners:
        return {}
    province_tags = {}
    for path in (mod / "history/states").glob("*.txt"):
        body = get(parse(path.read_text(encoding="utf-8-sig")), "state")
        tag = get(get(body, "history", []), "owner")
        for p, _, _ in get(body, "provinces", []):
            province_tags[int(p)] = tag
    tag_owner = {}
    for ident, manifest in owners:
        for tag in manifest["countries"]:
            if tag in tag_owner:
                raise ValueError("Multiple logistics owners for " + tag)
            tag_owner[tag] = ident
    result = {}
    for relative in FILES:
        anchor = min((m["map_baselines"][relative] for _, m in owners), key=lambda x: x["lines"])
        current = (mod / relative).read_text().splitlines()
        prefix = "\n".join(current[:anchor["lines"]]).rstrip() + "\n"
        if hashlib.sha256(prefix.encode()).hexdigest() != anchor["sha256"]:
            raise ValueError("Immutable logistics prefix changed: " + relative)
        actual = defaultdict(list)
        seen = set()
        for line in current[anchor["lines"]:]:
            if not line.strip():
                continue
            provinces = row_provinces(line, relative)
            tags = {province_tags.get(p) for p in provinces}
            if len(tags) != 1 or next(iter(tags)) not in tag_owner:
                raise ValueError("Undeclared/foreign-country logistics row: " + relative)
            normalized = " ".join(line.split())
            if normalized in seen:
                raise ValueError("Duplicate logistics row: " + relative)
            seen.add(normalized)
            actual[tag_owner[next(iter(tags))]].append(normalized)
        tail = []
        for ident, manifest in owners:
            expected = manifest_rows(manifest, relative)
            # A not-yet-generated family may be installed by either generator.
            # A present foreign family must be exact, never hash-blessed.
            if ident != owner and actual[ident] and actual[ident] != expected:
                raise ValueError("Stale or mutated foreign logistics owner " + ident + ": " + relative)
            for line in expected:
                tags = {province_tags.get(p) for p in row_provinces(line, relative)}
                if len(tags) != 1 or next(iter(tags)) not in manifest["countries"]:
                    raise ValueError("Manifest crosses country ownership: " + ident)
            tail.extend(expected)
        if len(set(tail)) != len(tail):
            raise ValueError("Duplicate declared logistics owners: " + relative)
        result[relative] = prefix + "\n".join(tail) + "\n"
    return result
