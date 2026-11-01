"""Reproduce composed world-start source gates without native game execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, help="Read-only installed script reference")
    parser.add_argument("--baseline", type=Path, help="Read-only immutable mod baseline")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/evidence/world-starts/composed")
    parser.add_argument("--only", nargs="+", help="Run explicitly named affected gates; record this bounded selection")
    args = parser.parse_args()
    reference = ["--reference", str(args.engine.resolve())] if args.engine else []
    python_checks = [
        ("world-starts", ["tools/world_starts/test_world_starts.py", *reference]),
        ("legacy-logistics", ["tools/world_starts/test_legacy_logistics.py", *reference, "--require-integrated-owner"]),
        ("legacy-rosters", ["tools/world_legacy/test_legacy.py"]),
        ("replacement-plans", ["tools/replacements/test_replacements.py"]),
        ("existing-foundations", ["tools/world_foundation/test_foundation.py", *reference]),
        ("anea-foundation", ["tools/anea/test_foundation.py", *reference]),
        ("economy", ["tools/Test-EconomyV2.py"]),
        ("ledger", ["tools/Test-EconomyLedger.py"]),
        ("institutions", ["tools/Test-Institutions.py"]),
        ("shared-owners", ["tools/Test-SharedSystems.py"]),
        ("force-costs", ["tools/Test-ForceUpkeep.py"]),
        ("factions", ["tools/Test-UlyssesFactions.py"]),
        ("partner-generated", ["tools/usean_partners/build.py", "--check", "--require-dependencies"]),
        ("partner-runtime", ["tools/usean_partners/test_content.py", "--require-dependencies"]),
        ("partner-owner-contracts", ["tools/usean_partners/test_integration.py"]),
        ("stories", ["tools/Test-SquadronStories.py"]),
        ("story-art", ["tools/Test-SquadronArt.py"]),
        ("reconstruction-runtime", ["tools/Test-ReconstructionContinuations.py"]),
        ("reconstruction-art", ["tools/Test-ReconstructionAssets.py"]),
        ("macro-generated", ["tools/economy_v2/build.py", "--check"]),
        ("institution-generated", ["tools/institutions/build.py", "--check"]),
        ("registry", ["tools/world_foundation/registry.py", "--check"]),
        ("physical-coverage", ["tools/world_starts/coverage.py", "--check", "--require-integrated-owner"]),
        ("release-inventory", ["tools/world_starts/release_inventory.py", "--check"]),
        ("release-inventory-regressions", ["tools/world_starts/test_release_inventory.py"]),
        ("startup-chronology-regressions", ["tools/Test-StartupChronology.py"]),
        ("startup-chronology", ["tools/compatibility/variant_order.py"]),
        ("overview", ["tools/overhaul/build_overview.py", "--check"]),
        ("decisions", ["tools/Test-DecisionUI.py"]),
        ("focus-canvas", ["tools/Test-FocusScreenRepairs.py"]),
        ("interface", ["tools/Test-InterfaceRepairs.py"]),
        ("screenshot-repairs", ["tools/Test-OverhaulRepairs.py"]),
        ("effective-providers", ["tools/Test-EffectiveDependencies.py"]),
        ("authored-presentation", ["tools/check_presentation_sources.py"]),
        ("presentation-structure", ["tools/Test-PresentationSources.py"]),
        ("authored-assets", ["tools/audit_visual_dependencies.py", "--strict-all"]),
        ("briefing", ["tools/frontend_briefing/validate.py"]),
        ("typography", ["tools/frontend_typography/validate.py"]),
        ("roadmap", ["tools/overhaul/check_release_plan.py"]),
    ]
    checks = [(name, [sys.executable, "-B", *command]) for name, command in python_checks]
    pwsh = shutil.which("pwsh")
    if not pwsh:
        raise SystemExit("PowerShell 7 is required for the composed static suite")
    core = [pwsh, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
            "tools/Test-UlyssesStatic.ps1", "-ModRoot", "mod/2985041246"]
    if args.engine:
        core += ["-ReferenceGameRoot", str(args.engine.resolve())]
    if args.baseline:
        core += ["-BaselineRoot", str(args.baseline.resolve())]
    checks.append(("core", core))
    if args.only:
        unknown = set(args.only) - {name for name, _ in checks}
        if unknown:
            raise SystemExit("Unknown gate names: " + ", ".join(sorted(unknown)))
        checks = [(name, command) for name, command in checks if name in args.only]
    args.output.mkdir(parents=True, exist_ok=True)
    source_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    results = []
    for name, command in checks:
        start = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, env=environment)
        log = (result.stdout + result.stderr).decode("utf-8", errors="replace")
        shown = ["python" if command[0] == sys.executable else "pwsh", *command[1:]]
        for original, replacement in ((ROOT, "<repository>"), (args.engine, "<installed-reference>"),
                                      (args.baseline, "<immutable-baseline>")):
            if original:
                for spelling in (str(original.resolve()), original.resolve().as_posix()):
                    log = log.replace(spelling, replacement)
                    shown = [part.replace(spelling, replacement) for part in shown]
        (args.output / (name + ".txt")).write_text(log, encoding="utf-8", newline="\n")
        results.append(dict(name=name, command=shown, exit_code=result.returncode,
                            seconds=round(time.monotonic() - start, 3), log=name + ".txt"))
        print(name + ": " + ("PASS" if result.returncode == 0 else "FAIL"), flush=True)
    payload = hashlib.sha256()
    for path in sorted((ROOT / "mod/2985041246").rglob("*"), key=lambda path: path.as_posix()):
        if path.is_file():
            payload.update(path.relative_to(ROOT).as_posix().encode() + b"\0" + path.read_bytes())
    end_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if end_head != source_head:
        raise SystemExit("Source commit changed during verification; results were not published as a final candidate")
    report = dict(schema=1, source_head=source_head, selection=args.only or "all",
                  payload_sha256=payload.hexdigest(), payload_hash_rule="Sorted repository-relative POSIX path,NUL,raw bytes for each delivered mod file.",
                  passed=sum(row["exit_code"] == 0 for row in results), failed=sum(row["exit_code"] != 0 for row in results),
                  coverage="Source, primary-reference metadata and offline execution; not native rendering, save/reload, AI pacing or balance acceptance.",
                  native_status="Paused; no native game, desktop control or installation synchronization.",
                  full_conversion_acceptance=False, checks=results)
    (args.output / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(report["failed"] != 0)


if __name__ == "__main__":
    main()
