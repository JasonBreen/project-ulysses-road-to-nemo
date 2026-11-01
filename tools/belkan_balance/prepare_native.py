"""Prepare and audit an isolated Project Ulysses native-playtest root.

This helper never launches or terminates HOI4, never edits the installed engine
or normal profile, and refuses to overwrite an existing native root. It copies
the engine and exact committed mod payload, creates a disposable profile, and
writes the provenance contract consumed by ``native_checkpoint.py``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "mod" / "2985041246"
HEX_40_RE = re.compile(r"[0-9a-fA-F]{40}\Z")
LABEL_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}\Z")


class PreparationError(ValueError):
    """Raised when isolation or provenance cannot be proved statically."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def under(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def validate_roots(target: Path, game: Path, normal: Path, source: Path) -> None:
    if not target.name.startswith("Project-Ulysses-Native-"):
        raise PreparationError("Target directory name must start with Project-Ulysses-Native-.")
    if target.exists():
        raise PreparationError("Refusing to overwrite an existing native session.")
    if not target.parent.is_dir():
        raise PreparationError("Target parent directory does not exist.")
    for label, path in (("installed game", game), ("normal profile", normal), ("source payload", source)):
        if not path.is_dir():
            raise PreparationError(f"Missing {label}: {path}")
    resolved_target = target.resolve()
    for label, protected in (("installed game", game), ("normal profile", normal), ("source payload", source), ("repository", ROOT)):
        if under(resolved_target, protected) or under(protected, resolved_target):
            raise PreparationError(f"Native target overlaps the {label}: {resolved_target}")
    for required in ("descriptor.mod", "common", "history", "map", "localisation"):
        if not (source / required).exists():
            raise PreparationError(f"Source payload is incomplete; missing {required}.")
    if not (game / "hoi4.exe").is_file() or not (game / "launcher-settings.json").is_file():
        raise PreparationError("Installed game is missing hoi4.exe or launcher-settings.json.")
    if not (normal / "settings.txt").is_file():
        raise PreparationError("Normal profile is missing settings.txt.")


def protected_files(normal: Path) -> list[Path]:
    files = [path for path in normal.iterdir() if path.is_file()]
    for dirname in ("logs", "save games"):
        directory = normal / dirname
        if directory.is_dir():
            files.extend(path for path in directory.rglob("*") if path.is_file())
    return sorted(set(files), key=lambda item: item.relative_to(normal).as_posix().lower())


def protected_manifest(normal: Path) -> dict[str, dict[str, Any]]:
    return {
        path.relative_to(normal).as_posix(): {"size": path.stat().st_size, "sha256": sha256(path)}
        for path in protected_files(normal)
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def snapshot_normal(target: Path, normal: Path, label: str) -> Path:
    if not LABEL_RE.fullmatch(label):
        raise PreparationError("Snapshot label must use letters, digits, dot, underscore, or hyphen.")
    if not target.is_dir() or not (target / "native-provenance.json").is_file():
        raise PreparationError("Target is not a prepared Belkan native root.")
    path = target / "evidence" / f"normal-{label}-before.json"
    if path.exists():
        raise PreparationError(f"Refusing to overwrite an existing normal-profile snapshot: {path.name}")
    write_json(path, {"schema_version": 1, "label": label, "files": protected_manifest(normal)})
    return path


def verify_normal(target: Path, normal: Path, label: str) -> dict[str, Any]:
    if not LABEL_RE.fullmatch(label):
        raise PreparationError("Snapshot label must use letters, digits, dot, underscore, or hyphen.")
    before_path = target / "evidence" / f"normal-{label}-before.json"
    if not before_path.is_file():
        raise PreparationError(f"Missing before snapshot for label {label}.")
    before = json.loads(before_path.read_text(encoding="utf-8"))["files"]
    after = protected_manifest(normal)
    changed = sorted(path for path in before.keys() & after.keys() if before[path] != after[path])
    added = sorted(after.keys() - before.keys())
    removed = sorted(before.keys() - after.keys())
    report = {
        "schema_version": 1,
        "label": label,
        "clean": not (changed or added or removed),
        "before_count": len(before),
        "after_count": len(after),
        "changed": changed,
        "added": added,
        "removed": removed,
        "action": "No restoration attempted; report any unrelated activity separately.",
    }
    write_json(target / "evidence" / f"normal-{label}-verification.json", report)
    return report


def source_commit(source_commit_arg: str | None) -> str:
    if source_commit_arg:
        commit = source_commit_arg.strip()
    else:
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout
        if status.strip():
            raise PreparationError("Repository must be clean before creating an exact native payload.")
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip()
    if not HEX_40_RE.fullmatch(commit):
        raise PreparationError("Source commit must be a full 40-character Git SHA.")
    return commit.lower()


def payload_manifest(source: Path) -> dict[str, str]:
    return {
        path.relative_to(source).as_posix(): sha256(path)
        for path in sorted(source.rglob("*"), key=lambda item: item.as_posix().lower())
        if path.is_file()
    }


def parse_build_id(app_manifest: Path) -> str:
    if not app_manifest.is_file():
        raise PreparationError(f"Steam app manifest is missing: {app_manifest}")
    match = re.search(r'"buildid"\s+"(\d+)"', app_manifest.read_text(encoding="utf-8-sig"))
    if match is None:
        raise PreparationError("Steam app manifest does not contain a buildid.")
    return match.group(1)


def disposable_settings(source: str, width: int, height: int) -> str:
    settings = re.sub(
        r"(?m)^([ \t]*)size=\{\r?\n[ \t]*x=\d+\r?\n[ \t]*y=\d+[ \t]*\}",
        lambda match: (
            f"{match.group(1)}size={{\n"
            f"{match.group(1)}\tx={width}\n"
            f"{match.group(1)}\ty={height} }}"
        ),
        source,
        count=1,
    )
    if settings == source:
        raise PreparationError("Normal settings do not contain a supported graphics size block.")

    def replace_or_append(name: str, value: str) -> None:
        nonlocal settings
        pattern = rf"(?m)^([ \t]*){re.escape(name)}=.*$"
        if re.search(pattern, settings):
            settings = re.sub(
                pattern,
                lambda match: f"{match.group(1)}{name}={value}",
                settings,
                count=1,
            )
        else:
            settings += f"\n{name}={value}"

    replace_or_append("gui_scale", "1.000000")
    replace_or_append("fullScreen", "no")
    replace_or_append("borderless", "yes")
    replace_or_append("autosave", '"MONTHLY"')
    replace_or_append("autosave_tocloud", "no")
    replace_or_append("save_career_to_cloud", "no")
    replace_or_append("save_as_binary", "no")
    for volume in ("master_volume", "music_volume", "sound_fx_volume", "ambient_volume", "voice_volume"):
        replace_or_append(volume, "0.000000")
    replace_or_append("lastplayer", '"BelkanBalance"')
    replace_or_append("lasthost", '"BelkanBalance"')
    return settings.rstrip() + "\n"


def prepare(
    target: Path,
    game: Path,
    normal: Path,
    source: Path,
    app_manifest: Path,
    commit_arg: str | None = None,
    width: int = 3440,
    height: int = 1440,
) -> dict[str, Any]:
    if width <= 0 or height <= 0:
        raise PreparationError("Display width and height must be positive integers.")
    target = target.resolve()
    game = game.resolve()
    normal = normal.resolve()
    source = source.resolve()
    validate_roots(target, game, normal, source)
    if commit_arg is None and source != DEFAULT_SOURCE.resolve():
        raise PreparationError("An exact native preparation must use this worktree's mod payload.")
    commit = source_commit(commit_arg)
    launcher = json.loads((game / "launcher-settings.json").read_text(encoding="utf-8-sig"))
    version = str(launcher.get("version", "")).strip()
    raw_version = str(launcher.get("rawVersion", "")).strip()
    checksum_match = re.search(r"\(([^()]+)\)\s*$", version)
    if not version or not raw_version or checksum_match is None:
        raise PreparationError("Installed launcher settings do not expose version/rawVersion/checksum.")
    build_id = parse_build_id(app_manifest)

    evidence = target / "evidence"
    profile = target / "profile"
    engine = target / "engine"
    payload = profile / "mod" / "project_ulysses_belkan_balance"
    descriptor = profile / "mod" / "project_ulysses_belkan_balance.mod"

    evidence.mkdir(parents=True)
    write_json(evidence / "normal-prepare-before.json", {"schema_version": 1, "label": "prepare", "files": protected_manifest(normal)})
    shutil.copytree(game, engine)
    profile.mkdir()
    (profile / "logs").mkdir()
    (profile / "save games").mkdir()
    (profile / "mod").mkdir()
    # Clausewitz reads this marker as a literal path. A Windows text-mode
    # newline becomes CRLF and causes this engine build to fall back to the
    # normal Documents profile, so write the exact UTF-8 bytes with no suffix.
    (engine / "userdir.txt").write_bytes(profile.as_posix().encode("utf-8"))
    copied_launcher = dict(launcher)
    copied_launcher["gameDataPath"] = profile.as_posix()
    write_json(engine / "launcher-settings.json", copied_launcher)
    (profile / "settings.txt").write_text(
        disposable_settings((normal / "settings.txt").read_text(encoding="utf-8-sig"), width, height),
        encoding="utf-8",
    )
    # Do not carry account- or machine-specific launcher/profile data into the
    # disposable user directory. HOI4 may populate this isolated file itself.
    write_json(profile / "pdx_settings.json", {})

    expected = payload_manifest(source)
    shutil.copytree(source, payload)
    actual = payload_manifest(payload)
    if actual != expected:
        raise PreparationError("Copied payload does not exactly match the candidate source.")
    manifest_path = target / "payload-manifest.json"
    write_json(manifest_path, {"schema_version": 1, "source_commit": commit, "files": expected})

    descriptor_text = (payload / "descriptor.mod").read_text(encoding="utf-8-sig")
    descriptor_text = re.sub(r'(?m)^name\s*=.*$', 'name="Project Ulysses - Belkan Balance Native"', descriptor_text, count=1)
    descriptor_text = re.sub(r'(?m)^path\s*=.*$\n?', "", descriptor_text)
    descriptor_text = descriptor_text.rstrip() + f'\npath="{payload.as_posix()}"\n'
    descriptor.write_text(descriptor_text, encoding="utf-8")
    write_json(profile / "dlc_load.json", {"disabled_dlcs": [], "enabled_mods": ["mod/project_ulysses_belkan_balance.mod"]})

    if sha256(engine / "hoi4.exe") != sha256(game / "hoi4.exe"):
        raise PreparationError("Copied hoi4.exe does not match the installed executable.")
    native = {
        "schema_version": 1,
        "source_commit": commit,
        "payload_manifest": {"file": "payload-manifest.json", "sha256": sha256(manifest_path)},
        "engine": {
            "version": version,
            "raw_version": raw_version,
            "build_id": build_id,
            "checksum": checksum_match.group(1),
            "executable_sha256": sha256(engine / "hoi4.exe"),
        },
        "session_policy": {
            "difficulty": "regular",
            "historical_ai": True,
            "dlc": "all currently owned DLC; no DLC explicitly disabled",
            "display": {"mode": "borderless", "width": width, "height": height},
            "saves": {"format": "text", "autosave": "monthly", "cloud": False},
            "audio_muted": True,
            "natural_runs": "no console, tag switch, resource edits, or outcome intervention",
        },
    }
    write_json(target / "native-provenance.json", native)
    launch = {
        "schema_version": 1,
        "executable": (engine / "hoi4.exe").as_posix(),
        "arguments": ["-gdpr-compliant", f"-userdir={profile.as_posix()}"],
        "profile": profile.as_posix(),
        "descriptor": descriptor.as_posix(),
        "enabled_mod": "mod/project_ulysses_belkan_balance.mod",
        "evidence": "prepared configuration only; not a native launch result",
    }
    write_json(target / "launch.json", launch)

    after = protected_manifest(normal)
    before = json.loads((evidence / "normal-prepare-before.json").read_text(encoding="utf-8"))["files"]
    preparation_report = {
        "schema_version": 1,
        "label": "prepare",
        "clean": before == after,
        "changed": sorted(path for path in before.keys() & after.keys() if before[path] != after[path]),
        "added": sorted(after.keys() - before.keys()),
        "removed": sorted(before.keys() - after.keys()),
        "action": "No restoration attempted; report any unrelated activity separately.",
    }
    write_json(evidence / "normal-prepare-verification.json", preparation_report)
    if not preparation_report["clean"]:
        raise PreparationError("Normal profile changed while the native root was prepared; evidence was retained, but preservation is not clean.")
    return {
        "target": target,
        "profile": profile,
        "engine": engine,
        "payload": payload,
        "descriptor": descriptor,
        "source_commit": commit,
        "payload_files": len(expected),
        "payload_manifest_sha256": native["payload_manifest"]["sha256"],
        "engine_version": version,
        "build_id": build_id,
        "checksum": checksum_match.group(1),
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("--target", type=Path, required=True)
    prepare_parser.add_argument("--game-root", type=Path, required=True)
    prepare_parser.add_argument("--normal-profile", type=Path, required=True)
    prepare_parser.add_argument("--app-manifest", type=Path, required=True)
    prepare_parser.add_argument("--width", type=int, default=3440)
    prepare_parser.add_argument("--height", type=int, default=1440)
    for name in ("snapshot-normal", "verify-normal"):
        command = commands.add_parser(name)
        command.add_argument("--target", type=Path, required=True)
        command.add_argument("--normal-profile", type=Path, required=True)
        command.add_argument("--label", required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare(
                args.target,
                args.game_root,
                args.normal_profile,
                DEFAULT_SOURCE,
                args.app_manifest,
                None,
                args.width,
                args.height,
            )
            printable = {key: str(value) if isinstance(value, Path) else value for key, value in result.items()}
            print(json.dumps(printable, indent=2))
            return 0
        if args.command == "snapshot-normal":
            print(snapshot_normal(args.target.resolve(), args.normal_profile.resolve(), args.label))
            return 0
        report = verify_normal(args.target.resolve(), args.normal_profile.resolve(), args.label)
        print(json.dumps(report, indent=2))
        return 0 if report["clean"] else 1
    except (PreparationError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"native preparation error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
