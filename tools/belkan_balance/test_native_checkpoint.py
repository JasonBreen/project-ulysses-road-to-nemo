from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.belkan_balance import native_checkpoint as checkpoint


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "minimal_checkpoint.hoi4"
COMMIT = "1" * 40


class NativeCheckpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.root = Path(self.scratch.name)
        self.save_dir = self.root / "profile" / "save games"
        self.save_dir.mkdir(parents=True)
        self.save = self.save_dir / "checkpoint.hoi4"
        shutil.copyfile(FIXTURE, self.save)
        self.manifest = self.root / "payload-manifest.json"
        self.manifest.write_text('{"files":[]}\n', encoding="utf-8")
        self.write_sidecar()

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def write_sidecar(self, manifest_hash: str | None = None) -> None:
        digest = manifest_hash or hashlib.sha256(self.manifest.read_bytes()).hexdigest()
        data = {
            "schema_version": 1,
            "source_commit": COMMIT,
            "payload_manifest": {"file": "payload-manifest.json", "sha256": digest},
            "engine": {
                "version": "Operation Postern v1.19.4.1.99a5 (fixture)",
                "build_id": "26282552",
                "checksum": "f584",
            },
        }
        (self.root / "native-provenance.json").write_text(json.dumps(data), encoding="utf-8")

    def test_extracts_bounded_campaign_economy_and_control_evidence(self) -> None:
        result = checkpoint.capture(self.save, "obs-full-01-war-day-30", "natural")
        self.assertEqual(1, result["schema_version"])
        self.assertEqual("native_observation", result["evidence_class"])
        self.assertEqual(COMMIT, result["source"]["commit"])
        self.assertEqual("1995.3.25.12", result["run"]["date"])
        self.assertEqual("BLK", result["run"]["player_tag"])
        self.assertTrue(result["lifecycle"]["committed"])
        self.assertTrue(result["lifecycle"]["war_active"])
        self.assertEqual(5, result["lifecycle"]["war_weeks"])
        self.assertTrue(result["lifecycle"]["stages"]["one"])
        self.assertEqual("belka_dlp_belkan_war", result["countries"]["BLK"]["focus_tree"])
        self.assertEqual("BLK_dlp_war", result["countries"]["BLK"]["selected_focus"])
        self.assertEqual(100, result["countries"]["BLK"]["economy"]["macro"]["cash"])
        self.assertEqual(64000, result["countries"]["BLK"]["fuel"]["current"])
        self.assertEqual(73.25, result["countries"]["BLK"]["political_power"])
        self.assertTrue(result["control_groups"]["BLK_belkan_war_controls_heart_lands"]["passed"])
        self.assertTrue(result["control_groups"]["BLK_belkan_war_controls_south"]["passed"])
        self.assertIsNone(result["control_groups"]["BLK_belkan_war_controls_ustio"]["passed"])

    def test_output_excludes_private_and_absolute_source_material(self) -> None:
        serialized = json.dumps(checkpoint.capture(self.save, "blk-full", "natural"))
        self.assertNotIn("Private Fixture Name", serialized)
        self.assertNotIn(str(self.root), serialized)
        self.assertNotIn("player_countries", serialized)
        self.assertNotIn("raw", serialized)

    def test_missing_optional_fields_are_null_with_structured_warnings(self) -> None:
        result = checkpoint.capture(self.save, "blk-full", "natural")
        self.assertIsNone(result["countries"]["BLK"]["surrender_progress"])
        self.assertTrue(
            any(
                row["code"] == "missing_optional_field"
                and row["scope"] == "countries.BLK"
                and row["field"] == "surrender_progress"
                for row in result["warnings"]
            )
        )

    def test_rejects_binary_or_malformed_input(self) -> None:
        self.save.write_bytes(b"PK\x03\x04binary")
        with self.assertRaisesRegex(checkpoint.CheckpointError, "uncompressed native text save"):
            checkpoint.capture(self.save, "broken", "natural")
        self.save.write_text('HOI4txt\nplayer="BLK"\ndate="1995.3.25.12"\ncountries={\n', encoding="utf-8")
        with self.assertRaisesRegex(checkpoint.CheckpointError, "Unclosed native block"):
            checkpoint.capture(self.save, "broken", "natural")

    def test_requires_exact_hash_verified_native_provenance(self) -> None:
        (self.root / "native-provenance.json").unlink()
        with self.assertRaisesRegex(checkpoint.CheckpointError, "Missing native-provenance"):
            checkpoint.capture(self.save, "missing", "natural")
        self.write_sidecar("0" * 64)
        with self.assertRaisesRegex(checkpoint.CheckpointError, "manifest hash"):
            checkpoint.capture(self.save, "mismatch", "natural")

    def test_rejects_unbounded_identifiers_and_provenance_labels(self) -> None:
        with self.assertRaisesRegex(checkpoint.CheckpointError, "run-id"):
            checkpoint.capture(self.save, "contains spaces", "natural")
        with self.assertRaisesRegex(checkpoint.CheckpointError, "provenance"):
            checkpoint.capture(self.save, "run", "shortcut")

    def test_cli_writes_json_without_modifying_the_raw_save(self) -> None:
        before = hashlib.sha256(self.save.read_bytes()).hexdigest()
        output = self.root / "evidence" / "checkpoint.json"
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(ROOT / "tools" / "belkan_balance" / "native_checkpoint.py"),
                str(self.save),
                "--run-id",
                "obs-full-01",
                "--provenance",
                "natural",
                "--output",
                str(output),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, hashlib.sha256(self.save.read_bytes()).hexdigest())
        self.assertEqual("obs-full-01", json.loads(output.read_text(encoding="utf-8"))["run"]["id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
