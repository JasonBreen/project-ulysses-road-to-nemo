#!/usr/bin/env python3
"""Mutation checks proving continuation definitions and localization are enforced."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod" / "2985041246"
VALIDATOR = ROOT / "tools" / "validate_campaign.py"


def run_validator(mod_root: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--mod-root", str(mod_root)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        raise AssertionError("validator accepted a deliberately mutated campaign")
    return result.stdout + result.stderr


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ulysses-contract-mutation-") as temporary:
        temporary_mod = Path(temporary) / "2985041246"
        shutil.copytree(MOD, temporary_mod)

        decision_path = temporary_mod / "common" / "decisions" / "ac_continuation_decisions.txt"
        decision_text = decision_path.read_text(encoding="utf-8-sig")
        decision_path.write_text(
            decision_text.replace(
                "ac_postwar_reconstruction_program = {",
                "ac_postwar_reconstruction_program_removed = {",
                1,
            ),
            encoding="utf-8",
        )
        output = run_validator(temporary_mod)
        if "decision not declared in campaign file: ac_postwar_reconstruction_program" not in output:
            raise AssertionError("validator did not reject a removed continuation decision")

        shutil.rmtree(temporary_mod)
        shutil.copytree(MOD, temporary_mod)
        localization_path = temporary_mod / "localisation" / "english" / "country_BLK_continuation_l_english.yml"
        localization_text = localization_path.read_text(encoding="utf-8-sig")
        localization_path.write_text(
            "\n".join(
                line for line in localization_text.splitlines()
                if not line.lstrip().startswith("ac_postwar_local_recovery_desc:")
            ) + "\n",
            encoding="utf-8",
        )
        output = run_validator(temporary_mod)
        if "missing localization pair: ac_postwar_local_recovery" not in output:
            raise AssertionError("validator did not reject a removed continuation localization")

    print("Campaign contract mutation regressions passed: removed decision and localization were rejected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
