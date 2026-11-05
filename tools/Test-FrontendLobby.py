"""Country-selection lobby restyle (phase 1): dispositions, bindings, review,
the hover-name override and the phase-2 capture hook. Static only."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/frontend_briefing'))
import build  # noqa: E402


class FrontendLobby(unittest.TestCase):
    def run_tool(self, *args):
        result = subprocess.run([sys.executable, '-B', *args], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_validator_style_and_review_agree(self):
        self.run_tool('tools/frontend_briefing/validate.py')
        self.run_tool('tools/frontend_briefing/style_gui.py', '--check')
        self.run_tool('tools/frontend_briefing/render_review.py', '--check')

    def test_dispositions_cover_the_screen_and_counts(self):
        record = json.loads((ROOT / 'tools/frontend_briefing/lobby_sprites.json').read_text())['sprites']
        counts = {kind: sum(r['disposition'] == kind for r in record) for kind in ('restyle', 'hide', 'keep_engine')}
        self.assertEqual({'restyle': 8, 'hide': 4, 'keep_engine': 43}, counts)
        # Interactive controls wait for the engine capture; none is restyled blind.
        for row in record:
            if any(part in row['sprite'] for part in ('button', 'checkbox', 'slider', 'scroll')):
                self.assertEqual('keep_engine', row['disposition'], row['sprite'])

    def test_capture_contract_reads_only_kept_engine_definitions(self):
        with tempfile.TemporaryDirectory() as folder:
            engine = Path(folder) / 'game'; (engine / 'interface').mkdir(parents=True); (engine / 'gfx').mkdir()
            (engine / 'interface/core.gfx').write_text(
                'spriteTypes = {\n spriteType = { name = "GFX_play_button" texturefile = "gfx/play.dds" noOfFrames = 3 effectFile = "gfx/FX/buttonstate.lua" }\n'
                ' corneredTileSpriteType = { name = "GFX_tiled_frontend_upper_bar" texturefile = "gfx/bar.dds" size = { x = 64 y = 64 } borderSize = { x = 8 y = 8 } }\n}\n')
            from PIL import Image
            Image.new('RGBA', (90, 30)).save(engine / 'gfx/play.dds')
            target = Path(folder) / 'contract.json'
            contract = build.capture_contract(engine, target)
            self.assertEqual(json.loads(target.read_text()), contract)
            play = contract['sprites']['GFX_play_button']
            self.assertEqual((3, [90, 30], 'spriteType'), (play['frames'], play['texture_size'], play['kind']))
            self.assertNotIn('GFX_tiled_frontend_upper_bar', contract['sprites'])  # restyled, not kept
            self.assertIn('GFX_generic_checkbox', contract['missing'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
