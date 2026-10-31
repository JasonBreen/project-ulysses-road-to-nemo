"""Static contract for the 1997 Usean rebellion. Not a HOI4 launch."""

from __future__ import annotations

import argparse
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod" / "2985041246"

CONTENT = (
    "events/ac_usean_rebellion.txt",
    "common/on_actions/ac_usean_rebellion.txt",
    "common/ideas/ac_usean_rebellion.txt",
    "common/decisions/ac_usean_rebellion.txt",
    "common/decisions/categories/ac_usean_rebellion.txt",
    "common/national_focus/ac_usean_rebellion.txt",
)
FOCUSES = (
    "FCU_ur_acknowledge",
    "FCU_ur_unified_command",
    "FCU_ur_scarface_sortie",
    "FCU_ur_stand_down",
    "FCU_ur_keep_mobilized",
    "FCU_ur_assessment",
)
EVENTS = ("ac_ur.1", "ac_ur.2", "ac_ur.3", "ac_ur.4")
FORBIDDEN = (
    "transfer_state",
    "add_core_of",
    "remove_core_of",
    "set_state_owner",
    "set_province_controller",
    "set_politics",
    "create_country_leader",
    "promote_character",
    "retire_country_leader",
    "add_popularity",
)
ISOLATED = (
    "events/ac_ucw.txt",
    "common/on_actions/ac_ucw.txt",
    "common/on_actions/ac_anea.txt",
    "events/ac_anea.txt",
    "common/national_focus/FCU.txt",
    "common/national_focus/ERU.txt",
    "common/decisions/ac_ucw.txt",
)


def read(relative: str) -> str:
    return (MOD / relative).read_text(encoding="utf-8-sig")


def loc_keys() -> set[str]:
    text = read("localisation/english/ac_usean_rebellion_l_english.yml")
    return set(re.findall(r"(?m)^\s*([A-Za-z0-9_.]+):\d+\s+\"", text))


class UseanRebellion(unittest.TestCase):
    def test_contract_files_and_flags(self) -> None:
        blob = "\n".join(read(path) for path in CONTENT)
        for token in ("ac_ur_skully_recorded", "ac_ur_coup_started", "ac_ur_coup_defeated", "ac_ur_coup_prolonged"):
            self.assertIn(token, blob)
        for token in FORBIDDEN:
            self.assertNotIn(token, blob, token)
        for path in ISOLATED:
            self.assertNotIn("ac_ur_", read(path), path)
        opening = read("common/national_focus/FCU_opening.txt")
        for focus in FOCUSES:
            self.assertIn(f"shared_focus = {focus}", opening)
            self.assertEqual(1, len(re.findall(rf"(?m)^\s*id\s*=\s*{focus}\s*$", read("common/national_focus/ac_usean_rebellion.txt"))))

    def test_events_and_localization(self) -> None:
        events = read("events/ac_usean_rebellion.txt")
        keys = loc_keys()
        for event in EVENTS:
            self.assertEqual(1, len(re.findall(rf"(?m)^\s*id\s*=\s*{re.escape(event)}\s*$", events)), event)
            self.assertIn(f"{event}.t", keys)
            self.assertIn(f"{event}.d", keys)
        for key in ("ac_ur.1.a", "ac_ur.2.a", "ac_ur.3.a", "ac_ur.3.b", "ac_ur.4.a"):
            self.assertIn(key, keys)
        self.assertIn("Provisional gameplay", read("localisation/english/ac_usean_rebellion_l_english.yml"))
        raw = (MOD / "localisation/english/ac_usean_rebellion_l_english.yml").read_bytes()
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf"))
        for focus in FOCUSES:
            self.assertIn(focus, keys)
            self.assertIn(f"{focus}_desc", keys)
        for decision in ("ac_ur_record_southern_district", "ac_ur_commit_scarface", "ac_ur_restore_administration"):
            self.assertIn(decision, keys)
            self.assertIn(f"{decision}_desc", keys)
        for idea in ("ac_ur_coup_strain", "ac_ur_unified_command", "ac_ur_scarface_sortie"):
            self.assertIn(idea, keys)
            self.assertIn(f"{idea}_desc", keys)

    def test_belkan_chain_is_untouched_by_the_skully_event(self) -> None:
        events = "\n".join(re.sub(r"#.*", "", line) for line in read("events/ac_usean_rebellion.txt").splitlines())
        self.assertNotIn("belka", events.lower())
        on_action = read("common/on_actions/ac_usean_rebellion.txt")
        self.assertNotIn("belka", on_action.lower())
        self.assertIn("date > 1995.12.30", on_action)
        self.assertIn("date > 1997.5.29", on_action)
        self.assertIn("original_tag = ERU", on_action)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", default="")
    unittest.main(argv=["Test-UseanRebellion"])


if __name__ == "__main__":
    main()
