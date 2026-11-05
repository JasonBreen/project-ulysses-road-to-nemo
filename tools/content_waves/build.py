"""Compile every registered content wave.

Run without arguments to regenerate the owned files; --check is read-only.
Each wave module in content_waves.registry declares where its focuses go:
IMPORTS adds shared focuses to an existing tree through a marked block that
the tree's own generator preserves; TREES creates a new national tree. All
content is provisional gameplay unless a source ledger row says otherwise;
see README.md and the per-wave ledgers in docs/.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / "mod/2985041246"
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools/usea_expansion")]

from content_waves.framework import block, compile_wave, empty_wave, focus_id, readable_flags  # noqa: E402
from content_waves.registry import MODULES  # noqa: E402
from script import parse, get  # noqa: E402

PURPOSES = ("Unlock the first funded service", "Exclusive enduring policy", "Exclusive enduring policy",
            "Unlock the second funded service", "Require a completed ninety-day service period",
            "Improve the chosen policy while retaining its cost")


def attach(source, tag, ids, name):
    """Replace or append only the owned import block inside the single tree."""
    begin, end = f"# BEGIN {name} IMPORTS", f"# END {name} IMPORTS"
    if source.count(begin) != source.count(end) or source.count(begin) > 1:
        raise ValueError(f"Unbalanced {name} imports: {tag}")
    if source.count("focus_tree") != 1:
        raise ValueError("Expected one focus tree in " + tag)
    lines = "\t" + begin + "\n" + "".join("\tshared_focus = " + i + "\n" for i in ids) + "\t" + end + "\n"
    if begin in source:
        start = source.index("\t" + begin)
        finish = source.index(end) + len(end) + 1
        owned = parse(source[start:finish])
        if any(k != "shared_focus" or v not in ids for k, _, v in owned):
            raise ValueError(f"Foreign content inside {name} imports: {tag}")
        return source[:start] + lines + source[finish:]
    if not source.endswith("}\n"):
        raise ValueError("Unexpected tree ending: " + tag)
    return source[:-2] + lines + "}\n"


def wave_files(module):
    wave, name, owner = module.WAVE, module.NAME, module.owner()
    frag = compile_wave(wave) if wave.branches else empty_wave(wave)
    note = f"# Original provisional gameplay; source: tools/content_waves ({wave.label}). Native acceptance pending.\n"
    effects, triggers, loc = frag["effects"], frag["triggers"], frag["loc"]
    ideas, events, custom = list(frag["ideas"]), list(frag["events"]), list(frag["custom"])
    hooks, categories = frag["hooks"] + owner.get("hooks", ""), frag["categories"] + owner.get("categories", [])
    decisions = frag["decisions"]
    for key, value in owner.get("effects", {}).items():
        assert key not in effects, key
        effects[key] = value
    for key, value in owner.get("triggers", {}).items():
        assert key not in triggers, key
        triggers[key] = value
    for key, value in owner.get("loc", {}).items():
        assert key not in loc, key
        loc[key] = value
    for tag, prefix in owner.get("category_prefix", {}).items():
        key = f"{wave.prefix}_{tag.lower()}_services_desc"
        loc[key] = prefix + loc[key]
    ideas.extend(owner.get("ideas", []))
    events = owner.get("events", []) + events
    if owner.get("custom"):
        custom.append(owner["custom"])
    for category, rows in owner.get("decisions", {}).items():
        decisions[category] = rows + decisions[category]
    if f"{wave.prefix}_interrupt" in effects:
        effects[f"{wave.prefix}_interrupt"] += owner.get("interrupt_extra", "")
    out = {
        f"common/scripted_effects/ac_{name}.txt": note + "\n".join(block(k, v) for k, v in effects.items()),
        f"common/scripted_triggers/ac_{name}.txt": note + "\n".join(block(k, v) for k, v in triggers.items()),
        f"common/ideas/ac_{name}.txt": note + block("ideas", block("country", "\n".join(ideas))),
        f"common/decisions/categories/ac_{name}.txt": note + "\n".join(categories),
        f"common/decisions/ac_{name}.txt": note + "\n".join(block(k, "\n".join(v)) for k, v in decisions.items()),
        f"common/on_actions/ac_{name}.txt": note + block("on_actions", hooks),
        f"common/custom_localization/ac_{name}.txt": note + "\n".join(custom),
        f"events/ac_{name}.txt": note + f"add_namespace = {wave.prefix}\n" + "\n".join(events),
    }
    if frag["focuses"]:
        out[f"common/national_focus/ac_{name}.txt"] = note + "\n".join(frag["focuses"])
    if owner.get("ai_strategy"):
        out[f"common/ai_strategy/ac_{name}.txt"] = note + owner["ai_strategy"]
    readable_flags(wave, frag, [v for k, v in out.items()], parse, get)
    out[f"localisation/english/ac_{name}_l_english.yml"] = "\ufeffl_english:\n" + "".join(
        f' {k}:0 "' + v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"\n' for k, v in loc.items())
    return out, frag


def new_tree(module, tag, tree_id, frag):
    wave = module.WAVE
    ids = [focus_id(wave, b, i) for b in wave.branches if b.tag == tag for i in range(6)]
    right = max(frag["positions"][i][0] for i in ids)
    body = (f"id = {tree_id}\ncountry = {{ factor = 0 modifier = {{ add = 45 tag = {tag} original_tag = {tag} }} }}\n"
            "default = no\nreset_on_civilwar = no\n"
            f"initial_show_position = {{ focus = {ids[0]} }}\ncontinuous_focus_position = {{ x = {(right + 4) * 96} y = 16 }}\n" +
            "".join("shared_focus = " + i + "\n" for i in ids))
    return f"# Original provisional gameplay; source: tools/content_waves ({wave.label}). Native acceptance pending.\n" + block("focus_tree", body)


def outputs():
    out, frags = {}, {}
    for module in MODULES:
        files, frag = wave_files(module)
        overlap = set(files) & set(out)
        assert not overlap, overlap
        out.update(files)
        frags[module.KEY] = frag
        for tag, name in getattr(module, "IMPORTS", {}).items():
            relative = f"common/national_focus/{tag}.txt"
            ids = [focus_id(module.WAVE, b, i) for b in module.WAVE.branches if b.tag == tag for i in range(6)]
            out[relative] = attach((MOD / relative).read_text(encoding="utf-8"), tag, ids, name)
        for tag, tree_id in getattr(module, "TREES", {}).items():
            out[f"common/national_focus/{tag}.txt"] = new_tree(module, tag, tree_id, frag)
    return out, frags


def inventory(frags):
    rows = []
    for module in MODULES:
        wave = module.WAVE
        where = frags[module.KEY]["positions"]
        for b in wave.branches:
            for i in range(6):
                ident = focus_id(wave, b, i)
                rows.append(dict(id=ident, wave=module.KEY, tag=b.tag, branch=b.key, title=b.titles[i], x=where[ident][0], y=where[ident][1],
                                 cost_days=70 if i in (1, 2, 5) else 35, purpose=PURPOSES[i],
                                 entry=list(b.entry) if i == 0 else [], gate=b.gate if i == 0 else "",
                                 exclusive_with=focus_id(wave, b, 2 if i == 1 else 1) if i in (1, 2) else None,
                                 source_layer="provisional gameplay"))
    counts = {}
    for row in rows:
        counts[row["tag"]] = counts.get(row["tag"], 0) + 1
    return dict(schema=2, title="Content waves", counts=counts, total=len(rows),
                waves=[dict(key=m.KEY, name=m.NAME, label=m.WAVE.label, ledger=m.LEDGER, source_layers=m.SOURCES) for m in MODULES],
                services=[dict(id=ident, wave=m.KEY, tag=b.tag, branch=b.key, days=90, cooldown_days=90, political_power=35, capacity=4)
                          for m in MODULES for b, n, ident in frags[m.KEY]["services"]],
                focuses=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    out, frags = outputs()
    failures = []
    for relative, text in out.items():
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    data = inventory(frags)
    manifest = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    path = HERE / "manifest.json"
    if args.check:
        if not path.exists() or path.read_text(encoding="utf-8") != manifest:
            failures.append("tools/content_waves/manifest.json")
    else:
        path.write_text(manifest, encoding="utf-8", newline="\n")
    if failures:
        raise SystemExit("Content waves output differs: " + ", ".join(failures))
    waves = "+".join(m.KEY for m in MODULES)
    print(f"Content waves {waves}: {data['total']} focus definitions {data['counts']}, {len(data['services'])} funded services; "
          + ("consistent" if args.check else "generated"))


if __name__ == "__main__":
    main()
