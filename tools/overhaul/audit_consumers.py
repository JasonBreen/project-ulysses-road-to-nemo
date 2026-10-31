"""Inventory effective GUI and runtime art consumers, including engine fallback.

This is a source dependency audit, not a native render/reachability certificate.
Same-path mod overrides and descriptor replace_path isolation are applied before
indexing definitions. Runtime icons, portraits, MIOs, agencies, model clone/mesh/
animation edges and audio references are reported separately from screen gates.
Legacy ownership gates cover requested screens; --gate-presentation also gates
all supported conservative roots in an explicit DLC audit profile. A clean
source gate never certifies native visibility or unsupported binary bindings.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import posixpath
from pathlib import Path
import re
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT_MOD = ROOT / "mod/2985041246"
MEDIA_SUFFIXES = {".dds", ".tga", ".png", ".jpg", ".jpeg", ".bmp", ".mesh", ".anim", ".wav", ".ogg", ".fnt", ".ttf", ".lua", ".shader", ".fx", ".fxh"}
RESOURCE_SUFFIXES = {"image": {".dds", ".tga", ".png", ".jpg", ".jpeg", ".bmp"},
                     "program": {".lua", ".shader", ".fx", ".fxh"},
                     "audio": {".wav", ".ogg"}, "font": {".fnt", ".ttf"},
                     "mesh": {".mesh"}, "animation": {".anim"}}
sys.path.insert(0, str(ROOT / "tools/usea_expansion"))
from script import get, parse, walk
from providers import Providers


def scalar(value):
    return value.strip('"') if isinstance(value, str) else value


def normal(value):
    return re.sub(r"/+", "/", value.replace("\\", "/")).strip("/").lower()


def fields(node):
    for key, _, value in node:
        if isinstance(value, str):
            yield key.lower(), scalar(value)


class EffectiveFiles:
    def __init__(self, mod, engine, profile=None):
        self.mod, self.engine = Path(mod).resolve(), Path(engine).resolve()
        self.providers = Providers(self.mod, self.engine, parse, profile)
        self.replace_paths = self.providers.replace_paths
        self._files = self.providers.files

    def files(self, prefix, suffix=None, authored_only=False):
        prefix = normal(prefix)
        return [(rel, origin, path) for rel, (origin, path) in sorted(self._files.items())
                if (rel == prefix or rel.startswith(prefix + "/"))
                and (suffix is None or path.suffix.lower() in suffix)
                and (not authored_only or origin == "mod")]

    def resource(self, value, source=None, usage=None):
        requested = normal(value)
        probes = [requested]
        if source:
            relative = normal(posixpath.normpath(posixpath.join(posixpath.dirname(source), value.replace("\\", "/"))))
            if relative not in probes:
                probes.append(relative)
        found = [(candidate, self._files[candidate][1]) for candidate in probes if candidate in self._files]
        alias = None
        if not found and requested.endswith(".lua"):
            shader = requested[:-4] + ".shader"
            if shader in self._files:
                found = [(shader, self._files[shader][1])]; alias = requested
        if found:
            relative, asset = found[0]
            ambiguous = relative in self.providers.ambiguities
            if len(found)>1:
                try:
                    ambiguous |= len({candidate.sha256() for _, candidate in found})>1
                except (OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError):
                    ambiguous = True
            classification, evidence = self.providers.classify(asset, usage)
            wrong_type = usage in RESOURCE_SUFFIXES and asset.suffix.lower() not in RESOURCE_SUFFIXES[usage]
            if wrong_type:
                classification, evidence = "unresolved", "Resource type does not satisfy its " + usage + " binding"
            service = classification == "technical"
            result = dict(path=relative, status="ambiguous_asset" if ambiguous else "unsupported_resource_kind" if wrong_type else
                          "engine_service" if asset.origin == "engine" and service else
                          "mod_asset" if asset.origin == "mod" else "engine_asset",
                          provider=asset.provider, source=asset.source, bytes=asset.bytes, sha256=asset._hash, classification="unresolved" if ambiguous else classification,
                          classification_evidence=evidence)
            if usage:
                result["binding_usage"] = usage
            if ambiguous:
                result["provider_candidates"] = self.providers.ambiguities.get(relative, [a.metadata() for _, a in found])
            if alias:
                result["legacy_alias"] = alias
            if asset.suffix.lower() == ".mesh":
                result["binary_material_dependencies"] = "uninspected; declared mesh settings are audited separately"
            return result
        return dict(path=requested, status="missing_asset", classification="unresolved",
                    isolated_engine_path=any(requested == p or requested.startswith(p + "/") for p in self.replace_paths))


class Audit:
    def __init__(self, mod, engine, profile=None):
        self.vfs = EffectiveFiles(mod, engine, profile)
        self.definitions = defaultdict(lambda: defaultdict(list))
        self.trees = {}
        self.parse_failures = []
        self._cache = {}
        self.rows = []
        self._complete = False
        self.retired_consumers = []
        self.index()

    def read(self, rel, origin, path):
        if rel in self.trees:
            return self.trees[rel]
        try:
            tree = parse(path.read_text(encoding="utf-8-sig", errors="replace"))
        except (ValueError, IndexError, OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError) as exc:
            self.parse_failures.append(dict(source=rel, origin=origin, provider=getattr(path,"provider",origin), provider_source=getattr(path,"source",rel), error=str(exc).replace(str(self.vfs.engine), "engine://").replace(str(self.vfs.mod), "mod://")))
            tree = []
        self.trees[rel] = tree
        return tree

    def register(self, family, name, rel, origin, kind, node):
        if name:
            self.definitions[family][name].append(dict(source=rel, origin=origin, kind=kind, node=node, provider=self.vfs._files[rel][1].provider,
                                                      provider_source=self.vfs._files[rel][1].source))

    def index(self):
        for rel, origin, path in self.vfs.files("interface", {".gfx", ".gui"}):
            tree = self.read(rel, origin, path)
            if path.suffix.lower() == ".gfx":
                for kind, _, node in get(tree, "spriteTypes", []):
                    if isinstance(node, list):
                        self.register("sprite", scalar(get(node, "name", "")), rel, origin, kind, node)
                for kind, _, node in get(tree, "objectTypes", []):
                    if isinstance(node, list):
                        self.register("presentation_object", scalar(get(node, "name", "")), rel, origin, kind, node)
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
                              "sound": "sound", "soundeffect": "audio", "music": "music",
                              "particle": "particle", "pdxparticle": "particle_proxy"}.get(kind.lower())
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
        # Equal text in different directories can still bind different relative
        # media. Do not certify that duplicate by comparing node text alone.
        signatures = set()
        for definition in ordered:
            relative_context = any(Path(value).suffix.lower() in MEDIA_SUFFIXES
                                   for _, node in [(definition["kind"], definition["node"])] + list(walk(definition["node"]))
                                   for key, value in fields(node) if key not in ("name", "id", "text", "tooltip", "description"))
            signatures.add(json.dumps([definition["node"], posixpath.dirname(definition["source"]) if relative_context else None], sort_keys=True))
        conflict = [d["provider_source"] for d in ordered] if len(signatures) > 1 else []
        for definition in ordered:
            if definition["source"] in self.vfs.providers.ambiguities:
                conflict.extend(row["source"] for row in self.vfs.providers.ambiguities[definition["source"]])
        return ordered[-1], conflict

    def resolve(self, family, name, visiting=None):
        token = (family, name)
        if token in self._cache:
            return self._cache[token]
        visiting = set() if visiting is None else set(visiting)
        if token in visiting:
            return dict(family=family, name=name, status="dependency_cycle", classification="unresolved", resources=[])
        if len(visiting) >= 128:
            return dict(family=family,name=name,status="dependency_depth_uninspected",classification="unresolved",resources=[])
        visiting.add(token)
        definition, conflicts = self.definition(family, name)
        if definition is None:
            return dict(family=family, name=name, status="missing_definition", classification="unresolved", resources=[])
        node = definition["node"]; resources = []; dependencies = []; animation_ids = set(); state_animations = set(); materials = []
        for kind, child in [(definition["kind"], node)] + list(walk(node)):
            for key, value in fields(child):
                if key in ("texturefile", "texturefile1", "texturefile2", "diffuse", "normalmap", "specularmap",
                           "texture_diffuse", "texture_normal", "texture_specular", "animationmaskfile", "animationtexturefile",
                           "texture", "normal", "specular", "masking_texture"):
                    resources.append(self.vfs.resource(value, definition["source"], usage="image"))
                elif key in ("file", "meshfile", "animationfile", "effectfile"):
                    if value and ("/" in value or "\\" in value or Path(value).suffix):
                        usage = {"meshfile": "mesh", "animationfile": "animation", "effectfile": "program"}.get(key)
                        if key == "file":
                            usage = {"sound": "audio", "song": "audio", "audio": "audio", "sprite": "image", "mesh": "mesh", "animation": "animation", "font": "font"}.get(family)
                        resources.append(self.vfs.resource(value, definition["source"], usage=usage))
                elif key == "path" and family == "font":
                    for extension in (".fnt", ".dds"):
                        resources.append(self.vfs.resource(value + extension, usage="font" if extension == ".fnt" else "image"))
                elif family == "entity" and key in ("clone", "pdxmesh"):
                    dependency = self.resolve("entity" if key == "clone" else "mesh", value, visiting)
                    dependencies.append(dependency)
                    animation_ids.update(dependency.get("declared_animation_ids", []))
                elif family == "entity" and kind.lower() == "attach" and key not in ("name", "node", "target", "scale", "position", "rotation"):
                    # Attachment names need not use an _entity suffix. Numeric
                    # transform fields are data; other named targets stay visible.
                    if not re.fullmatch(r"[-+0-9.eE]+", value) and value not in ("yes", "no"):
                        dependencies.append(self.resolve("entity", value, visiting))
                elif family == "entity" and kind.lower() == "state" and key == "animation":
                    state_animations.add(value)
                elif family in ("entity", "particle", "particle_proxy") and key in ("particle", "type") and (key == "particle" or family == "particle_proxy"):
                    target = "particle_proxy" if value in self.definitions["particle_proxy"] and family != "particle_proxy" else "particle"
                    dependencies.append(self.resolve(target, value, visiting))
                elif family in ("entity", "particle") and key == "soundeffect":
                    dependencies.append(self.resolve("audio", value, visiting))
                elif family == "mesh" and kind.lower() == "animation" and key == "type":
                    dependencies.append(self.resolve("animation", value, visiting))
                elif family == "mesh" and kind.lower() == "animation" and key == "id":
                    animation_ids.add(value)
                elif family == "audio" and key in ("sound", "sounds"):
                    dependencies.append(self.resolve("sound", value, visiting))
                elif family == "mio" and key == "include":
                    dependencies.append(self.resolve("mio", value, visiting))
                elif family == "mio" and key == "icon":
                    candidates = [value] if value.startswith("GFX_") else ["GFX_" + value, "GFX_mio_" + value]
                    sprite = next((v for v in candidates if v in self.definitions["sprite"]), candidates[0])
                    dependencies.append(self.resolve("sprite", sprite, visiting))
                elif key not in ("name", "id", "text", "tooltip", "description") and Path(value).suffix.lower() in MEDIA_SUFFIXES:
                    # Unknown literal media bindings stay in the dependency
                    # graph instead of being hidden by a closed key allowlist.
                    resources.append(self.vfs.resource(value, definition["source"], usage="program" if key == "effect" else None))
        for kind, material in walk(node):
            if family == "mesh" and kind.lower() == "meshsettings":
                textures = [dict(binding=key, resource=self.vfs.resource(value, definition["source"], usage="image"))
                            for key, value in fields(material) if key in ("texture_diffuse", "texture_normal", "texture_specular")]
                materials.append(dict(name=scalar(get(material,"name","<unnamed mesh setting>")), textures=textures))
        # Attachment animations belong to the attached entity, not its parent.
        # Clone + explicit mesh override binding semantics are not certified by
        # this reader, so do not turn a union of their labels into closure.
        if family == "entity" and get(node, "clone") and get(node, "pdxmesh"):
            dependencies.append(dict(family="animation_binding", name="clone_mesh_override", status="runtime_binding_uninspected",
                                     classification="unresolved", resources=[],
                                     reason="Entity overrides a cloned mesh; effective inherited state/animation replacement needs native binding inspection"))
        for name in sorted(state_animations - animation_ids):
            dependencies.append(dict(family="animation_binding", name=name, status="runtime_binding_uninspected",
                                     classification="unresolved", resources=[],
                                     reason="Entity state label has no resolved inherited mesh animation ID; embedded native bindings are uninspected"))
        issues = {r["status"] for r in resources if r["status"] in ("missing_asset", "engine_asset", "ambiguous_asset", "unsupported_resource_kind")}
        issues.update(d["status"] for d in dependencies if d["status"] not in ("mod_resolved", "engine_service"))
        if conflicts:
            status = "conflicting_definitions"
        elif "ambiguous_asset" in issues or "ambiguous_provider" in issues:
            status = "ambiguous_provider"
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
                      definition_origin=definition["origin"], definition_provider=definition["provider"],
                      definition_source=definition["provider_source"], resources=resources)
        if dependencies:
            result["dependencies"] = dependencies
        if animation_ids:
            result["declared_animation_ids"] = sorted(animation_ids)
        if materials:
            result["declared_materials"] = materials
        classes = [r.get("classification","unresolved") for r in resources] + [d.get("classification","unresolved") for d in dependencies]
        if (conflicts or not classes or any(c == "unresolved" for c in classes)
                or any(r.get("binary_material_dependencies") for r in resources)
                or status in ("dependency_cycle", "missing_asset_or_dependency", "runtime_binding_uninspected", "ambiguous_provider")):
            result["classification"] = "unresolved"
        else:
            result["classification"] = "approved_sourced" if "approved_sourced" in classes else "authored" if "authored" in classes else "technical"
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
                    elif key not in ("name", "id", "text", "tooltip", "description") and Path(value).suffix.lower() in MEDIA_SUFFIXES:
                        usage = "program" if key in ("effectfile", "effect") else "image" if "texture" in key or key in ("normal", "specular", "diffuse", "mask") else None
                        resource = self.vfs.resource(value, source, usage=usage)
                        rows.append(dict(family="file", name=value, consumer=source, owner=owner, consumer_family="screen_literal",
                                         status="mod_resolved" if resource["status"] == "mod_asset" else resource["status"],
                                         classification="unresolved" if resource.get("binary_material_dependencies") else resource["classification"], resources=[resource]))
                    elif key in ("verticalscrollbar", "horizontalscrollbar", "scrollbartype"):
                        if value in seen:
                            continue
                        seen.add(value)
                        definition, conflict = self.definition("template", value)
                        if definition is None:
                            rows.append(dict(family="template", name=value, status="missing_definition", consumer=source, owner=owner))
                        else:
                            templates.append(dict(name=value, source=definition["source"], conflicts=conflict))
                            if conflict:
                                rows.append(dict(family="template",name=value,status="conflicting_definitions",classification="unresolved",consumer=source,owner=owner))
                            queue.append((definition["source"], [[definition["kind"], "=", definition["node"]]]))
        if runtime_decisions:
            rows.extend(self.decision_consumers(self._complete))
        # Audio and the nation's runtime-selected flag are separate inventories;
        # this gate certifies texture/font/template resolution, not provenance,
        # actual visibility, screen position, sound replacement or native input.
        failures = sorted({r["family"] + ":" + r["name"] + ":" + r["status"] for r in rows
                           if r["status"] != "mod_resolved"})
        failures.extend("template:" + t["name"] + ":conflicting_definitions" for t in templates if t["conflicts"])
        if rel in self.vfs.providers.ambiguities:
            failures.append("screen:ambiguous_provider")
        failures.extend("provider:"+problem for problem in self.vfs.providers.errors)
        failures.extend("parse:" + row["source"] for row in self.parse_failures
                        if row["source"] == rel or runtime_decisions and row["source"].startswith("common/decisions/"))
        self.rows.extend(rows)
        return dict(source=rel, origin=origin, coverage="effective GUI textures/fonts/scrollbar templates and authored decision icons; not native rendering",
                    templates=templates, consumers=rows, failures=failures)

    def decision_consumers(self, include_fallback=False):
        rows = []
        for rel, origin, path in self.vfs.files("common/decisions", {".txt"}):
            if origin != "mod" and not include_fallback:
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
                                                        classification="unreachable", consumer_family="decision_category" if category else "decision",
                                                        icon=scalar(get(node, "icon", "<engine default>"))))
                    continue
                icons = [value for key, _, value in node if key.lower() == 'icon']
                prefixes = ("GFX_decision_category_", "GFX_decision_") if category else ("GFX_decision_",)
                fallback = "GFX_decision_category_generic" if category else "GFX_decision_unknown"
                conditional = False; found = False; unconditional = False
                for value in icons:
                    value = scalar(value)
                    if isinstance(value, str) and value:
                        rows.append(self.icon(value, rel, name, "decision_category" if category else "decision", prefixes))
                        found = True; unconditional = True
                    elif isinstance(value, list):
                        conditional = True
                        # Repeated icon blocks use unprefixed `key` values.
                        # Their trigger does not exempt a branch from coverage.
                        for key, candidate in fields(value):
                            if key in ("key", "icon", "value"):
                                rows.append(self.icon(candidate, rel, name, "conditional_decision_icon", prefixes))
                                found = True
                # Logical trigger exhaustiveness is not established offline.
                # Include the runtime default for conditional-only declarations,
                # or an empty/malformed declaration with no usable candidate.
                if not found or conditional and not unconditional:
                    rows.append(self.icon(fallback, rel, name, "conditional_decision_default" if conditional else "decision_default"))
                picture = scalar(get(node, "picture", ""))
                if isinstance(picture, str) and picture:
                    rows.append(self.icon(picture, rel, name, "decision_picture", ("GFX_",)))
        return rows

    def scripted_bindings(self, include_fallback=False):
        windows = defaultdict(list)
        for rel, origin, path in self.vfs.files("interface", {".gui"}):
            for kind, node in walk(self.read(rel, origin, path)):
                if kind.lower() == "containerwindowtype" and get(node, "name"):
                    windows[scalar(get(node, "name"))].append((rel, node))
        rows = []
        for rel, origin, path in self.vfs.files("common/scripted_guis", {".txt"}, authored_only=not include_fallback):
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

    def runtime(self, include_fallback=False):
        # These are actual authored consumers. We do not assert that every
        # branch is reachable in a played campaign or every DLC is active.
        for prefix, family in (("common/characters", "portrait"),
                               ("common/military_industrial_organization/organizations", "mio"),
                               ("common/intelligence_agencies", "agency")):
            for rel, origin, path in self.vfs.files(prefix, {".txt"}, authored_only=not include_fallback):
                tree = self.read(rel, origin, path)
                for kind, node in walk(tree):
                    for key, value in fields(node):
                        if family == "portrait" and key in ("large", "small"):
                            if value.startswith("GFX_"):
                                self.icon(value, rel, kind, family)
                            else:
                                resource = self.vfs.resource(value, rel, usage="image")
                                self.rows.append(dict(consumer_family=family, consumer=rel, owner=kind, family="file", name=value,
                                                      status=resource["status"], classification=resource["classification"], resources=[resource]))
                        elif family in ("mio", "agency") and key in ("icon", "picture", "portrait"):
                            self.icon(value, rel, kind, family, ("GFX_", "GFX_mio_", "GFX_intelligence_agency_"))
        # Random generals/operatives/scientists are selected from bare sprite
        # tokens in portrait pools, not only explicit character large/small keys.
        # Country/continent eligibility is deliberately not assumed here.
        for rel, origin, path in self.vfs.files("portraits", {".txt"}, authored_only=not include_fallback):
            tree = self.read(rel, origin, path)
            for kind, node in [("portrait_pool", tree)] + list(walk(tree)):
                for key, op, value in node:
                    token = scalar(key)
                    if op is None and token.startswith("GFX_"):
                        self.icon(token, rel, kind, "portrait_pool")
        for name, definitions in sorted(self.definitions["mio"].items()):
            if any(d["origin"] == "mod" for d in definitions) or include_fallback:
                d, _ = self.definition("mio", name)
                self.row("mio", name, d["source"], name, "mio_inheritance")
        for name, definitions in sorted(self.definitions["presentation_object"].items()):
            if include_fallback or any(d["origin"] == "mod" for d in definitions):
                definition, _ = self.definition("presentation_object", name)
                self.row("presentation_object", name, definition["source"], name, "presentation_object")
        # Content-selected focus, continuous-focus and event pictures do not
        # appear as literal GUI sprites. Ideas use the engine's GFX_idea_ prefix.
        for prefix, family in (("common/national_focus", "focus"), ("common/continuous_focus", "continuous_focus"),
                               ("common/ideas", "idea"), ("events", "event_picture"), ("common/technologies", "technology")):
            for rel, origin, path in self.vfs.files(prefix, {".txt"}, authored_only=not include_fallback):
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
        for family in ("entity", "mesh", "animation", "particle", "particle_proxy", "audio", "sound", "music"):
            for name, definitions in sorted(self.definitions[family].items()):
                if any(d["origin"] == "mod" or d["provider"].startswith("dlc:") for d in definitions) or include_fallback:
                    d, _ = self.definition(family, name)
                    self.row(family, name, d["source"], name, "model" if family in ("entity", "mesh", "animation", "particle", "particle_proxy") else "audio")
        # Runtime culture/model selection is generated by engine conventions.
        # Log named unit sprite consumers and mark unexpanded convention roots.
        for rel, origin, path in self.vfs.files("common/units", {".txt"}, authored_only=not include_fallback):
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
            for rel, origin, path in self.vfs.files(prefix, suffixes, authored_only=not include_fallback):
                for kind, node in walk(self.read(rel, origin, path)):
                    for key, value in fields(node):
                        if key in ("clicksound", "show_sound", "hide_sound", "play_sound", "soundeffect") and value:
                            self.row("audio", value, rel, scalar(get(node, "name", kind)), "audio_consumer")

    def music_consumers(self):
        for rel, origin, path in self.vfs.files("music", {".txt"}):
            for kind, node in walk(self.read(rel, origin, path)):
                for key, value in fields(node):
                    if key == "song":
                        self.row("music", value, rel, kind, "music_playlist")

    def run(self, screens, complete=False):
        screens = list(screens)
        self._complete = complete
        if complete:
            screens = list(dict.fromkeys(screens + [rel.removeprefix("interface/") for rel, _, _ in self.vfs.files("interface", {".gui"})]))
        covered = {filename: self.screen(filename, filename.lower() == "countrydecisionview.gui") for filename in screens}
        self.runtime(complete)
        self.music_consumers()
        unique = {json.dumps(row, sort_keys=True): row for row in self.rows}
        rows = sorted(unique.values(), key=lambda r: (r.get("consumer_family", ""), r["consumer"], r["name"]))
        counts = Counter(row["status"] for row in rows)
        by_family = defaultdict(Counter)
        for row in rows:
            by_family[row.get("consumer_family", row["family"])][row["status"]] += 1
        for row in rows:
            if row["consumer"] in self.vfs._files:
                asset=self.vfs._files[row["consumer"]][1]
                row.setdefault("consumer_provider",asset.provider);row.setdefault("consumer_source",asset.source)
            row.setdefault("classification", "unresolved")
            row.setdefault("reachability", "conservative_potential; actual campaign visibility not certified")
        classifications = Counter(row["classification"] for row in rows)
        classifications["unreachable"] += len(self.retired_consumers)
        gate_failures = []
        if complete:
            if self.vfs.providers.profile is None:
                gate_failures.append("DLC activation profile is unspecified; pass an explicit selection, including an empty selection when intended")
            gate_failures += self.vfs.providers.errors
            gate_failures += ["provider_ambiguity:"+path for path in self.vfs.providers.ambiguities]
            gate_failures += ["screen:"+name+":"+failure for name,screen in covered.items() for failure in screen["failures"]
                              if failure == "missing screen" or failure.startswith(("template:","parse:","screen:","provider:"))]
            gate_failures += [row["consumer"]+":"+row["family"]+":"+row["name"]+":"+row["status"]
                              for row in rows if row.get("classification","unresolved") == "unresolved"]
            gate_failures += ["parse:"+row["source"] for row in self.parse_failures]
            gate_failures += ["binding:"+row["source"]+":"+row["scripted_gui"] for row in self.scripted_bindings(True) if row["problems"]]
        return dict(schema=2, coverage="Profile-scoped effective source dependency inventory; classifications require exact provenance and do not establish native reachability or copyright permission",
                    engine_version="read installed launcher-settings/version separately; no runtime version inferred",
                    dlc_archive_coverage=self.vfs.providers.report(),
                    classification_summary={kind: classifications[kind] for kind in ("authored", "approved_sourced", "technical", "unreachable", "unresolved")},
                    completed_presentation_gate=dict(requested=complete, passed=complete and not gate_failures,
                                                     failures=sorted(set(gate_failures)),
                                                     scope="All effective GUI files, conservative engine/DLC/mod runtime consumers and literal music playlists; unknown conventions/binary material bindings remain unresolved"),
                    replace_paths=self.vfs.replace_paths, gate_covered_screens=covered,
                    summary=dict(counts), by_consumer_family={k: dict(v) for k, v in sorted(by_family.items())},
                    parse_failures=self.parse_failures,
                    scripted_gui_bindings=self.scripted_bindings(complete),
                    statically_retired_consumers=self.retired_consumers,
                    coverage_limits=["Engine-generated entity/culture combinations are logged but not fully expanded.",
                                     "Literal portrait-pool choices are conservative roots; native eligibility and random selection are not certified.",
                                     "Runtime-selected country flags and native DLC membership need native checks.",
                                     "MIO/agency conditional branches are inspected; their gameplay reachability is not certified.",
                                     "Mod-local paths do not prove originality, copyright permission, or absence of copied vanilla pixels.",
                                     "Legacy screen gates retain their original ownership scope; --gate-presentation additionally fails unresolved presentation across the conservative effective roots."],
                    consumers=rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("engine", type=Path)
    p.add_argument("--mod-root", type=Path, default=DEFAULT_MOD)
    p.add_argument("--screen", action="append", default=[])
    p.add_argument("--gate-decisions", action="store_true")
    p.add_argument("--gate-screen", action="append", default=[], help="Gate another effective profile-scoped screen by filename using the legacy mod-ownership requirement")
    p.add_argument("--profile", type=Path, help="Explicit schema1 DLC/provenance audit scenario; never inferred from installed packs")
    p.add_argument("--gate-presentation", action="store_true", help="Fail any unresolved conservative presentation root; requires an explicit DLC profile")
    p.add_argument("--summary-only", action="store_true", help="Retain counts/failures/provider evidence while omitting the bulky consumer graph")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    screens = list(dict.fromkeys(["countrydecisionview.gui"] + args.screen + args.gate_screen))
    profile = json.loads(args.profile.read_text(encoding="utf-8-sig")) if args.profile else None
    report = Audit(args.mod_root, args.engine, profile).run(screens, args.gate_presentation)
    if args.summary_only:
        report.pop("consumers", None)
        for screen in report["gate_covered_screens"].values():
            screen["consumer_count"] = len(screen["consumers"]); screen.pop("consumers")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(summary=report["summary"], classification_summary=report["classification_summary"],
                          completed_presentation_gate=dict(requested=args.gate_presentation,passed=report["completed_presentation_gate"]["passed"],
                                                           failure_count=len(report["completed_presentation_gate"]["failures"])),
                          dlc_profile_status=report["dlc_archive_coverage"]["status"], by_consumer_family=report["by_consumer_family"],
                          screen_failures={k: len(v["failures"]) if args.summary_only else v["failures"] for k, v in report["gate_covered_screens"].items()},
                          parse_failures=len(report["parse_failures"])), indent=2))
    gates = (["countrydecisionview.gui"] if args.gate_decisions else []) + args.gate_screen
    if any(report["gate_covered_screens"][name]["failures"] for name in gates) or args.gate_presentation and not report["completed_presentation_gate"]["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
