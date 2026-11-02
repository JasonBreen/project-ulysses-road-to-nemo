"""Compile Wave A (the oversight years) and Wave D (the northern reserve).

Run without arguments to regenerate the owned files; --check is read-only.
Wave A adds 36 Erusean and 24 Central Usean shared focuses to the existing
Continental War trees through a marked import block that
tools/build_continental_war.py preserves. Wave D adds Nordennavic's 42-focus
national tree. All content is provisional gameplay; see README.md.
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

from content_waves.framework import SUFFIXES, block, branch_id, compile_wave, focus_id, readable_flags  # noqa: E402
from content_waves import free_erusea, nordennavic  # noqa: E402
from script import parse, get  # noqa: E402

IMPORT_NAME = "OVERSIGHT YEARS"
BEGIN, END = f"# BEGIN {IMPORT_NAME} IMPORTS", f"# END {IMPORT_NAME} IMPORTS"
PURPOSES = ("Unlock the first funded service", "Exclusive enduring policy", "Exclusive enduring policy",
            "Unlock the second funded service", "Require a completed ninety-day service period",
            "Improve the chosen policy while retaining its cost")


def attach(source, tag, ids):
    """Replace or append only the owned import block inside the single tree."""
    if source.count(BEGIN) != source.count(END) or source.count(BEGIN) > 1:
        raise ValueError("Unbalanced oversight-years imports: " + tag)
    if source.count("focus_tree") != 1:
        raise ValueError("Expected one focus tree in " + tag)
    lines = "\t" + BEGIN + "\n" + "".join("\tshared_focus = " + i + "\n" for i in ids) + "\t" + END + "\n"
    if BEGIN in source:
        start = source.index("\t" + BEGIN)
        finish = source.index(END) + len(END) + 1
        owned = parse(source[start:finish])
        if any(k != "shared_focus" or v not in ids for k, _, v in owned):
            raise ValueError("Foreign content inside oversight-years imports: " + tag)
        return source[:start] + lines + source[finish:]
    if not source.endswith("}\n"):
        raise ValueError("Unexpected tree ending: " + tag)
    return source[:-2] + lines + "}\n"


def wave_files(wave, name, owner):
    frag = compile_wave(wave)
    note = f"# Original provisional gameplay; source: tools/content_waves ({wave.label}). Native acceptance pending.\n"
    effects, triggers, loc = frag["effects"], frag["triggers"], frag["loc"]
    ideas, events, custom, hooks = list(frag["ideas"]), list(frag["events"]), list(frag["custom"]), frag["hooks"]
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
    effects[f"{wave.prefix}_interrupt"] += owner.get("interrupt_extra", "")
    out = {
        f"common/national_focus/ac_{name}.txt": note + "\n".join(frag["focuses"]),
        f"common/scripted_effects/ac_{name}.txt": note + "\n".join(block(k, v) for k, v in effects.items()),
        f"common/scripted_triggers/ac_{name}.txt": note + "\n".join(block(k, v) for k, v in triggers.items()),
        f"common/ideas/ac_{name}.txt": note + block("ideas", block("country", "\n".join(ideas))),
        f"common/decisions/categories/ac_{name}.txt": note + "\n".join(frag["categories"]),
        f"common/decisions/ac_{name}.txt": note + "\n".join(block(k, "\n".join(v)) for k, v in decisions.items()),
        f"common/on_actions/ac_{name}.txt": note + block("on_actions", hooks),
        f"common/custom_localization/ac_{name}.txt": note + "\n".join(custom),
        f"events/ac_{name}.txt": note + f"add_namespace = {wave.prefix}\n" + "\n".join(events),
    }
    readable_flags(wave, frag, [v for k, v in out.items()], parse, get)
    out[f"localisation/english/ac_{name}_l_english.yml"] = "\ufeffl_english:\n" + "".join(
        f' {k}:0 "' + v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"\n' for k, v in loc.items())
    return out, frag


def nec_tree(frag):
    wave = nordennavic.WAVE
    ids = [focus_id(wave, b, i) for b in wave.branches for i in range(6)]
    right = max(x for x, _ in frag["positions"].values())
    body = (f"id = {nordennavic.TREE_ID}\ncountry = {{ factor = 0 modifier = {{ add = 45 tag = NEC original_tag = NEC }} }}\n"
            "default = no\nreset_on_civilwar = no\n"
            f"initial_show_position = {{ focus = {ids[0]} }}\ncontinuous_focus_position = {{ x = {(right + 4) * 96} y = 16 }}\n" +
            "".join("shared_focus = " + i + "\n" for i in ids))
    return "# Original provisional gameplay; source: tools/content_waves (The Northern Reserve). Native acceptance pending.\n" + block("focus_tree", body)


def outputs():
    out = {}
    fe_files, fe = wave_files(free_erusea.WAVE, "free_erusea", free_erusea.owner())
    nc_files, nc = wave_files(nordennavic.WAVE, "nordennavic", nordennavic.owner())
    out.update(fe_files)
    out.update(nc_files)
    for tag in ("ERU", "FCU"):
        relative = f"common/national_focus/{tag}.txt"
        ids = [focus_id(free_erusea.WAVE, b, i) for b in free_erusea.WAVE.branches if b.tag == tag for i in range(6)]
        out[relative] = attach((MOD / relative).read_text(encoding="utf-8"), tag, ids)
    out["common/national_focus/NEC.txt"] = nec_tree(nc)
    return out, {"A": fe, "D": nc}


def inventory(frags):
    rows = []
    for key, wave in (("A", free_erusea.WAVE), ("D", nordennavic.WAVE)):
        where = frags[key]["positions"]
        for b in wave.branches:
            for i in range(6):
                ident = focus_id(wave, b, i)
                rows.append(dict(id=ident, wave=key, tag=b.tag, branch=b.key, title=b.titles[i], x=where[ident][0], y=where[ident][1],
                                 cost_days=70 if i in (1, 2, 5) else 35, purpose=PURPOSES[i],
                                 entry=list(b.entry) if i == 0 else [], gate=b.gate if i == 0 else "",
                                 exclusive_with=focus_id(wave, b, 2 if i == 1 else 1) if i in (1, 2) else None,
                                 source_layer="provisional gameplay"))
    counts = {}
    for row in rows:
        counts[row["tag"]] = counts.get(row["tag"], 0) + 1
    return dict(schema=1, title="Content waves A and D", counts=counts, total=len(rows),
                source_layers={"official_anchors": ["Chronicle 2005 / 09.26 provisional government under ISAF oversight (ac_ucw)",
                                                    "Chronicle 2006 / 09.26 Free Erusea insurrection (release_plan.json chronology)"],
                               "provisional_gameplay": "Every focus, policy, service, dialogue, value, the insurrection pressure model and its containment"},
                services=[dict(id=ident, tag=b.tag, branch=b.key, days=90, cooldown_days=90, political_power=35, capacity=4)
                          for key in ("A", "D") for b, n, ident in frags[key]["services"]],
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
    manifest = json.dumps(inventory(frags), indent=2, ensure_ascii=False) + "\n"
    path = HERE / "manifest.json"
    if args.check:
        if not path.exists() or path.read_text(encoding="utf-8") != manifest:
            failures.append("tools/content_waves/manifest.json")
    else:
        path.write_text(manifest, encoding="utf-8", newline="\n")
    if failures:
        raise SystemExit("Content waves output differs: " + ", ".join(failures))
    data = inventory(frags)
    print(f"Content waves A and D: {data['total']} focus definitions {data['counts']}, {len(data['services'])} funded services; "
          + ("consistent" if args.check else "generated"))


if __name__ == "__main__":
    main()
