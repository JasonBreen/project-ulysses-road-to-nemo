#!/usr/bin/env python3
"""Create or replace the sticky pull-request scan comment."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

MARKER = "<!-- ulysses-pr-scan -->"


def gh(args: list[str]) -> str:
    result = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", required=True)
    parser.add_argument("--body", type=Path, required=True)
    args = parser.parse_args()
    body = args.body.read_text(encoding="utf-8")
    if MARKER not in body:
        body = MARKER + "\n" + body
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        print(body)
        print("GITHUB_REPOSITORY is unset; comment was not published.")
        return 0
    comments = json.loads(gh(["api", f"repos/{repo}/issues/{args.pr}/comments", "--paginate"]))
    match = next((comment for comment in comments if MARKER in comment.get("body", "")), None)
    payload = json.dumps({"body": body})
    request = ["api", "--method", "PATCH" if match else "POST"]
    request.append(match["url"] if match else f"repos/{repo}/issues/{args.pr}/comments")
    request.extend(["--input", "-"])
    subprocess.run(["gh", *request], input=payload, text=True, check=True)
    print("Updated the scan comment." if match else "Opened the scan comment.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
