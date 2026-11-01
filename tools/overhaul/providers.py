"""Read-only engine/DLC/mod providers for the presentation dependency audit.

Descriptors say where a pack is mounted, not whether this user owns/enabled it
or how cross-pack conflicts are ordered. Only an explicit audit profile mounts
DLC. Different same-path fallback bytes remain ambiguous without a hash-pinned
per-path choice. No archive member is ever extracted or executed.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile
from text_structure import validate_structure

ROOTS = {"interface", "common", "gfx", "sound", "music", "events", "history", "portraits"}
MAX_TEXT_BYTES = 8 * 1024 * 1024
DEFINITION_SUFFIXES = {".gfx", ".gui", ".asset", ".txt", ".dlc"}


def normal(value):
    return re.sub(r"/+", "/", str(value).replace("\\", "/")).strip("/").lower()


def safe_member(value):
    path = str(value).replace("\\", "/")
    parts = PurePosixPath(path).parts
    return bool(parts) and not path.startswith("/") and not re.match(r"^[a-zA-Z]:", path) and ".." not in parts


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


@dataclass
class Asset:
    relative: str
    provider: str
    origin: str
    source: str
    path: Path
    member: str | None = None
    bytes: int = 0
    _hash: str | None = None

    @property
    def suffix(self):
        return PurePosixPath(self.relative).suffix

    def read_bytes(self):
        if self.member is None:
            return self.path.read_bytes()
        with zipfile.ZipFile(self.path) as archive:
            return archive.read(self.member)

    def read_text(self, encoding="utf-8-sig", errors="replace"):
        if self.bytes > MAX_TEXT_BYTES:
            raise ValueError("Definition exceeds the bounded text-reader limit")
        return self.read_bytes().decode(encoding, errors=errors)

    def sha256(self):
        if self.suffix.lower() in DEFINITION_SUFFIXES and self.bytes > MAX_TEXT_BYTES:
            raise ValueError("Definition exceeds the bounded text-reader limit; not hashed or decompressed")
        if self._hash is None:
            if self.member is None:
                self._hash = digest(self.path)
            else:
                value = hashlib.sha256()
                with zipfile.ZipFile(self.path) as archive, archive.open(self.member) as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        value.update(chunk)
                self._hash = value.hexdigest()
        return self._hash

    def metadata(self):
        return dict(provider=self.provider, source=self.source, bytes=self.bytes, sha256=self._hash)


class Providers:
    def __init__(self, mod, engine, parser, profile=None):
        self.mod, self.engine = Path(mod).resolve(), Path(engine).resolve()
        self.profile = profile
        self.errors = []
        self.inventory = []
        self.candidates = {}
        self.ambiguities = {}
        self.overrides = {}
        self.payload_overrides = {}
        self.approvals = {}
        self.replace_paths = []
        descriptor = self.mod / "descriptor.mod"
        if descriptor.exists():
            declaration = descriptor.read_text(encoding="utf-8-sig")
            validate_structure(declaration)
            self.replace_paths = [normal(v.strip('"')) for k, _, v in parser(declaration)
                                  if k == "replace_path" and isinstance(v, str)]
        selected = set()
        if profile is not None:
            if not isinstance(profile, dict) or profile.get("schema") != 1 or not isinstance(profile.get("enabled_dlc"), list):
                raise ValueError("Profile needs schema1 and an explicit enabled_dlc list (which may be empty)")
            if not all(isinstance(p,str) for p in profile["enabled_dlc"]):
                raise ValueError("DLC selections must be exact descriptor path strings")
            selected = {normal(p.removeprefix("engine://")) for p in profile["enabled_dlc"]}
            if len(selected) != len(profile["enabled_dlc"]):
                raise ValueError("Duplicate DLC selection")
            for row in profile.get("provider_overrides", []):
                path = self.record(row, "provider override")
                if path in self.overrides:
                    raise ValueError("Duplicate provider override: " + path)
                self.overrides[path] = row
            for row in profile.get("payload_overrides", []):
                descriptor_path = self.record(row, "descriptor payload mapping")
                payload = row.get("payload")
                if not isinstance(payload, str) or not safe_member(payload) or any(c in payload for c in "*?["):
                    raise ValueError("A descriptor payload mapping needs one safe exact installed payload path")
                if row["provider"] != "dlc:" + descriptor_path:
                    raise ValueError("A descriptor payload mapping must bind its exact descriptor provider")
                if descriptor_path in self.payload_overrides:
                    raise ValueError("Duplicate descriptor payload mapping: " + descriptor_path)
                self.payload_overrides[descriptor_path] = row
            for row in profile.get("provenance", []):
                path = self.record(row, "provenance")
                if row.get("classification") not in ("authored", "approved_sourced"):
                    raise ValueError("Only exact authored/approved_sourced provenance records are accepted")
                key = (path, row["provider"])
                if key in self.approvals:
                    raise ValueError("Duplicate provenance: " + path)
                self.approvals[key] = row
        self.directory(self.engine, "engine", "engine", "engine://")
        described = set()
        descriptors = [path for folder in ("dlc", "integrated_dlc") for path in (self.engine / folder).rglob("*.dlc")]
        for path in sorted(descriptors):
            relative = path.relative_to(self.engine).as_posix()
            ident = normal(relative); described.add(ident)
            row = dict(descriptor="engine://" + relative, descriptor_sha256=None, selected=ident in selected)
            try:
                if path.stat().st_size > MAX_TEXT_BYTES:
                    raise ValueError("Descriptor exceeds the bounded text-reader limit")
                row["descriptor_sha256"] = digest(path)
                declaration = path.read_text(encoding="utf-8-sig")
                validate_structure(declaration)
                fields = {k: v.strip('"') for k, _, v in parser(declaration) if isinstance(v, str)}
                row.update(name=fields.get("name", ""), steam_id=fields.get("steam_id"),
                           payload_kind="archive" if "archive" in fields else "directory" if "path" in fields else "unresolved")
                location = fields.get("archive", fields.get("path"))
                if not location or not safe_member(location):
                    raise ValueError("Missing or unsafe descriptor payload path")
                row["declared_payload"] = "engine://" + location.replace("\\", "/")
                mapping = self.payload_overrides.get(ident)
                if mapping:
                    if mapping["sha256"] != row["descriptor_sha256"]:
                        raise ValueError("Descriptor payload mapping hash changed")
                    location = mapping["payload"]
                    row["payload_mapping"] = dict(reason=mapping["reason"], evidence=mapping["evidence"],
                                                  status="explicit_audit_mapping_not_native_mount_proof")
                payload = (self.engine / location).resolve()
                if not payload.is_relative_to(self.engine):
                    raise ValueError("Descriptor payload escapes the installed reference")
                row["payload"] = "engine://" + payload.relative_to(self.engine).as_posix()
                provider = "dlc:" + ident
                if row["payload_kind"] == "archive":
                    row.update(payload_bytes=payload.stat().st_size, payload_sha256=digest(payload))
                    with zipfile.ZipFile(payload) as archive:
                        entries = archive.infolist()
                        row["member_count"] = sum(not item.is_dir() for item in entries)
                        member_names = Counter(normal(item.filename) for item in entries if not item.is_dir())
                        row["duplicate_members"] = sorted(name for name, count in member_names.items() if count > 1)
                        if row["duplicate_members"]:
                            # ZipFile's name lookup picks the last entry. Reject
                            # the provider before mounting so candidate hashes,
                            # bounds and bytes cannot refer to different entries.
                            raise ValueError("Duplicate normalized archive member names are not mounted")
                        row["unsafe_members"] = [item.filename for item in entries if not safe_member(item.filename)
                                                 or stat.S_ISLNK(item.external_attr >> 16)]
                        if row["unsafe_members"]:
                            raise ValueError("Unsafe archive members are not mounted")
                        if any(item.flag_bits & 1 for item in entries):
                            raise ValueError("Encrypted archive members are not inspected")
                        if row["selected"]:
                            for item in entries:
                                if item.is_dir() or normal(item.filename).split("/", 1)[0] not in ROOTS:
                                    continue
                                rel = normal(item.filename)
                                asset = Asset(rel, provider, "engine", row["payload"] + "!/" + item.filename,
                                              payload, item.filename, item.file_size)
                                self.add(asset)
                else:
                    if not payload.is_dir():
                        raise ValueError("Missing descriptor directory")
                    row["member_count"] = sum(p.is_file() for p in payload.rglob("*"))
                    if row["selected"]:
                        self.directory(payload, provider, "engine", row["payload"] + "/")
                row["inspection"] = "mounted_by_explicit_audit_profile" if row["selected"] else "inventory_only_not_enabled"
            except (ValueError, IndexError, OSError, zipfile.BadZipFile) as exc:
                row.update(inspection="unresolved_provider", error=str(exc).replace(str(self.engine), "engine://"))
                if row["selected"]:
                    self.errors.append("Selected provider cannot be inspected: " + relative)
            self.inventory.append(row)
        for missing in sorted(selected - described):
            self.errors.append("Selected descriptor is not installed: " + missing)
        for unused in sorted(self.payload_overrides.keys() - selected):
            self.errors.append("Descriptor payload mapping does not belong to an explicitly selected provider: " + unused)
        repo = Path(__file__).resolve().parents[2]
        prefix = self.mod.relative_to(repo).as_posix() + "/" if self.mod.is_relative_to(repo) else "mod://"
        self.directory(self.mod, "mod", "mod", prefix)
        self.files = {}
        for rel, assets in self.candidates.items():
            local = [a for a in assets if a.origin == "mod"]
            candidates = local or assets
            choice = self.overrides.get(rel)
            winner = candidates[-1]
            try:
                differing = len(candidates) > 1 and len({a.sha256() for a in candidates}) > 1
            except (ValueError, OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError):
                self.errors.append("Provider collision cannot be read: " + rel)
                differing = True
            if differing:
                self.ambiguities[rel] = [a.metadata() for a in candidates]
                # Winner is explanatory only; ambiguity fails resolution.
            if choice:
                try:
                    matching = [a for a in candidates if a.provider == choice["provider"] and a.sha256() == choice["sha256"]]
                except (ValueError, OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError):
                    matching = []
                if len(matching) == 1:
                    winner = matching[0]; self.ambiguities.pop(rel, None)
                else:
                    self.errors.append("Provider override is unavailable or its hash changed: " + rel)
                    self.ambiguities[rel] = [a.metadata() for a in candidates]
            self.files[rel] = (winner.origin, winner)
        for unused in sorted(self.overrides.keys() - self.candidates.keys()):
            self.errors.append("Provider override has no effective path: " + unused)

    @staticmethod
    def record(row, kind):
        if not isinstance(row,dict):
            raise ValueError("A "+kind+" must be a structured exact-resource record")
        path = row.get("path", "")
        if not isinstance(path,str) or not safe_member(path) or any(c in path for c in "*?["):
            raise ValueError("A " + kind + " must name one safe exact resource path")
        if (any(not isinstance(row.get(key),str) or not row[key].strip() for key in ("provider","reason","evidence"))
                or not isinstance(row.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"])):
            raise ValueError("A " + kind + " needs a provider, SHA256, reason and evidence")
        return normal(path)

    def directory(self, base, provider, origin, source_prefix):
        for folder in ROOTS:
            for path in (base / folder).rglob("*"):
                if not path.is_file():
                    continue
                if not path.resolve().is_relative_to(base.resolve()):
                    self.errors.append("Provider symlink escapes its declared root: " + provider)
                    continue
                rel = normal(path.relative_to(base).as_posix())
                self.add(Asset(rel, provider, origin, source_prefix + path.relative_to(base).as_posix(),
                               path, bytes=path.stat().st_size))

    def add(self, asset):
        if asset.origin != "mod" and any(asset.relative == p or asset.relative.startswith(p + "/") for p in self.replace_paths):
            return
        self.candidates.setdefault(asset.relative, []).append(asset)

    def classify(self, asset, usage=None):
        if usage == "program" and asset.suffix.lower() in (".lua", ".fx", ".shader", ".fxh"):
            return "technical", "Executable shader/program service; not a texture or audio family exemption"
        approval = self.approvals.get((asset.relative, asset.provider))
        try:
            matches = approval and asset.sha256() == approval["sha256"]
        except (ValueError, OSError, RuntimeError, zipfile.BadZipFile, NotImplementedError):
            return "unresolved", "Hash-pinned resource cannot be read"
        if matches:
            if approval["classification"] == "authored" and asset.origin != "mod":
                return "unresolved", "An authored record cannot relabel installed engine/DLC content"
            return approval["classification"], approval["evidence"]
        return "unresolved", "No matching hash-pinned authored/approved-source record"

    def report(self):
        return dict(status="explicit_profile_inspected" if self.profile is not None else "activation_unspecified_inventory_only",
                    profile_name=self.profile.get("name", "unnamed audit scenario") if self.profile is not None else None,
                    selected_descriptors=sorted(normal(p.removeprefix("engine://")) for p in self.profile["enabled_dlc"]) if self.profile is not None else [],
                    profile_sha256=hashlib.sha256(json.dumps(self.profile,sort_keys=True).encode()).hexdigest() if self.profile is not None else None,
                    provenance_record_count=len(self.approvals), provider_choice_count=len(self.overrides),
                    explicit_payload_mapping_count=len(self.payload_overrides),
                    activation="An explicit static audit scenario is not proof of ownership, activation or native load order",
                    precedence="Mod same-path overrides and descriptor isolation; differing fallback collisions require exact hash-pinned choices",
                    native_cross_dlc_precedence="unverified; lexical/explanatory selection is never accepted as proof",
                    descriptors=self.inventory, provider_errors=self.errors, ambiguous_paths=self.ambiguities)
