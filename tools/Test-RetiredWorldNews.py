"""Actual compatibility handlers for retired Earth news; no native execution."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod/2985041246"
SOURCE = ROOT / "tools/usea_expansion"
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(ROOT / "tools"))
from script import get, parse
from build_retired_mechanics import build

parser = argparse.ArgumentParser()
parser.add_argument("--reference", type=Path)
args, rest = parser.parse_known_args()


def literal_retired_calls(text):
    # Token inspection deliberately does not assert that this small AST reader
    # supports every tagged country-color/history grammar. Quoted strings and
    # comments are atomic; the actual compatibility handlers are parsed below.
    tokens = [token for token in re.findall(r'"(?:\\.|[^"\\])*"|\#[^\n]*|[{}=]|[^\s{}=#]+', text)
              if not token.startswith('#')]
    calls = []
    for index, token in enumerate(tokens):
        if token.lower() not in ("news_event", "country_event") or tokens[index+1:index+2] != ['=']:
            continue
        value = tokens[index+2] if index+2 < len(tokens) else ''
        if re.fullmatch(r'news\.\d+', value.strip('"')):
            calls.append(value.strip('"'))
            continue
        if value != '{':
            continue
        depth = 1
        cursor = index + 3
        while cursor < len(tokens) and depth:
            current = tokens[cursor]
            if current == '{': depth += 1
            elif current == '}': depth -= 1
            elif depth == 1 and current.lower() == 'id' and tokens[cursor+1:cursor+2] == ['=']:
                value = tokens[cursor+2] if cursor+2 < len(tokens) else ''
                if re.fullmatch(r'news\.\d+', value.strip('"')):
                    calls.append(value.strip('"'))
            cursor += 1
    return calls


class RetiredWorldNews(unittest.TestCase):
    def test_compatibility_ids_equal_the_independently_captured_union(self):
        source = json.loads((SOURCE / "retired_news_sources.json").read_text())
        rows = json.loads((SOURCE / "retired_event_contract.json").read_text())
        row = next(row for row in rows if row["file"] == "NewsEvents.txt")
        expected = set(source["mod_original_event_ids"]) | set(source["installed_reference_event_ids"])
        self.assertEqual(expected, set(row["events"]))
        self.assertEqual(len(expected), source["union_event_count"])
        self.assertEqual(len(row["events"]), len(set(row["events"])))
        self.assertEqual("news_event", row["event_kind"])
        tree = parse((MOD / "events/NewsEvents.txt").read_text())
        actual = [get(node, "id") for kind, _, node in tree if kind == "news_event"]
        self.assertEqual(expected, set(actual))
        self.assertEqual(len(actual), len(expected))

    def test_every_actual_handler_is_hidden_triggered_and_effect_free(self):
        tree = parse((MOD / "events/NewsEvents.txt").read_text())
        for kind, _, node in tree:
            if kind == "add_namespace":
                continue
            self.assertEqual("news_event", kind)
            self.assertEqual({"id", "hidden", "is_triggered_only", "immediate"}, {key for key, _, _ in node})
            self.assertEqual("yes", get(node, "hidden"))
            self.assertEqual("yes", get(node, "is_triggered_only"))
            self.assertEqual([], get(node, "immediate"))

    def test_authored_routes_do_not_call_the_retired_world_news(self):
        calls = []
        for folder in ("common", "events", "history"):
            for path in sorted((MOD / folder).rglob("*.txt")):
                if path == MOD / "events/NewsEvents.txt":
                    continue
                text = path.read_text(encoding="utf-8-sig")
                calls.extend((path.relative_to(MOD).as_posix(), ident) for ident in literal_retired_calls(text))
        self.assertEqual([], calls)

    def test_call_scan_preserves_quoted_ids_and_ignores_comments_and_display_text(self):
        source = '# news_event={id=news.3}\nlog="news_event={id=news.4}"\neffect={news_event={id="news.1"} country_event={id=news.2} news_event=news.5 country_event="news.6"}'
        self.assertEqual(["news.1", "news.2", "news.5", "news.6"], literal_retired_calls(source))

    def test_inline_comments_are_separate_even_without_whitespace(self):
        self.assertEqual(['news.1'], literal_retired_calls('news_event = news.1# comment'))
        self.assertEqual([], literal_retired_calls('log = yes# news_event={id=news.3}'))
        self.assertEqual(['news.2'], literal_retired_calls('news_event={id=news.2# comment\n}'))
        self.assertEqual([], literal_retired_calls('log="yes# news_event={id=news.4}"'))

    def test_generator_has_only_explicit_retirement_ownership(self):
        expected = {"events/" + row["file"] for row in json.loads((SOURCE / "retired_event_contract.json").read_text())}
        expected |= {"common/scripted_effects/ac_retired_mechanics.txt", "common/on_actions/ac_retired_mechanics.txt",
                     "common/decisions/categories/ac_retired_mechanics.txt", "common/decisions/ac_retired_mechanics.txt"}
        self.assertEqual(expected, set(build()))
        subprocess.run([sys.executable, "-B", str(SOURCE / "build_retired_mechanics.py"), "--check"],
                       cwd=ROOT, check=True, capture_output=True)

    @unittest.skipUnless(args.reference, "No installed read-only reference supplied; captured metadata is not native acceptance")
    def test_primary_hidden_news_and_reference_ids_match_the_capture(self):
        source = json.loads((SOURCE / "retired_news_sources.json").read_text())
        for row in source["hidden_news_primary_examples"]:
            path = args.reference / row["source"].removeprefix("engine://")
            self.assertEqual(row["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            events = {get(node, "id"): node for kind, _, node in parse(path.read_text(encoding="utf-8-sig"))
                      if kind == "news_event" and isinstance(node, list)}
            self.assertEqual("yes", get(events[row["id"]], "hidden"))
        path = args.reference / "events/NewsEvents.txt"
        actual = {get(node, "id") for kind, _, node in parse(path.read_text(encoding="utf-8-sig"))
                  if kind in ("country_event", "news_event") and isinstance(node, list)}
        self.assertEqual(set(source["installed_reference_event_ids"]), actual)


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + rest, verbosity=2)
