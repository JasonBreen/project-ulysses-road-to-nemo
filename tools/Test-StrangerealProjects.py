#!/usr/bin/env python3
"""Offline contract checks for the Strangereal special projects (Track C and later owners).

Checks that the vanilla WWII projects and scientist traits are replaced, every
ac_sp_* project is localised and has mod-owned art, each project has a matching
no-DLC fallback decision granting the same reward, and the shared flag contract
with the Continental War (ac_ucw_*) and Yuktobania (ac_yuk_*) tracks holds.
Projects may live in any file under the replaced folders: the Track C files
(hash-pinned by the air and naval programmes) and the content-wave owners'
own files (tools/content_waves). Static only: this does not prove the engine
parses or reaches the content.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MOD = ROOT / "mod" / "2985041246"
REPLACE_PATHS = (
    "common/special_projects/projects",
    "common/special_projects/prototype_rewards",
    "common/special_projects/specialization",
    "common/special_projects/project_tags",
    "common/scientist_traits",
)
# Gates re-checked when a programme finishes; the fallback decision must also
# cancel on them, so a destroyed or seized target never pays out.
COMPLETION_GATES = {
    "ac_sp_excalibur": ("has_global_flag = excalibur_destroyed",),
    "ac_sp_v2": ("date",),
    "ac_sp_stonehenge": ("has_global_flag = ac_ucw_stonehenge_seized", "has_global_flag = ac_ucw_stonehenge_destroyed"),
    "ac_sp_megalith": ("has_global_flag = ac_ucw_megalith_destroyed",),
    "ac_sp_rhongomyniad": ("has_global_flag = excalibur_destroyed",),
    "ac_sp_arsenal_birds": ("has_global_flag = ac_lhw_arsenal_birds_lost",),
    "ac_sp_aerial_fleet": ("has_global_flag = ac_eew_aerial_fleet_lost",),
    "ac_sp_chandelier": ("has_global_flag = ac_eew_chandelier_lost",),
}
PROJECTS = (
    "ac_sp_excalibur",
    "ac_sp_v2",
    "ac_sp_stonehenge",
    "ac_sp_arkbird",
    "ac_sp_megalith",
    "ac_sp_rhongomyniad",
)
# Projects a content-wave owner adds; counted only once that owner's files exist.
OWNER_PROJECTS = {
    "lighthouse": ("ac_sp_arsenal_birds", "ac_sp_alicorn"),
    "anean_war": ("ac_sp_aerial_fleet", "ac_sp_chandelier"),
}
ENGINE_SPECIALIZATIONS = (
    "specialization_nuclear",
    "specialization_air",
    "specialization_naval",
    "specialization_land",
)
FOREIGN_FLAGS = re.compile(r"\b(?:set|clr)_(?:global|country)_flag\s*=\s*(ac_ucw_\w+|ac_yuk_\w+)")
# The Track C files (every one hash-pinned by tools/air_program and tools/naval_program).
CONTENT_FILES = (
    "common/special_projects/projects/ac_strangereal_projects.txt",
    "common/special_projects/prototype_rewards/ac_generic_prototype_rewards.txt",
    "common/special_projects/specialization/ac_specializations.txt",
    "common/special_projects/project_tags/ac_tags.txt",
    "common/scientist_traits/ac_scientist_traits.txt",
    "common/scripted_effects/ac_special_projects.txt",
    "common/ideas/ac_special_projects.txt",
    "common/decisions/ac_superweapons.txt",
    "common/decisions/categories/ac_superweapons.txt",
    "portraits/998_scientist_portraits.txt",
)
# Owners that add projects of their own (completion effects, reward ideas and
# fallback decisions in their own files, under the shared ac_superweapons category).
OWNER_FILES = {
    "lighthouse": (
        "common/scripted_effects/ac_lighthouse.txt",
        "common/ideas/ac_lighthouse.txt",
        "common/decisions/ac_lighthouse.txt",
    ),
    "anean_war": (
        "common/scripted_effects/ac_anean_war.txt",
        "common/ideas/ac_anean_war.txt",
        "common/decisions/ac_anean_war.txt",
    ),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def strip_comments(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def top_blocks(text: str) -> dict[str, str]:
    """Return {key: body} for every top-level `key = { ... }` block."""
    blocks: dict[str, str] = {}
    for match in re.finditer(r"(?m)^([A-Za-z0-9_]+)\s*=\s*\{", text):
        depth = 0
        for index in range(match.end() - 1, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    blocks[match.group(1)] = text[match.end() : index]
                    break
    return blocks


def inner_blocks(text: str, indent: str) -> dict[str, str]:
    return top_blocks("\n".join(line[len(indent):] if line.startswith(indent) else "~" + line
                                for line in text.splitlines()))


def localisation_keys(mod: Path) -> set[str]:
    keys: set[str] = set()
    for path in (mod / "localisation" / "english").rglob("*.yml"):
        for line in read(path).splitlines():
            match = re.match(r"\s+([A-Za-z0-9_.\-]+):\d*\s+\"", line)
            if match:
                keys.add(match.group(1))
    return keys


def sprites(mod: Path) -> dict[str, str]:
    """Map every mod sprite name to its texture path."""
    found: dict[str, str] = {}
    for path in (mod / "interface").glob("*.gfx"):
        text = strip_comments(read(path))
        for block in re.finditer(r"(?is)(?:spriteType|frameAnimatedSpriteType)\s*=\s*\{(.*?)\}", text):
            name = re.search(r'(?i)\bname\s*=\s*"?(GFX_\w+)', block.group(1))
            texture = re.search(r'(?i)\btexturefile\s*=\s*"?([^"\s}]+)', block.group(1))
            if name and texture:
                found[name.group(1)] = texture.group(1)
    return found


def texture_exists(mod: Path, texture: str) -> bool:
    return (mod / re.sub(r"/+", "/", texture.replace("\\", "/")).lstrip("/")).is_file()


def check(mod: Path) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    # Descriptors replace the vanilla project and trait databases.
    for descriptor in (mod / "descriptor.mod", mod / "ProjectUlysses.mod", mod.parent / f"{mod.name}.mod"):
        require(descriptor.is_file(), f"missing descriptor {descriptor.name}")
        if descriptor.is_file():
            text = read(descriptor)
            for replaced in REPLACE_PATHS:
                require(f'replace_path="{replaced}"' in text, f"{descriptor.name} lacks replace_path {replaced}")

    owners = {name: files for name, files in OWNER_FILES.items() if any((mod / f).is_file() for f in files)}
    owner_files = tuple(relative for files in owners.values() for relative in files)
    expected_projects = PROJECTS + tuple(p for name in owners for p in OWNER_PROJECTS.get(name, ()))
    for relative in CONTENT_FILES + owner_files:
        require((mod / relative).is_file(), f"missing {relative}")
    if errors:
        return errors

    # No vanilla sp_ project, reward, tag or trait can be defined or reached.
    defined: dict[str, dict[str, str]] = {}
    projects: dict[str, str] = {}
    tags: set[str] = set()
    for folder in REPLACE_PATHS:
        for path in sorted((mod / folder).glob("*.txt")):
            text = strip_comments(read(path))
            relative = path.relative_to(mod).as_posix()
            defined[relative] = top_blocks(text)
            require(not re.search(r"\bsp_(?!complexity|time|progress|scientist_xp_gain)\w+", text.replace("ac_sp_", "")),
                    f"{relative} references a vanilla sp_ token")
            require(not re.search(r"\bscientist_trait_\w+", text.replace("ac_scientist_trait_", "")),
                    f"{relative} references a vanilla scientist trait")
            if folder == "common/special_projects/projects":
                for name, body in defined[relative].items():
                    require(name not in projects, f"{name} is defined twice")
                    projects[name] = body
            elif folder == "common/special_projects/project_tags":
                tags |= set(re.findall(r"\bac_sp_tag_\w+", text))
    rewards = defined["common/special_projects/prototype_rewards/ac_generic_prototype_rewards.txt"]
    specializations = defined["common/special_projects/specialization/ac_specializations.txt"]
    traits = defined["common/scientist_traits/ac_scientist_traits.txt"]
    require(sorted(projects) == sorted(expected_projects), f"project set differs: {sorted(projects)}")
    require(sorted(specializations) == sorted(ENGINE_SPECIALIZATIONS),
            "specializations must redefine exactly the four engine tokens bound to facility buildings")
    for name in traits:
        require(name.startswith("ac_scientist_trait_"), f"non-mod scientist trait {name}")
    for relative in (p.relative_to(mod).as_posix() for p in mod.rglob("*.txt")):
        if relative.startswith(("common/", "events/", "history/")):
            text = strip_comments(read(mod / relative))
            for scope in re.findall(r"\bsp:(\w+)", text):
                require(scope in projects, f"{relative} scopes to undefined project sp:{scope}")
    for override in ("events/Special_Project_Events.txt", "common/technologies/special_projects_tech.txt"):
        text = strip_comments(read(mod / override)) if (mod / override).is_file() else None
        require(text is not None, f"missing vanilla override {override}")
        if text is not None:
            require(not re.search(r"\bsp:|\bsp_\w+_speed_factor", text), f"{override} still reaches vanilla projects")
    generic = strip_comments(read(mod / "common/decisions/_generic_decisions.txt"))
    require(not re.search(r"(?m)^special_projects\s*=", generic), "vanilla special_projects decisions remain")

    # Projects: specialization, tags, rewards, completion effect. Completion
    # effects, reward ideas and fallback decisions may come from any owner file.
    effects: dict[str, str] = {}
    decisions: dict[str, str] = {}
    idea_texts: list[str] = []
    for relative in CONTENT_FILES + owner_files:
        text = strip_comments(read(mod / relative))
        if relative.startswith("common/scripted_effects/"):
            for name, body in top_blocks(text).items():
                require(name not in effects, f"scripted effect {name} is defined twice")
                effects[name] = body
        elif relative.startswith("common/decisions/") and not relative.startswith("common/decisions/categories/"):
            for name, body in inner_blocks(top_blocks(text).get("ac_superweapons", ""), "\t").items():
                require(name not in decisions, f"fallback decision {name} is defined twice")
                decisions[name] = body
        elif relative.startswith("common/ideas/"):
            idea_texts.append(text)
    keys = localisation_keys(mod)
    gfx = sprites(mod)
    referenced_gfx: set[str] = set()
    for project, body in projects.items():
        specialization = re.search(r"\bspecialization\s*=\s*(\w+)", body)
        require(bool(specialization) and specialization.group(1) in specializations,
                f"{project} has no mod specialization")
        for tag in re.findall(r"\bac_sp_tag_\w+", body):
            require(tag in tags, f"{project} uses undefined tag {tag}")
        generic_block = re.search(r"generic_prototype_rewards\s*=\s*\{([^}]*)\}", body)
        for reward in (generic_block.group(1).split() if generic_block else []):
            require(reward in rewards, f"{project} uses undefined generic reward {reward}")
        effect = f"{project}_complete_effect"
        output = re.search(r"project_output\s*=\s*\{(.*?)\n\t\}", body, re.S)
        require(bool(output) and f"{effect} = yes" in output.group(1), f"{project} output does not call {effect}")
        require(effect in effects, f"missing scripted effect {effect}")
        require(f"set_global_flag = {project}_complete" in effects.get(effect, ""),
                f"{effect} does not set {project}_complete")
        decision = f"ac_superweapons_{project[len('ac_sp_'):]}"
        require(decision in decisions, f"{project} has no fallback decision {decision}")
        if decision in decisions:
            require(f"{effect} = yes" in decisions[decision], f"{decision} does not call {effect}")
            require('NOT = { has_dlc = "Gotterdammerung" }' in decisions[decision],
                    f"{decision} is not gated to players without Gotterdammerung")
            require(f"has_global_flag = {project}_complete" in decisions[decision],
                    f"{decision} is not guarded by {project}_complete")
            cancel = re.search(r"cancel_trigger\s*=\s*\{(.*?)\n\t\t\}", decisions[decision], re.S)
            for gate in COMPLETION_GATES.get(project, ()):
                require(bool(cancel) and gate in cancel.group(1), f"{decision} does not cancel on {gate}")
                require(gate in effects.get(effect, "").split("set_global_flag")[0],
                        f"{effect} does not re-check {gate} before completing")
            referenced_gfx.update(re.findall(r"\bGFX_\w+", decisions[decision]))
            for suffix in ("", "_desc"):
                require(decision + suffix in keys, f"missing localisation {decision + suffix}")
        for suffix in ("", "_desc"):
            require(project + suffix in keys, f"missing localisation {project + suffix}")
        referenced_gfx.update(re.findall(r"\bGFX_\w+", body))
        for token in re.findall(r"(?m)^\t\t(ac_sp_\w+)\s*=\s*\{", body):
            for suffix in ("", "_desc"):
                require(token + suffix in keys, f"missing localisation {token + suffix}")
        for option in re.findall(r"\btoken\s*=\s*(\w+)", body):
            require(option in keys, f"missing localisation {option}")
    for reward, body in rewards.items():
        referenced_gfx.update(re.findall(r"\bGFX_\w+", body))
        for suffix in ("", "_desc"):
            require(reward + suffix in keys, f"missing localisation {reward + suffix}")
        for option in re.findall(r"\btoken\s*=\s*(\w+)", body):
            require(option in keys, f"missing localisation {option}")

    # Ideas, traits, tags, specializations, categories and portraits.
    completion_effects = "\n".join(body for name, body in effects.items() if name.endswith("_complete_effect"))
    for idea_text in idea_texts:
        for idea, picture in re.findall(r"(?m)^\t\t(ac_sp_\w+)\s*=\s*\{\s*picture\s*=\s*(\w+)", idea_text):
            referenced_gfx.add(f"GFX_idea_{picture}")
            for suffix in ("", "_desc"):
                require(idea + suffix in keys, f"missing localisation {idea + suffix}")
            require(f"add_ideas = {idea}" in completion_effects, f"idea {idea} is never granted by a completion effect")
    for trait, body in traits.items():
        require(trait in keys, f"missing localisation {trait}")
        referenced_gfx.update(re.findall(r"\bGFX_\w+", body))
    for tag in tags:
        for suffix in ("", "_speed_factor", "_speed_factor_tt"):
            require(tag + suffix in keys, f"missing localisation {tag + suffix}")
    for token, body in specializations.items():
        require(token in keys, f"missing localisation {token}")
        referenced_gfx.update(re.findall(r"\bGFX_\w+", body))
    for relative in ("common/decisions/categories/ac_superweapons.txt", "portraits/998_scientist_portraits.txt"):
        referenced_gfx.update(re.findall(r"\bGFX_\w+", strip_comments(read(mod / relative))))
    category = strip_comments(read(mod / "common/decisions/categories/BLK_decisions_categories.txt"))
    excalibur = top_blocks(category).get("BLK_excalibur_cat", "")
    referenced_gfx.update(re.findall(r"\bicon\s*=\s*(GFX_\w+)", excalibur))
    require("tur_the_constitutional_arrows" not in excalibur, "BLK_excalibur_cat still borrows a vanilla icon")
    for name in ("ac_superweapons", "ac_superweapons_desc", "ac_superweapons_programme_started_tt"):
        require(name in keys, f"missing localisation {name}")
    for sprite in sorted(referenced_gfx):
        require(sprite in gfx, f"sprite {sprite} is not defined by the mod")
        if sprite in gfx:
            require(texture_exists(mod, gfx[sprite]), f"sprite {sprite} uses unshipped texture {gfx[sprite]}")
    techtree = strip_comments(read(mod / "interface/countrytechtreeview.gfx"))
    for name, texture in sprites(mod).items():
        if "special_project" in name and name.startswith("GFX_technology_"):
            require(texture_exists(mod, texture), f"tech-tree sprite {name} uses unshipped texture {texture}")
    require("technology_special_project_" not in techtree, "tech tree still points at unshipped special-project textures")
    for path in (mod / "localisation/english/ac_special_projects_l_english.yml",
                 mod / "localisation/english/replace/ac_special_projects_replace_l_english.yml"):
        require(path.read_bytes().startswith(b"\xef\xbb\xbf"), f"{path.name} lacks a UTF-8 BOM")

    # Shared flag contract: the Track C files set only their own completion flags,
    # and no project file writes another track's flags.
    for relative in CONTENT_FILES + owner_files:
        if relative.startswith(("common/special_projects/", "common/scripted_effects/ac_special_projects")):
            for flag in FOREIGN_FLAGS.findall(strip_comments(read(mod / relative))):
                errors.append(f"{relative} writes {flag}, which another track owns")
    set_flags = set(re.findall(r"\bset_global_flag\s*=\s*(\w+)", completion_effects))
    require(set_flags == {f"{project}_complete" for project in expected_projects},
            f"completion effects set unexpected flags: {sorted(set_flags)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod-root", type=Path, default=DEFAULT_MOD)
    args = parser.parse_args()
    errors = check(args.mod_root.resolve())
    if errors:
        print("Strangereal special project checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    owners = [name for name, files in OWNER_FILES.items() if any((args.mod_root / f).is_file() for f in files)]
    count = len(PROJECTS) + sum(len(OWNER_PROJECTS.get(name, ())) for name in owners)
    print(f"Strangereal special projects: {count} projects with fallback decisions, art and localisation (static).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
