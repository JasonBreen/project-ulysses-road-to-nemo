#!/usr/bin/env python3
"""Diff-scoped pull-request scan for HOI4 script.

Millennium Dawn posts a validation report on every pull request and fails the
check on common scripting mistakes. This is the smaller Ulysses version of
that pattern: changed script is scanned, annotations are printed for the
files view, and a sticky comment body is written for the publisher.

A clean full-repository duplicate-id check still runs, because a new file can
collide with an id that the diff does not contain.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

MARKER = "<!-- ulysses-pr-scan -->"
MOD_PREFIX = "mod/2985041246/"
LOC_RE = re.compile(r"(?m)^\s*([A-Za-z0-9_.]+):\d*\s+\"")
EVENT_LOC_RE = re.compile(r"(?m)^\s*(?:title|desc|name)\s*=\s*([A-Za-z0-9_.]+)\s*$")
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*")
FOCUS_BLOCKS = {"focus", "shared_focus"}
EVENT_BLOCKS = {
    "country_event",
    "news_event",
    "state_event",
    "unit_leader_event",
    "operative_leader_event",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    path: str
    line: int
    message: str


def strip_comments(text: str) -> str:
    return "\n".join(re.sub(r"#.*", "", line) for line in text.splitlines())


def brace_balance(text: str) -> int | None:
    depth = 0
    for line_number, line in enumerate(strip_comments(text).splitlines(), 1):
        depth += line.count("{") - line.count("}")
        if depth < 0:
            return line_number
    return None if depth == 0 else len(text.splitlines())


def shadowed_else(text: str) -> list[int]:
    """Flag else_if that follows else in the same block. MD reports this.

    The marker stays when the else body closes and depth returns to it. It
    drops when the containing scope closes, or when a new if starts there.
    """
    hits: list[int] = []
    depth = 0
    else_depth: set[int] = set()
    for line_number, raw in enumerate(strip_comments(text).splitlines(), 1):
        code = raw.strip()
        if re.match(r"else\s*=", code):
            else_depth.add(depth)
        elif re.match(r"else_if\s*=", code) and depth in else_depth:
            hits.append(line_number)
        elif re.match(r"if\s*=", code):
            else_depth.discard(depth)
        next_depth = depth + code.count("{") - code.count("}")
        if next_depth < depth:
            else_depth = {item for item in else_depth if item <= next_depth}
        depth = next_depth
    return hits


def definition_ids(text: str, kind: str) -> list[tuple[int, str]]:
    """Return ids of focus or event definitions, not nested id parameters.

    An event definition is a top-level event block. A nested
    `country_event = { id = ... }` effect is not one. Focus ids are direct
    fields of `focus` and `shared_focus` blocks, so a power-balance or
    province id inside a reward is not a focus id.
    """
    names = FOCUS_BLOCKS if kind == "focus" else EVENT_BLOCKS
    cleaned = strip_comments(text)
    depth = 0
    active: set[int] = set()
    found: list[tuple[int, str]] = []
    index = 0
    line = 1
    length = len(cleaned)
    while index < length:
        char = cleaned[index]
        if char == "\n":
            line += 1
            index += 1
            continue
        if char.isspace():
            index += 1
            continue
        if char == '"':
            index += 1
            while index < length and cleaned[index] != '"':
                if cleaned[index] == "\n":
                    line += 1
                index += 1
            index = min(index + 1, length)
            continue
        if char == "{":
            depth += 1
            index += 1
            continue
        if char == "}":
            depth -= 1
            active = {item for item in active if item <= depth}
            index += 1
            continue
        match = IDENT.match(cleaned, index)
        if not match:
            index += 1
            continue
        word = match.group(0)
        word_line = line
        cursor = match.end()
        while cursor < length and cleaned[cursor].isspace():
            if cleaned[cursor] == "\n":
                line += 1
            cursor += 1
        if cursor >= length or cleaned[cursor] != "=":
            index = match.end()
            continue
        cursor += 1
        while cursor < length and cleaned[cursor].isspace():
            if cleaned[cursor] == "\n":
                line += 1
            cursor += 1
        if cursor < length and cleaned[cursor] == "{" and word in names:
            depth += 1
            if kind == "focus" or depth == 1:
                active.add(depth)
            index = cursor + 1
            continue
        if word == "id" and depth in active:
            value = IDENT.match(cleaned, cursor)
            if value:
                found.append((word_line, value.group(0)))
                index = value.end()
                continue
        if cursor < length and cleaned[cursor] != "{":
            value = IDENT.match(cleaned, cursor)
            index = value.end() if value else cursor
            continue
        index = cursor
    return found


def loc_index(mod: Path) -> set[str]:
    keys: set[str] = set()
    root = mod / "localisation"
    if not root.exists():
        return keys
    for path in root.rglob("*.yml"):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        keys.update(LOC_RE.findall(text))
    return keys


def duplicate_ids(mod: Path, changed: set[str]) -> list[Finding]:
    seen: dict[tuple[str, str], tuple[str, int]] = {}
    findings: list[Finding] = []
    for folder, kind in (("common/national_focus", "focus"), ("events", "event")):
        root = mod / folder
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.txt")):
            relative = path.relative_to(mod.parents[1]).as_posix()
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            for line_number, ident in definition_ids(text, kind):
                key = (kind, ident)
                if key in seen:
                    previous, previous_line = seen[key]
                    if relative in changed or previous in changed:
                        findings.append(Finding("error", relative, line_number, f"Duplicate {kind} id {ident}; also at {previous}:{previous_line}"))
                else:
                    seen[key] = (relative, line_number)
    return findings


def scan_changed(mod: Path, repo: Path, changed: list[str]) -> list[Finding]:
    findings = duplicate_ids(mod, set(changed))
    keys = loc_index(mod)
    for relative in changed:
        path = repo / relative
        if not path.is_file():
            continue
        if relative.endswith(".yml"):
            raw = path.read_bytes()
            if not raw.startswith(b"\xef\xbb\xbf"):
                findings.append(Finding("error", relative, 1, "Localization file is missing a UTF-8 BOM"))
            continue
        if not relative.endswith(".txt"):
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        broken = brace_balance(text)
        if broken is not None:
            findings.append(Finding("error", relative, broken, "Unbalanced braces"))
        for line in shadowed_else(text):
            findings.append(Finding("error", relative, line, "else_if follows else in the same block"))
        if relative.startswith(MOD_PREFIX + "events/"):
            for line_number, raw in enumerate(text.splitlines(), 1):
                match = EVENT_LOC_RE.match(re.sub(r"#.*", "", raw))
                if match and match.group(1) not in keys:
                    findings.append(Finding("error", relative, line_number, f"Missing localization key {match.group(1)}"))
        if "/national_focus/" in relative:
            for line_number, ident in definition_ids(text, "focus"):
                if "." in ident:
                    continue
                for key in (ident, ident + "_desc"):
                    if key not in keys:
                        findings.append(Finding("error", relative, line_number, f"Missing localization key {key}"))
        for line_number, raw in enumerate(text.splitlines(), 1):
            if re.search(r"(?i)\blog\s*=", re.sub(r"#.*", "", raw)):
                findings.append(Finding("warning", relative, line_number, "Debug log = left in script"))
    return findings


def comment_body(findings: list[Finding], changed: list[str]) -> str:
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    if not changed:
        summary = "No changed mod script in this pull request. Static validation still runs in its own check."
    elif errors:
        summary = f"{len(errors)} error(s), {len(warnings)} warning(s) in {len(changed)} changed file(s)."
    else:
        summary = f"Clean. {len(warnings)} warning(s) in {len(changed)} changed file(s)."
    lines = [
        MARKER,
        "### Pull request scan",
        "",
        "This comment updates in place, in the same way Millennium Dawn publishes its validation report. It checks changed HOI4 script for a missing localization BOM, unbalanced braces, an `else_if` after `else`, missing keys on new events and focuses, and duplicate focus or event ids in the whole mod.",
        "",
        f"**Result:** {summary}",
        "",
    ]
    shown = errors + warnings
    if shown:
        lines.append("| Severity | File | Line | Finding |")
        lines.append("| --- | --- | ---: | --- |")
        for item in shown[:40]:
            lines.append(f"| {item.severity} | `{item.path}` | {item.line} | {item.message} |")
        if len(shown) > 40:
            lines.append("")
            lines.append(f"{len(shown) - 40} further findings were omitted from this comment and kept in the check log.")
    else:
        lines.append("No findings.")
    lines.append("")
    lines.append("Static validation does not launch HOI4. A clean scan is not native play.")
    lines.append("")
    return "\n".join(lines)


def annotations(findings: list[Finding]) -> str:
    commands = []
    for item in findings:
        level = "error" if item.severity == "error" else "warning"
        message = item.message.replace("\n", " ")
        commands.append(f"::{level} file={item.path},line={item.line}::{message}")
    return "\n".join(commands) + ("\n" if commands else "")


def changed_files(repo: Path, base: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    names = []
    for line in result.stdout.splitlines():
        relative = line.strip().replace("\\", "/")
        if relative.startswith(MOD_PREFIX) and relative.endswith((".txt", ".yml")):
            names.append(relative)
    return names


def write_outputs(findings: list[Finding], changed: list[str], comment_out: Path | None, annotations_out: Path | None) -> None:
    body = comment_body(findings, changed)
    notes = annotations(findings)
    if comment_out:
        comment_out.parent.mkdir(parents=True, exist_ok=True)
        comment_out.write_text(body, encoding="utf-8")
    if annotations_out:
        annotations_out.parent.mkdir(parents=True, exist_ok=True)
        annotations_out.write_text(notes, encoding="utf-8")
    sys.stdout.write(notes)
    errors = [item for item in findings if item.severity == "error"]
    print(f"PR scan: {len(errors)} error(s), {len(findings) - len(errors)} warning(s), {len(changed)} changed file(s).")


class ScanTests(unittest.TestCase):
    def test_detectors(self) -> None:
        self.assertIsNone(brace_balance("a = {\n\tb = { 1 }\n}\n"))
        self.assertIsNotNone(brace_balance("a = {\n"))
        self.assertEqual([], shadowed_else("if = { limit = { always = yes }\nx = 1\n}\nelse_if = { limit = { always = no }\nx = 2\n}\nelse = { x = 3 }\n"))
        self.assertEqual([3], shadowed_else("if = { limit = { always = yes } x = 1 }\nelse = { x = 2 }\nelse_if = { limit = { always = no } x = 3 }\n"))
        multiline = "if = {\n\tlimit = { always = yes }\n\tx = 1\n}\nelse = {\n\tx = 2\n}\nelse_if = {\n\tlimit = { always = no }\n\tx = 3\n}\n"
        self.assertEqual([8], shadowed_else(multiline))
        restarted = "if = {\n\tx = 1\n}\nelse = {\n\tx = 2\n}\nif = {\n\tx = 3\n}\nelse_if = {\n\tx = 4\n}\n"
        self.assertEqual([], shadowed_else(restarted))

    def test_missing_key_and_bom(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            mod = repo / "mod" / "2985041246"
            event = mod / "events"
            event.mkdir(parents=True)
            loc = mod / "localisation" / "english"
            loc.mkdir(parents=True)
            (event / "sample.txt").write_text("country_event = {\n\tid = sample.1\n\ttitle = sample.1.t\n\tdesc = sample.1.d\n\toption = {\n\t\tname = sample.1.a\n\t}\n}\n", encoding="utf-8")
            (loc / "sample_l_english.yml").write_bytes("l_english:\n sample.1.t:0 \"Title\"\n".encode("utf-8"))
            changed = [
                "mod/2985041246/events/sample.txt",
                "mod/2985041246/localisation/english/sample_l_english.yml",
            ]
            findings = scan_changed(mod, repo, changed)
            messages = [item.message for item in findings]
            self.assertTrue(any("UTF-8 BOM" in message for message in messages))
            self.assertTrue(any("sample.1.d" in message for message in messages))
            self.assertTrue(any("sample.1.a" in message for message in messages))

    def test_definition_ids_ignore_nested_parameters(self) -> None:
        event = "country_event = {\n\tid = sample.1\n\toption = {\n\t\tcountry_event = { id = sample.2 days = 7 }\n\t}\n}\nshared_focus = { id = INLINE_FOCUS x = 1 }\n"
        self.assertEqual(["sample.1"], [ident for _, ident in definition_ids(event, "event")])
        self.assertEqual(["INLINE_FOCUS"], [ident for _, ident in definition_ids(event, "focus")])
        sap = Path(__file__).resolve().parents[1] / "mod" / "2985041246" / "common" / "national_focus" / "SAP_pre_belkan_war.txt"
        idents = [ident for _, ident in definition_ids(sap.read_text(encoding="utf-8-sig"), "focus")]
        self.assertIn("sap_1991_parliamentary_elections", idents)
        self.assertNotIn("SAP_power_balance", idents)
        geb = sap.with_name("GEB_pre_belkan_war.txt")
        geb_ids = [ident for _, ident in definition_ids(geb.read_text(encoding="utf-8-sig"), "focus")]
        self.assertIn("GEB_the_meike_line", geb_ids)
        self.assertFalse(any(ident.isdigit() for ident in geb_ids))

    def test_nested_focus_id_does_not_require_localization(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            mod = repo / "mod" / "2985041246"
            focus_dir = mod / "common" / "national_focus"
            focus_dir.mkdir(parents=True)
            loc = mod / "localisation" / "english"
            loc.mkdir(parents=True)
            (focus_dir / "sample.txt").write_text(
                "shared_focus = {\n\tid = REAL_FOCUS\n\tcompletion_reward = {\n\t\tadd_power_balance_value = { id = SAP_power_balance value = -0.05 }\n\t\tprovince = { id = 1835 }\n\t}\n}\n",
                encoding="utf-8",
            )
            (loc / "sample_l_english.yml").write_bytes("\ufeffl_english:\n REAL_FOCUS:0 \"Title\"\n REAL_FOCUS_desc:0 \"Desc\"\n".encode("utf-8"))
            relative = "mod/2985041246/common/national_focus/sample.txt"
            messages = [item.message for item in scan_changed(mod, repo, [relative])]
            self.assertFalse(any("SAP_power_balance" in message or "1835" in message for message in messages))

    def test_duplicate_definition_is_still_reported(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            mod = repo / "mod" / "2985041246"
            focus_dir = mod / "common" / "national_focus"
            focus_dir.mkdir(parents=True)
            (focus_dir / "a.txt").write_text(
                "shared_focus = {\n\tid = SAME\n\tcompletion_reward = {\n\t\tadd_power_balance_value = { id = SAP_power_balance }\n\t}\n}\n",
                encoding="utf-8",
            )
            (focus_dir / "b.txt").write_text("shared_focus = {\n\tid = SAME\n}\n", encoding="utf-8")
            changed = "mod/2985041246/common/national_focus/b.txt"
            findings = duplicate_ids(mod, {changed})
            self.assertTrue(any(item.message.startswith("Duplicate focus id SAME;") for item in findings))
            self.assertFalse(any("SAP_power_balance" in item.message for item in findings))

    def test_comment_pages(self) -> None:
        from publish_pr_scan import load_comments

        slurped = json.dumps([[{"body": "<!-- ulysses-pr-scan --> one"}], [{"body": "two"}]])
        self.assertEqual(["<!-- ulysses-pr-scan --> one", "two"], [item["body"] for item in load_comments(slurped)])
        separate = '[{"body": "a"}]\n[{"body": "b"}]'
        self.assertEqual(["a", "b"], [item["body"] for item in load_comments(separate)])
        self.assertEqual([], load_comments(""))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="")
    parser.add_argument("--comment-out", type=Path)
    parser.add_argument("--annotations-out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(ScanTests)
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        return 0 if result.wasSuccessful() else 1
    repo = Path(__file__).resolve().parents[1]
    mod = repo / "mod" / "2985041246"
    changed = changed_files(repo, args.base) if args.base else []
    findings = scan_changed(mod, repo, changed)
    write_outputs(findings, changed, args.comment_out, args.annotations_out)
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
