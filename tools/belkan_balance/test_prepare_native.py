from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.belkan_balance import prepare_native


COMMIT = "2" * 40


class PrepareNative(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.root = Path(self.scratch.name)
        self.game = self.root / "game"
        self.normal = self.root / "normal"
        self.source = self.root / "source"
        self.target = self.root / "Project-Ulysses-Native-test"
        self.game.mkdir()
        self.normal.mkdir()
        self.source.mkdir()
        (self.game / "hoi4.exe").write_bytes(b"fixture executable")
        (self.game / "launcher-settings.json").write_text(
            json.dumps(
                {
                    "version": "Operation Postern v1.19.4.1.99a5 (f584)",
                    "rawVersion": "1.19.4.1",
                    "gameDataPath": "normal",
                }
            ),
            encoding="utf-8",
        )
        self.app_manifest = self.root / "appmanifest_394360.acf"
        self.app_manifest.write_text('"buildid"\t\t"26282552"\n', encoding="utf-8")
        (self.normal / "logs").mkdir()
        (self.normal / "save games").mkdir()
        (self.normal / "logs" / "error.log").write_text("before\n", encoding="utf-8")
        (self.normal / "save games" / "normal.hoi4").write_text("protected\n", encoding="utf-8")
        (self.normal / "pdx_settings.json").write_text("{}\n", encoding="utf-8")
        (self.normal / "settings.txt").write_text(
            """graphics={
\tsize={
\t\tx=1920
\t\ty=1080 }
\tgui_scale=1.000000
\tfullScreen=no
\tborderless=yes
}
master_volume=100.000000
music_volume=100.000000
sound_fx_volume=100.000000
ambient_volume=100.000000
voice_volume=100.000000
lastplayer="Private"
lasthost="PrivateHost"
autosave="NEVER"
autosave_tocloud=no
save_career_to_cloud=no
save_as_binary=yes
""",
            encoding="utf-8",
        )
        for directory in ("common", "history", "map", "localisation"):
            (self.source / directory).mkdir()
            (self.source / directory / "fixture.txt").write_text(directory + "\n", encoding="utf-8")
        (self.source / "descriptor.mod").write_text('name="Fixture"\npath="old"\n', encoding="utf-8")

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def test_prepare_copies_exact_payload_and_preserves_normal_profile(self) -> None:
        normal_before = prepare_native.protected_manifest(self.normal)
        result = prepare_native.prepare(
            self.target,
            self.game,
            self.normal,
            self.source,
            self.app_manifest,
            COMMIT,
            3440,
            1440,
        )
        self.assertEqual(normal_before, prepare_native.protected_manifest(self.normal))
        self.assertEqual(COMMIT, result["source_commit"])
        self.assertEqual("26282552", result["build_id"])
        self.assertEqual("f584", result["checksum"])
        self.assertEqual(
            prepare_native.payload_manifest(self.source),
            prepare_native.payload_manifest(result["payload"]),
        )
        self.assertEqual(
            result["profile"].as_posix().encode("utf-8"),
            (result["engine"] / "userdir.txt").read_bytes(),
        )
        self.assertNotIn(b"\r", (result["engine"] / "userdir.txt").read_bytes())
        self.assertNotIn(b"\n", (result["engine"] / "userdir.txt").read_bytes())
        settings = (result["profile"] / "settings.txt").read_text(encoding="utf-8")
        self.assertEqual(settings.count("{"), settings.count("}"))
        self.assertIn("graphics={\n\tsize={\n\t\tx=3440\n\t\ty=1440 }", settings)
        self.assertIn("\tgui_scale=1.000000", settings)
        self.assertIn("\tfullScreen=no", settings)
        self.assertIn("\tborderless=yes", settings)
        self.assertIn('autosave="MONTHLY"', settings)
        self.assertIn("save_as_binary=no", settings)
        self.assertIn('lastplayer="BelkanBalance"', settings)
        self.assertNotIn("PrivateHost", settings)
        self.assertIn("x=3440", settings)
        self.assertIn("y=1440", settings)
        provenance = json.loads((self.target / "native-provenance.json").read_text(encoding="utf-8"))
        manifest = self.target / provenance["payload_manifest"]["file"]
        self.assertEqual(
            provenance["payload_manifest"]["sha256"],
            hashlib.sha256(manifest.read_bytes()).hexdigest(),
        )
        self.assertTrue(json.loads((self.target / "evidence" / "normal-prepare-verification.json").read_text())["clean"])
        launch = json.loads((self.target / "launch.json").read_text(encoding="utf-8"))
        self.assertNotIn("-debug_mode", launch["arguments"])
        self.assertEqual("regular", provenance["session_policy"]["difficulty"])
        self.assertTrue(provenance["session_policy"]["historical_ai"])

    def test_rejects_unsupported_graphics_shape(self) -> None:
        with self.assertRaisesRegex(prepare_native.PreparationError, "graphics size block"):
            prepare_native.disposable_settings("graphics={}\n", 3440, 1440)

    def test_accepts_engine_rewritten_single_line_graphics_size(self) -> None:
        source = "graphics={\n\tsize={ x=1920 y=1080 }\n\tgui_scale=1.000000\n}\n"
        settings = prepare_native.disposable_settings(source, 3440, 1440)
        self.assertEqual(settings.count("{"), settings.count("}"))
        self.assertIn("\tsize={\n\t\tx=3440\n\t\ty=1440 }", settings)
        self.assertIn("\tgui_scale=1.000000", settings)

    def test_rejects_nonpositive_display_dimensions(self) -> None:
        with self.assertRaisesRegex(prepare_native.PreparationError, "positive integers"):
            prepare_native.prepare(
                self.target,
                self.game,
                self.normal,
                self.source,
                self.app_manifest,
                COMMIT,
                0,
                1440,
            )

    def test_refuses_existing_or_overlapping_targets(self) -> None:
        self.target.mkdir()
        with self.assertRaisesRegex(prepare_native.PreparationError, "overwrite"):
            prepare_native.prepare(self.target, self.game, self.normal, self.source, self.app_manifest, COMMIT)
        bad = self.game / "Project-Ulysses-Native-overlap"
        with self.assertRaisesRegex(prepare_native.PreparationError, "overlaps"):
            prepare_native.validate_roots(bad, self.game, self.normal, self.source)

    def test_snapshot_verification_reports_changes_without_restoring(self) -> None:
        prepare_native.prepare(self.target, self.game, self.normal, self.source, self.app_manifest, COMMIT)
        prepare_native.snapshot_normal(self.target, self.normal, "run-01")
        log = self.normal / "logs" / "error.log"
        log.write_text("changed externally\n", encoding="utf-8")
        report = prepare_native.verify_normal(self.target, self.normal, "run-01")
        self.assertFalse(report["clean"])
        self.assertEqual(["logs/error.log"], report["changed"])
        self.assertEqual("changed externally\n", log.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
