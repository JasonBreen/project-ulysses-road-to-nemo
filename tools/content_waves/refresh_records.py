"""Refresh the shared review records that enumerate every country, decision or event.

Content waves add focuses, decisions and events, so three records owned by other
packages go stale and fail CI:

* tools/world_foundation/country_registry.json (per-country focus counts, input digest);
* docs/evidence/decision-rows/consumer-bounds.json and index.html (every decision row);
* docs/evidence/event-style/measurements.json and gallery.html (every event text field).

Only their text outputs are written. Their PNG review sheets are left as committed,
because PNG compression differs between platforms; the script reports whether
their pixels still match. The event-style generator sorts event files with the
platform's path ordering, so on non-Windows hosts it is run with Windows
(case-insensitive) ordering, which reproduces the committed record exactly.

Usage: python -B tools/content_waves/refresh_records.py [--check]
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def registry(check):
    path = ROOT / "tools/world_foundation/registry.py"
    report = ROOT / "tools/world_foundation/country_registry.json"
    if check:
        result = subprocess.run([sys.executable, "-B", str(path), "--check"], cwd=ROOT, capture_output=True, text=True)
        return [report.relative_to(ROOT).as_posix()] if result.returncode else []
    before = report.read_bytes() if report.exists() else b""
    subprocess.run([sys.executable, "-B", str(path), "--output", str(report)], cwd=ROOT, check=True, capture_output=True)
    return [report.relative_to(ROOT).as_posix()] if report.read_bytes() != before else []


def write_text_outputs(outputs, check, same_png):
    stale = []
    for path, data in outputs.items():
        path = Path(path)
        current = path.read_bytes() if path.exists() else b""
        if path.suffix == ".png":
            if not same_png(current, data):
                print(f"note: {path.relative_to(ROOT).as_posix()} pixels differ; PNG sheets are not rewritten")
            continue
        if current.replace(b"\r\n", b"\n") != data:
            stale.append(path.relative_to(ROOT).as_posix())
            if not check:
                path.write_bytes(data)
    return stale


def decision_rows(check):
    sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools/decision_row_art")]
    from event_picture_fit.fit import same_review_png
    module = runpy.run_path(str(ROOT / "tools/decision_row_art/render_review.py"), run_name="content_waves_decision_rows")
    outputs, _ = module["build"]()
    return write_text_outputs(outputs, check, same_review_png)


def event_style_child(check):
    if os.name != "nt":
        import pathlib
        # Match the Windows CI runner, which compares paths case-insensitively.
        pathlib.PurePath._str_normcase = property(lambda self: str(self).lower())
    sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools/event_style")]
    from event_picture_fit.fit import same_review_png
    module = runpy.run_path(str(ROOT / "tools/event_style/review.py"), run_name="content_waves_event_style")
    outputs = {module["OUT"] / name: data for name, data in module["generated"]().items()}
    stale = write_text_outputs(outputs, check, same_review_png)
    for name in stale:
        print("STALE " + name)


def event_style(check):
    args = [sys.executable, "-B", str(Path(__file__)), "--event-style-child"] + (["--check"] if check else [])
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    for line in result.stdout.splitlines():
        if line.startswith("note:"):
            print(line)
    return [line[6:] for line in result.stdout.splitlines() if line.startswith("STALE ")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--event-style-child", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.event_style_child:
        event_style_child(args.check)
        return
    stale = registry(args.check) + decision_rows(args.check) + event_style(args.check)
    if args.check and stale:
        raise SystemExit("Stale shared records: " + ", ".join(stale))
    print(("Shared records consistent" if args.check else "Shared records refreshed") + (": " + ", ".join(stale) if stale else ""))


if __name__ == "__main__":
    main()
