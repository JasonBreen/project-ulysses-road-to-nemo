"""Inventory effective GUI and runtime art consumers, including engine fallback.

This is a source dependency audit, not a native render/reachability certificate.
Same-path mod overrides and descriptor replace_path isolation are applied before
indexing definitions. Runtime icons, portraits, MIOs, agencies, model clone/mesh/
animation edges and audio references are reported separately from screen gates.
Only requested screens are gated. A clean gate never means the backlog is empty.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT_MOD = ROOT / "mod/2985041246"
sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
from script import get, parse, walk


def scalar(value):
    return value.strip('"') if isinstance(value, str) else value


def normal(value):
    return re.sub(r"/+", "/", value.replace("\\", "/")).strip("/").lower()


def fields(node):
    for key, _, value in node:
        if isinstance(value, str):
            yield key.lower(), scalar(value)


class EffectiveFiles:
    def __init__(self, mod, engine):
        self.mod, self.engine = mod.resolve(), engine.resolve()
        self.replace_paths = []
        descriptor = self.mod / "descriptor.mod"
        if descriptor.exists():
            self.replace_paths = [normal(scalar(value)) for key, _, value in parse(descriptor.read_text(encoding="utf-8-sig"))
                                  if key.lower() == "replace_path" and isinstance(value, str)]
        self._files = {}
        # Build once, with case-insensitive relative paths matching Windows.
        for origin, base in (("engine", self.engine), ("mod", self.mod)):
            for folder in ("interface", "common", "gfx", "sound", "music", "events", "history"):
                root = base / folder
                if not root.exists():
                    continue
                for path in root.rglob("*"):
                    if not path.is_file():
                        continue
                    relative = normal(path.relative_to(base).as_posix())
                    if origin == "engine" and any(relative == p or relative.startswith(p + "/") for p in self.replace_paths):
                        continue
                    self._files[relative] = (origin, path)

    def files(self, prefix, suffix=None, authored_only=False):
        prefix = normal(prefix)
        return [(rel, origin, path) for rel, (origin, path) in sorted(self._files.items())
                if (rel == prefix or rel.startswith(prefix + "/"))
                and (suffix is None or path.suffix.lower() in suffix)
                and (not authored_only or origin == "mod")]

    def resource(self, value, source=None):
        requested = normal(value)
        relative = requested
        found = self._files.get(relative)
        if found is None and source:
            # Sound assets sometimes use a path relative to their definition.
            relative = normal(str(Path(source).parent / value))
            found = self._files.get(relative)
        if found:
            origin, _ = found
            service = Path(relative).suffix.lower() in (".lua", ".fx", ".shader", ".fxh")
            return dict(path=relative, status="engine_service" if origin == "engine" and service else "mod_asset" if origin == "mod" else "engine_asset")
        if any(normal(value) == p or normal(value).startswith(p + "/") for p in self.replace_paths):
            return dict(path=normal(value), status="missing_asset", isolated_engine_path=True)
        # Engine shaders are services, not artwork, and are intentionally not
        # copied into the mod. Retain their ownership in the report.
        candidate = self.engine / requested
        if candidate.is_file():
            return dict(path=normal(value), status="engine_service" if candidate.suffix.lower() in (".lua", ".fx", ".shader", ".fxh") else "engine_asset")
        if requested.endswith(".lua"):
            shader = requested[:-4] + ".shader"
            if (self.engine / shader).is_file():
                return dict(path=shader, status="engine_service", legacy_alias=normal(value))
        return dict(path=normal(value), status="missing_asset")


class Audit:
    def __init__(self, mod, engine):
        self.vfs = EffectiveFiles(mod, engine)
        self.definitions = defaultdict(lambda: defaultdict(list))
        self.trees = {}
        self.parse_failures = []
        self._cache = {}
        self.rows = []
        self.retired_consumers = []
        self.index()

    def read(self, rel, origin, path):
        if rel in self.trees:
            return self.trees[rel]
        try:
            tree = parse(path.read_text(encoding="utf-8-sig", errors="replace"))
        except (ValueError, IndexError) as exc:
            self.parse_failures.append(dict(source=rel, origin=origin, error=str(exc)))
            tree = []
        self.trees[rel] = tree
        return tree

    def register(self, family, name, rel, origin, kind, node):
        if name:
            self.definitions[family][name].append(dict(source=rel, origin=origin, kind=kind, node=node))

    def index(self):
        for rel, origin, path in self.vfs.files("interface", {".gfx", ".gui"}):
            tree = self.read(rel, origin, path)
            if path.suffix.lower() == ".gfx":
                for kind, _, node in get(tree, "spriteTypes", []):
                    if isinstance(node, list):
                        self.register("sprite", scalar(get(node, "name", "")), rel, origin, kind, node)
                for kind, node in walk(tree):
                    if kind.lower() in ("bitmapfont", "font"):
                        self.register("font", scalar(get(node, "name", "")), rel, origin, kind, node)
            else:
                for kind, _, node in get(tree, "guiTypes", []):
                    if isinstance(node, list):
                        self.register("template", scalar(get(node, "name", "")), rel, origin, kind, node)
        for prefix, suffixes in (("gfx", {".gfx", ".asset"}), ("sound", {".asset"}), ("music", {".asset"})):
            for rel, origin, path in self.vfs.files(prefix, suffixes):
                tree = self.read(rel, origin, path)
                for kind, node in walk(tree):
                    family = {"entity": "entity", "pdxmesh": "mesh", "animation": "animation",
                              "sound": "sound", "soundeffect": "audio", "music": "music"}.get(kind.lower())
                    if family:
                        self.register(family, scalar(get(node, "name", "")), rel, origin, kind, node)
        for rel, origin, path in self.vfs.files("common/military_industrial_organization/organizations", {".txt"}):
            for name, _, node in self.read(rel, origin, path):
                if isinstance(node, list):
                    self.register("mio", name, rel, origin, "organization", node)

    def definition(self, family, name):
        candidates = self.definitions[family].get(name, [])
        if not candidates:
            return None, []
        # Cross-file duplicate load order is not certified by this audit. Use
        # mod-last only for the explanatory trace and report every conflict.
        ordered = sorted(candidates, key=lambda d: (d["origin"] == "mod", d["source"]))
        signatures = {json.dumps(d["node"], sort_keys=True) for d in ordered}
        conflict = [d["source"] for d in ordered] if len(signatures) > 1 else []
        return ordered[-1], conflict

    def resolve(self, family, name, visiting=None):
        token = (family, name)
        if token in self._cache:
            return self._cache[token]
        visiting = set() if visiting is None else set(visiting)
        if token in visiting:
            return dict(family=family, name=name, status="dependency_cycle", resources=[])
        visiting.add(token)
        definition, conflicts = self.definition(family, name)
        if definition is None:
            return dict(family=family, name=name, status="missing_definition", resources=[])
        node = definition["node"]; resources = []; dependencies = []
        for kind, child in [(definition["kind"], node)] + list(walk(node)):
            for key, value in fields(child):
                if key in ("texturefile", "texturefile1", "texturefile2", "diffuse", "normalmap", "specularmap",
                           "texture_diffuse", "texture_normal", "texture_specular"):
                    resources.append(self.vfs.resource(value, definition["source"]))
                elif key in ("file", "meshfile", "animationfile", "effectfile"):
                    if value and ("/" in value or "\\" in value or Path(value).suffix):
                        resources.append(self.vfs.resource(value, definition["source"]))
                elif key == "path" and family == "font":
                    for extension in (".fnt", ".dds"):
                        resources.append(self.vfs.resource(value + extension))
                elif family == "entity" and key in ("clone", "pdxmesh"):
                    dependencies.append(self.resolve("entity" if key == "clone" else "mesh", value, visiting))
                elif family == "entity" and kind.lower() == "attach" and key != "name" and value.endswith("_entity"):
                    dependencies.append(self.resolve("entity", value, visiting))
                elif family == "mesh" and kind.lower() == "animation" and key == "type":
                    dependencies.append(self.resolve("animation", value, visiting))
                elif family == "audio" and key in ("sound", "sounds"):
                    dependencies.append(self.resolve("sound", value, visiting))
                elif family == "mio" and key == "include":
                    dependencies.append(self.resolve("mio", value, visiting))
                elif family == "mio" and key == "icon":
                    candidates = [value] if value.startswith("GFX_") else ["GFX_" + value, "GFX_mio_" + value]
                    sprite = next((v for v in candidates if v in self.definitions["sprite"]), candidates[0])
                    dependencies.append(self.resolve("sprite", sprite, visiting))
        issues = {r["status"] for r in resources if r["status"] in ("missing_asset", "engine_asset")}
        issues.update(d["status"] for d in dependencies if d["status"] not in ("mod_resolved", "engine_service"))
        if conflicts:
            status = "conflicting_definitions"
        elif "dependency_cycle" in issues:
            status = "dependency_cycle"
        elif any(s.startswith("missing") for s in issues):
            status = "missing_asset_or_dependency"
        elif issues or (not resources and not dependencies and definition["origin"] == "engine"):
            status = "engine_fallback"
        elif not resources and not dependencies:
            status = "runtime_binding_uninspected"
        else:
            status = "mod_resolved"
        result = dict(family=family, name=name, status=status, definition=definition["source"],
                      definition_origin=definition["origin"], resources=resources)
        if dependencies:
            result["dependencies"] = dependencies
        if conflicts:
            result["conflicts"] = conflicts
        self._cache[token] = result
        return result

    def row(self, family, name, source, owner, consumer_family):
        result = dict(self.resolve(family, name))
        result.update(consumer=source, owner=owner, consumer_family=consumer_family)
        self.rows.append(result)
        return result

    def icon(self, value, source, owner, family, prefixes=()):
        candidates = [value] if value.startswith("GFX_") else [p + value for p in prefixes] + [value, "GFX_" + value]
        name = next((n for n in candidates if n in self.definitions["sprite"]), candidates[0])
        return self.row("sprite", name, source, owner, family)

    def screen(self, filename, runtime_decisions=False):
        rel = "interface/" + filename.lower()
        found = self.vfs._files.get(rel)
        if not found:
            return dict(source=rel, failures=["missing screen"], consumers=[])
        origin, path = found; tree = self.read(rel, origin, path)
        queue = [(rel, tree)]; seen = set(); rows = []; templates = []
        while queue:
            source, nodes = queue.pop()
            for kind, node in walk(nodes):
                owner = scalar(get(node, "name", kind))
                for key, value in fields(node):
                    if not value:
                        continue
                    if key in ("spritetype", "quadtexturesprite"):
                        rows.append(self.row("sprite", value, source, owner, "screen"))
                    elif key in ("font", "buttonfont"):
                        rows.append(self.row("font", value, source, owner, "screen"))
                    elif key in ("verticalscrollbar", "horizontalscrollbar", "scrollbartype"):
                        if value in seen:
                            continue
                        seen.add(value)
                        definition, conflict = self.definition("template", value)
                        if definition is None:
                            rows.append(dict(family="template", name=value, status="missing_definition", consumer=source, owner=owner))
                        else:
                            templates.append(dict(name=value, source=definition["source"], conflicts=conflict))
                            queue.append((definition["source"], [[definition["kind"], "=", definition["node"]]]))
        if runtime_decisions:
            rows.extend(self.decision_consumers())
        # Audio and the nation's runtime-selected flag are separate inventories;
        # this gate certifies texture/font/template resolution, not provenance,
        # actual visibility, screen position, sound replacement or native input.
        failures = sorted({r["family"] + ":" + r["name"] + ":" + r["status"] for r in rows
                           if r["status"] != "mod_resolved"})
        failures.extend("template:" + t["name"] + ":conflicting_definitions" for t in templates if t["conflicts"])
        failures.extend("parse:" + row["source"] for row in self.parse_failures
                        if row["source"] == rel or runtime_decisions and row["source"].startswith("common/decisions/"))
        return dict(source=rel, origin=origin, coverage="effective GUI textures/fonts/scrollbar templates and authored decision icons; not native rendering",
                    templates=templates, consumers=rows, failures=failures)

    def decision_consumers(self):
        rows = []
        for rel, origin, path in self.vfs.files("common/decisions", {".txt"}):
            if origin != "mod":
                continue
            tree = self.read(rel, origin, path)
            if "/categories/" in rel:
                entries = tree; category = True
            else:
                entries = [entry for _, _, node in tree if isinstance(node, list) for entry in node]; category = False
            for name, _, node in entries:
                if not isinstance(node, list):
                    continue
                # Statically retired categories/decisions cannot display art.
                disabled = any(get(get(node, key, []), "always") == "no" for key in ("allowed", "visible"))
                if disabled:
                    self.retired_consumers.append(dict(consumer=rel, owner=name,
                                                        reason="statically disabled by allowed/visible always = no",
                                                        consumer_family="decision_category" if category else "decision",
                                                        icon=scalar(get(node, "icon", "<engine default>"))))
                    continue
                value = scalar(get(node, "icon", ""))
                if isinstance(value, str) and value:
                    prefixes = ("GFX_decision_category_", "GFX_decision_") if category else ("GFX_decision_",)
                    rows.append(self.icon(value, rel, name, "decision_category" if category else "decision", prefixes))
                elif not value:
                    rows.append(self.icon("GFX_decision_category_generic" if category else "GFX_decision_unknown", rel, name, "decision_default"))
                else:
                    # Conditional icon blocks have runtime branches. Inspect all
                    # scalar GFX candidates instead of assuming the first branch.
                    for _, child in walk([["icon", "=", value]]):
                        for key, candidate in fields(child):
                            if key in ("icon", "value") and candidate.startswith("GFX_"):
                                rows.append(self.icon(candidate, rel, name, "conditional_decision_icon"))
                picture = scalar(get(node, "picture", ""))
                if isinstance(picture, str) and picture:
                    rows.append(self.icon(picture, rel, name, "decision_picture", ("GFX_",)))
        return rows

    def scripted_bindings(self):
        windows = defaultdict(list)
        for rel, origin, path in self.vfs.files("interface", {".gui"}):
            for kind, node in walk(self.read(rel, origin, path)):
                if kind.lower() == "containerwindowtype" and get(node, "name"):
                    windows[scalar(get(node, "name"))].append((rel, node))
        rows = []
        for rel, origin, path in self.vfs.files("common/scripted_guis", {".txt"}, authored_only=True):
            for ident, _, node in get(self.read(rel, origin, path), "scripted_gui", []):
                if not isinstance(node, list):
                    continue
                window = scalar(get(node, "window_name", ""))
                found = windows.get(window, [])
                problems = []
                if not found:
                    problems.append("missing window " + window)
                    controls = set()
                else:
                    controls = {scalar(get(child, "name", "")) for _, body in found for _, child in walk([["window", "=", body]])}
                for effect, _, _ in get(node, "effects", []):
                    button = re.sub(r"_(?:(?:alt|control|shift|right)_)*click$", "", effect)
                    if button not in controls:
                        problems.append("missing click target " + button)
                for _, _, dynamic in get(node, "dynamic_lists", []):
                    template = scalar(get(dynamic, "entry_container", ""))
                    if template and template not in windows:
                        problems.append("missing dynamic-list entry " + template)
                rows.append(dict(source=rel, scripted_gui=ident, window=window,
                                 status="missing_binding" if problems else "bindings_resolved",
                                 definitions=sorted({source for source, _ in found}), problems=problems))
        return rows

    def runtime(self):
        # These are actual authored consumers. We do not assert that every
        # branch is reachable in a played campaign or every DLC is active.
        for prefix, family in (("common/characters", "portrait"),
                               ("common/military_industrial_organization/organizations", "mio"),
                               ("common/intelligence_agencies", "agency")):
            for rel, origin, path in self.vfs.files(prefix, {".txt"}, authored_only=True):
                tree = self.read(rel, origin, path)
                for kind, node in walk(tree):
                    for key, value in fields(node):
                        if family == "portrait" and key in ("large", "small"):
                            if value.startswith("GFX_"):
                                self.icon(value, rel, kind, family)
                            else:
                                resource = self.vfs.resource(value, rel)
                                self.rows.append(dict(consumer_family=family, consumer=rel, owner=kind, family="file", name=value,
                                                      status=resource["status"], resources=[resource]))
                        elif family in ("mio", "agency") and key in ("icon", "picture", "portrait"):
                            self.icon(value, rel, kind, family, ("GFX_", "GFX_mio_", "GFX_intelligence_agency_"))
        for name, definitions in sorted(self.definitions["mio"].items()):
            if any(d["origin"] == "mod" for d in definitions):
                d, _ = self.definition("mio", name)
                self.row("mio", name, d["source"], name, "mio_inheritance")
        # Content-selected focus, continuous-focus and event pictures do not
        # appear as literal GUI sprites. Ideas use the engine's GFX_idea_ prefix.
        for prefix, family in (("common/national_focus", "focus"), ("common/continuous_focus", "continuous_focus"),
                               ("common/ideas", "idea"), ("events", "event_picture"), ("common/technologies", "technology")):
            for rel, origin, path in self.vfs.files(prefix, {".txt"}, authored_only=True):
                for kind, node in walk(self.read(rel, origin, path)):
                    for key, value in fields(node):
                        if family in ("focus", "continuous_focus") and key == "icon":
                            self.icon(value, rel, scalar(get(node, "id", kind)), family, ("GFX_goal_",))
                        elif family in ("event_picture", "idea") and key == "picture":
                            self.icon(value, rel, scalar(get(node, "id", kind)), family,
                                      ("GFX_idea_",) if family == "idea" else ("GFX_",))
                        elif family == "technology" and key in ("picture", "icon"):
                            self.icon(value, rel, kind, family, ("GFX_",))
        # Models include inherited clone/attachment/mesh/animation edges, rather
        # than claiming a local infantry texture makes the whole entity local.
        for family in ("entity", "mesh", "animation", "audio", "sound", "music"):
            for name, definitions in sorted(self.definitions[family].items()):
                if any(d["origin"] == "mod" for d in definitions):
                    d, _ = self.definition(family, name)
                    self.row(family, name, d["source"], name, "model" if family in ("entity", "mesh", "animation") else "audio")
        # Runtime culture/model selection is generated by engine conventions.
        # Log named unit sprite consumers and mark unexpanded convention roots.
        for rel, origin, path in self.vfs.files("common/units", {".txt"}, authored_only=True):
            for kind, node in walk(self.read(rel, origin, path)):
                for key, value in fields(node):
                    if key in ("sprite", "entity"):
                        if value in self.definitions["entity"]:
                            self.row("entity", value, rel, kind, "unit_model")
                        else:
                            self.rows.append(dict(consumer_family="unit_model", family="entity_convention", name=value,
                                                  consumer=rel, owner=kind, status="runtime_binding_uninspected", resources=[]))
        # Menu, UI and event sounds are consumers too. Engine click services are
        # retained but visible in the ledger, outside the imagery screen gate.
        for prefix, suffixes in (("interface", {".gui"}), ("events", {".txt"}), ("common/scripted_effects", {".txt"})):
            for rel, origin, path in self.vfs.files(prefix, suffixes, authored_only=True):
                for kind, node in walk(self.read(rel, origin, path)):
                    for key, value in fields(node):
                        if key in ("clicksound", "show_sound", "hide_sound", "play_sound", "soundeffect") and value:
                            self.row("audio", value, rel, scalar(get(node, "name", kind)), "audio_consumer")

    def run(self, screens):
        covered = {filename: self.screen(filename, filename.lower() == "countrydecisionview.gui") for filename in screens}
        self.runtime()
        unique = {json.dumps(row, sort_keys=True): row for row in self.rows}
        rows = sorted(unique.values(), key=lambda r: (r.get("consumer_family", ""), r["consumer"], r["name"]))
        counts = Counter(row["status"] for row in rows)
        by_family = defaultdict(Counter)
        for row in rows:
            by_family[row.get("consumer_family", row["family"])][row["status"]] += 1
        archives = [dict(path=path.relative_to(self.vfs.engine).as_posix(), bytes=path.stat().st_size)
                    for path in sorted((self.vfs.engine / "dlc").rglob("*.zip"))]
        return dict(schema=1, coverage="initial Package 0 loose-file effective dependency inventory; not full conversion acceptance, native acceptance or proof of original asset provenance",
                    engine_version="read installed launcher-settings/version separately; no runtime version inferred",
                    dlc_archive_coverage=dict(status="uninspected", installed_archive_inventory=archives,
                                              activation="unknown; installed archives do not prove ownership or active DLC",
                                              gate_scope="loose installed engine + authored mod only"),
                    replace_paths=self.vfs.replace_paths, gate_covered_screens=covered,
                    summary=dict(counts), by_consumer_family={k: dict(v) for k, v in sorted(by_family.items())},
                    parse_failures=self.parse_failures,
                    scripted_gui_bindings=self.scripted_bindings(),
                    statically_retired_consumers=self.retired_consumers,
                    coverage_limits=["Engine-generated entity/culture combinations are logged but not fully expanded.",
                                     "Runtime-selected country flags and native DLC membership need native checks.",
                                     "MIO/agency conditional branches are inspected; their gameplay reachability is not certified.",
                                     "Mod-local paths do not prove originality, copyright permission, or absence of copied vanilla pixels.",
                                     "Only explicitly gated screens affect exit status; model/audio/portrait backlog is reported, not silently waived."],
                    consumers=rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("engine", type=Path)
    p.add_argument("--mod-root", type=Path, default=DEFAULT_MOD)
    p.add_argument("--screen", action="append", default=[])
    p.add_argument("--gate-decisions", action="store_true")
    p.add_argument("--gate-screen", action="append", default=[], help="Gate another complete effective loose-file screen by filename")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    screens = list(dict.fromkeys(["countrydecisionview.gui"] + args.screen + args.gate_screen))
    report = Audit(args.mod_root, args.engine).run(screens)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(summary=report["summary"], by_consumer_family=report["by_consumer_family"],
                          screen_failures={k: v["failures"] for k, v in report["gate_covered_screens"].items()},
                          parse_failures=len(report["parse_failures"])), indent=2))
    gates = (["countrydecisionview.gui"] if args.gate_decisions else []) + args.gate_screen
    if any(report["gate_covered_screens"][name]["failures"] for name in gates):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
