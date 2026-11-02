"""Static contract checks for the 1991 starting-setup data cleanup.

These read the shipped scripts offline; they are not the HOI4 engine. They
cover the history-data gaps recorded in docs/PORT_1_19.md and
docs/NEXT_TASKS.md: ideology popularities summing to 100, placeholder
``xxx`` values in starting equipment/portrait/division-name data, the
Shilage/Delarus shared-leader conflict, and ship/division name groups for
countries whose starting fleets and templates reference them.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod/2985041246"


def text(relative):
    return (MOD / relative).read_text(encoding="utf-8-sig", errors="replace")


def fleet_ship_types(tag):
    types = set()
    units = MOD / "history/units"
    for path in units.glob(f"{tag}_navy*.txt"):
        types.update(re.findall(r"definition\s*=\s*(\w+)", path.read_text(encoding="utf-8-sig", errors="replace")))
    return types


class HistoryDataCleanupTests(unittest.TestCase):
    def test_reviewed_source_update_receipts_match_protected_baselines(self):
        updates = json.loads((ROOT / "tools/history_data_cleanup_updates.json").read_text(encoding="utf-8"))["files"]
        expected = {
            "mod/2985041246/history/countries/BLK - Belka.txt",
            "mod/2985041246/history/countries/NEC - Nordennavic.txt",
            "mod/2985041246/history/countries/SHI - Shilage.txt",
            "mod/2985041246/history/units/PBL_land.txt",
            "mod/2985041246/history/units/SYC_land.txt",
            "mod/2985041246/history/units/SYC_ws_land.txt",
        }
        self.assertEqual(expected, set(updates))

        protected = []
        for relative, key in (
            ("tools/air_program/preserved_sources.json", "sources"),
            ("tools/land_program/preserved_sources.json", "protected_sources_sha256"),
            ("tools/naval_program/preserved_sources.json", "sources"),
        ):
            protected.append(json.loads((ROOT / relative).read_text(encoding="utf-8"))[key])

        for relative, row in updates.items():
            old_hash = row["old_normalized_sha256"]
            new_hash = row["new_normalized_sha256"]
            self.assertNotEqual(old_hash, new_hash, relative)
            self.assertTrue(row["reason"], relative)
            for manifest in protected:
                self.assertEqual(old_hash, manifest[relative], relative)
            data = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual(new_hash, hashlib.sha256(data).hexdigest(), relative)

    def test_popularities_sum_to_100(self):
        for path in sorted((MOD / "history/countries").glob("*.txt")):
            match = re.search(r"set_popularities\s*=\s*\{(.*?)\}", path.read_text(encoding="utf-8-sig", errors="replace"), re.S)
            if not match:
                continue
            values = [float(v) for _, v in re.findall(r"(\w+)\s*=\s*([\d.]+)", match.group(1))]
            self.assertAlmostEqual(100.0, sum(values), places=2, msg=f"{path.name}: popularities sum to {sum(values)}")

    def test_no_xxx_placeholders_in_starting_setup(self):
        offenders = []
        for folder in ("history/countries", "history/units", "common/characters"):
            for path in sorted((MOD / folder).rglob("*.txt")):
                for number, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1):
                    if re.search(r'(icon\s*=\s*"xxx"|large\s*=\s*"xxx"|division_names_group\s*=\s*xxx\b)', line):
                        offenders.append(f"{path.relative_to(MOD)}:{number}: {line.strip()}")
        self.assertEqual([], offenders)

    def test_pbl_syc_division_name_groups_are_defined(self):
        defined = set()
        for path in (MOD / "common/units/names_divisions").glob("*.txt"):
            defined.update(re.findall(r"(?m)^([A-Za-z0-9_]+)\s*=\s*\{", path.read_text(encoding="utf-8-sig", errors="replace")))
        for tag in ("PBL", "SYC"):
            referenced = set(re.findall(r"division_names_group\s*=\s*(\S+)", text(f"history/units/{tag}_land.txt")))
            self.assertTrue(referenced, tag)
            # GER_* groups ship with the game itself; every other referenced
            # group must be defined by the mod.
            own = {group for group in referenced if not group.startswith("GER_")}
            self.assertLessEqual(own, defined, f"{tag}: {sorted(own - defined)}")

    def test_shilage_does_not_recruit_delarus_leader(self):
        history = text("history/countries/SHI - Shilage.txt")
        recruited = re.findall(r"recruit_character\s*=\s*(\S+)", history)
        self.assertNotIn("DEL_artur_clarkson", recruited)
        self.assertIn("SHI_ac_government_office", recruited)
        governments = text("common/characters/ac_starting_governments.txt")
        self.assertRegex(governments, r"(?m)^SHI_ac_government_office\s*=\s*\{")

    def test_sapin_and_fato_ship_name_groups_cover_starting_fleets(self):
        for tag in ("SAP", "FAT"):
            names = text(f"common/units/names/00_{tag}_names.txt")
            sections = set(re.findall(r"(?m)^\t(\w+)\s*=\s*\{", names))
            needed = fleet_ship_types(tag)
            self.assertTrue(needed, tag)
            self.assertLessEqual(needed, sections, f"{tag}: missing {sorted(needed - sections)}")
            for section in needed:
                block = re.search(rf"(?m)^\t{section}\s*=\s*\{{(.*?)^\t\}}", names, re.S)
                self.assertIsNotNone(block, f"{tag}/{section}")
                self.assertIn("unique", block.group(1), f"{tag}/{section}")

    def test_belkan_variant_icons_resolve_to_mod_sprites(self):
        gfx = "\n".join(path.read_text(encoding="utf-8-sig", errors="replace") for path in (MOD / "interface").glob("*.gfx"))
        sprites = set(re.findall(r'name\s*=\s*"?(GFX_[A-Za-z0-9_]+)"?', gfx))
        history = text("history/countries/BLK - Belka.txt")
        for icon in re.findall(r'icon\s*=\s*"([^"]+)"', history):
            self.assertNotEqual("xxx", icon)
            if icon.startswith("GFX_BLK_"):
                self.assertIn(icon, sprites, icon)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=MOD)
    args, remaining = parser.parse_known_args()
    MOD = args.mod_root.resolve()
    unittest.main(argv=[sys.argv[0]] + remaining)
