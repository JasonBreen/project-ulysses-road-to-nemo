"""Run the seams test and every Usea Depth package test (tools/usea_depth/*/test_*.py).

Static and offline only. Each test file runs in its own interpreter so packages
can keep separate content modules.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    tests = [HERE / "test_seams.py"] + sorted(HERE.glob("*/test_*.py"))
    failed = []
    for test in tests:
        result = subprocess.run([sys.executable, "-B", str(test)], cwd=ROOT, capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
        name = test.relative_to(ROOT).as_posix()
        print(("PASS: " if result.returncode == 0 else "FAIL: ") + name, flush=True)
        if result.returncode:
            print((result.stdout + result.stderr)[-6000:], flush=True)
            failed.append(name)
    print("Usea Depth: %d test files, %d failed." % (len(tests), len(failed)))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
