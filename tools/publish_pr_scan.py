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


def load_comments(payload: str) -> list:
    """Flatten comment pages from `gh api --paginate`.

    `--slurp` returns one JSON array of pages, and each page is a list of
    comment objects. Without `--slurp`, pages are concatenated JSON documents.
    """
    text = payload.strip()
    if not text:
        return []
    documents: list = []
    try:
        documents.append(json.loads(text))
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        index = 0
        while index < len(text):
            while index < len(text) and text[index].isspace():
                index += 1
            if index >= len(text):
                break
            document, index = decoder.raw_decode(text, index)
            documents.append(document)
    comments: list = []
    for document in documents:
        if isinstance(document, dict):
            comments.append(document)
            continue
        if not isinstance(document, list):
            raise ValueError("Unexpected comment payload")
        if document and all(isinstance(item, list) for item in document):
            for page in document:
                comments.extend(page)
            continue
        comments.extend(document)
    return comments


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
    comments = load_comments(gh(["api", f"repos/{repo}/issues/{args.pr}/comments", "--paginate", "--slurp"]))
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
