"""Capture bounded metadata-only evidence for explicit installed-reference scenarios.

No engine/DLC media, shader code or script definitions are copied. Directory
payload aliases for integrated packs are explicit audit mappings, not inferred
native activation. Full reports can be reproduced with audit_consumers.py.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from audit_consumers import Audit, DEFAULT_MOD, ROOT, parse, scalar
from providers import digest


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def compact(report):
    """Keep totals, pinned hashes and explicit samples, never turn FAIL into PASS."""
    report.pop("consumers", None)
    for screen in report["gate_covered_screens"].values():
        screen["consumer_count"] = len(screen.pop("consumers"))
        failures = screen.pop("failures")
        screen.update(failure_count=len(failures), failure_samples=failures[:3])
    gate = report["completed_presentation_gate"]
    failures = gate.pop("failures")
    gate.update(failure_count=len(failures), failure_samples=failures[:40],
                complete_failure_list_sha256=hashlib.sha256(json.dumps(failures, sort_keys=True).encode()).hexdigest(),
                omitted_failure_count=max(0, len(failures) - 40))
    return report


def profiles(engine):
    # Only this already-reviewed, reproducibly authored family is credited.
    # No installed art/audio, inherited mod file or filename family is approved.
    manifest_path = ROOT / "tools/overhaul/decisions_assets.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest["source_layer"] != "original procedural artwork":
        raise ValueError("Unexpected decision asset provenance")
    provenance = []
    for item in manifest["assets"]:
        if digest(DEFAULT_MOD / item["file"]) != item["sha256"]:
            raise ValueError("Authored decision manifest hash changed: " + item["file"])
        provenance.append(dict(path=item["file"], provider="mod", sha256=item["sha256"], classification="authored",
                               reason="Original procedural geometry with retained generator and byte-pinned manifest.",
                               evidence="tools/overhaul/decisions_assets.json; tools/overhaul/build_decisions_ui.py"))
    descriptors = sorted(path.relative_to(engine).as_posix() for folder in ("dlc", "integrated_dlc")
                         for path in (engine / folder).rglob("*.dlc"))
    mappings = []
    for descriptor in descriptors:
        if descriptor.startswith("integrated_dlc/"):
            fields = {key: scalar(value) for key, _, value in parse((engine / descriptor).read_text(encoding="utf-8-sig")) if isinstance(value, str)}
            declared = fields.get("path")
            declared_payload = engine / declared if declared else None
            if not declared or declared_payload.is_file() or declared_payload.is_dir() and any(path.is_file() for path in declared_payload.rglob("*")):
                continue
            mappings.append(dict(path=descriptor, provider="dlc:" + descriptor,
                                 sha256=digest(engine / descriptor), payload=str(Path(descriptor).parent).replace("\\", "/"),
                                 reason="Installed integrated descriptor declares an empty or missing dlc/ payload; this explicit static scenario inspects its actual adjacent installed directory.",
                                 evidence="engine://" + descriptor + "; engine://" + str(Path(descriptor).parent).replace("\\", "/") + "; native mount priority unverified"))
    selected = ["dlc/dlc003_rocket_launcher_unit_pack/dlc003.dlc", "dlc/dlc005_heavy_cruisers_unit_pack/dlc005.dlc",
                "dlc/dlc011_german_march_order_music_pack/dlc011.dlc"]
    def profile(name, enabled, mappings=(), credits=()):
        return dict(schema=1, name=name + " explicit static audit scenario; not a claim of ownership or active DLC",
                    enabled_dlc=enabled, provider_overrides=[], payload_overrides=list(mappings), provenance=list(credits))
    return {"base-only": profile("base-only", []),
            "archives-and-music": profile("archives-and-music", selected, credits=provenance),
            "all-installed": profile("all-installed", descriptors, mappings=mappings, credits=provenance)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("engine", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/evidence/effective-dependencies")
    args = parser.parse_args()
    engine = args.engine.resolve()
    sources = ["tools/overhaul/audit_consumers.py", "tools/overhaul/providers.py",
               "tools/overhaul/text_structure.py", "tools/usea_expansion/script.py",
               "tools/overhaul/capture_dependency_evidence.py", "tools/overhaul/decisions_assets.json"]
    source_hashes = {path: digest(ROOT / path) for path in sources}
    started = datetime.now(timezone.utc).isoformat()
    scenarios = profiles(engine)
    results = []
    for name, profile in scenarios.items():
        write(args.output / "profiles" / (name + ".json"), profile)
        audit = Audit(DEFAULT_MOD, engine, profile)
        complete = name != "base-only"
        report = audit.run(["countrydecisionview.gui"], complete)
        expected_pass = not complete
        actual_pass = not report["gate_covered_screens"]["countrydecisionview.gui"]["failures"] if not complete else report["completed_presentation_gate"]["passed"]
        output = compact(report)
        write(args.output / (name + ".json"), output)
        results.append(dict(scenario=name, gate="legacy_decision_mod_ownership" if not complete else "completed_presentation",
                            actual="PASS" if actual_pass else "FAIL", expected="PASS" if expected_pass else "FAIL",
                            matches_expected=expected_pass == actual_pass,
                            classification_summary=output["classification_summary"],
                            complete_gate_failure_count=output["completed_presentation_gate"]["failure_count"],
                            selected_descriptor_count=len(profile["enabled_dlc"]),
                            parse_failure_count=len(output["parse_failures"])))
        print(json.dumps(results[-1]), flush=True)
        if name == "all-installed":
            version = json.loads((engine / "launcher-settings.json").read_text(encoding="utf-8-sig"))["rawVersion"]
            extensions = Counter()
            for folder in ("dlc", "integrated_dlc"):
                extensions.update(path.suffix.lower() or "<no extension>" for path in (engine / folder).rglob("*") if path.is_file())
            write(args.output / "installed-reference.json",
                  dict(schema=1, evidence_layer="Installed textual descriptor and filesystem metadata; no native activation or rendering evidence",
                       installed_version=version, version_source="engine://launcher-settings.json#rawVersion",
                       installed_version_file_sha256=digest(engine / "launcher-settings.json"),
                       extensions=dict(sorted(extensions.items())), providers=audit.vfs.providers.report()))
    if source_hashes != {path: digest(ROOT / path) for path in sources}:
        raise SystemExit("Audit sources changed during capture; rerun before retaining this evidence")
    write(args.output / "results.json", dict(schema=1, evidence_layer="Offline source audit; expected failures are retained conversion backlog, not native acceptance",
          baseline_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
          started_utc=started, executed_source_sha256=source_hashes, results=results,
          full_report_reproduction="python -B tools/overhaul/audit_consumers.py <engine> --profile <profile.json> --gate-presentation --output <local-full-report.json>"))
    if not all(row["matches_expected"] for row in results):
        raise SystemExit("An installed-reference result changed; inspect the report rather than updating an expected result blindly")


if __name__ == "__main__":
    main()
